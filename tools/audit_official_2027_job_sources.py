#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit official 2027 campus retrieval coverage for every registered company."""

from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "market/jobs/official-2027-campus-sources.json"
NORM = ROOT / "market/jobs/official-2027-agent-jobs.generated.json"
BROWSER = ROOT / "market/jobs/official-2027-browser-discovery.generated.json"
FEISHU = ROOT / "market/jobs/official-2027-feishu-discovery.generated.json"
MOKA = ROOT / "market/jobs/official-2027-moka-discovery.generated.json"
OUT = ROOT / "market/jobs/official-2027-coverage-audit.generated.md"

TERMINAL = {"ENUMERATED_WITH_MATCHES", "ENUMERATED_ZERO_MATCHES", "NO_PUBLIC_2027_PROJECT"}

def read(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def main() -> int:
    reg = read(REG)
    norm = read(NORM)
    browser = read(BROWSER)
    feishu = read(FEISHU)
    moka = read(MOKA)
    sources = {x.get("company"): x for x in reg.get("sources", []) if x.get("company")}
    normalized = {x.get("company"): x for x in norm.get("sources", []) if x.get("company")}
    browsed = {x.get("company"): x for x in browser.get("results", []) if x.get("company")}
    fei = {x.get("company"): x for x in feishu.get("results", []) if x.get("company")}
    mok = {x.get("company"): x for x in moka.get("results", []) if x.get("company")}
    rows = []
    for company, src in sources.items():
        n = normalized.get(company, {})
        b = browsed.get(company, {})
        f = fei.get(company, {})
        m = mok.get(company, {})
        status = n.get("status") or "BLOCKED"
        reason = n.get("error") or ""
        fetched = int(n.get("fetched") or 0)
        matched = int(n.get("matched") or 0)

        # A browser run is a valid first-party enumerator when it both proves
        # the 2027 project and completes the full configured keyword search.
        b_status = b.get("status")
        b_has_2027 = bool(b.get("has2027"))
        b_full = bool(b.get("full_keyword_search"))
        b_jobs = b.get("jobs") or []
        if b_status == "BROWSER_ENUMERATED" and b_has_2027 and b_full:
            status = "ENUMERATED_WITH_MATCHES" if b_jobs else "ENUMERATED_ZERO_MATCHES"
            fetched = max(fetched, len(b_jobs))
            matched = max(matched, len(b_jobs))
            reason = "official browser completed full 2027 keyword enumeration"
        elif b_status == "BROWSER_ENUMERATED_ZERO" and b_has_2027 and b_full:
            status = "ENUMERATED_ZERO_MATCHES"
            reason = "official browser completed full 2027 keyword enumeration; 0 target jobs"
        elif b_status == "BROWSER_NO_2027_EVIDENCE" and src.get("allow_no_public_2027"):
            status = "NO_PUBLIC_2027_PROJECT"
            reason = "official root exhaustively checked; no public 2027 project exposed"

        if status not in TERMINAL:
            if f.get("status") == "OK" and f.get("jobs") and src.get("verified_2027_project"):
                status = "DISCOVERED_NEEDS_NORMALIZATION"
                reason = "official Feishu 2027 pool discovered: %s jobs" % len(f.get("jobs") or [])
            elif m.get("status") == "OK" and m.get("jobs") and src.get("verified_2027_project"):
                status = "DISCOVERED_NEEDS_NORMALIZATION"
                reason = "official Moka 2027 pool discovered: %s jobs" % len(m.get("jobs") or [])
            elif b_jobs:
                status = "DISCOVERED_NEEDS_ADAPTER"
                reason = "official browser extracted %s target-shaped records; exhaustive 2027 enumeration not yet proven" % len(b_jobs)
            elif b_has_2027:
                status = "BLOCKED"
                reason = reason or "official 2027 project found, but full keyword/job-detail enumeration is incomplete"
            else:
                status = "BLOCKED"
                reason = reason or "official root exists, but public 2027 job pool is not yet proven"

        rows.append({
            "company": company, "status": status,
            "root": src.get("official_root") or src.get("portal") or "",
            "portal": src.get("portal") or "",
            "fetched": fetched, "matched": matched,
            "reason": reason.replace("|", "/").replace("\\n", " ")[:240],
        })
    counts = Counter(r["status"] for r in rows)
    blocked = [r for r in rows if r["status"] not in TERMINAL]
    out = [
        "# 2027 校招官方岗位源覆盖审计", "",
        "- 固定公司：**%d**" % len(rows),
        "- 已形成终态：**%d**" % (len(rows) - len(blocked)),
        "- 尚未闭环：**%d**" % len(blocked), "",
        "只有 ENUMERATED_WITH_MATCHES、ENUMERATED_ZERO_MATCHES、NO_PUBLIC_2027_PROJECT 算闭环。",
        "BLOCKED / DISCOVERED_* 不能被解释成 0 个岗位。", "",
        "## 状态统计", ""
    ]
    for k, v in sorted(counts.items()):
        out.append("- %s：%d" % (k, v))
    out += ["", "## 逐公司", "", "| 公司 | 状态 | 拉取岗位 | 目标候选 | 官方根入口 | 实际职位入口 | 说明 |", "|---|---|---:|---:|---|---|---|"]
    for r in rows:
        out.append("| {company} | {status} | {fetched} | {matched} | {root} | {portal} | {reason} |".format(**r))
    out += ["", "## 尚未闭环公司", ""]
    if blocked:
        for r in blocked:
            out.append("- **%s** — %s：%s" % (r["company"], r["status"], r["reason"]))
    else:
        out.append("- 无。固定覆盖矩阵已全部闭环。")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("companies=%d terminal=%d blocked=%d" % (len(rows), len(rows)-len(blocked), len(blocked)))
    for r in blocked:
        print("BLOCKED %s: %s %s" % (r["company"], r["status"], r["reason"]))
    return 0 if not blocked else 2

if __name__ == "__main__":
    raise SystemExit(main())
