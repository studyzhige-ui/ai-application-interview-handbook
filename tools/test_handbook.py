import unittest
import tempfile
from pathlib import Path
import check_handbook as h

class MarkdownTests(unittest.TestCase):
    def test_balanced_url(self):
        self.assertEqual(list(h.markdown_links('[x](a(b).md)')), [('x','a(b).md')])
    def test_code_is_not_navigation(self):
        self.assertEqual(list(h.markdown_links('```md\n[x](missing.md)\n```')),[])
    def test_duplicate_anchors(self):
        self.assertEqual(h.anchors('# 中文标题\n## 中文标题\n'),{'中文标题','中文标题-1'})
    def test_explicit_anchor(self):
        self.assertIn('core-1',h.anchors('<a id="core-1"></a>'))
    def test_encoded_path(self):
        root=Path(__file__).resolve().parent
        p,a=h.resolve(root,root/'a/x.md','../%E4%B8%AD.md#标题')
        self.assertEqual(p,root/'中.md');self.assertEqual(a,'标题')
    def test_external(self):
        self.assertIsNone(h.resolve(Path('/r'),Path('/r/x.md'),'https://example.com/a'))
    def test_conflict_examples(self):
        self.assertEqual(h.conflict_text('<!-- conflict-example:start -->\n<<<<<<< a\n=======\n>>>>>>> b\n<!-- conflict-example:end -->'),'')
    def test_bad_conflict_example(self):
        with self.assertRaises(ValueError): h.conflict_text('<!-- conflict-example:start -->')


class BusinessLayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Minimal architecture fixture with complete local navigation.
        for area in ('curriculum', 'products', 'practice', 'market', 'interview', 'tools', '.github'):
            (self.root / area).mkdir()
            if area != '.github':
                (self.root / area / 'README.md').touch()
        for name in ('README.md', 'WRITING.md'):
            (self.root / name).touch()
        modules = ('01-python', '02-fastapi', '03-mysql', '04-redis',
                   '05-backend-engineering', '06-llm-foundation', '07-vector-db',
                   '08-rag', '09-agent', '10-system-design')
        for name in modules:
            module = self.root / 'curriculum' / name
            (module / 'docs').mkdir(parents=True)
            (module / 'README.md').touch()
            domain = self.root / 'interview' / name
            domain.mkdir()
            for page in ('README.md', '01-高频面试题.md', '02-易混易错点.md', '03-面试速查.md'):
                (domain / page).touch()
        for name in ('codex', 'claude-code', 'deepseek-harness', 'deer-flow'):
            product = self.root / 'products' / name
            product.mkdir()
            (product / 'README.md').touch()
        for name in ('coding/docs', 'coding/exercises', 'software'):
            (self.root / 'practice' / name).mkdir(parents=True)
        (self.root / 'practice/coding/README.md').touch()
        for business in ('job-description', 'interview-experience'):
            directory = self.root / 'market' / business
            directory.mkdir()
            (directory / 'README.md').touch()
            for layer in ('01-data', '02-analysis', '03-strategy', '04-scripts', '05-logs'):
                (directory / layer).mkdir()
        (self.root / 'market/job-description/official-campus-links.md').touch()
        for readme in self.root.rglob('README.md'):
            if 'market' in readme.relative_to(self.root).parts:
                continue
            children = list(readme.parent.glob('*.md'))
            children += list(readme.parent.glob('*/README.md'))
            readme.write_text('\n'.join(
                f'[page]({child.relative_to(readme.parent).as_posix()})'
                for child in children if child != readme), encoding='utf-8')

    def test_official_campus_entry_is_valid(self):
        self.assertEqual(h.check(self.root), [])

    def test_unexpected_business_entries_are_rejected(self):
        for business in ('job-description', 'interview-experience'):
            with self.subTest(business=business):
                extra = self.root / 'market' / business / 'unexpected.md'
                extra.touch()
                self.assertEqual(h.check(self.root), [f'market/{business}: invalid business layers'])
                extra.unlink()

    def test_campus_entry_is_specific_to_job_description(self):
        (self.root / 'market/interview-experience/official-campus-links.md').touch()
        self.assertEqual(h.check(self.root), ['market/interview-experience: invalid business layers'])

    def test_required_business_entries_cannot_be_missing(self):
        for relative in ('job-description/official-campus-links.md',
                         'job-description/05-logs', 'interview-experience/05-logs'):
            with self.subTest(relative=relative):
                entry = self.root / 'market' / relative
                is_dir = entry.is_dir()
                entry.rmdir() if is_dir else entry.unlink()
                business = relative.split('/')[0]
                self.assertEqual(h.check(self.root), [f'market/{business}: invalid business layers'])
                entry.mkdir() if is_dir else entry.touch()

if __name__=='__main__': unittest.main()
