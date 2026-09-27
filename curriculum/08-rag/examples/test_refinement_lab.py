"""Deterministic tests, including the actual chapter 07 Markdown table."""
from dataclasses import asdict, FrozenInstanceError
from pathlib import Path
import unittest

from refinement_lab import (Generation, Publication, advance_contiguous, bind_request,
                            bm25_term_weight, demo, publish, support_gaps)

DOCS = Path(__file__).resolve().parents[1] / "docs"


class BM25Checks(unittest.TestCase):
    def test_numbers_match_actual_markdown_table(self):
        text = (DOCS / "07-RetrievalStack.md").read_text(encoding="utf-8")
        table = text.split("<!-- refinement-table: bm25-saturation -->", 1)[1]
        table = table.lstrip().split("\n\n", 1)[0]
        values = []
        for line in table.splitlines():
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if cells and cells[0].isdigit():
                values.append((int(cells[0]), float(cells[-1])))
        self.assertEqual([tf for tf, _ in values], [1, 2, 4, 8])
        for tf, expected in values:
            self.assertAlmostEqual(bm25_term_weight(tf, 100, 100), expected, places=6)

    def test_diminishing_marginal_gain(self):
        scores = [bm25_term_weight(tf, 100, 100) for tf in range(1, 9)]
        gains = [right - left for left, right in zip(scores, scores[1:])]
        self.assertTrue(all(g > 0 for g in gains))
        self.assertTrue(all(a > b for a, b in zip(gains, gains[1:])))

    def test_length_normalization(self):
        self.assertAlmostEqual(bm25_term_weight(1, 200, 100), 2.2 / 3.1)

    def test_zero_frequency(self):
        self.assertEqual(bm25_term_weight(0, 100, 100), 0)

    def test_invalid_inputs(self):
        for args in [(True, 100, 100), (-1, 100, 100), (101, 100, 100),
                     (1, 0, 100), (1, 100, float("nan")), (1, 100, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                bm25_term_weight(*args)
        for kwargs in [{"k1": 0}, {"b": 2}, {"idf": float("inf")}, {"idf": -1}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                bm25_term_weight(1, 100, 100, **kwargs)


class SupportChecks(unittest.TestCase):
    def test_unchecked_condition_is_gap_without_known_exception_id(self):
        self.assertEqual(support_gaps(["product", "time", "resource_status"],
                                     {"product": "supported", "time": "supported"}),
                         ["resource_status"])

    def test_supported_is_only_a_supplied_judgment(self):
        self.assertEqual(support_gaps(["resource_status"], {"resource_status": "supported"}), [])

    def test_conflict_remains_gap(self):
        self.assertEqual(support_gaps(["x"], {"x": "conflict"}), ["x"])

    def test_invalid_judgments(self):
        for conditions, judgments in [("x", {}), (["x", "x"], {}), ([""], {}),
                                      (["x"], {"y": "supported"}), (["x"], {"x": "maybe"})]:
            with self.subTest(conditions=conditions), self.assertRaises(ValueError):
                support_gaps(conditions, judgments)


class PublicationChecks(unittest.TestCase):
    def setUp(self):
        self.g1 = Generation("g1", "e1", "v1", "s1", "c1")
        self.g2 = Generation("g2", "e2", "v2", "s2", "c2")
        self.current = Publication()
        self.arguments = dict(expected_revision=7, target=self.g2, boundary=103,
                              applied_through=103, dispatch_paused=True,
                              in_flight=0, resources_ready=True)

    def test_bundle_remains_bound_to_old_request(self):
        generations = {"g1": self.g1, "g2": self.g2}
        q1 = bind_request(self.current, generations)
        after = publish(self.current, **self.arguments)
        self.assertEqual(q1.content_store, "c1")
        self.assertEqual(bind_request(after, generations).content_store, "c2")
        with self.assertRaises(FrozenInstanceError):
            q1.content_store = "c2"

    def test_record_updates_query_and_dispatch_target_together(self):
        after = publish(self.current, **self.arguments)
        self.assertEqual((after.active, after.write_target, after.boundary, after.release_revision),
                         ("g2", "g2", 103, 8))
        self.assertEqual(self.current.active, "g1")

    def test_sequence_seen_is_not_contiguous_completion(self):
        self.assertEqual(advance_contiguous(100, [102, 103]), 100)
        self.assertEqual(advance_contiguous(100, [103, 101, 102]), 103)
        self.assertEqual(advance_contiguous(103, [103, 104, 104, 106]), 104)

    def test_gap_blocks_publication(self):
        self.arguments["applied_through"] = advance_contiguous(100, [102, 103])
        with self.assertRaises(ValueError):
            publish(self.current, **self.arguments)

    def test_stale_publication_rejected(self):
        after = publish(self.current, **self.arguments)
        with self.assertRaises(ValueError):
            publish(after, **self.arguments)

    def test_unsettled_or_unready_blocks_publication(self):
        for changes in [{"dispatch_paused": False}, {"in_flight": 1}, {"resources_ready": False},
                        {"dispatch_paused": 1}, {"boundary": 99}]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                publish(self.current, **(self.arguments | changes))

    def test_recovery_decision_after_commit_sends_104_to_g2(self):
        after = publish(self.current, **self.arguments)
        recovered = Publication(**asdict(after))
        self.assertEqual(recovered.write_target, "g2")
        self.assertEqual(advance_contiguous(recovered.boundary, [104]), 104)

    def test_before_commit_old_record_sends_104_to_g1(self):
        recovered = Publication(**asdict(self.current))
        self.assertEqual(recovered.write_target, "g1")

    def test_incomplete_bundle_rejected(self):
        self.arguments["target"] = Generation("g2", "e2", "v2", "s2", "")
        with self.assertRaises(ValueError):
            publish(self.current, **self.arguments)

    def test_unknown_generation_not_silently_substituted(self):
        with self.assertRaises(KeyError):
            bind_request(Publication(active="missing"), {"g1": self.g1})

    def test_invalid_sequence(self):
        for args in [(100, [True]), (100, [-1]), (-1, [1])]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                advance_contiguous(*args)

    def test_demo_identifies_its_limits(self):
        result = demo()
        self.assertTrue(result["simulation_only"])
        self.assertTrue(result["support_judgments_are_manual"])
        self.assertEqual(result["online_gaps"], ["resource_status"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
