"""Build JSON and human-readable projections from already collected first-party facts."""
from __future__ import annotations
import json
import re
from typing import Any
from .model import txt
from .paths import OUT_JSON, OUT_MD, VERIFIED_INDEX, VERIFIED_INDEX_MD, SCAN_POOL_MD

def clean(value, limit=None):
    # The readable first-party body is complete. Never silently truncate it.
    return str(value or "").strip()

def render(cfg, verified_index, role_families, all_matches, results, now, source_commit):
    result_map = {r.company: r for r in results}
    family_counts: dict[str, list[dict[str, Any]]] = {}
    for f in role_families:
        family_counts.setdefault(f["company"], []).append(f)

    source_rows = []
    for src in cfg["sources"]:
        company = src["company"]
        r = result_map.get(company)
        fams = family_counts.get(company, [])
        source_rows.append({
            "company": company,
            "mode": r.mode if r else src.get("mode", ""),
            "retrieval_status": r.status if r else "MISSING_RESULT",
            "fetched": r.fetched if r else 0,
            "matched_requisitions": r.matched if r else 0,
            "error": r.error if r else "source returned no result",
            "official_root": src.get("official_root", ""),
            "search_url": src.get("search_url") or src.get("job_list_url") or "",
            "board_scope": src.get("board_scope") or ("campus" if src.get("current_campus_board") else "official_recruiting"),
            "result_status": (
                "HAS_TARGET_JDS" if fams
                else "ZERO_TARGET_JDS" if r and r.status == "ENUMERATED_ZERO_MATCHES"
                else "NEEDS_ENUMERATION"
            ),
            "role_family_count": len(fams),
            "full_jd_count": sum(f.get("detail_status") == "FULL_JD" for f in fams),
            "title_only_count": sum(f.get("detail_status") == "TITLE_ONLY_OFFICIAL" for f in fams),
            "role_verified_current_source_count": sum(
                f.get("detail_status") == "ROLE_VERIFIED_CURRENT_SOURCE" for f in fams
            ),
            "verified_representative_role": next(
                (
                    txt((x.get("representative_roles") or [{}])[0].get("title"))
                    for x in verified_index.get("companies") or []
                    if x.get("company") == company
                ),
                "",
            ),
        })

    counts = {
        "companies": len(source_rows),
        "companies_with_targets": sum(x["result_status"] == "HAS_TARGET_JDS" for x in source_rows),
        "companies_zero_targets": sum(x["result_status"] == "ZERO_TARGET_JDS" for x in source_rows),
        "companies_needing_enumeration": sum(x["result_status"] == "NEEDS_ENUMERATION" for x in source_rows),
        "role_families": len(role_families),
        "full_jd_families": sum(f.get("detail_status") == "FULL_JD" for f in role_families),
        "title_only_families": sum(f.get("detail_status") == "TITLE_ONLY_OFFICIAL" for f in role_families),
        "role_verified_current_source_families": sum(
            f.get("detail_status") == "ROLE_VERIFIED_CURRENT_SOURCE" for f in role_families
        ),
        "raw_requisitions": len(all_matches),
    }
    payload = {
        "schema_version": 1,
        "generated_at": now,
        "source_commit": source_commit,
        "cycle": cfg["cycle"],
        "scope": "current official campus/new-grad non-algorithm AI application & Agent engineering",
        "methodology": {
            "inclusion": "First-party official source + current campus/new-grad eligibility + explicit engineering title materially about Agent/AI application/RAG/Harness/Runtime/Infra/Coding Agent.",
            "exclusion": "Algorithm/model-training/research, product, sales, operations, marketing, internship-only and generic engineering jobs that merely mention AI tooling.",
            "role_family": "Same-company near-identical titles are grouped while every official requisition remains attached.",
            "detail_status": "FULL_JD = first-party duties/requirements captured; TITLE_ONLY_OFFICIAL = first-party title only; ROLE_VERIFIED_CURRENT_SOURCE = current role presence verified and official application/search entry fixed, first-party body still being backfilled.",
            "zero_miss_policy": "Company membership is independent from job presence. Crawler miss/failure may not erase persistent verified role presence; ZERO_TARGET_JDS is valid only after complete official enumeration.",
        },
        "counts": counts,
        "sources": source_rows,
        "role_families": role_families,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 当前官方校招 / 应届｜非算法 AI 应用 & Agent 工程 JD 全量结果",
        "",
        f"> Generated: **{now}**",
        f"> Source commit: **{source_commit or 'local/manual'}**",
        f"> 固定长期扫描公司 **{counts['companies']}** 家；当前有目标岗位 **{counts['companies_with_targets']}** 家；完整枚举确认 0 岗 **{counts['companies_zero_targets']}** 家；仍待完整枚举 **{counts['companies_needing_enumeration']}** 家。",
        f"> 其中 **{counts['full_jd_families']}** 个抓到第一方 JD 正文，**{counts['title_only_families']}** 个仅能确认第一方职位标题，**{counts['role_verified_current_source_families']}** 个已核验岗位存在并固定官方入口、正文仍待补齐。",
        "",
        "## 1. 公司结果总表",
        "",
        "| 公司 | Retrieval | 官方职位池 | 结果 | Role Family | 完整 JD | 仅标题 |",
        "|---|---|---|---|---:|---:|---:|",
    ]
    for s in source_rows:
        status = s["retrieval_status"]
        if s["error"]:
            status += "；" + s["error"].replace("|", "\\|")
        lines.append(
            f"| {s['company']} | {status} | {s['search_url']} | {s['result_status']} | "
            f"{s['role_family_count']} | {s['full_jd_count']} | {s['title_only_count']} |"
        )

    lines += ["", "## 2. 严格 Role Family", ""]
    last_company = ""
    for f in role_families:
        if f["company"] != last_company:
            last_company = f["company"]
            lines += [f"## {last_company}", ""]
        lines += [
            f"### {f['role_family']}",
            "",
            f"- **证据状态**：{f['detail_status']}",
            f"- **地点**：{' / '.join(f['locations']) or '官方未提供'}",
            f"- **项目 / 届别**：{f['cycle_evidence'] or '当前官方招聘池 / 校招池'}",
            f"- **官方 Requisition**：{len(f['requisitions'])} 个",
        ]
        for req in f["requisitions"]:
            prefix = (f"`{req['job_id']}` · " if req.get("job_id") else "")
            loc = (f" · {req['location']}" if req.get("location") else "")
            url = (f" · {req['official_url']}" if req.get("official_url") else "")
            lines.append(f"  - {prefix}{req['title']}{loc}{url}")
        if f.get("evidence_url"):
            lines.append(f"- **岗位核验证据**：{f['evidence_url']}")
        if f.get("detail_status") == "FULL_JD":
            lines += ["", "**官方职责**", "", clean(f.get("description", ""), 6000) or "官方未返回职责正文。"]
            lines += ["", "**官方要求**", "", clean(f.get("requirements", ""), 6000) or "官方未返回任职要求。"]
        elif f.get("detail_status") == "ROLE_VERIFIED_CURRENT_SOURCE":
            lines += ["", "**已核验岗位摘要**", "", clean(f.get("evidence_summary", ""), 3000) or "岗位存在与官方投递入口已核验。"]
            lines += ["", "**JD 完整度**", "", "> 第一方职责 / 要求正文仍待回填；该摘要不冒充第一方完整 JD。"]
        else:
            lines += ["", "**JD 完整度**", "", "> 第一方当前职位列表已确认岗位标题；职责 / 要求正文尚未稳定取得，不用二手来源补写。"]
        lines.append("")

    OUT_MD.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    # Keep human-readable company status files in lockstep with the JSON state.
    index_rows = {x.get("company"): x for x in verified_index.get("companies") or [] if x.get("company")}
    index_lines = [
        f"# {len(cfg.get('sources') or [])} 家目标公司｜官方 AI / Agent 工程岗位状态索引",
        "",
        "> 公司扫描池与岗位存在性分离；状态只由第一方职位池完整枚举更新。",
        "",
        "| 公司 | 主要业务 | 官方职位池 | 状态 | 代表岗位 |",
        "|---|---|---|---|---|",
    ]
    pool_lines = [
        f"# 目标公司扫描池｜{len(cfg.get('sources') or [])} 家知名中大厂与 AI 公司",
        "",
        "> 公司进入扫描池不代表当前一定存在目标岗位；岗位是否存在由每轮第一方职位池完整枚举决定。",
        "",
        "| # | 公司 | 主要业务 | 第一方职位池 | 当前持久化状态 |",
        "|---:|---|---|---|---|",
    ]
    for n, source in enumerate(cfg.get("sources") or [], 1):
        company = source.get("company") or ""
        row = index_rows.get(company) or {}
        roles = row.get("representative_roles") or []
        representative = txt(roles[0].get("title")) if roles else ""
        business = txt(source.get("business_summary")).replace("|", "\\|")
        search_url = source.get("search_url") or source.get("job_list_url") or ""
        status = row.get("status") or "NEEDS_ENUMERATION"
        safe_company = company.replace("|", "\\|")
        safe_role = representative.replace("|", "\\|")
        index_lines.append(f"| {safe_company} | {business} | {search_url} | {status} | {safe_role} |")
        pool_lines.append(f"| {n} | {safe_company} | {business} | {search_url} | {status} |")
    index_lines += [
        "",
        "## 状态语义",
        "",
        "- VERIFIED_ROLE：本轮或历史完整第一方证据已核验目标工程岗位。",
        "- ZERO_TARGET_JDS：本轮完整第一方枚举后确认当前没有符合 Role Scope 的正式岗位。",
        "- NEEDS_ENUMERATION：尚未完成可靠完整枚举；不能解释为 0 岗。",
    ]
    pool_lines += [
        "",
        "## 状态语义",
        "",
        "- VERIFIED_ROLE：已有至少一个第一方核验的目标工程岗位事实。",
        "- ZERO_TARGET_JDS：本轮已完整枚举官方职位池，但当前没有符合 Role Scope 的正式岗位。",
        "- NEEDS_ENUMERATION：公司与第一方职位池已固定，但完整分页 / 关键词穷举尚未闭环。",
    ]
    VERIFIED_INDEX_MD.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    SCAN_POOL_MD.write_text("\n".join(pool_lines) + "\n", encoding="utf-8")

    VERIFIED_INDEX.write_text(json.dumps(verified_index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload
