#!/usr/bin/env python3
"""Extract one named teaching example; refuses accidental overwrites."""
from pathlib import Path
import argparse
import re


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--overwrite',action='store_true')
    args=parser.parse_args()
    docs=Path(__file__).resolve().parents[1]/'curriculum/02-fastapi/docs'
    found=[]
    for path in sorted(docs.glob('*.md')):
        for code in re.findall(r'```python\n(.*?)\n```',path.read_text(encoding="utf-8"),re.S):
            if code.splitlines()[0]==f'# example: {args.name}':found.append(code)
    if len(found)!=1:parser.error(f'Expected one example named {args.name!r}, found {len(found)}')
    if args.output.exists() and not args.overwrite:parser.error(f'Output exists: {args.output}')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(found[0]+'\n', encoding='utf-8')
    print(args.output)

if __name__=='__main__':main()
