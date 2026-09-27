"""小型机制实验，不是任务平台、HTTP 服务、支付网关或分布式锁实现。

Python 3.13；SQLite 方言。每个调用建立并关闭自己的连接。
显式 BEGIN/COMMIT/ROLLBACK，避免依赖驱动隐式事务默认值。
"""
from __future__ import annotations

import json
import math
import sqlite3
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from threading import BoundedSemaphore, Lock
from typing import Callable, Iterator, TypeVar

T = TypeVar("T")


class Conflict(ValueError):
    """同一作用域操作键被用于不同参数。"""


class InjectedFailure(RuntimeError):
    """教学注入的本地异常，不模拟断电和磁盘硬件。"""


class Overloaded(RuntimeError):
    """拒绝超过在途上限的新提交。"""


# region bounded_executor
class BoundedExecutor:
    """workers 限制执行线程；capacity 限制已接收但尚未终结的任务总数。"""

    def __init__(self, workers: int, capacity: int) -> None:
        if workers < 1 or capacity < workers:
            raise ValueError("需要 capacity >= workers >= 1")
        self._pool = ThreadPoolExecutor(max_workers=workers)
        self._slots = BoundedSemaphore(capacity)
        self._lock = Lock()
        self._closed = False

    def submit(self, fn: Callable[..., T], *args: object) -> Future[T]:
        with self._lock:
            if self._closed:
                raise RuntimeError("executor 已关闭")
            if not self._slots.acquire(blocking=False):
                raise Overloaded("执行中与等待中的任务总数已到上限")
            try:
                future = self._pool.submit(fn, *args)
            except BaseException:
                self._slots.release()
                raise
            future.add_done_callback(lambda _future: self._slots.release())
            return future

    def close(self) -> None:
        with self._lock:
            self._closed = True
        self._pool.shutdown(wait=True, cancel_futures=True)
# endregion bounded_executor


@dataclass
class TokenBucket:
    """确定性单线程模型。调用者传入同一单调时间域，单位为秒。"""

    capacity: float
    rate: float
    tokens: float
    updated_at: float

    def __post_init__(self) -> None:
        values = (self.capacity, self.rate, self.tokens, self.updated_at)
        if not all(math.isfinite(x) for x in values):
            raise ValueError("参数必须有限")
        if self.capacity <= 0 or self.rate < 0 or not 0 <= self.tokens <= self.capacity:
            raise ValueError("令牌桶参数不合法")

    def take(self, now: float, cost: float = 1) -> bool:
        if not math.isfinite(now) or now < self.updated_at:
            raise ValueError("时钟不能倒退或非有限")
        if not math.isfinite(cost) or cost <= 0:
            raise ValueError("成本必须为有限正数")
        self.tokens = min(self.capacity, self.tokens + (now - self.updated_at) * self.rate)
        self.updated_at = now
        if cost > self.tokens:
            return False
        self.tokens -= cost
        return True


def remaining_budget(deadline: float, now: float, cleanup_reserve: float) -> float:
    """剩余可执行秒数；不跨机器发送本机 monotonic 值。"""
    if not all(math.isfinite(x) for x in (deadline, now, cleanup_reserve)):
        raise ValueError("时间必须有限")
    if cleanup_reserve < 0:
        raise ValueError("预留不能为负")
    return max(0.0, deadline - now - cleanup_reserve)


@contextmanager
def connection(path: Path) -> Iterator[sqlite3.Connection]:
    con = sqlite3.connect(path, autocommit=True, timeout=5.0)
    try:
        con.execute("PRAGMA foreign_keys=ON")
        con.execute("PRAGMA synchronous=FULL")
        yield con
    finally:
        con.close()


@contextmanager
def transaction(con: sqlite3.Connection) -> Iterator[None]:
    # SQLite 的写者串行化与 InnoDB 行锁不同，不用于证明 MySQL 并发性能。
    con.execute("BEGIN IMMEDIATE")
    try:
        yield
        con.execute("COMMIT")
    except BaseException:
        if con.in_transaction:
            con.execute("ROLLBACK")
        raise


SCHEMA = """
CREATE TABLE IF NOT EXISTS operations (
    tenant TEXT NOT NULL,
    op_key TEXT NOT NULL,
    fingerprint TEXT NOT NULL,
    result TEXT NOT NULL,
    PRIMARY KEY (tenant, op_key)
);
CREATE TABLE IF NOT EXISTS documents (
    tenant TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    version INTEGER NOT NULL CHECK (version >= 1),
    content TEXT NOT NULL,
    PRIMARY KEY (tenant, doc_id)
);
CREATE TABLE IF NOT EXISTS outbox (
    event_id TEXT PRIMARY KEY,
    tenant TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    payload TEXT NOT NULL,
    sent INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    status TEXT NOT NULL CHECK (status IN ('queued','running','succeeded','cancelled')),
    owner TEXT,
    generation INTEGER NOT NULL DEFAULT 0,
    lease_until REAL NOT NULL DEFAULT 0,
    result TEXT
);
"""


def init_db(path: Path) -> None:
    """仅创建缺失表；不清空已有文件。实验使用新的临时目录重置。"""
    with connection(path) as con:
        con.executescript(SCHEMA)


def _canonical(value: object) -> str:
    # 教学参数只有字符串与整数；不用它承诺任意 JSON/浮点的跨语言规范化。
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


# region local_idempotency
def save_document(
    path: Path, tenant: str, op_key: str, doc_id: str, content: str,
    *, fail_before_commit: bool = False,
) -> dict[str, object]:
    """本地文档更新、结果记录和 Outbox 在同一 SQLite 事务中提交。"""
    if not all(isinstance(x, str) and x for x in (tenant, op_key, doc_id, content)):
        raise ValueError("本实验字段必须是非空字符串")
    fingerprint = _canonical({"doc_id": doc_id, "content": content})
    with connection(path) as con, transaction(con):
        previous = con.execute(
            "SELECT fingerprint, result FROM operations WHERE tenant=? AND op_key=?",
            (tenant, op_key),
        ).fetchone()
        if previous:
            if previous[0] != fingerprint:
                raise Conflict("相同操作键的参数不同")
            return json.loads(previous[1])
        row = con.execute(
            "SELECT version FROM documents WHERE tenant=? AND doc_id=?",
            (tenant, doc_id),
        ).fetchone()
        version = row[0] + 1 if row else 1
        con.execute(
            "INSERT INTO documents VALUES(?,?,?,?) "
            "ON CONFLICT(tenant,doc_id) DO UPDATE "
            "SET version=excluded.version, content=excluded.content",
            (tenant, doc_id, version, content),
        )
        result = {"doc_id": doc_id, "version": version}
        event_id = _canonical([tenant, op_key])
        con.execute("INSERT INTO outbox(event_id,tenant,doc_id,version,payload) VALUES(?,?,?,?,?)",
                    (event_id, tenant, doc_id, version, _canonical(result)))
        con.execute("INSERT INTO operations VALUES(?,?,?,?)",
                    (tenant, op_key, fingerprint, _canonical(result)))
        if fail_before_commit:
            raise InjectedFailure("本地提交前失败：三张表一起回滚")
        return result
# endregion local_idempotency


def read_document(path: Path, tenant: str, doc_id: str) -> tuple[int, str] | None:
    with connection(path) as con:
        return con.execute("SELECT version,content FROM documents WHERE tenant=? AND doc_id=?",
                           (tenant, doc_id)).fetchone()


def table_count(path: Path, table: str) -> int:
    if table not in {"operations", "documents", "outbox", "tasks"}:
        raise ValueError("表名只允许实验内部白名单")
    with connection(path) as con:
        return con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def create_task(path: Path, task_id: str) -> None:
    with connection(path) as con, transaction(con):
        con.execute("INSERT INTO tasks(task_id,status) VALUES(?,'queued')", (task_id,))


def claim_task(path: Path, task_id: str, owner: str, now: float, ttl: float) -> int | None:
    """同一逻辑时间域下领取；真实跨机器系统需要权威授时/租约协议。"""
    if not owner or ttl <= 0 or not all(math.isfinite(x) for x in (now, ttl)):
        raise ValueError("owner、now 和 ttl 不合法")
    with connection(path) as con, transaction(con):
        cursor = con.execute(
            "UPDATE tasks SET status='running',owner=?,generation=generation+1,lease_until=? "
            "WHERE task_id=? AND (status='queued' OR (status='running' AND lease_until<=?))",
            (owner, now + ttl, task_id, now),
        )
        if cursor.rowcount != 1:
            return None
        return con.execute("SELECT generation FROM tasks WHERE task_id=?", (task_id,)).fetchone()[0]


# region fenced_update
FINISH_SQL = """UPDATE tasks SET status='succeeded', result=?
WHERE task_id=? AND status='running'
  AND owner=? AND generation=? AND lease_until>?"""


def finish_task(path: Path, task_id: str, owner: str, generation: int,
                now: float, result: str) -> bool:
    with connection(path) as con, transaction(con):
        changed = con.execute(FINISH_SQL, (result, task_id, owner, generation, now)).rowcount
        return changed == 1
# endregion fenced_update


class FakeProvider:
    """反例专用内存对象：没有幂等、没有状态查询，也不是外部真实服务。"""

    def __init__(self) -> None:
        self.actions: list[str] = []

    def act(self, label: str) -> None:
        self.actions.append(label)


def unsafe_external_then_record(provider: FakeProvider, label: str) -> None:
    provider.act(label)
    raise InjectedFailure("外部模拟动作之后、本地记录之前失败；重做会重复")


def main() -> None:
    from tempfile import TemporaryDirectory
    with TemporaryDirectory(prefix="backend-lab-") as directory:
        path = Path(directory) / "lesson.sqlite"
        init_db(path)
        print("第一次:", save_document(path, "team-a", "save-42", "doc-42", "正文"))
        print("同键重试:", save_document(path, "team-a", "save-42", "doc-42", "正文"))
        print("文档数/操作数/事件数:", *(table_count(path, x) for x in ("documents", "operations", "outbox")))
        create_task(path, "job-42")
        old = claim_task(path, "job-42", "A", 0, 10)
        new = claim_task(path, "job-42", "B", 11, 10)
        print("代际:", old, new)
        print("旧工作者写回:", finish_task(path, "job-42", "A", old, 12, "old"))
        print("新工作者写回:", finish_task(path, "job-42", "B", new, 12, "new"))


if __name__ == "__main__":
    main()
