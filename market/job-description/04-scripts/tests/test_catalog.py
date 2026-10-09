"""Offline evidence/counter checks; model relevance decisions are supplied data."""
import copy
import hashlib
import unittest
import json
import tempfile
from pathlib import Path
from jd.catalog import counts, validate_catalog, render_catalog, load_catalog

class CatalogTests(unittest.TestCase):
    def fixture(self):
        body='职责：开发Agent服务。\n要求：在校生，Python。'
        job=dict(req_id='r1',title='工程实习',official_url='https://example.com/jobs/r1',full_text=body,
                 decision_reason='明确开发服务',official_type_evidence='实习，在校生',checked_at_utc='2026-10-09T00:00:00Z',
                 decision='include',review_depth='full_jd',recruitment_type='internship',official_recruitment_type='实习',
                 locations=['北京','上海'],body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                 engineering_evidence=['开发Agent服务'],role_track='应用与Agent核心研发')
        x=dict(companies=[dict(source_id='s1',company='公司',coverage={'coverage_level':'limited'},jobs=[job],other_observations=[])],
               historical_observations=[],snapshot={'checked_at_utc':'2026-10-09'})
        x['counts']=counts(x)
        return x
    def write_split_fixture(self, directory):
        original=self.fixture(); current=copy.deepcopy(original)
        support={'schema_version':1,'snapshot':current['snapshot'],'companies':[{'source_id':c['source_id'],'other_observations':c.pop('other_observations')} for c in current['companies']],'historical_observations':current.pop('historical_observations')}
        raw=json.dumps(support).encode();path=Path(directory)/'official-jds.json'
        (path.parent/'source-observations.json').write_bytes(raw)
        current['supporting_observations']={'path':'source-observations.json','bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
        path.write_text(json.dumps(current));return path,original
    def test_two_files_reconstruct_the_exact_reviewed_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            path,original=self.write_split_fixture(directory)
            self.assertEqual(load_catalog(path),original)
    def test_changed_support_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path,_=self.write_split_fixture(directory)
            support=path.parent/'source-observations.json';support.write_bytes(support.read_bytes()+b' ')
            with self.assertRaisesRegex(ValueError,'hash or size'):load_catalog(path)
    def test_valid_partial_coverage_and_all_locations(self):
        x=self.fixture();self.assertEqual(validate_catalog(x,['s1']),[])
        self.assertIn('北京、上海',render_catalog(x));self.assertEqual(x['counts']['coverage']['limited'],1)
    def test_index_columns_match_and_keep_cohort(self):
        x=self.fixture();x['companies'][0]['jobs'][0]['cohort']='2028届及以后'
        rows=[line for line in render_catalog(x).splitlines() if line.startswith('|')]
        self.assertTrue(all(len(line.split('|'))==7 for line in rows))
        self.assertIn('毕业/学历范围',rows[0]);self.assertIn('2028届及以后',rows[-1])
    def test_source_access_parameter_is_not_published(self):
        x=self.fixture();x['companies'][0]['jobs'][0]['official_url']+='?sourceToken=fixture-not-a-secret'
        self.assertTrue(any('source access parameter' in e for e in validate_catalog(x,['s1'])))
    def test_modified_source_and_untraceable_quote_fail(self):
        x=self.fixture();x['companies'][0]['jobs'][0]['full_text']='替换正文'
        errors=validate_catalog(x,['s1']);self.assertTrue(any('hash mismatch' in e for e in errors));self.assertTrue(any('verbatim' in e for e in errors))
    def test_duplicate_real_requisition_rejected(self):
        x=self.fixture();x['companies'][0]['jobs']*=2;x['counts']=counts(x)
        self.assertTrue(any('duplicate requisition' in e for e in validate_catalog(x,['s1'])))
    def test_unreviewed_candidate_cannot_be_current(self):
        x=self.fixture();x['companies'][0]['jobs'][0]['review_depth']='listing_responsibilities'
        self.assertTrue(any('full-JD' in e for e in validate_catalog(x,['s1'])))
    def test_history_never_in_current_count(self):
        x=self.fixture();x['historical_observations']=[{'status':'historical','current_pool_eligible':False}];x['counts']=counts(x)
        self.assertEqual(x['counts']['current_jobs'],1);self.assertEqual(validate_catalog(x,['s1']),[])
        x['historical_observations'][0]['current_pool_eligible']=True
        self.assertTrue(validate_catalog(x,['s1']))
    def test_registry_and_counts_cannot_silently_drift(self):
        x=self.fixture();self.assertTrue(validate_catalog(x,['s1','s2']))
        x['counts']['current_jobs']=9;self.assertTrue(validate_catalog(x,['s1']))
if __name__=='__main__':unittest.main()
