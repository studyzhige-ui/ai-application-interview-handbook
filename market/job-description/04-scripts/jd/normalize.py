"""Pure Role Family derivation without losing per-requisition bodies or evidence."""
from __future__ import annotations
import re
from typing import Any
from dataclasses import asdict
from .model import Job, txt

def family_title(title: str) -> str:
    title_lines = (title or "").splitlines()
    first = (title_lines[0] if title_lines else "").strip()
    return re.sub(r"\s+-\s+.+$", "", re.sub(r"\s+", " ", first)).strip()


def normalize(all_matches, manual_seed_payload, previous_payload, results):
    family_map: dict[tuple[str, str], dict[str, Any]] = {}
    for j in all_matches:
        family = family_title(j.title)
        key = (j.company, family)
        item = family_map.setdefault(key, {
            "company": j.company,
            "role_family": family,
            "representative_title": (j.title or "").splitlines()[0].strip(),
            "locations": set(),
            "description": "",
            "requirements": "",
            "cycle_evidence": "",
            "requisitions": [],
            "detail_status": "TITLE_ONLY_OFFICIAL",
        })
        for loc in re.split(r"\s*/\s*|,\s*", j.location or ""):
            if loc:
                item["locations"].add(loc)
        old_score = len(item["description"]) + len(item["requirements"])
        new_score = len(j.description or "") + len(j.requirements or "")
        if new_score > old_score:
            item["description"] = j.description or ""
            item["requirements"] = j.requirements or ""
            item["representative_title"] = (j.title or "").splitlines()[0].strip()
            item["cycle_evidence"] = j.cycle_evidence or ""
        if item["description"] or item["requirements"]:
            item["detail_status"] = "FULL_JD"
        req = asdict(j)
        if not any(
            (req["job_id"] and x.get("job_id") == req["job_id"])
            or (
                not req["job_id"]
                and x.get("official_url") == req["official_url"]
                and x.get("title") == req["title"]
            )
            for x in item["requisitions"]
        ):
            item["requisitions"].append(req)

    role_families = []
    for item in family_map.values():
        role_families.append({
            **item,
            "locations": sorted(item["locations"]),
        })
    role_families.sort(key=lambda x: (x["company"], x["role_family"]))

    # First-party manual seeds cover official pages that are current and
    # verifiable but not reliably enumerable (SPA/WAF/signed ATS). They never
    # import secondary-source JD text. Fresh automated FULL_JD data wins.
    automated_keys = {(x["company"], x["role_family"]) for x in role_families}
    seeded_companies: set[str] = set()
    for seed in manual_seed_payload.get("roles") or []:
        company = txt(seed.get("company"))
        family = txt(seed.get("title"))
        if not company or not family:
            continue
        key = (company, family)
        seeded_companies.add(company)
        if key in automated_keys:
            continue
        role_families.append({
            "company": company,
            "role_family": family,
            "representative_title": family,
            "locations": list(seed.get("locations") or []),
            "description": "",
            "requirements": "",
            "evidence_summary": txt(seed.get("evidence_summary")),
            "cycle_evidence": txt(seed.get("recruitment_type")),
            "requisitions": [{
                "job_id": txt(seed.get("job_id")),
                "title": family,
                "location": " / ".join(seed.get("locations") or []),
                "official_url": txt(seed.get("official_url")),
                "official_api": "FIRST_PARTY_MANUAL_SEED",
            }],
            "source_evidence": ["FIRST_PARTY_MANUAL_SEED"],
            "evidence_url": txt(seed.get("evidence_url") or seed.get("official_url")),
            "detail_status": "ROLE_VERIFIED_CURRENT_SOURCE",
            "manual_first_party_seed": True,
            "verified_on": txt(seed.get("verified_on")),
        })
        automated_keys.add(key)

    role_families.sort(key=lambda x: (x["company"], x["role_family"]))

    # Preserve the last verified role families whenever this run did not
    # successfully enumerate matching roles for that company. This prevents
    # an incomplete/blocked/zero-result crawl from erasing known-good data.
    current_keys = {(x["company"], x["role_family"]) for x in role_families}
    result_map = {r.company: r for r in results}
    live_match_companies = {
        r.company for r in results if r.status == "ENUMERATED_WITH_MATCHES"
    }
    live_zero_companies = {
        r.company for r in results if r.status == "ENUMERATED_ZERO_MATCHES"
    }
    for old in previous_payload.get("role_families") or []:
        company = old.get("company")
        family = old.get("role_family")
        if not company or not family or company in live_match_companies or company in live_zero_companies:
            continue
        key = (company, family)
        if key in current_keys:
            current = next(x for x in role_families if (x["company"], x["role_family"]) == key)
            # A title-only manual seed must not hide an already captured body
            # when this run could not complete the official enumeration.
            if current.get("manual_first_party_seed"):
                saved_seed = dict(current)
                current.update(old)
                current["manual_seed_evidence"] = saved_seed
                current["carried_forward"] = True
                current["carry_reason"] = result_map[company].status if company in result_map else "NO_RUNTIME_RESULT"
        else:
            carried = dict(old)
            carried["carried_forward"] = True
            carried["carry_reason"] = (
                result_map.get(company).status
                if result_map.get(company)
                else "NO_RUNTIME_RESULT"
            )
            role_families.append(carried)
            current_keys.add(key)

    return role_families, seeded_companies
