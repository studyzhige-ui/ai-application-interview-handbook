"""Run with unittest; no pytest or service dependency is required."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import json
import math
import re
import unittest
import numeric_lab as lab

class NumericTests(unittest.TestCase):
    def setUp(self):
        self.data = lab.load_data()
    def ids(self, result): return [r['id'] for r in result]
    def test_same_fixture_as_text(self):
        rows = self.data['records']
        q = self.data['query']
        self.assertEqual(self.ids(lab.exact_search(rows,q,3)), ['A','C','F'])
        self.assertEqual(self.ids(lab.exact_search(rows,q,3,tenant='alpha')), ['A','C','D'])
    def test_cosine_ties(self):
        self.assertEqual(self.ids(lab.exact_search(self.data['records'],[1,0],3,'cosine')), ['A','B','C'])
    def test_inner_product_norm(self):
        self.assertEqual(self.ids(lab.exact_search(self.data['records'],[1,0],2,'ip')), ['B','A'])
    def test_mismatched_dimensions(self):
        with self.assertRaises(ValueError): lab.measure([1,2],[1])
    def test_nonfinite(self):
        for value in (float('nan'),float('inf'),-float('inf')):
            with self.subTest(value=value), self.assertRaises(ValueError): lab.measure([1,value],[1,2])
    def test_zero_cosine(self):
        with self.assertRaises(ValueError): lab.measure([0,0],[1,0],'cosine')
        self.assertEqual(lab.measure([0,0],[1,0]),1)
    def test_empty_vector(self):
        with self.assertRaises(ValueError): lab.measure([],[])
    def test_invalid_metric(self):
        with self.assertRaises(ValueError): lab.measure([1],[1],'unknown')
    def test_invalid_k(self):
        for k in (0,-1,1.5,True):
            with self.subTest(k=k), self.assertRaises(ValueError): lab.exact_search([], [1,0], k)
    def test_less_than_k(self):
        self.assertEqual(len(lab.exact_search(self.data['records'],[1,0],20,tenant='alpha')),4)
    def test_empty_eligible(self):
        self.assertEqual(lab.exact_search(self.data['records'],[1,0],3,tenant='none'),[])
        self.assertIsNone(lab.recall_at_k([],[],3))
    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError): lab.exact_search([self.data['records'][0]]*2,[1,0],3)
    def test_recall_duplicates_do_not_add_credit(self):
        self.assertAlmostEqual(lab.recall_at_k(['A','C','C'],['A','C','D'],4),2/3)
    def test_oversized_pool_not_final_recall(self):
        self.assertEqual(lab.recall_at_k(['X','Y','Z','A'],['A'],3),0)
    def test_bad_gold(self):
        with self.assertRaises(ValueError): lab.recall_at_k([],['A','A'],3)
    def test_unit_vector_relation(self):
        a,b=(.6,.8),(0.,1.)
        self.assertAlmostEqual(lab.measure(a,b),2-2*lab.measure(a,b,'ip'))
    def test_graph_candidate_process(self):
        self.assertEqual(lab.graph_width_demo(1)['winner'],'A')
        self.assertEqual(lab.graph_width_demo(2)['winner'],'T')
        self.assertNotIn('T',lab.graph_width_demo(1)['seen'])
    def test_graph_new_condition(self):
        self.assertEqual(lab.graph_width_demo(1,7)['winner'],'A')
        self.assertEqual(lab.graph_width_demo(2,7)['winner'],'A')
    def test_ivf_boundary(self):
        self.assertEqual(lab.ivf_boundary_demo(4.9,1),4)
        self.assertEqual(lab.ivf_boundary_demo(4.9,2),5.1)
    def test_ivf_new_condition(self):
        self.assertEqual(lab.ivf_boundary_demo(4.2,1),4)
        self.assertEqual(lab.ivf_boundary_demo(4.2,2),4)
    def test_pq_original_vs_approx(self):
        result=lab.pq_demo()
        self.assertAlmostEqual(result['adc'],.30)
        self.assertAlmostEqual(result['original_distance'],.15)
        self.assertAlmostEqual(lab.pq_demo((1,0))['adc'],2.30)
    def test_codebook_amortization(self):
        codebook_bytes=2*256*4*4
        self.assertEqual(codebook_bytes,8192)
        self.assertGreater(2+codebook_bytes,32)
        self.assertLess(1000*2+codebook_bytes,1000*32)
    def test_ordered_deletion(self):
        state=lab.VersionedState()
        self.assertTrue(state.apply(lab.Event('D',8,None)))
        self.assertFalse(state.apply(lab.Event('D',7,'old')))
        self.assertIsNone(state.visible('D'))
    def test_idempotent_replay_and_newer_event(self):
        state=lab.VersionedState();event=lab.Event('D',8,None)
        state.apply(event)
        self.assertFalse(state.apply(event))
        self.assertTrue(state.apply(lab.Event('D',9,'authorized new version')))
    def test_same_version_conflict(self):
        state=lab.VersionedState();state.apply(lab.Event('D',8,None))
        with self.assertRaises(ValueError): state.apply(lab.Event('D',8,'different'))
    def test_chapter_two_code_extracted(self):
        text=(Path(__file__).parents[1]/'docs/02-VectorSpace与Similarity.md').read_text(encoding='utf-8')
        blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
        self.assertEqual(len(blocks),1)
        out=StringIO()
        with redirect_stdout(out): exec(compile(blocks[0],'<chapter02>','exec'),{})
        self.assertEqual(out.getvalue().strip(),'A 1.0 1.0 0.0\nB 10.0 1.0 81.0\nC 0.8 0.8 0.4')
    def test_chapter_three_code_extracted(self):
        text=(Path(__file__).parents[1]/'docs/03-ExactSearch与ANN.md').read_text(encoding='utf-8')
        blocks=re.findall(r'^```python\n(.*?)^```',text,re.M|re.S)
        self.assertEqual(len(blocks),1)
        out=StringIO()
        with redirect_stdout(out): exec(compile(blocks[0],'<chapter03>','exec'),{})
        self.assertEqual(out.getvalue().strip(),'0.667')
    def test_review_capacity(self):
        original=10_000_000*768*4/2**30
        self.assertAlmostEqual(original+5+5+3,41.61,places=2)
        self.assertAlmostEqual(original*2+5+5+3,70.22,places=2)
    def test_review_query_scaling(self):
        # Query-only unit normalization scales all IP scores by same positive factor.
        before=[lab.measure([0,2],r['vector'],'ip') for r in self.data['records']]
        after=[lab.measure([0,1],r['vector'],'ip') for r in self.data['records']]
        self.assertEqual(before,[2*x for x in after])
    def test_run_is_serializable(self):
        result=lab.run()
        self.assertEqual(result['cosine_postfiltered'],['A','C'])
        self.assertFalse(result['stale_write_after_delete_accepted'])
        json.dumps(result)

if __name__=='__main__': unittest.main(verbosity=2)
