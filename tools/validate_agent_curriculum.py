#!/usr/bin/env python3
"""Structural regression checks; never substitutes for semantic review or product tests.

No network access and no execution of Markdown code. Counts describe the current
reviewed curriculum; update deliberately when the curriculum itself changes.
"""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MODULES = ['python', 'fastapi', 'backend-engineering', 'mysql', 'redis',
           'vector-db', 'llm-foundation', 'rag', 'agent', 'system-design']
LINK = re.compile(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)')


def prose(text):
    out = []
    fence = None
    for line in text.splitlines():
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        elif fence is None:
            out.append(line)
    return '\n'.join(out)


def local_links():
    bad, anchors, checked = [], [], 0
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts:
            continue
        for match in LINK.finditer(prose(p.read_text(encoding='utf-8'))):
            target = match.group(1).strip().split(' "', 1)[0].strip('<>')
            if not target or target.startswith(('http:', 'https:', 'mailto:', 'data:')):
                continue
            path, _, fragment = target.partition('#')
            path = unquote(path.split('?', 1)[0])
            dest = (ROOT / path.lstrip('/')) if path.startswith('/') else p.parent / path
            if not path:
                dest = p
            if path:
                checked += 1
                if not dest.exists():
                    bad.append((str(p.relative_to(ROOT)), target))
                    continue
            if 'agent' in p.relative_to(ROOT).parts and re.fullmatch(r'(part-\d+|q-\d+|chapter-\d+|concept-map)', fragment):
                if f'id="{fragment}"' not in dest.read_text(encoding='utf-8'):
                    anchors.append((str(p.relative_to(ROOT)), target))
    return checked, bad, anchors


def main():
    errors = []
    docs = sorted((ROOT / 'agent/docs').glob('*.md'))
    if len(docs) != 16:
        errors.append(f'expected 16 Agent chapters, found {len(docs)}')
    if [p.name[:2] for p in docs] != [f'{i:02}' for i in range(1, 17)]:
        errors.append('chapter numbers not continuous')
    for obsolete in ['agent-harness', 'agent/architecture']:
        if (ROOT / obsolete).exists():
            errors.append('obsolete/parallel learning directory exists: ' + obsolete)
    home = (ROOT / 'agent/README.md').read_text(encoding='utf-8')
    for i, p in enumerate(docs):
        text = p.read_text(encoding='utf-8')
        if not text.startswith(f'# {i + 1:02}. '):
            errors.append('H1 does not match chapter number: ' + p.name)
        if home.count('](docs/' + p.name + ')') != 1:
            errors.append('homepage chapter link not unique: ' + p.name)
        if any(s not in text for s in ['主线位置', '本章产物', '阅读提示']):
            errors.append('missing chapter scaffold: ' + p.name)
        if text.count('<details>') < 4:
            errors.append('missing scenario quizzes: ' + p.name)
        if i and docs[i - 1].name not in text:
            errors.append('missing previous link: ' + p.name)
        if i < len(docs) - 1 and docs[i + 1].name not in text:
            errors.append('missing next link: ' + p.name)
        if len(text.encode('utf-8')) < 2500:
            errors.append('unexpectedly short chapter (manual review required): ' + p.name)
    for p in (ROOT / 'agent').rglob('*.md'):
        text = p.read_text(encoding='utf-8')
        if text.count('<details>') != text.count('</details>') or re.search(r'<details\s+open', text):
            errors.append('unbalanced/default-open details: ' + str(p.relative_to(ROOT)))
        if len(re.findall(r'^```', text, re.M)) % 2:
            errors.append('unclosed fence: ' + str(p.relative_to(ROOT)))
    q = (ROOT / 'research/questions/agent-harness.md').read_text(encoding='utf-8')
    ids = set(re.findall(r'^###\s+(AGENT-\d{3})\s+·', q, re.M))
    interview = (ROOT / 'agent/interview/README.md').read_text(encoding='utf-8')
    covered = set(re.findall(r'`(AGENT-\d{3})`', interview))
    if len(ids) != 44 or ids != covered:
        errors.append('44 ACTIVE Canonical learning map mismatch')
    legacy = sorted(map(int, re.findall(r'legacy-question: (\d+)', interview)))
    if legacy != list(range(1, 57)):
        errors.append('main 56 drill identities missing/duplicated')
    questions = list(map(int, re.findall(r'<summary>Q(\d{2})｜', interview)))
    if questions != list(range(1, 65)):
        errors.append('64 practice questions not continuous')
    if any(interview.count(label) != 64 for label in ['**参考开场：**', '**具体追问：**', '**掌握标准：**']):
        errors.append('practice question scaffold mismatch')
    pitfalls = sorted(map(int, re.findall(r'^(\d+)\. ❌', interview, re.M)))
    if pitfalls != list(range(1, 87)):
        errors.append('86 pitfall distinctions missing/duplicated')
    total = sum(len(list((ROOT / d / 'docs').glob('*.md'))) for d in MODULES)
    if total != 177:
        errors.append(f'expected 177 curriculum files, found {total}')
    checked, bad, anchors = local_links()
    errors.extend(f'broken local link: {path} -> {target}' for path, target in bad)
    errors.extend(f'broken Agent explicit anchor: {path} -> {target}' for path, target in anchors)
    print(f'Agent: {len(docs)} chapters; curriculum: {total}; Canonical: {len(ids)}; drills: {len(questions)}; pitfalls: {len(pitfalls)}')
    print(f'Local file links: {checked}; broken: {len(bad)}; bad explicit anchors: {len(anchors)}')
    if errors:
        print('\n'.join(errors))
        return 1
    print('PASS: structural regression only; semantic review and production tests are separate')
    return 0


if __name__ == '__main__':
    sys.exit(main())
