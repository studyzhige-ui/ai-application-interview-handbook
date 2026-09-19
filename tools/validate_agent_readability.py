#!/usr/bin/env python3
"""Validate Agent documentation structure, not a blanket semantic-quality PASS.

--run-examples runs only explicitly named in-memory standard-library examples.
No model, network, credential or real external side effect is exercised.
"""
from pathlib import Path
from urllib.parse import unquote
import argparse, ast, re, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]
MODULES={'01-python':13,'02-fastapi':16,'03-backend-engineering':22,'04-mysql':23,'05-redis':24,'06-vector-db':16,'07-llm-foundation':14,'08-rag':14,'09-agent':24,'10-system-design':19}
ALLOWED_EXAMPLES={'feedback_loop','registry_projection'}

def split_fences(text):
    prose=[];blocks=[];opening=None;code=[];lang=''
    for line in text.splitlines():
        if opening is None:
            m=re.match(r'^\s*(`{3,}|~{3,})(.*)$',line)
            if m:opening=m[1];lang=m[2].strip().split(' ',1)[0];code=[]
            else:prose.append(line)
        elif re.fullmatch(r'\s*'+re.escape(opening[0])+'{'+str(len(opening))+r',}\s*',line):
            blocks.append((lang,'\n'.join(code)+'\n'));opening=None
        else:code.append(line)
    if opening:raise ValueError('unclosed code fence')
    return '\n'.join(prose),blocks

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-examples',action='store_true');args=parser.parse_args()
    errors=[];docs=sorted((ROOT/'curriculum/09-agent/docs').glob('*.md'));examples={};counts={'interviews':0,'self_tests':0,'pitfalls':0}
    if [p.name[:2] for p in docs]!=[f'{i:02}' for i in range(1,25)]:errors.append('Agent chapter count/numbering differs from 01-24')
    if (ROOT/'agent-harness').exists():errors.append('old parallel learning directory still exists')
    homepage=(ROOT/'curriculum/09-agent/README.md').read_text()
    found_ids=set();explicit={}
    for p in docs:
        text=p.read_text();relative=p.relative_to(ROOT).as_posix()
        if not text.startswith('# '+p.name[:2]+'.'):errors.append(relative+': H1 number mismatch')
        if homepage.count('](docs/'+p.name+')')!=1:errors.append(relative+': homepage entry must be unique')
        try:prose,blocks=split_fences(text)
        except ValueError as exc:errors.append(relative+': '+str(exc));continue
        titles=re.findall(r'^## \d+\. (.*)$',prose,re.M)
        if titles[-4:]!=['HUMAN-A 信号','面试怎么答','高频易错点','本章自测']:errors.append(relative+': wrong endcap order')
        positions=[text.find('<a id="'+key+'"></a>') for key in ('human-a','interview','pitfalls','self-test')]
        if min(positions)<0 or positions!=sorted(positions):errors.append(relative+': missing endcap anchors');continue
        qa=text[positions[1]:positions[2]];pit=text[positions[2]:positions[3]];quiz=text[positions[3]:]
        if '<details' in qa:errors.append(relative+': interview answers must be visible')
        if '<details' in pit:errors.append(relative+': quizzes leaked into pitfalls')
        nq=len(re.findall(r'^### Q：',qa,re.M));nt=len(re.findall(r'<details><summary>\d+\.',quiz));np=len(re.findall(r'^⚠️',pit,re.M))
        if nq<2 or nt<3 or np<3:errors.append(relative+': incomplete chapter-end training')
        counts['interviews']+=nq;counts['self_tests']+=nt;counts['pitfalls']+=np
        if '🎯' not in qa or '<summary>查看参考答案</summary>' in quiz:errors.append(relative+': rejected uniform answer-button format')
        if text.count('<details>')!=text.count('</details>') or re.search(r'<details\s+open',text):errors.append(relative+': invalid/default-open details')
        found_ids.update(re.findall(r'`(AGENT-\d{3})`',text))
        for lang,code in blocks:
            if lang=='python':
                try:ast.parse(code,filename=relative)
                except SyntaxError as exc:errors.append(relative+': '+str(exc))
            marker=re.search(r'^# runnable-example: ([\w-]+)',code,re.M)
            if marker:
                name=marker[1]
                if name not in ALLOWED_EXAMPLES or name in examples:errors.append('unexpected example '+name)
                examples[name]=code
        ids=re.findall(r'<a\s+id="([^"]+)"',text)
        if len(ids)!=len(set(ids)):errors.append(relative+': duplicate explicit anchor')
        explicit[p.resolve()]=set(ids)
    expected=set(re.findall(r'^###\s+(AGENT-\d{3})\s+·',(ROOT/'interview/canonical/agent-harness.md').read_text(),re.M))
    if len(expected)!=44 or expected!=found_ids:errors.append(f'Canonical mismatch: missing {expected-found_ids}, extra {found_ids-expected}')
    if set(examples)!=ALLOWED_EXAMPLES:errors.append('missing named teaching examples')
    total=0
    for module,count in MODULES.items():
        actual=len(list((ROOT/'curriculum'/module/'docs').glob('*.md')));total+=actual
        if actual!=count:errors.append(f'{module}: expected {count}, got {actual}')
    checked=0;anchor_checks=0
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts:continue
        # Historical snapshots are intentionally preserved at a new archive path;
        # their old relative links describe the original location and are not rewritten.
        if 'history' in p.parts and p.name != 'README.md':continue
        try:prose,_=split_fences(p.read_text())
        except ValueError as exc:errors.append(str(p.relative_to(ROOT))+': '+str(exc));continue
        for target in re.findall(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)',prose):
            target=target.strip().split(' "',1)[0].strip('<>')
            if not target or target.startswith(('http:','https:','mailto:','data:')):continue
            path,_,anchor=target.partition('#');path=unquote(path.split('?',1)[0]);anchor=unquote(anchor)
            dest=((ROOT/path.lstrip('/')) if path.startswith('/') else (p.parent/path)).resolve() if path else p.resolve()
            if path:
                checked+=1
                if not dest.exists():errors.append(f'{p.relative_to(ROOT)} -> {target}: missing file')
            if dest in explicit and anchor and (anchor.startswith(('legacy-','section-')) or anchor in ('human-a','interview','pitfalls','self-test')):
                anchor_checks+=1
                if anchor not in explicit[dest]:errors.append(f'{p.relative_to(ROOT)} -> {target}: missing explicit anchor')
    report=(ROOT/'guide/project/agent-reader-revision.md').read_text()
    mapped=re.findall(r'^\| (\d{2})/(\d{2}) \|',report,re.M)
    if len(mapped)!=395 or len(set(mapped))!=395:errors.append('original numbered-section disposition map must have 395 unique entries')
    drills=(ROOT/'curriculum/09-agent/interview/高频面试题.md').read_text()
    if len(re.findall(r'^### \d+\.',drills,re.M))!=56:errors.append('centralized 56-question scope not retained')
    print(f'Agent: {len(docs)} chapters; curriculum: {total}; Agent Canonical: {len(expected)}')
    print('Chapter endcaps:',counts)
    print(f'Original sections mapped: {len(mapped)}; local file links: {checked}; explicit anchors checked: {anchor_checks}; errors: {len(errors)}')
    if errors:print('\n'.join(errors));return 1
    if args.run_examples:
        for name,code in examples.items():
            with tempfile.TemporaryDirectory(prefix='agent-teaching-') as temp:
                path=Path(temp)/'example.py';path.write_text(code)
                subprocess.run([sys.executable,'-I',str(path)],cwd=temp,check=True,timeout=5)
            print('Executed teaching example:',name)
    print('PASS: bounded structural/retention-reference checks only; reader understanding and production behavior are separate.')
    return 0
if __name__=='__main__':sys.exit(main())
