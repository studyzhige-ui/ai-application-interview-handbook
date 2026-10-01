#!/usr/bin/env python3
"""Run the handbook's bounded offline course checks in isolated processes.

These tests check teaching snippets, numerical examples and explicit local models.
They do not connect to MySQL, Redis, vector databases, model APIs or product runtimes.
FastAPI's target-version/local-network suite is run separately in its declared environment.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    ('Python foundations', ['-m', 'unittest', 'discover', '-s', 'curriculum/01-python/examples', '-p', 'test_*.py', '-v']),
    ('Redis offline models', ['-m', 'unittest', 'discover', '-s', 'curriculum/04-redis/examples', '-p', 'test_offline.py', '-v']),
    ('Backend mechanisms', ['-m', 'unittest', 'discover', '-s', 'curriculum/05-backend-engineering/examples', '-p', 'test_*.py', '-v']),
    ('LLM numerical examples', ['curriculum/06-llm-foundation/labs/test_examples.py', '-v']),
    ('Vector numerical models', ['-m', 'unittest', 'discover', '-s', 'curriculum/07-vector-db/labs', '-p', 'test_*.py', '-v']),
    ('RAG examples', ['-m', 'unittest', 'discover', '-s', 'curriculum/08-rag/examples', '-p', 'test_*.py', '-v']),
    ('System Design models', ['-m', 'unittest', 'discover', '-s', 'curriculum/10-system-design/review', '-p', 'test_*.py', '-v']),
]


def main():
    for label, arguments in SUITES:
        print(f'\n=== {label} ===', flush=True)
        result = subprocess.run([sys.executable, *arguments], cwd=ROOT)
        if result.returncode:
            return result.returncode
    print('\nOffline course suites passed; no live-service or product validation claimed.', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
