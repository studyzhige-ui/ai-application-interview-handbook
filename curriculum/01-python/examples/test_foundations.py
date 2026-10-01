"""Offline checks of teaching snippets; no user files, services, or model calls.

Run from the repository root:
    python -m unittest discover -s curriculum/01-python/examples -v
"""
import ast
import asyncio
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
import unittest

MODULE = Path(__file__).resolve().parents[1]
ROOT = MODULE.parents[1]


def blocks(path):
    return re.findall(r"```python\n(.*?)\n```", path.read_text(), re.S)


def snippet(number, marker):
    path = next((MODULE / "docs").glob(number + "*.md"))
    found = [code for code in blocks(path) if marker in code]
    if len(found) != 1:
        raise AssertionError((path, marker, len(found)))
    return found[0]


def execute(code):
    namespace = {}
    with redirect_stdout(StringIO()):
        exec(compile(code, "<teaching-snippet>", "exec"), namespace)
    return namespace


class FoundationExamples(unittest.TestCase):
    def test_all_body_python_blocks_parse(self):
        for path in sorted((MODULE / "docs").glob("*.md")):
            for number, code in enumerate(blocks(path), 1):
                with self.subTest(path=path.name, block=number):
                    ast.parse(code)

    def test_scalar_and_text_blocks(self):
        for marker in ['print(7 / 2)', 'from decimal import Decimal', 'raw = "  Python']:
            execute(snippet("02", marker))
        self.assertEqual((-7 // 2, -7 % 2), (-4, 1))
        result = execute(snippet("02", 'raw = "  Python'))
        self.assertEqual(result['parts'], ['Python', ' API', '  数据'])
        self.assertEqual(result['raw'], '  Python, API,  数据  ')

    def test_recursive_call_and_return(self):
        result = execute(snippet("04", 'def total_to'))
        for value, expected in [(0, 0), (1, 1), (3, 6), (10, 55)]:
            self.assertEqual(result['total_to'](value), expected)

    def test_type_hint_default_are_separate(self):
        result = execute(snippet("04", 'def required'))
        self.assertIsNone(result['required'](None))
        self.assertIsNone(result['optional']())
        with self.assertRaises(TypeError):
            result['required']()
        names = execute(snippet("04", 'def first_name'))
        self.assertIsNone(names['first_name']([]))
        self.assertEqual(names['first_name'](['A']), 'A')

    def test_stable_sort_preserves_equal_key_order(self):
        result = execute(snippet("05", 'users = [("A", 20)'))
        self.assertEqual(sorted(result['users'], key=lambda item: item[1]),
                         [('B', 18), ('A', 20), ('C', 20)])

    def test_property_precedes_instance_dictionary(self):
        result = execute(snippet("08", '@age.setter'))
        person = result['p']
        person.__dict__['age'] = 999
        self.assertEqual(person.age, 21)
        with self.assertRaises(ValueError):
            person.age = -1
        self.assertEqual(person.age, 21)

    def test_mro_attribute_is_resolved_before_descriptor_precedence(self):
        class Base:
            @property
            def value(self):
                return 1
        read_only = Base()
        read_only.__dict__['value'] = 99
        self.assertEqual(read_only.value, 1)
        with self.assertRaises(AttributeError):
            read_only.value = 2
        class Child(Base):
            value = 10  # First MRO match shadows the inherited descriptor.
        child = Child()
        child.value = 20
        self.assertEqual(child.value, 20)
        self.assertEqual(child.__dict__['value'], 20)

    def test_value_key_hash_contract(self):
        result = execute(snippet("08", 'class ItemKey'))
        left, right = result['left'], result['right']
        self.assertEqual(left, right)
        self.assertEqual(hash(left), hash(right))
        self.assertEqual({left: 'found'}[right], 'found')
        with self.assertRaises(TypeError):
            left[0] = 'other'

    def test_async_iteration_and_group(self):
        result = execute(snippet("12", 'async def chunks'))
        async def collect():
            return [item async for item in result['chunks']()]
        self.assertEqual(asyncio.run(collect()), ['你', '好'])
        execute(snippet("12", 'raise ExceptionGroup'))

    def test_queue_slot_released_at_get_not_task_done(self):
        async def check():
            queue = asyncio.Queue(maxsize=2)
            await queue.put('A')
            await queue.put('B')
            with self.assertRaises(asyncio.QueueFull):
                queue.put_nowait('C')
            self.assertEqual(await queue.get(), 'A')
            queue.put_nowait('C')  # No task_done yet, but get released the slot.
            queue.task_done()
            self.assertEqual(await queue.get(), 'B')
            queue.task_done()
            self.assertEqual(await queue.get(), 'C')
            queue.task_done()
            await queue.join()
        asyncio.run(check())

    def test_practice_nested_dictionary_contract(self):
        path = ROOT / 'practice/python-basics/Python高频Coding小题.md'
        code = next(code for code in blocks(path) if 'def read_city' in code)
        read = execute(code)['read_city']
        for value in [{}, {'address': None}, {'address': {}}, {'address': {'city': None}}]:
            self.assertIsNone(read(value))
        self.assertEqual(read({'address': {'city': '上海'}}), '上海')
        for value in [None, [], {'address': []}, {'address': 0}, {'address': {'city': 1}}]:
            with self.assertRaises(TypeError):
                read(value)

    def test_corrected_default_example_returns_result(self):
        path = MODULE / 'interview/面试易错点.md'
        code = next(code for code in blocks(path) if 'def add(x, items=None)' in code)
        add = execute(code)['add']
        self.assertEqual(add(1), [1])
        self.assertEqual(add(2), [2])
        passed = []
        self.assertIs(add(3, passed), passed)
        self.assertEqual(passed, [3])


if __name__ == '__main__':
    unittest.main()
