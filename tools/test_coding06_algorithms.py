#!/usr/bin/env python3
"""Regression checks for the algorithms printed in Coding 06.

Execute the actual trusted chapter examples, then compare their functions with
small independent references. These checks validate behavior, not readability.
No generated teaching files or student exercises are changed.
"""
from __future__ import annotations

import bisect
import itertools
import math
from pathlib import Path
import re
import unittest

CHAPTER = (Path(__file__).resolve().parents[1] /
           "practice/coding/docs/06-problem-solving-and-algorithms.md")


def sequences(values, maximum):
    for length in range(maximum + 1):
        yield from itertools.product(values, repeat=length)


class Coding06Algorithms(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples = {}
        text = CHAPTER.read_text(encoding="utf-8")
        blocks = re.findall(r"```python\n(.*?)\n```", text, re.S)
        for index, code in enumerate(blocks, 1):
            namespace = {}
            exec(compile(code, f"{CHAPTER.name}:block-{index}", "exec"), namespace)
            cls.examples.update(namespace)
        cls.block_count = len(blocks)

    def test_examples_are_independently_executable(self):
        self.assertGreater(self.block_count, 0)

    def test_two_sum_distinct_positions_and_absent_pair(self):
        solve = self.examples["two_sum"]
        for nums in sequences((-1, 0, 1), 5):
            for target in range(-2, 3):
                pairs = [(i, j) for i in range(len(nums))
                         for j in range(i + 1, len(nums))
                         if nums[i] + nums[j] == target]
                result = solve(list(nums), target)
                if not pairs:
                    self.assertEqual(result, [])
                else:
                    self.assertEqual(len(result), 2)
                    i, j = result
                    self.assertTrue(0 <= i < j < len(nums))
                    self.assertEqual(nums[i] + nums[j], target)

    def test_longest_consecutive_matches_sorted_runs(self):
        solve = self.examples["longest_consecutive"]
        for nums in sequences((-2, -1, 0, 2), 5):
            ordered = sorted(set(nums))
            expected = run = 0
            previous = None
            for value in ordered:
                run = run + 1 if previous is not None and value == previous + 1 else 1
                expected = max(expected, run)
                previous = value
            self.assertEqual(solve(list(nums)), expected)

    def test_palindrome_and_stable_in_place_move(self):
        palindrome = self.examples["is_palindrome"]
        move = self.examples["move_zeroes"]
        for chars in sequences("ab", 7):
            text = "".join(chars)
            self.assertEqual(palindrome(text), text == text[::-1])
        for original in sequences((-1, 0, 2), 6):
            nums = list(original)
            identity = id(nums)
            expected = [x for x in original if x != 0] + [0] * original.count(0)
            self.assertIsNone(move(nums))
            self.assertEqual(id(nums), identity)
            self.assertEqual(nums, expected)

    def test_unique_window_matches_all_substrings(self):
        solve = self.examples["longest_unique"]
        for chars in sequences("abc", 7):
            text = "".join(chars)
            expected = max((right - left
                            for left in range(len(text) + 1)
                            for right in range(left, len(text) + 1)
                            if len(set(text[left:right])) == right - left), default=0)
            self.assertEqual(solve(text), expected, text)

    def test_prefix_counts_negative_zero_and_repeated_boundaries(self):
        solve = self.examples["subarray_sum"]
        for nums in sequences((-1, 0, 1), 6):
            for target in range(-2, 3):
                expected = sum(sum(nums[left:right]) == target
                               for left in range(len(nums))
                               for right in range(left + 1, len(nums) + 1))
                self.assertEqual(solve(list(nums), target), expected, (nums, target))

    def test_binary_search_strictly_increasing_contract(self):
        solve = self.examples["search_insert"]
        for length in range(6):
            for nums in itertools.combinations(range(-3, 4), length):
                for target in range(-4, 5):
                    self.assertEqual(solve(list(nums), target), bisect.bisect_left(nums, target))

    def test_temperature_stack_matches_forward_scan(self):
        solve = self.examples["daily_temperatures"]
        for temperatures in sequences((1, 2, 3), 6):
            expected = [next((j - i for j in range(i + 1, len(temperatures))
                              if temperatures[j] > temperature), 0)
                        for i, temperature in enumerate(temperatures)]
            self.assertEqual(solve(list(temperatures)), expected)

    def test_recursive_returns_traversal_and_original_tree_identity(self):
        for n in range(30):
            self.assertEqual(self.examples["sum_to"](n), n * (n + 1) // 2)
        node = self.examples["TreeNode"]
        depth = self.examples["max_depth"]
        inorder = self.examples["inorder"]
        invert = self.examples["invert_tree"]
        self.assertEqual(depth(None), 0)
        self.assertEqual(inorder(None), [])
        self.assertIsNone(invert(None))
        root = node(4, node(2, node(1), node(3)), node(5, None, node(6)))
        before = inorder(root)
        self.assertEqual(depth(root), 3)
        self.assertIs(invert(root), root)
        self.assertEqual(inorder(root), before[::-1])
        self.assertEqual(depth(root), 3)
        self.assertIs(invert(root), root)
        self.assertEqual(inorder(root), before)
        chain = None
        for value in range(20):
            chain = node(value, chain)
        self.assertEqual(depth(chain), 20)

    def test_islands_match_union_find_and_documented_mutation(self):
        solve = self.examples["num_islands"]
        self.assertEqual(solve([]), 0)
        self.assertEqual(solve([[]]), 0)
        for rows, cols in ((1, 1), (1, 4), (2, 2), (2, 3), (3, 2)):
            for cells in itertools.product("01", repeat=rows * cols):
                parent = {i: i for i, value in enumerate(cells) if value == "1"}

                def root(i):
                    while parent[i] != i:
                        i = parent[i]
                    return i

                for i in parent:
                    row, col = divmod(i, cols)
                    for neighbor in ((i + 1,) if col + 1 < cols else ()) + (
                            (i + cols,) if row + 1 < rows else ()):
                        if neighbor in parent:
                            parent[root(i)] = root(neighbor)
                expected = len({root(i) for i in parent})
                grid = [list(cells[r * cols:(r + 1) * cols]) for r in range(rows)]
                self.assertEqual(solve(grid), expected)
                self.assertTrue(all(value == "0" for row in grid for value in row))

    def test_bfs_cycles_reachability_and_distance_order(self):
        solve = self.examples["bfs"]
        edges = [(a, b) for a in range(3) for b in range(3) if a != b]
        for flags in itertools.product((False, True), repeat=len(edges)):
            graph = {i: [] for i in range(3)}
            distances = [[0 if i == j else math.inf for j in range(3)] for i in range(3)]
            for (a, b), included in zip(edges, flags):
                if included:
                    graph[a].append(b)
                    distances[a][b] = 1
            for via in range(3):
                for a in range(3):
                    for b in range(3):
                        distances[a][b] = min(distances[a][b], distances[a][via] + distances[via][b])
            for start in range(3):
                order = solve(graph, start)
                expected = {i for i in range(3) if distances[start][i] < math.inf}
                self.assertEqual(set(order), expected)
                self.assertEqual(len(order), len(expected))
                levels = [distances[start][i] for i in order]
                self.assertEqual(levels, sorted(levels))
        self.assertEqual(solve({}, 9), [9])

    def test_permutations_complete_unique_and_independent_results(self):
        solve = self.examples["permutations"]
        for n in range(7):
            nums = list(range(n))
            result = solve(nums)
            expected = list(itertools.permutations(nums))
            self.assertEqual([tuple(item) for item in result], expected)
            self.assertEqual(len({id(item) for item in result}), len(result))
            self.assertEqual(nums, list(range(n)))

    def test_top_k_duplicates_and_all_valid_k(self):
        solve = self.examples["kth_largest"]
        for nums in sequences((-1, 0, 2), 6):
            for k in range(1, len(nums) + 1):
                self.assertEqual(solve(list(nums), k), sorted(nums, reverse=True)[k - 1])

    def test_stock_matches_all_date_pairs(self):
        solve = self.examples["max_profit"]
        for prices in sequences((1, 2, 4), 6):
            expected = max([0] + [prices[j] - prices[i] for i in range(len(prices))
                                  for j in range(i + 1, len(prices))])
            self.assertEqual(solve(list(prices)), expected)

    def test_dp_table_and_compact_match_counting_step_arrangements(self):
        table = self.examples["climb_stairs"]
        compact = self.examples["climb_stairs_compact"]
        for n in range(1, 60):
            # With t two-step moves, n-t total moves contain t selected slots.
            expected = sum(math.comb(n - t, t) for t in range(n // 2 + 1))
            self.assertEqual(table(n), expected)
            self.assertEqual(compact(n), expected)


if __name__ == "__main__":
    unittest.main()
