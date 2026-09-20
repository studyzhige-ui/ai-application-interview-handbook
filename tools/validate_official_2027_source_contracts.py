#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static contract validation for the fixed official company scan pool."""

from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "market/jobs/official-2027-campus-sources.json"
INDEX = ROOT / "market/jobs/official-company-role-index.json"
SYNC = ROOT / "tools/sync_official_2027_agent_jobs.py"
SEEDS = ROOT / "market/jobs/official-first-party-role-seeds.json"

BANNED = {
    "nowcoder.com", "liepin.com", "zhaopin.com", "shixiseng.com",
    "jdwatch.work", "niuqizp.com", "ultraai.site", "datahub.ac.cn",
}
ALLOWED_INDEX_STATUS = {"VERIFIED_ROLE", "ZERO_TARGET_JDS", "NEEDS_ENUMERATION"}

def host(url: str) -> str:
    return (urlparse(url).hostname or "").lower().removeprefix("www.")

def main() -> int:
    cfg = json.loads(REG.read_text(encoding="utf-8"))
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    sources = cfg.get("sources") or []
    expected = int(cfg.get("expected_company_count") or 0)
    sync = SYNC.read_text(encoding="utf-8")
    errors: list[str] = []
    names = [s.get("company") for s in sources]

    if not expected:
        errors.append("expected_company_count missing")
    if len(names) != len(set(names)):
        errors.append("duplicate company in official source registry")
    if len(names) != expected:
        errors.append(f"official source registry must contain exactly {expected} companies; got {len(names)}")

    index_rows = index.get("companies") or []
    index_names = [x.get("company") for x in index_rows]
    if set(index_names) != set(names) or len(index_names) != len(names):
        errors.append("company role-state index must contain exactly the same companies as the scan registry")
    index_by_company = {x.get("company"): x for x in index_rows if x.get("company")}

    for s in sources:
        company = s.get("company") or "<unknown>"
        root = s.get("official_root") or ""
        jobs = s.get("job_list_url") or ""
        mode = s.get("mode") or ""
        state = s.get("campus_entry_status")
        search_url = s.get("search_url") or jobs
        board_scope = s.get("board_scope") or ("campus" if s.get("current_campus_board") else "official_recruiting")

        if not root.startswith("https://"):
            errors.append(f"{company}: official_root missing/invalid")
        for label, url in (("official_root", root), ("job_list_url", jobs), ("search_url", search_url)):
            if not url:
                errors.append(f"{company}: {label} missing")
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
        if search_url != jobs:
            errors.append(f"{company}: job_list_url must equal search_url")
        if board_scope == "campus" and s.get("current_campus_board") is not True:
            errors.append(f"{company}: campus board requires current_campus_board=true")
        if board_scope == "official_recruiting" and s.get("current_campus_board") is not False:
            errors.append(f"{company}: official recruiting board requires current_campus_board=false")

        idx = index_by_company.get(company) or {}
        status = idx.get("status")
        roles = idx.get("representative_roles") or []
        if status not in ALLOWED_INDEX_STATUS:
            errors.append(f"{company}: invalid role-state index status {status!r}")
        if (idx.get("official_search_url") or "") != search_url:
            errors.append(f"{company}: registry search_url and role-state index official_search_url diverge")
        if status == "VERIFIED_ROLE" and (not roles or not (roles[0].get("title") or "").strip()):
            errors.append(f"{company}: VERIFIED_ROLE requires at least one representative role")
        if status != "VERIFIED_ROLE" and roles:
            errors.append(f"{company}: non-VERIFIED_ROLE state must not carry representative roles")

        if mode != "portal_only":
            token = f'"{mode}":'
            if token not in sync:
                errors.append(f"{company}: mode {mode} has no sync fetcher")

    if SEEDS.exists():
        try:
            seed_payload = json.loads(SEEDS.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"manual first-party role seed parse error: {exc}")
            seed_payload = {"roles": []}
        for seed in seed_payload.get("roles") or []:
            company = seed.get("company") or ""
            title = (seed.get("title") or "").strip()
            url = seed.get("official_url") or seed.get("evidence_url") or ""
            if company not in set(names):
                errors.append(f"manual first-party role seed company outside scan pool: {company}")
            if not title:
                errors.append(f"{company}: manual first-party role seed title missing")
            if not url.startswith("https://"):
                errors.append(f"{company}: manual first-party role seed official_url missing/invalid")
            else:
                h = host(url)
                if any(h == b or h.endswith("." + b) for b in BANNED):
                    errors.append(f"{company}: manual first-party role seed uses banned domain {h}")

    print(f"Official company scan-pool contracts: companies={len(sources)}/{expected}, errors={len(errors)}")
    for e in errors:
        print("ERROR:", e)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
