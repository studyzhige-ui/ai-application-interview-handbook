"""Reject expired, future, wrong-commit, or previous-run discovery caches."""
import os
from datetime import datetime, timezone
CACHE_MAX_AGE_SECONDS = 6 * 60 * 60

def cache_is_fresh(payload: dict) -> bool:
    for env_name, field in (("SYNC_SOURCE_SHA", "source_commit"), ("GITHUB_RUN_ID", "run_id"), ("GITHUB_RUN_ATTEMPT", "run_attempt")):
        expected = os.environ.get(env_name, "").strip()
        if expected and str(payload.get(field) or "") != expected:
            return False
    raw = str(payload.get("generated_at") or "").strip()
    try:
        stamp = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return False
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - stamp.astimezone(timezone.utc)).total_seconds()
    return -300 <= age <= CACHE_MAX_AGE_SECONDS
