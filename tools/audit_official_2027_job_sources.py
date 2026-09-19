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
    sources = {x.get("company"): x for x in reg.get("sources", []) if x.get("company")}
    normalized = {x.get("company"): x for x in norm.get("sources", []) if x.get("company")}
    browsed = {x.get("company"): x for x in browser.get("results", []) if x.get("company")}
    fei = {x.get("company"): x for x in feishu.get("results", []) if x.get("company")}
    rows = []
    for company, src in sources.items():
        n = normalized.get(company, {})
        b = browsed.get(company, {})
        f = fei.get(company, {})
        status = n.get("status") or "BLOCKED"
        reason = n.get("error") or ""
        if status not in TERMINAL:
            if f.get("status") == "OK" and f.get("jobs"):
                status = "DISCOVERED_NEEDS_NORMALIZATION"
                reason = "official Feishu pool discovered: %s jobs" % len(f.get("jobs") or [])
            elif b.get("jobs"):
                status = "DISCOVERED_NEEDS_ADAPTER"
                reason = "official browser extracted: %s target-shaped records" % len(b.get("jobs") or [])
            elif b.get("has2027"):
                status = "BLOCKED"
                reason = reason or "official 2027 project found, but full job pool is not reliably enumerated"
            else:
                status = "BLOCKED"
                reason = reason or "official root exists, but public 2027 job pool is not yet proven"
        rows.append({
            "company": company, "status": status,
            "root": src.get("official_root") or src.get("portal") or "",
            "portal": src.get("portal") or "",
            "fetched": n.get("fetched", 0), "matched": n.get("matched", 0),
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
