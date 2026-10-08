"""Structural preservation and explicit-reference tests; no semantic tests."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import verify_interview_data as v


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index, cls.manifest, cls.records, cls.summary = v.parse_corpus()
        cls.contract = v.load(v.BUSINESS / "03-strategy/corpus-contract.json")

    def test_corpus_contract_and_unique_sources(self):
        ids = [source["source_id"] for source in self.index["sources"]]
        self.assertEqual(ids, self.contract["source_ids"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(self.summary["batch_count"], len(self.contract["raw_sha256"]))

    def test_all_raw_bytes_and_sections_preserved(self):
        for entry in self.manifest["files"]:
            raw = (v.BUSINESS / entry["path"]).read_bytes()
            self.assertEqual(len(raw), entry["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), self.contract["raw_sha256"][entry["path"]])
        sections = [section for source in self.index["sources"] for section in source["raw_sections"]]
        for section in sections:
            lines = (v.BUSINESS / section["raw_path"]).read_bytes().splitlines(keepends=True)
            raw = b"".join(lines[section["line_start"] - 1:section["line_end"]])
            self.assertEqual(v.sha(raw), self.contract["source_section_sha256"][section["section_id"]])
        self.assertEqual(len(sections), len(self.contract["source_section_sha256"]))

    def test_records_have_stable_ids_and_exact_original_slices(self):
        for rid, record in self.records.items():
            self.assertEqual(rid, f"{record['source_id']}:{Path(record['raw_path']).stem}:L{record['original_line_start']:05d}")
            lines = (v.BUSINESS / record["raw_path"]).read_bytes().splitlines(keepends=True)
            raw = b"".join(lines[record["line_start"] - 1:record["line_end"]])
            self.assertEqual(record["raw_text"].encode("utf-8"), raw)

    def test_all_numbered_and_declared_bullet_records_accounted_for(self):
        total = sum(bool(v.NUMBERED.match(line)) for path in (v.BUSINESS / "01-data/raw").glob("batch-*.md")
                    for line in path.read_text(encoding="utf-8").splitlines())
        self.assertEqual(total, self.summary["numbered_record_count"] + self.summary["numbered_items_outside_source_sections"])
        bullets = {rid for rid, record in self.records.items() if record["original_list_marker"] == "-"}
        self.assertEqual(bullets, set(self.contract.get("unnumbered_record_ids", [])))
        self.assertEqual(sum(source["record_count"] for source in self.index["sources"]), len(self.records))

    def test_extensions_refer_to_existing_sources(self):
        for source in self.index["sources"]:
            self.assertEqual(sum(not section["is_extension"] for section in source["raw_sections"]), 1)
            self.assertTrue(all(section["source_id"] == source["source_id"] for section in source["raw_sections"]))

    def test_existing_assertions_are_verbatim_and_referenced(self):
        prior = v.load(v.BUSINESS / "02-analysis/prior-reviewed-assertions.json")
        self.assertEqual(v.sha(v.dumps(prior["original_document"]).encode()), prior["origin"]["sha256"])
        self.assertEqual(set(prior["references"]), set(prior["original_document"]["decisions"]))
        for rid, reference in prior["references"].items():
            v.verify_reference(rid, reference, self.records)

    def test_default_check_writes_nothing(self):
        paths = [path for path in v.BUSINESS.rglob("*") if path.is_file() and "__pycache__" not in path.parts]
        before = {path: (path.stat().st_mtime_ns, v.sha(path.read_bytes())) for path in paths}
        v.verify()
        after = {path: (path.stat().st_mtime_ns, v.sha(path.read_bytes())) for path in paths}
        self.assertEqual(before, after)


class StructuralFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        for subdir in ("01-data/raw", "02-analysis", "03-strategy"):
            (self.base / subdir).mkdir(parents=True)
        self.blocks = [
            "## S900 Example A\n\n来源：https://example.com/a\n\n1. First item\n   Continuation remains verbatim.\n\n",
            "## S901 Example B\n\n来源：https://example.com/b\n\n1. (1–24) Original range remains one item\n\n- Original unnumbered item\n\n",
            "## Existing-process extension S900\n\n2. Extension item\n",
        ]
        self.write_corpus()
        original = {"schema_version": 1, "decisions": {}}
        self.write("02-analysis/prior-reviewed-assertions.json", {
            "status": "limited_existing_assertions", "origin": {"sha256": v.sha(v.dumps(original).encode())},
            "original_document": original, "references": {}})
        self.write_review([])

    def write(self, relative, value):
        (self.base / relative).write_text(v.dumps(value), encoding="utf-8")

    def write_corpus(self):
        raw_path = "01-data/raw/batch-90.md"
        text = "# Structural fixture\n\n" + "".join(self.blocks)
        (self.base / raw_path).write_text(text, encoding="utf-8")
        proof, section_hashes, bullet_ids = [], {}, []
        line = 3
        for block in self.blocks:
            heading = block.splitlines()[0]
            match = v.SOURCE.match(heading) or v.EXTENSION.match(heading)
            sid = match[1]
            count = len(block.splitlines())
            origin = line + 100
            digest = v.sha(block.encode())
            proof.append({"source_id": sid, "raw_path": raw_path, "is_extension": bool(v.EXTENSION.match(heading)),
                          "line_start": line, "line_end": line + count - 1,
                          "original_line_start": origin, "original_line_end": origin + count - 1, "sha256": digest})
            section_hashes[f"{sid}:batch-90:{origin}"] = digest
            bullet_ids.extend(f"{sid}:batch-90:L{origin + i:05d}" for i, item in enumerate(block.splitlines()) if item.startswith("- "))
            line += count
        ids = sorted(v.SOURCE.match(block.splitlines()[0])[1] for block in self.blocks if v.SOURCE.match(block.splitlines()[0]))
        self.write("01-data/source-provenance.json", {"sections": proof})
        self.write("03-strategy/corpus-contract.json", {"source_ids": ids, "raw_sha256": {raw_path: v.sha(text.encode())},
                   "source_section_sha256": section_hashes, "unnumbered_record_ids": bullet_ids})

    def write_review(self, rows, status=None):
        self.write("02-analysis/model-review.json", {"schema_version": 1, "status": status or ("partial" if rows else "pending"), "reviews": rows})

    def make_review(self, rid, records):
        record = records[rid]
        reference = {key: record[key] for key in ("source_id", "raw_path", "line_start", "source_section_sha256")}
        reference["quote"] = record["original_text"]
        return {"occurrence_id": rid, "reference": reference, "status": "reviewed", "label": "explicit-test-label",
                "reason": "Synthetic fixture assertion, never included in corpus.", "model": "test-fixture", "reviewed_at": "2026-10-08T00:00:00Z"}

    def test_append_source_needs_no_python_constant_change(self):
        _, _, original_records, before = v.parse_corpus(self.base)
        self.blocks.append("## S902 Example C\n\n来源：https://example.com/c\n\n1. New structural item\n")
        self.write_corpus()
        _, _, records, after = v.parse_corpus(self.base)
        self.assertEqual(after["source_count"], before["source_count"] + 1)
        self.assertEqual(after["structural_record_count"], before["structural_record_count"] + 1)
        self.assertTrue(set(original_records) <= set(records))
        self.assertEqual(after["source_section_count"], after["source_count"] + 1)

    def test_changed_raw_bytes_fail(self):
        with (self.base / "01-data/raw/batch-90.md").open("a") as stream:
            stream.write("Changed bytes\n")
        with self.assertRaisesRegex(ValueError, "Raw hash mismatch"):
            v.parse_corpus(self.base)

    def test_missing_or_extra_raw_file_fails(self):
        (self.base / "01-data/raw/batch-91.md").write_text("# Unexpected file\n")
        with self.assertRaisesRegex(ValueError, "Raw file set"):
            v.parse_corpus(self.base)

    def test_stale_provenance_span_fails(self):
        proof = v.load(self.base / "01-data/source-provenance.json")
        proof["sections"][0]["line_start"] += 1
        self.write("01-data/source-provenance.json", proof)
        with self.assertRaisesRegex(ValueError, "Stale provenance span"):
            v.parse_corpus(self.base)

    def test_duplicate_source_fails(self):
        self.blocks.append(self.blocks[0])
        self.write_corpus()
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            v.parse_corpus(self.base)

    def test_range_is_one_record_and_continuation_is_verbatim(self):
        _, _, records, summary = v.parse_corpus(self.base)
        self.assertEqual(summary["structural_record_count"], 4)
        self.assertEqual(summary["declared_unnumbered_record_count"], 1)
        first = next(iter(records.values()))
        self.assertEqual(first["raw_text"], "1. First item\n   Continuation remains verbatim.\n\n")

    def test_only_explicit_reviewed_labels_count(self):
        _, _, records, _ = v.parse_corpus(self.base)
        ids = list(records)
        rows = [self.make_review(rid, records) for rid in (ids[0], ids[-1])]
        unfinished = self.make_review(ids[1], records)
        unfinished.update(status="needs_review", label=None)
        self.write_review(rows + [unfinished])
        summary = v.verify_reviews(self.base, records)
        self.assertEqual(summary["model_reviewed_record_count"], 2)
        self.assertEqual(summary["explicit_reviewed_labels"]["explicit-test-label"],
                         {"record_count": 2, "source_ids": ["S900"], "source_count": 1})
        self.assertEqual(summary["records_without_completed_model_review"], len(records) - 2)

    def test_unknown_duplicate_or_altered_review_reference_fails(self):
        _, _, records, _ = v.parse_corpus(self.base)
        original = self.make_review(next(iter(records)), records)
        for field, value in (("occurrence_id", "unknown"), ("quote", "Invented quote"), ("line_start", -1), ("source_id", "S000")):
            row = copy.deepcopy(original)
            (row if field == "occurrence_id" else row["reference"])[field] = value
            self.write_review([row])
            with self.subTest(field=field), self.assertRaises(ValueError):
                v.verify_reviews(self.base, records)
        self.write_review([original, original])
        with self.assertRaisesRegex(ValueError, "Duplicate review"):
            v.verify_reviews(self.base, records)

    def test_unreviewed_label_and_false_completion_fail(self):
        _, _, records, _ = v.parse_corpus(self.base)
        row = self.make_review(next(iter(records)), records)
        row["status"] = "needs_review"
        self.write_review([row])
        with self.assertRaisesRegex(ValueError, "Unfinished review"):
            v.verify_reviews(self.base, records)
        self.write_review([], status="complete")
        with self.assertRaisesRegex(ValueError, "status must be pending"):
            v.verify_reviews(self.base, records)

    def test_absent_optional_review_file_is_pending(self):
        (self.base / "02-analysis/model-review.json").unlink()
        _, _, records, _ = v.parse_corpus(self.base)
        summary = v.verify_reviews(self.base, records)
        self.assertEqual(summary["model_review_status"], "pending")
        self.assertEqual(summary["explicit_reviewed_labels"], {})

    def test_stale_index_and_broken_local_link_fail(self):
        v.verify(self.base, write_index=True)
        (self.base / "01-data/sources.json").write_text("{}\n")
        with self.assertRaisesRegex(ValueError, "Stale structural index"):
            v.verify(self.base)
        v.verify(self.base, write_index=True)
        (self.base / "README.md").write_text("[missing](missing.md)\n")
        with self.assertRaisesRegex(ValueError, "Broken local link"):
            v.verify(self.base)


if __name__ == "__main__":
    unittest.main()
