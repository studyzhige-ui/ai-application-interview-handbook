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
    out = []
    page = 1
    while page <= 50:
        data = get_json(src["api"], params={"pageNum": page, "pageSize": 100})
        rows = (data.get("data") or {}).get("rows") or []
        if not rows:
            break
        for j in rows:
            out.append(Job(
                src["company"], txt(j.get("positionName")), txt(j.get("id")),
                txt(j.get("workCity")), txt(j.get("recruitType")), txt(j.get("deptName")),
                txt(j.get("requirement")), txt(j.get("description")),
                f"https://hr.xiaomi.com/position/{txt(j.get('id'))}", src["api"],
                txt(j.get("recruitType")),
            ))
        total = int((data.get("data") or {}).get("total") or 0)
        if page * 100 >= total:
            break
        page += 1
    return out


def fetch_kuaishou(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 50:
        params = {
            "page": page, "pageSize": 50, "workCity": "", "jobType": "",
            "recruitSubProjectCodes": src.get("project_code", ""),
        }
        data = get_json(src["api"], params=params)
        d = data.get("data") or {}
        rows = d.get("jobList") or []
        if not rows:
            break
        for j in rows:
            jid = txt(j.get("jobId"))
            out.append(Job(
                src["company"], txt(j.get("jobName")), jid,
                txt(j.get("workCity")), txt(j.get("jobType")), txt(j.get("deptName")),
                txt(j.get("jobResponsibility")), txt(j.get("jobRequirements")),
                src["portal"] + f"&jobId={jid}", src["api"],
                "2027 project=" + txt(src.get("project_code")),
            ))
        total = int(d.get("total") or 0)
        if page * 50 >= total:
            break
        page += 1
    return out


def fetch_baidu(src: dict) -> list[Job]:
    out = []
    page = 1
    while page <= 30:
        data = post_form(
            src["api"],
            data={"recruitType": "CAMPUS", "pageSize": 100, "curPage": page, "projectType": ""},
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
        if page * 100 >= total:
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


FETCHERS: dict[str, Callable[[dict], list[Job]]] = {
    "xiaomi_api": fetch_xiaomi,
    "kuaishou_api": fetch_kuaishou,
    "baidu_api": fetch_baidu,
    "tencent_api": fetch_tencent,
    "meituan_api": fetch_meituan,
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

    def collect(src: dict) -> tuple[SourceResult, list[Job]]:
        company = src["company"]
        mode = src["mode"]
        if mode == "portal_only":
            return SourceResult(company, mode, src["portal"], "PORTAL_ONLY", 0, 0), []
        fetcher = FETCHERS.get(mode)
        if not fetcher:
            return SourceResult(company, mode, src["portal"], "NO_FETCHER", 0, 0), []
        try:
            jobs = fetcher(src)
            matches = [
                j for j in jobs
                if campusish(j)
                and is_agent_related(j, keywords)
                and (not engineering_signals or looks_engineering(j, engineering_signals))
                and not is_hard_excluded(j, excludes)
            ]
            seen = set()
            uniq = []
            for j in matches:
                key = (j.company, j.job_id or j.title, j.location)
                if key in seen:
                    continue
                seen.add(key)
                uniq.append(j)
            return SourceResult(company, mode, src["portal"], "OK", len(jobs), len(uniq)), uniq
        except Exception as e:
            discovered = discover_api_candidates(src["portal"])
            diagnostic = f"{type(e).__name__}: {e}"
            if discovered:
                diagnostic += " | discovered: " + " ; ".join(discovered[:8])
            return SourceResult(
                company, mode, src["portal"], "ERROR", 0, 0,
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
        "> 仅调用公司官方招聘接口 / 官方招聘入口。该文件是 discovery layer；最终 Active JD 仍需确认岗位属于 2027 校招且职责主体不是算法/模型训练。",
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
