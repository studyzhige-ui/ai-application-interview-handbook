#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static contract validation for official current-campus job sources."""

from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "market/jobs/official-2027-campus-sources.json"
INDEX = ROOT / "market/jobs/official-company-role-index.json"
SYNC = ROOT / "tools/sync_official_2027_agent_jobs.py"

BANNED = {
    "nowcoder.com", "zhipin.com", "liepin.com", "zhaopin.com", "shixiseng.com",
    "jdwatch.work", "niuqizp.com", "ultraai.site", "datahub.ac.cn",
}
REQUIRED = {
    "字节跳动","阿里巴巴","蚂蚁集团","腾讯","百度","美团","京东","拼多多","快手",
    "小红书","哔哩哔哩","网易","携程","滴滴","小米","华为","OPPO","vivo","360",
    "金山办公/WPS","荣耀","得物","Shopee","联想","蔚来","顺丰","DeepSeek",
    "月之暗面/Kimi","MiniMax","智谱/Z.ai","阶跃星辰","百川智能","零一万物/01.AI",
    "商汤科技","科大讯飞","生数科技","硅基流动","面壁智能","Manus",
    "无问芯穹/Infini-AI","昆仑万维/天工",
}

def host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")

def main() -> int:
    cfg = json.loads(REG.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    sources = cfg.get("sources") or []
    sync = SYNC.read_text(encoding="utf-8")
    errors: list[str] = []
    names = [s.get("company") for s in sources]

    if len(names) != len(set(names)):
        errors.append("duplicate company in official source registry")
    registered = set(names)
    missing = REQUIRED - registered
    extra = registered - REQUIRED
    if missing:
        errors.append("missing fixed companies: " + ", ".join(sorted(missing)))
    if extra:
        errors.append("unexpected companies outside fixed corpus: " + ", ".join(sorted(extra)))
    if len(names) != len(REQUIRED):
        errors.append(f"official source registry must contain exactly {len(REQUIRED)} companies; got {len(names)}")

    index_rows = index.get("companies") or []
    index_names = [x.get("company") for x in index_rows]
    if set(index_names) != REQUIRED or len(index_names) != len(REQUIRED):
        errors.append("verified role index must contain exactly the fixed 41 companies")
    index_by_company = {x.get("company"): x for x in index_rows if x.get("company")}
    for company in sorted(REQUIRED):
        row = index_by_company.get(company) or {}
        roles = row.get("representative_roles") or []
        if row.get("status") != "VERIFIED_ROLE":
            errors.append(f"{company}: verified role index status must be VERIFIED_ROLE")
        if not (row.get("official_search_url") or "").startswith("https://"):
            errors.append(f"{company}: verified role index official_search_url missing/invalid")
        if not roles or not (roles[0].get("title") or "").strip():
            errors.append(f"{company}: verified role index representative role missing")

    for s in sources:
        company = s.get("company") or "<unknown>"
        root = s.get("official_root") or ""
        jobs = s.get("job_list_url") or ""
        mode = s.get("mode") or ""
        state = s.get("campus_entry_status")
        search_url = s.get("search_url") or s.get("job_list_url") or ""
        board_scope = s.get("board_scope") or ("campus" if s.get("current_campus_board") else "official_recruiting")

        if not root.startswith("https://"):
            errors.append(f"{company}: official_root missing/invalid")
        for label, url in (("official_root", root), ("job_list_url", jobs),
                           ("search_url", search_url)):
            if not url:
                continue
            if not url.startswith("https://"):
                errors.append(f"{company}: {label} missing/invalid")
                continue
            h = host(url)
            if any(h == b or h.endswith("." + b) for b in BANNED):
                errors.append(f"{company}: {label} uses banned second-hand domain {h}")

        if state not in {"PUBLIC_CAMPUS_BOARD", "PUBLIC_OFFICIAL_BOARD"}:
            errors.append(f"{company}: invalid/missing campus_entry_status")
        if board_scope not in {"campus", "official_recruiting"}:
            errors.append(f"{company}: invalid/missing board_scope")
        if not search_url:
            errors.append(f"{company}: every company must define enumerable search_url")
        if search_url != jobs:
            errors.append(f"{company}: job_list_url must equal search_url")
        if board_scope == "campus" and s.get("current_campus_board") is not True:
            errors.append(f"{company}: campus board requires current_campus_board=true")
        if board_scope == "official_recruiting" and s.get("current_campus_board") is not False:
            errors.append(f"{company}: official recruiting board requires current_campus_board=false")

        idx = index_by_company.get(company) or {}
        if idx.get("official_search_url") != search_url:
            errors.append(f"{company}: registry search_url and verified role index official_search_url diverge")

        if mode != "portal_only":
            token = f'"{mode}":'
            if token not in sync:
                errors.append(f"{company}: mode {mode} has no sync fetcher")

    print(f"Official current-campus source contracts: companies={len(sources)}, errors={len(errors)}")
    for e in errors:
        print("ERROR:", e)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
