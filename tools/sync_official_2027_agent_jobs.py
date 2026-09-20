#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync current-campus Agent/AI-application engineering candidates from first-party recruitment endpoints.

This tool is discovery-only: it only calls company-owned recruitment APIs/portals listed in
market/jobs/official-2027-campus-sources.json. It never imports JD text from aggregators.
Portal-only companies remain in the coverage matrix for manual official-site review.
"""

from __future__ import annotations

import json
import os
import tempfile
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urljoin, urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "market/jobs/official-2027-campus-sources.json"
VERIFIED_INDEX = ROOT / "market/jobs/official-company-role-index.json"
MANUAL_ROLE_SEEDS = ROOT / "market/jobs/official-first-party-role-seeds.json"
VERIFIED_INDEX_MD = ROOT / "market/jobs/official-company-role-index.md"
SCAN_POOL_MD = ROOT / "market/jobs/company-scan-pool.md"
OUT_MD = ROOT / "market/jobs/official-2027-agent-jobs.generated.md"
OUT_JSON = ROOT / "market/jobs/official-2027-agent-jobs.generated.json"
BROWSER_CACHE = ROOT / "market/jobs/official-2027-browser-discovery.generated.json"
FEISHU_CACHE = ROOT / "market/jobs/official-2027-feishu-discovery.generated.json"
MOKA_CACHE = ROOT / "market/jobs/official-2027-moka-discovery.generated.json"
TEMP_ROOT = Path(os.environ.get("RUNNER_TEMP") or tempfile.gettempdir())
XIAOMI_NODE_CACHE = Path(os.environ.get("XIAOMI_CACHE") or (TEMP_ROOT / "xiaomi-2027-campus.json"))
BYTEDANCE_NODE_CACHE = Path(os.environ.get("BYTEDANCE_CACHE") or (TEMP_ROOT / "bytedance-campus.json"))

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
TIMEOUT = 12
CACHE_MAX_AGE_SECONDS = 6 * 60 * 60
TARGET_TITLE_HINT_RE = re.compile(
    r"(?:agent|智能体|rag|harness|runtime|coding|"
    r"ai\s*(?:应用|全栈|开发|研发|工程|平台|infra|devops|builder|软件|系统|技术|后端|前端)|"
    r"大模型(?:应用|开发|研发|工程|平台)|fde)",
    re.I,
)


def likely_target_title(title: str) -> bool:
    return bool(TARGET_TITLE_HINT_RE.search(title or ""))


@dataclass
class Job:
    company: str
    title: str
    job_id: str
    location: str
    category: str
    department: str
    description: str
    requirements: str
    official_url: str
    official_api: str
    cycle_evidence: str


@dataclass
class SourceResult:
    company: str
    mode: str
    portal: str
    status: str
    fetched: int
    matched: int
    error: str = ""


def txt(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return ", ".join(txt(x) for x in v if x is not None)
    if isinstance(v, dict):
        return " ".join(txt(x) for x in v.values())
    return str(v).strip()


def blob(job: Job) -> str:
    return " ".join([
        job.title, job.category, job.department, job.description, job.requirements
    ]).lower()


def is_agent_related(job: Job, keywords: list[str], body_signals: list[str]) -> bool:
    title = job.title.lower()
    body = " ".join([job.category, job.department, job.description, job.requirements]).lower()
    # A strong signal in the title is sufficient. In the body, require multiple
    # Agent/application mechanisms so generic "AI应用探索/AI工具" boilerplate
    # on ordinary engineering jobs does not become a false positive.
    if any(k.lower() in title for k in keywords):
        return True
    hits = {k.lower() for k in body_signals if k.lower() in body}
    return len(hits) >= 2


def looks_engineering(job: Job, signals: list[str]) -> bool:
    title = job.title.lower()
    return any(s.lower() in title for s in signals)


def training_heavy(job: Job, signals: list[str]) -> bool:
    title = job.title.lower()
    if any(k in title for k in ["算法", "研究员", "research scientist", "scientist"]):
        return True
    body = " ".join([job.description, job.requirements]).lower()
    hits = {s.lower() for s in signals if s.lower() in body}
    # Protect explicit Agent systems/infra roles that mention training only as
    # surrounding context; generic R&D roles dominated by 2+ training signals
    # are outside this engineering JD library.
    protected = any(k in title for k in ["agent", "智能体", "harness", "runtime", "infra", "ai应用", "ai 应用", "大模型应用", "coding"])
    return (not protected) and len(hits) >= 2


def discover_api_candidates(portal: str) -> list[str]:
    """Best-effort discovery of current API paths from an official JS recruitment portal.

    This is diagnostic only. A discovered endpoint is never treated as a JD until
    a company adapter explicitly understands its request/response contract.
    """
    base = portal.split("#", 1)[0]
    try:
        r = requests.get(base, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except Exception:
        return []

    bodies = [r.text]
    scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r.text, flags=re.I)
    for src in scripts[:16]:
        try:
            js = requests.get(urljoin(base, src), headers=HEADERS, timeout=TIMEOUT)
            if js.ok:
                bodies.append(js.text[:5_000_000])
        except Exception:
            continue

    candidates: set[str] = set()
    patterns = [
        r'https?://[^"\'\s]{1,240}',
        r'["\']([^"\']{0,80}(?:/api/|api/|/recruit/)[^"\']{0,180})["\']',
    ]
    for body in bodies:
        for pattern in patterns:
            for m in re.finditer(pattern, body, flags=re.I):
                raw = m.group(1) if m.lastindex else m.group(0)
                raw = raw.replace("\\/", "/")
                low = raw.lower()
                if any(k in low for k in ("job", "position", "recruit", "opportun")):
                    candidates.add(raw[:260])
    return sorted(candidates)[:30]


def is_hard_excluded(job: Job, excludes: list[str]) -> bool:
    title = job.title.lower()
    return any(k.lower() in title for k in excludes)


def campusish(job: Job) -> bool:
    s = " ".join([
        job.category, job.cycle_evidence, job.title,
        job.description, job.requirements,
    ]).lower()
    return any(k in s for k in [
        "校招", "校园", "应届", "毕业生", "毕业", "2027",
        "graduate", "campus", "new grad", "new-grad", "new graduate",
        "fresh grad", "fresh graduate", "graduates welcome",
        "new graduates welcome", "应届生优先", "欢迎应届",
    ])


def clean(s: str, limit: int = 1600) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:limit]


def cache_is_fresh(payload: dict) -> bool:
    raw = txt(payload.get("generated_at"))
    if not raw:
        return False
    try:
        stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return False
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - stamp.astimezone(timezone.utc)).total_seconds()
    return -300 <= age <= CACHE_MAX_AGE_SECONDS


def get_json(url: str, *, params=None, headers=None) -> Any:
    h = dict(HEADERS)
    if headers:
        h.update(headers)
    r = requests.get(url, params=params, headers=h, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def post_json(url: str, *, payload=None, headers=None) -> Any:
    h = dict(HEADERS)
    h["Content-Type"] = "application/json"
    if headers:
        h.update(headers)
    r = requests.post(url, json=payload or {}, headers=h, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def post_form(url: str, *, data=None, headers=None) -> Any:
    h = dict(HEADERS)
    h["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    if headers:
        h.update(headers)
    r = requests.post(url, data=data or {}, headers=h, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()




def fetch_xiaomi(src: dict) -> list[Job]:
    """Read Xiaomi campus jobs fetched by the official Node ATSX adapter.

    Xiaomi's official ATSX endpoint is first-party but its WAF currently treats
    Python requests differently from browser/Node fetch on GitHub runners.
    The workflow therefore runs tools/fetch_xiaomi_2027.mjs first.
    """
    cache = XIAOMI_NODE_CACHE
    if not cache.exists():
        raise RuntimeError("Xiaomi official Node adapter output missing")
    payload = json.loads(cache.read_text(encoding="utf-8"))
    out: list[Job] = []
    for j in payload.get("jobs") or []:
        out.append(Job(
            src["company"], txt(j.get("title")), txt(j.get("job_id")),
            txt(j.get("location")), txt(j.get("category")), txt(j.get("department")),
            txt(j.get("description")), txt(j.get("requirements")),
            txt(j.get("official_url")), txt(j.get("official_api")),
            txt(j.get("cycle_evidence")),
        ))
    return out


def fetch_bytedance(src: dict) -> list[Job]:
    cache = BYTEDANCE_NODE_CACHE
    if not cache.exists():
        raise RuntimeError("ByteDance official Node adapter output missing")
    payload = json.loads(cache.read_text(encoding="utf-8"))
    out: list[Job] = []
    for j in payload.get("jobs") or []:
        out.append(Job(
            src["company"], txt(j.get("title")), txt(j.get("job_id")),
            txt(j.get("location")), txt(j.get("category")), txt(j.get("department")),
            txt(j.get("description")), txt(j.get("requirements")),
            txt(j.get("official_url")), txt(j.get("official_api")),
            txt(j.get("cycle_evidence")),
        ))
    return out


def fetch_sangfor_campus(src: dict) -> list[Job]:
    """Enumerate Sangfor's official campus API without relying on its slow SPA."""
    api = "https://hr.sangfor.com/api/Jobs"
    headers = {
        **HEADERS,
        "Origin": "https://hr.sangfor.com",
        "Referer": "https://hr.sangfor.com/schoolRecruitment",
    }
    out: list[Job] = []
    page = 1
    total = None
    while page <= 100:
        payload = {
            "channelId": 101,
            "page": page,
            "pageSize": 100,
            "departmentId": 0,
            "functionId": 0,
            "kw": "",
            "locationId": 0,
            "workPlaceId": 0,
        }
        data = post_json(api, payload=payload, headers=headers)
        root = data.get("data") or data.get("Data") or data
        rows: list[dict[str, Any]] = []
        if isinstance(root, list):
            rows = [x for x in root if isinstance(x, dict)]
        elif isinstance(root, dict):
            for key in ("list", "rows", "items", "jobs", "data", "records"):
                value = root.get(key)
                if isinstance(value, list):
                    rows = [x for x in value if isinstance(x, dict)]
                    break
            if total is None:
                for key in ("total", "count", "Total", "Count"):
                    if root.get(key) is not None:
                        try:
                            total = int(root.get(key))
                        except Exception:
                            pass
                        break
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id") or j.get("jobId") or j.get("job_id"))
            title = txt(j.get("jobName") or j.get("title") or j.get("name"))
            out.append(Job(
                src["company"], title, jid,
                txt(j.get("workPlace") or j.get("workplace") or j.get("location")),
                txt(j.get("functionName") or j.get("category") or "2027校园招聘"),
                txt(j.get("departmentName") or j.get("department")),
                _strip_html(j.get("jobDescription") or j.get("description") or j.get("duty")),
                _strip_html(j.get("jobRequirement") or j.get("requirement") or j.get("qualifications")),
                src.get("search_url") or src.get("portal") or "https://hr.sangfor.com/schoolRecruitment",
                api,
                "深信服2027届校园招聘",
            ))
        if len(rows) < 100 or (total is not None and page * 100 >= total):
            break
        page += 1
    return out


def fetch_kuaishou(src: dict) -> list[Job]:
    """Enumerate Kuaishou's official 2027 project; list API already returns full JD."""
    base = "https://campus.kuaishou.cn"
    list_api = base + "/recruit/campus/e/api/v1/open/positions/simple"
    project = str(src.get("project_code") or "20271779425607")
    headers = {
        **HEADERS,
        "Referer": src["portal"],
        "Content-Type": "application/json",
    }
    out: list[Job] = []
    page = 1
    while page <= 20:
        payload = {
            "recruitSubProjectCodes": [project],
            "pageSize": 500,
            "pageNum": page,
            "positionNatureCode": "fulltime",
        }
        r = requests.post(list_api, json=payload, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        body = r.json()
        if body.get("code") not in (None, 0):
            raise RuntimeError(f"Kuaishou API code={body.get('code')} message={body.get('message')}")
        result = body.get("result") or {}
        rows = result.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            code = txt(j.get("code"))
            locations = j.get("workLocationDicts") or []
            city = " / ".join(
                txt(x.get("name")) for x in locations if isinstance(x, dict) and x.get("name")
            )
            out.append(Job(
                src["company"],
                txt(j.get("name")),
                jid,
                city,
                "2027校招正式",
                txt(j.get("departmentName") or j.get("positionCategoryName")),
                txt(j.get("description")),
                txt(j.get("positionDemand")),
                f"{base}/recruit/campus/e/#/campus/job-info/{jid}?code={code}&recruitSubProjectCodes={project}",
                list_api,
                f"快手官方2027项目 {project}",
            ))
        pages = int(result.get("pages") or 0)
        total = int(result.get("total") or 0)
        if (pages and page >= pages) or (total and page * 500 >= total) or len(rows) < 500:
            break
        page += 1
    return out


def fetch_baidu(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        data = post_form(
            src["api"],
            data={"recruitType": "GRADUATE", "pageSize": 20, "curPage": page, "projectType": "", "keyWord": ""},
            headers={"Referer": "https://talent.baidu.com/jobs/list?projectType=1"},
        )
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            pid = txt(j.get("jobId") or j.get("postId"))
            out.append(Job(
                src["company"], txt(j.get("name")), pid,
                txt(j.get("workPlace")), "校招", txt(j.get("serviceType")),
                txt(j.get("workContent")), txt(j.get("serviceCondition")),
                f"https://talent.baidu.com/jobs/detail/GRADUATE/{pid}", src["api"],
                "百度当前校园招聘=2027届",
            ))
        total = int(d.get("total") or 0)
        if page * 20 >= total:
            break
        page += 1
    return out


def fetch_tencent(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        params = {
            "timestamp": int(time.time() * 1000), "attrId": "1",
            "pageIndex": page, "pageSize": 100, "language": "zh-cn", "area": "cn",
        }
        data = get_json(src["api"], params=params)
        d = data.get("Data") or {}
        rows = d.get("Posts") or []
        if not rows:
            break
        for j in rows:
            pid = txt(j.get("PostId"))
            out.append(Job(
                src["company"], txt(j.get("RecruitPostName")), pid,
                txt(j.get("LocationName")), "校招", txt(j.get("BGName")),
                txt(j.get("Responsibility")), txt(j.get("Requirement")),
                f"https://careers.tencent.com/jobdesc.html?postId={pid}", src["api"],
                "腾讯当前校园招聘",
            ))
        total = int(d.get("Count") or 0)
        if page * 100 >= total:
            break
        page += 1
    return out


def fetch_meituan(src: dict) -> list[Job]:
    out = []
    offset = 0
    while offset <= 5000:
        data = get_json(src["api"], params={"limit": 100, "offset": offset, "jobType": 2})
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                txt(j.get("city")), "校招", txt(j.get("orgName")),
                txt(j.get("responsibility")), txt(j.get("requirement")),
                f"https://zhaopin.meituan.com/job-detail?jobId={jid}", src["api"],
                "美团当前校园招聘",
            ))
        total = int(d.get("total") or 0)
        if offset + 100 >= total:
            break
        offset += 100
    return out


def fetch_netease(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        data = post_json(src["api"], payload={"currentPage": page, "pageSize": 100},
                         headers={"Origin": "https://hr.163.com"})
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                txt(j.get("workPlaceName")), txt(j.get("recruitTypeName")), txt(j.get("deptName")),
                txt(j.get("requirement")), "学历: " + txt(j.get("educationName")),
                f"https://hr.163.com/position/detail.html?id={jid}", src["api"],
                txt(j.get("recruitTypeName")),
            ))
        pages = int(d.get("pages") or 0)
        if pages and page >= pages:
            break
        page += 1
    return out


def fetch_bilibili(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        data = get_json(src["api"], params={"page": page, "pageSize": 100})
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                txt(j.get("city")), txt(j.get("type")), txt(j.get("department")),
                txt(j.get("description")), txt(j.get("requirement")),
                f"https://jobs.bilibili.com/position/{jid}", src["api"],
                txt(j.get("type")),
            ))
        total = int(d.get("total") or 0)
        if page * 100 >= total:
            break
        page += 1
    return out


def fetch_didi(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        data = get_json(src["api"], params={"page": page, "pageSize": 100, "language": "zh"})
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                txt(j.get("city")), txt(j.get("recruitType")), txt(j.get("department")),
                txt(j.get("description")), txt(j.get("requirement")),
                f"https://talent.didiglobal.com/position/{jid}", src["api"],
                txt(j.get("recruitType")),
            ))
        total = int(d.get("total") or 0)
        if page * 100 >= total:
            break
        page += 1
    return out


def fetch_pdd(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        data = get_json(src["api"], params={"page": page, "pageSize": 100})
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                txt(j.get("city")), txt(j.get("type")), txt(j.get("department")),
                txt(j.get("description")), txt(j.get("requirement")),
                f"https://careers.pinduoduo.com/position/{jid}", src["api"],
                txt(j.get("type")),
            ))
        total = int(d.get("total") or 0)
        if page * 100 >= total:
            break
        page += 1
    return out


def fetch_huawei(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        payload = {"pageIndex": page, "pageSize": 100, "positionType": "", "keyWord": ""}
        data = post_json(src["api"], payload=payload)
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("positionId"))
            out.append(Job(
                src["company"], txt(j.get("positionName")), jid,
                txt(j.get("workLocation")), txt(j.get("positionType")), txt(j.get("department")),
                txt(j.get("description")), txt(j.get("requirement")),
                f"https://career.huawei.com/reccampportal/campus/position/{jid}", src["api"],
                txt(j.get("positionType")),
            ))
        total = int(d.get("total") or 0)
        if page * 100 >= total:
            break
        page += 1
    return out


def fetch_tencent_campus(src: dict) -> list[Job]:
    api = "https://join.qq.com/api/v1/position/searchPosition"
    detail_api = "https://join.qq.com/api/v1/jobDetails/getJobDetailsByPostId"
    headers = {**HEADERS, "Content-Type": "application/json", "Referer": "https://join.qq.com/post.html"}
    out, seen = [], set()
    page = 1
    while page <= 50:
        body = {
            "keyword": "", "pageIndex": page, "pageSize": 50,
            "recruitType": "40003", "bgIds": [], "productIds": [],
            "categoryIds": [], "workLocations": [], "timestamp": "",
        }
        r = requests.post(api, json=body, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        d = (r.json().get("data") or {})
        rows = d.get("positionList") or []
        if not rows:
            break
        for row in rows:
            pid = txt(row.get("postId") or row.get("id"))
            if not pid or pid in seen:
                continue
            seen.add(pid)
            project = txt(row.get("recruitLabelName") or row.get("projectName") or "校招")
            if "实习" in project:
                continue
            title = txt(row.get("positionTitle"))
            if not likely_target_title(title):
                continue
            try:
                detail = get_json(
                    detail_api,
                    params={"timestamp": int(time.time() * 1000), "postId": pid},
                    headers={"Referer": "https://join.qq.com/post.html"},
                )
                dd = detail.get("data") or {}
            except Exception:
                dd = {}
            desc = txt(dd.get("desc") or dd.get("topicDetail") or dd.get("introduction"))
            req = txt(dd.get("request") or dd.get("topicRequirement"))
            out.append(Job(
                src["company"], title, pid,
                txt(row.get("workCities")), project, txt(row.get("bgs")),
                desc, req,
                f"https://join.qq.com/post_detail.html?postId={pid}", api,
                project or "腾讯官方校园招聘",
            ))
        if page * 50 >= int(d.get("count") or 0):
            break
        page += 1
    return out


def fetch_meituan_campus(src: dict) -> list[Job]:
    api = "https://zhaopin.meituan.com/api/official/job/getJobList"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Referer": "https://zhaopin.meituan.com/web/campus",
        "Origin": "https://zhaopin.meituan.com",
        "X-Requested-With": "XMLHttpRequest",
    }
    out, seen = [], set()
    for page in range(1, 30):
        body = {
            "page": {"pageNo": page, "pageSize": 100},
            "jobShareType": "1", "keywords": "", "cityList": [],
            "department": [], "jfJgList": [],
            "jobType": [{"code": "1", "subCode": []}],
            "typeCode": [], "specialCode": [],
        }
        r = requests.post(api, json=body, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        d = r.json().get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            if str(j.get("jobType") or "") not in ("", "1"):
                continue
            jid = txt(j.get("jobUnionId"))
            if not jid or jid in seen:
                continue
            seen.add(jid)
            city = " / ".join(
                txt(x.get("name")) for x in (j.get("cityList") or [])
                if isinstance(x, dict) and x.get("name")
            )
            out.append(Job(
                src["company"], txt(j.get("name")), jid, city,
                "校招正式", txt(j.get("departmentName") or j.get("jobCategoryName")),
                txt(j.get("jobDuty") or j.get("desc")), txt(j.get("jobRequirement")),
                f"https://zhaopin.meituan.com/web/position/detail?jobUnionId={jid}&highlightType=campus",
                api, "美团官方当前校园招聘正式岗（届别需主库复核）",
            ))
        p = d.get("page") or {}
        if page >= int(p.get("totalPage") or page):
            break
    return out


def fetch_jd_campus(src: dict) -> list[Job]:
    api = "https://campus.jd.com/api/wx/position/page"
    headers = {**HEADERS, "Content-Type": "application/json", "Referer": "https://campus.jd.com/"}
    out = []
    for recruit_type in ("present", "talent"):
        page, seen = 0, set()
        while page < 30:
            payload = {
                "pageSize": 50, "pageIndex": page,
                "parameter": {
                    "positionName": "", "planIdList": [], "jobDirectionCodeList": [],
                    "workCityCodeList": [], "positionDeptList": [],
                },
            }
            r = requests.post(f"{api}?type={recruit_type}", json=payload, headers=headers, timeout=TIMEOUT)
            r.raise_for_status()
            d = r.json().get("body") or {}
            rows = d.get("items") or []
            if not rows:
                break
            for j in rows:
                pid = txt(j.get("publishId") or j.get("reqId"))
                key = f"{recruit_type}:{pid}"
                if not pid or key in seen:
                    continue
                seen.add(key)
                cities = []
                for req in j.get("requirementVoList") or []:
                    city = txt(req.get("workCity"))
                    if city and city not in cities:
                        cities.append(city)
                out.append(Job(
                    src["company"], txt(j.get("positionName")), key,
                    " / ".join(cities), "校招正式", txt(j.get("positionDept")),
                    txt(j.get("workContent")), txt(j.get("qualification")),
                    f"https://campus.jd.com/#/details?type={recruit_type}&id={pid}",
                    api, f"京东官方校园招聘 {recruit_type}（届别需主库复核）",
                ))
            total = int(d.get("totalNumber") or 0)
            page += 1
            if page * 50 >= total:
                break
    return out


def fetch_pdd_campus(src: dict) -> list[Job]:
    root = "https://careers.pddglobalhr.com/api/careers/api/recruit/position"
    list_api, detail_api = root + "/list", root + "/detail"
    headers = {
        **HEADERS, "Content-Type": "application/json;charset=UTF-8",
        "Referer": "https://careers.pddglobalhr.com/campus/grad",
    }
    session = requests.Session()
    session.headers.update(headers)
    rows, page = [], 1
    while page <= 30:
        r = session.post(list_api, json={"page": page, "pageSize": 100, "t": None}, timeout=TIMEOUT)
        r.raise_for_status()
        body = r.json()
        if not body.get("success"):
            raise RuntimeError(body.get("errorMsg") or "PDD official API success=false")
        d = body.get("result") or {}
        got = d.get("list") or []
        if not got:
            break
        rows.extend(got)
        if len(rows) >= int(d.get("total") or len(rows)):
            break
        page += 1

    out = []
    for row in rows:
        pid = txt(row.get("id"))
        if not pid:
            continue
        try:
            r = session.post(detail_api, json={"id": pid, "t": None}, timeout=TIMEOUT)
            r.raise_for_status()
            body = r.json()
            detail = (body.get("result") or {}) if body.get("success") else {}
        except Exception:
            detail = {}
        year = txt(detail.get("graduationYear") or row.get("graduationYear"))
        recruit_type = txt(detail.get("recruitTypeName") or row.get("recruitTypeName"))
        out.append(Job(
            src["company"], txt(row.get("name")), pid,
            txt(detail.get("workLocationName") or row.get("workLocationName") or row.get("workLocation")),
            "校招正式" + (f" {year}届" if year else ""), txt(row.get("departmentName")),
            txt(detail.get("jobDuty") or row.get("jobDuty")),
            txt(detail.get("serveRequirement") or row.get("serveRequirement")),
            txt(detail.get("shareUrl")) or f"https://careers.pddglobalhr.com/campus/grad/detail?positionId={pid}",
            list_api, f"拼多多官方校招 {year + '届' if year else '届别待复核'} {recruit_type}",
        ))
    return out


def fetch_oppo_campus(src: dict) -> list[Job]:
    api = "https://careers.oppo.com/openapi/position/pageNew"
    headers = {
        **HEADERS, "Content-Type": "application/json", "Tenant-Id": "1000",
        "Referer": "https://careers.oppo.com/university/oppo/recruitment/post",
    }
    out, page = [], 1
    while page <= 20:
        payload = {
            "pageNum": page, "pageSize": 100, "positionName": "",
            "projectList": [], "positionTypeList": [], "workCityCodeList": [],
        }
        r = requests.post(api, json=payload, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        d = r.json().get("data") or {}
        rows = d.get("records") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("idProjPosition") or j.get("idRecruitPosition"))
            project = txt(j.get("projectName"))
            out.append(Job(
                src["company"], txt(j.get("positionName") or j.get("projectPositionName")), jid,
                txt(j.get("workCityName")), txt(j.get("positionTypeName") or "校招"),
                project, txt(j.get("positionDesc")), txt(j.get("positionRequire")),
                f"https://careers.oppo.com/university/oppo/campus/post/{jid}",
                api, project or "OPPO官方校园招聘（届别待复核）",
            ))
        total = int(d.get("total") or len(rows))
        if page * 100 >= total:
            break
        page += 1
    return out


def fetch_lenovo(src: dict) -> list[Job]:
    api = "https://talent.lenovo.com.cn/gateway/jobBase/list"
    headers = {
        **HEADERS, "Referer": "https://talent.lenovo.com.cn/position",
        "portal-type": "PC",
    }
    out, page = [], 1
    while page <= 30:
        data = get_json(api, params={"pageNum": page, "pageSize": 50}, headers=headers)
        d = data.get("result") or {}
        rows = d.get("rows") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("jobName")), jid, txt(j.get("workPlace")),
                txt(j.get("recruitType") or j.get("jobType") or "校招待复核"),
                txt(j.get("jobCategory")), txt(j.get("cont") or j.get("jobDesc")),
                txt(j.get("requirement")),
                f"https://talent.lenovo.com.cn/position/detail?id={jid}",
                api, "联想官方招聘（2027归属需复核）",
            ))
        if page * 50 >= int(d.get("total") or 0):
            break
        page += 1
    return out


def fetch_sf(src: dict) -> list[Job]:
    api = "https://campus.sf-express.com/api/web/position/query"
    out, page = [], 1
    while page <= 20:
        data = get_json(api, params={"pageNum": page, "pageSize": 50}, headers={"Referer": "https://campus.sf-express.com/positionList"})
        rows = data.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("positionName")), jid,
                txt(j.get("demandCity")), "校招", txt(j.get("positionTypeName") or j.get("orgSourceName")),
                txt(j.get("postDuty")), txt(j.get("jobRequirement")),
                f"https://campus.sf-express.com/#/postDetail/{jid}",
                api, "顺丰官方校园招聘（届别待复核）",
            ))
        if page * 50 >= int(data.get("total") or 0):
            break
        page += 1
    return out


def fetch_alibaba_campus(src: dict) -> list[Job]:
    origin = "https://campus-talent.alibaba.com"
    batch_id = int(src.get("batch_id") or 100000540002)
    page_url = f"{origin}/campus/position?batchId={batch_id}"
    session = requests.Session()
    session.headers.update({**HEADERS, "Referer": page_url, "Content-Type": "application/json"})
    warm = session.get(page_url, timeout=TIMEOUT)
    warm.raise_for_status()
    csrf = session.cookies.get("XSRF-TOKEN")
    if not csrf:
        raise RuntimeError("Alibaba campus XSRF-TOKEN missing")
    out, page = [], 1
    while page <= 30:
        payload = {
            "batchId": batch_id, "pageIndex": page, "pageSize": 50,
            "channel": "campus_group_official_site", "language": "zh",
        }
        r = session.post(f"{origin}/position/search?_csrf={csrf}", json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        content = r.json().get("content") or {}
        rows = content.get("datas") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                " / ".join(txt(x) for x in (j.get("workLocations") or [])),
                "校招", txt(j.get("departmentName") or j.get("categoryName")),
                txt(j.get("description")), txt(j.get("requirement")),
                f"{origin}/campus/position-detail?positionId={jid}",
                f"{origin}/position/search",
                f"阿里官方校园招聘 batchId={batch_id}（2027归属需复核）",
            ))
        total = int(content.get("totalCount") or content.get("total") or 0)
        if page * 50 >= total:
            break
        page += 1
    return out


def _strip_html(value: Any) -> str:
    s = txt(value)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</(?:p|div|li|h[1-6]|tr|td|th|ul|ol|section)>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return (
        s.replace("&nbsp;", " ").replace("&amp;", "&")
        .replace("&lt;", "<").replace("&gt;", ">")
        .replace("&quot;", '"').replace("&#39;", "'")
        .strip()
    )


def fetch_xiaohongshu_2027(src: dict) -> list[Job]:
    api = "https://job.xiaohongshu.com/websiterecruit/position/pageQueryPosition"
    detail_api = "https://job.xiaohongshu.com/websiterecruit/position/queryPositionDetail"
    headers = {**HEADERS, "Origin": "https://job.xiaohongshu.com", "Referer": "https://job.xiaohongshu.com/campus"}
    out: list[Job] = []
    page = 1
    while page <= 30:
        data = post_json(
            api,
            payload={
                "positionName": "", "pageNum": page, "pageSize": 100,
                "recruitType": "campus", "jobProjects": ["red_star_27"],
            },
            headers=headers,
        )
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for row in rows:
            pid = txt(row.get("positionId"))
            list_title = txt(row.get("positionName"))
            if not likely_target_title(list_title):
                continue
            detail = {}
            if pid:
                try:
                    detail_payload = get_json(detail_api, params={"positionId": pid}, headers=headers)
                    detail = detail_payload.get("data") or {}
                except Exception:
                    detail = {}
            title = txt(detail.get("positionName") or list_title)
            out.append(Job(
                src["company"], title, pid,
                txt(detail.get("workplace") or row.get("workplace")),
                "2027校园招聘", txt(detail.get("positionType") or row.get("jobType")),
                txt(detail.get("duty") or row.get("duty")),
                txt(detail.get("qualification") or row.get("qualification")),
                f"https://job.xiaohongshu.com/campus/position/{pid}" if pid else src["portal"],
                api,
                "小红书2027校园招聘 / red_star_27",
            ))
        total_pages = int(d.get("totalPage") or 0)
        if total_pages and page >= total_pages:
            break
        if len(rows) < 100:
            break
        page += 1
    return out


def fetch_bilibili_2027(src: dict) -> list[Job]:
    root = "https://jobs.bilibili.com"
    token_url = root + "/api/auth/v1/csrf/token"
    list_api = root + "/api/campus/position/positionList"
    base_headers = {
        **HEADERS,
        "Content-Type": "application/json",
        "X-AppKey": "ops.ehr-api.auth",
        "X-UserType": "2",
        "Referer": root + "/campus/positions",
    }
    token_payload = get_json(token_url, headers=base_headers)
    token = txt(token_payload.get("data"))
    if not token:
        raise RuntimeError("Bilibili official CSRF token missing")
    headers = {**base_headers, "X-CSRF": token, "Cookie": f"X-CSRF={token}"}
    out: list[Job] = []
    page = 1
    while page <= 50:
        data = post_json(
            list_api,
            payload={
                "pageSize": 100, "pageNum": page, "positionName": "",
                "postCode": [], "postCodeList": [], "workLocationList": [],
                "workTypeList": [3], "positionTypeList": [],
                "deptCodeList": [], "recruitType": 1,
                "practiceTypes": [], "onlyHotRecruit": 0,
            },
            headers=headers,
        )
        if data.get("code") != 0:
            raise RuntimeError(f"Bilibili code={data.get('code')}: {data.get('message')}")
        d = data.get("data") or {}
        rows = d.get("list") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            jd = txt(j.get("positionDescription"))
            out.append(Job(
                src["company"], txt(j.get("positionName")), jid,
                txt(j.get("workLocation")), txt(j.get("positionTypeName") or "校招全职"),
                txt(j.get("postCodeName")), jd, "",
                f"{root}/campus/positions/{jid}" if jid else src["portal"],
                list_api,
                "哔哩哔哩官方校园招聘全职项目" + (" / 2027" if "2027" in jd else ""),
            ))
        total = int(d.get("total") or 0)
        if page * 100 >= total or len(rows) < 100:
            break
        page += 1
    return out


def fetch_huawei_2027(src: dict) -> list[Job]:
    portal_root = "https://career.huawei.com/reccampportal"
    pub = portal_root + "/services/portal/portalpub"
    user_api = portal_root + "/services/portal/portaluser"
    page_url = portal_root + "/portal5/campus-recruitment.html"
    session = requests.Session()
    session.headers.update({**HEADERS, "Referer": page_url})
    try:
        session.get(portal_root + "/", timeout=TIMEOUT)
    except Exception:
        pass

    out: list[Job] = []
    page = 1
    while page <= 50:
        params = {
            "jobType": "0", "jobTypes": "2", "language": "zh_CN",
            "reqTime": int(time.time() * 1000),
            "orderBy": "ISS_STARTDATE_DESC_AND_IS_HOT_JOB",
        }
        url = f"{pub}/getJob/newHr/page/50/{page}"
        r = session.get(url, params=params, timeout=TIMEOUT)
        r.raise_for_status()
        payload = r.json()
        rows = payload.get("result") or []
        if not rows:
            break
        for row in rows:
            jid = txt(row.get("jobId"))
            ds = txt(row.get("dataSource") or "1")
            list_title = txt(row.get("jobname"))
            if not likely_target_title(list_title):
                continue
            detail = {}
            if jid:
                try:
                    dr = session.get(
                        f"{pub}/getJobDetail/newHr",
                        params={"jobId": jid, "dataSource": ds, "language": "zh_CN"},
                        timeout=TIMEOUT,
                    )
                    dr.raise_for_status()
                    detail = dr.json() or {}
                except Exception:
                    detail = {}
            desc = txt(detail.get("mainBusiness") or row.get("mainBusiness"))
            req = txt(detail.get("jobRequire") or row.get("jobRequire"))
            req_id = txt(detail.get("jobRequirementId") or row.get("jobRequirementId"))
            if req_id and (not desc or "详见岗位意向" in desc or not req or "详见岗位意向" in req):
                try:
                    ir = session.get(
                        f"{user_api}/findIntentListByJobRequirementId/newHr/zh_CN/{req_id}/null",
                        params={"dataSource": ds, "jobId": jid},
                        timeout=TIMEOUT,
                    )
                    ir.raise_for_status()
                    intents = ir.json() or []
                    if isinstance(intents, list) and intents:
                        desc = "\n\n".join(
                            f"【{txt(i.get('positionIntention'))}】\n{_strip_html(i.get('jobResponsibilities'))}"
                            for i in intents
                        )
                        req = "\n\n".join(
                            f"【{txt(i.get('positionIntention'))}】\n{_strip_html(i.get('jobDemand'))}"
                            for i in intents
                        )
                except Exception:
                    pass
            out.append(Job(
                src["company"], txt(detail.get("jobname") or list_title), jid,
                txt(detail.get("jobArea") or row.get("jobArea") or row.get("jobAddress")),
                "2027应届生", txt(detail.get("jobFamilyName") or row.get("jobFamilyName")),
                _strip_html(desc), _strip_html(req),
                f"{page_url.replace('campus-recruitment.html','campus-recruitment-detail.html')}?jobId={jid}&dataSource={ds}",
                f"{pub}/getJob/newHr/page/50/{{page}}",
                "华为2027届应届生招聘",
            ))
        pvo = payload.get("pageVO") or {}
        total_pages = int(pvo.get("totalPages") or 0)
        if total_pages and page >= total_pages:
            break
        if len(rows) < 50:
            break
        page += 1
    return out


def fetch_ant_2027(src: dict) -> list[Job]:
    api = "https://hrcareersweb.antgroup.com/api/campus/position/search"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Origin": "https://talent.antgroup.com",
        "Referer": "https://talent.antgroup.com/campus-list",
    }
    out: list[Job] = []
    page = 1
    while page <= 80:
        data = post_json(
            api,
            payload={"key": "", "pageIndex": page, "pageSize": 49, "language": "zh"},
            headers=headers,
        )
        if data.get("success") is not True:
            raise RuntimeError(data.get("errorMsg") or f"Ant success={data.get('success')}")
        rows = data.get("content") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id") or j.get("code"))
            graduation = txt(j.get("graduationTime"))
            out.append(Job(
                src["company"], txt(j.get("name")), jid,
                txt(j.get("workLocations")), txt(j.get("positionType") or "校招"),
                txt(j.get("department") or j.get("project") or j.get("categoryName")),
                _strip_html(j.get("description")), _strip_html(j.get("requirement")),
                f"https://talent.antgroup.com/campus-position?positionId={jid}" if jid else src["portal"],
                api,
                "蚂蚁集团官方校园招聘" + (f" / {graduation}" if graduation else ""),
            ))
        total = int(data.get("totalCount") or 0)
        if page * 49 >= total or len(rows) < 49:
            break
        page += 1
    return out


def _beisen_fetch_all(
    *,
    company: str,
    root: str,
    portal_id: str,
    categories: list[str] | None,
    cycle_evidence: str,
    source_url: str,
) -> list[Job]:
    api = root.rstrip("/") + "/api/Jobad/GetJobAdPageList"
    headers = {
        **HEADERS,
        "Content-Type": "application/json",
        "Origin": root.rstrip("/"),
        "Referer": source_url,
        "x-requested-with": "xmlhttprequest",
        "langtype": "zh_CN",
    }
    out: list[Job] = []
    page = 0
    while page < 50:
        body: dict[str, Any] = {
            "PageIndex": page, "PageSize": 100, "KeyWords": "",
            "SpecialType": 0, "PortalId": portal_id,
            "DisplayFields": ["Category", "Kind", "LocId", "Org", "HeadCount", "PostDate", "Salary"],
        }
        if categories:
            body["Category"] = categories
        data = post_json(api, payload=body, headers=headers)
        if data.get("Code") != 200:
            raise RuntimeError(data.get("Message") or f"Beisen code={data.get('Code')}")
        rows = data.get("Data") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("JobAdId") or j.get("Id"))
            out.append(Job(
                company, txt(j.get("JobAdName")), jid,
                txt(j.get("LocNames")), txt(j.get("Category") or "校园招聘"),
                txt(j.get("Org")), _strip_html(j.get("Duty")), _strip_html(j.get("Require")),
                f"{root.rstrip('/')}/campus/detail?jobAdId={jid}" if jid else source_url,
                api, cycle_evidence,
            ))
        total = int(data.get("Count") or data.get("Total") or 0)
        page += 1
        if page * 100 >= total or len(rows) < 100:
            break
    return out


def fetch_vivo_2027(src: dict) -> list[Job]:
    return _beisen_fetch_all(
        company=src["company"], root="https://hr-campus.vivo.com",
        portal_id="903cbcbf-4898-46e1-817c-da522a9752b1",
        categories=["2"], cycle_evidence="vivo官方校园招聘（2027届别由职位/项目正文复核）",
        source_url="https://hr-campus.vivo.com/campus/jobs",
    )


def fetch_beisen_direct(src: dict) -> list[Job]:
    """Enumerate a company-proven Beisen/Zhiye campus tenant via the public first-party API."""
    parsed = urlparse(src.get("search_url") or src.get("portal") or "")
    root = f"{parsed.scheme}://{parsed.netloc}"
    if not parsed.netloc or not parsed.netloc.endswith("zhiye.com"):
        raise RuntimeError("beisen_direct requires a zhiye.com official ATS search_url")
    cond_api = root + "/api/Jobad/GetJobAdSearchConditions"
    headers = {
        **HEADERS, "Content-Type": "application/json", "Origin": root,
        "Referer": src.get("search_url") or src.get("portal") or root,
        "x-requested-with": "xmlhttprequest", "langtype": "zh_CN",
    }
    categories: list[str] = []
    try:
        conditions = post_json(cond_api, payload={"displayFilters": ["Category"]}, headers=headers)
        if conditions.get("Code") == 200:
            for axis in conditions.get("Data") or []:
                if txt(axis.get("Value")) != "Category":
                    continue
                for item in axis.get("Data") or []:
                    label = txt(item.get("Text"))
                    cid = txt(item.get("StrValue") or item.get("Value"))
                    if cid and not re.search(r"社会|社招|实习", label):
                        categories.append(cid)
    except Exception:
        categories = []
    return _beisen_fetch_all(
        company=src["company"], root=root, portal_id=txt(src.get("beisen_portal_id")),
        categories=categories or None,
        cycle_evidence=txt(src.get("beisen_cycle_evidence")) or "官方校园招聘",
        source_url=src.get("search_url") or src.get("portal") or root,
    )

def fetch_iflytek_2027(src: dict) -> list[Job]:
    root = "https://iflytek.zhiye.com"
    cond_api = root + "/api/Jobad/GetJobAdSearchConditions"
    headers = {
        **HEADERS, "Content-Type": "application/json", "Origin": root,
        "Referer": root + "/jobs", "x-requested-with": "xmlhttprequest", "langtype": "zh_CN",
    }
    categories: list[str] = []
    try:
        conditions = post_json(cond_api, payload={"displayFilters": ["Category"]}, headers=headers)
        if conditions.get("Code") == 200:
            for axis in conditions.get("Data") or []:
                if txt(axis.get("Value")) != "Category":
                    continue
                for item in axis.get("Data") or []:
                    label = txt(item.get("Text"))
                    cid = txt(item.get("StrValue") or item.get("Value"))
                    if cid and not re.search(r"社会|社招|实习", label):
                        categories.append(cid)
    except Exception:
        pass
    if not categories:
        categories = ["4", "5", "6"]
    return _beisen_fetch_all(
        company=src["company"], root=root, portal_id="", categories=categories,
        cycle_evidence="科大讯飞官方校园招聘（2027届别由职位/项目正文复核）",
        source_url=root + "/jobs",
    )


def fetch_ctrip_2027(src: dict) -> list[Job]:
    api = "https://careers.ctrip.com/api/hrrecruit/getJobAd"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Origin": "https://careers.ctrip.com", "Referer": "https://careers.ctrip.com/#/campus",
    }
    data = post_json(api, payload={"condition": {"pageIndex": 1, "pageSize": 100, "category": "2"}}, headers=headers)
    if txt(data.get("retCode")) != "201":
        raise RuntimeError(data.get("retMessage") or f"Ctrip retCode={data.get('retCode')}")
    d = data.get("retValue") or {}
    out: list[Job] = []
    for j in d.get("recruitJobAdList") or []:
        jid = txt(j.get("id") or j.get("jobId"))
        mj = txt(j.get("fromId"))
        out.append(Job(
            src["company"], txt(j.get("jobTitle")), jid,
            txt(j.get("cityName")), "2027届应届校招",
            txt(j.get("buName") or j.get("jobFamilyGroupName")),
            _strip_html(j.get("duty")), _strip_html(j.get("requirements")),
            f"https://careers.ctrip.com/campus#/experienced/job-detail/{mj}" if mj else "https://careers.ctrip.com/#/campus",
            api, "携程集团2027届应届校招生",
        ))
    return out


def fetch_honor_2027(src: dict) -> list[Job]:
    host = "https://career.honor.com"
    su = "SU60eea919bef57c1023f6fe78"
    list_api = f"{host}/wecruit/positionInfo/listPosition/{su}"
    detail_api = f"{host}/wecruit/positionInfo/listPositionDetail/{su}"
    headers = {
        **HEADERS, "Content-Type": "application/x-www-form-urlencoded",
        "Origin": host, "Referer": f"{host}/{su}/pb/school.html",
        "X-Requested-With": "XMLHttpRequest",
    }
    out: list[Job] = []
    page = 1
    while page <= 100:
        params = {"iSaJAx": "isAjax", "request_locale": "zh_CN", "t": int(time.time() * 1000)}
        # Official Wecruit list endpoint is form-urlencoded with query params.
        rr = requests.post(
            list_api,
            params=params,
            data={"isFrompb": "true", "recruitType": 1, "pageSize": 100, "currentPage": page},
            headers=headers, timeout=TIMEOUT,
        )
        rr.raise_for_status()
        data = rr.json()
        if txt(data.get("state")) != "200":
            raise RuntimeError(data.get("msg") or f"Honor state={data.get('state')}")
        pf = ((data.get("data") or {}).get("pageForm") or {})
        rows = pf.get("pageData") or []
        if not rows:
            break
        for row in rows:
            pid = txt(row.get("postId"))
            list_title = txt(row.get("postName"))
            if not likely_target_title(list_title):
                continue
            detail: dict[str, Any] = {}
            if pid:
                try:
                    dr = requests.post(
                        detail_api,
                        params={"iSaJAx": "isAjax", "request_locale": "zh_CN", "t": int(time.time() * 1000)},
                        data={"postId": pid, "recruitType": 1},
                        headers=headers | {"Referer": f"{host}/{su}/pb/posDetail.html"},
                        timeout=TIMEOUT,
                    )
                    dr.raise_for_status()
                    dp = dr.json()
                    if txt(dp.get("state")) == "200":
                        detail = dp.get("data") or {}
                except Exception:
                    detail = {}
            out.append(Job(
                src["company"], txt(detail.get("postName") or list_title), pid,
                txt(detail.get("workPlaceStr") or row.get("workPlaceStr")),
                "荣耀2027校招", txt(detail.get("orgName") or row.get("department") or row.get("postTypeName")),
                _strip_html(detail.get("workContent") or row.get("description") or row.get("duty")),
                _strip_html(detail.get("serviceCondition") or row.get("require") or row.get("requirement")),
                f"{host}/{su}/pb/school.html#/postDetail?postId={pid}" if pid else src["portal"],
                list_api, "荣耀2027校招",
            ))
        total_pages = int(pf.get("totalPage") or 0)
        if total_pages and page >= total_pages:
            break
        if len(rows) < 100:
            break
        page += 1
    return out


def fetch_feishu_direct(src: dict) -> list[Job]:
    """Enumerate a company-proven Feishu Recruiting tenant directly.

    Feishu's public job search is anonymous. Portal scope is selected by the
    official portal-channel / website-path header; optional subject/project and
    recruitment filters come only from the company's official career URL.
    """
    host = txt(src.get("feishu_host"))
    channel = txt(src.get("feishu_channel"))
    if not host:
        host = urlparse(src["portal"]).hostname or ""
    if not channel:
        path = urlparse(src["portal"]).path.strip("/")
        channel = path.split("/")[0] if path else ""
    if not host:
        raise RuntimeError("Feishu host missing")

    api = f"https://{host}/api/v1/search/job/posts"
    apply_prefix = txt(src.get("feishu_apply_prefix")) or f"https://{host}/{channel}/position"
    headers = {
        **HEADERS,
        "Content-Type": "application/json",
        "portal-channel": channel,
        "portal-platform": "pc",
        "website-path": channel,
        "Origin": f"https://{host}",
        "Referer": src["portal"],
    }
    subject_ids = [str(x) for x in (src.get("feishu_subject_ids") or [])]
    recruitment_ids = [str(x) for x in (src.get("feishu_recruitment_ids") or [])]
    out: list[Job] = []
    offset = 0
    total = None
    for _ in range(100):
        body: dict[str, Any] = {
            "keyword": "", "limit": 100, "offset": offset,
            "portal_type": 3, "portal_entrance": 1, "language": "zh",
            "job_category_id_list": [], "location_code_list": [],
        }
        if subject_ids:
            body["subject_id_list"] = subject_ids
        if recruitment_ids:
            body["recruitment_id_list"] = recruitment_ids
        data = post_json(api, payload=body, headers=headers)
        if data.get("code") != 0:
            raise RuntimeError(f"Feishu {host}/{channel} code={data.get('code')}: {data.get('message')}")
        d = data.get("data") or {}
        rows = d.get("job_post_list") or []
        if total is None:
            total = int(d.get("count") or 0)
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("id"))
            cities = " / ".join(
                txt(x.get("name")) for x in (j.get("city_list") or [])
                if isinstance(x, dict) and x.get("name")
            ) or txt((j.get("city_info") or {}).get("name"))
            category = txt((j.get("recruit_type") or {}).get("name"))
            department = txt((j.get("job_category") or {}).get("name")) or txt((j.get("job_function") or {}).get("name"))
            subjects = []
            raw_subjects = j.get("job_subject_list") or ([j.get("job_subject")] if j.get("job_subject") else [])
            for s in raw_subjects:
                if not isinstance(s, dict):
                    continue
                name = s.get("name")
                if isinstance(name, dict):
                    name = name.get("zh_cn") or name.get("i18n") or name.get("en_us")
                if name:
                    subjects.append(txt(name))
            cycle = " / ".join(subjects + ([category] if category else []))
            out.append(Job(
                src["company"], txt(j.get("title")), jid, cities, category, department,
                txt(j.get("description")), txt(j.get("requirement")),
                f"{apply_prefix.rstrip('/')}/{jid}/detail" if jid else src["portal"],
                api, cycle,
            ))
        offset += len(rows)
        if len(rows) < 100 or (total is not None and offset >= total):
            break
    return out


def fetch_mihoyo_campus(src: dict) -> list[Job]:
    """Enumerate miHoYo's complete current formal campus pool via its first-party ATS."""
    list_api = "https://ats.openout.mihoyo.com/ats-portal/v1/job/list"
    detail_api = "https://ats.openout.mihoyo.com/ats-portal/v1/job/info"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Origin": "https://jobs.mihoyo.com",
        "Referer": "https://jobs.mihoyo.com/#/campus/position",
    }
    rows: list[dict[str, Any]] = []
    page = 1
    page_size = 100
    total = None
    while page <= 100:
        payload = {
            "pageNo": page, "pageSize": page_size,
            "channelDetailIds": [1], "hireType": 1,
        }
        data = post_json(list_api, payload=payload, headers=headers)
        d = data.get("data") or {}
        got = d.get("list") or d.get("records") or d.get("items") or []
        if not got:
            break
        rows.extend(x for x in got if isinstance(x, dict))
        try:
            total = int(d.get("total") or d.get("totalCount") or 0)
        except Exception:
            total = 0
        if len(got) < page_size or (total and len(rows) >= total):
            break
        page += 1

    out: list[Job] = []
    for row in rows:
        jid = txt(row.get("id") or row.get("jobId"))
        title = txt(row.get("title") or row.get("jobTitle") or row.get("positionName"))
        cities = " / ".join(
            txt(x.get("addressDetail") or x.get("name"))
            for x in (row.get("addressDetailList") or row.get("addressList") or [])
            if isinstance(x, dict) and (x.get("addressDetail") or x.get("name"))
        )
        desc = txt(row.get("description") or row.get("jobDescription") or row.get("jobSummary"))
        req = txt(row.get("jobRequire") or row.get("requirement") or row.get("jobRequirement"))
        detail: dict[str, Any] = {}
        if jid and likely_target_title(title):
            try:
                dd = post_json(
                    detail_api,
                    payload={"id": jid, "channelDetailIds": [1], "hireType": 1},
                    headers=headers,
                )
                detail = dd.get("data") or {}
            except Exception:
                detail = {}
        if detail:
            desc = txt(
                detail.get("description") or detail.get("jobDescription") or
                detail.get("responsibility") or detail.get("jobResponsibility") or desc
            )
            req = txt(
                detail.get("jobRequire") or detail.get("requirement") or
                detail.get("jobRequirement") or detail.get("qualification") or req
            )
        out.append(Job(
            src["company"], title, jid, cities,
            txt(row.get("jobNature") or row.get("projectName") or "2027校园招聘正式岗"),
            txt(row.get("competencyType") or row.get("jobCategory")),
            _strip_html(desc), _strip_html(req),
            f"https://jobs.mihoyo.com/#/campus/position/{jid}" if jid else src["portal"],
            list_api,
            "米哈游官方校园招聘 / 校招渠道 channelDetailIds=1 / 正式岗 hireType=1",
        ))
    return out


def fetch_byd_campus(src: dict) -> list[Job]:
    """Enumerate BYD's complete 2027 formal campus list, enriching only target-like titles."""
    root = "https://job.byd.com"
    list_api = root + "/portal/api/portal-api/schoolPortal/queryPositionList"
    detail_api = root + "/portal/api/portal-api/schoolPortal/queryPosition"
    headers = {
        **HEADERS, "Content-Type": "application/json",
        "Origin": root, "Referer": src.get("search_url") or src.get("portal") or root,
    }
    rows: list[dict[str, Any]] = []
    page = 1
    page_size = 100
    while page <= 100:
        payload = {
            "topicCode": "", "batch": "2027", "campusNature": "008501",
            "abroad": "", "degree": "", "jobType": [], "researchDirection": [],
            "workPlace": [], "keywords": "", "pageSize": page_size, "pageIndex": page,
        }
        data = post_json(list_api, payload=payload, headers=headers)
        got = data.get("data") if isinstance(data, dict) else None
        if not isinstance(got, list) or not got:
            break
        rows.extend(x for x in got if isinstance(x, dict))
        if len(got) < page_size:
            break
        page += 1

    out: list[Job] = []
    for row in rows:
        outer_id = txt(row.get("id"))
        outer_title = txt(row.get("jobName") or row.get("positionName") or row.get("title"))
        detail_outer: dict[str, Any] = {}
        inner_rows: list[dict[str, Any]] = []
        if outer_id and likely_target_title(outer_title):
            try:
                detail_payload = get_json(
                    detail_api,
                    params={"id": outer_id, "abroad": "", "degree": ""},
                    headers={"Referer": src.get("search_url") or root},
                )
                detail_outer = detail_payload.get("data") or {}
                raw_inner = detail_outer.get("positionInfoList") or []
                inner_rows = [x for x in raw_inner if isinstance(x, dict)]
            except Exception:
                detail_outer, inner_rows = {}, []
        if inner_rows:
            for inner in inner_rows:
                inner_id = txt(inner.get("id"))
                title = txt(inner.get("jobName") or inner.get("positionName") or outer_title)
                out.append(Job(
                    src["company"], title, f"{outer_id}:{inner_id}" if inner_id else outer_id,
                    txt(inner.get("workPlace") or detail_outer.get("workPlace") or row.get("workPlace")),
                    "比亚迪2027校园招聘正式岗",
                    txt(inner.get("jobType") or detail_outer.get("jobType") or row.get("jobType")),
                    _strip_html(inner.get("jobDuty") or inner.get("description")),
                    _strip_html(inner.get("jobRequirements") or inner.get("requirement")),
                    f"{detail_api}?id={outer_id}&abroad=&degree=",
                    list_api,
                    "比亚迪2027届校园招聘 / campusNature=008501 / 全职",
                ))
        else:
            out.append(Job(
                src["company"], outer_title, outer_id,
                txt(row.get("workPlace")), "比亚迪2027校园招聘正式岗",
                txt(row.get("jobType")),
                _strip_html(row.get("jobDuty") or row.get("description")),
                _strip_html(row.get("jobRequirements") or row.get("requirement")),
                f"{detail_api}?id={outer_id}&abroad=&degree=" if outer_id else src["portal"],
                list_api,
                "比亚迪2027届校园招聘 / campusNature=008501 / 全职",
            ))
    return out


def fetch_ashby_official(src: dict) -> list[Job]:
    """Enumerate every currently published posting from an official Ashby job board."""
    board = txt(src.get("ashby_board_name"))
    if not board:
        path = urlparse(src.get("portal") or "").path.strip("/")
        board = path.split("/")[0] if path else ""
    if not board:
        raise RuntimeError("Ashby board name missing")
    api = f"https://api.ashbyhq.com/posting-api/job-board/{board}"
    data = get_json(api, params={"includeCompensation": "true"})
    rows = data.get("jobs") or []
    out: list[Job] = []
    for j in rows:
        job_url = txt(j.get("jobUrl") or j.get("applyUrl"))
        jid = ""
        if job_url:
            jid = urlparse(job_url).path.rstrip("/").split("/")[-1]
        description = _strip_html(
            j.get("descriptionHtml") or j.get("description") or j.get("descriptionPlain") or ""
        )
        team = txt(j.get("team") or j.get("department"))
        out.append(Job(
            src["company"], txt(j.get("title")), jid,
            txt(j.get("location")), "当前官方招聘", team,
            description, "",
            job_url or src.get("portal") or api,
            api,
            "Ashby 当前已发布官方岗位；职位正文决定应届/新毕业生资格",
        ))
    return out


def fetch_hikvision_campus(src: dict) -> list[Job]:
    """Enumerate Hikvision's current graduate pool through its first-party campus API."""
    root = "https://mcampus.hikvision.com"
    batch_api = root + "/api/userfacade/crsBatch/findBatchAll"
    list_api = root + "/api/search/crsPositionSearch/getPositionByQuery"
    headers = {
        **HEADERS,
        "Referer": root + "/#/position?activeTab=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": root,
    }
    batch_data = get_json(batch_api, params={"jobNature": "应届生"}, headers=headers)
    def walk_batches(v: Any) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        if isinstance(v, dict):
            if any(k in v for k in ("batchId", "id")) and any(
                "2027" in txt(v.get(k)) for k in ("batchName", "name", "title", "batchDesc")
            ):
                found.append(v)
            for x in v.values():
                found.extend(walk_batches(x))
        elif isinstance(v, list):
            for x in v:
                found.extend(walk_batches(x))
        return found
    batches = walk_batches(batch_data)
    batch_id = txt((batches[0] if batches else {}).get("batchId") or (batches[0] if batches else {}).get("id"))
    if not batch_id:
        # Current official browser discovery exposed this endpoint; if the API
        # omits the year label, fall back to the first active batch object.
        def first_id(v: Any) -> str:
            if isinstance(v, dict):
                for k in ("batchId", "id"):
                    if v.get(k):
                        return txt(v.get(k))
                for x in v.values():
                    got = first_id(x)
                    if got:
                        return got
            elif isinstance(v, list):
                for x in v:
                    got = first_id(x)
                    if got:
                        return got
            return ""
        batch_id = first_id(batch_data)
    if not batch_id:
        raise RuntimeError("Hikvision current graduate batchId missing")

    def rows_from(payload: Any) -> tuple[list[dict[str, Any]], int]:
        if not isinstance(payload, (dict, list)):
            return [], 0
        candidates: list[list[dict[str, Any]]] = []
        totals: list[int] = []
        def walk(v: Any) -> None:
            if isinstance(v, dict):
                for k in ("total", "count", "totalCount"):
                    try:
                        if v.get(k) is not None:
                            totals.append(int(v.get(k)))
                    except Exception:
                        pass
                for x in v.values():
                    walk(x)
            elif isinstance(v, list):
                ds = [x for x in v if isinstance(x, dict)]
                if ds and any(
                    any(key in x for key in ("positionName", "postName", "jobName", "positionId", "postAdSn"))
                    for x in ds
                ):
                    candidates.append(ds)
                for x in v:
                    walk(x)
        walk(payload)
        rows = max(candidates, key=len) if candidates else []
        return rows, max(totals) if totals else 0

    out: list[Job] = []
    seen: set[str] = set()
    page = 1
    while page <= 100:
        form = {
            "pageNum": page, "pageSize": 100, "keyWord": "",
            "jobNature": "应届生", "batchId": batch_id,
            "postAdSnList": "", "workPlaces": "", "adNeedDept": "", "interviewMethodList": "",
        }
        data = post_form(list_api, data=form, headers=headers)
        rows, total = rows_from(data)
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("positionId") or j.get("postAdSn") or j.get("id"))
            key = jid or (txt(j.get("positionName") or j.get("postName") or j.get("jobName")) + "|" + txt(j.get("workPlace")))
            if key in seen:
                continue
            seen.add(key)
            title = txt(j.get("positionName") or j.get("postName") or j.get("jobName") or j.get("name"))
            out.append(Job(
                src["company"], title, jid,
                txt(j.get("workPlace") or j.get("workPlaces") or j.get("location")),
                "【2027校园招聘】应届生", txt(j.get("departmentName") or j.get("adNeedDept") or j.get("department")),
                _strip_html(j.get("description") or j.get("positionDescription") or j.get("duty")),
                _strip_html(j.get("requirement") or j.get("jobRequirement") or j.get("qualification")),
                src.get("search_url") or root + "/#/position?activeTab=0",
                list_api,
                "海康威视官方 2027 校园招聘 / 应届生",
            ))
        if len(rows) < 100 or (total and page * 100 >= total):
            break
        page += 1
    return out


FETCHERS: dict[str, Callable[[dict], list[Job]]] = {
    "xiaomi_api": fetch_xiaomi,
    "bytedance_api": fetch_bytedance,
    "sangfor_campus_api": fetch_sangfor_campus,
    "ashby_official": fetch_ashby_official,
    "mihoyo_campus_api": fetch_mihoyo_campus,
    "byd_campus_api": fetch_byd_campus,
    "hikvision_campus_api": fetch_hikvision_campus,
    "kuaishou_api": fetch_kuaishou,
    "baidu_api": fetch_baidu,
    "tencent_api": fetch_tencent,
    "tencent_campus_api": fetch_tencent_campus,
    "meituan_api": fetch_meituan,
    "meituan_campus_api": fetch_meituan_campus,
    "jd_campus_api": fetch_jd_campus,
    "pdd_campus_api": fetch_pdd_campus,
    "oppo_campus_api": fetch_oppo_campus,
    "lenovo_api": fetch_lenovo,
    "sf_campus_api": fetch_sf,
    "alibaba_campus_api": fetch_alibaba_campus,
    "netease_api": fetch_netease,
    "bilibili_api": fetch_bilibili_2027,
    "xiaohongshu_2027_api": fetch_xiaohongshu_2027,
    "ant_2027_api": fetch_ant_2027,
    "vivo_2027_api": fetch_vivo_2027,
    "iflytek_2027_api": fetch_iflytek_2027,
    "beisen_direct": fetch_beisen_direct,
    "ctrip_2027_api": fetch_ctrip_2027,
    "honor_2027_api": fetch_honor_2027,
    "feishu_direct": fetch_feishu_direct,
    "didi_api": fetch_didi,
    "pdd_api": fetch_pdd,
    "huawei_api": fetch_huawei_2027,
}


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))

    # Persistent facts are deliberately separate from runtime discovery.
    # A transient WAF/API/browser failure must never turn a previously verified
    # company role into "0 jobs".
    verified_index = {"companies": []}
    if VERIFIED_INDEX.exists():
        try:
            verified_index = json.loads(VERIFIED_INDEX.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"verified role index parse warning: {e}", file=sys.stderr)

    manual_seed_payload: dict[str, Any] = {"roles": []}
    if MANUAL_ROLE_SEEDS.exists():
        try:
            manual_seed_payload = json.loads(MANUAL_ROLE_SEEDS.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"manual first-party role seed parse warning: {e}", file=sys.stderr)

    previous_payload: dict[str, Any] = {}
    if OUT_JSON.exists():
        try:
            previous_payload = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"previous generated job payload parse warning: {e}", file=sys.stderr)
    keywords = [x.lower() for x in cfg.get("strong_agent_keywords", cfg["agent_keywords"])]
    excludes = [x.lower() for x in cfg["hard_exclude_title_keywords"]]
    engineering_signals = [x.lower() for x in cfg.get("engineering_title_signals", [])]
    body_agent_signals = [x.lower() for x in cfg.get("body_agent_signals", [])]
    training_signals = [x.lower() for x in cfg.get("training_heavy_signals", [])]
    strict_title_allowlist = {x.lower() for x in cfg.get("strict_title_allowlist", [])}

    all_matches: list[Job] = []
    results: list[SourceResult] = []

    dynamic_by_company: dict[str, dict] = {}
    if BROWSER_CACHE.exists():
        try:
            browser_payload = json.loads(BROWSER_CACHE.read_text(encoding="utf-8"))
            if cache_is_fresh(browser_payload):
                dynamic_by_company = {
                    x.get("company"): x
                    for x in (browser_payload.get("results") or [])
                    if x.get("company")
                }
            else:
                print("browser discovery cache is stale; ignoring it for this runtime", file=sys.stderr)
        except Exception as e:
            print(f"browser discovery cache parse warning: {e}", file=sys.stderr)

    feishu_by_company: dict[str, dict] = {}
    if FEISHU_CACHE.exists():
        try:
            feishu_payload = json.loads(FEISHU_CACHE.read_text(encoding="utf-8"))
            if cache_is_fresh(feishu_payload):
                feishu_by_company = {
                    x.get("company"): x
                    for x in (feishu_payload.get("results") or [])
                    if x.get("company")
                }
            else:
                print("feishu discovery cache is stale; ignoring it for this runtime", file=sys.stderr)
        except Exception as e:
            print(f"feishu discovery cache parse warning: {e}", file=sys.stderr)

    moka_by_company: dict[str, dict] = {}
    if MOKA_CACHE.exists():
        try:
            moka_payload = json.loads(MOKA_CACHE.read_text(encoding="utf-8"))
            if cache_is_fresh(moka_payload):
                moka_by_company = {
                    x.get("company"): x
                    for x in (moka_payload.get("results") or [])
                    if x.get("company")
                }
            else:
                print("moka discovery cache is stale; ignoring it for this runtime", file=sys.stderr)
        except Exception as e:
            print(f"moka discovery cache parse warning: {e}", file=sys.stderr)

    def to_jobs(company: str, raw_jobs: list[dict], fallback_url: str, fallback_api: str) -> list[Job]:
        return [
            Job(
                company,
                txt(j.get("title")),
                txt(j.get("job_id")),
                txt(j.get("location")),
                txt(j.get("category") or "官方动态招聘"),
                txt(j.get("department")),
                txt(j.get("description")),
                txt(j.get("requirements")),
                txt(j.get("official_url") or fallback_url),
                txt(j.get("official_api") or fallback_api),
                txt(j.get("cycle_evidence")),
            )
            for j in raw_jobs
        ]

    def strict_role_title(job: Job) -> bool:
        title = job.title.splitlines()[0].strip().lower()
        body = " ".join([job.category, job.department, job.description, job.requirements]).lower()

        if title in strict_title_allowlist:
            return True

        # Formal library requires the job itself to be an engineering role whose
        # title explicitly names the Agent / AI-application system being built.
        explicit = (
            any(k in title for k in keywords)
            and any(s in title for s in engineering_signals)
        )
        if explicit:
            return True

        # FDE and generic "large-model R&D/development engineer" titles are admitted
        # only when their first-party JD clearly describes Agent/RAG/application work.
        body_hits = {k for k in body_agent_signals if k in body}
        if "fde" in title and len(body_hits) >= 2:
            return True
        if any(k in title for k in ("大模型研发工程师", "大模型开发工程师")) and any(
            k in body for k in ("agent", "智能体", "rag", "function calling", "工具调用")
        ):
            return True
        return False

    def target_matches(jobs: list[Job], src: dict) -> list[Job]:
        # Official recruiting policy:
        # - campus board: the live board itself is the time gate;
        # - mixed official Careers/ATS board: the JD must explicitly allow new grads.
        # Role scope is intentionally title-first so generic software jobs that merely
        # mention "using AI tools" in boilerplate never enter the formal library.
        explicit_campus_board = bool(src.get("current_campus_board"))
        matches = [
            j for j in jobs
            if (explicit_campus_board or campusish(j))
            and strict_role_title(j)
            and not training_heavy(j, training_signals)
            and not is_hard_excluded(j, excludes)
            and "实习" not in (j.title + " " + j.category).lower()
            and "intern" not in (j.title + " " + j.category).lower()
        ]
        seen = set()
        uniq: list[Job] = []
        for j in matches:
            key = (j.company, j.job_id or j.title, j.location)
            if key in seen:
                continue
            seen.add(key)
            uniq.append(j)
        return uniq

    def collect(src: dict) -> tuple[SourceResult, list[Job]]:
        company = src["company"]
        mode = src["mode"]

        feishu = feishu_by_company.get(company) or {}
        if feishu.get("status") == "OK":
            jobs = to_jobs(company, feishu.get("jobs") or [], src["portal"], "FEISHU:" + src["portal"])
            matches = target_matches(jobs, src)
            return SourceResult(
                company, "feishu_official", src["portal"],
                "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                len(jobs), len(matches)
            ), matches

        moka = moka_by_company.get(company) or {}
        if moka.get("status") == "OK":
            jobs = to_jobs(company, moka.get("jobs") or [], src["portal"], txt(moka.get("api")) or ("MOKA:" + src["portal"]))
            matches = target_matches(jobs, src)
            return SourceResult(
                company, "moka_official", src["portal"],
                "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                len(jobs), len(matches)
            ), matches

        if mode == "portal_only":
            dyn = dynamic_by_company.get(company) or {}
            raw_jobs = dyn.get("jobs") or []
            jobs = to_jobs(company, raw_jobs, src["portal"], "BROWSER:" + src["portal"])
            matches = target_matches(jobs, src)
            raw_status = txt(dyn.get("status"))
            full_search = bool(dyn.get("full_keyword_search")) or bool(dyn.get("list_scan_complete"))
            if raw_status == "BROWSER_ENUMERATED":
                status = "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES"
                error = ""
            elif raw_status in ("BROWSER_ENUMERATED_ZERO","BROWSER_OK_0_MATCH") and full_search:
                status = "ENUMERATED_ZERO_MATCHES"
                error = ""
            elif raw_status in ("BROWSER_NO_PUBLIC_CAMPUS","BROWSER_NO_PUBLIC_2027"):
                status = "NO_PUBLIC_CAMPUS_PROJECT"
                error = "官网当前未公开校园招聘职位池"
            elif raw_status in ("BROWSER_NO_CAMPUS_EVIDENCE","BROWSER_NO_2027_EVIDENCE","BROWSER_CAMPUS_NEEDS_ADAPTER","BROWSER_2027_NEEDS_ADAPTER"):
                status = "BLOCKED"
                error = "官方校招入口尚未完成可靠全量枚举；不能判定 0 岗位"
            elif raw_status == "BROWSER_ERROR":
                status = "BLOCKED"
                error = txt(dyn.get("error")) or "浏览器枚举失败"
            else:
                status = "BLOCKED"
                error = "官方根入口存在，但尚未完成可靠的当前校招岗位池枚举"
            return SourceResult(company, "browser_dynamic", src["portal"], status, len(raw_jobs), len(matches), error), matches
        fetcher = FETCHERS.get(mode)
        if not fetcher:
            return SourceResult(company, mode, src["portal"], "NO_FETCHER", 0, 0), []
        try:
            jobs = fetcher(src)
            uniq = target_matches(jobs, src)
            status = "ENUMERATED_WITH_MATCHES" if uniq else "ENUMERATED_ZERO_MATCHES"
            return SourceResult(company, mode, src["portal"], status, len(jobs), len(uniq)), uniq
        except Exception as e:
            # Dedicated adapter failure never means "0 jobs". If browser discovery
            # succeeded from the company's official root / ATS chain, use it as a
            # first-party fallback; otherwise keep the source explicitly BLOCKED.
            dyn = dynamic_by_company.get(company) or {}
            raw_jobs = dyn.get("jobs") or []
            browser_terminal = (
                (bool(dyn.get("full_keyword_search")) or bool(dyn.get("list_scan_complete")))
                and txt(dyn.get("status")) == "BROWSER_ENUMERATED"
            )
            if browser_terminal:
                browser_jobs = to_jobs(company, raw_jobs, src["portal"], "BROWSER:" + src["portal"])
                matches = target_matches(browser_jobs, src)
                return SourceResult(
                    company, "browser_fallback", src["portal"],
                    "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                    len(raw_jobs), len(matches),
                    f"dedicated adapter failed; exhaustive official current-campus browser fallback used: {type(e).__name__}: {e}"[:700],
                ), matches
            discovered = discover_api_candidates(src["portal"])
            diagnostic = f"{type(e).__name__}: {e}"
            if discovered:
                diagnostic += " | discovered: " + " ; ".join(discovered[:8])
            return SourceResult(
                company, mode, src["portal"], "BLOCKED", 0, 0,
                diagnostic[:1600],
            ), []

    # Company sources are independent. Run official API adapters concurrently so one
    # slow/blocked dynamic recruitment site cannot stall the whole discovery cycle.
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(collect, src): src for src in cfg["sources"]}
        for future in as_completed(futures):
            result, matches = future.result()
            results.append(result)
            all_matches.extend(matches)
            print(
                f"collect {result.company}: {result.status}, "
                f"fetched={result.fetched}, matched={result.matched}, error={result.error}",
                flush=True,
            )

    results.sort(key=lambda r: r.company)
    all_matches.sort(key=lambda j: (j.company, j.title, j.location, j.job_id))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def family_title(title: str) -> str:
        first = (title or "").splitlines()[0].strip()
        return re.sub(r"\\s+-\\s+.+$", "", re.sub(r"\\s+", " ", first)).strip()

    family_map: dict[tuple[str, str], dict[str, Any]] = {}
    for j in all_matches:
        family = family_title(j.title)
        key = (j.company, family)
        item = family_map.setdefault(key, {
            "company": j.company,
            "role_family": family,
            "representative_title": (j.title or "").splitlines()[0].strip(),
            "locations": set(),
            "description": "",
            "requirements": "",
            "cycle_evidence": "",
            "requisitions": [],
            "detail_status": "TITLE_ONLY_OFFICIAL",
        })
        for loc in re.split(r"\\s*/\\s*|,\\s*", j.location or ""):
            if loc:
                item["locations"].add(loc)
        old_score = len(item["description"]) + len(item["requirements"])
        new_score = len(j.description or "") + len(j.requirements or "")
        if new_score > old_score:
            item["description"] = j.description or ""
            item["requirements"] = j.requirements or ""
            item["representative_title"] = (j.title or "").splitlines()[0].strip()
            item["cycle_evidence"] = j.cycle_evidence or ""
        if item["description"] or item["requirements"]:
            item["detail_status"] = "FULL_JD"
        req = {
            "job_id": j.job_id,
            "title": (j.title or "").splitlines()[0].strip(),
            "location": j.location,
            "official_url": j.official_url,
            "official_api": j.official_api,
        }
        if not any(
            (req["job_id"] and x.get("job_id") == req["job_id"])
            or (
                not req["job_id"]
                and x.get("official_url") == req["official_url"]
                and x.get("title") == req["title"]
            )
            for x in item["requisitions"]
        ):
            item["requisitions"].append(req)

    role_families = []
    for item in family_map.values():
        role_families.append({
            **item,
            "locations": sorted(item["locations"]),
        })
    role_families.sort(key=lambda x: (x["company"], x["role_family"]))

    # First-party manual seeds cover official pages that are current and
    # verifiable but not reliably enumerable (SPA/WAF/signed ATS). They never
    # import secondary-source JD text. Fresh automated FULL_JD data wins.
    automated_keys = {(x["company"], x["role_family"]) for x in role_families}
    seeded_companies: set[str] = set()
    for seed in manual_seed_payload.get("roles") or []:
        company = txt(seed.get("company"))
        family = txt(seed.get("title"))
        if not company or not family:
            continue
        key = (company, family)
        seeded_companies.add(company)
        if key in automated_keys:
            continue
        role_families.append({
            "company": company,
            "role_family": family,
            "representative_title": family,
            "locations": list(seed.get("locations") or []),
            "description": "",
            "requirements": "",
            "evidence_summary": txt(seed.get("evidence_summary")),
            "cycle_evidence": txt(seed.get("recruitment_type")),
            "requisitions": [{
                "job_id": txt(seed.get("job_id")),
                "title": family,
                "location": " / ".join(seed.get("locations") or []),
                "official_url": txt(seed.get("official_url")),
                "official_api": "FIRST_PARTY_MANUAL_SEED",
            }],
            "source_evidence": ["FIRST_PARTY_MANUAL_SEED"],
            "evidence_url": txt(seed.get("evidence_url") or seed.get("official_url")),
            "detail_status": "ROLE_VERIFIED_CURRENT_SOURCE",
            "manual_first_party_seed": True,
            "verified_on": txt(seed.get("verified_on")),
        })
        automated_keys.add(key)

    role_families.sort(key=lambda x: (x["company"], x["role_family"]))

    # Preserve the last verified role families whenever this run did not
    # successfully enumerate matching roles for that company. This prevents
    # an incomplete/blocked/zero-result crawl from erasing known-good data.
    current_keys = {(x["company"], x["role_family"]) for x in role_families}
    result_map = {r.company: r for r in results}
    live_match_companies = {
        r.company for r in results if r.status == "ENUMERATED_WITH_MATCHES"
    }
    live_zero_companies = {
        r.company for r in results if r.status == "ENUMERATED_ZERO_MATCHES"
    }
    for old in previous_payload.get("role_families") or []:
        company = old.get("company")
        family = old.get("role_family")
        if not company or not family or company in live_match_companies or company in live_zero_companies:
            continue
        key = (company, family)
        if key not in current_keys:
            carried = dict(old)
            carried["carried_forward"] = True
            carried["carry_reason"] = (
                result_map.get(company).status
                if result_map.get(company)
                else "NO_RUNTIME_RESULT"
            )
            role_families.append(carried)
            current_keys.add(key)

    # Update persistent company role state only from a complete fresh first-party enumeration.
    # BLOCKED/partial runs never overwrite the last verified fact.
    source_by_company = {x.get("company"): x for x in cfg.get("sources") or [] if x.get("company")}
    index_by_company = {
        x.get("company"): x for x in verified_index.get("companies") or [] if x.get("company")
    }
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for company, source in source_by_company.items():
        row = index_by_company.get(company)
        if row is None:
            row = {
                "company": company,
                "status": "NEEDS_ENUMERATION",
                "official_root": source.get("official_root", ""),
                "official_search_url": source.get("search_url") or source.get("job_list_url") or "",
                "board_scope": source.get("board_scope") or ("campus" if source.get("current_campus_board") else "official_recruiting"),
                "business_summary": source.get("business_summary", ""),
                "representative_roles": [],
                "last_verified": None,
            }
            verified_index.setdefault("companies", []).append(row)
            index_by_company[company] = row

        row["official_root"] = source.get("official_root", "")
        row["official_search_url"] = source.get("search_url") or source.get("job_list_url") or ""
        row["board_scope"] = source.get("board_scope") or ("campus" if source.get("current_campus_board") else "official_recruiting")
        row["business_summary"] = source.get("business_summary", "")

        runtime = result_map.get(company)
        if runtime and (runtime.status == "ENUMERATED_WITH_MATCHES" or runtime.matched > 0):
            candidates = [
                f for f in role_families
                if f.get("company") == company and not f.get("carried_forward")
            ]
            if candidates:
                candidates.sort(
                    key=lambda f: (
                        f.get("detail_status") == "FULL_JD",
                        len(f.get("description") or "") + len(f.get("requirements") or ""),
                        len(f.get("requisitions") or []),
                    ),
                    reverse=True,
                )
                best = candidates[0]
                req = (best.get("requisitions") or [{}])[0]
                full = best.get("detail_status") == "FULL_JD"
                summary = "\n".join(
                    x for x in [best.get("description") or "", best.get("requirements") or ""] if x
                )[:5000]
                row["status"] = "VERIFIED_ROLE"
                row["representative_roles"] = [{
                    "title": best.get("representative_title") or best.get("role_family") or "",
                    "recruitment_type": best.get("cycle_evidence") or (
                        "当前校园招聘" if row["board_scope"] == "campus" else "当前官方招聘（应届可投）"
                    ),
                    "role_scope": best.get("role_family") or best.get("representative_title") or "",
                    "official_apply_url": req.get("official_url") or row["official_search_url"],
                    "evidence_url": req.get("official_url") or row["official_search_url"],
                    "evidence_type": "FIRST_PARTY_FULL_JD" if full else "FIRST_PARTY_OFFICIAL_TITLE",
                    "jd_status": "FULL_FIRST_PARTY_JD" if full else "TITLE_ONLY_FIRST_PARTY",
                    "jd_summary": summary,
                    "source_role_family": best.get("role_family") or "",
                }]
                row["last_verified"] = today
        elif runtime and runtime.status == "ENUMERATED_ZERO_MATCHES" and company not in seeded_companies:
            row["status"] = "ZERO_TARGET_JDS"
            row["representative_roles"] = []
            row["last_verified"] = today
        elif company in seeded_companies:
            candidates = [f for f in role_families if f.get("company") == company]
            if candidates:
                best = next((f for f in candidates if f.get("manual_first_party_seed")), candidates[0])
                req = (best.get("requisitions") or [{}])[0]
                row["status"] = "VERIFIED_ROLE"
                row["representative_roles"] = [{
                    "title": best.get("representative_title") or best.get("role_family") or "",
                    "recruitment_type": best.get("cycle_evidence") or "当前校园招聘",
                    "role_scope": best.get("role_family") or "",
                    "official_apply_url": req.get("official_url") or row["official_search_url"],
                    "evidence_url": best.get("evidence_url") or req.get("official_url") or row["official_search_url"],
                    "evidence_type": "FIRST_PARTY_OFFICIAL_LISTING",
                    "jd_status": "ROLE_VERIFIED",
                    "jd_summary": best.get("evidence_summary") or "",
                    "source_role_family": best.get("role_family") or "",
                }]
                row["last_verified"] = today

    verified_index["schema_version"] = max(2, int(verified_index.get("schema_version") or 1))
    verified_index["generated_at"] = today
    VERIFIED_INDEX.write_text(
        json.dumps(verified_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    # Persistent VERIFIED_ROLE entries are a minimum role-presence invariant inside the larger company scan pool.
    # Runtime discovery may upgrade these entries to first-party full JDs, but
    # may never delete them merely because the crawler missed the role.
    for company_row in verified_index.get("companies") or []:
        company = company_row.get("company")
        roles = company_row.get("representative_roles") or []
        if not company or company_row.get("status") != "VERIFIED_ROLE" or not roles:
            continue
        role = roles[0]
        family = txt(role.get("title"))
        if not family:
            continue
        key = (company, family)
        if key in current_keys:
            continue
        official_url = txt(role.get("official_apply_url") or company_row.get("official_search_url"))
        role_families.append({
            "company": company,
            "role_family": family,
            "representative_title": family,
            "locations": [],
            "description": "",
            "requirements": "",
            "evidence_summary": txt(role.get("jd_summary")),
            "cycle_evidence": txt(role.get("recruitment_type")),
            "requisitions": [{
                "job_id": "",
                "title": family,
                "location": "",
                "official_url": official_url,
                "official_api": "",
            }],
            "source_evidence": [txt(role.get("evidence_type") or "VERIFIED_ROLE_INDEX")],
            "evidence_url": txt(role.get("evidence_url")),
            "detail_status": "ROLE_VERIFIED_CURRENT_SOURCE",
            "persistent_verified_role": True,
        })
        current_keys.add(key)

    role_families.sort(key=lambda x: (x["company"], x["role_family"]))

    family_counts: dict[str, list[dict[str, Any]]] = {}
    for f in role_families:
        family_counts.setdefault(f["company"], []).append(f)

    source_rows = []
    for src in cfg["sources"]:
        company = src["company"]
        r = result_map.get(company)
        fams = family_counts.get(company, [])
        source_rows.append({
            "company": company,
            "mode": r.mode if r else src.get("mode", ""),
            "retrieval_status": r.status if r else "MISSING_RESULT",
            "fetched": r.fetched if r else 0,
            "matched_requisitions": r.matched if r else 0,
            "error": r.error if r else "source returned no result",
            "official_root": src.get("official_root", ""),
            "search_url": src.get("search_url") or src.get("job_list_url") or "",
            "board_scope": src.get("board_scope") or ("campus" if src.get("current_campus_board") else "official_recruiting"),
            "result_status": (
                "HAS_TARGET_JDS" if fams
                else "ZERO_TARGET_JDS" if r and r.status == "ENUMERATED_ZERO_MATCHES"
                else "NEEDS_ENUMERATION"
            ),
            "role_family_count": len(fams),
            "full_jd_count": sum(f.get("detail_status") == "FULL_JD" for f in fams),
            "title_only_count": sum(f.get("detail_status") == "TITLE_ONLY_OFFICIAL" for f in fams),
            "role_verified_current_source_count": sum(
                f.get("detail_status") == "ROLE_VERIFIED_CURRENT_SOURCE" for f in fams
            ),
            "verified_representative_role": next(
                (
                    txt((x.get("representative_roles") or [{}])[0].get("title"))
                    for x in verified_index.get("companies") or []
                    if x.get("company") == company
                ),
                "",
            ),
        })

    counts = {
        "companies": len(source_rows),
        "companies_with_targets": sum(x["result_status"] == "HAS_TARGET_JDS" for x in source_rows),
        "companies_zero_targets": sum(x["result_status"] == "ZERO_TARGET_JDS" for x in source_rows),
        "companies_needing_enumeration": sum(x["result_status"] == "NEEDS_ENUMERATION" for x in source_rows),
        "role_families": len(role_families),
        "full_jd_families": sum(f.get("detail_status") == "FULL_JD" for f in role_families),
        "title_only_families": sum(f.get("detail_status") == "TITLE_ONLY_OFFICIAL" for f in role_families),
        "role_verified_current_source_families": sum(
            f.get("detail_status") == "ROLE_VERIFIED_CURRENT_SOURCE" for f in role_families
        ),
        "raw_requisitions": len(all_matches),
    }
    payload = {
        "schema_version": 1,
        "generated_at": now,
        "cycle": cfg["cycle"],
        "scope": "current official campus/new-grad non-algorithm AI application & Agent engineering",
        "methodology": {
            "inclusion": "First-party official source + current campus/new-grad eligibility + explicit engineering title materially about Agent/AI application/RAG/Harness/Runtime/Infra/Coding Agent.",
            "exclusion": "Algorithm/model-training/research, product, sales, operations, marketing, internship-only and generic engineering jobs that merely mention AI tooling.",
            "role_family": "Same-company near-identical titles are grouped while every official requisition remains attached.",
            "detail_status": "FULL_JD = first-party duties/requirements captured; TITLE_ONLY_OFFICIAL = first-party title only; ROLE_VERIFIED_CURRENT_SOURCE = current role presence verified and official application/search entry fixed, first-party body still being backfilled.",
            "zero_miss_policy": "Company membership is independent from job presence. Crawler miss/failure may not erase persistent verified role presence; ZERO_TARGET_JDS is valid only after complete official enumeration.",
        },
        "counts": counts,
        "sources": source_rows,
        "role_families": role_families,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 当前官方校招 / 应届｜非算法 AI 应用 & Agent 工程 JD 全量结果",
        "",
        f"> Generated: **{now}**",
        f"> 固定长期扫描公司 **{counts['companies']}** 家；当前有目标岗位 **{counts['companies_with_targets']}** 家；完整枚举确认 0 岗 **{counts['companies_zero_targets']}** 家；仍待完整枚举 **{counts['companies_needing_enumeration']}** 家。",
        f"> 其中 **{counts['full_jd_families']}** 个抓到第一方 JD 正文，**{counts['title_only_families']}** 个仅能确认第一方职位标题，**{counts['role_verified_current_source_families']}** 个已核验岗位存在并固定官方入口、正文仍待补齐。",
        "",
        "## 1. 公司结果总表",
        "",
        "| 公司 | Retrieval | 官方职位池 | 结果 | Role Family | 完整 JD | 仅标题 |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for s in source_rows:
        status = s["retrieval_status"]
        if s["error"]:
            status += "；" + s["error"].replace("|", "\\|")
        lines.append(
            f"| {s['company']} | {status} | {s['search_url']} | {s['result_status']} | "
            f"{s['role_family_count']} | {s['full_jd_count']} | {s['title_only_count']} |"
        )

    lines += ["", "## 2. 严格 Role Family", ""]
    last_company = ""
    for f in role_families:
        if f["company"] != last_company:
            last_company = f["company"]
            lines += [f"## {last_company}", ""]
        lines += [
            f"### {f['role_family']}",
            "",
            f"- **证据状态**：{f['detail_status']}",
            f"- **地点**：{' / '.join(f['locations']) or '官方未提供'}",
            f"- **项目 / 届别**：{f['cycle_evidence'] or '当前官方招聘池 / 校招池'}",
            f"- **官方 Requisition**：{len(f['requisitions'])} 个",
        ]
        for req in f["requisitions"]:
            prefix = (f"`{req['job_id']}` · " if req.get("job_id") else "")
            loc = (f" · {req['location']}" if req.get("location") else "")
            url = (f" · {req['official_url']}" if req.get("official_url") else "")
            lines.append(f"  - {prefix}{req['title']}{loc}{url}")
        if f.get("evidence_url"):
            lines.append(f"- **岗位核验证据**：{f['evidence_url']}")
        if f.get("detail_status") == "FULL_JD":
            lines += ["", "**官方职责**", "", clean(f.get("description", ""), 6000) or "官方未返回职责正文。"]
            lines += ["", "**官方要求**", "", clean(f.get("requirements", ""), 6000) or "官方未返回任职要求。"]
        elif f.get("detail_status") == "ROLE_VERIFIED_CURRENT_SOURCE":
            lines += ["", "**已核验岗位摘要**", "", clean(f.get("evidence_summary", ""), 3000) or "岗位存在与官方投递入口已核验。"]
            lines += ["", "**JD 完整度**", "", "> 第一方职责 / 要求正文仍待回填；该摘要不冒充第一方完整 JD。"]
        else:
            lines += ["", "**JD 完整度**", "", "> 第一方当前职位列表已确认岗位标题；职责 / 要求正文尚未稳定取得，不用二手来源补写。"]
        lines.append("")

    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    # Keep human-readable company status files in lockstep with the JSON state.
    index_rows = {x.get("company"): x for x in verified_index.get("companies") or [] if x.get("company")}
    index_lines = [
        "# 69 家目标公司｜官方 AI / Agent 工程岗位状态索引",
        "",
        "> 公司扫描池与岗位存在性分离；状态只由第一方职位池完整枚举更新。",
        "",
        "| 公司 | 主要业务 | 官方职位池 | 状态 | 代表岗位 |",
        "|---|---|---|---|---|",
    ]
    pool_lines = [
        "# 目标公司扫描池｜69 家知名中大厂与 AI 公司",
        "",
        "> 公司进入扫描池不代表当前一定存在目标岗位；岗位是否存在由每轮第一方职位池完整枚举决定。",
        "",
        "| # | 公司 | 主要业务 | 第一方职位池 | 当前持久化状态 |",
        "|---:|---|---|---|---|",
    ]
    for n, source in enumerate(cfg.get("sources") or [], 1):
        company = source.get("company") or ""
        row = index_rows.get(company) or {}
        roles = row.get("representative_roles") or []
        representative = txt(roles[0].get("title")) if roles else ""
        business = txt(source.get("business_summary")).replace("|", "\\|")
        search_url = source.get("search_url") or source.get("job_list_url") or ""
        status = row.get("status") or "NEEDS_ENUMERATION"
        safe_company = company.replace("|", "\\|")
        safe_role = representative.replace("|", "\\|")
        index_lines.append(f"| {safe_company} | {business} | {search_url} | {status} | {safe_role} |")
        pool_lines.append(f"| {n} | {safe_company} | {business} | {search_url} | {status} |")
    index_lines += [
        "",
        "## 状态语义",
        "",
        "- VERIFIED_ROLE：本轮或历史完整第一方证据已核验目标工程岗位。",
        "- ZERO_TARGET_JDS：本轮完整第一方枚举后确认当前没有符合 Role Scope 的正式岗位。",
        "- NEEDS_ENUMERATION：尚未完成可靠完整枚举；不能解释为 0 岗。",
    ]
    pool_lines += [
        "",
        "## 状态语义",
        "",
        "- VERIFIED_ROLE：已有至少一个第一方核验的目标工程岗位事实。",
        "- ZERO_TARGET_JDS：本轮已完整枚举官方职位池，但当前没有符合 Role Scope 的正式岗位。",
        "- NEEDS_ENUMERATION：公司与第一方职位池已固定，但完整分页 / 关键词穷举尚未闭环。",
    ]
    VERIFIED_INDEX_MD.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    SCAN_POOL_MD.write_text("\n".join(pool_lines) + "\n", encoding="utf-8")

    print(
        f"official sources={len(results)}, requisitions={len(all_matches)}, "
        f"role_families={len(role_families)}"
    )
    for r in results:
        print(f"{r.company}: {r.status}, fetched={r.fetched}, matched={r.matched}, error={r.error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
