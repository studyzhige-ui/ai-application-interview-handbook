#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit company scan coverage separately from target-JD presence and runtime health."""

from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "market/jobs/official-2027-campus-sources.json"
INDEX = ROOT / "market/jobs/official-company-role-index.json"
NORM = ROOT / "market/jobs/official-2027-agent-jobs.generated.json"
BROWSER = ROOT / "market/jobs/official-2027-browser-discovery.generated.json"
FEISHU = ROOT / "market/jobs/official-2027-feishu-discovery.generated.json"
MOKA = ROOT / "market/jobs/official-2027-moka-discovery.generated.json"
OUT = ROOT / "market/jobs/official-2027-coverage-audit.generated.md"

TERMINAL = {"ENUMERATED_WITH_MATCHES", "ENUMERATED_ZERO_MATCHES"}
CACHE_MAX_AGE_SECONDS = 6 * 60 * 60

def read(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def cache_is_fresh(payload: dict) -> bool:
    raw = str(payload.get("generated_at") or "").strip()
    if not raw:
        return False
    try:
        stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return False
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - stamp.astimezone(timezone.utc)).total_seconds()
    return -300 <= age <= CACHE_MAX_AGE_SECONDS

def main() -> int:
    reg, index, norm, browser, feishu, moka = map(read, (REG, INDEX, NORM, BROWSER, FEISHU, MOKA))
    expected = int(reg.get("expected_company_count") or 0)
    ns = {x.get("company"): x for x in norm.get("sources", []) if x.get("company")}
    ix = {x.get("company"): x for x in index.get("companies", []) if x.get("company")}
    bs = {x.get("company"): x for x in browser.get("results", []) if x.get("company")}
    fs = {x.get("company"): x for x in feishu.get("results", []) if x.get("company")}
    ms = {x.get("company"): x for x in moka.get("results", []) if x.get("company")}
    browser_fresh = cache_is_fresh(browser)
    feishu_fresh = cache_is_fresh(feishu)
    moka_fresh = cache_is_fresh(moka)

    rows = []
    hard_errors: list[str] = []
    expected_source_sha = os.environ.get("SYNC_SOURCE_SHA", "").strip()
    generated_source_sha = str(norm.get("source_commit") or "").strip()
    if expected_source_sha and generated_source_sha != expected_source_sha:
        hard_errors.append(
            f"generated source_commit mismatch: expected {expected_source_sha}, got {generated_source_sha or '<missing>'}"
        )
    for src in reg.get("sources", []):
        company = src["company"]
        n, i, b, f, m = ns.get(company, {}), ix.get(company, {}), bs.get(company, {}), fs.get(company, {}), ms.get(company, {})
        search_url = src.get("search_url") or src.get("job_list_url") or ""
        contract = "READY" if src.get("official_root") and search_url and src.get("job_list_url") == search_url else "BROKEN"
        roles = i.get("representative_roles") or []
        persistent_state = i.get("status") or "NEEDS_ENUMERATION"
        representative = roles[0].get("title", "") if roles else ""

        raw_norm = n.get("retrieval_status") or n.get("previous_retrieval_status") or n.get("status") or ""
        b_full = browser_fresh and (bool(b.get("full_keyword_search")) or bool(b.get("list_scan_complete")))
        b_status = (b.get("status") or "") if browser_fresh else ""
        ats_ok = ((feishu_fresh and f.get("status") == "OK") or (moka_fresh and m.get("status") == "OK"))

        if raw_norm in TERMINAL:
            runtime = "ENUMERATED"
        elif b_status in {"BROWSER_ENUMERATED", "BROWSER_ENUMERATED_ZERO"} and b_full:
            runtime = "ENUMERATED"
        elif ats_ok and (int(f.get("requests") or 0) > 0 or int(m.get("requests") or 0) > 0):
            runtime = "ENUMERATED"
        elif browser_fresh and b.get("pages") and not any(p.get("error") for p in b.get("pages") or []):
            runtime = "LIST_REACHABLE"
        else:
            runtime = "BLOCKED"

        role_count = int(n.get("role_family_count") or 0)
        if role_count > 0 or persistent_state == "VERIFIED_ROLE":
            result = "HAS_TARGET_JDS"
        elif raw_norm == "ENUMERATED_ZERO_MATCHES":
            result = "ZERO_TARGET_JDS"
        else:
            result = "NEEDS_ENUMERATION"

        if contract != "READY":
            hard_errors.append(f"{company}: official source contract is broken")
        rows.append({
            "company": company, "business": src.get("business_summary", ""), "contract": contract,
            "persistent_state": persistent_state, "representative": representative,
            "result": result, "runtime": runtime, "jobs": search_url,
        })

    if len(rows) != expected:
        hard_errors.append(f"scan registry must contain exactly {expected} companies; got {len(rows)}")
    if set(ix) != {x["company"] for x in rows}:
        hard_errors.append("role-state index company set diverges from scan registry")

    for row in rows:
        if row["runtime"] != "ENUMERATED":
            hard_errors.append(
                f"{row['company']}: runtime must be ENUMERATED, got {row['runtime']}"
            )
        if row["result"] == "NEEDS_ENUMERATION":
            hard_errors.append(
                f"{row['company']}: target-job result still NEEDS_ENUMERATION"
            )

    runtime_counts = Counter(x["runtime"] for x in rows)
    result_counts = Counter(x["result"] for x in rows)
    counts = norm.get("counts") or {}
    out = [
        "# 官方 AI / Agent 工程岗位覆盖审计", "",
        "> 公司扫描覆盖、当前目标岗位存在性、自动抓取 Runtime 三者分开。公司当前 0 岗不会被移出长期扫描池；抓取失败也不能解释为 0 岗。", "",
        "## 扫描池覆盖", "",
        f"- 固定长期扫描公司：**{len(rows)}/{expected}**",
        f"- 第一方官方招聘 / 校招入口 READY：**{sum(x['contract']=='READY' for x in rows)}/{len(rows)}**",
        f"- 当前有目标岗位：**{result_counts.get('HAS_TARGET_JDS',0)}**",
        f"- 完整枚举后确认当前 0 个目标岗位：**{result_counts.get('ZERO_TARGET_JDS',0)}**",
        f"- 仍需完成本轮枚举：**{result_counts.get('NEEDS_ENUMERATION',0)}**",
        f"- Role Family：**{int(counts.get('role_families') or 0)}**",
        f"- 第一方完整 JD：**{int(counts.get('full_jd_families') or 0)}**", "",
        "## Runtime 诊断", "",
        f"- ENUMERATED：**{runtime_counts.get('ENUMERATED',0)}/{len(rows)}**",
        f"- LIST_REACHABLE：**{runtime_counts.get('LIST_REACHABLE',0)}**",
        f"- BLOCKED：**{runtime_counts.get('BLOCKED',0)}**",
        f"- Browser cache fresh：**{'YES' if browser_fresh else 'NO'}**",
        f"- Feishu cache fresh：**{'YES' if feishu_fresh else 'NO'}**",
        f"- Moka cache fresh：**{'YES' if moka_fresh else 'NO'}**", "",
        "## 逐公司", "",
        "| 公司 | 主要业务 | 官方职位池 | 当前目标岗 | Runtime | 代表岗位 |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        out.append(f"| {r['company']} | {r['business']} | {r['jobs']} | {r['result']} | {r['runtime']} | {r['representative']} |")
    out += ["", "## 验收规则", "",
        f"- {expected}/{expected} 公司必须始终保留固定第一方职位池；公司扫描覆盖是硬失败条件。",
        "- HAS_TARGET_JDS 表示已有符合非算法 AI/Agent 工程范围的岗位；ZERO_TARGET_JDS 只允许在完整枚举后产生。",
        "- NEEDS_ENUMERATION 表示自动维护链路尚未完成该公司的本轮完整分页/关键词穷举，不等价于无岗位。",
        "- Runtime ENUMERATED 与岗位存在性分开；任何一次 WAF/API/browser 失败不得删除历史 VERIFIED_ROLE。",
        "- 正式 JD 继续只接受第一方公司官网或公司官方 ATS 正文。"
    ]
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"companies={len(rows)}/{expected} target={result_counts.get('HAS_TARGET_JDS',0)} zero={result_counts.get('ZERO_TARGET_JDS',0)} needs={result_counts.get('NEEDS_ENUMERATION',0)} runtime={runtime_counts.get('ENUMERATED',0)}/{len(rows)} hard_errors={len(hard_errors)}")
    for e in hard_errors:
        print("ERROR:", e)
    return 1 if hard_errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
