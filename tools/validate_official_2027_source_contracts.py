#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static contract validation for official current-campus job sources."""

from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "market/jobs/official-2027-campus-sources.json"
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
    sources = cfg.get("sources") or []
    sync = SYNC.read_text(encoding="utf-8")
    errors: list[str] = []
    names = [s.get("company") for s in sources]

    if len(names) != len(set(names)):
        errors.append("duplicate company in official source registry")
    missing = REQUIRED - set(names)
    if missing:
        errors.append("missing fixed companies: " + ", ".join(sorted(missing)))

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
