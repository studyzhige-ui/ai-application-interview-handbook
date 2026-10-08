"""Small business pipeline: collect → normalize → preserve state → write projections."""
import json
import os
from datetime import datetime, timezone
from .paths import CONFIG, VERIFIED_INDEX, MANUAL_ROLE_SEEDS, OUT_JSON
from .collection import collect_sources
from .normalize import normalize
from .state import update_state
from .render import render

def read_required(path):
    # Corrupt persistent data is a hard failure, never an empty state to overwrite.
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    cfg = read_required(CONFIG)
    verified_index = read_required(VERIFIED_INDEX)
    seeds = read_required(MANUAL_ROLE_SEEDS)
    previous = read_required(OUT_JSON)
    results, jobs = collect_sources(cfg)
    families, seeded = normalize(jobs, seeds, previous, results)
    verified_index, families = update_state(cfg, verified_index, families, seeded, results)
    payload = render(cfg, verified_index, families, jobs, results,
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        os.environ.get("SYNC_SOURCE_SHA", "").strip())
    print(f"official sources={len(results)}, requisitions={len(jobs)}, role_families={len(families)}")
    return 0
