#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit first-party current-campus job retrieval coverage."""

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

def read(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def main() -> int:
    reg, norm, browser, feishu, moka = map(read, (REG, NORM, BROWSER, FEISHU, MOKA))
    ns = {x.get("company"): x for x in norm.get("sources", []) if x.get("company")}
    bs = {x.get("company"): x for x in browser.get("results", []) if x.get("company")}
    fs = {x.get("company"): x for x in feishu.get("results", []) if x.get("company")}
    ms = {x.get("company"): x for x in moka.get("results", []) if x.get("company")}
    rows = []
    terminal = {"ENUMERATED_WITH_MATCHES", "ENUMERATED_ZERO_MATCHES"}

    for src in reg.get("sources", []):
        company = src["company"]
        n, b, f, m = ns.get(company, {}), bs.get(company, {}), fs.get(company, {}), ms.get(company, {})
        scope = src.get("board_scope") or ("campus" if src.get("current_campus_board") else "official_recruiting")
        search_url = src.get("search_url") or src.get("job_list_url") or ""
        contract = "READY" if src.get("official_root") and search_url and src.get("job_list_url") == search_url else "BROKEN"
        browser_jobs = len(b.get("jobs") or [])
        ats_jobs = max(len(f.get("jobs") or []), len(m.get("jobs") or []))
        raw = b.get("status", "")
        full_search = bool(b.get("full_keyword_search")) or bool(b.get("list_scan_complete"))

        if n.get("status") in terminal:
            retrieval = "ENUMERATED"
        elif raw in {"BROWSER_ENUMERATED", "BROWSER_ENUMERATED_ZERO"} and full_search:
            retrieval = "ENUMERATED"
        elif (browser_jobs or ats_jobs) and full_search:
            retrieval = "ENUMERATED"
        elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []) and full_search:
            retrieval = "ENUMERATED"
        elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []):
            retrieval = "LIST_REACHABLE"
        else:
            retrieval = "BLOCKED"

        rows.append(dict(
            company=company, scope=scope, contract=contract, retrieval=retrieval,
            fetched=int(n.get("fetched") or 0), matched=int(n.get("matched") or 0),
            root=src.get("official_root") or "", jobs=search_url,
        ))

    cc = Counter(r["contract"] for r in rows)
    cr = Counter(r["retrieval"] for r in rows)
    incomplete = [r for r in rows if r["contract"] != "READY" or r["retrieval"] != "ENUMERATED"]

    out = [
        "# 官方招聘岗位源全覆盖审计", "",
        "> 完成标准：每家公司必须有可枚举的第一方招聘职位池，并完成完整分页/站内关键词穷举。公司首页、页面可达、接口存在都不算完成。", "",
        f"- 固定公司：**{len(rows)}**",
        f"- 可枚举路径 READY：**{cc.get('READY',0)}/{len(rows)}**",
        f"- 已完成职位池枚举：**{cr.get('ENUMERATED',0)}/{len(rows)}**",
        f"- 仍未打通：**{len(incomplete)}**", "",
        "## 逐公司", "",
        "| 公司 | 招聘池范围 | 路径契约 | Retrieval | 上次拉取 | 目标候选 | 官方根入口 | 固定职位池 |",
        "|---|---|:---:|---|---:|---:|---|---|",
    ]
    for r in rows:
        out.append("| {company} | {scope} | {contract} | {retrieval} | {fetched} | {matched} | {root} | {jobs} |".format(**r))

    out += ["", "## 验收规则", "",
        "- ENUMERATED：已经对固定第一方职位池完成站内关键词搜索或完整列表分页，并能明确得出目标岗位集合（包括合法的 0 个）。",
        "- LIST_REACHABLE：页面能打开但搜索/分页未跑完；仍属于未完成。",
        "- BLOCKED：职位池或采集链路没有闭环；必须继续修复，不能解释为 0 岗位。",
        "- campus：独立校园招聘职位池；official_recruiting：公司官方混合招聘池，入库时只保留应届/校招/明确欢迎应届生的相关工程 JD。",
        "- 只有 41/41 ENUMERATED 才算官方招聘源真正全覆盖。",
    ]
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"contracts={cc.get('READY',0)}/{len(rows)} enumerated={cr.get('ENUMERATED',0)}/{len(rows)} incomplete={len(incomplete)}")
    return 1 if incomplete else 0

if __name__ == "__main__":
    raise SystemExit(main())
