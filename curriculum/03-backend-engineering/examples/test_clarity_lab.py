"""运行方式同原实验测试；直接执行正文的小例子，并检查新增逻辑模型。"""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys
import unittest
from threading import Event

from backend_lab import BoundedExecutor

from clarity_lab import Revision, SourceUnavailable, VersionedReadModel, ring_owner, s256_challenge

ROOT = Path(__file__).resolve().parents[1]


class FutureProseTests(unittest.TestCase):
    def test_example_is_executed_from_prose(self) -> None:
        text = (ROOT / "docs/04-Concurrency与ThreadPool.md").read_text(encoding="utf-8")
        blocks = re.findall(
            r"<!-- runnable-example: future_exception -->\n```python\n(.*?)\n```\n<!-- /runnable-example -->",
            text, re.S,
        )
        self.assertEqual(len(blocks), 1)
        result = subprocess.run([sys.executable, "-c", blocks[0]],
                                capture_output=True, text=True, timeout=10, check=True)
        self.assertEqual(result.stdout, "观察到任务失败\n")
        self.assertEqual(result.stderr, "")


    def test_failed_work_releases_admission_after_callback(self) -> None:
        pool = BoundedExecutor(1, 1)
        settled = Event()
        try:
            future = pool.submit(lambda: 1 / 0)
            # 注册顺序保证先执行内部归还，再确认本测试可提交下一项。
            future.add_done_callback(lambda _: settled.set())
            with self.assertRaises(ZeroDivisionError):
                future.result(timeout=2)
            self.assertTrue(settled.wait(timeout=2))
            self.assertEqual(pool.submit(lambda: 7).result(timeout=2), 7)
        finally:
            pool.close()


class VersionedReadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = VersionedReadModel()
        self.v7 = Revision("team-a", "doc-42", 7)
        self.v8 = Revision("team-a", "doc-42", 8)
        self.store.publish(self.v7, "old")

    def test_normal_read_fills_exact_key(self) -> None:
        self.assertEqual(self.store.read_current("team-a", "doc-42"), (7, "old"))
        self.assertEqual(self.store.cache[self.v7], (self.v7, "old"))

    def test_old_refill_after_new_eviction_does_not_select_old(self) -> None:
        selected = self.store.select_revision("team-a", "doc-42")
        self.store.publish(self.v8, "new")
        self.store.read_selected(self.v8)
        self.store.cache.clear()
        self.store.fill(selected, self.v7, "old")
        self.assertEqual(self.store.read_current("team-a", "doc-42"), (8, "new"))

    def test_already_selected_old_read_can_finish_old(self) -> None:
        selected = self.store.select_revision("team-a", "doc-42")
        self.store.publish(self.v8, "new")
        self.assertEqual(self.store.read_selected(selected), (7, "old"))
        self.assertEqual(self.store.read_current("team-a", "doc-42"), (8, "new"))

    def test_head_unavailable_does_not_fall_back(self) -> None:
        self.store.read_current("team-a", "doc-42")
        self.store.head_available = False
        with self.assertRaises(SourceUnavailable):
            self.store.read_current("team-a", "doc-42")

    def test_cache_unavailable_reads_exact_authoritative_body(self) -> None:
        self.store.publish(self.v8, "new")
        self.store.cache_available = False
        self.assertEqual(self.store.read_current("team-a", "doc-42"), (8, "new"))
        self.assertEqual(self.store.cache, {})

    def test_unavailable_exact_body_does_not_return_v7(self) -> None:
        self.store.read_current("team-a", "doc-42")
        self.store.publish(self.v8, "new")
        self.store.body_available = False
        with self.assertRaises(SourceUnavailable):
            self.store.read_current("team-a", "doc-42")

    def test_missing_selected_body_fails_without_substitution(self) -> None:
        self.store.publish(self.v8, "new")
        del self.store.bodies[self.v8]  # 故意破坏正文可用前提
        with self.assertRaises(KeyError):
            self.store.read_current("team-a", "doc-42")

    def test_wrong_version_cannot_be_labeled_as_new(self) -> None:
        self.store.publish(self.v8, "new")
        with self.assertRaises(ValueError):
            self.store.fill(self.v8, self.v7, "old")

    def test_same_revision_content_cannot_be_replaced(self) -> None:
        self.store.fill(self.v7, self.v7, "old")
        with self.assertRaises(ValueError):
            self.store.fill(self.v7, self.v7, "changed")

    def test_deleted_head_denies_new_read_even_if_cache_remains(self) -> None:
        self.store.read_current("team-a", "doc-42")
        self.store.publish(self.v8, None)
        with self.assertRaises(KeyError):
            self.store.read_current("team-a", "doc-42")
        self.assertIn(self.v7, self.store.cache)

    def test_revision_cannot_restart_after_delete(self) -> None:
        self.store.publish(self.v8, None)
        with self.assertRaises(ValueError):
            self.store.publish(self.v7, "recreated")

    def test_tenants_use_distinct_content_keys(self) -> None:
        other = Revision("team-b", "doc-42", 7)
        self.store.publish(other, "other")
        self.assertEqual(self.store.read_current("team-b", "doc-42"), (7, "other"))
        self.assertEqual(self.store.read_current("team-a", "doc-42"), (7, "old"))
        # 只检查键隔离，不实现真实主体授权。


class MappingAndPkceTests(unittest.TestCase):
    def test_pkce_rfc7636_appendix_b_vector(self) -> None:
        verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
        challenge = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
        self.assertEqual(s256_challenge(verifier), challenge)
        self.assertNotEqual(s256_challenge("A" * 43), challenge)

    def test_pkce_rejects_invalid_verifier_format(self) -> None:
        for value in ("short", "A" * 129, "A" * 42 + " "):
            with self.subTest(value=value), self.assertRaises(ValueError):
                s256_challenge(value)

    def test_hash_ring_matches_prose_rows(self) -> None:
        before = {"A": 20, "B": 60, "C": 90}
        after = {**before, "D": 50}
        for position, old, new in ((10, "A", "A"), (40, "B", "D"),
                                   (70, "C", "C"), (95, "A", "A")):
            self.assertEqual((ring_owner(position, before), ring_owner(position, after)), (old, new))

    def test_only_claimed_ring_interval_changes(self) -> None:
        before = {"A": 20, "B": 60, "C": 90}
        after = {**before, "D": 50}
        changed = {p for p in range(100) if ring_owner(p, before) != ring_owner(p, after)}
        self.assertEqual(changed, set(range(21, 51)))

    def test_ring_rejects_undefined_inputs(self) -> None:
        for position, nodes in ((-1, {"A": 20}), (100, {"A": 20}),
                                (1, {}), (1, {"A": 20, "B": 20})):
            with self.subTest(position=position, nodes=nodes), self.assertRaises(ValueError):
                ring_owner(position, nodes)

    def test_fd_prose_arithmetic(self) -> None:
        text = (ROOT / "docs/18-LinuxTroubleshooting.md").read_text(encoding="utf-8")
        rows = re.findall(r"\| 10:\d\d:\d\d \| (\d+) \| (\d+) \|", text)
        self.assertEqual(rows, [("510", "420"), ("810", "720"), ("1016", "926")])
        self.assertEqual(round(int(rows[-1][0]) / 1024 * 100, 1), 99.2)
        self.assertLess(int(rows[-1][0]), 1024)


if __name__ == "__main__":
    unittest.main()
