#!/usr/bin/env python3
"""Synchronize active entry-page navigation; never rewrites history, stats, or paths.

Default is a dry run. Use --apply after reviewing the printed changes. Authoritative
order is guide/learning-order.json. Existing section bodies and table columns survive.
"""
from pathlib import Path
import argparse
import json
import re

ID_RE = re.compile(r"(?:curriculum/|\.\./)(\d{2}-[a-z-]+)/README\.md")
ALIASES = {
    "Python Foundation":"01-python", "Python":"01-python", "FastAPI":"02-fastapi",
    "AI Backend Engineering":"03-backend-engineering", "Backend":"03-backend-engineering",
    "MySQL":"04-mysql", "Redis":"05-redis", "Vector Database":"06-vector-db",
    "Vector DB":"06-vector-db", "LLM Foundation（应用工程深度）":"07-llm-foundation",
    "LLM Foundation":"07-llm-foundation", "Agent":"09-agent", "RAG":"08-rag",
    "System Design":"10-system-design",
}


def identify(segment):
    found=ID_RE.search(segment)
    if found: return found.group(1)
    return ALIASES.get(segment.strip().strip('*'))


def transform(path, text, order, labels):
    lines=text.splitlines(keepends=True)
    # Full curriculum chains; not ordinary domain flowcharts.
    for i,line in enumerate(lines):
        pieces=line.rstrip('\n').split(' → ')
        ids=[identify(x) for x in pieces]
        if len(pieces)==len(order) and set(ids)==set(order):
            mapping=dict(zip(ids,pieces))
            lines[i]=' → '.join(mapping[x] for x in order)+'\n'
    # A ten-module index table: keep all other columns and the directory IDs intact.
    locations=[i for i,l in enumerate(lines) if l.startswith('|') and identify(l) in order]
    if len(locations)==len(order) and set(identify(lines[i]) for i in locations)==set(order):
        rows={identify(lines[i]):lines[i] for i in locations}
        for rank,(i,identifier) in enumerate(zip(locations,order),1):
            lines[i]=re.sub(r'^\|\s*\d+\s*\|',f'| {rank:02d} |',rows[identifier],count=1)
        for i in range(max(0,locations[0]-3),locations[0]):
            lines[i]=lines[i].replace('| # |','| 学习顺序 |')
    text=''.join(lines)
    if path=='guide/knowledge-map.md':
        # All ten numbered module descriptions are contiguous, before usage rules.
        pattern=r'^## \d{2}\. \[.*?\]\(\.\./curriculum/(\d{2}-[a-z-]+)/README\.md\).*$'
        matches=list(re.finditer(pattern,text,re.M))
        if len(matches)==len(order) and set(m.group(1) for m in matches)==set(order):
            tail=re.search(r'^## 使用规则\s*$',text[matches[-1].end():],re.M)
            end=matches[-1].end()+tail.start() if tail else len(text)
            blocks={}
            for i,m in enumerate(matches):
                stop=matches[i+1].start() if i+1<len(matches) else end
                blocks[m.group(1)]=text[m.start():stop]
            middle=''.join(re.sub(r'^## \d{2}\.',f'## {i:02d}.',blocks[k],count=1) for i,k in enumerate(order,1))
            text=text[:matches[0].start()]+middle+text[end:]
    if path.startswith('curriculum/') and path.count('/')==2:
        identifier=path.split('/')[1]
        rank=order.index(identifier)
        lines=text.splitlines(keepends=True)
        # Only opening navigation and explicit final next-module line; do not rewrite prose refs.
        for i,line in enumerate(lines):
            if i<5:
                if rank:
                    prev=order[rank-1]
                    line=re.sub(r'\[← [^\]]+\]\(\.\./\d{2}-[a-z-]+/README\.md\)',f'[← {labels[prev]}](../{prev}/README.md)',line)
                if rank+1<len(order):
                    nxt=order[rank+1]
                    line=re.sub(r'\[[^\]]+ →\]\(\.\./\d{2}-[a-z-]+/README\.md\)',f'[{labels[nxt]} →](../{nxt}/README.md)',line)
            if line.startswith('下一环：') and rank+1<len(order):
                nxt=order[rank+1]
                line=f'下一环：[{labels[nxt]}](../{nxt}/README.md)。\n'
            lines[i]=line
        text=''.join(lines)
    return text


def planned_changes(root):
    data=json.loads((root/'guide/learning-order.json').read_text(encoding="utf-8"))
    order=[x['directory'] for x in data['modules']]
    labels={x['directory']:x['label'] for x in data['modules']}
    if len(order)!=10 or len(set(order))!=10: raise ValueError('Expected ten unique modules')
    targets=['README.md','guide/knowledge-map.md']+[f'curriculum/{x}/README.md' for x in order]
    changes={}
    missing=[x for x in targets if not (root/x).is_file()]
    if missing: raise FileNotFoundError('Requires full repository: '+', '.join(missing))
    for path in targets:
        before=(root/path).read_text(encoding="utf-8");after=transform(path,before,order,labels)
        if after!=before:changes[path]=after
    return changes


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--apply',action='store_true')
    args=p.parse_args();root=args.root.resolve()
    changes=planned_changes(root)
    for path in changes:print(('WRITE ' if args.apply else 'WOULD UPDATE ')+path)
    if args.apply:
        for path,content in changes.items():(root/path).write_text(content, encoding="utf-8")
    print(f'{len(changes)} entry pages; directory paths and frozen statistics unchanged.')

if __name__=='__main__':main()
