"""运行：python -m unittest discover -s examples -p 'test_*.py' -v（从模块目录）。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from pathlib import Path
from threading import Barrier, Event

from backend_lab import (
    BoundedExecutor, Conflict, FakeProvider, InjectedFailure, Overloaded, TokenBucket,
    claim_task, connection, create_task, finish_task, init_db, read_document,
    remaining_budget, save_document, table_count, unsafe_external_then_record,
)


class DatabaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="backend-test-")
        self.addCleanup(self.tmp.cleanup)
        self.db = Path(self.tmp.name) / "state.sqlite"
        init_db(self.db)

    def test_same_key_reuses_result_and_one_event(self) -> None:
        first = save_document(self.db, "team-a", "save-42", "doc-42", "v1")
        second = save_document(self.db, "team-a", "save-42", "doc-42", "v1")
        self.assertEqual(first, second)
        self.assertEqual(first["version"], 1)
        for table in ("documents", "operations", "outbox"):
            self.assertEqual(table_count(self.db, table), 1)

    def test_same_key_different_payload_conflicts(self) -> None:
        save_document(self.db, "team-a", "save-42", "doc-42", "v1")
        with self.assertRaises(Conflict):
            save_document(self.db, "team-a", "save-42", "doc-42", "different")
        self.assertEqual(read_document(self.db, "team-a", "doc-42"), (1, "v1"))

    def test_tenant_key_scope_is_independent(self) -> None:
        save_document(self.db, "team-a", "same-key", "doc-42", "A")
        save_document(self.db, "team-b", "same-key", "doc-42", "B")
        self.assertEqual(read_document(self.db, "team-a", "doc-42"), (1, "A"))
        self.assertEqual(read_document(self.db, "team-b", "doc-42"), (1, "B"))
        self.assertIsNone(read_document(self.db, "team-c", "doc-42"))

    def test_failure_before_commit_rolls_back_all_tables(self) -> None:
        with self.assertRaises(InjectedFailure):
            save_document(self.db, "team-a", "save-42", "doc-42", "v1", fail_before_commit=True)
        for table in ("documents", "operations", "outbox"):
            self.assertEqual(table_count(self.db, table), 0)
        self.assertEqual(save_document(self.db, "team-a", "save-42", "doc-42", "v1")["version"], 1)

    def test_new_key_is_new_business_operation(self) -> None:
        save_document(self.db, "team-a", "first", "doc-42", "v1")
        save_document(self.db, "team-a", "second", "doc-42", "v2")
        self.assertEqual(read_document(self.db, "team-a", "doc-42"), (2, "v2"))
        self.assertEqual(table_count(self.db, "operations"), 2)

    def test_simultaneous_clients_use_independent_connections(self) -> None:
        barrier = Barrier(6)
        def call(_: int) -> dict[str, object]:
            barrier.wait(timeout=5)
            return save_document(self.db, "team-a", "same", "doc-42", "content")
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(call, range(6)))
        self.assertTrue(all(x == results[0] for x in results))
        self.assertEqual(table_count(self.db, "operations"), 1)
        self.assertEqual(table_count(self.db, "outbox"), 1)

    def test_completed_process_exits_and_another_process_reads(self) -> None:
        script = (
            "import json,sys; from pathlib import Path; from backend_lab import save_document; "
            "print(json.dumps(save_document(Path(sys.argv[1]),'team-a','op','doc-42','saved')))"
        )
        result = subprocess.run([sys.executable, "-c", script, str(self.db)],
                                cwd=Path(__file__).parent, text=True, capture_output=True,
                                timeout=10, check=True)
        self.assertEqual(json.loads(result.stdout)["version"], 1)
        # 调用进程已经正常退出；并非断电/强杀或断盘测试。
        self.assertEqual(read_document(self.db, "team-a", "doc-42"), (1, "saved"))
        self.assertEqual(save_document(self.db, "team-a", "op", "doc-42", "saved")["version"], 1)

    def test_response_loss_model_retries_persisted_result(self) -> None:
        save_document(self.db, "team-a", "op", "doc-42", "saved")  # 主动丢弃返回值
        again = save_document(self.db, "team-a", "op", "doc-42", "saved")
        self.assertEqual(again["version"], 1)
        self.assertEqual(table_count(self.db, "outbox"), 1)

    def test_old_generation_cannot_overwrite_new_owner(self) -> None:
        create_task(self.db, "job-42")
        a = claim_task(self.db, "job-42", "A", 0, 10)
        self.assertIsNone(claim_task(self.db, "job-42", "B", 9, 10))
        b = claim_task(self.db, "job-42", "B", 11, 10)
        self.assertEqual((a, b), (1, 2))
        self.assertFalse(finish_task(self.db, "job-42", "A", a, 12, "old"))
        self.assertTrue(finish_task(self.db, "job-42", "B", b, 12, "new"))
        with connection(self.db) as con:
            self.assertEqual(con.execute("SELECT result FROM tasks").fetchone()[0], "new")

    def test_expired_owner_cannot_finish_even_without_reclaim(self) -> None:
        create_task(self.db, "job-42")
        a = claim_task(self.db, "job-42", "A", 0, 10)
        self.assertFalse(finish_task(self.db, "job-42", "A", a, 10, "late"))

    def test_terminal_task_cannot_be_reclaimed(self) -> None:
        create_task(self.db, "job-42")
        a = claim_task(self.db, "job-42", "A", 0, 10)
        self.assertTrue(finish_task(self.db, "job-42", "A", a, 5, "ok"))
        self.assertIsNone(claim_task(self.db, "job-42", "B", 50, 10))


class CapacityTests(unittest.TestCase):
    def test_running_timeout_does_not_release_admission_slot(self) -> None:
        started, release = Event(), Event()
        executor = BoundedExecutor(workers=1, capacity=1)
        def work() -> str:
            started.set()
            if not release.wait(timeout=5):
                raise RuntimeError("测试未释放工作者")
            return "done"
        try:
            future = executor.submit(work)
            self.assertTrue(started.wait(timeout=2))
            with self.assertRaises(TimeoutError):
                future.result(timeout=0.001)
            self.assertFalse(future.cancel())
            with self.assertRaises(Overloaded):
                executor.submit(lambda: "too early")
            release.set()
            self.assertEqual(future.result(timeout=2), "done")
        finally:
            release.set()
            executor.close()

    def test_pending_cancel_releases_slot(self) -> None:
        release, started = Event(), Event()
        executor = BoundedExecutor(workers=1, capacity=2)
        def work() -> None:
            started.set()
            if not release.wait(timeout=5):
                raise RuntimeError("测试未释放工作者")
        try:
            first = executor.submit(work)
            self.assertTrue(started.wait(timeout=2))
            pending = executor.submit(lambda: "not started")
            with self.assertRaises(Overloaded):
                executor.submit(lambda: "full")
            self.assertTrue(pending.cancel())
            replacement = executor.submit(lambda: "replacement")
            release.set()
            first.result(timeout=2)
            self.assertEqual(replacement.result(timeout=2), "replacement")
        finally:
            release.set()
            executor.close()

    def test_close_rejects_new_work(self) -> None:
        executor = BoundedExecutor(1, 1)
        executor.close()
        with self.assertRaises(RuntimeError):
            executor.submit(lambda: 1)

    def test_token_refill_and_burst(self) -> None:
        bucket = TokenBucket(capacity=4, rate=2, tokens=4, updated_at=0)
        self.assertTrue(bucket.take(0, 4))
        self.assertFalse(bucket.take(0.25, 1))
        self.assertTrue(bucket.take(0.5, 1))
        self.assertEqual(bucket.tokens, 0)
        self.assertTrue(bucket.take(100, 4))  # 再长空闲也最多累计 capacity
        self.assertFalse(bucket.take(100, 1))

    def test_invalid_bucket_clock_and_cost(self) -> None:
        bucket = TokenBucket(4, 2, 4, 1)
        for now, cost in [(0, 1), (float("nan"), 1), (1, -1), (1, float("inf"))]:
            with self.assertRaises(ValueError):
                bucket.take(now, cost)

    def test_remaining_budget_reserves_cleanup(self) -> None:
        self.assertAlmostEqual(remaining_budget(5, 3.2, 0.3), 1.5)
        self.assertEqual(remaining_budget(5, 5.1, 0.3), 0)
        with self.assertRaises(ValueError):
            remaining_budget(5, 1, -0.1)


class FailureModelTests(unittest.TestCase):
    def test_external_effect_is_not_rolled_back_by_local_exception(self) -> None:
        provider = FakeProvider()
        for _ in range(2):
            with self.assertRaises(InjectedFailure):
                unsafe_external_then_record(provider, "publish-doc-42")
        self.assertEqual(provider.actions, ["publish-doc-42", "publish-doc-42"])

    def test_cache_delete_still_allows_old_refill(self) -> None:
        # 显式的顺序模型，不是 Redis 服务测试。
        database = {"version": 1, "value": "old"}
        old_reader = dict(database)
        database = {"version": 2, "value": "new"}
        cache = None  # 写者成功删除缓存
        cache = old_reader  # 慢读者随后回填
        self.assertEqual(cache["version"], 1)
        self.assertEqual(database["version"], 2)

    def test_eviction_loses_cache_only_version_guard(self) -> None:
        cache = {"version": 2, "value": "new"}
        slow = {"version": 1, "value": "old"}
        self.assertLess(slow["version"], cache["version"])
        cache = None  # 删除版本信息，不再有可比较的高水位
        if cache is None or slow["version"] >= cache["version"]:
            cache = slow
        self.assertEqual(cache["version"], 1)


if __name__ == "__main__":
    unittest.main()
