#!/usr/bin/env python3
"""Bounded Agent curriculum regressions: actual examples, Schema and rendered structure.

Install tools/agent-validation-requirements.txt in an isolated environment.
Missing dependencies fail explicitly; no real model, network tool or recovery service is run.
"""
from __future__ import annotations
import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest

import jsonschema
from markdown_it import MarkdownIt
from sync_agent_materials import build
from validate_agent_readability import ROOT, MODULE, chapter_errors, collect_examples, split_fences

DOCS = sorted((MODULE / 'docs').glob('[0-9][0-9]-*.md'))
TEXTS = {int(p.name[:2]): p.read_text(encoding='utf-8') for p in DOCS}
EXAMPLES = collect_examples(DOCS)
QUESTIONS = json.loads((MODULE / 'interview/questions.json').read_text(encoding='utf-8'))['questions']


def namespace(name: str) -> dict:
    scope = {'__name__': '__main__'}
    exec(compile(EXAMPLES[name], f'<teaching:{name}>', 'exec'), scope)
    return scope


class RenderInspection(HTMLParser):
    def __init__(self):
        super().__init__()
        self.counts = {}; self.details = []; self.bad = []; self.ids = []
    def handle_starttag(self, tag, attrs):
        self.counts[tag] = self.counts.get(tag, 0) + 1
        attributes = dict(attrs)
        if 'id' in attributes:
            self.ids.append(attributes['id'])
        if tag == 'details':
            self.details.append(0)
            if 'open' in attributes:
                self.bad.append('default-open answer')
        if tag == 'summary':
            if not self.details:
                self.bad.append('summary outside details')
            else:
                self.details[-1] += 1
    def handle_endtag(self, tag):
        if tag == 'details':
            if not self.details:
                self.bad.append('unmatched details close')
            elif self.details.pop() != 1:
                self.bad.append('details must have exactly one summary')


class FeedbackTests(unittest.TestCase):
    def test_returns_observed_content(self):
        scope = namespace('feedback_loop')
        self.assertEqual(scope['run_report'](), '发布日期待确认')
    def test_empty_observation_requests_tool(self):
        scope = namespace('feedback_loop')
        self.assertEqual(scope['decide']({'observations': []})['kind'], 'tool')
    def test_observation_changes_decision(self):
        scope = namespace('feedback_loop')
        self.assertEqual(scope['decide']({'observations': ['new']})['text'], 'new')
    def test_repeated_tool_hits_budget(self):
        scope = namespace('feedback_loop')
        scope['decide'] = lambda state: {'kind': 'tool', 'name': 'read', 'doc': 'A'}
        with self.assertRaisesRegex(RuntimeError, '预算'):
            scope['run_report']()
    def test_unverified_final_rejected(self):
        scope = namespace('feedback_loop')
        scope['decide'] = lambda state: {'kind': 'final', 'text': 'claimed'}
        with self.assertRaises(ValueError):
            scope['run_report']()
    def test_unknown_tool_rejected(self):
        scope = namespace('feedback_loop')
        scope['decide'] = lambda state: {'kind': 'tool', 'name': 'delete', 'doc': 'A'}
        with self.assertRaises(ValueError):
            scope['run_report']()


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.scope = namespace('registry_projection')
        self.dispatch = self.scope['dispatch']
    def test_authorized_read(self):
        result = self.dispatch({'name': 'read_document', 'arguments': {'document_id': 'A'}}, {'A'})
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['text'], self.scope['DOCUMENTS']['A'])
    def test_existing_but_unauthorized(self):
        self.assertEqual(self.dispatch({'name': 'read_document', 'arguments': {'document_id': 'B'}}, {'A'})['status'], 'denied')
    def test_missing_document_distinct(self):
        self.assertEqual(self.dispatch({'name': 'read_document', 'arguments': {'document_id': 'C'}}, {'C'})['status'], 'unavailable')
    def test_unknown_tool(self):
        self.assertEqual(self.dispatch({'name': 'other', 'arguments': {}}, {'A'})['status'], 'invalid_tool')
    def test_invalid_argument_shapes(self):
        for args in (None, [], {}, {'document_id': 3}, {'document_id': ''}, {'document_id': 'A', 'user_id': 'other'}):
            with self.subTest(args=args):
                self.assertEqual(self.dispatch({'name': 'read_document', 'arguments': args}, {'A'})['status'], 'invalid_arguments')
    def test_model_projection_has_no_handler(self):
        for spec in self.scope['visible_specs']:
            self.assertNotIn('handler', spec)
            self.assertNotIn('read_only', spec)
        json.dumps(self.scope['visible_specs'], ensure_ascii=False)


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        blocks = [json.loads(c) for lang, c in split_fences(TEXTS[4])[1] if lang == 'json']
        cls.schema = next(b for b in blocks if b.get('properties', {}).get('amount', {}).get('minimum') == 0)
        jsonschema.Draft202012Validator.check_schema(cls.schema)
        cls.validator = jsonschema.Draft202012Validator(cls.schema)
    def test_positive(self):
        self.validator.validate({'amount': 10})
    def test_zero_allowed(self):
        self.validator.validate({'amount': 0})
    def test_negative_rejected_by_minimum(self):
        with self.assertRaises(jsonschema.ValidationError) as context:
            self.validator.validate({'amount': -100})
        self.assertEqual(context.exception.validator, 'minimum')
    def test_string_rejected(self):
        with self.assertRaises(jsonschema.ValidationError):
            self.validator.validate({'amount': '10'})
    def test_missing_required(self):
        with self.assertRaises(jsonschema.ValidationError):
            self.validator.validate({})
    def test_extra_field(self):
        with self.assertRaises(jsonschema.ValidationError):
            self.validator.validate({'amount': 10, 'role': 'admin'})
    def test_parse_failure_precedes_schema(self):
        with self.assertRaises(json.JSONDecodeError):
            json.loads('{"amount":')


class TeachingStructureTests(unittest.TestCase):
    def test_all_chapters(self):
        for n, text in TEXTS.items():
            with self.subTest(chapter=n):
                self.assertEqual(chapter_errors(text, n), [])
    def test_mutation_missing_endcap_detected(self):
        self.assertTrue(chapter_errors(TEXTS[1].replace('## 本章小结', '## Removed'), 1))
    def test_mutation_evidence_leak_detected(self):
        self.assertTrue(chapter_errors(TEXTS[1] + '\nAGENT-001 HUMAN-A\n', 1))
    def test_mutation_hidden_interview_detected(self):
        text = TEXTS[1].replace('## 🎯 面试怎么回答', '## 🎯 面试怎么回答\n<details>')
        self.assertTrue(chapter_errors(text, 1))
    def test_mutation_open_answer_detected(self):
        self.assertTrue(chapter_errors(TEXTS[1].replace('<details>', '<details open>', 1), 1))
    def test_mutation_invalid_json_detected(self):
        self.assertTrue(chapter_errors(TEXTS[4] + '\n```json\n{broken}\n```\n', 4))
    def test_mutation_unclosed_fence_detected(self):
        self.assertTrue(chapter_errors(TEXTS[1] + '\n```text\nunfinished', 1))
    def test_interview_generation_exact(self):
        for path, expected in build(ROOT).items():
            with self.subTest(path=path):
                self.assertEqual((ROOT / path).read_text(encoding='utf-8'), expected)
    def test_question_scope_and_uniqueness(self):
        self.assertEqual([q['id'] for q in QUESTIONS], list(range(1, 57)))
        self.assertEqual(len({q['answer'] for q in QUESTIONS}), 56)
    def test_skill_hook_targets_not_mcp(self):
        self.assertEqual([QUESTIONS[i-1]['chapter'] for i in (42, 43)], [17, 17])
    def test_questions_target_main_explanation(self):
        for q in QUESTIONS:
            with self.subTest(question=q['id']):
                main = TEXTS[q['chapter']].split('## 本章小结')[0]
                self.assertIn(f'id="core-{q["section"]}"', main)
    def test_no_copied_mcp_interview_in_extensions(self):
        qa = TEXTS[17].split('## 🎯 面试怎么回答')[1].split('## ⚠️ 易错点')[0]
        self.assertNotIn('### MCP', qa)
        self.assertNotIn('### Host', qa)
    def test_nonexistent_recovery_demo_removed(self):
        quiz = TEXTS[13].split('## 本章自测')[1].split('## 知识回看')[0]
        self.assertNotIn('示例代码证明了什么', quiz)
    def test_plan_quiz_does_not_require_cache(self):
        quiz = TEXTS[8].split('## 🎯 面试怎么回答')[1].split('## 知识回看')[0]
        self.assertNotIn('Prompt Cache', quiz)
        self.assertNotIn('前缀缓存', quiz)
    def test_budget_arithmetic(self):
        rows = re.findall(r'^\| ([^|]+) \| (\d+)k \|$', TEXTS[9], re.M)
        values = {label.strip(): int(value) for label, value in rows}
        self.assertEqual(sum(values[k] for k in ('指令','目标与状态','近期历史','记忆与检索证据','工具说明','工具结果')), values['输入小计'])
        self.assertEqual(values['输入小计'] + values['输出预留'] + values['安全余量'], values['合计'])
    def test_markdown_rendering_and_fold_structure(self):
        renderer = MarkdownIt('commonmark', {'html': True}).enable('table')
        for n, text in TEXTS.items():
            with self.subTest(chapter=n):
                output = renderer.render(text)
                parser = RenderInspection(); parser.feed(output); parser.close()
                self.assertEqual(parser.bad, [])
                self.assertEqual(parser.details, [])
                self.assertEqual(parser.counts.get('h1'), 1)
                self.assertGreaterEqual(parser.counts.get('h2', 0), 6)
                self.assertGreaterEqual(parser.counts.get('details', 0), 3)
                self.assertEqual(len(parser.ids), len(set(parser.ids)))
                self.assertNotIn('{{feedback_loop}}', output)


if __name__ == '__main__':
    unittest.main(verbosity=2)
