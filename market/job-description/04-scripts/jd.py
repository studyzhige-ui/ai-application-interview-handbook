#!/usr/bin/env python3
"""Stored JD integrity checks; collection is disabled unless explicitly bounded."""
from __future__ import annotations
import argparse
import math
from pathlib import Path
import subprocess
import sys
import unittest

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def positive_number(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be finite and positive")
    return number


def check():
    from jd.contracts import main as contracts
    if contracts():
        return 1
    suite = unittest.defaultTestLoader.discover(str(SCRIPTS / "tests"), pattern="test_*.py")
    if not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
        return 1
    for path in sorted((SCRIPTS / "jd/adapters").glob("*.mjs")):
        subprocess.run(["node", "--check", str(path)], check=True)
    subprocess.run(["node", "--test", str(SCRIPTS / "tests/test_browser.mjs")], check=True)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("check", help="Read-only offline integrity, counts, syntax and fixture tests")
    commands.add_parser("sources", help="List registered source IDs without network access")
    collect = commands.add_parser("collect", help="Explicit bounded capture into a new directory; never publishes")
    collect.add_argument("--enable-code-collection", action="store_true", required=True)
    collect.add_argument("--source-id", action="append", required=True)
    collect.add_argument("--max-pages", type=positive_int, required=True)
    collect.add_argument("--max-jobs", type=positive_int, required=True)
    collect.add_argument("--timeout-seconds", type=positive_number, required=True)
    collect.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    if not args.command:
        print("Code collection is disabled. Use check or sources for offline inspection.")
        return 0
    if args.command == "check":
        return check()
    if args.command == "sources":
        from jd.collection import registry
        for source_id, source in registry().items():
            print(f"{source_id}\t{source['company']}\t{source['portal']}")
        return 0
    from jd.collection import collect_manual
    return collect_manual(args.source_id, enabled=args.enable_code_collection,
                          max_pages=args.max_pages, max_jobs=args.max_jobs,
                          timeout_seconds=args.timeout_seconds, output=args.output_dir)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
