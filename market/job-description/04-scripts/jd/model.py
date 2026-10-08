"""Extracted transport fields; exact response bytes remain in raw observations."""
from dataclasses import dataclass
from typing import Any
@dataclass
class Job:
    company: str
    title: str
    job_id: str
    location: str
    category: str
    department: str
    description: str
    requirements: str
    official_url: str
    official_api: str
    cycle_evidence: str


    def __post_init__(self):
        from .limits import record_job
        record_job(self)


def txt(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return ", ".join(txt(x) for x in v if x is not None)
    if isinstance(v, dict):
        return " ".join(txt(x) for x in v.values())
    return str(v).strip()
