#!/usr/bin/env python3
"""Check main's 23-chapter reader revision; not a semantic-quality verdict.

By default this reads files only. --run-examples explicitly runs four reviewed,
standard-library teaching examples in separate Python subprocesses, with a
five-second timeout. They use in-memory fake services, not real providers.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MODULES = {'python':13, 'fastapi':16, 'backend-engineering':22, 'mysql':23,
           'redis':24, 'vector-db':16, 'llm-foundation':14, 'rag':14,
           'agent-harness':23, 'system-design':19}
EXAMPLES = {'minimal_feedback_loop', 'registry_projection',
            'append_and_plan_view', 'recovery_window'}


def split_fences(text: str):
    """Return prose and (language, code) blocks, rejecting unclosed fences."""
    prose, blocks, code = [], [], []
    opening = None
    language = ''
    for line in text.splitlines():
        if opening is None:
            m = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
            if m:
                opening = m.group(1)
                language = m.group(2).strip().split(' ', 1)[0]
                code = []
            else:
                prose.append(line)
        elif re.fullmatch(r'\s*' + re.escape(opening[0]) +
                          '{' + str(len(opening)) + r',}\s*', line):
            blocks.append((language, '\n'.join(code) + '\n'))
            opening = None
        else:
            code.append(line)
    if opening:
        raise ValueError('unclosed code fence')
    return '\n'.join(prose), blocks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-examples', action='store_true')
    args = parser.parse_args()
    errors = []
    docs = sorted((ROOT / 'agent-harness/docs').glob('*.md'))
    if [p.name[:2] for p in docs] != [f'{n:02}' for n in range(1,24)]:
        errors.append('Agent chapter numbering/count mismatch')
    home = (ROOT / 'agent-harness/README.md').read_text(encoding='utf-8')
    interview_count = quiz_count = pitfall_count = 0
    actual_ids = set()
    examples = {}
    for p in docs:
        text = p.read_text(encoding='utf-8')
        if not text.startswith('# ' + p.name[:2] + '.'):
            errors.append(f'{p.name}: H1 does not match filename')
        if f'](docs/{p.name})' not in home:
            errors.append(f'{p.name}: missing README link')
        headings = ['## 面试怎么答', '## 高频易错点', '## 章节自测', '## 资料与下一步']
        positions = [text.find(h) for h in headings]
        if min(positions) < 0 or positions != sorted(positions):
            errors.append(f'{p.name}: missing/out-of-order chapter endcaps')
            continue
        interviews = text[positions[0]:positions[1]]
        quizzes = text[positions[2]:positions[3]]
        iq = len(re.findall(r'^### \d+\.', interviews, re.M))
        sq = len(re.findall(r'^### 自测 \d+：', quizzes, re.M))
        if iq < 4 or sq < 6:
            errors.append(f'{p.name}: insufficient local training coverage {iq}/{sq}')
        interview_count += iq
        quiz_count += sq
        rows = [line for line in text[positions[1]:positions[2]].splitlines()
                if line.startswith('|')]
        pitfall_count += max(0, len(rows)-2)
        for section, count in [(interviews, iq), (quizzes, sq)]:
            if section.count('<details>') != count:
                errors.append(f'{p.name}: answers must be locally collapsed')
        if re.search(r'<details\s+open\b', text) or text.count('<details>') != text.count('</details>'):
            errors.append(f'{p.name}: invalid or default-open details')
        actual_ids.update(re.findall(r'`(AGENT-\d{3})`', text))
        try:
            _, blocks = split_fences(text)
            for language, code in blocks:
                if language == 'python':
                    ast.parse(code, filename=p.name)
                match = re.search(r'^# runnable-example: (\w+)\s*$', code, re.M)
                if match:
                    name = match.group(1)
                    if name not in EXAMPLES or name in examples:
                        errors.append('unknown or duplicate executable example: ' + name)
                    examples[name] = code
        except (ValueError, SyntaxError) as exc:
            errors.append(f'{p.name}: {exc}')
    qtext=(ROOT/'research/questions/agent-harness.md').read_text(encoding='utf-8')
    expected_ids = set(re.findall(r'^###\s+(AGENT-\d{3})\s+·', qtext, re.M))
    if len(expected_ids) != 44 or actual_ids != expected_ids:
        errors.append(f'Canonical map mismatch: missing {expected_ids-actual_ids}, extra {actual_ids-expected_ids}')
    total = 0
    for module, expected in MODULES.items():
        count = len(list((ROOT/module/'docs').glob('*.md')))
        total += count
        if count != expected:
            errors.append(f'{module}: expected {expected}, found {count}')
    if set(examples) != EXAMPLES:
        errors.append('teaching examples missing: ' + str(EXAMPLES-set(examples)))

    # Ordinary inline local Markdown file links. External URLs and generated
    # GitHub heading slugs are deliberately not claimed as verified here.
    checked = 0
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts:
            continue
        try:
            prose, _ = split_fences(p.read_text(encoding='utf-8'))
        except ValueError as exc:
            errors.append(f'{p.relative_to(ROOT)}: {exc}')
            continue
        for target in re.findall(r'(?<!!)\[[^\]\n]*\]\(([^\n)]+)\)', prose):
            target = target.strip().split(' "',1)[0].strip('<>')
            if not target or target.startswith(('#','http:','https:','mailto:','data:')):
                continue
            target = unquote(target.split('#',1)[0].split('?',1)[0])
            if not target:
                continue
            dest = ROOT/target.lstrip('/') if target.startswith('/') else p.parent/target
            checked += 1
            if not dest.exists():
                errors.append(f'{p.relative_to(ROOT)} -> {target}: missing local file')
    highfreq = (ROOT/'agent-harness/interview/高频面试题.md').read_text(encoding='utf-8')
    if len(re.findall(r'^### \d+\.', highfreq, re.M)) != 56:
        errors.append('legacy centralized 56-question set not retained')
    print(f'Agent chapters: {len(docs)}; curriculum: {total}; Canonical: {len(expected_ids)}')
    print(f'Chapter interviews: {interview_count}; self-tests: {quiz_count}; pitfall rows: {pitfall_count}')
    print(f'Inline local file links checked: {checked}; errors: {len(errors)}')
    if errors:
        print('\n'.join(errors))
        return 1
    if args.run_examples:
        for name, code in examples.items():
            with tempfile.TemporaryDirectory(prefix='agent-teaching-') as d:
                p=Path(d)/'example.py';p.write_text(code, encoding='utf-8')
                subprocess.run([sys.executable, '-I', str(p)], cwd=d,
                               timeout=5, check=True)
            print('Executed teaching example:', name)
    print('PASS: document structure, file navigation, training presence, Canonical mapping and Python syntax.')
    print('Not a claim of complete external-link/rendering validation, reader comprehension, or production reliability.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
