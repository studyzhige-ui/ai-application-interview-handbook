"""One-time, branch-scoped rendering correction; removed before final commit."""
from pathlib import Path
import hashlib, json, os, re, subprocess, sys
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
BRANCH='work/agent-clarity-20260928'
BASE='1a09d90a7ce7690e94dee3e401203264a307a7f1'
MODULE='curriculum/09-agent'
VALIDATION='guide/project/agent-clarity-validation-2026-09-28.json'
REPORT='guide/project/agent-clarity-refinement-2026-09-28.md'
TEMP=['_agent_final_polish.py','.github/workflows/agent-final-polish.yml']
def git(*args):
    return subprocess.check_output(['git','-c','core.quotePath=false',*args]).decode('utf-8')
def write(p,text):
    Path(p).write_text(text,encoding='utf-8',newline='\n')
def replace_once(s,old,new):
    assert s.count(old)==1, 'unexpected source: '+old
    return s.replace(old,new)
def normalize(text):
    lines=[]; fence=None
    for line in text.splitlines(keepends=True):
        mark=re.match(r'^\s*(`{3,}|~{3,})',line)
        if mark:
            token=mark[1]
            if fence is None: fence=token
            elif token[0]==fence[0] and len(token)>=len(fence): fence=None
            lines.append(line);continue
        if fence is None:
            # Match every pair first; skipping a valid pair could pair its closing
            # delimiter with the next opening delimiter on the same line.
            line=re.sub(r'\*\*[^*\n]+\*\*',lambda m:m[0]+(' ' if m.end()<len(line) and re.match(r'\w',line[m.end()]) else ''),line)
        lines.append(line)
    return ''.join(lines)
assert os.environ.get('GITHUB_REPOSITORY')=='studyzhige-ui/ai-application-interview-handbook'
assert os.environ.get('GITHUB_REF_NAME')==BRANCH
assert not git('status','--porcelain').strip()
assert git('rev-parse','origin/main').strip()==BASE, 'main changed; reconcile before publication'
# Integrate the inspected System Design commit; only shared generated registries
# may conflict. Regenerate those from the combined tree below, never choose one
# module's stale registry as the final version.
subprocess.run(['git','config','user.name','github-actions[bot]'],check=True)
subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'],check=True)
merge=subprocess.run(['git','merge','--no-commit','--no-ff',BASE],text=True,encoding='utf-8',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print(merge.stdout,flush=True)
conflicts=git('diff','--name-only','--diff-filter=U').splitlines()
assert set(conflicts)<={'guide/navigation-index.json','guide/navigation-index.md'}, 'unexpected merge conflict: '+repr(conflicts)
if conflicts:
    subprocess.run(['git','checkout','--theirs','--',*conflicts],check=True)
    subprocess.run(['git','add','--',*conflicts],check=True)
elif merge.returncode:
    raise RuntimeError('main integration failed: '+merge.stdout)
for p in sorted(Path(MODULE).rglob('*.md')):
    before=p.read_text(encoding='utf-8');after=normalize(before)
    assert normalize(after)==after
    assert re.findall(r'```.*?```',before,re.S)==re.findall(r'```.*?```',after,re.S), 'code changed'
    if before!=after:write(p,after)
p=Path(MODULE)/'interview/questions.json'
s=p.read_text(encoding='utf-8')
assert '不不可逆丢掉' in s
write(p,s.replace('不不可逆丢掉','不要不可逆地丢掉'))
p=Path('tools/test_agent_course.py');s=p.read_text(encoding='utf-8')
s=replace_once(s,'self.counts = {}; self.details = []; self.bad = []; self.ids = []','self.counts = {}; self.details = []; self.bad = []; self.ids = []\n        self.code_depth = 0')
s=replace_once(s,'    def handle_starttag(self, tag, attrs):\n        self.counts',"    def handle_starttag(self, tag, attrs):\n        if tag in ('code', 'pre'):\n            self.code_depth += 1\n        self.counts")
s=replace_once(s,'    def handle_endtag(self, tag):\n        if tag',"    def handle_endtag(self, tag):\n        if tag in ('code', 'pre'):\n            self.code_depth -= 1\n        if tag")
s=replace_once(s,'\n\nclass FeedbackTests',"\n    def handle_data(self, data):\n        if self.code_depth == 0 and '**' in data:\n            self.bad.append('unparsed strong-emphasis marker')\n\n\nclass FeedbackTests")
new='''    def test_cjk_strong_emphasis_regression(self):
        renderer = MarkdownIt('commonmark', {'html': True})
        samples = [
            ('**Checkpoint（检查点）**保存状态', True),
            ('**Checkpoint（检查点）** 保存状态', False),
            ('`**literal code**`', False),
        ]
        for text, should_fail in samples:
            with self.subTest(text=text):
                parser = RenderInspection(); parser.feed(renderer.render(text)); parser.close()
                self.assertEqual(bool(parser.bad), should_fail)

'''
s=replace_once(s,'    def test_markdown_rendering_and_fold_structure(self):',new+'    def test_markdown_rendering_and_fold_structure(self):')
write(p,s)
p=Path(REPORT)
write(p,p.read_text(encoding='utf-8')+'\n\n## 交付前排版复核\n\n修正17章中中文紧接强调分隔符造成的加粗失效，保留代码块原样；修正集中问答第23题的重复否定。渲染回归加入无效强调的反例、正确写法和代码中文字面星号，单元检查共36项。浏览器复核另行在本地以精确Markdown、Markdown-it与GitHub近似样式进行，不冒充GitHub生产页面或真实Agent集成。\n')
for p in TEMP:Path(p).unlink()
subprocess.run([sys.executable,'tools/sync_agent_materials.py','--apply'],check=True)
subprocess.run([sys.executable,'tools/sync_outer_navigation.py','--apply'],check=True)
exact={
 'guide/documentation-style-guide.md','guide/navigation-index.json','guide/navigation-index.md','guide/project/README.md',
 'guide/project/agent-clarity-mapping-2026-09-28.json',VALIDATION,REPORT,
 'references/agent/README.md','references/agent/implementation-notes.md','references/agent/runtime-capability-map.md',
 'tools/agent-validation-requirements.txt','tools/sync_agent_materials.py','tools/test_agent_course.py','tools/validate_agent_readability.py',
}
def scoped(path):return path.startswith(MODULE+'/') or path in exact
changed=git('diff','--name-only',BASE).splitlines()
assert all(scoped(p) for p in changed), 'out-of-scope changes: '+repr(changed)
results=[]
commands=[['-m','compileall','-q','tools'],['tools/sync_agent_materials.py','--check'],['tools/test_agent_course.py'],['tools/validate_agent_readability.py','--run-examples'],['tools/sync_outer_navigation.py','--check'],['tools/test_outer_navigation.py'],['tools/test_learning_navigation.py'],['tools/validate_repository_semantics.py']]
for command in commands:
    print('RUN:',command,flush=True)
    result=subprocess.run([sys.executable,*command],text=True,encoding='utf-8',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    print(result.stdout,flush=True)
    results.append({'command':command,'exit_code':result.returncode,'output':result.stdout})
    assert result.returncode==0, 'validation failed: '+repr(command)
v=json.loads(Path(VALIDATION).read_text(encoding='utf-8'))
v['publication_base']=BASE
v['previous_validation_workflow_run']=v['workflow_run']
v['workflow_run']=os.environ['GITHUB_RUN_ID']
v['commands']=results
v['changed_files']=changed
v['rendering_regression']='CJK strong-emphasis mutation fails before correction; normal and code-literal cases pass'
v['content_sha256']={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in changed if Path(p).is_file() and p!=VALIDATION}
v['browser_visual_review']='Separate local review of exact Markdown; workflow checks rendered HTML structure and emphasis, not GitHub production frontend'
write(VALIDATION,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
# Include exact validated changes and temporary-file deletions, never an unrelated path.
pending=set(git('diff','--name-only').splitlines())
assert all(scoped(p) or p in TEMP for p in pending)
assert not git('ls-files','--others','--exclude-standard').strip()
subprocess.run(['git','add','-A','--',*sorted(pending)],check=True)
assert all(scoped(p) for p in git('diff','--cached','--name-only',BASE).splitlines())
subprocess.run(['git','config','user.name','github-actions[bot]'],check=True)
subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'],check=True)
subprocess.run(['git','commit','-m','docs(agent): verify CJK rendering and finalize teaching regression checks'],check=True)
subprocess.run(['git','push','origin',f'HEAD:refs/heads/{BRANCH}'],check=True)
print('FINAL REVIEW COMMIT:',git('rev-parse','HEAD').strip(),flush=True)
