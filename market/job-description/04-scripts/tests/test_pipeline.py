"""Offline regression contracts for preserved evidence and failure-safe state."""
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from jd import paths, render, publication
from jd.model import Job, SourceResult
from jd.matching import RoleMatcher
from jd.collection import Collector
from jd.normalize import normalize, family_title
from jd.state import update_state
from jd.freshness import cache_is_fresh
from jd.evidence import preserve_observation
from jd.pipeline import read_required
from jd.adapters import official

CFG = {"cycle": "test", "agent_keywords": ["agent"], "engineering_title_signals": ["工程师"],
       "hard_exclude_title_keywords": ["算法"], "sources": []}
SRC = {"company": "Company", "mode": "portal_only", "portal": "https://example.test/jobs",
       "current_campus_board": True, "official_root": "https://example.test", "search_url": "https://example.test/jobs"}
CFG["sources"] = [SRC]


def job(**kwargs):
    data = dict(company="Company", title="Agent工程师", job_id="a1", location="上海 / 北京",
                category="校招", department="研发", description="完整职责\n多行正文", requirements="要求全文",
                official_url="https://example.test/job/a1", official_api="https://example.test/api", cycle_evidence="2027校招")
    return Job(**(data | kwargs))


def result(status, matched=0):
    return SourceResult("Company", "test", SRC["portal"], status, matched, matched)


class MatchingTests(unittest.TestCase):
    def test_target_engineering_retained(self):
        self.assertEqual(len(RoleMatcher(CFG).target_matches([job()], SRC)), 1)

    def test_generic_or_algorithm_or_internship_not_promoted(self):
        for title in ("后端工程师", "Agent算法工程师", "Agent工程师实习"):
            self.assertEqual(RoleMatcher(CFG).target_matches([job(title=title)], SRC), [])

    def test_mixed_official_board_needs_graduate_evidence(self):
        j = job(category="", cycle_evidence="", description="build agents", requirements="")
        self.assertEqual(RoleMatcher(CFG).target_matches([j], {**SRC, "current_campus_board": False}), [])


class CollectionTests(unittest.TestCase):
    def collector(self, **kwargs):
        return Collector(CFG, browser=kwargs.pop("browser", {}), feishu=kwargs.pop("feishu", {}),
                         moka=kwargs.pop("moka", {}), fetchers=kwargs.pop("fetchers", {}))

    def test_browser_status_without_full_pool_proof_is_blocked(self):
        c = self.collector(browser={"Company": {"status": "BROWSER_ENUMERATED", "jobs": [asdict(job())]}})
        r, jobs = c.collect(SRC)
        self.assertEqual(r.status, "BLOCKED")
        self.assertEqual(len(jobs), 1)  # observation is still retained

    def test_explicit_empty_complete_pool_is_zero(self):
        c = self.collector(browser={"Company": {"status": "BROWSER_ENUMERATED_ZERO", "list_scan_complete": True, "jobs": []}})
        self.assertEqual(c.collect(SRC)[0].status, "ENUMERATED_ZERO_MATCHES")

    def test_ats_ok_alone_is_not_completeness(self):
        c = self.collector(feishu={"Company": {"status": "OK", "jobs": []}})
        self.assertEqual(c.collect(SRC)[0].status, "BLOCKED")

    def test_ats_complete_zero_is_accepted(self):
        c = self.collector(moka={"Company": {"status": "OK", "complete": True, "jobs": []}})
        self.assertEqual(c.collect(SRC)[0].status, "ENUMERATED_ZERO_MATCHES")

    def test_api_failure_never_becomes_zero(self):
        def fail(src):
            raise RuntimeError("fixture unavailable")
        c = self.collector(fetchers={"fixture": fail})
        with patch("jd.collection.discover_api_candidates", return_value=[]):
            self.assertEqual(c.collect({**SRC, "mode": "fixture"})[0].status, "BLOCKED")


class EvidenceTests(unittest.TestCase):
    def test_family_keeps_each_requisition_body_and_all_fields(self):
        jobs = [job(), job(job_id="a2", description="另一份完整职责" * 3000, requirements="独立要求")]
        families, _ = normalize(jobs, {}, {}, [result("ENUMERATED_WITH_MATCHES", 2)])
        self.assertEqual(len(families), 1)
        self.assertEqual(families[0]["requisitions"], [asdict(j) for j in jobs])
        self.assertEqual(families[0]["locations"], ["上海", "北京"])

    def test_family_title_uses_real_whitespace(self):
        self.assertEqual(family_title("Agent工程师   - 上海"), "Agent工程师")

    def test_blocked_run_preserves_old_family_metadata(self):
        old = {"company": "Company", "role_family": "Historical", "description": "body", "verified_on": "2020-01-01", "custom": [1]}
        families, _ = normalize([], {}, {"role_families": [old]}, [result("BLOCKED")])
        self.assertEqual({k: families[0][k] for k in old}, old)
        self.assertEqual(families[0]["carry_reason"], "BLOCKED")

    def test_blocked_run_preserves_verified_state_and_timestamp(self):
        index = {"companies": [{"company": "Company", "status": "VERIFIED_ROLE", "last_verified": "2020-01-01", "representative_roles": [{"title": "Historical", "jd_summary": "body"}]}]}
        updated, _ = update_state(CFG, deepcopy(index), [], set(), [result("BLOCKED", 2)])
        self.assertEqual(updated["companies"][0]["representative_roles"], index["companies"][0]["representative_roles"])
        self.assertEqual(updated["companies"][0]["last_verified"], "2020-01-01")

    def test_complete_zero_updates_state(self):
        index = {"companies": [{"company": "Company", "status": "VERIFIED_ROLE", "representative_roles": [{"title": "Old"}]}]}
        updated, _ = update_state(CFG, index, [], set(), [result("ENUMERATED_ZERO_MATCHES")])
        self.assertEqual(updated["companies"][0]["status"], "ZERO_TARGET_JDS")
        self.assertEqual(updated["companies"][0]["representative_roles"], [])

    def test_observation_is_byte_exact_content_addressed_and_idempotent(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "source.json"
            body = b'{"full": "body", "timestamp": null}\n'
            p.write_bytes(body)
            target = preserve_observation(p, Path(d) / "observations")
            self.assertEqual(target.read_bytes(), body)
            self.assertEqual(preserve_observation(p, Path(d) / "observations"), target)
            p.write_bytes(b'{"new": true}\n')
            self.assertNotEqual(preserve_observation(p, Path(d) / "observations"), target)
            self.assertEqual(target.read_bytes(), body)

    def test_manual_seed_cannot_hide_old_full_body_after_a_blocked_run(self):
        old = {"company": "Company", "role_family": "Agent工程师", "description": "已保存完整正文", "requirements": "要求", "detail_status": "FULL_JD"}
        seed = {"company": "Company", "title": "Agent工程师", "official_url": SRC["portal"], "verified_on": "2020-01-01"}
        families, _ = normalize([], {"roles": [seed]}, {"role_families": [old]}, [result("BLOCKED")])
        self.assertEqual(families[0]["description"], old["description"])
        self.assertEqual(families[0]["manual_seed_evidence"]["verified_on"], "2020-01-01")

    def test_manual_seed_does_not_claim_a_new_verification_date(self):
        seed = {"company": "Company", "title": "Agent工程师", "official_url": SRC["portal"], "verified_on": "2020-01-01"}
        families, seeded = normalize([], {"roles": [seed]}, {}, [result("BLOCKED")])
        index, _ = update_state(CFG, {"companies": []}, families, seeded, [result("BLOCKED")])
        self.assertEqual(index["companies"][0]["last_verified"], "2020-01-01")

    def test_render_writes_all_outputs_in_isolated_fixture(self):
        with tempfile.TemporaryDirectory() as d:
            from contextlib import ExitStack
            with ExitStack() as stack:
                for name in ("OUT_JSON", "OUT_MD", "VERIFIED_INDEX", "VERIFIED_INDEX_MD", "SCAN_POOL_MD"):
                    stack.enter_context(patch.object(render, name, Path(d) / name))
                jobs = [job()]
                results = [result("ENUMERATED_WITH_MATCHES", 1)]
                families, seeds = normalize(jobs, {}, {}, results)
                index, families = update_state(CFG, {"companies": []}, families, seeds, results)
                payload = render.render(CFG, index, families, jobs, results, "test-time", "test-sha")
                self.assertEqual(payload["counts"]["full_jd_families"], 1)
                self.assertEqual(payload["role_families"][0]["requisitions"][0], asdict(jobs[0]))
                self.assertIn("完整职责", (Path(d) / "OUT_MD").read_text())

    def test_corrupt_state_fails_instead_of_replacing_it(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.json"
            p.write_text("{bad")
            with self.assertRaises(json.JSONDecodeError):
                read_required(p)

    def test_render_keeps_long_bodies(self):
        self.assertEqual(render.clean("完整正文\n" * 4000, 10), ("完整正文\n" * 4000).strip())


class FreshnessTests(unittest.TestCase):
    def test_date_and_provenance_are_both_required(self):
        now = datetime.now(timezone.utc)
        p = {"generated_at": now.isoformat(), "source_commit": "sha", "run_id": "run", "run_attempt": "1"}
        with patch.dict("os.environ", {"SYNC_SOURCE_SHA": "sha", "GITHUB_RUN_ID": "run", "GITHUB_RUN_ATTEMPT": "1"}):
            self.assertTrue(cache_is_fresh(p))
            self.assertFalse(cache_is_fresh({**p, "source_commit": "old"}))
            self.assertFalse(cache_is_fresh({**p, "run_id": "old"}))
            self.assertFalse(cache_is_fresh({**p, "generated_at": (now-timedelta(hours=7)).isoformat()}))
            self.assertFalse(cache_is_fresh({**p, "generated_at": (now+timedelta(minutes=10)).isoformat()}))
            self.assertFalse(cache_is_fresh({}))

    def test_stale_node_accelerator_cannot_be_reused(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "cache.json"
            p.write_text(json.dumps({"jobs": [], "complete": True, "total": 0}))
            with patch.object(official, "XIAOMI_NODE_CACHE", p):
                with self.assertRaisesRegex(RuntimeError, "stale or incomplete"):
                    official.fetch_xiaomi(SRC)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        (root / "generated.txt").write_text("fixture")
        for name, value in (("ROOT", root), ("OUTPUT_PATHS", ["generated.txt"])):
            patcher = patch.object(publication, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_publication_denied_outside_main_actions(self):
        with patch.dict("os.environ", {"GITHUB_ACTIONS": "", "GITHUB_REF": "refs/heads/main"}):
            with self.assertRaisesRegex(RuntimeError, "authorized main-branch"):
                publication.main()

    def test_all_business_inputs_and_outputs_invalidate_inflight_run(self):
        with patch.object(publication, "git") as git:
            git.return_value.stdout = "changed\n"
            self.assertTrue(publication.relevant_inputs_changed("old", "new"))
            self.assertEqual(git.call_args.args[:4], ("diff", "--name-only", "old..new", "--"))
            self.assertIn(publication.PREFIX, git.call_args.args)

    def test_stale_run_does_not_reset_commit_or_push(self):
        def fake_git(*args, **kwargs):
            from types import SimpleNamespace
            out = "source" if args == ("rev-parse", "HEAD") else "remote" if args == ("rev-parse", "origin/main") else "changed" if args[0] == "diff" else ""
            return SimpleNamespace(stdout=out, returncode=0)
        env = {"GITHUB_ACTIONS": "true", "GITHUB_REF": "refs/heads/main", "SYNC_SOURCE_SHA": "source"}
        with patch.dict("os.environ", env), patch.object(publication, "git", side_effect=fake_git) as git:
            self.assertEqual(publication.main(), 0)
            self.assertFalse(any(c.args[0] in {"reset", "commit", "push"} for c in git.call_args_list))

    def test_publish_rebases_unrelated_changes_and_retries_push(self):
        from types import SimpleNamespace
        remotes = iter(["source", "advance", "advance"])
        pushes = iter([1, 0])
        def fake_git(*args, **kwargs):
            out, code = "", 0
            if args == ("rev-parse", "HEAD"):
                out = "source"
            elif args == ("rev-parse", "origin/main"):
                out = next(remotes)
            elif args == ("rev-parse", "HEAD^"):
                out = "source"
            elif args[0] == "status":
                out = " M generated"
            elif args[0] == "push":
                code = next(pushes)
            return SimpleNamespace(stdout=out, returncode=code)
        env = {"GITHUB_ACTIONS": "true", "GITHUB_REF": "refs/heads/main", "SYNC_SOURCE_SHA": "source"}
        with patch.dict("os.environ", env), patch.object(publication, "git", side_effect=fake_git) as git:
            self.assertEqual(publication.main(), 0)
            self.assertTrue(any(c.args[0] == "rebase" for c in git.call_args_list))
            self.assertEqual(sum(c.args[0] == "push" for c in git.call_args_list), 2)
            self.assertFalse(any("--force" in c.args for c in git.call_args_list))

    def test_relevant_race_discards_commit_without_pushing(self):
        from types import SimpleNamespace
        remotes = iter(["source", "changed"])
        def fake_git(*args, **kwargs):
            out = ""
            if args == ("rev-parse", "HEAD") or args == ("rev-parse", "HEAD^"):
                out = "source"
            elif args == ("rev-parse", "origin/main"):
                out = next(remotes)
            elif args[0] in {"status", "diff"}:
                out = "changed"
            return SimpleNamespace(stdout=out, returncode=0)
        env = {"GITHUB_ACTIONS": "true", "GITHUB_REF": "refs/heads/main", "SYNC_SOURCE_SHA": "source"}
        with patch.dict("os.environ", env), patch.object(publication, "git", side_effect=fake_git) as git:
            self.assertEqual(publication.main(), 0)
            self.assertFalse(any(c.args[0] == "push" for c in git.call_args_list))


class AdapterCompletenessTests(unittest.TestCase):
    def test_midea_short_page_below_total_fails(self):
        from types import SimpleNamespace
        from unittest.mock import Mock
        response = Mock()
        response.json.return_value = {"total": 30, "jobs": [{"positionId": "1", "positionName": "Agent工程师"}]}
        session = Mock()
        session.headers = {}
        session.post.return_value = response
        with patch.object(official, "requests", SimpleNamespace(Session=lambda: session)):
            with self.assertRaisesRegex(RuntimeError, "incomplete"):
                official.fetch_midea_campus_api({**SRC, "midea_project_rule_id": "fixture"})

    def test_midea_empty_second_page_cannot_erase_initial_total(self):
        from types import SimpleNamespace
        from unittest.mock import Mock
        first, second = Mock(), Mock()
        first.json.return_value = {"total": 30, "jobs": [{"positionId": str(i), "positionName": "Agent工程师"} for i in range(20)]}
        second.json.return_value = {}
        session = Mock()
        session.headers = {}
        session.post.side_effect = [first, second]
        with patch.object(official, "requests", SimpleNamespace(Session=lambda: session)):
            with self.assertRaisesRegex(RuntimeError, "unique=20, advertised=30"):
                official.fetch_midea_campus_api({**SRC, "midea_project_rule_id": "fixture"})


class SavedContractTests(unittest.TestCase):
    def test_saved_json_is_readable_and_company_set_is_preserved(self):
        cfg = json.loads(paths.CONFIG.read_text())
        index = json.loads(paths.VERIFIED_INDEX.read_text())
        names = {x["company"] for x in cfg["sources"]}
        self.assertEqual(names, {x["company"] for x in index["companies"]})
        self.assertEqual(len(names), cfg["expected_company_count"])
        for path in paths.DATA.glob("*.json"):
            json.loads(path.read_text())

    def test_paths_are_within_business_and_independent_of_cwd(self):
        self.assertEqual(paths.CONFIG.parent, paths.STRATEGY)
        self.assertEqual(paths.OUT_JSON.parent, paths.DATA)
        self.assertTrue((paths.ROOT / ".github").exists())


if __name__ == "__main__":
    unittest.main()
