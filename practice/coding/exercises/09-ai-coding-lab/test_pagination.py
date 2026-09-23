"""此测试在初始缺陷实现上应失败；修复后应全部通过。"""
import unittest
from pagination import paginate


class PaginationTests(unittest.TestCase):
    def test_first_page(self):
        self.assertEqual(paginate([10, 20, 30]), [10, 20])

    def test_second_page(self):
        self.assertEqual(paginate([10, 20, 30], page=2), [30])

    def test_beyond_end(self):
        self.assertEqual(paginate([10], page=9), [])

    def test_empty(self):
        self.assertEqual(paginate([]), [])

    def test_page_bounds(self):
        for page in [0, -1, True, 1.5, "1", None]:
            self.assertRaises(ValueError, paginate, [10, 20], page=page)

    def test_size_bounds(self):
        for size in [0, -1, 6, True, 2.5, "2", None]:
            self.assertRaises(ValueError, paginate, [10, 20], page_size=size)

    def test_size_endpoints(self):
        self.assertEqual(paginate([1, 2, 3], page_size=1), [1])
        self.assertEqual(paginate([1, 2, 3], page_size=5), [1, 2, 3])

    def test_does_not_mutate_input(self):
        items = [10, 20, 30]
        result = paginate(items)
        self.assertEqual(items, [10, 20, 30])
        self.assertIsNot(result, items)


if __name__ == "__main__":
    unittest.main()
