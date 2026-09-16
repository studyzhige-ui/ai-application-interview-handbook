"""Temporary read-only inventory for the requested Agent curriculum refactor."""
from pathlib import Path
import re

root = Path('.')
for p in sorted(root.glob('agent-harness/docs/*.md')):
    print('\nFILE', p, 'BYTES', p.stat().st_size)
    fence = False
    for line in p.read_text().splitlines():
        if line.lstrip().startswith('```'):
            fence = not fence
        elif not fence and re.match(r'^#{1,3} ', line):
            print(line)
print('\n=== CROSS REFERENCES ===')
for p in sorted(root.rglob('*')):
    if not p.is_file() or '.git' in p.parts or p.suffix not in {'.md','.py','.json','.yml','.yaml','.csv','.toml'}:
        continue
    if p.parts[0] == 'agent-harness' or p.name == '_agent_refactor.py':
        continue
    text = p.read_text(encoding='utf-8')
    hits = [(i, s) for i,s in enumerate(text.splitlines(),1) if 'agent-harness' in s or 'Agent Harness / Runtime' in s or ('184' in s and p.parts[0] in {'roadmap','research'})]
    if hits:
        print('\nREF',p)
        for i,s in hits[:12]:
            print(f'{i}: {s[:500]}')
        if len(hits)>12:
            print('MORE',len(hits)-12)
print('\n=== TOOLS ===')
for p in sorted(root.glob('tools/*')):
    print(p)
