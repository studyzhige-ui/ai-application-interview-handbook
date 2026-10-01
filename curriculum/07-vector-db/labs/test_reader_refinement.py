"""Read the new numerical examples from Markdown, then check their arithmetic.

These tests exercise no vector database, persistence, or concurrent writer.
Run together with test_numeric_lab.py using unittest discovery.
"""
from pathlib import Path
import re
import unittest

import numeric_lab as lab

DOCS = Path(__file__).parents[1] / 'docs'


def values(text):
    return tuple(float(x.strip()) for x in re.split(r'[、,]', text))


def assign_and_update(samples, centres):
    groups = [[] for _ in centres]
    for sample in samples:
        index = min(range(len(centres)), key=lambda i: (abs(sample-centres[i]), i))
        groups[index].append(sample)
    if not all(groups):
        raise ValueError('The teaching fixture requires nonempty groups')
    return tuple(sum(group)/len(group) for group in groups), groups


class ReaderRefinementTests(unittest.TestCase):
    def test_ivf_training_table(self):
        text = (DOCS / '06-IVF原理.md').read_text(encoding='utf-8')
        match = re.search(r'用一维样本 `([^`]+)` 手算，指定两个初始中心 `([^`]+)`', text)
        self.assertIsNotNone(match, 'Keep the training inputs independently visible')
        samples, centres = map(values, match.groups())
        row = re.search(r'^\| 用组内平均值更新中心 \| (.+)$', text, re.M)
        self.assertIsNotNone(row)
        expected = tuple(float(x) for x in re.findall(r'=([0-9.]+)`', row.group(1)))
        self.assertEqual(len(expected), len(centres))
        updated, groups = assign_and_update(samples, centres)
        self.assertEqual(updated, expected)
        self.assertEqual(assign_and_update(samples, updated), (updated, groups))
        self.assertEqual(tuple(x for group in groups for x in group), samples)

    def test_ivf_transfer_task(self):
        text = (DOCS / '06-IVF原理.md').read_text(encoding='utf-8')
        task = text.split('**任务 2。**', 1)[1]
        match = re.search(r'一维样本改为 `([^`]+)`，初始中心为 `([^`]+)`', task)
        self.assertIsNotNone(match)
        samples, centres = map(values, match.groups())
        answer = re.search(r'平均值为 ([0-9.]+) 和 ([0-9.]+)', task)
        self.assertIsNotNone(answer)
        updated, groups = assign_and_update(samples, centres)
        self.assertEqual(updated, tuple(map(float, answer.groups())))
        self.assertEqual(assign_and_update(samples, updated), (updated, groups))

    def test_record_update_distances(self):
        text = (DOCS / '09-Vector数据建模.md').read_text(encoding='utf-8')
        section = text.split('<a id="record-state-example"></a>', 1)[1].split('## 3.', 1)[0]
        first = re.search(r'^\| 1 \| (.+)$', section, re.M).group(1)
        third = re.search(r'^\| 3 \| (.+)$', section, re.M).group(1)
        fifth = re.search(r'^\| 5 \| (.+)$', section, re.M).group(1)
        c = values(re.search(r'`\[([^]]+)\]`', first).group(1))
        a = values(re.search(r'`\[([^]]+)\]`', third).group(1))
        query = values(re.search(r'`q=\[([^]]+)\]`', fifth).group(1))
        expected = re.search(r'A 距离为 ([0-9.]+)，C 为 ([0-9.]+)', fifth)
        self.assertAlmostEqual(lab.measure(query, a), float(expected.group(1)))
        self.assertAlmostEqual(lab.measure(query, c), float(expected.group(2)))
        rows = [{'id':'A','vector':a,'tenant_id':'alpha'},
                {'id':'C','vector':c,'tenant_id':'alpha'}]
        self.assertEqual(lab.exact_search(rows, query, 1, tenant='alpha')[0]['id'], 'C')
        task = text.split('**任务 2。**', 1)[1]
        original_a = values(re.search(r'A=`\[([^]]+)\]`', task).group(1))
        rows[0]['vector'] = original_a
        before = lab.exact_search(rows, query, 1, tenant='alpha')
        rows[0]['label'] = '待复核'
        self.assertEqual(before, lab.exact_search(rows, query, 1, tenant='alpha'))
        self.assertEqual(before[0]['id'], 'A')


if __name__ == '__main__':
    unittest.main(verbosity=2)
