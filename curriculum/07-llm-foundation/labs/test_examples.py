#!/usr/bin/env python3
"""Verify trusted, named Python blocks extracted from this module's Markdown.

No model download, GPU, network request, API call, or repository write occurs.
Run from any directory: python path/to/labs/test_examples.py -v
"""
from __future__ import annotations

import ast
import math
from pathlib import Path
import re
import unittest

MODULE = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r"<!-- example: ([\w-]+) -->\s*```python\n(.*?)\n```", re.S)
EXPECTED = {"softmax", "kv-bytes", "lora-count"}


def load_examples() -> dict[str, dict[str, object]]:
    """Execute only repository-owned, reviewed example blocks in fresh scopes.

    This is not a sandbox and must not be used on untrusted Markdown.
    """
    examples: dict[str, dict[str, object]] = {}
    for path in sorted((MODULE / "docs").glob("*.md")):
        for name, source in BLOCK.findall(path.read_text(encoding="utf-8")):
            if name in examples:
                raise ValueError(f"duplicate example marker: {name}")
            scope: dict[str, object] = {"__name__": "__course_example__"}
            ast.parse(source, filename=str(path), feature_version=(3, 10))
            exec(compile(source, str(path), "exec"), scope)
            examples[name] = scope
    if set(examples) != EXPECTED:
        raise ValueError(f"unexpected example markers: {set(examples)!r}")
    return examples


class Examples(unittest.TestCase):
    def setUp(self) -> None:
        examples = load_examples()
        self.probabilities = examples["softmax"]["probabilities"]
        self.kv = examples["kv-bytes"]["kv_bytes"]
        self.lora = examples["lora-count"]["lora_parameter_counts"]

    def test_named_blocks_execute_their_own_assertions(self) -> None:
        self.assertEqual(set(load_examples()), EXPECTED)

    def test_softmax_translation_invariance(self) -> None:
        a = self.probabilities([2, 1, 0])
        b = self.probabilities([1002, 1001, 1000])
        for x, y in zip(a, b):
            self.assertAlmostEqual(x, y)

    def test_softmax_equal_logits(self) -> None:
        self.assertEqual(self.probabilities([0, 0]), [0.5, 0.5])

    def test_softmax_temperature_and_order(self) -> None:
        cold = self.probabilities([2, 1, 0], 0.5)
        warm = self.probabilities([2, 1, 0], 2.0)
        self.assertGreater(cold[0], warm[0])
        self.assertEqual(sorted(warm, reverse=True), warm)
        self.assertAlmostEqual(sum(warm), 1.0)
        self.assertEqual([round(x, 4) for x in warm], [0.5065, 0.3072, 0.1863])

    def test_softmax_rejects_invalid_numbers(self) -> None:
        for x in ([], [math.inf], [math.nan]):
            with self.subTest(logits=x), self.assertRaises(ValueError):
                self.probabilities(x)
        for t in (0, -1, math.inf, math.nan):
            with self.subTest(temperature=t), self.assertRaises(ValueError):
                self.probabilities([1, 0], t)

    def test_inputs_are_not_mutated(self) -> None:
        logits, lengths = [2, 1, 0], [1024, 3072]
        self.probabilities(logits)
        self.kv(16, 4, 64, 2, lengths)
        self.assertEqual(logits, [2, 1, 0])
        self.assertEqual(lengths, [1024, 3072])

    def test_kv_capacity_and_new_configuration(self) -> None:
        self.assertEqual(self.kv(16, 4, 64, 2, [1024, 3072]), 64 * 1024**2)
        self.assertEqual(self.kv(16, 4, 64, 2, [8192]), 128 * 1024**2)
        self.assertEqual(self.kv(24, 4, 64, 2, [2048, 4096]), 144 * 1024**2)
        self.assertEqual(self.kv(24, 8, 64, 2, [2048, 4096]), 288 * 1024**2)

    def test_kv_empty_and_zero_length(self) -> None:
        self.assertEqual(self.kv(16, 4, 64, 2, []), 0)
        self.assertEqual(self.kv(16, 4, 64, 2, [0]), 0)

    def test_kv_bad_dimensions_and_lengths(self) -> None:
        for args in ((0, 4, 64, 2, [1]), (True, 4, 64, 2, [1]),
                     (16, 4, 64, 0.5, [1]), (16, 4, 64, 2, [-1]),
                     (16, 4, 64, 2, [True])):
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.kv(*args)

    def test_lora_counts_and_fraction(self) -> None:
        self.assertEqual(self.lora(1024, 2048, 4), (2097152, 12288))
        base, adapter = self.lora(4096, 4096, 8)
        self.assertAlmostEqual(adapter / base * 100, 0.390625)
        self.assertEqual(self.lora(4, 4, 1), (16, 8))

    def test_lora_invalid_inputs(self) -> None:
        for args in ((0, 4, 1), (4, 4, 0), (4, 4, 5), (True, 4, 1), (4, 4, 1.5)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                self.lora(*args)

    def test_masked_attention_numeric_example(self) -> None:
        # Reuse the lesson's softmax. Masked entries are excluded before normalization.
        p = self.probabilities([1 / math.sqrt(2), 0])
        out = [p[0] * 2, p[1] * 4]
        self.assertEqual([round(x, 4) for x in p], [0.6698, 0.3302])
        self.assertEqual([round(x, 4) for x in out], [1.3395, 1.3210])
        self.assertGreater(math.exp(0), 0)  # A zero score is not a zero weight.

    def test_positive_temperature_does_not_change_argmax(self) -> None:
        x = [-2.0, 0.5, 7.0, 1.0]
        for t in (0.1, 1, 10):
            y = self.probabilities(x, t)
            self.assertEqual(max(range(len(y)), key=y.__getitem__), 2)

    def test_context_budget_examples(self) -> None:
        self.assertEqual(sum([400, 1600, 200, 3000, 500, 92]), 5792)
        self.assertEqual(8192 - 5792 - 1800 - 200, 400)
        self.assertEqual(16384 - 12000 - 3500 - 400, 484)
        self.assertEqual(12000 + 600 + 3500 + 400 - 16384, 116)

    def test_nucleus_and_top_k_arithmetic(self) -> None:
        self.assertAlmostEqual(0.4 / (0.4 + 0.35), 0.533333333333)
        self.assertAlmostEqual(0.4 / (0.4 + 0.35 + 0.2), 0.421052631579)
        self.assertGreaterEqual(0.92, 0.9)

    def test_paging_and_latency(self) -> None:
        self.assertEqual(math.ceil(35 / 16) * 16 - 35, 13)
        self.assertEqual(math.ceil(19 / 8) * 8 - 19, 5)
        self.assertAlmostEqual((2.8 - 0.8) / (101 - 1), 0.020)
        self.assertAlmostEqual((3.6 - 0.6) / (61 - 1), 0.050)

    def test_pooling_and_normalization(self) -> None:
        # A numerical check of the written formula, not a trained Embedding model.
        valid = [(1.0, 2.0), (3.0, 0.0)]
        mean = [sum(v[i] for v in valid) / len(valid) for i in range(2)]
        self.assertEqual(mean, [2, 1])
        norm = math.sqrt(sum(v*v for v in mean))
        self.assertEqual([round(x / norm, 4) for x in mean], [0.8944, 0.4472])

    def test_quality_counts_are_jointly_feasible(self) -> None:
        # Chapter 12 examples must have enough answered, answerable tasks for correct answers.
        for answerable, total, answered, correct, false_refusal in (
            (80, 100, 70, 64, 15), (60, 100, 50, 35, 20)
        ):
            answered_answerable = answerable - false_refusal
            answered_unanswerable = answered - answered_answerable
            self.assertLessEqual(correct, answered_answerable)
            self.assertGreaterEqual(answered_unanswerable, 0)
            self.assertLessEqual(answered_unanswerable, total-answerable)
            self.assertLessEqual(false_refusal, total-answered)
        chapter = next((MODULE / 'docs').glob('12-*.md')).read_text(encoding='utf-8')
        self.assertIn('35/50=70%', chapter)
        self.assertIn('20/60≈33.3%', chapter)

    def test_cost_per_success(self) -> None:
        self.assertAlmostEqual(130 * .01 / 80, .01625)
        self.assertAlmostEqual(105 * .014 / 98, .015)
        self.assertAlmostEqual(3.3 / 48, .06875)

    def test_grpo_relative_rewards(self) -> None:
        rewards = [0.0, 1.0, 1.0, 2.0]
        mean = sum(rewards) / len(rewards)
        sd = math.sqrt(sum((x-mean)**2 for x in rewards) / len(rewards))
        self.assertEqual([round((x-mean)/sd, 4) for x in rewards], [-1.4142, 0, 0, 1.4142])
        self.assertEqual([x-1 for x in [0, 0, 2, 2]], [-1, -1, 1, 1])

    def test_multimodal_coordinate_and_growth_examples(self) -> None:
        self.assertEqual((200 + 30, 100 + 40), (230, 140))
        self.assertEqual((200 + 30/.5, 100 + 40/.5), (260, 180))
        self.assertEqual((100-80)/80, .25)


if __name__ == '__main__':
    unittest.main()
