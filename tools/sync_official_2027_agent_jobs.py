#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync 2027-campus Agent/AI-application engineering candidates from first-party recruitment endpoints.

This tool is discovery-only: it only calls company-owned recruitment APIs/portals listed in
market/jobs/official-2027-campus-sources.json. It never imports JD text from aggregators.
Portal-only companies remain in the coverage matrix for manual official-site review.
"""

from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "market/jobs/official-2027-campus-sources.json"
OUT_MD = ROOT / "market/jobs/official-2027-agent-jobs.generated.md"
OUT_JSON = ROOT / "market/jobs/official-2027-agent-jobs.generated.json"
BROWSER_CACHE = ROOT / "market/jobs/official-2027-browser-discovery.generated.json"
FEISHU_CACHE = ROOT / "market/jobs/official-2027-feishu-discovery.generated.json"
MOKA_CACHE = ROOT / "market/jobs/official-2027-moka-discovery.generated.json"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}
TIMEOUT = 12


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


def is_agent_related(job: Job, keywords: list[str]) -> bool:
    s = blob(job)
    return any(k.lower() in s for k in keywords)


def looks_engineering(job: Job, signals: list[str]) -> bool:
    title = job.title.lower()
    return any(s.lower() in title for s in signals)


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
    s = f"{job.category} {job.cycle_evidence} {job.title}".lower()
    return any(k in s for k in ["校招", "校园", "graduate", "campus", "2027", "应届"])


def clean(s: str, limit: int = 1600) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:limit]


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
    cache = Path("/tmp/xiaomi-2027-campus.json")
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
    cache = Path("/tmp/bytedance-campus.json")
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
                src["company"], txt(row.get("positionTitle")), pid,
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


FETCHERS: dict[str, Callable[[dict], list[Job]]] = {
    "xiaomi_api": fetch_xiaomi,
    "bytedance_api": fetch_bytedance,
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
    "bilibili_api": fetch_bilibili,
    "didi_api": fetch_didi,
    "pdd_api": fetch_pdd,
    "huawei_api": fetch_huawei,
}


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    keywords = [x.lower() for x in cfg.get("strong_agent_keywords", cfg["agent_keywords"])]
    excludes = [x.lower() for x in cfg["hard_exclude_title_keywords"]]
    engineering_signals = [x.lower() for x in cfg.get("engineering_title_signals", [])]

    all_matches: list[Job] = []
    results: list[SourceResult] = []

    dynamic_by_company: dict[str, dict] = {}
    if BROWSER_CACHE.exists():
        try:
            browser_payload = json.loads(BROWSER_CACHE.read_text(encoding="utf-8"))
            dynamic_by_company = {
                x.get("company"): x
                for x in (browser_payload.get("results") or [])
                if x.get("company")
            }
        except Exception as e:
            print(f"browser discovery cache parse warning: {e}", file=sys.stderr)

    feishu_by_company: dict[str, dict] = {}
    if FEISHU_CACHE.exists():
        try:
            feishu_payload = json.loads(FEISHU_CACHE.read_text(encoding="utf-8"))
            feishu_by_company = {
                x.get("company"): x
                for x in (feishu_payload.get("results") or [])
                if x.get("company")
            }
        except Exception as e:
            print(f"feishu discovery cache parse warning: {e}", file=sys.stderr)

    moka_by_company: dict[str, dict] = {}
    if MOKA_CACHE.exists():
        try:
            moka_payload = json.loads(MOKA_CACHE.read_text(encoding="utf-8"))
            moka_by_company = {
                x.get("company"): x
                for x in (moka_payload.get("results") or [])
                if x.get("company")
            }
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

    def target_matches(jobs: list[Job], source_verified_2027: bool = False) -> list[Job]:
        def is_2027(j: Job) -> bool:
            if source_verified_2027:
                return True
            evidence = " ".join([
                j.title or "", j.category or "", j.cycle_evidence or "",
                j.description or "", j.requirements or ""
            ]).lower()
            return "2027" in evidence

        matches = [
            j for j in jobs
            if campusish(j)
            and is_2027(j)
            and is_agent_related(j, keywords)
            and (not engineering_signals or looks_engineering(j, engineering_signals))
            and not is_hard_excluded(j, excludes)
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
        if feishu.get("status") == "OK" and (feishu.get("jobs") or []):
            jobs = to_jobs(company, feishu.get("jobs") or [], src["portal"], "FEISHU:" + src["portal"])
            matches = target_matches(jobs, bool(src.get("verified_2027_project")))
            return SourceResult(
                company, "feishu_official", src["portal"],
                "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                len(jobs), len(matches)
            ), matches

        moka = moka_by_company.get(company) or {}
        if moka.get("status") == "OK":
            jobs = to_jobs(company, moka.get("jobs") or [], src["portal"], txt(moka.get("api")) or ("MOKA:" + src["portal"]))
            matches = target_matches(jobs, bool(src.get("verified_2027_project")))
            cycle = txt(moka.get("cycle_evidence"))
            has_2027 = "2027" in cycle or any("2027" in (j.cycle_evidence or "") for j in jobs)
            if has_2027:
                return SourceResult(
                    company, "moka_official", src["portal"],
                    "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                    len(jobs), len(matches)
                ), matches

        if mode == "portal_only":
            dyn = dynamic_by_company.get(company) or {}
            raw_jobs = dyn.get("jobs") or []
            jobs = to_jobs(company, raw_jobs, src["portal"], "BROWSER:" + src["portal"])
            matches = target_matches(jobs, bool(src.get("verified_2027_project")))
            raw_status = txt(dyn.get("status"))
            has_2027 = bool(dyn.get("has2027"))
            full_search = bool(dyn.get("full_keyword_search"))
            if raw_status == "BROWSER_ENUMERATED":
                status = "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES"
                error = ""
            elif raw_status == "BROWSER_ENUMERATED_ZERO" and has_2027 and full_search:
                status = "ENUMERATED_ZERO_MATCHES"
                error = ""
            elif raw_status == "BROWSER_NO_2027_EVIDENCE":
                status = "NO_PUBLIC_2027_PROJECT" if src.get("allow_no_public_2027") else "BLOCKED"
                error = "官方根站未取得公开2027项目证据" if status == "NO_PUBLIC_2027_PROJECT" else "官网浏览完成但未能证明无公开2027项目；继续适配"
            elif raw_status in ("BROWSER_2027_NEEDS_ADAPTER","BROWSER_OK_0_MATCH"):
                status = "BLOCKED"
                error = "发现2027官方项目，但尚未完成全关键词/职位详情枚举；不能判0"
            elif raw_status == "BROWSER_ERROR":
                status = "BLOCKED"
                error = txt(dyn.get("error")) or "浏览器枚举失败"
            else:
                status = "BLOCKED"
                error = "官方根入口存在，但尚未完成可靠的2027岗位池枚举"
            return SourceResult(company, "browser_dynamic", src["portal"], status, len(raw_jobs), len(matches), error), matches
        fetcher = FETCHERS.get(mode)
        if not fetcher:
            return SourceResult(company, mode, src["portal"], "NO_FETCHER", 0, 0), []
        try:
            jobs = fetcher(src)
            source_verified = bool(src.get("verified_2027_project"))
            uniq = target_matches(jobs, source_verified)
            explicit_2027 = source_verified or any(
                "2027" in " ".join([
                    j.title or "", j.category or "", j.cycle_evidence or "",
                    j.description or "", j.requirements or ""
                ])
                for j in jobs
            )
            if not explicit_2027:
                return SourceResult(
                    company, mode, src["portal"], "BLOCKED", len(jobs), len(uniq),
                    "官方职位池已取回，但尚未证明当前枚举范围属于2027；不能判定0岗位"
                ), uniq
            status = "ENUMERATED_WITH_MATCHES" if uniq else "ENUMERATED_ZERO_MATCHES"
            return SourceResult(company, mode, src["portal"], status, len(jobs), len(uniq)), uniq
        except Exception as e:
            # Dedicated adapter failure never means "0 jobs". If browser discovery
            # succeeded from the company's official root / ATS chain, use it as a
            # first-party fallback; otherwise keep the source explicitly BLOCKED.
            dyn = dynamic_by_company.get(company) or {}
            raw_jobs = dyn.get("jobs") or []
            browser_terminal = (
                bool(dyn.get("has2027"))
                and bool(dyn.get("full_keyword_search"))
                and txt(dyn.get("status")) == "BROWSER_ENUMERATED"
            )
            if raw_jobs and browser_terminal:
                browser_jobs = to_jobs(company, raw_jobs, src["portal"], "BROWSER:" + src["portal"])
                matches = target_matches(browser_jobs, bool(src.get("verified_2027_project")))
                return SourceResult(
                    company, "browser_fallback", src["portal"],
                    "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                    len(raw_jobs), len(matches),
                    f"dedicated adapter failed; exhaustive official 2027 browser fallback used: {type(e).__name__}: {e}"[:700],
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

    results.sort(key=lambda r: r.company)

    all_matches.sort(key=lambda j: (j.company, j.title, j.location, j.job_id))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    payload = {
        "generated_at": now,
        "cycle": cfg["cycle"],
        "jobs": [asdict(j) for j in all_matches],
        "sources": [asdict(x) for x in results],
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 2027 校招｜官方 Agent / AI 应用工程岗位自动发现结果",
        "",
        f"> Generated: **{now}**",
        ">",
        "> 仅调用公司官方招聘接口 / 官方招聘入口。对于动态站，浏览器从 registry 中记录的 **official_root** 出发，跟随官网自己的校招链接并监听第一手 XHR/JSON。该文件是 discovery layer；最终 Active JD 仍需确认岗位属于 2027 校招且职责主体不是算法/模型训练。",
        "",
        "## 官方源执行状态",
        "",
        "| 公司 | 模式 | 状态 | 拉取岗位 | Agent相关非算法候选 | 官方入口 |",
        "|---|---|---:|---:|---:|---|",
    ]
    for r in results:
        err = ("；" + r.error.replace("|", "\\|")) if r.error else ""
        lines.append(f"| {r.company} | {r.mode} | {r.status}{err} | {r.fetched} | {r.matched} | {r.portal} |")

    lines += ["", "## 自动发现候选", ""]
    if not all_matches:
        lines.append("> 本轮官方 API 未返回匹配候选；请查看上方 ERROR / PORTAL_ONLY 状态，并继续从官方校园招聘入口人工核验。")
    for j in all_matches:
        lines += [
            f"### {j.company}｜{j.title}" + (f"（{j.job_id}）" if j.job_id else ""),
            "",
            f"- 地点：{j.location or '官方未提供'}",
            f"- 招聘类型：{j.category or '官方未提供'}",
            f"- 部门/方向：{j.department or '官方未提供'}",
            f"- 2027/校招证据：{j.cycle_evidence or '需人工确认'}",
            f"- 官方职位页：{j.official_url}",
            f"- 官方接口：{j.official_api}",
            "",
            "**职责（官方接口）**",
            "",
            clean(j.description) or "官方接口未返回职责正文。",
            "",
            "**要求（官方接口）**",
            "",
            clean(j.requirements) or "官方接口未返回任职要求正文。",
            "",
        ]

    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"official sources={len(results)}, candidates={len(all_matches)}")
    for r in results:
        print(f"{r.company}: {r.status}, fetched={r.fetched}, matched={r.matched}, error={r.error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
