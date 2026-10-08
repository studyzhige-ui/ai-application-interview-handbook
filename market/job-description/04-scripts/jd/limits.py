"""Explicit per-source collection bounds. No network or files on import."""
from __future__ import annotations
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
import time


class CollectionStopped(BaseException):
    """Terminal manual bound; adapter retry/fallback handlers must not swallow it."""


@dataclass
class Budget:
    max_pages: int
    max_jobs: int
    timeout_seconds: float
    pages: int = 0
    jobs: list = field(default_factory=list)
    failures: list = field(default_factory=list)
    limits_hit: set = field(default_factory=set)
    started: float = field(default_factory=time.monotonic)

    def __post_init__(self):
        import math
        if (isinstance(self.max_pages, bool) or not isinstance(self.max_pages, int) or self.max_pages <= 0
                or isinstance(self.max_jobs, bool) or not isinstance(self.max_jobs, int) or self.max_jobs <= 0
                or not math.isfinite(self.timeout_seconds) or self.timeout_seconds <= 0):
            raise ValueError("Positive max-pages, max-jobs and timeout-seconds are required")

    def remaining(self):
        left = self.timeout_seconds - (time.monotonic() - self.started)
        if left <= 0:
            self.limits_hit.add("timeout")
            raise CollectionStopped("Manual timeout reached")
        return left

    def next_page(self):
        self.remaining()
        if len(self.jobs) >= self.max_jobs:
            self.limits_hit.add("max_jobs")
            return False
        if self.pages >= self.max_pages:
            self.limits_hit.add("max_pages")
            return False
        self.pages += 1
        return True

    def add_job(self, job):
        self.remaining()
        if len(self.jobs) >= self.max_jobs:
            self.limits_hit.add("max_jobs")
            raise CollectionStopped("Manual job limit reached")
        self.jobs.append(job)
        if getattr(self, "job_log", None):
            import json
            from dataclasses import asdict
            with self.job_log.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(asdict(job), ensure_ascii=False) + "\n")


_ACTIVE = ContextVar("explicit_jd_collection", default=None)


def current_budget():
    budget = _ACTIVE.get()
    if budget is None:
        raise RuntimeError("Code collection is disabled; use the explicit bounded collect command")
    return budget


@contextmanager
def collection_scope(budget):
    token = _ACTIVE.set(budget)
    try:
        yield budget
    finally:
        _ACTIVE.reset(token)


def list_page():
    return current_budget().next_page()


def pages(*args):
    for page in range(*args):
        if not list_page():
            return
        yield page
    # A hard adapter guard is not evidence of complete source enumeration.
    current_budget().limits_hit.add("adapter_page_guard")


def job_rows(rows):
    budget = current_budget()
    for row in rows:
        budget.remaining()
        if len(budget.jobs) >= budget.max_jobs:
            budget.limits_hit.add("max_jobs")
            return
        yield row


def record_job(job):
    budget = _ACTIVE.get()
    if budget is not None:
        budget.add_job(job)
