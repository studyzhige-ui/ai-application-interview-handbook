#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit first-party recruiting-board coverage and strict JD-result closure."""

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

TERMINAL = {"ENUMERATED_WITH_MATCHES", "ENUMERATED_ZERO_MATCHES"}


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
        scope = src.get("board_scope") or ("campus" if src.get("current_campus_board") else "official_recruiting")
        search_url = src.get("search_url") or src.get("job_list_url") or ""
        contract = (
            "READY"
            if src.get("official_root") and search_url and src.get("job_list_url") == search_url
            else "BROKEN"
        )

        raw_norm = (
            n.get("retrieval_status")
            or n.get("previous_retrieval_status")
            or n.get("status")
            or ""
        )
        result_status = n.get("result_status") or ""
        family_count = int(n.get("role_family_count") or 0)
        full_jd = int(n.get("full_jd_count") or 0)
        title_only = int(n.get("title_only_count") or 0)
        fetched = int(n.get("fetched") or 0)
        matched = int(n.get("matched_requisitions") or n.get("matched") or 0)

        b_full = bool(b.get("full_keyword_search")) or bool(b.get("list_scan_complete"))
        b_status = b.get("status") or ""
        ats_ok = (f.get("status") == "OK") or (m.get("status") == "OK")

        if raw_norm in TERMINAL:
            runtime = "ENUMERATED"
        elif b_status in {"BROWSER_ENUMERATED", "BROWSER_ENUMERATED_ZERO"} and b_full:
            runtime = "ENUMERATED"
        elif ats_ok and (
            int(f.get("requests") or 0) > 0
            or int(m.get("requests") or 0) > 0
        ):
            runtime = "ENUMERATED"
        elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []) and b_full:
            runtime = "ENUMERATED"
        elif b.get("pages") and not any(p.get("error") for p in b.get("pages") or []):
            runtime = "LIST_REACHABLE"
        else:
            runtime = "BLOCKED"

        result_closed = result_status in {"HAS_TARGET_JDS", "ZERO_TARGET_JDS"}
        rows.append(
            dict(
                company=company,
                scope=scope,
                contract=contract,
                runtime=runtime,
                result_status=result_status or "MISSING_RESULT",
                result_closed=result_closed,
                families=family_count,
                full_jd=full_jd,
                title_only=title_only,
                fetched=fetched,
                matched=matched,
                root=src.get("official_root") or "",
                jobs=search_url,
            )
        )

    cc = Counter(r["contract"] for r in rows)
    runtime_counts = Counter(r["runtime"] for r in rows)
    result_closed_count = sum(r["result_closed"] for r in rows)
    incomplete_runtime = [
        r for r in rows
        if r["contract"] != "READY" or r["runtime"] != "ENUMERATED"
    ]
    missing_results = [r for r in rows if not r["result_closed"]]

    counts = norm.get("counts") or {}
    family_total = int(counts.get("role_families") or sum(r["families"] for r in rows))
    full_total = int(counts.get("full_jd_families") or sum(r["full_jd"] for r in rows))
    title_total = int(counts.get("title_only_families") or sum(r["title_only"] for r in rows))

    out = [
        "# 官方招聘岗位源全覆盖审计",
        "",
        "> 审计分成两条轴：Current Result Closure 与 Recurring Runtime Certification。前者回答“41 家当前是否都有明确岗位结论”；后者回答“自动维护链路是否已经由一次完整运行重新证明”。两者不能混为一谈。",
        "",
        "## 当前结果闭环",
        "",
        f"- 固定公司：**{len(rows)}**",
        f"- 可枚举固定路径 READY：**{cc.get('READY',0)}/{len(rows)}**",
        f"- 严格结果已闭环：**{result_closed_count}/{len(rows)}**",
        f"- 严格 Role Family：**{family_total}**",
        f"- 抓到第一方 JD 正文：**{full_total}**",
        f"- 第一方仅标题：**{title_total}**",
        f"- 结果缺失：**{len(missing_results)}**",
        "",
        "## 自动维护运行证明",
        "",
        f"- 已由历史/当前完整运行证明 ENUMERATED：**{runtime_counts.get('ENUMERATED',0)}/{len(rows)}**",
        f"- 页面可达但旧快照没有完整穷举证明：**{runtime_counts.get('LIST_REACHABLE',0)}**",
        f"- 仍需 Runner/适配器重新完整执行：**{runtime_counts.get('BLOCKED',0)}**",
        "",
        "> 自动运行证明不足不会把当前严格结果改成未知；但在自动任务恢复并完成 41/41 之前，也不能把 Runtime Certification 写成 41/41。",
        "",
        "## 逐公司",
        "",
        "| 公司 | 招聘池范围 | 路径 | 当前严格结果 | Role Family | 完整 JD | 仅标题 | Runtime | 固定职位池 |",
        "|---|---|:---:|---|---:|---:|---:|---|---|",
    ]
    for r in rows:
        out.append(
            "| {company} | {scope} | {contract} | {result_status} | {families} | {full_jd} | "
            "{title_only} | {runtime} | {jobs} |".format(**r)
        )

    out += [
        "",
        "## 验收规则",
        "",
        "- HAS_TARGET_JDS：当前第一方招聘池中保留了至少一个严格非算法 AI 应用 / Agent 工程 Role Family。",
        "- ZERO_TARGET_JDS：当前公司仍保留在官方搜索矩阵中，但本轮严格 Role Scope 后没有岗位进入正式库；这不等于公司没有其他招聘。",
        "- FULL_JD：已保存第一方岗位职责 / 任职要求正文；TITLE_ONLY_OFFICIAL：只确认到第一方当前职位标题，不用二手来源补写 JD。",
        "- ENUMERATED：自动采集器已完成完整分页或全部关键词穷举；LIST_REACHABLE 只代表页面能打开；BLOCKED 代表自动链路仍需修复/重跑。",
        "- 未来自动维护的最终目标仍是 41/41 ENUMERATED；审计脚本因此在 Runtime 未全绿时返回非零，防止假绿灯。",
    ]
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")

    print(
        f"contracts={cc.get('READY',0)}/{len(rows)} "
        f"results={result_closed_count}/{len(rows)} "
        f"runtime={runtime_counts.get('ENUMERATED',0)}/{len(rows)} "
        f"families={family_total}"
    )
    return 1 if missing_results or incomplete_runtime else 0


if __name__ == "__main__":
    raise SystemExit(main())
