"""Incremental automation state must never turn transport uncertainty into semantic decisions."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from jd.automation import canonical_url, job_identity, reconcile, triage


def write_result(root: Path, source_id: str, jobs: list[dict], *, complete=False, status="COLLECTED_UNREVIEWED"):
    target = root / source_id
    target.mkdir(parents=True, exist_ok=True)
    (target / "result.json").write_text(json.dumps({
        "source_id": source_id,
        "company": "测试公司",
        "status": status,
        "complete": complete,
        "jobs": jobs,
    }, ensure_ascii=False), encoding="utf-8")


def job(job_id: str, title="Agent开发工程师", description="开发Agent和RAG服务。"):
    return {
        "job_id": job_id,
        "title": title,
        "location": "北京",
        "description": description,
        "requirements": "Python，后端工程能力。",
        "official_url": f"https://jobs.example.com/position/{job_id}?utm_source=test",
    }


class AutomationTests(unittest.TestCase):
    def registry(self):
        return {"official-001": {"source_id": "official-001", "company": "测试公司", "portal": "https://jobs.example.com"}}

    def run_reconcile(self, directory: Path, scan: Path):
        state = directory / "scan-state.json"
        queue = directory / "review-queue.json"
        report = directory / "status.md"
        with patch("jd.automation.registry", side_effect=self.registry):
            summary = reconcile(input_dir=scan, state_file=state, queue_file=queue, report_file=report)
        return summary, json.loads(state.read_text()), json.loads(queue.read_text()), report.read_text()

    def test_first_observation_bootstraps_without_flooding_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); scan = root / "scan"
            write_result(scan, "official-001", [job("1"), job("2")], complete=True, status="OK")
            summary, state, queue, report = self.run_reconcile(root, scan)
            self.assertEqual(summary["pending"], 0)
            self.assertTrue(state["sources"]["official-001"]["baseline_ready"])
            self.assertEqual(len(state["sources"]["official-001"]["jobs"]), 2)
            self.assertEqual(queue["entries"], {})
            self.assertIn("首次基线", report)

    def test_added_and_changed_are_queued_and_partial_scan_never_removes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first"; write_result(first, "official-001", [job("1"), job("2")], complete=True, status="OK")
            self.run_reconcile(root, first)
            second = root / "second"
            write_result(second, "official-001", [job("1", description="开发Agent、RAG和评测平台。"), job("3")], complete=False, status="PARTIAL")
            summary, state, queue, _ = self.run_reconcile(root, second)
            self.assertEqual(summary["counts"]["changed"], 1)
            self.assertEqual(summary["counts"]["added"], 1)
            self.assertNotIn("possibly_removed", summary["counts"])
            self.assertEqual(len(state["sources"]["official-001"]["jobs"]), 3)
            changes = {entry["change"] for entry in queue["entries"].values()}
            self.assertEqual(changes, {"added", "changed"})

    def test_only_complete_scan_can_queue_possible_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first"; write_result(first, "official-001", [job("1"), job("2")], complete=True, status="OK")
            self.run_reconcile(root, first)
            second = root / "second"; write_result(second, "official-001", [job("1")], complete=True, status="OK")
            summary, _, queue, _ = self.run_reconcile(root, second)
            self.assertEqual(summary["counts"]["possibly_removed"], 1)
            self.assertIn("possibly_removed", {entry["change"] for entry in queue["entries"].values()})

    def test_missing_artifact_preserves_existing_baseline_and_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first"; write_result(first, "official-001", [job("1")], complete=True, status="OK")
            self.run_reconcile(root, first)
            state_before = (root / "scan-state.json").read_text()
            empty = root / "empty"; empty.mkdir()
            summary, state, _, report = self.run_reconcile(root, empty)
            before = json.loads(state_before)["sources"]["official-001"]["jobs"]
            self.assertEqual(state["sources"]["official-001"]["jobs"], before)
            self.assertEqual(summary["counts"]["missing"], 1)
            self.assertIn("MISSING_ARTIFACT", report)

    def test_queue_is_cumulative_across_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first"; write_result(first, "official-001", [job("1")], complete=True, status="OK")
            self.run_reconcile(root, first)
            second = root / "second"; write_result(second, "official-001", [job("1"), job("2")], complete=True, status="OK")
            self.run_reconcile(root, second)
            third = root / "third"; write_result(third, "official-001", [job("1"), job("2"), job("3")], complete=True, status="OK")
            _, _, queue, _ = self.run_reconcile(root, third)
            self.assertEqual(len(queue["entries"]), 2)

    def test_tracking_parameters_do_not_change_identity(self):
        a = canonical_url("https://example.com/jobs/1?utm_source=a&x=1")
        b = canonical_url("https://example.com/jobs/1?x=1&utm_source=b")
        self.assertEqual(a, b)
        self.assertEqual(job_identity("official-001", job("1")), "id:1")

    def test_kuaishou_ats_namespaces_are_distinct(self):
        campus = {"job_id": "99", "official_url": "https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/99"}
        trainee = {"job_id": "99", "official_url": "https://zhaopin.kuaishou.cn/recruit/e/#/official/trainee/job-info/99"}
        self.assertEqual(job_identity("official-002", campus), "campus:99")
        self.assertEqual(job_identity("official-002", trainee), "trainee:99")

    def test_triage_is_priority_only_not_an_inclusion_decision(self):
        ranked = triage(job("1"))
        plain = triage(job("2", title="普通岗位", description="负责一般业务支持。"))
        self.assertEqual(ranked["priority"], "high")
        self.assertEqual(plain["priority"], "low")
        self.assertNotIn("decision", ranked)


if __name__ == "__main__":
    unittest.main()
