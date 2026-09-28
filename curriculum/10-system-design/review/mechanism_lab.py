"""Deterministic teaching models; NOT a database, broker, payment or auth service.

All mutable state is in process memory. Calls are sequential. Logical time is
supplied by the caller. Real persistence, concurrent transactions, wall clocks,
provider cancellation, credentials and network behaviour are not implemented.

Run from any directory: python path/to/mechanism_lab.py all
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
from typing import Any


class Conflict(ValueError):
    """The same identity or transition was given incompatible information."""


def amount(value: Any, name: str, *, positive: bool = False) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(f"{name}: boolean is not a number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{name}: invalid number") from exc
    if not result.is_finite() or result < 0 or (positive and result == 0):
        raise ValueError(f"{name}: expected {'positive' if positive else 'nonnegative'} finite number")
    return result


def integer(value: Any, name: str, *, positive: bool = False) -> int:
    if type(value) is not int or value < (1 if positive else 0):
        raise ValueError(f"{name}: expected {'positive' if positive else 'nonnegative'} integer")
    return value


def identity(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{name}: expected nonempty string")
    return value


def load_scenarios() -> dict[str, Any]:
    path = Path(__file__).with_name("scenarios.json")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def capacity(config: dict[str, Any]) -> dict[str, Decimal]:
    rates = {k: amount(v, k) for k, v in config["requests_per_second"].items()}
    sizes = {k: amount(v, k) for k, v in config["response_bytes"].items()}
    if set(rates) != {"status", "report", "create"} or rates.keys() != sizes.keys():
        raise ValueError("rates and response sizes must have status/report/create keys")
    calls = rates["create"]  # One model invocation per accepted generation job.
    ti = amount(config["input_tokens_per_call"], "input tokens")
    to = amount(config["output_tokens_per_call"], "output tokens")
    seconds = amount(config["mean_seconds_per_call"], "service seconds", positive=True)
    slots = amount(config["slots"], "slots", positive=True)
    pi = amount(config["input_cost_per_million"], "input price")
    po = amount(config["output_cost_per_million"], "output price")
    metadata = amount(config["metadata_bytes_per_job"], "metadata bytes")
    days = amount(config["retention_days"], "retention days", positive=True)
    copies = amount(config["copies"], "copies", positive=True)
    day_calls = calls * 86400
    one_cost = (ti * pi + to * po) / 1000000
    payload_rate = sum((rates[k] * sizes[k] for k in rates), Decimal(0))
    return {
        "http_requests_per_second": sum(rates.values(), Decimal(0)),
        "model_calls_per_second": calls,
        "input_tokens_per_second": calls * ti,
        "output_tokens_per_second": calls * to,
        "mean_inflight_calls": calls * seconds,
        "ideal_capacity_per_second": slots / seconds,
        "slot_utilization": calls * seconds / slots,
        "cost_per_call": one_cost,
        "cost_per_day": day_calls * one_cost,
        "metadata_bytes_per_day": day_calls * metadata,
        "retained_metadata_bytes": day_calls * metadata * days,
        "replicated_metadata_bytes": day_calls * metadata * days * copies,
        "response_payload_bytes_per_second": payload_rate,
        "response_payload_bits_per_second": payload_rate * 8,
    }


def fluid_queue(normal_rate: Any, burst_rate: Any, capacity: Any,
                burst_seconds: Any) -> dict[str, Any]:
    normal = amount(normal_rate, "normal rate")
    burst = amount(burst_rate, "burst rate")
    service = amount(capacity, "capacity", positive=True)
    seconds = amount(burst_seconds, "burst seconds")
    backlog = max(Decimal(0), (burst - service) * seconds)
    spare = service - normal
    drain = Decimal(0) if backlog == 0 else (backlog / spare if spare > 0 else None)
    return {"backlog": backlog, "net_drain_rate": spare,
            "drain_seconds": drain, "strict_mean_headroom": spare > 0}


@dataclass(frozen=True)
class Event:
    tenant: str
    user: str
    event_id: str
    sequence: int
    content: str

    def __post_init__(self) -> None:
        for name in ("tenant", "user", "event_id", "content"):
            identity(getattr(self, name), name)
        integer(self.sequence, "sequence")


class RecentProjection:
    """Keeps ALL accepted events to make reconstruction and dedup inspectable.

    This intentionally unbounded teaching history is not a production memory or
    retention strategy. Sequence numbers are unique inside each trusted scope.
    The model demonstrates isolation of data; it does not authenticate callers.
    """
    def __init__(self, limit: int, *, order: str = "source") -> None:
        self.limit = integer(limit, "limit", positive=True)
        if order not in {"source", "first_received"}:
            raise ValueError("order must be source or first_received")
        self.order = order
        self.events: dict[tuple[str, str, str], Event] = {}
        self.sequences: dict[tuple[str, str, int], str] = {}

    def apply(self, event: Event) -> bool:
        key = (event.tenant, event.user, event.event_id)
        if key in self.events:
            if self.events[key] != event:
                raise Conflict("same event identity has different content or sequence")
            return False
        seqkey = (event.tenant, event.user, event.sequence)
        if seqkey in self.sequences:
            raise Conflict("source sequence already belongs to another event")
        self.events[key] = event
        self.sequences[seqkey] = event.event_id
        return True

    def snapshot(self, tenant: str, user: str) -> list[Event]:
        identity(tenant, "tenant")
        identity(user, "user")
        rows = (e for e in self.events.values() if (e.tenant, e.user) == (tenant, user))
        if self.order == "source":
            return sorted(rows, key=lambda e: e.sequence, reverse=True)[:self.limit]
        # Dict insertion order models one consumer's FIRST receipt order only.
        # apply() never reinserts a duplicate. This is NOT a distributed clock.
        return list(rows)[::-1][:self.limit]


@dataclass
class Reservation:
    quantity: int
    state: str


class Inventory:
    """Sequential logical transactions, not a database concurrency benchmark."""
    def __init__(self, initial: int) -> None:
        self.initial = integer(initial, "initial")
        self.available = self.initial
        self.sold = 0
        self.operations: dict[str, Reservation] = {}

    @property
    def held(self) -> int:
        return sum(r.quantity for r in self.operations.values() if r.state == "HELD")

    def reserve(self, key: str, quantity: int) -> str:
        identity(key, "operation key")
        integer(quantity, "quantity", positive=True)
        if key in self.operations:
            existing = self.operations[key]
            if existing.quantity != quantity:
                raise Conflict("same operation key with different quantity")
            return existing.state
        if quantity > self.available:
            self.operations[key] = Reservation(quantity, "REJECTED")
            return "REJECTED"
        self.available -= quantity
        self.operations[key] = Reservation(quantity, "HELD")
        self.check()
        return "HELD"

    def finish(self, key: str, outcome: str) -> bool:
        if outcome not in {"PAID", "RELEASED"}:
            raise ValueError("outcome must be PAID or RELEASED")
        record = self.operations[key]
        if record.state == outcome:
            return False
        if record.state != "HELD":
            raise Conflict("reservation is no longer eligible for this transition")
        record.state = outcome
        if outcome == "PAID":
            self.sold += record.quantity
        else:
            self.available += record.quantity
        self.check()
        return True

    def check(self) -> None:
        assert self.available >= 0 and self.sold >= 0 and self.held >= 0
        assert self.available + self.held + self.sold == self.initial


class LeaseResource:
    """One authoritative in-memory resource; caller provides logical time.

    Claim and submit are single sequential operations in this model. There is no
    network, clock-skew handling, external resource fencing or real concurrency.
    """
    def __init__(self) -> None:
        self.generation = 0
        self.owner: str | None = None
        self.expires_at = Decimal(0)
        self.result: str | None = None
        self.writes = 0

    def claim(self, owner: str, now: Any, duration: Any) -> int:
        identity(owner, "owner")
        clock = amount(now, "now")
        span = amount(duration, "duration", positive=True)
        if self.result is not None:
            raise Conflict("completed resource cannot be claimed again")
        if self.owner is not None and clock < self.expires_at:
            raise Conflict("current lease is still valid")
        self.generation += 1
        self.owner = owner
        self.expires_at = clock + span
        return self.generation

    def submit(self, generation: int, now: Any, result: str) -> bool:
        integer(generation, "generation", positive=True)
        identity(result, "result")
        clock = amount(now, "now")
        if generation != self.generation or clock >= self.expires_at:
            raise Conflict("stale generation or expired lease")
        if self.result is not None:
            if self.result != result:
                raise Conflict("completed result cannot be replaced")
            return False
        self.result = result
        self.writes += 1
        return True


@dataclass
class BudgetOperation:
    reserved: Decimal
    state: str = "RESERVED"
    actual: Decimal | None = None


class BudgetLedger:
    """Sequential budget accounting in fictional units, not a billing service."""
    def __init__(self, limit: Any) -> None:
        self.limit = amount(limit, "budget limit")
        self.operations: dict[str, BudgetOperation] = {}

    @property
    def spent(self) -> Decimal:
        return sum((r.actual for r in self.operations.values() if r.actual is not None), Decimal(0))

    @property
    def held(self) -> Decimal:
        return sum((r.reserved for r in self.operations.values() if r.actual is None), Decimal(0))

    @property
    def available(self) -> Decimal:
        return self.limit - self.spent - self.held

    def reserve(self, key: str, units: Any) -> bool:
        identity(key, "operation key")
        needed = amount(units, "reservation", positive=True)
        if key in self.operations:
            if self.operations[key].reserved != needed:
                raise Conflict("reservation parameters changed")
            return False
        if needed > self.available:
            raise Conflict("insufficient available budget")
        self.operations[key] = BudgetOperation(needed)
        return True

    def mark_unknown(self, key: str) -> None:
        record = self.operations[key]
        if record.actual is None:
            record.state = "UNKNOWN"

    def settle(self, key: str, units: Any) -> bool:
        actual = amount(units, "actual usage")
        record = self.operations[key]
        if record.actual is not None:
            if record.actual != actual:
                raise Conflict("conflicting confirmed settlement")
            return False
        # Preserve the actual expense even if it exceeds the reservation/limit.
        record.actual = actual
        record.state = "SETTLED"
        return True

    def snapshot(self) -> dict[str, Any]:
        return {"spent": self.spent, "held": self.held,
                "available": self.available, "overdrawn": self.available < 0}


class QRRequest:
    """State-transition model only: NO real authentication, nonce or token issue."""
    def __init__(self, browser: str, expires_at: Any) -> None:
        self.browser = identity(browser, "browser")
        self.expires_at = amount(expires_at, "expires_at", positive=True)
        self.state = "PENDING"
        self.exchange_count = 0

    def advance(self, action: str, now: Any, browser: str) -> bool:
        if action not in {"scan", "confirm", "exchange"}:
            raise ValueError("unknown action")
        clock = amount(now, "now")
        if browser != self.browser:
            raise Conflict("wrong initiating browser binding")
        if self.state in {"EXCHANGED", "EXPIRED"}:
            return False
        if clock >= self.expires_at:
            self.state = "EXPIRED"
            return False
        expected, target = {"scan": ("PENDING", "SCANNED"),
                            "confirm": ("SCANNED", "CONFIRMED"),
                            "exchange": ("CONFIRMED", "EXCHANGED")}[action]
        if self.state != expected:
            raise Conflict("invalid state transition")
        self.state = target
        if target == "EXCHANGED":
            self.exchange_count += 1
        return True


@dataclass
class ExternalAction:
    """Stores uncertainty; this model never calls an external provider."""
    operation_key: str
    state: str = "UNKNOWN"
    receipt: str | None = None

    def next_step(self, *, query_supported: bool, idempotency_supported: bool) -> str:
        if self.state == "SUCCEEDED":
            return "reuse-confirmed-result"
        if query_supported:
            return "query-with-original-operation-identity"
        if idempotency_supported:
            return "retry-under-provider-contract-with-same-key"
        return "manual-reconciliation"

    def reconcile(self, receipt: str | None) -> None:
        # A single not-found query is NOT proof that an in-flight action failed.
        if receipt is None:
            return
        identity(receipt, "receipt")
        if self.receipt is not None and self.receipt != receipt:
            raise Conflict("different receipts for the same action require reconciliation")
        self.receipt = receipt
        self.state = "SUCCEEDED"


def demo(which: str) -> dict[str, Any]:
    fixtures = load_scenarios()
    output: dict[str, Any] = {}
    if which in {"all", "capacity"}:
        output["capacity"] = capacity(fixtures["workload"])
    if which in {"all", "queue"}:
        output["queue"] = fluid_queue(**fixtures["queue"])
    if which in {"all", "window"}:
        spec = fixtures["window"]
        projection = RecentProjection(spec["hand_worked_limit"])
        trace = []
        for raw in spec["events"]:
            projection.apply(Event(**raw))
            trace.append([e.sequence for e in projection.snapshot(*spec["scope"])])
        output["window"] = {"limit": projection.limit, "states": trace}
    if which in {"all", "budget"}:
        spec = fixtures["budget"]
        ledger = BudgetLedger(spec["limit"])
        states = [ledger.snapshot()]
        ledger.reserve(spec["operation_key"], spec["reservation"])
        states.append(ledger.snapshot())
        ledger.mark_unknown(spec["operation_key"])
        states.append(ledger.snapshot())
        ledger.settle(spec["operation_key"], spec["actual"])
        states.append(ledger.snapshot())
        ledger.settle(spec["operation_key"], spec["actual"])
        states.append(ledger.snapshot())
        output["budget"] = states
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=["all", "capacity", "queue", "window", "budget"], nargs="?", default="all")
    args = parser.parse_args()
    print(json.dumps(demo(args.scenario), ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
