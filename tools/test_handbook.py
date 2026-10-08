import unittest
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
        p,a=h.resolve(Path('/r'),Path('/r/a/x.md'),'../%E4%B8%AD.md#标题')
        self.assertEqual(str(p),'/r/中.md');self.assertEqual(a,'标题')
    def test_external(self):
        self.assertIsNone(h.resolve(Path('/r'),Path('/r/x.md'),'https://example.com/a'))
    def test_conflict_examples(self):
        self.assertEqual(h.conflict_text('<!-- conflict-example:start -->\n<<<<<<< a\n=======\n>>>>>>> b\n<!-- conflict-example:end -->'),'')
    def test_bad_conflict_example(self):
        with self.assertRaises(ValueError): h.conflict_text('<!-- conflict-example:start -->')

if __name__=='__main__': unittest.main()
