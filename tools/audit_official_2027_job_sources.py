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
        state = src.get("campus_entry_status", "")
        browser_jobs = len(b.get("jobs") or [])
        ats_jobs = max(len(f.get("jobs") or []), len(m.get("jobs") or []))
        raw = b.get("status", "")

        if state == "NO_PUBLIC_CAMPUS_BOARD":
            contract = "WATCH_ONLY"
            retrieval = "NO_PUBLIC_CAMPUS_BOARD"
        else:
            contract = "READY" if src.get("official_root") and src.get("campus_search_url") and src.get("job_list_url") else "BROKEN"
            if n.get("status") in terminal:
                retrieval = "ENUMERATED"
            elif raw in {"BROWSER_ENUMERATED","BROWSER_ENUMERATED_ZERO","BROWSER_OK","BROWSER_OK_0_MATCH"}:
                retrieval = "ENUMERATED"
            elif browser_jobs or ats_jobs:
                retrieval = "ENUMERATED"
            elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []):
                retrieval = "LIST_REACHABLE"
            else:
                retrieval = "BLOCKED"

        rows.append(dict(
            company=company, state=state, contract=contract, retrieval=retrieval,
            fetched=int(n.get("fetched") or 0), matched=int(n.get("matched") or 0),
            root=src.get("official_root") or "",
            jobs=src.get("campus_search_url") or src.get("career_watch_url") or "",
        ))

    cc = Counter(r["contract"] for r in rows)
    cr = Counter(r["retrieval"] for r in rows)
    public = [r for r in rows if r["state"] == "PUBLIC_CAMPUS_BOARD"]
    enumerated_public = sum(r["retrieval"] == "ENUMERATED" for r in public)
    incomplete_public = [r for r in public if r["retrieval"] != "ENUMERATED"]

    out = [
        "# 当前校招官方岗位源覆盖审计","",
        "> READY 不再等于“配置里有两个 URL”。公开校招公司只有在存在真实 campus_search_url 时才算路径 READY；没有公开校招的公司单列 WATCH_ONLY，不能用官网首页冒充校招职位列表。","",
        f"- 固定公司：**{len(rows)}**",
        f"- 有公开校招职位池：**{len(public)}**",
        f"- 公开校招路径 READY：**{sum(r['contract']=='READY' for r in public)}/{len(public)}**",
        f"- 已稳定枚举公开校招池：**{enumerated_public}/{len(public)}**",
        f"- 仍需完整枚举：**{len(incomplete_public)}**",
        f"- 官网已核验但无公开校招池：**{cr.get('NO_PUBLIC_CAMPUS_BOARD',0)}**","",
        "## 逐公司","",
        "| 公司 | 校招入口状态 | 路径契约 | Retrieval | 上次拉取 | 目标候选 | 官方根入口 | 校招搜索/巡检入口 |",
        "|---|---|:---:|---|---:|---:|---|---|",
    ]
    for r in rows:
        out.append("| {company} | {state} | {contract} | {retrieval} | {fetched} | {matched} | {root} | {jobs} |".format(**r))

    out += ["","## 验收规则","",
        "- PUBLIC_CAMPUS_BOARD：必须存在明确的校招/应届职位页或官方 ATS，并完成完整分页/关键词穷举后才能成为 ENUMERATED。",
        "- LIST_REACHABLE：只证明页面能打开，不代表岗位已获取完整。",
        "- BLOCKED：公开校招入口存在，但采集链路没有闭环；这是必须继续修复的真实失败。",
        "- NO_PUBLIC_CAMPUS_BOARD：官网已核验但当前没有公开校招职位池；只巡检 career_watch_url，不把社会招聘/公司首页伪装成校招。",
        "- 0 个目标岗位只有在公开校招职位池已 ENUMERATED 后才有意义；未枚举完成时绝不能把 0 当结论。",
    ]
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"public_campus={len(public)} enumerated={enumerated_public} incomplete={len(incomplete_public)} watch_only={cr.get('NO_PUBLIC_CAMPUS_BOARD',0)}")
    return 1 if any(r["contract"] == "BROKEN" or r["retrieval"] == "BLOCKED" for r in public) else 0

if __name__ == "__main__":
    raise SystemExit(main())
