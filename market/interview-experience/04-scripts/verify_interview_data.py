#!/usr/bin/env python3
"""Verify preserved bytes, structural IDs, references and explicit review counts.

Offline and read-only by default. --write-index refreshes only the source index
and raw-file manifest after the approved corpus contract/provenance are updated.
No classification, semantic grouping, normalization or inferred review labels.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, unquote

BUSINESS = Path(__file__).resolve().parents[1]
SOURCE = re.compile(r"^## (S\d{3,}) (.+)$")
EXTENSION = re.compile(r"^## Existing-process extension.*?\b(S\d{3,})\b(.*)$")
BOUNDARY = re.compile(r"^#{1,2} ")
NUMBERED = re.compile(r"^(\d+)\.\s+(.+)$")
URL = re.compile(r"https?://[^\s<>`]+")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dumps(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def local_path(base, relative):
    path = (base / relative).resolve()
    require(path.is_relative_to(base.resolve()), f"Path escapes corpus: {relative}")
    return path


def parse_corpus(base=BUSINESS):
    """Read formal blocks and list syntax; semantic content stays uninterpreted."""
    contract = load(base / "03-strategy/corpus-contract.json")
    proof = load(base / "01-data/source-provenance.json")["sections"]
    origins = {}
    for origin in proof:
        key = (origin["source_id"], origin["raw_path"], origin["sha256"])
        require(key not in origins, f"Duplicate provenance: {key}")
        origins[key] = origin
    bullet_ids = contract.get("unnumbered_record_ids", [])
    require(len(bullet_ids) == len(set(bullet_ids)), "Duplicate unnumbered record IDs")
    selected_bullets = set(bullet_ids)
    files, sections, records, sources = [], [], {}, {}
    seen_origins, seen_bullets = set(), set()
    numbered_outside_sources = 0
    paths = sorted((base / "01-data/raw").glob("batch-*.md"))
    require({p.relative_to(base).as_posix() for p in paths} == set(contract["raw_sha256"]),
            "Raw file set differs from corpus contract")
    for path in paths:
        raw = path.read_bytes()
        relative = path.relative_to(base).as_posix()
        require(sha(raw) == contract["raw_sha256"][relative], f"Raw hash mismatch: {relative}")
        files.append({"path": relative, "sha256": sha(raw), "bytes": len(raw)})
        lines = raw.decode("utf-8").splitlines(keepends=True)
        boundaries = [i for i, line in enumerate(lines) if BOUNDARY.match(line)]
        covered = set()
        for position, start in enumerate(boundaries):
            end = boundaries[position + 1] if position + 1 < len(boundaries) else len(lines)
            heading = lines[start].rstrip("\r\n")
            match, extension = SOURCE.match(heading), EXTENSION.match(heading)
            if not (match or extension):
                continue
            sid = (match or extension)[1]
            data = "".join(lines[start:end])
            digest = sha(data.encode("utf-8"))
            key = (sid, relative, digest)
            require(key in origins, f"Missing preservation proof: {sid} {relative}")
            require(key not in seen_origins, f"Duplicate source section: {key}")
            seen_origins.add(key)
            origin = origins[key]
            require(origin["line_start"] == start + 1 and origin["line_end"] == end,
                    f"Stale provenance span: {sid} {relative}")
            require(origin["is_extension"] == bool(extension), f"Extension mismatch: {sid}")
            require(origin["original_line_start"] > 0 and
                    origin["original_line_end"] - origin["original_line_start"] == end - start - 1,
                    f"Invalid original span: {sid}")
            section_id = f"{sid}:{path.stem}:{origin['original_line_start']}"
            section = {"section_id": section_id, "source_id": sid, "raw_path": relative,
                       "line_start": start + 1, "line_end": end,
                       "original_line_start": origin["original_line_start"],
                       "original_line_end": origin["original_line_end"],
                       "source_section_sha256": digest, "is_extension": bool(extension)}
            sections.append(section)
            covered.update(range(start, end))
            if match:
                require(sid not in sources, f"Duplicate formal source ID: {sid}")
                sources[sid] = {"source_id": sid, "heading_raw": match[2]}
            for line_index in range(start, end):
                line = lines[line_index]
                number = NUMBERED.match(line)
                original_line = origin["original_line_start"] + line_index - start
                record_id = f"{sid}:{path.stem}:L{original_line:05d}"
                bullet = record_id in selected_bullets
                if bullet:
                    require(line.startswith("- "), f"Declared bullet is not a bullet: {record_id}")
                    seen_bullets.add(record_id)
                if not (number or bullet):
                    continue
                stop = line_index + 1
                while stop < end and (not lines[stop].strip() or lines[stop].startswith((" ", "\t"))):
                    stop += 1
                require(record_id not in records, f"Duplicate record ID: {record_id}")
                records[record_id] = {
                    "occurrence_id": record_id, "source_id": sid, "section_id": section_id,
                    "raw_path": relative, "line_start": line_index + 1, "line_end": stop,
                    "original_line_start": original_line,
                    "original_line_end": original_line + stop - line_index - 1,
                    "original_list_marker": number[1] if number else "-",
                    "original_text": number[2] if number else line[2:].rstrip("\r\n"),
                    "raw_text": "".join(lines[line_index:stop]),
                    "source_section_sha256": digest,
                }
        numbered_outside_sources += sum(bool(NUMBERED.match(line)) for i, line in enumerate(lines) if i not in covered)
    require(seen_origins == set(origins), "Unused source provenance entries")
    require(seen_bullets == selected_bullets, "Unresolved declared unnumbered record IDs")
    require(sorted(sources) == contract["source_ids"], "Source IDs differ from corpus contract")
    require({s["section_id"]: s["source_section_sha256"] for s in sections} == contract["source_section_sha256"],
            "Source section hashes differ from corpus contract")
    for section in sections:
        require(section["source_id"] in sources, f"Orphan extension: {section['section_id']}")
    for sid, source in sources.items():
        source["raw_sections"] = [s for s in sections if s["source_id"] == sid]
        source["record_count"] = sum(r["source_id"] == sid for r in records.values())
        urls = []
        for section in source["raw_sections"]:
            lines = local_path(base, section["raw_path"]).read_text(encoding="utf-8").splitlines(keepends=True)
            text = "".join(lines[section["line_start"] - 1:section["line_end"]])
            urls.extend(u.rstrip("。；，,.") for u in URL.findall(text))
        source["urls"] = list(dict.fromkeys(urls))
        require(source["urls"], f"No source URL: {sid}")
        for url in source["urls"]:
            require(bool(urlsplit(url).hostname), f"Invalid source URL: {sid} {url}")
    index = {"schema_version": 2, "scope": "Structural source index; record counts are not question counts or review coverage.",
             "sources": [sources[sid] for sid in sorted(sources)]}
    manifest = {"schema_version": 1, "files": files}
    summary = {"source_count": len(sources), "batch_count": len(files), "source_section_count": len(sections),
               "structural_record_count": len(records), "numbered_record_count": len(records) - len(seen_bullets),
               "declared_unnumbered_record_count": len(seen_bullets),
               "numbered_items_outside_source_sections": numbered_outside_sources}
    return index, manifest, records, summary


def verify_reference(record_id, reference, records):
    require(record_id in records, f"Unknown review record: {record_id}")
    record = records[record_id]
    for field in ("source_id", "raw_path", "line_start", "source_section_sha256"):
        require(reference.get(field) == record[field], f"Review reference mismatch: {record_id} {field}")
    quote = reference.get("quote")
    require(isinstance(quote, str) and bool(quote.strip()) and quote in record["raw_text"],
            f"Review quote is not verbatim: {record_id}")


def verify_reviews(base, records):
    prior = load(base / "02-analysis/prior-reviewed-assertions.json")
    require(prior["status"] == "limited_existing_assertions", "Prior assertions must retain limited status")
    require(sha(dumps(prior["original_document"]).encode("utf-8")) == prior["origin"]["sha256"],
            "Original reviewed assertions changed")
    decisions = prior["original_document"]["decisions"]
    require(set(decisions) == set(prior["references"]), "Prior assertion references differ")
    for record_id, reference in prior["references"].items():
        verify_reference(record_id, reference, records)
    path = base / "02-analysis/model-review.json"
    review = load(path) if path.exists() else {"schema_version": 1, "status": "pending", "reviews": []}
    require(set(review) == {"schema_version", "status", "reviews"} and review["schema_version"] == 1,
            "Invalid model-review document")
    require(review["status"] in {"pending", "partial", "complete"} and isinstance(review["reviews"], list),
            "Invalid model-review status or rows")
    seen, completed = set(), set()
    label_records, label_sources = Counter(), defaultdict(set)
    for row in review["reviews"]:
        require(set(row) == {"occurrence_id", "reference", "status", "label", "reason", "model", "reviewed_at"},
                "Invalid model-review row fields")
        record_id = row["occurrence_id"]
        require(record_id not in seen, f"Duplicate review: {record_id}")
        seen.add(record_id)
        verify_reference(record_id, row["reference"], records)
        require(set(row["reference"]) == {"source_id", "raw_path", "line_start", "source_section_sha256", "quote"},
                f"Invalid review reference fields: {record_id}")
        require(row["status"] in {"reviewed", "needs_review"}, f"Invalid row status: {record_id}")
        require(all(isinstance(row[k], str) and row[k].strip() for k in ("reason", "model", "reviewed_at")),
                f"Missing model review provenance: {record_id}")
        stamp = datetime.fromisoformat(row["reviewed_at"].replace("Z", "+00:00"))
        require(stamp.tzinfo is not None, f"Review time needs timezone: {record_id}")
        if row["status"] == "reviewed":
            require(isinstance(row["label"], str) and bool(row["label"].strip()), f"Missing explicit label: {record_id}")
            completed.add(record_id)
            label_records[row["label"]] += 1
            label_sources[row["label"]].add(records[record_id]["source_id"])
        else:
            require(row["label"] is None, f"Unfinished review cannot contribute a label: {record_id}")
    expected_status = "complete" if records and completed == set(records) else "partial" if seen else "pending"
    require(review["status"] == expected_status, f"Review status must be {expected_status}")
    return {"prior_assertion_count": len(decisions), "model_review_status": review["status"],
            "model_reviewed_record_count": len(completed), "records_without_completed_model_review": len(records) - len(completed),
            "explicit_reviewed_labels": {label: {"record_count": label_records[label],
                "source_ids": sorted(label_sources[label]), "source_count": len(label_sources[label])}
                for label in sorted(label_records)}}


def verify_readme_links(base):
    for path in base.rglob("README.md"):
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            require((path.parent / unquote(parsed.path)).exists(), f"Broken local link: {path.relative_to(base)} -> {target}")


def verify(base=BUSINESS, write_index=False):
    index, manifest, records, summary = parse_corpus(base)
    summary.update(verify_reviews(base, records))
    verify_readme_links(base)
    outputs = {"01-data/sources.json": index, "01-data/raw-manifest.json": manifest}
    for relative, value in outputs.items():
        path, expected = base / relative, dumps(value)
        if write_index:
            path.write_text(expected, encoding="utf-8")
        else:
            require(path.exists() and path.read_bytes() == expected.encode("utf-8"), f"Stale structural index: {relative}")
    return summary, records


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Read-only verification (the default)")
    mode.add_argument("--write-index", action="store_true", help="Explicitly refresh only sources.json and raw-manifest.json")
    parser.add_argument("--record", help="Print one preserved structural record by stable occurrence ID")
    args = parser.parse_args(argv)
    try:
        summary, records = verify(write_index=args.write_index)
        if args.record:
            require(args.record in records, f"Unknown record: {args.record}")
        print(dumps(records[args.record] if args.record else summary), end="")
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
