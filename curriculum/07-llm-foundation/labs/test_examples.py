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

from lesson_data import numeric_table, table_fingerprint

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


class RefinedMechanisms(unittest.TestCase):
    """Read prose tables and test small calculations, not a trained model."""

    @staticmethod
    def vector(text: str) -> list[float]:
        value = ast.literal_eval(text.strip('`').replace('−', '-'))
        if not isinstance(value, list) or not all(type(x) in (int, float) for x in value):
            raise ValueError(f"not a numeric vector: {text!r}")
        return value

    def test_ffn_table_matches_each_step(self) -> None:
        rows = numeric_table('ffn')[1:]
        # The input and rules are also checked so a prose edit cannot silently change the experiment.
        text = next((MODULE / 'docs').glob('03-*.md')).read_text(encoding='utf-8')
        self.assertIn('h=[1,2]', text)
        self.assertEqual(rows[0][1], '[h₁, −h₁−h₂, 2h₂]')
        self.assertEqual(rows[2][1], '对中间结果 u 计算 [u₁+u₃, u₂−u₃]')
        h = [1, 2]
        first = [h[0], -h[0]-h[1], 2*h[1]]
        activated = [max(0, z) for z in first]
        last = [activated[0]+activated[2], activated[1]-activated[2]]
        self.assertEqual([self.vector(r[2]) for r in rows], [first, activated, last])

    def test_ffn_transfer_and_without_activation(self) -> None:
        for h, wanted, linear in [([-1,2], [4,-4], [3,-5]),
                                   ([2,-1], [2,0], [0,1])]:
            a = [h[0], -h[0]-h[1], 2*h[1]]
            u = [max(0, z) for z in a]
            self.assertEqual([u[0]+u[2], u[1]-u[2]], wanted)
            self.assertEqual([a[0]+a[2], a[1]-a[2]], linear)

    def test_normalization_table(self) -> None:
        rows = numeric_table('normalization')[1:]
        x = [2.,4.]
        mean = sum(x)/len(x)
        variance = sum((v-mean)**2 for v in x)/len(x)
        rms = math.sqrt(sum(v*v for v in x)/len(x))
        expected = [[(v-mean)/math.sqrt(variance) for v in x],
                    [round(v/rms,4) for v in x]]
        self.assertEqual([self.vector(r[3].removeprefix('约 ')) for r in rows], expected)

    def test_normalization_shift_not_softmax(self) -> None:
        def ln(x):
            mu = sum(x)/len(x)
            sigma = math.sqrt(sum((a-mu)**2 for a in x)/len(x))
            return [(a-mu)/sigma for a in x]
        self.assertEqual(ln([2,4]), ln([102,104]))
        self.assertEqual(sum(ln([2,4])), 0)
        self.assertNotAlmostEqual(2/math.sqrt(10), 102/math.sqrt((102**2+104**2)/2))

    def test_rope_table_and_relative_shift(self) -> None:
        rows = numeric_table('rope-quarter-turn')[1:]
        vectors = []
        for row in rows:
            position = int(row[0])
            angle = math.radians(float(row[1].rstrip('°')))
            self.assertAlmostEqual(angle, position*math.pi/2)
            wanted = self.vector(row[2])
            for a,b in zip([math.cos(angle),math.sin(angle)], wanted):
                self.assertAlmostEqual(a,b)
            vectors.append(wanted)
        dot = lambda a,b: sum(x*y for x,y in zip(a,b))
        self.assertEqual(dot(vectors[2],vectors[1]), 0)
        self.assertEqual(dot(vectors[3],vectors[2]), 0)
        self.assertEqual(dot(vectors[2],vectors[0]), -1)
        self.assertEqual(dot(vectors[1],vectors[0]), 0)

    def test_rope_general_relative_identity(self) -> None:
        def rotate(x,theta):
            c,s = math.cos(theta),math.sin(theta)
            return [c*x[0]-s*x[1],s*x[0]+c*x[1]]
        dot = lambda a,b: sum(x*y for x,y in zip(a,b))
        q,k = [2.,-1.],[1.,3.]
        theta,m,n = .37,5,2
        self.assertAlmostEqual(dot(rotate(q,m*theta),rotate(k,n*theta)),
                               dot(q,rotate(k,(n-m)*theta)))

    def test_sft_loss_table(self) -> None:
        for row in numeric_table('sft-loss')[1:]:
            self.assertAlmostEqual(-math.log(float(row[0])), float(row[1]), places=4)

    def test_lora_increment_table_and_rank_direction(self) -> None:
        rows = numeric_table('lora-increment')[1:]
        x = self.vector(rows[0][2])
        s = sum(a*b for a,b in zip([1,1,0,0], x))
        delta = [s*b for b in [1,2,3,4]]
        self.assertEqual(float(rows[1][2]), s)
        self.assertEqual(self.vector(rows[2][2]), delta)
        self.assertEqual(self.vector(rows[3][2]), [a+b for a,b in zip(x,delta)])
        # A requested delta [1,0,0,0] cannot be a scalar multiple of this fixed B.
        self.assertNotEqual([1,2,3,4], [1,0,0,0])

    def test_lora_transfer_preserves_base_branch(self) -> None:
        def run(x):
            s=x[0]+x[1]
            delta=[s*b for b in [1,2,3,4]]
            return delta,[a+b for a,b in zip(x,delta)]
        self.assertEqual(run([1,-1,0,0]), ([0,0,0,0],[1,-1,0,0]))
        a,b=run([2,1,0,0]),run([3,0,0,0])
        self.assertEqual(a[0], b[0])
        self.assertEqual(b[1], [6,6,9,12])
        self.assertNotEqual(a[1],b[1])

    def test_lora_zero_initialization_signal(self) -> None:
        # Sensitivity of b*a*x to a or b; not a simulation of an optimizer.
        x,a,b=1.,1.,0.
        derivative_a=b*x
        derivative_b=a*x
        self.assertEqual(derivative_a,0.)
        self.assertEqual(derivative_b,1.)
        self.assertEqual((0.*x,0.*x), (0.,0.))

    def test_dpo_table_and_loss(self) -> None:
        rows=numeric_table('dpo-pair')[1:]
        gains=[]
        for row in rows:
            gain=float(row[2])-float(row[1])
            self.assertEqual(float(row[3]),gain)
            gains.append(gain)
        s=gains[0]-gains[1]  # The prose fixes beta=1 for this experiment.
        self.assertEqual(s,2.)
        self.assertAlmostEqual(1/(1+math.exp(-s)), .8808, places=4)
        self.assertAlmostEqual(math.log1p(math.exp(-s)), .1269, places=4)
        self.assertAlmostEqual(math.log(2), .6931, places=4)

    def test_dpo_relative_improvement_is_not_absolute_probability(self) -> None:
        # Chapter self-test and review use new conditions, not the worked pair verbatim.
        for ref,now,score in [([-4,-3],[-5,-6],2), ([-2,-2],[-3,-4],1)]:
            s=(now[0]-ref[0])-(now[1]-ref[1])
            self.assertEqual(s,score)
            self.assertLess(math.exp(now[0]), math.exp(ref[0]))
            self.assertLess(math.log1p(math.exp(-s)), math.log(2))
        self.assertAlmostEqual(math.log1p(math.exp(-1)), .3133, places=4)

    def test_quarterly_figure_source_fingerprint(self) -> None:
        table=numeric_table('quarterly-evidence')
        records={r[0]:r[1:] for r in table[1:]}
        first,second=map(float,records['销售额'][:2])
        self.assertEqual((second-first)/first,.2)
        self.assertEqual(records['访问量'],['—','150','万次'])
        svg=(MODULE/'assets'/'quarterly-evidence.svg').read_text(encoding='utf-8')
        self.assertIn('source-sha256='+table_fingerprint(table), svg)

    def test_cache_self_test_has_no_later_lora_prerequisite(self) -> None:
        text=next((MODULE/'docs').glob('06-*.md')).read_text(encoding='utf-8')
        task=text.split('## 11. 自测',1)[1]
        self.assertNotIn('LoRA',task)
        self.assertNotIn('适配器',task)

    def test_quick_reference_chapter_cells_are_links(self) -> None:
        text=(MODULE/'interview'/'面试前速查表.md').read_text(encoding='utf-8')
        rows=[line for line in text.splitlines() if line.startswith('|')][2:]
        for row in rows:
            target=row.strip('|').split('|')[-1].strip()
            self.assertRegex(target,r'\[第 \d+ 章\]\(\.\./docs/[^)]+\.md\)')


if __name__ == '__main__':
    unittest.main()
