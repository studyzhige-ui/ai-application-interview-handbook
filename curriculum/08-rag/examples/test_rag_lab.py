"""Run with: python -m unittest discover -s curriculum/08-rag/examples -v"""
import contextlib
import io
import json
import math
import re
import unittest
from pathlib import Path

from rag_lab import (AccessPolicy, BAD_RERANK_FIXTURE, CHUNKS, Chunk,
                     DENSE_FIXTURE, LEXICAL_FIXTURE, REQUIRED_EVIDENCE,
                     RevisionLedger, authorized_chunks, greedy_pack, main,
                     ndcg, retrieval_metrics, rrf, validate_citation_ids, window_spans)


class MechanismTests(unittest.TestCase):
    def test_window_worked_example(self):
        spans = window_spans(1000, 200, 50)
        self.assertEqual(len(spans), 7)
        self.assertEqual(sum(b-a for a, b in spans), 1300)
        self.assertEqual(spans[-1], (900, 1000))

    def test_window_transfer(self):
        self.assertEqual(window_spans(850, 300, 100), [(0, 300), (200, 500), (400, 700), (600, 850)])

    def test_window_empty_small_and_exact(self):
        self.assertEqual(window_spans(0, 100, 0), [])
        self.assertEqual(window_spans(50, 100, 10), [(0, 50)])
        self.assertEqual(window_spans(200, 100, 0), [(0, 100), (100, 200)])

    def test_window_invalid_parameters(self):
        for args in [(-1, 2, 0), (2, 0, 0), (2, 2, -1), (2, 2, 2), (2, 2, 3), (True, 2, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                window_spans(*args)

    def test_rrf_fixture(self):
        scores = rrf([DENSE_FIXTURE, LEXICAL_FIXTURE])
        self.assertEqual([x[0] for x in scores], ["A", "B", "C", "D"])
        self.assertAlmostEqual(dict(scores)["A"], 1/61 + 1/62)
        self.assertAlmostEqual(dict(scores)["B"], 1/61 + 1/63)

    def test_rrf_missing_zero_and_tie(self):
        self.assertEqual(rrf([["B"], ["A"]], constant=1), [("A", .5), ("B", .5)])
        self.assertEqual(rrf([]), [])
        self.assertEqual(rrf([[], ["X"]], constant=0), [("X", 1.)])

    def test_rrf_rejects_duplicate_route_ids(self):
        with self.assertRaises(ValueError):
            rrf([["A", "A"]])

    def test_rrf_invalid_constants(self):
        for value in [-1, math.inf, math.nan, True, "60"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                rrf([["A"]], constant=value)

    def test_metrics_partial_coverage(self):
        self.assertEqual(retrieval_metrics(["A", "C", "B"], REQUIRED_EVIDENCE, 2),
                         {"recall": .5, "precision": .5, "hit": 1., "rr": 1., "complete": 0.})

    def test_metrics_full_coverage(self):
        m = retrieval_metrics(["A", "B"], REQUIRED_EVIDENCE, 2)
        self.assertTrue(all(value == 1 for value in m.values()))

    def test_metrics_short_list_fixed_denominator(self):
        self.assertEqual(retrieval_metrics(["A"], {"A"}, 5)["precision"], .2)

    def test_metrics_no_hit_and_empty_ranking(self):
        self.assertTrue(all(x == 0 for x in retrieval_metrics([], {"A"}, 2).values()))
        self.assertEqual(retrieval_metrics(["D", "C", "A"], {"A"}, 2)["rr"], 0.)

    def test_metrics_empty_relevance_not_applicable(self):
        self.assertTrue(all(x is None for x in retrieval_metrics(["A"], set(), 2).values()))

    def test_metrics_duplicate_and_k_errors(self):
        for ranking, k in [(["A", "A"], 2), (["A"], 0), ("A", 1)]:
            with self.subTest(ranking=ranking, k=k), self.assertRaises(ValueError):
                retrieval_metrics(ranking, {"A"}, k)

    def test_reciprocal_rank_is_first_relevant_only(self):
        self.assertEqual(retrieval_metrics(["C", "A", "B"], REQUIRED_EVIDENCE, 3)["rr"], .5)

    def test_ndcg_worked_example(self):
        self.assertAlmostEqual(ndcg(["C", "A", "B"], {"B": 2, "A": 1, "C": 0}, 3), .58688267143572)

    def test_ndcg_ideal_uses_unretrieved_labels(self):
        self.assertLess(ndcg(["A"], {"A": 1, "B": 2}, 1), 1)
        self.assertEqual(ndcg(["B", "A"], {"A": 1, "B": 2}, 2), 1.)

    def test_ndcg_empty_and_negative(self):
        self.assertIsNone(ndcg(["A"], {"A": 0}, 1))
        with self.assertRaises(ValueError):
            ndcg(["A"], {"A": -1}, 1)

    def test_citation_membership_only(self):
        self.assertIsNone(validate_citation_ids(["E1", "E2"], {"E1", "E2"}))
        with self.assertRaises(ValueError):
            validate_citation_ids(["E3"], {"E1", "E2"})
        with self.assertRaises(ValueError):
            validate_citation_ids("E1", {"E1"})

    def test_early_topk_loses_exception(self):
        self.assertEqual(greedy_pack(BAD_RERANK_FIXTURE[:2], CHUNKS, 110), ["A"])
        self.assertEqual(greedy_pack(BAD_RERANK_FIXTURE, CHUNKS, 110), ["A", "B"])

    def test_greedy_is_not_a_coverage_solver(self):
        self.assertEqual(greedy_pack(["C", "D", "A", "B"], CHUNKS, 110), ["C", "D"])
        self.assertEqual(greedy_pack(["A"], CHUNKS, 0), [])
        with self.assertRaises(ValueError):
            greedy_pack(["A"], CHUNKS, -1)

    def test_revision_late_tasks_and_delete(self):
        ledger = RevisionLedger()
        self.assertEqual(ledger.apply("P1", 8, "eight"), "accepted")
        self.assertEqual(ledger.apply("P1", 7, "seven"), "stale")
        self.assertEqual(ledger.apply("P1", 9, None), "accepted")
        self.assertEqual(ledger.apply("P1", 8, "eight"), "stale")
        self.assertIsNone(ledger.events["P1"].content)
        self.assertEqual(ledger.events["P1"].revision, 9)

    def test_revision_duplicate_and_conflict(self):
        ledger = RevisionLedger()
        ledger.apply("P1", 1, "one")
        self.assertEqual(ledger.apply("P1", 1, "one"), "duplicate")
        with self.assertRaises(ValueError):
            ledger.apply("P1", 1, "conflicting")

    def test_revision_independent_documents(self):
        ledger = RevisionLedger()
        ledger.apply("P1", 10, "ten")
        self.assertEqual(ledger.apply("P2", 1, "one"), "accepted")

    def test_revision_invalid(self):
        with self.assertRaises(ValueError):
            RevisionLedger().apply("P1", 0, "bad")

    def test_rollback_obeys_current_revoke(self):
        old_generation = list(CHUNKS.values())
        before = AccessPolicy("beichen", 1, frozenset({"P1", "P2", "P3"}))
        after = AccessPolicy("beichen", 2, frozenset({"P2", "P3"}))
        self.assertEqual(len(authorized_chunks(old_generation, before)), 4)
        self.assertEqual([c.id for c in authorized_chunks(old_generation, after)], ["C", "D"])

    def test_tombstone_blocks_old_generation(self):
        policy = AccessPolicy("beichen", 3, frozenset({"P1", "P2"}), frozenset({"P1"}))
        self.assertEqual([c.id for c in authorized_chunks(list(CHUNKS.values()), policy)], ["C"])

    def test_tenant_is_not_granted_by_document_id(self):
        foreign = Chunk("Z", "P1", "v2", "foreign", "private", 10)
        policy = AccessPolicy("beichen", 1, frozenset({"P1"}))
        self.assertEqual(authorized_chunks([foreign], policy), [])

    def test_policy_recheck_after_expansion(self):
        policy = AccessPolicy("beichen", 2, frozenset({"P2"}))
        self.assertFalse(policy.allows(CHUNKS["B"]))
        self.assertTrue(policy.allows(CHUNKS["C"]))

    def test_demo_matches_shared_data(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main()
        result = json.loads(output.getvalue())
        self.assertEqual(result["fused"], ["A", "B", "C", "D"])
        self.assertEqual(result["revision_timeline"], ["accepted", "stale", "accepted", "stale"])
        self.assertTrue(result["simulation_only"])

    def test_all_main_text_python_snippets(self):
        """Execute the ACTUAL chapter snippets, not manually maintained copies."""
        docs = Path(__file__).resolve().parents[1] / "docs"
        self.assertTrue(docs.is_dir())
        snippets = [(p, code) for p in sorted(docs.glob("*.md"))
                    for code in re.findall(r"```python\n(.*?)```", p.read_text(encoding="utf-8"), re.S)]
        self.assertGreater(len(snippets), 0)
        for p, code in snippets:
            with self.subTest(chapter=p.name):
                exec(compile(code, str(p), "exec"), {"__name__": "__chapter_example__"})


if __name__ == "__main__":
    unittest.main()
