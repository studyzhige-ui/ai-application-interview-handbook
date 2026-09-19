#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit fixed-path official job retrieval separately from 2027 cohort proof."""

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
    for src in reg.get("sources", []):
        company = src["company"]
        n, b, f, m = ns.get(company, {}), bs.get(company, {}), fs.get(company, {}), ms.get(company, {})
        contract = "READY" if src.get("official_root") and src.get("job_list_url") else "BROKEN"
        browser_jobs = len(b.get("jobs") or [])
        ats_jobs = max(len(f.get("jobs") or []), len(m.get("jobs") or []))
        browser_status = b.get("status", "")
        if n.get("status") in {"ENUMERATED_WITH_MATCHES", "ENUMERATED_ZERO_MATCHES"}:
            retrieval = "ENUMERATED"
        elif browser_status in {"BROWSER_ENUMERATED", "BROWSER_ENUMERATED_ZERO", "BROWSER_OK", "BROWSER_OK_0_MATCH"}:
            retrieval = "ENUMERATED"
        elif browser_jobs or ats_jobs:
            retrieval = "ENUMERATED"
        elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []):
            retrieval = "LIST_REACHABLE"
        elif src.get("allow_no_public_2027"):
            retrieval = "NO_PUBLIC_2027_PROJECT"
        else:
            retrieval = "NEEDS_RUNTIME_RECHECK"
        cycle_text = " ".join(str(j.get("cycle_evidence", "")) for j in (b.get("jobs") or []))
        if src.get("verified_2027_project") or b.get("has2027") or "2027" in cycle_text:
            cohort = "VERIFIED_2027"
        elif src.get("allow_no_public_2027") and retrieval in {"NO_PUBLIC_2027_PROJECT", "LIST_REACHABLE"}:
            cohort = "NO_PUBLIC_2027_PROJECT"
        else:
            cohort = "COHORT_UNVERIFIED"
        rows.append({
            "company": company, "contract": contract, "retrieval": retrieval, "cohort": cohort,
            "fetched": int(n.get("fetched") or 0), "matched": int(n.get("matched") or 0),
            "root": src.get("official_root") or "", "jobs": src.get("job_list_url") or "",
        })
    cc = Counter(r["contract"] for r in rows)
    cr = Counter(r["retrieval"] for r in rows)
    ch = Counter(r["cohort"] for r in rows)
    out = [
        "# 2027 校招官方岗位源覆盖审计", "",
        "> 本审计把“职位能否获取”和“是否有 2027 届官方证据”分开，避免把 cohort 未确认误写成抓取失败。", "",
        f"- 固定公司：**{len(rows)}**",
        f"- 固定路径契约 READY：**{cc.get('READY', 0)}/{len(rows)}**",
        f"- 上次运行已实际枚举：**{cr.get('ENUMERATED', 0)}**",
        f"- 上次运行职位页可达、需按新固定路径重跑：**{cr.get('LIST_REACHABLE', 0)}**",
        f"- 官方未公开 2027 项目：**{cr.get('NO_PUBLIC_2027_PROJECT', 0)}**",
        f"- 需要运行时复核：**{cr.get('NEEDS_RUNTIME_RECHECK', 0)}**", "",
        "## 2027 届别", "",
        f"- VERIFIED_2027：**{ch.get('VERIFIED_2027', 0)}**",
        f"- COHORT_UNVERIFIED：**{ch.get('COHORT_UNVERIFIED', 0)}**",
        f"- NO_PUBLIC_2027_PROJECT：**{ch.get('NO_PUBLIC_2027_PROJECT', 0)}**", "",
        "## 逐公司", "",
        "| 公司 | 固定路径 | Retrieval | Cohort | 上次拉取 | 目标候选 | 官方根入口 | 固定职位列表 |",
        "|---|:---:|---|---|---:|---:|---|---|",
    ]
    for r in rows:
        out.append("| {company} | {contract} | {retrieval} | {cohort} | {fetched} | {matched} | {root} | {jobs} |".format(**r))
    out += ["", "## 解释", "",
        "- READY 只表示采集契约完整：有第一手 official_root 和固定 job_list_url。",
        "- ENUMERATED 表示已有官方运行结果证明职位列表/详情能被读取。",
        "- LIST_REACHABLE 表示官方职位页已成功打开，但存量快照早于当前固定页面完整穷举版本；下一轮统一同步会重跑。",
        "- COHORT_UNVERIFIED 不代表抓不到，只代表官方页面尚未给出足够的 2027 届证据，因此不能进入 2027 正式主库。",
        "- 正式 JD 主库只允许 VERIFIED_2027 + 非算法工程 Role Scope。",
    ]
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"contracts={cc.get('READY',0)}/{len(rows)} enumerated={cr.get('ENUMERATED',0)} cohort2027={ch.get('VERIFIED_2027',0)}")
    return 1 if cc.get("READY", 0) != len(rows) else 0

if __name__ == "__main__":
    raise SystemExit(main())
