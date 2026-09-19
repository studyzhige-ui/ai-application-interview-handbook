#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit verified company-role coverage separately from recurring runtime health."""

from __future__ import annotations

import json
from collections import Counter
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


def read(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> int:
    reg, index, norm, browser, feishu, moka = map(
        read, (REG, INDEX, NORM, BROWSER, FEISHU, MOKA)
    )
    ns = {x.get("company"): x for x in norm.get("sources", []) if x.get("company")}
    ix = {x.get("company"): x for x in index.get("companies", []) if x.get("company")}
    bs = {x.get("company"): x for x in browser.get("results", []) if x.get("company")}
    fs = {x.get("company"): x for x in feishu.get("results", []) if x.get("company")}
    ms = {x.get("company"): x for x in moka.get("results", []) if x.get("company")}

    rows = []
    hard_errors: list[str] = []
    for src in reg.get("sources", []):
        company = src["company"]
        n, i, b, f, m = (
            ns.get(company, {}),
            ix.get(company, {}),
            bs.get(company, {}),
            fs.get(company, {}),
            ms.get(company, {}),
        )
        scope = src.get("board_scope") or (
            "campus" if src.get("current_campus_board") else "official_recruiting"
        )
        search_url = src.get("search_url") or src.get("job_list_url") or ""
        contract = (
            "READY"
            if src.get("official_root")
            and search_url
            and src.get("job_list_url") == search_url
            else "BROKEN"
        )

        roles = i.get("representative_roles") or []
        representative = roles[0].get("title", "") if roles else ""
        role_verified = i.get("status") == "VERIFIED_ROLE" and bool(representative)

        raw_norm = (
            n.get("retrieval_status")
            or n.get("previous_retrieval_status")
            or n.get("status")
            or ""
        )
        b_full = bool(b.get("full_keyword_search")) or bool(b.get("list_scan_complete"))
        b_status = b.get("status") or ""
        ats_ok = (f.get("status") == "OK") or (m.get("status") == "OK")

        if raw_norm in TERMINAL:
            runtime = "ENUMERATED"
        elif b_status in {"BROWSER_ENUMERATED", "BROWSER_ENUMERATED_ZERO"} and b_full:
            runtime = "ENUMERATED"
        elif ats_ok and (
            int(f.get("requests") or 0) > 0 or int(m.get("requests") or 0) > 0
        ):
            runtime = "ENUMERATED"
        elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []) and b_full:
            runtime = "ENUMERATED"
        elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []):
            runtime = "LIST_REACHABLE"
        else:
            runtime = "BLOCKED"

        if contract != "READY":
            hard_errors.append(f"{company}: official source contract is broken")
        if not role_verified:
            hard_errors.append(f"{company}: verified representative engineering role missing")

        rows.append(
            {
                "company": company,
                "scope": scope,
                "contract": contract,
                "role_verified": role_verified,
                "representative": representative,
                "evidence_type": (roles[0].get("evidence_type", "") if roles else ""),
                "runtime": runtime,
                "jobs": search_url,
            }
        )

    runtime_counts = Counter(x["runtime"] for x in rows)
    counts = norm.get("counts") or {}
    role_families = int(counts.get("role_families") or 0)
    full_jd = int(
        counts.get("full_first_party_jd_families")
        or counts.get("full_jd_families")
        or 0
    )
    title_only = int(
        counts.get("title_only_first_party_families")
        or counts.get("title_only_families")
        or 0
    )
    verified_summary = int(counts.get("role_verified_current_source_families") or 0)

    out = [
        "# 官方 AI / Agent 工程岗位覆盖审计",
        "",
        "> 岗位事实与自动抓取运行状态分开：crawler miss / WAF / API 失败不能把已核验岗位回写成 0。",
        "",
        "## 覆盖事实",
        "",
        f"- 固定公司：**{len(rows)}**",
        f"- 官方招聘 / 校招入口 READY：**{sum(x['contract']=='READY' for x in rows)}/{len(rows)}**",
        f"- 至少一个相关工程岗位已核验：**{sum(x['role_verified'] for x in rows)}/{len(rows)}**",
        f"- Role Family：**{role_families}**",
        f"- 第一方完整 JD：**{full_jd}**",
        f"- 第一方仅标题：**{title_only}**",
        f"- 已核验岗位、待补第一方正文：**{verified_summary}**",
        "",
        "## Runtime 诊断",
        "",
        f"- ENUMERATED：**{runtime_counts.get('ENUMERATED',0)}/{len(rows)}**",
        f"- LIST_REACHABLE：**{runtime_counts.get('LIST_REACHABLE',0)}**",
        f"- BLOCKED：**{runtime_counts.get('BLOCKED',0)}**",
        "",
        "> Runtime 不是岗位存在性 Gate。自动化恢复后继续把它推进到 41/41 ENUMERATED，但中途结果必须允许提交，不能形成审计死锁。",
        "",
        "## 逐公司",
        "",
        "| 公司 | 官方职位池 | 代表岗位 | 岗位覆盖 | Runtime |",
        "|---|---|---|:---:|---|",
    ]
    for r in rows:
        mark = "✅" if r["role_verified"] else "❌"
        out.append(
            f"| {r['company']} | {r['jobs']} | {r['representative']} | {mark} | {r['runtime']} |"
        )

    out += [
        "",
        "## 验收规则",
        "",
        "- 41/41 公司必须同时有固定第一方招聘入口和至少一个 VERIFIED_ROLE；这是硬失败条件。",
        "- Runtime ENUMERATED 表示自动采集已完成分页 / 关键词穷举；LIST_REACHABLE / BLOCKED 需要继续修复，但不会删除已核验岗位。",
        "- 自动同步可以新增、刷新或把岗位升级成第一方完整 JD；不得仅因为一次抓取 0 命中而把 VERIFIED_ROLE 降级成无岗位。",
        "- 第一方正文未补齐的岗位必须保持证据等级标注，不把外部摘要伪装成公司原文。",
    ]
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(
        f"companies={len(rows)} verified_roles={sum(x['role_verified'] for x in rows)}/{len(rows)} "
        f"runtime={runtime_counts.get('ENUMERATED',0)}/{len(rows)} hard_errors={len(hard_errors)}"
    )
    for error in hard_errors:
        print("ERROR:", error)
    return 1 if hard_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
