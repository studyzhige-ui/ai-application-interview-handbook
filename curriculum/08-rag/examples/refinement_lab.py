"""Small deterministic checks for chapters 07, 09 and 12.

Inputs include HUMAN-ASSIGNED support judgments and resource-readiness flags.
This is not a semantic judge, database, durable log or concurrent publisher.
No files, network, models or external services are used by the demo.
"""
from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from typing import Mapping, Sequence


def _int(value: int, name: str, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def bm25_term_weight(tf: int, length: int, average_length: float,
                     idf: float = 1.0, k1: float = 1.2, b: float = 0.75) -> float:
    """The common formula printed in chapter 07, not Lucene's exact score API."""
    _int(tf, "tf")
    _int(length, "length", 1)
    if tf > length:
        raise ValueError("tf cannot exceed the document length in this model")
    for value in (average_length, idf, k1, b):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("parameters must be finite numbers")
    if average_length <= 0 or idf < 0 or k1 <= 0 or not 0 <= b <= 1:
        raise ValueError("invalid length, IDF, k1 or b")
    return idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * length / average_length))


def support_gaps(conditions: Sequence[str], judgments: Mapping[str, str]) -> list[str]:
    """Consume supplied judgments; NEVER infer semantic support from text.

Allowed statuses: supported, unsupported, conflict, unchecked.
A missing judgment means unchecked. No unseen document IDs are required.
"""
    if isinstance(conditions, (str, bytes)):
        raise ValueError("conditions must be a sequence, not one string")
    if any(not isinstance(key, str) or not key for key in conditions):
        raise ValueError("each condition needs a non-empty name")
    if len(conditions) != len(set(conditions)):
        raise ValueError("duplicate condition")
    if set(judgments) - set(conditions):
        raise ValueError("judgment refers to an unknown condition")
    if any(value not in {"supported", "unsupported", "conflict", "unchecked"}
           for value in judgments.values()):
        raise ValueError("invalid judgment status")
    return [key for key in conditions if judgments.get(key) != "supported"]


@dataclass(frozen=True)
class Generation:
    name: str
    encoder: str
    vector_index: str
    term_index: str
    content_store: str


@dataclass(frozen=True)
class Publication:
    active: str = "g1"
    write_target: str = "g1"
    release_revision: int = 7
    boundary: int = 100


def bind_request(record: Publication, generations: Mapping[str, Generation]) -> Generation:
    """Return the immutable bundle selected when a request begins."""
    return generations[record.active]


def advance_contiguous(applied_through: int, completed: Sequence[int]) -> int:
    """Advance only the contiguous prefix; caller must retain unconsumed ACKs.

Each ACK is assumed to mean ALL required resources are confirmed usable.
Receiving a job or acknowledging an HTTP request does not meet that premise.
"""
    _int(applied_through, "applied_through")
    for value in completed:
        _int(value, "sequence", 1)
    acknowledged = set(completed)
    while applied_through + 1 in acknowledged:
        applied_through += 1
    return applied_through


def publish(record: Publication, *, expected_revision: int, target: Generation,
            boundary: int, applied_through: int, dispatch_paused: bool,
            in_flight: int, resources_ready: bool) -> Publication:
    """Pure transition under chapter 12's stated assumptions, NOT a real CAS.

A real implementation must read/check/write atomically in its control store.
Paused dispatch, in-flight work, readiness and ACKs require real verification.
"""
    for value, name in ((expected_revision, "expected_revision"), (boundary, "boundary"),
                        (applied_through, "applied_through"), (in_flight, "in_flight")):
        _int(value, name)
    if type(dispatch_paused) is not bool or type(resources_ready) is not bool:
        raise ValueError("readiness flags must be explicit booleans")
    if record.release_revision != expected_revision:
        raise ValueError("stale publication revision")
    if not dispatch_paused or in_flight:
        raise ValueError("dispatch must be paused and in-flight work settled")
    if not resources_ready or applied_through < boundary or boundary < record.boundary:
        raise ValueError("target has not passed the cutover boundary")
    if not all((target.name, target.encoder, target.vector_index, target.term_index, target.content_store)):
        raise ValueError("incomplete resource bundle")
    return Publication(target.name, target.name, record.release_revision + 1, boundary)


def demo() -> dict:
    generations = {
        "g1": Generation("g1", "e1", "v1", "s1", "c1"),
        "g2": Generation("g2", "e2", "v2", "s2", "c2"),
    }
    before = Publication()
    q1 = bind_request(before, generations)
    after = publish(before, expected_revision=7, target=generations["g2"],
                    boundary=103, applied_through=advance_contiguous(100, [101, 102, 103]),
                    dispatch_paused=True, in_flight=0, resources_ready=True)
    # Reconstruct from a supplied record to model recovery DECISION, not persistence.
    recovered = Publication(**asdict(after))
    return {
        "simulation_only": True,
        "support_judgments_are_manual": True,
        "bm25_table": [round(bm25_term_weight(tf, 100, 100), 6) for tf in (1, 2, 4, 8)],
        "doubled_length_weight": round(bm25_term_weight(1, 200, 100), 6),
        "online_gaps": support_gaps(["product", "time", "resource_status"],
                                    {"product": "supported", "time": "supported"}),
        "incomplete_prefix": advance_contiguous(100, [102, 103]),
        "publication": asdict(after),
        "event_104_target_after_recovery": recovered.write_target,
        "old_request_content_store": q1.content_store,
        "new_request_content_store": bind_request(after, generations).content_store,
    }


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
