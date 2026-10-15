#!/usr/bin/env python3
"""Official JD integrity, bounded collection, and GitHub-native incremental scanning."""
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


def nonnegative_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be non-negative")
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

    scan = commands.add_parser("scan", help="Collect one deterministic automation shard; source failures remain data")
    scan.add_argument("--shard-index", type=nonnegative_int, required=True)
    scan.add_argument("--shard-count", type=positive_int, required=True)
    scan.add_argument("--max-pages", type=positive_int, required=True)
    scan.add_argument("--max-jobs", type=positive_int, required=True)
    scan.add_argument("--timeout-seconds", type=positive_number, required=True)
    scan.add_argument("--output-dir", type=Path, required=True)

    reconcile = commands.add_parser("reconcile", help="Merge scan artifacts into baseline, pending review queue and status report")
    reconcile.add_argument("--input-dir", type=Path, required=True)
    reconcile.add_argument("--state-file", type=Path, required=True)
    reconcile.add_argument("--queue-file", type=Path, required=True)
    reconcile.add_argument("--report-file", type=Path, required=True)

    prepare_audit = commands.add_parser("prepare-audit", help="Export a small deterministic pending-JD batch for semantic review")
    prepare_audit.add_argument("--queue-file", type=Path, required=True)
    prepare_audit.add_argument("--batch-file", type=Path, required=True)
    prepare_audit.add_argument("--limit", type=positive_int, default=24)

    apply_audit = commands.add_parser("apply-audit", help="Mechanically apply completed semantic review decisions")
    apply_audit.add_argument("--queue-file", type=Path, required=True)
    apply_audit.add_argument("--decisions-file", type=Path, required=True)
    apply_audit.add_argument("--official-file", type=Path, required=True)
    apply_audit.add_argument("--bytedance-file", type=Path, required=True)
    apply_audit.add_argument("--index-file", type=Path, required=True)

    args = parser.parse_args(argv)
    if not args.command:
        print("Use check/sources for offline inspection, collect for manual capture, scan/reconcile for collection, or prepare-audit/apply-audit for semantic review.")
        return 0
    if args.command == "check":
        return check()
    if args.command == "sources":
        from jd.collection import registry
        for source_id, source in registry().items():
            print(f"{source_id}\t{source['company']}\t{source['portal']}")
        return 0
    if args.command == "collect":
        from jd.collection import collect_manual
        return collect_manual(
            args.source_id,
            enabled=args.enable_code_collection,
            max_pages=args.max_pages,
            max_jobs=args.max_jobs,
            timeout_seconds=args.timeout_seconds,
            output=args.output_dir,
        )
    if args.command == "scan":
        from jd.automation import scan_shard
        return scan_shard(
            shard_index=args.shard_index,
            shard_count=args.shard_count,
            max_pages=args.max_pages,
            max_jobs=args.max_jobs,
            timeout_seconds=args.timeout_seconds,
            output=args.output_dir,
        )
    if args.command == "prepare-audit":
        from jd.review import prepare_batch
        batch = prepare_batch(queue_file=args.queue_file, batch_file=args.batch_file, limit=args.limit)
        print(f"Prepared semantic audit batch={batch['batch_id']} count={batch['count']} pending={batch['pending_total']}")
        return 0
    if args.command == "apply-audit":
        from jd.review import apply_decisions
        result = apply_decisions(
            queue_file=args.queue_file,
            decisions_file=args.decisions_file,
            official_file=args.official_file,
            bytedance_file=args.bytedance_file,
            index_file=args.index_file,
        )
        print("Applied semantic audit " + " ".join(f"{key}={value}" for key, value in result.items()))
        return 0
    from jd.automation import reconcile as reconcile_run
    summary = reconcile_run(
        input_dir=args.input_dir,
        state_file=args.state_file,
        queue_file=args.queue_file,
        report_file=args.report_file,
    )
    print(f"Reconciled sources={summary['results']}, new events={sum(summary['counts'].get(k, 0) for k in ('added','changed','possibly_removed'))}, pending={summary['pending']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
