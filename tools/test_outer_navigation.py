"""Standard-library regression tests for peripheral-only synchronization."""
from pathlib import Path
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('outer',HERE/'sync_outer_navigation.py')
outer=importlib.util.module_from_spec(spec);spec.loader.exec_module(outer)

class LinkParsingTests(unittest.TestCase):
    def test_balanced_url_parentheses(self):
        self.assertEqual(list(outer.markdown_links('[x](../a(b).md#sec)')),[('x','../a(b).md#sec')])
    def test_fenced_and_inline_examples_are_not_links(self):
        text='```md\n[fake](no.md)\n```\n`[fake](no.md)`\n[real](yes.md)'
        self.assertEqual(list(outer.markdown_links(text)),[('real','yes.md')])
    def test_reference_and_html_links(self):
        pairs=list(outer.markdown_links('[ref]: ../a.md\n<a href="b.md">b</a>'))
        self.assertIn(('ref','../a.md'),pairs);self.assertIn(('HTML','b.md'),pairs)
    def test_heading_alias_and_duplicates(self):
        text='# Hello\n## Hello\n<a id="old-target"></a>\n'
        self.assertEqual(outer.anchors(text),{'hello','hello-1','old-target'})
    def test_absolute_external_is_not_local(self):
        self.assertIsNone(outer.resolve(Path('/r'),Path('/r/a.md'),'https://example.com/a.md'))
    def test_same_page_anchor(self):
        page=Path('/r/a.md')
        self.assertEqual(outer.resolve(Path('/r'),page,'#hello'),(page.resolve(),'hello'))
    def test_generated_blocks_replace_in_place(self):
        once=outer.block('# A\n','t','## Index','body')
        self.assertEqual(outer.block(once,'t','## Index','body'),once)
        self.assertEqual(outer.block(once,'t','## Index','changed').count('<!-- t:start -->'),1)

class FullFixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        def put(p,t):
            f=self.root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(t,encoding='utf-8')
        self.put=put
        self.order=list(outer.DESCRIPTIONS)
        put('guide/learning-order.json',json.dumps({'modules':[{'directory':x,'label':x.split('-',1)[1]} for x in self.order]}))
        helper=HERE/'sync_learning_navigation.py'
        if not helper.exists():
            put('tools/sync_learning_navigation.py','def transform(path,text,order,labels): return text\ndef identify(s):\n import re\n m=re.search(r"(?:curriculum/|\\.\\./)(\\d{2}-[a-z-]+)/README\\.md",s)\n return m.group(1) if m else None\n')
        else:
            (self.root/'tools').mkdir();shutil.copyfile(helper,self.root/'tools/sync_learning_navigation.py')
        for x in self.order:
            put(f'curriculum/{x}/README.md',f'# {x}\n\n1. [Start](docs/01-start.md)\n')
            put(f'curriculum/{x}/docs/01-start.md','# First lesson\n\nPROTECTED LESSON\n')
        for p in ['README.md','curriculum/README.md','guide/README.md','guide/project/README.md','guide/audits/README.md','tools/README.md','practice/README.md','products/README.md','products/agent/README.md']:
            put(p,'# Index\n')
        put('guide/learning-path.md','# Path\n181个正文章节\n')
        put('guide/knowledge-map.md','# Map\n')
        put('references/README.md','# References\n\n## 索引\n\nold\n\n证据来源包括：\n\ntext\n')
        for r in ['mysql','redis']:
            put(f'references/{r}/README.md',f'# {r}\n')
        put('interview/canonical/README.md','# Frozen\n26 Canonical / 55 independent HUMAN-A flows\n')
        put('market/interviews/batch-old.md','# Historical evidence\n')
        put('practice/tooling/README.md','# Tooling\n')
        put('practice/coding/README.md','# Coding\n')
        put('practice/coding/docs/01-fundamentals.md','# Coding lesson\n')
        put('products/agent/sample/README.md','# Example｜Module\nhttps://github.com/example/sample/tree/'+'a'*40+'\n'+''.join(f'| {i} | [Topic {i}]({i:02d}-topic.md) |\n' for i in range(1,5)))
        for i in range(1,5):put(f'products/agent/sample/{i:02d}-topic.md',f'# {i}\n')
    def apply(self,changes):
        for p,t in changes.items():self.put(p,t)
    def test_actual_files_determine_counts(self):
        data=outer.inventory(self.root)
        self.assertEqual(data['curriculum_chapters'],10)
        self.assertEqual(data['products'][0]['chapter_count'],4)
        self.assertEqual(data['coding_chapters'],1)
    def test_missing_chapter_in_module_index_fails(self):
        self.put('curriculum/01-python/docs/02-new.md','# New\n')
        with self.assertRaises(ValueError):outer.inventory(self.root)
    def test_expected_metadata_without_mutating_source(self):
        data=outer.inventory(self.root);changes=outer.plan(self.root,data)
        self.assertIn('10个正文章节',changes['guide/learning-path.md'])
        self.assertIn('(mysql/README.md)',changes['references/README.md'])
        self.assertIn('(redis/README.md)',changes['references/README.md'])
        self.assertEqual((self.root/'guide/learning-path.md').read_text(),'# Path\n181个正文章节\n')
    def test_idempotence_and_scope_protection(self):
        protected=[p for p in self.root.rglob('*') if p.is_file() and ('docs' in p.parts or 'market' in p.parts or 'canonical' in p.parts)]
        before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
        changes=outer.plan(self.root,outer.inventory(self.root));self.apply(changes)
        self.assertEqual(outer.plan(self.root,outer.inventory(self.root)),{})
        self.assertEqual({p:hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},before)
    def test_missing_file_and_anchor_detected(self):
        self.put('guide/check.md','# Check\n[missing](absent.md)\n[anchor](learning-path.md#absent)\n')
        result=outer.validate(self.root,[self.root/'guide/check.md'])
        self.assertEqual(len(result['missing_paths']),1)
        self.assertEqual(len(result['unresolved_anchors']),1)
    def test_same_page_invalid_anchor_detected(self):
        self.put('guide/check.md','# Check\n[anchor](#absent)\n')
        result=outer.validate(self.root,[self.root/'guide/check.md'])
        self.assertEqual(len(result['unresolved_anchors']),1)
    def test_do_not_count_notebooks_or_support_as_lessons(self):
        self.put('curriculum/01-python/docs/README.md','# Reference\n')
        self.put('curriculum/01-python/labs/01-example.md','# Lab\n')
        self.put('curriculum/01-python/docs/01-start.ipynb','{}')
        self.assertEqual(outer.inventory(self.root)['curriculum_chapters'],10)

    def test_all_markdown_not_only_readme_is_scanned(self):
        self.put('references/agent/source-index.md','# Index\n[bad](missing.md)\n')
        pages=outer.validation_paths(self.root)
        self.assertIn(self.root/'references/agent/source-index.md',pages)
        result=outer.validate(self.root,pages)
        self.assertIn({'page':'references/agent/source-index.md','href':'missing.md'},result['missing_paths'])
    def test_code_fence_does_not_hide_real_conflict(self):
        self.put('guide/check.md','```python\n<<<<<<< HEAD\na=1\n=======\na=2\n>>>>>>> other\n```\n')
        result=outer.validate(self.root,[self.root/'guide/check.md'])
        self.assertEqual(result['conflict_markers'],['guide/check.md'])
    def test_only_explicit_conflict_example_is_exempt(self):
        sample='<!-- conflict-example:start -->\n```text\n<<<<<<< HEAD\na\n=======\nb\n>>>>>>> other\n```\n<!-- conflict-example:end -->\n'
        self.put('guide/check.md',sample)
        self.assertEqual(outer.validate(self.root,[self.root/'guide/check.md'])['conflict_markers'],[])
        self.put('guide/check.md',sample+'<<<<<<< unmarked\n')
        self.assertEqual(outer.validate(self.root,[self.root/'guide/check.md'])['conflict_markers'],['guide/check.md'])
    def test_unbalanced_conflict_example_fails(self):
        with self.assertRaises(ValueError):outer.conflict_text('<!-- conflict-example:start -->')
    def test_product_table_order_beats_incidental_prerequisite(self):
        self.put('products/agent/sample/README.md','# Sample\n[Earlier example](02-topic.md)\n\n| 1 | [Context](01-topic.md) |\n| 2 | [Tool](03-topic.md) |\n| 3 | [Memory](02-topic.md) |\n| 4 | [Review](04-topic.md) |\n')
        names=[Path(x).name for x in outer.inventory(self.root)['products'][0]['reading_order']]
        self.assertEqual(names,['01-topic.md','03-topic.md','02-topic.md','04-topic.md'])
    def test_unlisted_product_chapter_fails(self):
        self.put('products/agent/sample/05-new.md','# New\n')
        with self.assertRaises(ValueError):outer.inventory(self.root)
    def test_body_change_invalidates_registry_without_rewriting_body(self):
        before=outer.inventory(self.root)
        self.apply(outer.plan(self.root,before))
        self.put('curriculum/01-python/docs/01-start.md','# New title\nNew explanation\n')
        after=outer.inventory(self.root)
        self.assertNotEqual(before['modules'][0]['chapter_metadata'],after['modules'][0]['chapter_metadata'])
        changes=outer.plan(self.root,after)
        self.assertIn(outer.REGISTRY,changes)
        self.assertIn(outer.INDEX,changes)
        self.assertNotIn('curriculum/01-python/docs/01-start.md',changes)
    def test_expanded_read_scope_does_not_expand_write_scope(self):
        data=outer.inventory(self.root)
        allowed={p.relative_to(self.root).as_posix() for p in outer.peripheral_paths(self.root)}|{outer.REGISTRY,outer.INDEX}
        self.assertTrue(set(outer.plan(self.root,data))<=allowed)
        self.assertNotIn('curriculum/01-python/docs/01-start.md',allowed)
        self.assertNotIn('market/interviews/batch-old.md',allowed)
    def test_missing_review_record_fails(self):
        path=self.root/'guide/learning-order.json';data=json.loads(path.read_text())
        data['modules'][0]['review_records']=['guide/project/absent.md']
        self.put('guide/learning-order.json',json.dumps(data))
        with self.assertRaises(ValueError):outer.inventory(self.root)
    def test_status_pages_are_generated_from_files_not_fixed_175(self):
        for path in outer.STATUS_PAGES:self.put(path,'# Status\n')
        changes=outer.plan(self.root,outer.inventory(self.root))
        self.assertIn('10 篇正文',changes['guide/audits/final-quality-audit.md'])
        self.assertNotIn('175',changes['guide/audits/final-quality-audit.md'])
        self.apply(changes)
        self.assertEqual(outer.plan(self.root,outer.inventory(self.root)),{})

if __name__=='__main__':unittest.main(verbosity=2)
