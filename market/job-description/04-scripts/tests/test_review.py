import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from jd.catalog import counts, load_catalog, validate_catalog
from jd.review import apply_decisions, prepare_batch


class SemanticAuditBridgeTests(unittest.TestCase):
    def write_json(self, path, value):
        Path(path).write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def base_catalog(self, jobs=None):
        body = "职责：开发Agent服务。\n要求：在校生，Python。"
        existing = dict(
            req_id="r1",
            title="Agent工程实习",
            official_url="https://example.com/jobs/r1",
            full_text=body,
            decision_reason="明确包含Agent工程实现",
            official_type_evidence="在校生",
            checked_at_utc="2026-10-14T00:00:00Z",
            decision="include",
            review_depth="full_jd",
            recruitment_type="internship",
            official_recruitment_type="实习",
            locations=["北京"],
            body_sha256=hashlib.sha256(body.encode()).hexdigest(),
            engineering_evidence=["开发Agent服务"],
            role_track="应用与Agent核心研发",
        )
        catalog = dict(
            companies=[
                dict(
                    source_id="s1",
                    company="公司",
                    coverage={"coverage_level": "limited"},
                    jobs=list(jobs if jobs is not None else []),
                )
            ],
            snapshot={"checked_at_utc": "2026-10-14"},
        )
        catalog["counts"] = {
            "registered_sources": 1,
            "current_jobs": len(catalog["companies"][0]["jobs"]),
            "companies_with_current_jobs": int(bool(catalog["companies"][0]["jobs"])),
            "historical_observations": 0,
            "coverage": {"complete": 0, "limited": 1, "restricted": 0, "not_started": 0},
        }
        return catalog, existing

    def queue_entry(self, change="added"):
        job = {
            "job_id": "r1",
            "title": "Agent工程实习",
            "location": "北京",
            "description": "职责：开发Agent服务。",
            "requirements": "要求：在校生，Python。",
            "official_url": "https://example.com/jobs/r1",
        }
        return {
            "event_id": "e1",
            "source_id": "s1",
            "company": "公司",
            "identity": "id:r1",
            "change": change,
            "first_seen_at_utc": "2026-10-14T00:00:00Z",
            "review_state": "pending",
            "triage": {"priority": "high"},
            "job": job if change != "possibly_removed" else None,
            "previous": None,
        }

    def test_prepare_batch_keeps_full_jd(self):
        with tempfile.TemporaryDirectory() as d:
            queue = {
                "schema_version": 2,
                "entries": {
                    "low": {**self.queue_entry(), "event_id": "low", "triage": {"priority": "low"}},
                    "high": {**self.queue_entry(), "event_id": "high", "triage": {"priority": "high"}},
                },
            }
            q = Path(d) / "queue.json"
            b = Path(d) / "batch.json"
            self.write_json(q, queue)
            payload = prepare_batch(queue_file=q, batch_file=b, limit=1)
            self.assertEqual(payload["entries"][0]["event_id"], "high")
            self.assertIn("开发Agent服务", payload["entries"][0]["job"]["description"])
            self.assertEqual(payload["pending_total"], 2)

    def test_include_adds_valid_full_jd_record_and_marks_queue_reviewed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            catalog, _ = self.base_catalog()
            queue = {"schema_version": 2, "entries": {"e1": self.queue_entry()}}
            decisions = {
                "schema_version": 1,
                "batch_id": "b1",
                "decisions": [{
                    "event_id": "e1",
                    "decision": "include",
                    "decision_reason": "明确负责Agent服务开发",
                    "role_track": "应用与Agent核心研发",
                    "recruitment_type": "internship",
                    "official_type_evidence": "在校生",
                    "engineering_evidence": ["开发Agent服务"],
                }],
            }
            self.write_json(root / "official.json", catalog)
            self.write_json(root / "bytedance.json", {"source_id": "official-012", "jobs": []})
            self.write_json(root / "queue.json", queue)
            self.write_json(root / "decisions.json", decisions)
            result = apply_decisions(
                queue_file=root / "queue.json",
                decisions_file=root / "decisions.json",
                official_file=root / "official.json",
                bytedance_file=root / "bytedance.json",
                index_file=root / "index.md",
            )
            self.assertEqual(result["included"], 1)
            loaded = load_catalog(root / "official.json")
            self.assertEqual(validate_catalog(loaded, ["s1"]), [])
            self.assertEqual(loaded["companies"][0]["jobs"][0]["req_id"], "r1")
            q = json.loads((root / "queue.json").read_text())
            self.assertNotIn("e1", q["entries"])
            self.assertEqual(q["entries"]["e1"]["semantic_review"]["decision"], "include")
            self.assertIn("Agent工程实习", (root / "index.md").read_text())

    def test_exclude_changed_event_removes_previously_included_job(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            catalog, existing = self.base_catalog()
            exact_text = "职责：开发Agent服务。\n\n要求：在校生，Python。"
            existing["full_text"] = exact_text
            existing["body_sha256"] = hashlib.sha256(exact_text.encode()).hexdigest()
            existing["engineering_evidence"] = ["开发Agent服务"]
            catalog["companies"][0]["jobs"] = [existing]
            catalog["counts"]["current_jobs"] = 1
            catalog["counts"]["companies_with_current_jobs"] = 1
            queue = {"schema_version": 2, "entries": {"e1": self.queue_entry(change="changed")}}
            decisions = {
                "schema_version": 1,
                "batch_id": "b2",
                "decisions": [{
                    "event_id": "e1",
                    "decision": "exclude",
                    "decision_reason": "新JD已变为普通后端职责",
                }],
            }
            for name, value in (
                ("official.json", catalog),
                ("bytedance.json", {"source_id": "official-012", "jobs": []}),
                ("queue.json", queue),
                ("decisions.json", decisions),
            ):
                self.write_json(root / name, value)
            result = apply_decisions(
                queue_file=root / "queue.json",
                decisions_file=root / "decisions.json",
                official_file=root / "official.json",
                bytedance_file=root / "bytedance.json",
                index_file=root / "index.md",
            )
            self.assertEqual(result["excluded"], 1)
            self.assertEqual(load_catalog(root / "official.json")["companies"][0]["jobs"], [])

    def test_incomplete_new_observation_preserves_prior_full_jd(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            catalog, existing = self.base_catalog()
            catalog["companies"][0]["jobs"] = [existing]
            catalog["counts"]["current_jobs"] = 1
            catalog["counts"]["companies_with_current_jobs"] = 1
            event = self.queue_entry(change="added")
            event["job"] = {"job_id": "r1", "title": "Agent工程实习",
                            "official_url": "https://example.com/jobs/r1"}
            queue = {"schema_version": 2, "entries": {"e1": event}}
            decisions = {"schema_version": 1, "decisions": [{
                "event_id": "e1", "decision": "exclude",
                "decision_reason": "只抓到标题，不能覆盖此前正式审阅的完整JD",
                "evidence_gate": "缺少完整JD"}]}
            for name, value in (("official.json", catalog),
                                ("bytedance.json", {"source_id": "official-012", "jobs": []}),
                                ("queue.json", queue),
                                ("decisions.json", decisions)):
                self.write_json(root / name, value)
            stats = apply_decisions(queue_file=root / "queue.json",
                                    decisions_file=root / "decisions.json",
                                    official_file=root / "official.json",
                                    bytedance_file=root / "bytedance.json",
                                    index_file=root / "index.md")
            self.assertEqual(stats["excluded"], 1)
            saved = load_catalog(root / "official.json")
            self.assertEqual(len(saved["companies"][0]["jobs"]), 1)
            self.assertEqual(saved["companies"][0]["jobs"][0]["req_id"], "r1")
            self.assertNotIn("e1", json.loads((root / "queue.json").read_text())["entries"])

    def test_needs_review_is_rejected_as_new_decision(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            catalog, _ = self.base_catalog()
            queue = {"schema_version": 2, "entries": {"e1": self.queue_entry()}}
            decisions = {"schema_version": 1, "decisions": [{
                "event_id": "e1", "decision": "needs_review",
                "decision_reason": "资格证据缺失"}]}
            for name, value in (
                ("official.json", catalog),
                ("bytedance.json", {"source_id": "official-012", "jobs": []}),
                ("queue.json", queue),
                ("decisions.json", decisions),
            ):
                self.write_json(root / name, value)
            with self.assertRaisesRegex(ValueError, "Unsupported audit decision"):
                apply_decisions(queue_file=root / "queue.json",
                                decisions_file=root / "decisions.json",
                                official_file=root / "official.json",
                                bytedance_file=root / "bytedance.json",
                                index_file=root / "index.md")
            self.assertEqual(json.loads((root / "queue.json").read_text())["entries"]["e1"]["review_state"], "pending")

    def test_missing_jd_is_explicit_exclusion_not_a_new_queue_loop(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            catalog, _ = self.base_catalog()
            event = self.queue_entry()
            event["job"] = {"title": "北京"}
            queue = {"schema_version": 2, "entries": {"e1": event}}
            decisions = {"schema_version": 1, "decisions": [{
                "event_id": "e1", "decision": "exclude",
                "decision_reason": "只有城市筛选项，缺少具体职位和完整JD"}]}
            for name, value in (
                ("official.json", catalog),
                ("bytedance.json", {"source_id": "official-012", "jobs": []}),
                ("queue.json", queue),
                ("decisions.json", decisions),
            ):
                self.write_json(root / name, value)
            stats = apply_decisions(queue_file=root / "queue.json",
                                    decisions_file=root / "decisions.json",
                                    official_file=root / "official.json",
                                    bytedance_file=root / "bytedance.json",
                                    index_file=root / "index.md")
            self.assertEqual(stats["excluded"], 1)
            self.assertEqual(json.loads((root / "queue.json").read_text())["entries"]["e1"]["review_state"], "reviewed")
            batch = prepare_batch(queue_file=root / "queue.json",
                                  batch_file=root / "batch.json", limit=10)
            self.assertEqual(batch["pending_total"], 0)

    def test_one_decision_consumed_once(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            catalog, _ = self.base_catalog()
            for name, payload in (
                ("official.json", catalog),
                ("bytedance.json", {"source_id": "official-012", "jobs": []}),
                ("queue.json", {"schema_version": 2, "entries": {"e1": self.queue_entry()}}),
                ("decisions.json", {"schema_version": 1, "batch_id": "b1", "decisions": [{
                    "event_id": "e1", "decision": "exclude", "decision_reason": "不符合目标职责"
                }]}),
            ):
                self.write_json(root / name, payload)
            args = dict(queue_file=root / "queue.json", decisions_file=root / "decisions.json",
                        official_file=root / "official.json", bytedance_file=root / "bytedance.json",
                        index_file=root / "index.md")
            self.assertEqual(apply_decisions(**args)["excluded"], 1)
            self.assertEqual(apply_decisions(**args)["applied"], 0)
            self.assertEqual(prepare_batch(queue_file=root / "queue.json",
                                          batch_file=root / "batch.json", limit=24)["count"], 0)


if __name__ == "__main__":
    unittest.main()
