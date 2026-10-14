import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from jd.catalog import counts, load_catalog, validate_catalog
from jd.review import apply_decisions, compact_backlog, prepare_batch


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

    def test_prepare_batch_prioritizes_high_and_keeps_full_jd(self):
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
            self.assertEqual(q["entries"]["e1"]["review_state"], "reviewed")
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

    def test_needs_review_is_recorded_without_guessing(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            catalog, _ = self.base_catalog()
            queue = {"schema_version": 2, "entries": {"e1": self.queue_entry()}}
            decisions = {
                "schema_version": 1,
                "batch_id": "b3",
                "decisions": [{
                    "event_id": "e1",
                    "decision": "needs_review",
                    "decision_reason": "招聘类型证据不足",
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
            self.assertEqual(result["needs_review"], 1)
            q = json.loads((root / "queue.json").read_text())
            self.assertEqual(q["entries"]["e1"]["semantic_review"]["decision"], "needs_review")

    def test_compaction_reuses_exact_existing_review_and_ignores_unpublished_removal(self):
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
            exact = self.queue_entry(change="changed")
            removal = {
                "event_id": "gone",
                "source_id": "s1",
                "company": "公司",
                "identity": "id:not-published",
                "change": "possibly_removed",
                "first_seen_at_utc": "2026-10-14T00:00:00Z",
                "review_state": "pending",
                "triage": {"priority": "low"},
                "job": None,
                "previous": {"fingerprint": "x", "title": "未入库职位"},
            }
            queue = {"schema_version": 2, "entries": {"e1": exact, "gone": removal}}
            self.write_json(root / "official.json", catalog)
            self.write_json(root / "queue.json", queue)
            result = compact_backlog(queue_file=root / "queue.json", official_file=root / "official.json")
            self.assertEqual(result["already_reviewed"], 1)
            self.assertEqual(result["unpublished_removals"], 1)
            stored = json.loads((root / "queue.json").read_text())
            self.assertEqual(stored["entries"]["e1"]["review_state"], "reviewed")
            self.assertEqual(stored["entries"]["gone"]["review_state"], "ignored")

    def test_compaction_keeps_full_id_event_over_listing_fallback_for_same_position(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            catalog, _ = self.base_catalog()
            full = self.queue_entry()
            full["event_id"] = "full"
            full["job"]["job_id"] = "7683042369134479657"
            full["identity"] = "id:7683042369134479657"
            fallback = {
                **self.queue_entry(),
                "event_id": "fallback",
                "identity": "url:abc",
                "job": {
                    "title": "Agent工程实习\\n职责和要求被错误拼进标题",
                    "official_url": "https://example.com/campus/position/7683042369134479657/detail?spread=x",
                },
            }
            queue = {"schema_version": 2, "entries": {"full": full, "fallback": fallback}}
            self.write_json(root / "official.json", catalog)
            self.write_json(root / "queue.json", queue)
            result = compact_backlog(queue_file=root / "queue.json", official_file=root / "official.json")
            self.assertEqual(result["duplicate_fallbacks"], 1)
            stored = json.loads((root / "queue.json").read_text())
            self.assertEqual(stored["entries"]["full"]["review_state"], "pending")
            self.assertEqual(stored["entries"]["fallback"]["review_state"], "ignored")


if __name__ == "__main__":
    unittest.main()
