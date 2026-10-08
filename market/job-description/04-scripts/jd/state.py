"""Persistent company facts: partial/blocked collection cannot erase verified roles."""
from __future__ import annotations
from datetime import datetime, timezone
from .model import txt

def update_state(cfg, verified_index, role_families, seeded_companies, results):
    result_map = {r.company: r for r in results}
    current_keys = {(x["company"], x["role_family"]) for x in role_families}
    source_by_company = {x.get("company"): x for x in cfg.get("sources") or [] if x.get("company")}
    index_by_company = {
        x.get("company"): x for x in verified_index.get("companies") or [] if x.get("company")
    }
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for company, source in source_by_company.items():
        row = index_by_company.get(company)
        if row is None:
            row = {
                "company": company,
                "status": "NEEDS_ENUMERATION",
                "official_root": source.get("official_root", ""),
                "official_search_url": source.get("search_url") or source.get("job_list_url") or "",
                "board_scope": source.get("board_scope") or ("campus" if source.get("current_campus_board") else "official_recruiting"),
                "business_summary": source.get("business_summary", ""),
                "representative_roles": [],
                "last_verified": None,
            }
            verified_index.setdefault("companies", []).append(row)
            index_by_company[company] = row

        row["official_root"] = source.get("official_root", "")
        row["official_search_url"] = source.get("search_url") or source.get("job_list_url") or ""
        row["board_scope"] = source.get("board_scope") or ("campus" if source.get("current_campus_board") else "official_recruiting")
        row["business_summary"] = source.get("business_summary", "")

        runtime = result_map.get(company)
        if runtime and runtime.status == "ENUMERATED_WITH_MATCHES":
            candidates = [
                f for f in role_families
                if f.get("company") == company and not f.get("carried_forward")
            ]
            if candidates:
                candidates.sort(
                    key=lambda f: (
                        f.get("detail_status") == "FULL_JD",
                        len(f.get("description") or "") + len(f.get("requirements") or ""),
                        len(f.get("requisitions") or []),
                    ),
                    reverse=True,
                )
                best = candidates[0]
                req = (best.get("requisitions") or [{}])[0]
                full = best.get("detail_status") == "FULL_JD"
                summary = "\n".join(
                    x for x in [best.get("description") or "", best.get("requirements") or ""] if x
                )[:5000]
                row["status"] = "VERIFIED_ROLE"
                row["representative_roles"] = [{
                    "title": best.get("representative_title") or best.get("role_family") or "",
                    "recruitment_type": best.get("cycle_evidence") or (
                        "当前校园招聘" if row["board_scope"] == "campus" else "当前官方招聘（应届可投）"
                    ),
                    "role_scope": best.get("role_family") or best.get("representative_title") or "",
                    "official_apply_url": req.get("official_url") or row["official_search_url"],
                    "evidence_url": req.get("official_url") or row["official_search_url"],
                    "evidence_type": "FIRST_PARTY_FULL_JD" if full else "FIRST_PARTY_OFFICIAL_TITLE",
                    "jd_status": "FULL_FIRST_PARTY_JD" if full else "TITLE_ONLY_FIRST_PARTY",
                    "jd_summary": summary,
                    "source_role_family": best.get("role_family") or "",
                }]
                row["last_verified"] = today
        elif runtime and runtime.status == "ENUMERATED_ZERO_MATCHES" and company not in seeded_companies:
            row["status"] = "ZERO_TARGET_JDS"
            row["representative_roles"] = []
            row["last_verified"] = today
        elif company in seeded_companies and row.get("status") != "VERIFIED_ROLE":
            candidates = [f for f in role_families if f.get("company") == company]
            if candidates:
                best = next((f for f in candidates if f.get("manual_first_party_seed")), candidates[0])
                req = (best.get("requisitions") or [{}])[0]
                row["status"] = "VERIFIED_ROLE"
                row["representative_roles"] = [{
                    "title": best.get("representative_title") or best.get("role_family") or "",
                    "recruitment_type": best.get("cycle_evidence") or "当前校园招聘",
                    "role_scope": best.get("role_family") or "",
                    "official_apply_url": req.get("official_url") or row["official_search_url"],
                    "evidence_url": best.get("evidence_url") or req.get("official_url") or row["official_search_url"],
                    "evidence_type": "FIRST_PARTY_OFFICIAL_LISTING",
                    "jd_status": "ROLE_VERIFIED",
                    "jd_summary": best.get("evidence_summary") or "",
                    "source_role_family": best.get("role_family") or "",
                }]
                row["last_verified"] = best.get("verified_on") or row.get("last_verified")

    verified_index["schema_version"] = max(2, int(verified_index.get("schema_version") or 1))
    verified_index["generated_at"] = today

    for company_row in verified_index.get("companies") or []:
        company = company_row.get("company")
        roles = company_row.get("representative_roles") or []
        if not company or company_row.get("status") != "VERIFIED_ROLE" or not roles:
            continue
        role = roles[0]
        family = txt(role.get("title"))
        if not family:
            continue
        key = (company, family)
        if key in current_keys:
            continue
        official_url = txt(role.get("official_apply_url") or company_row.get("official_search_url"))
        role_families.append({
            "company": company,
            "role_family": family,
            "representative_title": family,
            "locations": [],
            "description": "",
            "requirements": "",
            "evidence_summary": txt(role.get("jd_summary")),
            "cycle_evidence": txt(role.get("recruitment_type")),
            "requisitions": [{
                "job_id": "",
                "title": family,
                "location": "",
                "official_url": official_url,
                "official_api": "",
            }],
            "source_evidence": [txt(role.get("evidence_type") or "VERIFIED_ROLE_INDEX")],
            "evidence_url": txt(role.get("evidence_url")),
            "detail_status": "ROLE_VERIFIED_CURRENT_SOURCE",
            "persistent_verified_role": True,
        })
        current_keys.add(key)

    role_families.sort(key=lambda x: (x["company"], x["role_family"]))

    return verified_index, role_families
