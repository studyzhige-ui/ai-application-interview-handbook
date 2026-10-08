"""Focused regression tests for Notebook answer layout (standard library only).

Run: python -m unittest discover -s practice/coding/exercises -p 'test_coding_practice_renderer.py' -v
"""
from __future__ import annotations

import unittest

from build_coding_practice import SOURCE, explanation_html, extract, inline_html, notebook


class ExplanationRendererTests(unittest.TestCase):
    def test_paragraph_boundaries_remain_separate(self):
        result = explanation_html("先说规则。\n\n再解释例子。")
        self.assertEqual(result, "<p>先说规则。</p>\n<p>再解释例子。</p>")

    def test_numbered_steps_are_an_ordered_list(self):
        result = explanation_html("按顺序执行：\n\n1. 读旧值。\n2. 写新值。")
        self.assertIn("<ol>\n<li>读旧值。</li>\n<li>写新值。</li>\n</ol>", result)

    def test_parallel_roles_are_an_unordered_list(self):
        self.assertEqual(
            explanation_html("- `seen` 查重复。\n- `result` 保留顺序。"),
            "<ul>\n<li><code>seen</code> 查重复。</li>\n<li><code>result</code> 保留顺序。</li>\n</ul>",
        )

    def test_warning_is_a_separate_blockquote(self):
        result = explanation_html("说明。\n\n> ⚠️ **先查再记录**，不要重复使用位置。")
        self.assertIn("<blockquote>\n<p>⚠️ <strong>先查再记录</strong>", result)
        self.assertTrue(result.endswith("</p>\n</blockquote>"))

    def test_source_html_is_escaped(self):
        result = explanation_html('<script>alert("x")</script>\n\n> ⚠️ `x < 3`')
        self.assertNotIn("<script>", result)
        self.assertIn("&lt;script&gt;", result)
        self.assertIn("<code>x &lt; 3</code>", result)

    def test_code_contents_do_not_become_bold(self):
        self.assertEqual(inline_html("`x ** 2` 与 **结果**"), "<code>x ** 2</code> 与 <strong>结果</strong>")

    def test_list_can_start_at_another_number(self):
        self.assertIn('<ol start="3">', explanation_html("3. 下一步。"))

    def test_warning_can_contain_steps(self):
        result = explanation_html("> 1. 先检查类型。\n> 2. 再检查范围。")
        self.assertIn("<blockquote>\n<ol>", result)

    def test_unsupported_table_fails_instead_of_flattening(self):
        with self.assertRaises(ValueError):
            explanation_html("| A | B |\n|---|---|")

    def test_course_answers_keep_real_structures(self):
        exercises = extract(SOURCE.read_text(encoding="utf-8"))
        generated = notebook(exercises)
        answers = {
            c["metadata"]["exercise_id"]: "".join(c["source"])
            for c in generated["cells"] if c["metadata"]["role"] == "answer"
        }
        self.assertEqual(len(answers), 22)
        self.assertIn("<ol>", answers["E17"])
        self.assertIn("<ul>", answers["E12"])
        self.assertIn("<blockquote>", answers["E17"])
        self.assertNotIn("<details open", "".join(answers.values()))
        for source in answers.values():
            self.assertEqual(source.count("<details>"), 1)
            self.assertEqual(source.count("</details>"), 1)
        codes = [c for c in generated["cells"] if c["cell_type"] == "code"]
        self.assertEqual(len(codes), 44)
        self.assertTrue(all(c["execution_count"] is None and not c["outputs"] for c in codes))


if __name__ == "__main__":
    unittest.main()
