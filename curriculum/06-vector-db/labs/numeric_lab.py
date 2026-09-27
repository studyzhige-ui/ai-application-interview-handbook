"""Pure numerical examples and explicitly single-process teaching simulations.

No model, ANN package, database, network, persistence, or concurrency guarantee.
Run from any directory: python /path/to/numeric_lab.py
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
import heapq
import json
import math

DATA_PATH = Path(__file__).with_name('data.json')

def load_data() -> dict:
    return json.loads(DATA_PATH.read_text(encoding='utf-8'))

def checked_vector(value: Sequence[float]) -> tuple[float, ...]:
    if not value:
        raise ValueError('vector must not be empty')
    result = tuple(float(x) for x in value)
    if not all(math.isfinite(x) for x in result):
        raise ValueError('coordinates must be finite')
    return result

def positive_int(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f'{name} must be a positive integer')

def measure(a: Sequence[float], b: Sequence[float], metric: str = 'l2_squared') -> float:
    x, y = checked_vector(a), checked_vector(b)
    if len(x) != len(y):
        raise ValueError('dimension mismatch')
    dot = sum(u * v for u, v in zip(x, y))
    if metric == 'ip':
        result = dot
    elif metric == 'cosine':
        nx, ny = math.hypot(*x), math.hypot(*y)
        if nx == 0 or ny == 0:
            raise ValueError('cosine is undefined for a zero vector')
        result = dot / (nx * ny)
    elif metric == 'l2_squared':
        result = sum((u - v) ** 2 for u, v in zip(x, y))
    else:
        raise ValueError(f'unsupported metric: {metric}')
    if not math.isfinite(result):
        raise ValueError('numeric overflow: rescale inputs before computing')
    return result

def exact_search(records: list[dict], query: Sequence[float], k: int,
                 metric: str = 'l2_squared', tenant: str | None = None) -> list[dict]:
    positive_int(k, 'k')
    checked_vector(query)
    if metric not in ('l2_squared', 'ip', 'cosine'):
        raise ValueError('unsupported metric')
    if len({r['id'] for r in records}) != len(records):
        raise ValueError('record ids must be unique')
    results = []
    for row in records:
        if tenant is not None and row['tenant_id'] != tenant:
            continue
        results.append({'id': row['id'], 'score': measure(query, row['vector'], metric)})
    # Shared fixture uses string ids. Tie-break is explicitly part of this baseline.
    descending = metric != 'l2_squared'
    results.sort(key=lambda r: (-r['score'] if descending else r['score'], r['id']))
    return results[:k]

def recall_at_k(returned: Iterable[str], gold: Iterable[str], k: int) -> float | None:
    positive_int(k, 'k')
    gold_list = list(gold)
    target = set(gold_list)
    if len(target) != len(gold_list) or len(target) > k:
        raise ValueError('gold must contain at most k unique exact target ids')
    if not target:
        return None
    # Score the returned top-k slots, NOT the oversized internal candidate pool.
    actual = set(list(returned)[:k])
    return len(actual & target) / len(target)

def graph_width_demo(width: int, t_coordinate: float = 1.0) -> dict:
    """Hand-built graph search, not a HNSW constructor or product emulator."""
    positive_int(width, 'width')
    coords = {'S': 6.0, 'A': 4.0, 'B': 5.0, 'T': float(t_coordinate)}
    if not all(math.isfinite(v) for v in coords.values()):
        raise ValueError('coordinates must be finite')
    graph = {'S': ['A', 'B'], 'A': ['S'], 'B': ['S', 'T'], 'T': ['B']}
    distance = {n: abs(x) for n, x in coords.items()}
    frontier = [(distance['S'], 'S')]
    kept = {'S'}
    seen = {'S'}
    expanded = []
    while frontier:
        d, node = heapq.heappop(frontier)
        worst = max(distance[n] for n in kept)
        if len(kept) >= width and d > worst:
            break
        expanded.append(node)
        for nb in graph[node]:
            if nb in seen:
                continue
            seen.add(nb)
            if len(kept) < width or distance[nb] < max(distance[n] for n in kept):
                heapq.heappush(frontier, (distance[nb], nb))
                kept.add(nb)
                if len(kept) > width:
                    kept.remove(max(kept, key=lambda n: (distance[n], n)))
    return {'winner': min(kept, key=lambda n: (distance[n], n)),
            'expanded': expanded, 'seen': sorted(seen)}

def ivf_boundary_demo(query: float = 4.9, nprobe: int = 1) -> float:
    """Given centres/lists from chapter 06; NOT a trained IVF implementation."""
    positive_int(nprobe, 'nprobe')
    if nprobe > 2 or not math.isfinite(query):
        raise ValueError('this fixture has two lists and requires a finite query')
    lists = [(0.0, [0.0, 4.0]), (10.0, [5.1, 10.0])]
    selected = sorted(lists, key=lambda x: (abs(query - x[0]), x[0]))[:nprobe]
    return min((x for _, items in selected for x in items), key=lambda x: (abs(query-x), x))

def pq_demo(code: tuple[int, int] = (0, 1)) -> dict:
    """Given two tiny codebooks; returns chapter 07 lookup-table calculation."""
    if len(code) != 2 or any(c not in (0, 1) for c in code):
        raise ValueError('two codes, each 0 or 1, are required')
    q = ((.3, .4), (.8, .9))
    book = ((0., 0.), (1., 1.))
    table = [[measure(part, centre) for centre in book] for part in q]
    return {'table': table, 'adc': sum(table[i][c] for i, c in enumerate(code)),
            'original_distance': measure((.3, .4, .8, .9), (.2, .1, .9, 1.1))}

@dataclass(frozen=True)
class Event:
    doc_id: str
    version: int
    text: str | None  # None is a deletion tombstone, not an empty string.

class VersionedState:
    """Single-threaded ordering simulation. This is NOT database compare-and-swap."""
    def __init__(self) -> None:
        self.state: dict[str, Event] = {}

    def apply(self, event: Event) -> bool:
        positive_int(event.version, 'version')
        previous = self.state.get(event.doc_id)
        if previous and event.version <= previous.version:
            if event.version == previous.version and event != previous:
                raise ValueError('same version carries conflicting content')
            return False
        self.state[event.doc_id] = event
        return True

    def visible(self, doc_id: str) -> str | None:
        event = self.state.get(doc_id)
        return None if event is None else event.text

def run() -> dict:
    data = load_data()
    rows, q = data['records'], data['query']
    ids = lambda values: [r['id'] for r in values]
    global_cosine = ids(exact_search(rows, q, 3, 'cosine'))
    alpha_ids = {r['id'] for r in rows if r['tenant_id'] == 'alpha'}
    state = VersionedState()
    state.apply(Event('D', 8, None))
    stale_accepted = state.apply(Event('D', 7, 'old document'))
    return {
        'kind': 'numeric_and_single_process_teaching_simulation',
        'l2_global_top3': ids(exact_search(rows, q, 3)),
        'l2_alpha_top3': ids(exact_search(rows, q, 3, tenant='alpha')),
        'cosine_global_top3': global_cosine,
        'cosine_postfiltered': [x for x in global_cosine if x in alpha_ids],
        'cosine_alpha_top3': ids(exact_search(rows, q, 3, 'cosine', 'alpha')),
        'recall_example': recall_at_k(['A','C','E'], ['A','C','D'], 3),
        'graph_width_1': graph_width_demo(1), 'graph_width_2': graph_width_demo(2),
        'ivf_probe_1': ivf_boundary_demo(nprobe=1), 'ivf_probe_2': ivf_boundary_demo(nprobe=2),
        'pq': pq_demo(), 'stale_write_after_delete_accepted': stale_accepted,
    }

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
