from pathlib import Path
import re, subprocess
ROOT=Path(__file__).resolve().parents[1]
BASE='0266cbfa131ff4157cad9f4c18b75fe153c0b846'
def show(path):
    return subprocess.check_output(['git','show',f'{BASE}:{path}'],cwd=ROOT).decode()
def norm(s):
    return re.sub(r'\s+','',s).strip('`*_>#-')
def sections(text):
    lines=text.splitlines(); heads=[]; fence=False
    for i,l in enumerate(lines):
        if re.match(r'^\s*(```|~~~)',l): fence=not fence
        if not fence and re.match(r'^#{1,3}\s',l): heads.append((i,l))
    return [(h,'\n'.join(lines[i+1:(heads[k+1][0] if k+1<len(heads) else len(lines))])) for k,(i,h) in enumerate(heads)]
paths=subprocess.check_output(['git','ls-tree','-r','-z','--name-only',BASE,'agent-harness'],cwd=ROOT).decode().rstrip('\0').split('\0')
new=list(sorted((ROOT/'agent/docs').glob('*.md')))
ns=norm('\n'.join(p.read_text() for p in new))
out=['# Temporary source comparison (not a quality verdict)',f'Main: {BASE}', '## New chapter outline']
for p in new:
    txt=p.read_text(); out += [f'### {p.name} ({len(txt.splitlines())} lines)', '\n'.join(h for h,b in sections(txt))]
out += ['## Main mechanism retention candidates']; missing=[]
for path in paths:
    if '/docs/' not in path: continue
    txt=show(path); out += ['### '+path]
    for h,b in sections(txt):
        paras=[x.strip() for x in re.split(r'\n\s*\n',b) if len(norm(x))>=25 and not x.lstrip().startswith(('---','<details','</details'))]
        found=sum(norm(x) in ns for x in paras)
        out.append(f'{h} | exact normalized paragraphs {found}/{len(paras)}')
        if paras and found<len(paras) and not any(t in h for t in ['自测','面试','HUMAN','易错','追问','本章小结']):
            absent=[x for x in paras if norm(x) not in ns]
            missing.append('## '+path+' :: '+h+'\n\n'+'\n\n'.join(absent))
(ROOT/'tools/_agent_survey.md').write_text('\n\n'.join(out))
(ROOT/'tools/_agent_missing.md').write_text('\n\n'.join(missing))
print('survey',len(out),'missing candidate sections',len(missing))
