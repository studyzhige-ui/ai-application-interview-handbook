"""Small-batch semantic review bridge for scheduled ChatGPT audits.

GitHub Actions owns deterministic state transitions and catalog writes. A scheduled
ChatGPT task only reads audit-batch.json and writes audit-decisions.json.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from .automation import canonical_url, job_identity, now_utc
from .catalog import load_catalog, render_catalog

AUDIT_SCHEMA_VERSION = 1
ROLE_TRACKS = {
    "应用与Agent核心研发",
    "评测与测试工具研发",
    "算法或研究与应用工程混合",
    "多方向或跨职能工程",
}
DECISIONS = {"include", "exclude", "needs_review", "remove"}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _load(path: Path, default):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_like(path: Path, payload) -> None:
    """Preserve whether a large existing JSON file is compact or pretty printed."""
    path = Path(path)
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    pretty = "\n" in old.strip()
    if pretty:
        text = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    path.write_text(text + "\n", encoding="utf-8")



def _entry_job(entry: dict) -> dict:
    job = entry.get("job")
    return job if isinstance(job, dict) else {}


def _stable_key(entry: dict) -> str:
    """Return a source-scoped requisition key when the transport exposed enough identity."""
    source_id = str(entry.get("source_id") or "")
    job = _entry_job(entry)
    req_id = str(job.get("req_id") or job.get("job_id") or "").strip()
    if req_id:
        return f"{source_id}:id:{req_id}"

    url = canonical_url(job.get("official_url") or "")
    if url:
        path = urlsplit(url).path
        match = re.search(r"(?:position|job-info|jobs?|detail)/(\d{5,})", path, re.I)
        if match:
            return f"{source_id}:id:{match.group(1)}"
        return f"{source_id}:url:{url}"

    identity = str(entry.get("identity") or "")
    return f"{source_id}:identity:{identity}"


def _job_quality(entry: dict) -> tuple[int, int, int]:
    """Prefer stable IDs and separately extracted full JD fields over listing-text fallbacks."""
    job = _entry_job(entry)
    req_id = str(job.get("req_id") or job.get("job_id") or "").strip()
    description = str(job.get("description") or "").strip()
    requirements = str(job.get("requirements") or "").strip()
    title = str(job.get("title") or "").strip()
    full = bool(description or requirements)
    multiline_title = "\n" in title
    return (2 if full else 0, 1 if req_id else 0, 0 if multiline_title and not full else 1)


def _queue_full_text(entry: dict) -> str:
    job = _entry_job(entry)
    return _full_text(job)


def _official_keys(catalog: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    by_identity: dict[str, dict] = {}
    by_stable: dict[str, dict] = {}
    for company in catalog.get("companies", []):
        source_id = str(company.get("source_id") or "")
        for job in company.get("jobs", []):
            try:
                identity = job_identity(source_id, job)
            except Exception:
                identity = ""
            if identity:
                by_identity[f"{source_id}:{identity}"] = job
            req_id = str(job.get("req_id") or job.get("job_id") or "").strip()
            if req_id:
                by_stable[f"{source_id}:id:{req_id}"] = job
            url = canonical_url(job.get("official_url") or "")
            if url:
                by_stable.setdefault(f"{source_id}:url:{url}", job)
    return by_identity, by_stable


def _mark_ignored(entry: dict, *, reason: str, kind: str) -> None:
    entry["review_state"] = "ignored"
    entry["semantic_review"] = {
        "decision": "ignored",
        "decision_reason": reason,
        "reviewed_at_utc": now_utc(),
        "review_depth": "mechanical_dedup",
        "kind": kind,
    }



def _prior_exclusions(catalog: dict) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = {}
    for company in catalog.get("companies", []):
        source_id = str(company.get("source_id") or "")
        for observation in company.get("other_observations", []):
            if observation.get("decision") != "exclude":
                continue
            req_id = str(observation.get("req_id") or observation.get("job_id") or "").strip()
            if not req_id:
                continue
            index.setdefault(f"{source_id}:id:{req_id}", []).append(observation)
    return index



def _prior_exclusions_by_url_title(catalog: dict) -> dict[tuple[str, str, str], list[dict]]:
    index: dict[tuple[str, str, str], list[dict]] = {}
    for company in catalog.get("companies", []):
        source_id = str(company.get("source_id") or "")
        for observation in company.get("other_observations", []):
            if observation.get("decision") != "exclude":
                continue
            title = str(observation.get("title") or "").strip()
            url = canonical_url(observation.get("official_url") or "")
            if not title or not url:
                continue
            index.setdefault((source_id, title, url), []).append(observation)
    return index


def _body_hash_candidates(job: dict) -> set[str]:
    description = str(job.get("description") or "").strip()
    requirements = str(job.get("requirements") or "").strip()
    candidates = set()
    if description:
        candidates.add(description)
    if description and requirements:
        candidates.add(f"{description}\n\n{requirements}")
        candidates.add(f"职位描述\n{description}\n职位要求\n{requirements}")
    return {hashlib.sha256(text.encode("utf-8")).hexdigest() for text in candidates}


def _mark_reused_exclusion(entry: dict, *, observation: dict, reason: str) -> None:
    entry["review_state"] = "reviewed"
    entry["semantic_review"] = {
        "decision": "exclude",
        "decision_reason": reason,
        "reviewed_at_utc": now_utc(),
        "review_depth": "reused_existing_semantic_exclusion",
        "kind": "prior_semantic_exclusion",
        "prior_review_depth": observation.get("review_depth"),
    }


def _mark_reused_review(entry: dict, *, reason: str) -> None:
    entry["review_state"] = "reviewed"
    entry["semantic_review"] = {
        "decision": "include",
        "decision_reason": reason,
        "reviewed_at_utc": now_utc(),
        "review_depth": "reused_existing_full_jd_review",
        "kind": "already_reviewed_include",
    }


def compact_backlog(*, queue_file: Path, official_file: Path) -> dict:
    """Resolve only mechanically provable backlog redundancy; never infer role eligibility."""
    queue = _load(queue_file, {"schema_version": 2, "entries": {}})
    entries = queue.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("review queue entries must be an object")

    catalog = load_catalog(official_file)
    official_by_identity, official_by_stable = _official_keys(catalog)
    prior_exclusions = _prior_exclusions(catalog)
    prior_exclusions_by_url_title = _prior_exclusions_by_url_title(catalog)
    pending = [
        entry for entry in entries.values()
        if isinstance(entry, dict) and entry.get("review_state") == "pending"
    ]
    result = {
        "pending_before": len(pending),
        "already_reviewed": 0,
        "reused_exclusions": 0,
        "identity_migration_exclusions": 0,
        "unpublished_removals": 0,
        "superseded": 0,
        "duplicate_fallbacks": 0,
    }

    # First, reuse prior full-JD review when the same requisition still has byte-equivalent body text.
    for entry in pending:
        source_id = str(entry.get("source_id") or "")
        identity = str(entry.get("identity") or "")
        stable = _stable_key(entry)
        existing = official_by_identity.get(f"{source_id}:{identity}") or official_by_stable.get(stable)
        if entry.get("change") == "possibly_removed":
            if existing is None:
                _mark_ignored(
                    entry,
                    reason="该职位从未进入正式审核通过库；消失事件无需执行删除。",
                    kind="unpublished_removal",
                )
                result["unpublished_removals"] += 1
            continue
        if existing is None:
            job = _entry_job(entry)
            stable = _stable_key(entry)
            for observation in prior_exclusions.get(stable, []):
                review_depth = str(observation.get("review_depth") or "")
                description = str(job.get("description") or "").strip()
                exact_duties = (
                    review_depth == "full_list_duties"
                    and observation.get("duties_read") is True
                    and bool(description)
                    and hashlib.sha256(description.encode("utf-8")).hexdigest()
                        == observation.get("description_sha256")
                )
                exact_full_jd = (
                    review_depth in {"full_jd", "inherited_full_jd", "full_jd_read"}
                    and bool(observation.get("body_sha256"))
                    and observation.get("body_sha256") in _body_hash_candidates(job)
                )
                if exact_duties or exact_full_jd:
                    prior_reason = str(observation.get("decision_reason") or "").strip()
                    reason = (
                        "复用同一官方职位此前的语义排除结论：当前职责正文与此前已完整读取职责的记录哈希完全一致。"
                        if exact_duties else
                        "复用同一官方职位此前的完整 JD 语义排除结论：当前正文哈希与既有审核记录完全一致。"
                    )
                    if prior_reason:
                        reason += " 原审核理由：" + prior_reason
                    _mark_reused_exclusion(entry, observation=observation, reason=reason)
                    result["reused_exclusions"] += 1
                    break
            if entry.get("review_state") == "pending" and entry.get("change") == "added":
                triage_priority = str((entry.get("triage") or {}).get("priority") or "")
                title = str(job.get("title") or "").strip()
                url = canonical_url(job.get("official_url") or "")
                if triage_priority == "low" and title and url:
                    migrated = prior_exclusions_by_url_title.get((source_id, title, url), [])
                    if migrated:
                        observation = migrated[0]
                        prior_reason = str(observation.get("decision_reason") or "").strip()
                        reason = (
                            "该条为职位身份字段迁移造成的假新增：官方 URL 与职位标题均与此前已完成语义排除的同一职位完全一致，"
                            "且当前完整 JD 的自动 triage 仍为低优先；复用既有语义排除结论。"
                        )
                        if prior_reason:
                            reason += " 原审核理由：" + prior_reason
                        _mark_reused_exclusion(entry, observation=observation, reason=reason)
                        entry["semantic_review"]["kind"] = "identity_migration_prior_exclusion"
                        result["identity_migration_exclusions"] += 1
            continue
        current_text = _queue_full_text(entry)
        reviewed_text = str(existing.get("full_text") or "").strip()
        if current_text and current_text == reviewed_text:
            _mark_reused_review(
                entry,
                reason="当前完整 JD 正文与正式库中已完成 full_jd 语义审核的同一职位完全一致，复用既有审核结论。",
            )
            result["already_reviewed"] += 1

    # Then collapse multiple pending events for the same official requisition.
    groups: dict[str, list[dict]] = {}
    for entry in entries.values():
        if not isinstance(entry, dict) or entry.get("review_state") != "pending":
            continue
        if entry.get("change") == "possibly_removed":
            continue
        groups.setdefault(_stable_key(entry), []).append(entry)

    for stable, group in groups.items():
        if len(group) <= 1:
            continue
        # Newest event wins among equally complete records; full extracted JD beats listing fallbacks.
        ranked = sorted(
            group,
            key=lambda entry: (
                _job_quality(entry),
                str(entry.get("first_seen_at_utc") or ""),
                str(entry.get("event_id") or ""),
            ),
            reverse=True,
        )
        keeper = ranked[0]
        keeper_quality = _job_quality(keeper)
        for redundant in ranked[1:]:
            quality = _job_quality(redundant)
            if quality < keeper_quality:
                kind = "duplicate_fallback"
                reason = (
                    "同一官方职位已有包含稳定职位 ID 且职责/任职要求分字段提取的更完整事件；"
                    "本条仅为列表页/标题降级重复记录，不再单独语义审核。"
                )
                result["duplicate_fallbacks"] += 1
            else:
                kind = "superseded"
                reason = (
                    "同一官方职位存在更新或等价的待审事件；只保留信息更完整且更新的一条进行完整 JD 语义审核。"
                )
                result["superseded"] += 1
            _mark_ignored(redundant, reason=reason, kind=kind)

    remaining = sum(
        1 for entry in entries.values()
        if isinstance(entry, dict) and entry.get("review_state") == "pending"
    )
    result["pending_after"] = remaining
    queue["last_compaction"] = {
        "checked_at_utc": now_utc(),
        **result,
        "policy": (
            "Compaction only reuses byte-equivalent prior full-JD reviews and removes mechanically "
            "redundant/superseded queue events. It never decides new role eligibility."
        ),
    }
    _write_json(queue_file, queue)
    return result


def prepare_batch(*, queue_file: Path, batch_file: Path, limit: int) -> dict:
    if limit <= 0:
        raise ValueError("audit batch limit must be positive")
    queue = _load(queue_file, {"schema_version": 2, "entries": {}})
    entries = queue.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("review queue entries must be an object")

    pending = [
        entry for entry in entries.values()
        if isinstance(entry, dict) and entry.get("review_state") == "pending"
    ]
    pending.sort(
        key=lambda entry: (
            PRIORITY_ORDER.get((entry.get("triage") or {}).get("priority"), 9),
            str(entry.get("first_seen_at_utc") or ""),
            str(entry.get("event_id") or ""),
        )
    )
    selected = pending[:limit]
    event_ids = [str(entry.get("event_id") or "") for entry in selected]
    batch_id = (
        hashlib.sha256("\n".join(event_ids).encode("utf-8")).hexdigest()[:24]
        if event_ids else "empty"
    )
    payload = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "generated_at_utc": now_utc(),
        "batch_id": batch_id,
        "pending_total": len(pending),
        "count": len(selected),
        "entries": selected,
        "policy": (
            "Read the complete job description and requirements for every entry. "
            "Do not decide from title or keywords alone. Include only AI application/Agent/LLM/RAG/"
            "AI platform engineering/evaluation engineering roles with explicit implementation work. "
            "Use needs_review when the JD evidence is insufficient."
        ),
    }
    _write_json(batch_file, payload)
    return payload


def _company_and_jobs(official: dict, bytedance: dict, source_id: str):
    for company in official.get("companies", []):
        if company.get("source_id") != source_id:
            continue
        if source_id == "official-012" and company.get("jobs_file") is not None:
            if bytedance.get("source_id") != source_id or not isinstance(bytedance.get("jobs"), list):
                raise ValueError("ByteDance partition is missing or invalid")
            return company, bytedance["jobs"]
        jobs = company.setdefault("jobs", [])
        if not isinstance(jobs, list):
            raise ValueError(f"{source_id}: jobs must be a list")
        return company, jobs
    raise ValueError(f"Unknown source in decision: {source_id}")


def _find_job_index(source_id: str, jobs: list[dict], identity: str):
    for index, job in enumerate(jobs):
        try:
            if job_identity(source_id, job) == identity:
                return index
        except Exception:
            continue
    return None


def _full_text(job: dict) -> str:
    parts: list[str] = []
    for key in ("description", "requirements"):
        value = str(job.get(key) or "").strip()
        if value and value not in parts:
            parts.append(value)
    return "\n\n".join(parts).strip()


def _locations(job: dict) -> list:
    value = job.get("locations")
    if isinstance(value, list):
        return value
    value = job.get("location")
    if isinstance(value, list):
        return value
    if value not in (None, ""):
        return [value]
    return []


def _catalog_record(entry: dict, decision: dict, existing: dict | None) -> dict:
    if entry.get("change") not in {"added", "changed"}:
        raise ValueError("Only added/changed events can be included")
    job = entry.get("job")
    if not isinstance(job, dict):
        raise ValueError("Included event has no JD payload")
    req_id = str(job.get("req_id") or job.get("job_id") or "").strip()
    title = str(job.get("title") or "").strip()
    official_url = str(job.get("official_url") or "").strip()
    full_text = _full_text(job)
    if not req_id or not title or not official_url or not full_text:
        raise ValueError("Included event lacks requisition id, title, URL or full JD text")

    role_track = decision.get("role_track")
    if role_track not in ROLE_TRACKS:
        raise ValueError("Included decision has unsupported role_track")
    recruitment_type = decision.get("recruitment_type")
    if recruitment_type not in {"campus", "internship"}:
        raise ValueError("Included decision needs campus/internship recruitment_type")
    reason = str(decision.get("decision_reason") or "").strip()
    type_evidence = str(decision.get("official_type_evidence") or "").strip()
    evidence = decision.get("engineering_evidence")
    if not reason or not type_evidence:
        raise ValueError("Included decision lacks decision/type evidence")
    if not isinstance(evidence, list) or not evidence or any(
        not isinstance(item, str) or not item.strip() or item.strip() not in full_text
        for item in evidence
    ):
        raise ValueError("engineering_evidence must contain verbatim snippets from the full JD")

    record = dict(existing or {})
    record.update({
        "req_id": req_id,
        "title": title,
        "official_url": official_url,
        "full_text": full_text,
        "decision_reason": reason,
        "official_type_evidence": type_evidence,
        "checked_at_utc": now_utc(),
        "decision": "include",
        "review_depth": "full_jd",
        "recruitment_type": recruitment_type,
        "official_recruitment_type": str(
            decision.get("official_recruitment_type") or recruitment_type
        ),
        "locations": _locations(job),
        "body_sha256": hashlib.sha256(full_text.encode("utf-8")).hexdigest(),
        "engineering_evidence": [item.strip() for item in evidence],
        "role_track": role_track,
    })
    for key in ("category", "department", "official_api", "cycle_evidence"):
        if job.get(key) not in (None, ""):
            record[key] = job.get(key)
    if decision.get("cohort") not in (None, ""):
        record["cohort"] = decision.get("cohort")
    return record


def _raw_counts(official: dict, bytedance: dict) -> dict:
    companies = official.get("companies", [])
    current_jobs = 0
    companies_with_current_jobs = 0
    coverage = {level: 0 for level in ("complete", "limited", "restricted", "not_started")}
    for company in companies:
        source_id = company.get("source_id")
        if source_id == "official-012" and company.get("jobs_file") is not None:
            jobs = bytedance.get("jobs") or []
        else:
            jobs = company.get("jobs") or []
        current_jobs += len(jobs)
        companies_with_current_jobs += bool(jobs)
        level = (company.get("coverage") or {}).get("coverage_level")
        if level in coverage:
            coverage[level] += 1
    previous = official.get("counts") or {}
    return {
        "registered_sources": len(companies),
        "current_jobs": current_jobs,
        "companies_with_current_jobs": companies_with_current_jobs,
        "historical_observations": int(previous.get("historical_observations") or 0),
        "coverage": coverage,
    }


def _validate_decision(decision: dict) -> None:
    if not isinstance(decision, dict) or not decision.get("event_id"):
        raise ValueError("Every audit decision needs an event_id")
    if decision.get("decision") not in DECISIONS:
        raise ValueError(f"Unsupported audit decision: {decision.get('decision')}")


def apply_decisions(
    *,
    queue_file: Path,
    decisions_file: Path,
    official_file: Path,
    bytedance_file: Path,
    index_file: Path,
) -> dict:
    queue = _load(queue_file, {"schema_version": 2, "entries": {}})
    payload = _load(decisions_file, {"schema_version": AUDIT_SCHEMA_VERSION, "decisions": []})
    if payload.get("schema_version") != AUDIT_SCHEMA_VERSION:
        raise ValueError("Unsupported audit decision schema")
    decisions = payload.get("decisions") or []
    if not isinstance(decisions, list):
        raise ValueError("audit decisions must be a list")
    if not decisions:
        return {"applied": 0, "included": 0, "excluded": 0, "needs_review": 0, "removed": 0}

    official_file = Path(official_file)
    bytedance_file = Path(bytedance_file)
    official = json.loads(official_file.read_text(encoding="utf-8"))
    bytedance = json.loads(bytedance_file.read_text(encoding="utf-8"))
    queue_entries = queue.get("entries")
    if not isinstance(queue_entries, dict):
        raise ValueError("review queue entries must be an object")

    counts = {"applied": 0, "included": 0, "excluded": 0, "needs_review": 0, "removed": 0}
    seen = set()
    for decision in decisions:
        _validate_decision(decision)
        event_id = decision["event_id"]
        if event_id in seen:
            raise ValueError(f"Duplicate audit decision for {event_id}")
        seen.add(event_id)
        entry = queue_entries.get(event_id)
        if not isinstance(entry, dict):
            raise ValueError(f"Unknown audit event: {event_id}")
        if entry.get("review_state") != "pending":
            continue

        source_id = entry.get("source_id")
        identity = entry.get("identity")
        company, jobs = _company_and_jobs(official, bytedance, source_id)
        index = _find_job_index(source_id, jobs, identity)
        outcome = decision["decision"]

        if outcome == "include":
            existing = jobs[index] if index is not None else None
            record = _catalog_record(entry, decision, existing)
            if index is None:
                jobs.append(record)
            else:
                jobs[index] = record
            counts["included"] += 1
        elif outcome == "exclude":
            if index is not None:
                jobs.pop(index)
            counts["excluded"] += 1
        elif outcome == "remove":
            if entry.get("change") != "possibly_removed":
                raise ValueError("remove is only valid for possibly_removed events")
            if index is not None:
                jobs.pop(index)
            counts["removed"] += 1
        else:
            counts["needs_review"] += 1

        entry["review_state"] = "reviewed"
        entry["semantic_review"] = {
            "decision": outcome,
            "decision_reason": str(decision.get("decision_reason") or "").strip(),
            "reviewed_at_utc": now_utc(),
            "review_depth": "full_jd" if entry.get("job") else "source_state",
            "batch_id": payload.get("batch_id"),
        }
        counts["applied"] += 1

    official["counts"] = _raw_counts(official, bytedance)
    official["last_semantic_audit_at_utc"] = now_utc()

    _write_like(bytedance_file, bytedance)
    partition_raw = bytedance_file.read_bytes()
    for company in official.get("companies", []):
        if company.get("source_id") == "official-012" and company.get("jobs_file") is not None:
            company["jobs_file"]["bytes"] = len(partition_raw)
            company["jobs_file"]["sha256"] = hashlib.sha256(partition_raw).hexdigest()
            break
    _write_like(official_file, official)
    _write_json(queue_file, queue)

    catalog = load_catalog(official_file)
    index_file = Path(index_file)
    index_file.write_text(render_catalog(catalog), encoding="utf-8")

    receipt = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "last_batch_id": payload.get("batch_id"),
        "applied_at_utc": now_utc(),
        "decisions": [],
        "last_result": counts,
    }
    _write_json(decisions_file, receipt)
    return counts
