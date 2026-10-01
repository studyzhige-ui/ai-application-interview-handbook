"""Check the isolated runner's explicit UTF-8 protocol, even with hostile env defaults."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import build_coding_practice as practice
import validate_coding_curriculum as curriculum


class IsolatedRunnerEncoding(unittest.TestCase):
    def run_with_checked_protocol(self, action):
        original = subprocess.run
        calls = []

        def checked(command, **kwargs):
            self.assertIn('-I', command)
            self.assertIn('-S', command)
            index = command.index('-X')
            self.assertEqual(command[index + 1], 'utf8')
            self.assertEqual(kwargs.get('encoding'), 'utf-8')
            # -I must keep ignoring Python env configuration; the CLI flag is
            # what establishes the child/parent stream contract on Windows.
            kwargs['env'] = dict(os.environ, PYTHONUTF8='0', PYTHONIOENCODING='cp1252')
            calls.append(command)
            return original(command, **kwargs)

        with patch.object(subprocess, 'run', side_effect=checked):
            result = action()
        self.assertTrue(calls)
        return result

    def test_chinese_input_and_exact_output(self):
        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory)
            for number in range(1, 10):
                text = f'# {number:02d} Test\n'
                if number == 1:
                    options = json.dumps({'stdin': '中文输入\n', 'stdout': '收到：中文输入\n'}, ensure_ascii=False)
                    text += f'\n<!-- run: {options} -->\n```python\nprint("收到：" + input())\n```\n'
                (docs/f'{number:02d}-test.md').write_text(text, encoding='utf-8')
            with patch.object(curriculum, 'DOCS', docs):
                result = self.run_with_checked_protocol(curriculum.run_examples)
            self.assertEqual(result['exact_stdout_checks'], 1)
            self.assertEqual(result['cold_run_blocks']['01-test.md'], 1)

    def test_reference_answer_unicode_output(self):
        exercise = practice.Exercise('E01', '题目', '', 'assert value == "中文答案"',
                                     'value = "中文答案"\nprint(value)', '说明')
        assertions = self.run_with_checked_protocol(lambda: practice.validate_answers([exercise]))
        self.assertEqual(assertions, 1)


    def test_nonisolated_lab_fixes_stdio_and_keeps_import_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lab = root/'practice/coding/exercises/09-ai-coding-lab'
            lab.mkdir(parents=True)
            common = 'import sys\nprint("输出：中文")\nprint("诊断：中文", file=sys.stderr)\n'
            (lab/'pagination.py').write_text(common + 'value = "错误"\n', encoding='utf-8')
            solution = common + 'value = "正确"\n'
            (lab/'README.md').write_text('<!-- solution:pagination -->\n```python\n' + solution + '```\n', encoding='utf-8')
            (lab/'test_pagination.py').write_text(
                'import unittest\nfrom pagination import value\nclass Case(unittest.TestCase):\n'
                '    def test_value(self):\n        self.assertEqual(value, "正确")\n', encoding='utf-8')
            original = subprocess.run
            calls = []

            def checked(command, **kwargs):
                self.assertNotIn('-I', command)  # Keep the local exercise importable.
                self.assertEqual(kwargs['encoding'], 'utf-8')
                self.assertEqual(kwargs['env']['PYTHONIOENCODING'], 'utf-8')
                self.assertEqual(kwargs['env']['HANDBOOK_ENCODING_TEST'], 'preserved')
                result = original(command, **kwargs)
                self.assertIn('输出：中文', result.stdout)
                self.assertIn('诊断：中文', result.stderr)
                calls.append(result.returncode)
                return result

            with patch.dict(os.environ, {'PYTHONUTF8': '0', 'PYTHONIOENCODING': 'cp1252',
                                         'HANDBOOK_ENCODING_TEST': 'preserved'}):
                with patch.object(curriculum, 'ROOT', root), patch.object(subprocess, 'run', side_effect=checked):
                    result = curriculum.validate_lab()
            self.assertEqual(len(calls), 2)
            self.assertNotEqual(calls[0], 0)
            self.assertEqual(calls[1], 0)
            self.assertTrue(result['starter_expected_to_fail'])
            self.assertTrue(result['reference_passed'])


if __name__ == '__main__':
    unittest.main()
