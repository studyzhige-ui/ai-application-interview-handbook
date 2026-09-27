#!/usr/bin/env python3
"""Print one named example from the MySQL prose. Does not execute it."""
from pathlib import Path
import argparse
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "curriculum/04-mysql/examples"))
from mysql_course import examples

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", nargs="?")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    records = examples()
    if args.list:
        for name, item in records.items():
            print(f"{name}\t{item['file']}")
    elif args.name in records:
        print(records[args.name]["code"])
    else:
        parser.error("Use --list, or provide one listed example name")
if __name__ == "__main__":
    main()
