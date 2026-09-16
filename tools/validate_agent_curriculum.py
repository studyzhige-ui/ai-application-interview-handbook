#!/usr/bin/env python3
"""Validate the single Agent learning route without fetching external content."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote
ROOT = Path(__file__).resolve().parents[1]

def prose(text):
    out=[]; fenced=False
    for line in text.splitlines():
        if re.match(r'^\s*(```|~~~)',line):
            fenced=not fenced
        elif not fenced:
            out.append(line)
    return '\n'.join(out)

def local_links():
    bad=[]; checked=0
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts: continue
        for match in re.finditer(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)',prose(p.read_text(encoding='utf-8'))):
            target=match.group(1).strip().split(' "',1)[0].strip('<>')
            if not target or target.startswith(('#','http:','https:','mailto:','data:')): continue
            target=unquote(target.split('#',1)[0].split('?',1)[0])
            if not target: continue
            dest=(ROOT/target.lstrip('/')) if target.startswith('/') else p.parent/target
            checked+=1
            if not dest.exists(): bad.append((str(p.relative_to(ROOT)),target))
    return checked,bad

def main():
    errors=[]
    docs=sorted((ROOT/'agent/docs').glob('*.md'))
    if len(docs)!=16: errors.append(f'expected 16 Agent chapters, found {len(docs)}')
    if [p.name[:2] for p in docs] != [f'{i:02}' for i in range(1,17)]: errors.append('chapter numbers not continuous')
    if (ROOT/'agent-harness').exists(): errors.append('obsolete learning directory exists')
    if (ROOT/'agent/architecture').exists(): errors.append('parallel architecture course exists')
    home=(ROOT/'agent/README.md').read_text()
    for i,p in enumerate(docs):
        text=p.read_text()
        if home.count('](docs/'+p.name+')')!=1: errors.append('homepage chapter link not unique: '+p.name)
        if '主线位置' not in text or '本章产物' not in text: errors.append('missing chapter scaffold: '+p.name)
        if i and docs[i-1].name not in text: errors.append('missing previous link: '+p.name)
        if i<15 and docs[i+1].name not in text: errors.append('missing next link: '+p.name)
        if text.count('<details>')!=text.count('</details>') or re.search(r'<details\s+open',text): errors.append('invalid/default-open quiz: '+p.name)
        if len(re.findall(r'^```',text,re.M))%2: errors.append('unclosed fence: '+p.name)
        if len(text.encode('utf-8'))<2500: errors.append('unexpectedly short chapter: '+p.name)
    q=(ROOT/'research/questions/agent-harness.md').read_text()
    ids=set(re.findall(r'^###\s+(AGENT-\d{3})\s+·',q,re.M))
    if len(ids)!=44: errors.append('expected 44 ACTIVE Agent canonical questions')
    covered=set(re.findall(r'`(AGENT-\d{3})`',(ROOT/'agent/interview/README.md').read_text()))
    if ids!=covered: errors.append('canonical learning map mismatch')
    total=sum(len(list((ROOT/d/'docs').glob('*.md'))) for d in ['python','fastapi','backend-engineering','mysql','redis','vector-db','llm-foundation','rag','agent','system-design'])
    if total!=177: errors.append(f'expected 177 curriculum files, found {total}')
    checked,bad=local_links()
    for path,target in bad: errors.append(f'broken local link: {path} -> {target}')
    print(f'Agent chapters: {len(docs)}; curriculum total: {total}; Agent canonical: {len(ids)}; local links checked: {checked}; broken: {len(bad)}')
    if errors:
        print('\n'.join(errors)); return 1
    print('PASS: sequence, navigation, collapsed quizzes, fences, file links, counts and canonical map')
    return 0
if __name__=='__main__': sys.exit(main())
