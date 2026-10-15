"""Small-batch semantic review bridge for scheduled ChatGPT audits.

GitHub Actions owns deterministic state transitions and catalog writes. A scheduled
ChatGPT task only reads audit-batch.json and writes audit-decisions.json.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .automation import job_identity, now_utc
from .catalog import load_catalog, render_catalog

AUDIT_SCHEMA_VERSION = 1
ROLE_TRACKS = {
    "应用与Agent核心研发",
    "评测与测试工具研发",
    "算法或研究与应用工程混合",
    "多方向或跨职能工程",
}
DECISIONS = {"include", "exclude", "remove"}


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


def prepare_batch(*, queue_file: Path, batch_file: Path, limit: int) -> dict:
    """Export the next bounded batch of unscreened official JD changes."""
    if limit <= 0:
        raise ValueError("batch limit must be positive")
    queue = _load(queue_file, {"schema_version": 2, "entries": {}})
    entries = queue.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("screening queue entries must be an object")
    pending = [entry for entry in entries.values()
               if isinstance(entry, dict) and entry.get("review_state") == "pending"]
    pending.sort(key=lambda entry: (str(entry.get("first_seen_at_utc") or ""),
                                    str(entry.get("event_id") or "")))
    selected = pending[:limit]
    event_ids = [str(entry.get("event_id") or "") for entry in selected]
    batch_id = (hashlib.sha256("\n".join(event_ids).encode("utf-8")).hexdigest()[:24]
                if event_ids else "empty")
    payload = {
        "schema_version": AUDIT_SCHEMA_VERSION,
        "generated_at_utc": now_utc(),
        "batch_id": batch_id,
        "pending_total": len(pending),
        "count": len(selected),
        "entries": selected,
        "policy": ("Read the complete official duties, qualifications and campus/internship evidence. "
                   "Include only software engineering delivering AI applications, Agent, LLM/RAG, "
                   "runtime/platform or evaluation tooling. Quote exact engineering evidence. "
                   "Otherwise exclude with an evidence-based reason; use remove only for a "
                   "confirmed disappeared position. Never decide by title or keywords, "
                   "and never return needs_review."),
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
    if not str(decision.get("decision_reason") or "").strip():
        raise ValueError("Every final audit decision needs a concrete evidence reason")


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
        return {"applied": 0, "included": 0, "excluded": 0, "removed": 0}

    official_file = Path(official_file)
    bytedance_file = Path(bytedance_file)
    official = json.loads(official_file.read_text(encoding="utf-8"))
    bytedance = json.loads(bytedance_file.read_text(encoding="utf-8"))
    queue_entries = queue.get("entries")
    if not isinstance(queue_entries, dict):
        raise ValueError("review queue entries must be an object")

    counts = {"applied": 0, "included": 0, "excluded": 0, "removed": 0}
    seen = set()
    for decision in decisions:
        _validate_decision(decision)
        event_id = decision["event_id"]
        if event_id in seen:
            raise ValueError(f"Duplicate audit decision for {event_id}")
        seen.add(event_id)
        entry = queue_entries.get(event_id)
        if not isinstance(entry, dict):
            # A newer scan may supersede this pending JD while GPT is reading it.
            continue
        state = entry.get("review_state")
        if state != "pending":
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
            # A deficient scan event cannot revoke a separately reviewed full JD.
            # Revocation requires an actual full-JD change or verified ineligibility
            # already documented in the existing formal record.
            expired_campus = (
                index is not None
                and decision.get("evidence_gate") == "过期校招批次"
                and "2026" in str(jobs[index].get("cohort") or "")
            )
            materially_changed = (
                entry.get("change") == "changed"
                and bool(_full_text(_entry_job(entry)))
            )
            if index is not None and (expired_campus or materially_changed):
                jobs.pop(index)
            counts["excluded"] += 1
        elif outcome == "remove":
            if entry.get("change") != "possibly_removed":
                raise ValueError("remove is only valid for possibly_removed events")
            if index is not None:
                jobs.pop(index)
            counts["removed"] += 1
        else:
            raise ValueError(f"Unsupported terminal outcome: {outcome}")

        # Every event has one terminal decision. Missing evidence is an exclusion,
        # not an endless needs_review retry loop.
        entry["review_state"] = "reviewed"
        entry["semantic_review"] = {
            "decision": outcome,
            "decision_reason": str(decision.get("decision_reason") or "").strip(),
            "reviewed_at_utc": now_utc(),
            "review_depth": "full_jd" if entry.get("job") else "source_state",
            "batch_id": payload.get("batch_id"),
        }
        counts["applied"] += 1

    # The queue is temporary transport, not a second permanent audit database.
    for event_id in seen:
        queue_entries.pop(event_id, None)

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
