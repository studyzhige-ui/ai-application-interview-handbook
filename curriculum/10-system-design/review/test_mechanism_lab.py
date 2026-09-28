"""Executable checks of teaching models, not service integration tests."""
from copy import deepcopy
from decimal import Decimal
import random
import unittest

from mechanism_lab import (BudgetLedger, Conflict, Event, ExternalAction, Inventory,
                           LeaseResource, QRRequest, RecentProjection, amount,
                           capacity, demo, fluid_queue, load_scenarios)


class CapacityTests(unittest.TestCase):
    def setUp(self):
        self.config = load_scenarios()["workload"]

    def test_rates_and_units(self):
        r = capacity(self.config)
        self.assertEqual(r["http_requests_per_second"], 100)
        self.assertEqual(r["model_calls_per_second"], 20)
        self.assertEqual(r["input_tokens_per_second"], 60000)
        self.assertEqual(r["output_tokens_per_second"], 10000)

    def test_concurrency_not_cpu_count(self):
        r = capacity(self.config)
        self.assertEqual(r["mean_inflight_calls"], 200)
        self.assertEqual(r["ideal_capacity_per_second"], 30)
        self.assertAlmostEqual(r["slot_utilization"], Decimal(2) / 3)

    def test_cost_is_input_plus_output(self):
        r = capacity(self.config)
        self.assertEqual(r["cost_per_call"], Decimal("0.005"))
        self.assertEqual(r["cost_per_day"], 8640)

    def test_storage_and_network(self):
        r = capacity(self.config)
        self.assertEqual(r["metadata_bytes_per_day"], 3456000000)
        self.assertEqual(r["retained_metadata_bytes"], 103680000000)
        self.assertEqual(r["replicated_metadata_bytes"], 311040000000)
        self.assertEqual(r["response_payload_bytes_per_second"], 900000)
        self.assertEqual(r["response_payload_bits_per_second"], 7200000)

    def test_half_calls_double_tokens_transfer(self):
        config = deepcopy(self.config)
        config["requests_per_second"]["create"] = 10
        config["input_tokens_per_call"] = 6000
        config["output_tokens_per_call"] = 1000
        r = capacity(config)
        self.assertEqual(r["input_tokens_per_second"], 60000)
        self.assertEqual(r["output_tokens_per_second"], 10000)
        self.assertEqual(r["cost_per_day"], 8640)
        self.assertEqual(r["mean_inflight_calls"], 100)

    def test_changed_metadata_transfer(self):
        config = deepcopy(self.config)
        config["metadata_bytes_per_job"] = 5000
        config["retention_days"] = 7
        self.assertEqual(capacity(config)["retained_metadata_bytes"], 60480000000)

    def test_invalid_numbers(self):
        for value in (True, -1, "NaN", "Infinity", "abc", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                amount(value, "test")
        with self.assertRaises(ValueError):
            amount(0, "must positive", positive=True)

    def test_zero_service_time_rejected(self):
        self.config["mean_seconds_per_call"] = 0
        with self.assertRaises(ValueError):
            capacity(self.config)

    def test_rate_size_keys_must_match(self):
        self.config["response_bytes"].pop("status")
        with self.assertRaises(ValueError):
            capacity(self.config)


class QueueTests(unittest.TestCase):
    def test_burst_and_drain(self):
        r = fluid_queue(**load_scenarios()["queue"])
        self.assertEqual(r["backlog"], 600)
        self.assertEqual(r["net_drain_rate"], 10)
        self.assertEqual(r["drain_seconds"], 60)

    def test_equal_average_does_not_clear_backlog(self):
        r = fluid_queue(30, 40, 30, 60)
        self.assertIsNone(r["drain_seconds"])
        self.assertFalse(r["strict_mean_headroom"])

    def test_overloaded_recovery_cannot_drain(self):
        self.assertIsNone(fluid_queue(35, 40, 30, 60)["drain_seconds"])

    def test_no_backlog(self):
        r = fluid_queue(20, 25, 30, 60)
        self.assertEqual(r["backlog"], 0)
        self.assertEqual(r["drain_seconds"], 0)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            fluid_queue(20, 40, 0, 60)


class WindowTests(unittest.TestCase):
    def test_worked_trace(self):
        expected = [[101], [103, 101], [103, 102, 101],
                    [103, 102, 101], [104, 103, 102], [104, 103, 102]]
        self.assertEqual(demo("window")["window"]["states"], expected)

    def test_latest_twenty_under_shuffle(self):
        rng = random.Random(17)
        records = [Event("a", "u", f"e{i}", i, f"c{i}") for i in range(50)]
        records += records[:15]
        rng.shuffle(records)
        p = RecentProjection(20)
        for e in records:
            p.apply(e)
        self.assertEqual([e.sequence for e in p.snapshot("a", "u")], list(range(49, 29, -1)))

    def test_tenant_and_user_scopes(self):
        p = RecentProjection(20)
        p.apply(Event("a", "u", "x", 1, "a-content"))
        p.apply(Event("b", "u", "x", 1, "b-content"))
        p.apply(Event("a", "v", "x", 1, "v-content"))
        self.assertEqual([e.content for e in p.snapshot("a", "u")], ["a-content"])
        self.assertEqual(p.snapshot("a", "missing"), [])

    def test_same_id_different_content_rejected_without_mutation(self):
        p = RecentProjection(3)
        original = Event("a", "u", "x", 1, "old")
        p.apply(original)
        with self.assertRaises(Conflict):
            p.apply(Event("a", "u", "x", 1, "new"))
        self.assertEqual(p.snapshot("a", "u"), [original])

    def test_sequence_collision_rejected(self):
        p = RecentProjection(3)
        p.apply(Event("a", "u", "x", 1, "content"))
        with self.assertRaises(Conflict):
            p.apply(Event("a", "u", "y", 1, "content"))

    def test_duplicate_evicted_event_does_not_reenter(self):
        p = RecentProjection(2)
        events = [Event("a", "u", f"e{i}", i, f"c{i}") for i in range(3)]
        for e in events:
            p.apply(e)
        self.assertFalse(p.apply(events[0]))
        self.assertEqual([e.sequence for e in p.snapshot("a", "u")], [2, 1])

    def test_invalid_limit_and_sequence(self):
        for limit in (0, -1, True, 1.5):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                RecentProjection(limit)
        with self.assertRaises(ValueError):
            Event("a", "u", "id", True, "content")


class InventoryTests(unittest.TestCase):
    def test_reserve_repeat_pay_and_conservation(self):
        inventory = Inventory(100)
        self.assertEqual(inventory.reserve("R", 3), "HELD")
        self.assertEqual(inventory.reserve("R", 3), "HELD")
        self.assertEqual((inventory.available, inventory.held), (97, 3))
        self.assertTrue(inventory.finish("R", "PAID"))
        self.assertFalse(inventory.finish("R", "PAID"))
        self.assertEqual((inventory.available, inventory.held, inventory.sold), (97, 0, 3))

    def test_last_item_two_different_operations(self):
        inventory = Inventory(1)
        self.assertEqual(inventory.reserve("A", 1), "HELD")
        self.assertEqual(inventory.reserve("B", 1), "REJECTED")
        inventory.check()

    def test_release_once_and_no_late_payment_overwrite(self):
        inventory = Inventory(100)
        inventory.reserve("R", 3)
        self.assertTrue(inventory.finish("R", "RELEASED"))
        self.assertFalse(inventory.finish("R", "RELEASED"))
        with self.assertRaises(Conflict):
            inventory.finish("R", "PAID")
        self.assertEqual(inventory.available, 100)

    def test_same_key_changed_quantity(self):
        inventory = Inventory(10)
        inventory.reserve("R", 1)
        with self.assertRaises(Conflict):
            inventory.reserve("R", 2)
        self.assertEqual(inventory.available, 9)

    def test_seeded_sequential_conservation_walk(self):
        rng = random.Random(2026)
        inventory = Inventory(100)
        for i in range(400):
            key, qty = f"R-{i}", rng.randint(1, 7)
            state = inventory.reserve(key, qty)
            self.assertEqual(inventory.reserve(key, qty), state)
            if state == "HELD":
                outcome = rng.choice(["PAID", "RELEASED"])
                inventory.finish(key, outcome)
                self.assertFalse(inventory.finish(key, outcome))
            inventory.check()

    def test_invalid_quantity_no_effect(self):
        inventory = Inventory(10)
        for qty in (0, -1, True):
            with self.subTest(qty=qty), self.assertRaises(ValueError):
                inventory.reserve("R", qty)
        self.assertEqual(inventory.available, 10)


class LeaseTests(unittest.TestCase):
    def test_current_lease_cannot_be_stolen(self):
        r = LeaseResource()
        r.claim("A", 0, 10)
        with self.assertRaises(Conflict):
            r.claim("B", 9, 10)

    def test_expired_worker_rejected_after_takeover(self):
        r = LeaseResource()
        old = r.claim("A", 0, 10)
        new = r.claim("B", 10, 10)
        with self.assertRaises(Conflict):
            r.submit(old, 11, "old-result")
        self.assertTrue(r.submit(new, 11, "new-result"))
        self.assertFalse(r.submit(new, 12, "new-result"))
        self.assertEqual(r.writes, 1)
        self.assertEqual(r.result, "new-result")

    def test_expired_without_takeover_cannot_submit(self):
        r = LeaseResource()
        generation = r.claim("A", 0, 10)
        with self.assertRaises(Conflict):
            r.submit(generation, 10, "result")

    def test_completed_result_cannot_change(self):
        r = LeaseResource()
        generation = r.claim("A", 0, 10)
        r.submit(generation, 1, "result")
        with self.assertRaises(Conflict):
            r.submit(generation, 2, "different")
        with self.assertRaises(Conflict):
            r.claim("B", 20, 10)


class BudgetTests(unittest.TestCase):
    def test_unknown_keeps_reservation(self):
        ledger = BudgetLedger(100)
        ledger.reserve("K", 30)
        ledger.mark_unknown("K")
        self.assertEqual(ledger.held, 30)
        self.assertEqual(ledger.available, 70)

    def test_reserve_and_settle_idempotently(self):
        ledger = BudgetLedger(100)
        self.assertTrue(ledger.reserve("K", 30))
        self.assertFalse(ledger.reserve("K", 30))
        self.assertTrue(ledger.settle("K", 22))
        self.assertFalse(ledger.settle("K", 22))
        self.assertEqual((ledger.spent, ledger.held, ledger.available), (22, 0, 78))

    def test_changed_reservation_and_bill_conflict(self):
        ledger = BudgetLedger(100)
        ledger.reserve("K", 30)
        with self.assertRaises(Conflict):
            ledger.reserve("K", 31)
        ledger.settle("K", 22)
        with self.assertRaises(Conflict):
            ledger.settle("K", 23)

    def test_actual_overrun_is_recorded_not_hidden(self):
        ledger = BudgetLedger(100)
        ledger.reserve("K", 100)
        ledger.settle("K", 120)
        self.assertEqual(ledger.spent, 120)
        self.assertEqual(ledger.available, -20)
        self.assertTrue(ledger.snapshot()["overdrawn"])
        with self.assertRaises(Conflict):
            ledger.reserve("other", 1)

    def test_rejected_reservation_no_mutation(self):
        ledger = BudgetLedger(10)
        with self.assertRaises(Conflict):
            ledger.reserve("K", 11)
        self.assertEqual(ledger.operations, {})

    def test_exact_decimal(self):
        ledger = BudgetLedger("0.3")
        ledger.reserve("A", "0.1")
        ledger.reserve("B", "0.2")
        self.assertEqual(ledger.available, 0)


class QRTests(unittest.TestCase):
    def confirmed(self):
        q = QRRequest("browser-a", 100)
        q.advance("scan", 10, "browser-a")
        q.advance("confirm", 20, "browser-a")
        return q

    def test_exchange_before_expiry_once(self):
        q = self.confirmed()
        self.assertTrue(q.advance("exchange", 99, "browser-a"))
        self.assertFalse(q.advance("exchange", 101, "browser-a"))
        self.assertEqual(q.state, "EXCHANGED")
        self.assertEqual(q.exchange_count, 1)

    def test_exact_expiry_boundary(self):
        q = self.confirmed()
        self.assertFalse(q.advance("exchange", 100, "browser-a"))
        self.assertEqual(q.state, "EXPIRED")
        self.assertEqual(q.exchange_count, 0)

    def test_wrong_browser_and_missing_confirmation(self):
        q = self.confirmed()
        with self.assertRaises(Conflict):
            q.advance("exchange", 30, "browser-b")
        q = QRRequest("browser-a", 100)
        with self.assertRaises(Conflict):
            q.advance("exchange", 30, "browser-a")


class ExternalActionTests(unittest.TestCase):
    def test_not_found_is_still_unknown(self):
        record = ExternalAction("K")
        record.reconcile(None)
        self.assertEqual(record.state, "UNKNOWN")
        self.assertEqual(record.operation_key, "K")

    def test_unknown_routing_and_confirmed_receipt(self):
        record = ExternalAction("K")
        self.assertEqual(record.next_step(query_supported=False, idempotency_supported=False), "manual-reconciliation")
        self.assertIn("same-key", record.next_step(query_supported=False, idempotency_supported=True))
        self.assertIn("query", record.next_step(query_supported=True, idempotency_supported=True))
        record.reconcile("receipt-1")
        record.reconcile("receipt-1")
        self.assertEqual(record.next_step(query_supported=False, idempotency_supported=False), "reuse-confirmed-result")
        with self.assertRaises(Conflict):
            record.reconcile("receipt-2")


class TransferTests(unittest.TestCase):
    """Changed-condition examples reuse the same models and scenario source."""
    def test_window_change_of_order_not_identity(self):
        spec = load_scenarios()["window"]
        source = RecentProjection(3)
        received = RecentProjection(3, order="first_received")
        for raw in spec["events"]:
            source.apply(Event(**raw))
            received.apply(Event(**raw))
        scope = spec["scope"]
        self.assertEqual([e.sequence for e in source.snapshot(*scope)], [104, 103, 102])
        self.assertEqual([e.sequence for e in received.snapshot(*scope)], [99, 104, 102])
        self.assertFalse(received.apply(Event(**spec["events"][0])))
        self.assertEqual([e.sequence for e in received.snapshot(*scope)], [99, 104, 102])

    def test_order_mode_validation(self):
        with self.assertRaises(ValueError):
            RecentProjection(3, order="unknown")

    def test_queue_recovery_loses_capacity(self):
        cfg = deepcopy(load_scenarios()["workload"])
        self.assertEqual(fluid_queue(**load_scenarios()["queue"])["backlog"], 600)
        cfg["mean_seconds_per_call"] = 20
        result = capacity(cfg)
        self.assertEqual(result["ideal_capacity_per_second"], 15)
        self.assertEqual(result["model_calls_per_second"] - result["ideal_capacity_per_second"], 5)

    def test_tiered_storage_changed_retention(self):
        s = load_scenarios()["transfer"]["tiered_storage"]
        hot = Decimal(s["compressed_fraction"]) * s["daily_tb"] * s["hot_days"] * s["hot_copies"]
        archive = Decimal(s["compressed_fraction"]) * s["daily_tb"] * s["archive_days"] * s["archive_copies"]
        self.assertEqual((hot, archive, hot + archive), (105, 115, 220))

    def test_vector_generation_coexistence(self):
        s = load_scenarios()["transfer"]["vector_rebuild"]
        old = s["chunks"] * s["old_dimensions"] * s["bytes_per_dimension"]
        new = s["chunks"] * s["new_dimensions"] * s["bytes_per_dimension"]
        self.assertEqual((old, new, old + new), (4096000000, 8192000000, 12288000000))

    def test_budget_two_claimants_and_unknown(self):
        s = load_scenarios()["transfer"]["budget_competition"]
        ledger = BudgetLedger(s["limit"])
        ledger.reserve("earlier", s["prior_spent"])
        ledger.settle("earlier", s["prior_spent"])
        ledger.reserve("K", s["reserve_each"])
        with self.assertRaises(Conflict):
            ledger.reserve("L", s["reserve_each"])
        ledger.mark_unknown("K")
        self.assertEqual((ledger.spent, ledger.held, ledger.available), (20, 50, 30))
        ledger.settle("K", s["confirmed_k"])
        self.assertFalse(ledger.settle("K", s["confirmed_k"]))
        with self.assertRaises(Conflict):
            ledger.reserve("L", s["reserve_each"])
        self.assertEqual((ledger.spent, ledger.held, ledger.available), (55, 0, 45))
        self.assertNotIn("L", ledger.operations)

    def test_revenue_same_metric_after_refund(self):
        s = load_scenarios()["transfer"]["revenue"]
        previous = s["previous_a"] + s["previous_b"]
        current_b = s["current_gross_b"] - s["confirmed_refund_b"]
        current = s["current_net_a"] + current_b
        self.assertEqual((current_b, current), (250, 850))
        self.assertEqual(Decimal(current - previous) / previous, Decimal("-0.15"))

    def test_capstone_capacity_changes(self):
        s = load_scenarios()["transfer"]["capstone"]
        cfg = deepcopy(load_scenarios()["workload"])
        cfg["requests_per_second"]["create"] = s["normal_rate"]
        cfg["slots"] = s["slots"]
        cfg["mean_seconds_per_call"] = s["mean_seconds"]
        result = capacity(cfg)
        self.assertEqual((result["mean_inflight_calls"], result["ideal_capacity_per_second"]), (40, 12))
        queue = fluid_queue(s["normal_rate"], s["burst_rate"], result["ideal_capacity_per_second"], s["burst_seconds"])
        self.assertEqual((queue["backlog"], queue["net_drain_rate"], queue["drain_seconds"]), (120, 4, 30))
        cfg["mean_seconds_per_call"] = s["slow_seconds"]
        slow = capacity(cfg)
        self.assertEqual(slow["ideal_capacity_per_second"], 6)
        self.assertEqual(s["normal_rate"] - slow["ideal_capacity_per_second"], 2)

    def test_visible_interview_and_retained_teaching_columns(self):
        from pathlib import Path
        module = Path(__file__).resolve().parents[1]
        interview = (module / "interview" / "高频面试题.md").read_text(encoding="utf-8")
        self.assertEqual(interview.count("**参考回答**"), 38)
        self.assertNotIn("<details>", interview)
        for path in sorted((module / "docs").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                for marker in ("## 本章小结", "## 🎯", "## ⚠️", "## 本章自测"):
                    self.assertIn(marker, text)
                self.assertEqual(text.count("<details>"), text.count("</details>"))


if __name__ == "__main__":
    unittest.main()
