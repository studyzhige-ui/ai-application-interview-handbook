"""Test one byte-pinned upstream source file, not a simulated DeerFlow service.

Usage (Python >= 3.12 and Pydantic 2):
    python verify_source_config.py --source-root /path/to/deer-flow
    python verify_source_config.py --source-file /path/to/summarization_config.py

No model, network, database, or sandbox is called. Only --report writes output.
The upstream source itself is intentionally not redistributed with this lab.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import types
import io
import json
from pathlib import Path
import platform
import sys
import unittest

UPSTREAM_COMMIT = 'e2feca1e567d9bafce657de8ad8bc668bd7ad513'
SOURCE_PATH = Path('backend/packages/harness/deerflow/config/summarization_config.py')
SOURCE_BLOB = '965cd2ac12a95f912d822026de2c75dffc926922'


def load_verified_source(path: Path):
    data = path.read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
    if actual != SOURCE_BLOB:
        raise ValueError(f'Upstream bytes differ: expected {SOURCE_BLOB}, got {actual}. '
                         'Do not change the expected hash just to make this test pass.')
    # Execute exactly the verified bytes in memory: no second file read,
    # no __pycache__ written beside the upstream file.
    module = types.ModuleType('_deerflow_verified_summary_config')
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    previous = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        exec(compile(data, str(path), 'exec'), module.__dict__)
    finally:
        sys.dont_write_bytecode = previous
    return module, actual


def build_tests(source):
    from pydantic import ValidationError

    class SourceConfigTests(unittest.TestCase):
        def test_automatic_summary_is_disabled_by_class_default(self):
            config = source.SummarizationConfig()
            self.assertIs(config.enabled, False)
            self.assertIsNone(config.model_name)
            self.assertIsNone(config.trigger)

        def test_retention_default_and_summary_input_budget_are_different(self):
            config = source.SummarizationConfig()
            self.assertEqual(config.keep.to_tuple(), ('messages', 20))
            self.assertEqual(config.trim_tokens_to_summarize, 4000)

        def test_fraction_including_one_is_valid(self):
            for value in (0.01, 0.8, 1):
                with self.subTest(value=value):
                    self.assertEqual(source.ContextSize(type='fraction', value=value).value, value)

        def test_percentage_style_and_nonpositive_fractions_are_rejected(self):
            for value in (80, 0, -0.1, 1.01):
                with self.subTest(value=value), self.assertRaises(ValidationError):
                    source.ContextSize(type='fraction', value=value)

        def test_nonfinite_values_are_rejected(self):
            for kind in ('fraction', 'tokens', 'messages'):
                for value in (float('nan'), float('inf'), -float('inf')):
                    with self.subTest(kind=kind, value=str(value)), self.assertRaises(ValidationError):
                        source.ContextSize(type=kind, value=value)

        def test_message_count_must_be_positive_integer(self):
            self.assertEqual(source.ContextSize(type='messages', value=20).to_tuple(), ('messages', 20))
            for value in (0, -1, 20.5, 20.0):
                with self.subTest(value=value), self.assertRaises(ValidationError):
                    source.ContextSize(type='messages', value=value)

        def test_absolute_token_threshold_is_positive(self):
            self.assertEqual(source.ContextSize(type='tokens', value=4000).value, 4000)
            for value in (0, -1):
                with self.subTest(value=value), self.assertRaises(ValidationError):
                    source.ContextSize(type='tokens', value=value)

        def test_unknown_threshold_kind_is_rejected(self):
            with self.assertRaises(ValidationError):
                source.ContextSize(type='percent', value=80)

        def test_explicit_configuration_is_not_a_claim_about_running_service(self):
            config = source.SummarizationConfig(
                enabled=True,
                trigger={'type': 'tokens', 'value': 32000},
                keep={'type': 'messages', 'value': 12},
            )
            self.assertTrue(config.enabled)
            self.assertEqual(config.trigger.to_tuple(), ('tokens', 32000))
            self.assertEqual(config.keep.to_tuple(), ('messages', 12))

        def test_mutable_default_lists_are_not_shared(self):
            a, b = source.SummarizationConfig(), source.SummarizationConfig()
            a.skill_file_read_tool_names.append('test_only_reader')
            self.assertNotIn('test_only_reader', b.skill_file_read_tool_names)

    return unittest.defaultTestLoader.loadTestsFromTestCase(SourceConfigTests)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    location = parser.add_mutually_exclusive_group(required=True)
    location.add_argument('--source-root', type=Path)
    location.add_argument('--source-file', type=Path)
    parser.add_argument('--report', type=Path, help='Optional JSON report path.')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error('Python >= 3.12 is required; no silent fallback to another version.')
    path = args.source_file or args.source_root / SOURCE_PATH
    try:
        pydantic_version = importlib.metadata.version('pydantic')
        if int(pydantic_version.split('.')[0]) != 2:
            raise RuntimeError(f'Pydantic 2 is required; installed {pydantic_version}')
        source, actual_blob = load_verified_source(path)
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(build_tests(source))
    except (OSError, ImportError, ValueError, RuntimeError) as exc:
        print(f'NOT RUN: {exc}', file=sys.stderr)
        return 2
    report = {
        'scope': 'byte-pinned upstream summarization_config.py only',
        'upstream_commit': UPSTREAM_COMMIT,
        'source_path': SOURCE_PATH.as_posix(),
        'verified_git_blob': actual_blob,
        'python': platform.python_version(),
        'pydantic': pydantic_version,
        'dependency_environment': 'local source-file test environment, not the full upstream uv.lock environment',
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped),
        'success': result.wasSuccessful(),
        'not_tested': ['agent assembly', 'summary generation', 'provider payload', 'memory queue',
                       'database durability', 'MCP', 'sandbox', 'end-to-end service'],
        'unittest_output': stream.getvalue(),
    }
    print(stream.getvalue(), end='')
    print(json.dumps({key: value for key, value in report.items() if key != 'unittest_output'},
                     ensure_ascii=False, indent=2))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
