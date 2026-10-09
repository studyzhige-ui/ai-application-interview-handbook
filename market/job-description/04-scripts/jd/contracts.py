"""Read-only source integrity and count checks; no role eligibility judgments."""
from __future__ import annotations
import hashlib
import json
from urllib.parse import urlparse
from .paths import BUSINESS, CONFIG
from .catalog import validate_catalog, render_catalog, load_catalog


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
        errors.append("Code collection must remain disabled by default")
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
    catalog_path = BUSINESS / '01-data/official-jds.json'
    catalog = load_catalog(catalog_path)
    errors.extend(validate_catalog(catalog, ids))
    if (BUSINESS / '01-data/岗位JD.md').read_text(encoding='utf-8') != render_catalog(catalog):
        errors.append('Readable job index differs from the authoritative catalog')
    print(f"Stored sources={len(sources)}, snapshots={len(manifest['files'])}, bytes={total_bytes}, errors={len(errors)}")
    for error in errors:
        print("ERROR:", error)
    return 1 if errors else 0
