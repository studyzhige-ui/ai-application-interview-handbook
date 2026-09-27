"""Deterministic RAG mechanism lab, not a model, database, or authorization service.

Python 3.13+ standard library only. All policies, rankings and costs are fixtures.
Running this file prints JSON and does not create files or contact a service.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


def _integer(value: int, name: str, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _unique_ids(items: Sequence[str], name: str = "ranking") -> list[str]:
    if isinstance(items, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of IDs, not one string")
    result = list(items)
    if any(not isinstance(x, str) or not x for x in result):
        raise ValueError(f"{name} contains an invalid ID")
    if len(result) != len(set(result)):
        raise ValueError(f"{name} contains duplicate IDs")
    return result


def window_spans(length: int, size: int, overlap: int) -> list[tuple[int, int]]:
    """Return half-open integer spans; units are NOT automatically model Tokens."""
    _integer(length, "length")
    _integer(size, "size", 1)
    _integer(overlap, "overlap")
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")
    result: list[tuple[int, int]] = []
    start = 0
    while start < length:
        end = min(start + size, length)
        result.append((start, end))
        if end == length:
            break
        start += size - overlap
    return result


def rrf(rankings: Sequence[Sequence[str]], constant: float = 60) -> list[tuple[str, float]]:
    """One-based RRF. Missing entries contribute zero; ties sort by ID.

Each route must already be authorized and use a shared identity definition.
The constant is a math parameter; a product API can impose stricter limits.
"""
    if isinstance(constant, bool) or not isinstance(constant, (int, float)):
        raise ValueError("constant must be a finite non-negative number")
    if not math.isfinite(constant) or constant < 0:
        raise ValueError("constant must be a finite non-negative number")
    scores: dict[str, float] = {}
    for route in rankings:
        for rank, item_id in enumerate(_unique_ids(route), 1):
            scores[item_id] = scores.get(item_id, 0.0) + 1.0 / (constant + rank)
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))


def retrieval_metrics(ranking: Sequence[str], relevant: set[str], k: int) -> dict[str, float | None]:
    """Binary relevance. Precision denominator is K even for a short result list.

Empty relevance is not a retrieval-recall task: all five values are None.
Unanswerable/refusal tasks need their own labels, not an invented recall of 1.
"""
    _integer(k, "k", 1)
    ranked = _unique_ids(ranking)
    _unique_ids(list(relevant), "relevant")
    if not relevant:
        return dict.fromkeys(("recall", "precision", "hit", "rr", "complete"))
    top = ranked[:k]
    hits = set(top) & relevant
    first = next((i for i, item in enumerate(top, 1) if item in relevant), None)
    return {
        "recall": len(hits) / len(relevant),
        "precision": len(hits) / k,
        "hit": float(bool(hits)),
        "rr": 1.0 / first if first else 0.0,
        "complete": float(relevant <= set(top)),
    }


def ndcg(ranking: Sequence[str], grades: Mapping[str, int], k: int) -> float | None:
    """NDCG@K using (2**grade - 1)/log2(rank+1), ideal from ALL known grades.

An absent grade is treated as zero ONLY for this fully labelled toy corpus.
This convention must not convert unjudged production documents into negatives.
"""
    _integer(k, "k", 1)
    ranked = _unique_ids(ranking)
    for grade in grades.values():
        _integer(grade, "grade")
    def dcg(values: Iterable[int]) -> float:
        return sum((2.0 ** grade - 1.0) / math.log2(rank + 1)
                   for rank, grade in enumerate(values, 1))
    ideal = dcg(sorted(grades.values(), reverse=True)[:k])
    if ideal == 0:
        return None
    return dcg(grades.get(item_id, 0) for item_id in ranked[:k]) / ideal


def validate_citation_ids(citations: Sequence[str], allowed: set[str]) -> None:
    """Validate IDs only; does NOT establish entailment, source truth or permission."""
    if isinstance(citations, (str, bytes)):
        raise ValueError("citations must be a list of IDs")
    if any(not isinstance(item_id, str) or item_id not in allowed for item_id in citations):
        raise ValueError("citation ID was not supplied in this request")


@dataclass(frozen=True)
class Chunk:
    id: str
    document: str
    version: str
    tenant: str
    text: str
    cost: int  # artificial budget units, NOT Token measurements


# Fictional data shared by the chapters, demo and tests. These are not company facts.
CHUNKS = {
    "A": Chunk("A", "P1", "v2", "beichen", "标准版订阅购买后14天内可申请普通退款。", 70),
    "B": Chunk("B", "P1", "v2", "beichen", "已经开通专属资源的订单不适用普通退款规则，需人工复核。", 40),
    "C": Chunk("C", "P2", "v1", "beichen", "发票信息可在开具后30天内申请更正。", 60),
    "D": Chunk("D", "P3", "v1", "beichen", "账户停用前应确认未完成事项。", 30),
}
DENSE_FIXTURE = ["A", "C", "B"]
LEXICAL_FIXTURE = ["B", "A", "D"]
BAD_RERANK_FIXTURE = ["A", "C", "B", "D"]
REQUIRED_EVIDENCE = {"A", "B"}  # hand-labelled oracle for evaluation, not a model prediction


def greedy_pack(ranking: Sequence[str], chunks: Mapping[str, Chunk], budget: int) -> list[str]:
    """Illustrate order and budget only. Does NOT optimize semantic coverage."""
    _integer(budget, "budget")
    selected = []
    used = 0
    for item_id in _unique_ids(ranking):
        chunk = chunks[item_id]  # unknown IDs fail loudly instead of being fabricated
        _integer(chunk.cost, "cost")
        if used + chunk.cost <= budget:
            selected.append(item_id)
            used += chunk.cost
    return selected


@dataclass(frozen=True)
class SourceEvent:
    revision: int
    content: str | None  # None is a deletion tombstone, not "no event"


class RevisionLedger:
    """Single-process state simulation. No persistence, threads, or external writes."""
    def __init__(self) -> None:
        self.events: dict[str, SourceEvent] = {}

    def apply(self, document: str, revision: int, content: str | None) -> str:
        _integer(revision, "revision", 1)
        if not isinstance(document, str) or not document:
            raise ValueError("document must be a non-empty ID")
        if content is not None and not isinstance(content, str):
            raise ValueError("content must be text or a deletion tombstone")
        event = SourceEvent(revision, content)
        current = self.events.get(document)
        if current and revision < current.revision:
            return "stale"
        if current and revision == current.revision:
            if event != current:
                raise ValueError("one source revision cannot describe conflicting content")
            return "duplicate"
        self.events[document] = event
        return "accepted"


@dataclass(frozen=True)
class AccessPolicy:
    """Explicit current-policy fixture; supplied by a trusted caller in this lab."""
    tenant: str
    revision: int
    allowed_documents: frozenset[str]
    deleted_documents: frozenset[str] = frozenset()

    def allows(self, chunk: Chunk) -> bool:
        return (chunk.tenant == self.tenant
                and chunk.document in self.allowed_documents
                and chunk.document not in self.deleted_documents)


def authorized_chunks(generation: Sequence[Chunk], current_policy: AccessPolicy) -> list[Chunk]:
    """Generation describes content; the caller must supply CURRENT authorization."""
    return [chunk for chunk in generation if current_policy.allows(chunk)]


def main() -> None:
    fused = [item_id for item_id, _ in rrf([DENSE_FIXTURE, LEXICAL_FIXTURE])]
    early = greedy_pack(BAD_RERANK_FIXTURE[:2], CHUNKS, 110)
    packed = greedy_pack(BAD_RERANK_FIXTURE, CHUNKS, 110)
    ledger = RevisionLedger()
    state_result = [ledger.apply("P1", n, text)
                    for n, text in [(8, "v8"), (7, "v7"), (9, None), (8, "v8")]]
    old_generation = list(CHUNKS.values())
    revoked = AccessPolicy("beichen", 2, frozenset({"P2", "P3"}))
    result = {
        "simulation_only": True,
        "rankings_are_fixtures": True,
        "budget_units_are_not_tokens": True,
        "fused": fused,
        "early_top2_context": early,
        "keep_candidates_context": packed,
        "early_top2_metrics": retrieval_metrics(early, REQUIRED_EVIDENCE, 2),
        "packed_metrics": retrieval_metrics(packed, REQUIRED_EVIDENCE, 2),
        "graded_ndcg": ndcg(["C", "A", "B"], {"A": 1, "B": 2, "C": 0, "D": 0}, 3),
        "revision_timeline": state_result,
        "rollback_current_permission": [chunk.id for chunk in authorized_chunks(old_generation, revoked)],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
