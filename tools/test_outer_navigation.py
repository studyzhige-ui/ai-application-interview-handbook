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
        for p in ['README.md','guide/README.md','guide/project/README.md','guide/audits/README.md','tools/README.md','practice/README.md','products/README.md','products/agent/README.md']:
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
        put('products/agent/sample/README.md','# Example｜Module\nhttps://github.com/example/sample/tree/'+'a'*40+'\n')
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

if __name__=='__main__':unittest.main(verbosity=2)
