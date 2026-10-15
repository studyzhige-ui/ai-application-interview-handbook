"""Read-only source, catalog and automation-state integrity checks; no role eligibility judgments."""
from __future__ import annotations

import hashlib
import json
from urllib.parse import urlparse

from .paths import BUSINESS, CONFIG
from .catalog import validate_catalog, render_catalog, load_catalog

AUTOMATION_SCHEMA_VERSION = 2


def _validate_automation(registered_ids):
    errors = []
    state_path = BUSINESS / "01-data/automation/scan-state.json"
    queue_path = BUSINESS / "01-data/automation/review-queue.json"
    if not state_path.is_file() or not queue_path.is_file():
        errors.append("Automation state and review queue must both exist")
        return errors
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Automation JSON unreadable: {exc}"]
    if state.get("schema_version") != AUTOMATION_SCHEMA_VERSION:
        errors.append("Automation scan-state schema version mismatch")
    if queue.get("schema_version") != AUTOMATION_SCHEMA_VERSION:
        errors.append("Automation review-queue schema version mismatch")
    sources = state.get("sources")
    entries = queue.get("entries")
    if not isinstance(sources, dict):
        errors.append("Automation scan-state sources must be an object")
        sources = {}
    if not isinstance(entries, dict):
        errors.append("Automation review queue entries must be an object")
        entries = {}
    unknown_sources = set(sources) - set(registered_ids)
    if unknown_sources:
        errors.append("Automation state contains unregistered source IDs: " + ", ".join(sorted(unknown_sources)))
    for source_id, source in sources.items():
        if not isinstance(source, dict):
            errors.append(f"{source_id}: automation source state must be an object")
            continue
        if source.get("baseline_ready") not in (True, False, None):
            errors.append(f"{source_id}: automation baseline_ready must be boolean")
        jobs = source.get("jobs", {})
        if not isinstance(jobs, dict):
            errors.append(f"{source_id}: automation jobs baseline must be an object")
            continue
        for identity, job in jobs.items():
            if not identity or not isinstance(job, dict) or not job.get("fingerprint"):
                errors.append(f"{source_id}: invalid automation job baseline entry")
                break
    for event_id, entry in entries.items():
        if not event_id or not isinstance(entry, dict):
            errors.append("Automation review queue contains invalid event entry")
            continue
        if entry.get("event_id") != event_id:
            errors.append(f"Automation event key mismatch: {event_id}")
        if entry.get("source_id") not in registered_ids:
            errors.append(f"Automation event uses unregistered source: {event_id}")
        if entry.get("change") not in {"added", "changed", "possibly_removed"}:
            errors.append(f"Automation event has unsupported change type: {event_id}")
        if entry.get("review_state") not in {"pending", "reviewed", "needs_review", "ignored"}:
            errors.append(f"Automation event has unsupported review_state: {event_id}")
    return errors


def main():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    manifest = json.loads((BUSINESS / "03-strategy/stored-snapshots.json").read_text(encoding="utf-8"))
    errors = []
    sources = cfg["sources"]
    ids = [source.get("source_id") for source in sources]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        errors.append("Source IDs must be nonempty and unique")
    if len(sources) != cfg["expected_company_count"]:
        errors.append("Registered source count differs from the recorded count")
    if cfg.get("code_collection_enabled_by_default") is not False:
        errors.append("Interactive code collection must remain disabled by default; scheduled automation enables it explicitly")
    for source in sources:
        for key in ("portal", "official_root", "job_list_url"):
            parsed = urlparse(source.get(key, ""))
            if parsed.scheme != "https" or not parsed.hostname:
                errors.append(f"{source['source_id']}: invalid stored {key}")
    total_bytes = 0
    for entry in manifest["files"]:
        path = BUSINESS / entry["path"]
        if not path.is_file():
            errors.append(f"Missing stored snapshot: {entry['path']}")
            continue
        raw = path.read_bytes()
        total_bytes += len(raw)
        if len(raw) != entry["bytes"] or hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            errors.append(f"Stored snapshot bytes changed: {entry['path']}")
    catalog_path = BUSINESS / "01-data/official-jds.json"
    catalog = load_catalog(catalog_path)
    errors.extend(validate_catalog(catalog, ids))
    if (BUSINESS / "01-data/岗位JD.md").read_text(encoding="utf-8") != render_catalog(catalog):
        errors.append("Readable job index differs from the authoritative catalog")
    errors.extend(_validate_automation(ids))
    print(f"Stored sources={len(sources)}, snapshots={len(manifest['files'])}, bytes={total_bytes}, errors={len(errors)}")
    for error in errors:
        print("ERROR:", error)
    return 1 if errors else 0
