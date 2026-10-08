#!/usr/bin/env python3
"""Minimal official-JD business interface. Network collection is explicit."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parent


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


def collect(live):
    if not live:
        raise ValueError("Live collection requires --live; use check for offline verification")
    # Fail before changing a current snapshot if the live dependencies are absent.
    import requests  # noqa: F401
    from jd.evidence import preserve_current
    from jd.pipeline import main as pipeline
    from jd.audit import main as audit
    preserve_current()
    adapters = SCRIPTS / "jd/adapters"
    subprocess.run(["node", str(adapters / "browser.mjs")], check=True)
    for name in ("xiaomi", "bytedance", "feishu", "moka"):
        result = subprocess.run(["node", str(adapters / f"{name}.mjs")], check=False)
        if result.returncode:
            print(f"{name} accelerator failed; only fresh complete alternatives may be used", file=sys.stderr)
    pipeline()
    preserve_current()
    return audit()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Offline contracts, unit tests, and Node syntax/regressions")
    commands.add_parser("collect", help="Collect, normalize, preserve, render, and audit").add_argument("--live", action="store_true")
    commands.add_parser("audit", help="Audit saved snapshots and refresh local analysis, without network")
    commands.add_parser("publish", help="Actions-only stale-safe publication of generated output")
    args = parser.parse_args()
    if args.command == "check":
        return check()
    if args.command == "collect":
        return collect(args.live)
    if args.command == "audit":
        from jd.audit import main as audit
        return audit()
    from jd.publication import main as publish
    return publish()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
