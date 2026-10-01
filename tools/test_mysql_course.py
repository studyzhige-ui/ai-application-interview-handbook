"""Static/tooling checks, NOT MySQL grammar or server behavior validation."""
import ast
import importlib.util
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'curriculum/03-mysql'
EX = MOD / 'examples'
sys.path.insert(0, str(EX))
import mysql_course
import mysql_runtime_checks

REQUIRED = ['## 本章小结', '## 🎯 面试怎么回答', '## ⚠️ 易错点', '## 本章自测', '## 知识回看与权威资料']

class ChapterChecks(unittest.TestCase):
    """Check only explicit structural invariants; not ease of understanding."""

for path in sorted((MOD/'docs').glob('*.md')):
    def check(self, path=path):
        text = path.read_text(encoding='utf-8')
        self.assertEqual(len(re.findall(r'^# ',text,re.M)),1)
        positions = [text.index(h) for h in REQUIRED]
        self.assertEqual(positions, sorted(positions))
        self.assertGreater(len(text.split('## ',1)[0]), 120)
        self.assertEqual(text.count('<details>'),text.count('</details>'))
        self.assertEqual(text.count('<summary>'),text.count('</summary>'))
        self.assertNotRegex(text, r'<details\s+open')
        self.assertEqual(text.count('```')%2,0)
        quiz = text[text.index('## 本章自测'):text.index('## 知识回看与权威资料')]
        self.assertGreaterEqual(quiz.count('<details>'),1)
        self.assertIn('> ⚠️',text)
        self.assertRegex(text, r'https://(?:dev\.mysql\.com|redis\.io|learn\.microsoft\.com)/')
        # Every internal chapter navigation must point to an existing file.
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http:', 'https:', '#')):
                continue
            resolved=(path.parent/target.split('#',1)[0]).resolve()
            # The review bundle is not the entire repo. This one external-to-bundle
            # target was read at the fixed repo snapshot; do not fabricate its content.
            known_repo_targets={'market/interviews/batch-32.md', 'curriculum/04-redis/README.md'}
            self.assertTrue(resolved.exists() or resolved.relative_to(ROOT).as_posix() in known_repo_targets,f'{path.name}: {target}')
    setattr(ChapterChecks, 'test_chapter_'+path.name[:2],check)

class SQLExtractionChecks(unittest.TestCase):
    def test_source_ids_are_portable_repository_paths(self):
        posix = mysql_course.relative_source_id(PurePosixPath('/course/docs/01-SQL.md'), PurePosixPath('/course'))
        windows = mysql_course.relative_source_id(PureWindowsPath('C:/course/docs/01-SQL.md'), PureWindowsPath('C:/course'))
        self.assertEqual(posix, 'docs/01-SQL.md')
        self.assertEqual(windows, posix)
        self.assertTrue(all(chr(92) not in item['file'] for item in mysql_course.examples().values()))

    def test_named_blocks_unique(self):
        items=mysql_course.examples()
        retained=json.loads((ROOT/'guide/project/mysql-sql-source-map-2026-09-27.json').read_text())['retained_previous_names']
        self.assertTrue(set(retained).issubset(items))
        self.assertEqual(len(items),len(set(items)))
        self.assertTrue(all(mysql_course.split_sql(x['code']) for x in items.values()))
    def test_both_marker_forms(self):
        items=mysql_course.examples()
        self.assertIn('environment',items)
        self.assertIn('isolation_rr_begin',items)
    def test_quoted_semicolons(self):
        self.assertEqual(mysql_course.split_sql("SELECT 'a;b'; SELECT `x;y`;"),["SELECT 'a;b'","SELECT `x;y`"])
    def test_doubled_quote(self):
        self.assertEqual(mysql_course.split_sql("SELECT 'it''s;a';"),["SELECT 'it''s;a'"])
    def test_backslash_escape(self):
        self.assertEqual(mysql_course.split_sql(r"SELECT 'it\'s;a';"),[r"SELECT 'it\'s;a'"])
    def test_comments(self):
        self.assertEqual(mysql_course.split_sql('-- note;\nSELECT 1; # other;\n/* ; */ SELECT 2;'),['SELECT 1','SELECT 2'])
    def test_invalid_open_quote(self):
        with self.assertRaises(ValueError):mysql_course.split_sql("SELECT 'not closed")
    def test_invalid_open_comment(self):
        with self.assertRaises(ValueError):mysql_course.split_sql('/* not closed')
    def test_export_without_server(self):
        proc=subprocess.run([sys.executable,str(ROOT/'tools/export_mysql_example.py'),'filter_tasks'],capture_output=True,text=True)
        self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertIn("WHERE tenant_id = 10",proc.stdout)
    def test_export_unknown_fails(self):
        proc=subprocess.run([sys.executable,str(ROOT/'tools/export_mysql_example.py'),'unknown_example'],capture_output=True,text=True)
        self.assertNotEqual(proc.returncode,0)

class DeliveryContracts(unittest.TestCase):
    def test_python_syntax_only(self):
        for path in [*EX.glob('*.py'),ROOT/'tools/export_mysql_example.py']:
            ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    def test_engine_cases_are_prepared_not_run(self):
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(mysql_runtime_checks.MySQLChecks)
        self.assertEqual(suite.countTestCases(),43)
        self.assertIsNone(mysql_runtime_checks.CONFIG)
        self.assertIsNone(mysql_runtime_checks.PYMYSQL)
    def test_engine_case_dependencies_exist(self):
        items=mysql_course.examples()
        for name,(setups,expected) in mysql_runtime_checks.CASES.items():
            self.assertIn(name,items)
            for setup in setups:self.assertIn(setup,items)
            self.assertIsInstance(expected,list)
        # Literal block() references elsewhere in the runner also exist in the prose.
        source=(EX/'mysql_runtime_checks.py').read_text()
        for name in re.findall(r'block\([^,]+,\s*"([a-z0-9_]+)"\)',source):
            self.assertIn(name,items)
    def test_reset_requires_explicit_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc=subprocess.run([sys.executable,str(EX/'mysql_runtime_checks.py')],cwd=tmp,capture_output=True,text=True)
            self.assertNotEqual(proc.returncode,0)
            self.assertIn('--confirm-reset',proc.stderr)
            self.assertFalse((Path(tmp)/'mysql-runtime-result.json').exists())
    def test_seed_drops_only_named_course_tables(self):
        source=(EX/'seed.sql').read_text()
        drops=re.findall(r'^DROP TABLE IF EXISTS ([\w.]+);',source,re.M)
        self.assertEqual(len(drops),10)
        self.assertTrue(all(x.startswith('handbook_mysql_lab.') for x in drops))
        self.assertNotIn('DROP DATABASE',source)
        self.assertNotRegex(source,r'(?i)SET\s+GLOBAL')
    def test_seed_exact_initial_values(self):
        source=(EX/'seed.sql').read_text()
        self.assertIn("(1,100,0),(2,100,0)",source)
        self.assertIn("VALUES (10),(20),(30)",source)
        self.assertIn("(4,10,NULL,'写周报','pending',1,'2026-09-02 10:00:00')",source)
    def test_container_local_binding(self):
        source=(EX/'compose.yaml').read_text()
        self.assertIn('127.0.0.1:3307:3306',source)
        self.assertIn('mysql:9.7.3',source)
        self.assertNotIn('privileged:',source)
    def test_environment_file_ignored(self):
        self.assertIn('.env',(EX/'.gitignore').read_text().splitlines())
        self.assertFalse((EX/'.env').exists())
    def test_canonical_mapping_and_frequencies_unchanged(self):
        data=json.loads((ROOT/'guide/project/mysql-evidence-map-2026-09-27.json').read_text())
        rows=data['canonical_topics']
        self.assertEqual(len(rows),26)
        self.assertEqual(len({s for r in rows for s in r['sources']}),55)
        self.assertEqual([r['source'] for r in data['new_source_review']],[f'S{i}' for i in range(280,298)])
        byid={r['qid']:r for r in rows}
        self.assertEqual(byid['MYSQL-025']['chapter'],4)
        self.assertEqual(byid['MYSQL-026']['chapter'],9)
        self.assertEqual(byid['MYSQL-028']['chapter'],14)
        for row in rows:self.assertTrue((ROOT/row['path']).is_file())
        self.assertNotIn('MYSQL-001',byid)
        self.assertNotIn('MYSQL-023',byid)
    def test_reader_navigation_follows_approved_order(self):
        source=(MOD/'README.md').read_text()
        self.assertIn('[← FastAPI](../02-fastapi/README.md)',source)
        self.assertIn('[Redis →](../04-redis/README.md)',source)
    def test_review_and_interview_survive(self):
        review=(MOD/'review/README.md').read_text()
        self.assertGreaterEqual(review.count('<details>'),20)
        self.assertGreaterEqual(review.count('```text'),4)
        questions=(MOD/'interview/高频面试题.md').read_text()
        self.assertEqual(len(re.findall(r'^## \d+',questions,re.M)),31)
        self.assertNotIn('<details>',questions)
        pitfalls=(MOD/'interview/面试易错点.md').read_text()
        self.assertEqual(len(re.findall(r'^> ⚠️',pitfalls,re.M)),40)
    def test_first_writing_has_explicit_reading_and_commit_context(self):
        first=next((MOD/'docs').glob('01-*.md')).read_text()
        second=next((MOD/'docs').glob('02-*.md')).read_text()
        self.assertIn('下一章会给出建表与状态变化',first)
        self.assertIn('自动提交',first)
        self.assertLess(second.index('basics_create'),second.index('basics_insert'))
        self.assertIn('不作为阅读', (EX/'README.md').read_text())
    def test_all_payload_json_parses(self):
        for path in ROOT.rglob('*.json'):json.loads(path.read_text(encoding='utf-8'))
    def test_exporter_scope_excludes_global_stats_and_other_modules(self):
        # This suite runs in the full handbook, not an isolated delivery bundle.
        # Assert the exported payload boundary instead of deleting valid modules.
        result = subprocess.run([sys.executable, str(ROOT/'tools/export_mysql_example.py'), '--list'],
                                check=True, capture_output=True, text=True)
        rows = [line.split('\t', 1) for line in result.stdout.splitlines()]
        self.assertEqual({name for name, _ in rows}, set(mysql_course.examples()))
        self.assertTrue(all(path.startswith(('docs/', 'examples/')) for _, path in rows))
        self.assertTrue(all((MOD/path).is_file() for _, path in rows))

class HandCalculationChecks(unittest.TestCase):
    """Plain Python hand-calculation consistency, NOT a SQL/lock simulator."""
    def test_cost_example_dimensions(self):
        self.assertEqual(2100-800+50,1350)
    def test_tree_example_capacity(self):
        self.assertEqual(100**2*100,1000000)
    def test_reference_query_and_second_page(self):
        # Small literal fixture used only to cross-check the printed ID lists.
        rows=[(1,10,'pending',2,1),(2,10,'done',1,2),(3,10,'pending',3,3),
              (4,10,'pending',1,4),(5,20,'pending',2,5),(6,10,'done',2,6)]
        self.assertEqual([i for i,t,s,p,d in rows if t==10 and s=='pending'],[1,3,4])
        descending=sorted([r for r in rows if r[1]==10],key=lambda r:r[4],reverse=True)
        self.assertEqual([r[0] for r in descending[2:4]],[3,2])
        self.assertEqual(sum(1 for r in rows if r[1]==10 and r[2]=='done'),2)


class RevisionContracts(unittest.TestCase):
    def test_chapter_map_has_complete_old_and_new_coverage(self):
        data=json.loads((ROOT/'guide/project/mysql-chapter-migration-2026-09-27.json').read_text())
        self.assertEqual(len(data['mapping']),23)
        dest={p for row in data['mapping'] for p in row['new_paths']}
        self.assertEqual(dest,{p.relative_to(ROOT).as_posix() for p in (MOD/'docs').glob('*.md')})
    def test_main_no_language_specific_driver_code(self):
        text='\n'.join(p.read_text() for p in (MOD/'docs').glob('*.md'))
        self.assertNotIn('```python',text)
        self.assertNotIn('```java',text)
        self.assertNotIn('import pymysql',text)
    def test_named_sources_single_and_both_places_used(self):
        items=mysql_course.examples()
        self.assertTrue(any(x['file'].startswith('docs/') for x in items.values()))
        self.assertTrue(any(x['file'].startswith('examples/') for x in items.values()))
    def test_current_map_counts_and_frozen_source_numbers(self):
        text=(ROOT/'guide/knowledge-map.md').read_text()
        self.assertIn('README.md) | 19 | 26 |',text)
        self.assertIn('26 Canonical / 55 independent HUMAN-A flows',text)
        count = sum(1 for p in (ROOT/'curriculum').glob('*/docs/[0-9][0-9]-*.md'))
        self.assertIn(f'当前合计 {count} 篇', (ROOT/'guide/learning-path.md').read_text())
    def test_no_empty_redirect_chapters(self):
        for path in (MOD/'docs').glob('*.md'):
            self.assertIn('## 本章自测',path.read_text())
            self.assertGreater(len(path.read_text()),1000)
    def test_new_source_placements_within_chapter_range(self):
        data=json.loads((ROOT/'guide/project/mysql-evidence-map-2026-09-27.json').read_text())
        for row in data['new_source_review']:
            self.assertTrue(all(1 <= int(n) <= 19 for n in re.findall(r'\d+',row['placement'])))

    def test_interview_evidence_does_not_leak_into_curriculum_prose(self):
        prose='\n'.join(p.read_text(encoding='utf-8') for p in (MOD/'docs').glob('*.md'))
        self.assertNotRegex(prose, r'\bS\d{3}\b')
        self.assertNotIn('正式收录', prose)
        self.assertFalse((MOD/'docs/20-数据库与缓存边界.md').exists())
        self.assertNotIn('Cache Aside', prose)
        self.assertNotIn('延迟双删', prose)
        self.assertIn('跨系统协作留到后续模块', (MOD/'docs/19-AI应用数据建模.md').read_text(encoding='utf-8'))

    def test_interview_sections_are_compression_not_hidden_curriculum(self):
        for path in (MOD/'docs').glob('*.md'):
            text=path.read_text(encoding='utf-8')
            before=text.split('## 🎯 面试怎么回答',1)[0]
            interview=text.split('## 🎯 面试怎么回答',1)[1].split('## ⚠️ 易错点',1)[0]
            # The answer may reuse technical terms already introduced, but should not introduce references or code fences.
            self.assertNotRegex(interview, r'\bS\d{3}\b')
            self.assertNotIn('```', interview)
            self.assertGreater(len(before), 500)

if __name__=='__main__':
    unittest.main(verbosity=2)
