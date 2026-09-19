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
    rows=[]
    terminal={"ENUMERATED_WITH_MATCHES","ENUMERATED_ZERO_MATCHES"}
    for src in reg.get("sources", []):
        company=src["company"]
        n,b,f,m=ns.get(company,{}),bs.get(company,{}),fs.get(company,{}),ms.get(company,{})
        contract="READY" if src.get("official_root") and src.get("job_list_url") else "BROKEN"
        browser_jobs=len(b.get("jobs") or [])
        ats_jobs=max(len(f.get("jobs") or []),len(m.get("jobs") or []))
        raw=b.get("status","")
        if n.get("status") in terminal:
            retrieval="ENUMERATED"
        elif raw in {"BROWSER_ENUMERATED","BROWSER_ENUMERATED_ZERO","BROWSER_OK","BROWSER_OK_0_MATCH"}:
            retrieval="ENUMERATED"
        elif browser_jobs or ats_jobs:
            retrieval="ENUMERATED"
        elif n.get("status") in {"NO_PUBLIC_CAMPUS_PROJECT","NO_PUBLIC_2027_PROJECT"}:
            retrieval="NO_PUBLIC_CAMPUS_PROJECT"
        elif src.get("no_public_campus_when_empty") and b.get("pages") and not any(p.get("error") for p in b.get("pages") or []):
            retrieval="NO_PUBLIC_CAMPUS_PROJECT"
        elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []):
            retrieval="LIST_REACHABLE"
        else:
            retrieval="BLOCKED"
        rows.append(dict(company=company,contract=contract,retrieval=retrieval,
                         fetched=int(n.get("fetched") or 0),matched=int(n.get("matched") or 0),
                         root=src.get("official_root") or "",jobs=src.get("job_list_url") or ""))
    cc=Counter(r["contract"] for r in rows); cr=Counter(r["retrieval"] for r in rows)
    out=["# 当前校招官方岗位源覆盖审计","",
         "> 年份不作为 Gate。只审计：当前官方校园招聘职位池能否稳定全量枚举，以及是否命中目标非算法工程 Role Scope。","",
         f"- 固定公司：**{len(rows)}**",
         f"- 固定路径契约 READY：**{cc.get('READY',0)}/{len(rows)}**",
         f"- 已稳定枚举：**{cr.get('ENUMERATED',0)}**",
         f"- 职位页可达、仍需完整枚举：**{cr.get('LIST_REACHABLE',0)}**",
         f"- 官网当前无公开校招：**{cr.get('NO_PUBLIC_CAMPUS_PROJECT',0)}**",
         f"- 采集仍 BLOCKED：**{cr.get('BLOCKED',0)}**","",
         "## 逐公司","",
         "| 公司 | 固定路径 | Retrieval | 上次拉取 | 目标候选 | 官方根入口 | 固定校招职位列表 |",
         "|---|:---:|---|---:|---:|---|---|"]
    for r in rows:
        out.append("| {company} | {contract} | {retrieval} | {fetched} | {matched} | {root} | {jobs} |".format(**r))
    out += ["","## 状态解释","",
            "- ENUMERATED：当前官方校园职位池已有真实运行结果证明可稳定枚举。",
            "- LIST_REACHABLE：官方校招职位页可访问，但现有快照尚未完成全关键词 + 完整分页穷举。",
            "- NO_PUBLIC_CAMPUS_PROJECT：官网当前没有公开校园招聘职位池。",
            "- BLOCKED：官方校招入口存在/待确认，但采集尚未可靠闭环；不能解释为 0 岗位。",
            "- 年份、毕业窗口、项目名称只作备注；正式 JD 的时间 Gate 是“当前官网校招链接仍有效”。"]
    OUT.write_text("\n".join(out)+"\n",encoding="utf-8")
    print(f"contracts={cc.get('READY',0)}/{len(rows)} enumerated={cr.get('ENUMERATED',0)} blocked={cr.get('BLOCKED',0)}")
    return 1 if cc.get("READY",0)!=len(rows) else 0

if __name__=="__main__":
    raise SystemExit(main())
