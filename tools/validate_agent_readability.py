#!/usr/bin/env python3
"""Validate Agent structure, mappings, links and explicitly bounded examples.

The checks are NOT a claim of readability, model quality or production reliability.
--run-examples executes only the two named local standard-library examples.
"""
from __future__ import annotations
import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from sync_agent_materials import build
from sync_outer_navigation import anchors, inventory, markdown_links, resolve, validation_paths

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'curriculum/09-agent'
ALLOWED_EXAMPLES = {'feedback_loop', 'registry_projection'}
ENDCAPS = ['## 本章小结', '## 🎯 面试怎么回答', '## ⚠️ 易错点', '## 本章自测', '## 知识回看与权威资料']
MAP = 'guide/project/agent-clarity-mapping-2026-09-28.json'


def split_fences(text: str):
    prose = []; blocks = []; opening = None; code = []; lang = ''
    for line in text.splitlines():
        if opening is None:
            match = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
            if match:
                opening = match[1]; lang = match[2].strip().split(' ', 1)[0]; code = []
            else:
                prose.append(line)
        elif re.fullmatch(r'\s*' + re.escape(opening[0]) + '{' + str(len(opening)) + r',}\s*', line):
            blocks.append((lang, '\n'.join(code) + '\n')); opening = None
        else:
            code.append(line)
    if opening:
        raise ValueError('unclosed code fence')
    return '\n'.join(prose), blocks


def chapter_errors(text: str, number: int) -> list[str]:
    errors = []
    if not text.startswith(f'# {number:02d}. '):
        errors.append('H1 number mismatch')
    try:
        prose, blocks = split_fences(text)
    except ValueError as exc:
        return [str(exc)]
    positions = [prose.find(h) for h in ENDCAPS]
    if min(positions) < 0 or positions != sorted(positions):
        errors.append('missing or unordered teaching endcaps')
        return errors
    if any(prose.count(h) != 1 for h in ENDCAPS):
        errors.append('duplicated teaching endcap')
    if re.search(r'HUMAN-A|AGENT-\d{3}|Tier [ABCD]|S\d{3}', re.sub(r'<[^>]*>', '', prose)):
        errors.append('evidence identifiers or governance labels leaked into teaching prose')
    if re.search(r'\{\{[a-z_]+\}\}', text):
        errors.append('unresolved draft placeholder')
    qa = prose[positions[1]:positions[2]]
    pitfalls = prose[positions[2]:positions[3]]
    quiz = prose[positions[3]:positions[4]]
    if '<details' in qa or '<details' in pitfalls:
        errors.append('core interview/pitfall explanations are hidden')
    if len(re.findall(r'^### ', qa, re.M)) < 2:
        errors.append('insufficient distinct interview questions')
    if len(re.findall(r'^> ⚠️', pitfalls, re.M)) < 3:
        errors.append('missing localizable pitfalls')
    questions = re.findall(r'<details>\s*<summary>(\d+)\.\s*(.*?)</summary>(.*?)</details>', quiz, re.S)
    if len(questions) < 3 or [int(q[0]) for q in questions] != list(range(1, len(questions) + 1)):
        errors.append('self-test numbers or folded answers invalid')
    if any(not answer.strip() for _, _, answer in questions):
        errors.append('empty self-test answer')
    if text.count('<details>') != text.count('</details>') or re.search(r'<details\s+open', text):
        errors.append('unbalanced or default-open details')
    ids = re.findall(r'<a\s+id="([^"]+)"', text)
    if len(ids) != len(set(ids)):
        errors.append('duplicate explicit anchor')
    if not re.search(r'^## 1\. ', prose, re.M):
        errors.append('missing substantive numbered explanation')
    for lang, code in blocks:
        if lang == 'python':
            try:
                ast.parse(code)
            except SyntaxError as exc:
                errors.append(str(exc))
        if lang == 'json':
            try:
                json.loads(code)
            except ValueError as exc:
                errors.append('invalid JSON example: ' + str(exc))
    return errors


def collect_examples(docs: list[Path]) -> dict[str, str]:
    examples = {}
    for p in docs:
        _, blocks = split_fences(p.read_text(encoding='utf-8'))
        for lang, code in blocks:
            marker = re.search(r'^# runnable-example: ([\w-]+)', code, re.M)
            if marker:
                name = marker[1]
                if lang != 'python' or name not in ALLOWED_EXAMPLES or name in examples:
                    raise ValueError('unexpected or duplicate example: ' + name)
                examples[name] = code
    if set(examples) != ALLOWED_EXAMPLES:
        raise ValueError('named teaching examples missing')
    return examples


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-examples', action='store_true')
    args = parser.parse_args()
    errors = []
    docs = sorted((MODULE / 'docs').glob('*.md'))
    if [p.name[:2] for p in docs] != [f'{i:02d}' for i in range(1, 25)]:
        errors.append('expected reviewed 01-24 chapter scope')
    homepage = (MODULE / 'README.md').read_text(encoding='utf-8')
    for number, p in enumerate(docs, 1):
        text = p.read_text(encoding='utf-8')
        errors.extend(f'{p.relative_to(ROOT)}: {e}' for e in chapter_errors(text, number))
        if homepage.count('](docs/' + p.name + ')') != 1:
            errors.append(p.name + ': expected one formal homepage entry')
    try:
        examples = collect_examples(docs)
    except ValueError as exc:
        errors.append(str(exc)); examples = {}
    try:
        desired = build(ROOT)
        for path, text in desired.items():
            if (ROOT / path).read_text(encoding='utf-8') != text:
                errors.append(path + ': generated aid drift')
    except (ValueError, KeyError, IndexError) as exc:
        errors.append('aid source invalid: ' + str(exc))
    mapping = json.loads((ROOT / MAP).read_text(encoding='utf-8'))
    canonical = (ROOT / 'interview/canonical/agent-harness.md').read_text(encoding='utf-8')
    expected = set(re.findall(r'^###\s+(AGENT-\d{3})\s+·', canonical, re.M))
    mapped = {row['canonical_id'] for row in mapping['evidence']}
    if not expected or expected != mapped:
        errors.append(f'evidence map mismatch: missing={expected-mapped}, extra={mapped-expected}')
    for row in mapping['evidence']:
        for target in row['teaching_targets']:
            p, _, fragment = target.partition('#')
            if not (ROOT / p).is_file() or fragment not in anchors((ROOT / p).read_text(encoding='utf-8')):
                errors.append('invalid evidence teaching target: ' + target)
    for row in mapping['aliases']:
        p = ROOT / row['path']
        found = anchors(p.read_text(encoding='utf-8'))
        if row['alias'] not in found or row['target'] not in found:
            errors.append('lost compatibility target: ' + row['path'] + '#' + row['alias'])
    # Freeze historical retention evidence; a new curriculum does not rewrite history.
    old_report = (ROOT / 'guide/project/agent-reader-revision.md').read_text(encoding='utf-8')
    disposition = re.findall(r'^\| (\d{2})/(\d{2}) \|', old_report, re.M)
    if len(disposition) != 395 or len(set(disposition)) != 395:
        errors.append('historical 395-section record changed or incomplete')
    actual = inventory(ROOT)
    registry = json.loads((ROOT / 'guide/navigation-index.json').read_text(encoding='utf-8'))
    if actual != registry:
        errors.append('navigation registry differs from actual files')
    checked = 0; cache = {}
    for p in validation_paths(ROOT):
        # Historical documents retain their historical facts and links; missing paths
        # remain checked, but original historical heading fragments are not rewritten.
        historical = 'history' in p.parts and p.name != 'README.md'
        try:
            text = p.read_text(encoding='utf-8'); split_fences(text)
        except (ValueError, UnicodeError) as exc:
            errors.append(f'{p}: {exc}'); continue
        for _, href in markdown_links(text):
            value = resolve(ROOT, p, href)
            if value is None:
                continue
            dest, fragment = value; checked += 1
            if not dest.exists():
                if not historical:
                    errors.append(f'{p.relative_to(ROOT)} -> {href}: missing local target')
                continue
            if fragment and dest.suffix.lower() == '.md' and not historical:
                if dest not in cache:
                    cache[dest] = anchors(dest.read_text(encoding='utf-8'))
                if fragment not in cache[dest]:
                    errors.append(f'{p.relative_to(ROOT)} -> {href}: missing anchor')
    print(f'Agent chapters: {len(docs)}; current curriculum chapters: {actual["curriculum_chapters"]}')
    print(f'Canonical map: {len(expected)}; historical entries: {len(disposition)}; local references checked: {checked}')
    print(f'Compatibility aliases: {len(mapping["aliases"])}; errors: {len(errors)}')
    if errors:
        print('\n'.join(errors))
        return 1
    if args.run_examples:
        for name, code in sorted(examples.items()):
            with tempfile.TemporaryDirectory(prefix='agent-teaching-') as temp:
                p = Path(temp) / 'example.py'
                p.write_text(code, encoding='utf-8')
                subprocess.run([sys.executable, '-I', str(p)], cwd=temp, check=True, timeout=5)
            print('Executed named local teaching example:', name)
    print('PASS: declared structural, mapping and reference scope only; no model/production claim.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
