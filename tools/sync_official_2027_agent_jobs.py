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
            detail = {}
            if pid:
                try:
                    detail_payload = get_json(detail_api, params={"positionId": pid}, headers=headers)
                    detail = detail_payload.get("data") or {}
                except Exception:
                    detail = {}
            title = txt(detail.get("positionName") or row.get("positionName"))
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
                src["company"], txt(detail.get("jobname") or row.get("jobname")), jid,
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
                src["company"], txt(detail.get("postName") or row.get("postName")), pid,
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
    "bilibili_api": fetch_bilibili_2027,
    "xiaohongshu_2027_api": fetch_xiaohongshu_2027,
    "ant_2027_api": fetch_ant_2027,
    "vivo_2027_api": fetch_vivo_2027,
    "iflytek_2027_api": fetch_iflytek_2027,
    "ctrip_2027_api": fetch_ctrip_2027,
    "honor_2027_api": fetch_honor_2027,
    "didi_api": fetch_didi,
    "pdd_api": fetch_pdd,
    "huawei_api": fetch_huawei_2027,
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
        if feishu.get("status") == "OK":
            jobs = to_jobs(company, feishu.get("jobs") or [], src["portal"], "FEISHU:" + src["portal"])
            matches = target_matches(jobs, bool(src.get("verified_2027_project")))
            feishu_has_2027 = bool(src.get("verified_2027_project")) or any(
                "2027" in " ".join([
                    j.title or "", j.category or "", j.cycle_evidence or "",
                    j.description or "", j.requirements or ""
                ])
                for j in jobs
            )
            if feishu_has_2027:
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
            has_2027 = bool(src.get("verified_2027_project")) or "2027" in cycle or any(
                "2027" in " ".join([
                    j.title or "", j.category or "", j.cycle_evidence or "",
                    j.description or "", j.requirements or ""
                ])
                for j in jobs
            )
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
            has_2027 = bool(src.get("verified_2027_project")) or bool(dyn.get("has2027"))
            full_search = bool(dyn.get("full_keyword_search")) or bool(dyn.get("list_scan_complete"))
            if raw_status == "BROWSER_ENUMERATED":
                status = "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES"
                error = ""
            elif raw_status == "BROWSER_ENUMERATED_ZERO" and has_2027 and full_search:
                status = "ENUMERATED_ZERO_MATCHES"
                error = ""
            elif raw_status == "BROWSER_NO_PUBLIC_2027":
                status = "NO_PUBLIC_2027_PROJECT" if src.get("allow_no_public_2027") else "BLOCKED"
                error = (
                    "固定官方招聘入口已完整巡检，未公开2027校园招聘项目"
                    if status == "NO_PUBLIC_2027_PROJECT"
                    else "官网未发现2027证据，但该公司仍有校园/招聘入口，不能直接判定无公开2027项目"
                )
            elif raw_status == "BROWSER_NO_2027_EVIDENCE":
                status = "NO_PUBLIC_2027_PROJECT" if src.get("allow_no_public_2027") else "BLOCKED"
                error = "官方根站未取得公开2027项目证据" if status == "NO_PUBLIC_2027_PROJECT" else "官网存在访问异常，尚不能判断2027项目状态"
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
                (bool(src.get("verified_2027_project")) or bool(dyn.get("has2027")))
                and (bool(dyn.get("full_keyword_search")) or bool(dyn.get("list_scan_complete")))
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
