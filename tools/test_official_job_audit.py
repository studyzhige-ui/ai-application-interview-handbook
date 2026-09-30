"""Offline regression checks for official-job audit and market-summary syncing."""

from collections import Counter
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "official_job_audit", Path(__file__).with_name("audit_official_2027_job_sources.py")
)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class MarketSummaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.market = Path(self.temp.name) / "market.md"
        self.market_patch = patch.object(audit, "MARKET", self.market)
        self.market_patch.start()
        self.addCleanup(self.market_patch.stop)
        self.before = (
            "# Official jobs\n\n## 2. Scope\n\nKeep scope.\n\n"
            "## 3. Old snapshot\n\nOld counts.\n\n"
            "## 4. Old overview\n\nOld company table.\n\n"
            "## 5. Evidence\n\nKeep evidence.\n\n"
            "## 10. 维护日志\n\n- Keep history.\n"
        )
        self.market.write_text(self.before, encoding="utf-8")

    def sync(self):
        return audit.sync_market_summary(
            company_count=69,
            expected=69,
            ready_count=69,
            result_counts=Counter(HAS_TARGET_JDS=44, ZERO_TARGET_JDS=25),
            runtime_counts=Counter(ENUMERATED=68, LIST_REACHABLE=1),
            role_families=479,
            full_jd_families=469,
        )

    def test_numbered_maintenance_heading_updates_counts_and_keeps_evidence(self):
        self.assertTrue(self.sync())
        updated = self.market.read_text(encoding="utf-8")
        self.assertIn("长期扫描公司：69 家", updated)
        self.assertIn("HAS_TARGET_JDS 44 / ZERO_TARGET_JDS 25", updated)
        self.assertIn("ENUMERATED 68 / LIST_REACHABLE 1 / BLOCKED 0", updated)
        self.assertIn("严格 Role Family：479；第一方完整 JD：469", updated)
        self.assertTrue(updated.startswith(self.before.split("## 3.")[0]))
        self.assertIn(self.before[self.before.index("## 5."):], updated)
        self.assertNotIn("Old company table.", updated)

    def test_heading_number_and_horizontal_spacing(self):
        for heading in ("## 7. 维护日志", "## 12.维护日志", "##\t10.\t维护日志  "):
            with self.subTest(heading=heading):
                self.market.write_text(
                    self.before.replace("## 10. 维护日志", heading), encoding="utf-8"
                )
                self.assertTrue(self.sync())

    def test_sync_is_idempotent_and_does_not_duplicate_history(self):
        self.assertTrue(self.sync())
        first = self.market.read_bytes()
        self.assertFalse(self.sync())
        self.assertEqual(self.market.read_bytes(), first)
        self.assertEqual(first.decode("utf-8").count("快照一致性修复"), 1)

    def test_missing_maintenance_heading_fails_without_writing(self):
        before = self.before.replace("## 10. 维护日志", "## 10. Other history")
        self.market.write_text(before, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "maintenance-log section not found"):
            self.sync()
        self.assertEqual(self.market.read_text(encoding="utf-8"), before)

    def test_missing_snapshot_or_overview_fails_without_writing(self):
        for section in (3, 4):
            with self.subTest(section=section):
                before = self.before.replace(f"## {section}.", "## Missing.")
                self.market.write_text(before, encoding="utf-8")
                with self.assertRaises(RuntimeError):
                    self.sync()
                self.assertEqual(self.market.read_text(encoding="utf-8"), before)

    def test_repository_summary_can_be_synced_without_touching_the_original(self):
        original = audit.ROOT / "market/jobs/ai-agent-jd-market.md"
        before = original.read_bytes()
        self.market.write_bytes(before)
        self.sync()
        self.assertFalse(self.sync())
        self.assertEqual(original.read_bytes(), before)


class AuditGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.paths = {}
        for name in ("REG", "INDEX", "NORM", "BROWSER", "FEISHU", "MOKA", "OUT", "MARKET"):
            path = Path(self.temp.name) / name
            self.paths[name] = path
            patcher = patch.object(audit, name, path)
            patcher.start()
            self.addCleanup(patcher.stop)
        env = patch.dict("os.environ", {"SYNC_SOURCE_SHA": ""})
        env.start()
        self.addCleanup(env.stop)
        self.names = [f"Company {i}" for i in range(68)] + ["BOSS直聘/看准科技"]
        self.write("REG", {"expected_company_count": 69, "sources": [
            {"company": name, "official_root": "https://example.test/",
             "search_url": "https://example.test/jobs", "job_list_url": "https://example.test/jobs"}
            for name in self.names
        ]})
        self.write("INDEX", {"companies": [
            {"company": name, "status": "VERIFIED_ROLE"} for name in self.names
        ]})
        self.norm = {"sources": [
            {"company": name, "retrieval_status": "ENUMERATED_WITH_MATCHES", "role_family_count": 1}
            for name in self.names
        ], "counts": {"role_families": 69, "full_jd_families": 69}}
        self.write("NORM", self.norm)
        self.paths["MARKET"].write_text(
            "## 3. Snapshot\n\nold\n\n## 4. Overview\n\nold\n\n"
            "## 5. Evidence\n\nkeep\n\n## 10. 维护日志\n\n- History\n", encoding="utf-8"
        )

    def write(self, name, payload):
        self.paths[name].write_text(json.dumps(payload), encoding="utf-8")

    def run_audit(self):
        output = io.StringIO()
        with redirect_stdout(output):
            result = audit.main()
        return result, output.getvalue()

    def test_complete_enumeration_passes_all_69_companies(self):
        result, output = self.run_audit()
        self.assertEqual(result, 0, output)
        self.assertIn("runtime=69/69", output)
        self.assertIn("hard_errors=0", output)

    def test_reachable_only_company_still_fails_after_summary_fix(self):
        self.norm["sources"][-1]["retrieval_status"] = "LIST_REACHABLE"
        self.write("NORM", self.norm)
        self.write("BROWSER", {"generated_at": datetime.now(timezone.utc).isoformat(), "results": [
            {"company": self.names[-1], "pages": [{"url": "https://example.test/jobs"}]}
        ]})
        before_index = self.paths["INDEX"].read_bytes()
        result, output = self.run_audit()
        self.assertEqual(result, 1)
        self.assertIn("BOSS直聘/看准科技: runtime must be ENUMERATED, got LIST_REACHABLE", output)
        self.assertIn("market_changed=1 hard_errors=1", output)
        self.assertNotIn("summary sync failed", output)
        self.assertEqual(self.paths["INDEX"].read_bytes(), before_index)

    def test_stale_browser_cache_cannot_certify_current_enumeration(self):
        self.norm["sources"][-1]["retrieval_status"] = "BLOCKED"
        self.write("NORM", self.norm)
        self.write("BROWSER", {
            "generated_at": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "results": [{"company": self.names[-1], "status": "BROWSER_ENUMERATED", "full_keyword_search": True}],
        })
        result, output = self.run_audit()
        self.assertEqual(result, 1)
        self.assertIn("runtime must be ENUMERATED, got BLOCKED", output)

    def test_missing_company_cannot_pass(self):
        self.norm["sources"].pop()
        self.write("NORM", self.norm)
        result, output = self.run_audit()
        self.assertEqual(result, 1)
        self.assertIn("runtime=68/69", output)

    def test_source_commit_mismatch_cannot_pass(self):
        with patch.dict("os.environ", {"SYNC_SOURCE_SHA": "expected-commit"}):
            result, output = self.run_audit()
        self.assertEqual(result, 1)
        self.assertIn("generated source_commit mismatch", output)


if __name__ == "__main__":
    unittest.main()
