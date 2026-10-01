"""Reader-facing route contracts: order, numbering, adjacency and optional study plan.

These checks protect navigation consistency; they do not grade prose comprehension.
"""
from pathlib import Path
import json
import re
import unittest
import sync_outer_navigation as navigation

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ['01-python', '02-fastapi', '03-mysql', '04-redis',
            '05-backend-engineering', '06-llm-foundation', '07-vector-db',
            '08-rag', '09-agent', '10-system-design']


class LearningSystemContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = navigation.inventory(ROOT)

    def test_module_prefixes_match_approved_reading_order(self):
        self.assertEqual([m['directory'] for m in self.inventory['modules']], EXPECTED)
        self.assertEqual(sorted(p.name for p in (ROOT/'curriculum').iterdir() if p.is_dir()), EXPECTED)

    def test_entry_tables_share_the_same_course_order(self):
        entries = {str((ROOT/'curriculum'/name/'README.md').resolve()): name for name in EXPECTED}
        pages = ['README.md', 'curriculum/README.md', 'guide/knowledge-map.md',
                 'interview/canonical/README.md', 'interview/canonical/module-index.md']
        for relative in pages:
            page = ROOT/relative
            actual = []
            for line in page.read_text(encoding='utf-8').splitlines():
                if not line.startswith('|'):
                    continue
                for _, href in navigation.markdown_links(line):
                    target = navigation.resolve(ROOT, page, href)
                    if target and str(target[0]) in entries:
                        actual.append(entries[str(target[0])])
            with self.subTest(page=relative):
                self.assertEqual(actual, EXPECTED)

    def test_chapter_prefixes_match_reading_order(self):
        for module in [*self.inventory['modules'], *self.inventory['products']]:
            with self.subTest(module=module['readme']):
                paths = module['reading_order']
                self.assertEqual([int(Path(p).name[:2]) for p in paths], list(range(1, len(paths)+1)))

    def test_course_chapter_navigation_is_adjacent(self):
        for module in self.inventory['modules']:
            paths = [ROOT/p for p in module['reading_order']]
            for index, page in enumerate(paths):
                with self.subTest(page=page.relative_to(ROOT)):
                    # Compatibility anchors may precede the opening navigation.
                    header = '\n'.join(page.read_text(encoding='utf-8').splitlines()[:35])
                    links = [(label, navigation.resolve(ROOT, page, href))
                             for label, href in navigation.markdown_links(header)]
                    prev = [target[0] for label, target in links if target and '←' in label and target[0] in paths]
                    nxt = [target[0] for label, target in links if target and '→' in label and target[0] in paths]
                    if index:
                        self.assertIn(paths[index-1], prev)
                    if index+1 < len(paths):
                        self.assertIn(paths[index+1], nxt)
                    self.assertTrue(all(p == paths[index-1] for p in prev) if index else not prev)
                    self.assertTrue(all(p == paths[index+1] for p in nxt) if index+1 < len(paths) else not nxt)

    def test_product_source_and_private_snapshot_boundaries(self):
        expected = {'codex': 'openai/codex', 'claude-code': 'studyzhige-ui/claude-code-source-private',
                    'deepseek-harness': 'deepseek-ai/deepseek-harness', 'deer-flow': 'bytedance/deer-flow'}
        actual = {Path(item['readme']).parent.name: item for item in self.inventory['products']}
        self.assertEqual(set(actual), set(expected))
        for product, repository in expected.items():
            with self.subTest(product=product):
                self.assertEqual(actual[product]['source_repository'], repository)
                self.assertRegex(actual[product]['source_commit'], r'^[0-9a-f]{40}$')
                self.assertEqual(actual[product]['private_mirror'], product == 'claude-code')

    def test_optional_route_has_no_calendar_or_exit_gate(self):
        text = (ROOT/'guide/learning-path.md').read_text(encoding='utf-8')
        self.assertNotRegex(text, r'第\s*\d+\s*周|\d+\s*周安排|Module Exit Gate|最终验收|每周列')
        self.assertIn('已有可用的代码环境', text)
        self.assertIn('Python 与 Coding 分别顺读', text)

    def test_historical_pinned_urls_do_not_point_to_renamed_paths(self):
        # Old commit links are evidence. Local navigation migrations must not
        # silently invent paths inside historical immutable commits.
        old_commit = 'b87c56d0895de5fd8b16ee325e0937fdc70a8e19'
        new_only = ['03-mysql', '04-redis', '05-backend-engineering', '06-llm-foundation', '07-vector-db']
        pattern = re.compile(r'https://github\.com/studyzhige-ui/ai-application-interview-handbook/blob/' + old_commit + r'/curriculum/(' + '|'.join(new_only) + r')/')
        for page in ROOT.rglob('*.md'):
            with self.subTest(page=page.relative_to(ROOT)):
                self.assertIsNone(pattern.search(page.read_text(encoding='utf-8')))


if __name__ == '__main__':
    unittest.main()
