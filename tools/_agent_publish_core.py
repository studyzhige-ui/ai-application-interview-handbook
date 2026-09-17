"""One-time, source-preserving Agent reconstruction. Publishes no refs by itself."""
from pathlib import Path
import re, json, subprocess, hashlib, ast
ROOT = Path(__file__).resolve().parents[1]
OLD = '37cbfd2b152c6a0aa5bbd8ca0c19820debc632b8'
BASE = '83a3b96c10d8a3feb2c87d8fa2e59c02b8e8f178'
NAMES = [
'01-AgentSystemAndResponsibilities.md','02-WorkflowAutonomyAndRuntimeBoundary.md','03-AgentLoopAndExecutionScopes.md',
'04-ToolContractAndValidation.md','05-ToolRegistrationAndDiscovery.md','06-ToolExecutionAndFailure.md',
'07-ToolConcurrencyAndCancellation.md','08-PlanningGoalAndControl.md','09-ContextAssemblyAndCache.md',
'10-CompactionAndContinuation.md','11-MemoryLifecycle.md','12-StateHistoryAndPersistence.md',
'13-CheckpointResumeAndRecovery.md','14-PermissionApprovalAndSandbox.md','15-InjectionAndContainment.md',
'16-MCPArchitectureAndLifecycle.md','17-SkillsHooksAndExtensions.md','18-RoutingAndProviderResilience.md',
'19-MultiAgentAndA2A.md','20-TraceReplayAndDiagnosis.md','21-EvaluationBenchmarkAndImprovement.md',
'22-CodingAgentDelivery.md','23-ProductionRuntime.md','24-FrameworkSelection.md']
TITLES = ['Agent 系统的全貌：模型之外，谁把任务做完','Workflow、Agent 与自主权：执行角色的边界',
'Agent Loop：Session、Run、Turn、Step 与执行事件','Tool Contract：工具说明、参数与语义校验',
'Tool Registry：工具注册、模型可见说明与按需发现','Tool Execution：结果回填、错误分类与有限恢复',
'Tool Control：副作用、并发、取消与进度','Planning / ReAct：计划、目标、停止与预算',
'Context Assembly：上下文编排、缓存与结果外部化','Context Compaction：压缩、替代历史与继续执行',
'Memory：提取、召回、更新、纠错与遗忘','State / Persistence：程序怎样记住当前工作',
'Checkpoint / Resume：检查点、恢复、分叉与重放','Permission / Approval / Sandbox：政策、批准与隔离',
'Guardrails：提示注入、秘密保护与风险控制','MCP：从 Host / Client / Server 到完整协议往返',
'Skills / Hooks / Plugins：能力扩展与生命周期','Routing：意图、模型适配与供应商容错',
'Multi-Agent / A2A：内部协作与跨系统任务','Trace / Replay：记录必要证据，定位具体问题',
'Agent Evaluation、Benchmark 与 Data Flywheel','Coding Agent：Repo Understanding → Patch → Test → Verify',
'Production Agent：从单进程到可运营执行系统','Framework Mapping：按核心语义比较框架与自研']

def git_text(ref, path):
    return subprocess.check_output(['git','show',f'{ref}:{path}'],cwd=ROOT).decode('utf-8')

def git_paths(ref, path):
    return subprocess.check_output(['git','ls-tree','-r','--name-only',ref,path],cwd=ROOT).decode().splitlines()

OLD_PATHS = {int(Path(p).name[:2]):p for p in git_paths(OLD,'agent-harness/docs') if p.endswith('.md')}

def sections(text):
    lines=text.splitlines(); heads=[]; fence=None
    for i,line in enumerate(lines):
        m=re.match(r'^\s*(`{3,}|~{3,})',line)
        if m:
            if fence is None: fence=m[1][0]
            elif fence==m[1][0]: fence=None
            continue
        if fence is None and i and re.match(r'^#{1,2} (?:\d+(?:[.｜ ](?!\d))|面试怎么答|高频易错点|章节自测|资料与下一步)',line):
            heads.append((i,line))
    assert heads, 'No source headings'
    intro='\n'.join(lines[:heads[0][0]]).strip().removesuffix('---').strip()
    result=[]
    for k,(i,h) in enumerate(heads):
        m=re.match(r'^#{1,2} (\d+)[.｜ ]',h)
        title=re.sub(r'^#{1,2}\s*(?:\d+[.｜ ]\s*)?','',h)
        body='\n'.join(lines[i+1:heads[k+1][0] if k+1<len(heads) else len(lines)]).strip()
        body=re.sub(r'(?:\n\s*---\s*)+$','',body).strip()
        result.append({'id':int(m[1]) if m else title,'title':title,'body':body,'level':len(h.split(' ')[0])})
    return intro,result

ORIGINALS={i:sections(git_text(OLD,p)) for i,p in OLD_PATHS.items()}
CURRENTS={i:sections(git_text(BASE,p)) for i,p in OLD_PATHS.items()}

def source(i,k,current=False):
    return next(s for s in (CURRENTS if current else ORIGINALS)[i][1] if s['id']==k)

def cur(i,k): return source(i,k,True)['body']
def box(title,text): return '<details>\n<summary>'+title+'</summary>\n\n'+text.strip()+'\n\n</details>'

def body_text(s):
    # Old details are quizzes, extracted separately so they do not remain
    # accidentally embedded in a pitfall or follow-up section as well.
    text=re.sub(r'<details[^>]*>\s*<summary>.*?</summary>.*?</details>','',s['body'],flags=re.S)
    result=[];fence=False
    for line in text.splitlines():
        if re.match(r'^\s*(```|~~~)',line): fence=not fence
        if not fence:
            m=re.match(r'^(#{1,6}) (.*)',line)
            if m: line='#'*min(6,max(3,len(m[1])+(s['level']==1)))+' '+m[2]
        result.append(line)
    return '\n'.join(result).strip()

def classify(s):
    h=s['title']
    if any(k in h for k in ('HUMAN-A','证据分层','本章证据边界')):return 'human-a'
    if any(k in h for k in ('面试怎么','🎯','选型回答模板')):return 'interview'
    if '易错' in h:return 'pitfalls'
    if '自测' in h:return 'self-test'
    if '继续追问' in h or '面试官继续追问' in h:return 'follow'
    if any(k in h for k in ('源码','Claude Code 侧','官方资料为什么','官方证据','Building effective agents` 的重要启发')):return 'source'
    return 'body'

def extract_details(text):
    return [(re.sub(r'^(?:自测\s*)?\d+[.：:]\s*','',q).strip(),a.strip()) for q,a in re.findall(r'<details[^>]*>\s*<summary>(.*?)</summary>(.*?)</details>',text,re.S)]

def current_qas(i,quiz=False):
    t=cur(i,'章节自测' if quiz else '面试怎么答')
    pattern=r'### 自测 \d+：(.*?)\n\s*<details>\s*<summary>查看参考答案</summary>\s*(.*?)\s*</details>' if quiz else r'### \d+\. (.*?)\n\s*<details>\s*<summary>参考答案</summary>\s*(.*?)\s*</details>'
    return [(q.strip(),a.strip()) for q,a in re.findall(pattern,t,re.S)]

def plain(s): return re.sub(r'[^\w\u4e00-\u9fff]','',s).lower()

def distinct_append(items, additions):
    # Preserve original questions. Merge only a very close duplicate added by
    # the short revision; do not collapse independent failure capabilities.
    import difflib
    for q,a in additions:
        if not any(difflib.SequenceMatcher(None,plain(q),plain(x[0])).ratio()>.77 for x in items): items.append((q,a))
    return items

def old_qas(i):
    qs=[];extras=[]
    for s in ORIGINALS[i][1]:
        if classify(s)!='interview':continue
        text=body_text(s)
        matches=list(re.finditer(r'^#{2,4}\s+Q[：:]\s*(.*?)$',text,re.M))
        if matches:
            for k,m in enumerate(matches):qs.append((m[1],text[m.end():matches[k+1].start() if k+1<len(matches) else len(text)].strip()))
        elif ('框架' in s['title'] or 'Level' in text) and i in (1,2):extras.append(text)
        else:
            titles={1:'为什么模型之外还需要执行系统？',2:'Workflow与Agent的本质区别是什么？',3:'怎样解释一个完整Agent Loop？',4:'怎样设计生产工具契约？',5:'注册、发现和调用怎样配合？',6:'一次工具调用怎样从请求走到可用结果？',7:'怎样设计工具并发、取消与进度？',23:'怎样完整说明框架选型的理由？'}
            qs.append((titles.get(i,s['title']),text))
    return qs,extras

def footer(i,custom=None):
    qa,extras=old_qas(i)
    qa=distinct_append(qa,current_qas(i))
    quizzes=distinct_append(extract_details(git_text(OLD,OLD_PATHS[i])),current_qas(i,True))
    human='\n\n'.join(body_text(s) for s in ORIGINALS[i][1] if classify(s)=='human-a')
    pits=[]
    for s in ORIGINALS[i][1]:
        if classify(s)!='pitfalls':continue
        t=body_text(s)
        if '⚠️' in t:pits.extend(x.strip() for x in re.split(r'\n\s*\n',t) if x.strip())
        else:pits.extend('⚠️ '+x[2:].strip() for x in t.splitlines() if x.startswith('- '))
    for row in cur(i,'高频易错点').splitlines():
        if not row.startswith('|') or '---' in row or '容易混淆' in row:continue
        cells=[x.strip() for x in row.strip('|').split('|')]
        if len(cells)>=2:
            q,a=cells[:2]
            if not any(plain(q) in plain(p) for p in pits):pits.append('⚠️ **'+q+'。** '+a)
    if custom:
        qa=custom.get('qa',qa);quizzes=custom.get('quizzes',quizzes);human=custom.get('human',human);pits=custom.get('pits',pits);extras=[]
    interview=[]
    for q,a in qa:
        a=re.sub(r'^🎯[^\n]*\n+','',a).strip()
        a=re.sub(r'^>\s?', '',a,flags=re.M).strip()
        interview.append('### Q：'+q+'\n\n🎯 **'+('建议回答' if len(a)>320 else '30 秒回答')+'**：\n\n'+'\n'.join('> '+line if line else '>' for line in a.splitlines()))
    interview.extend('### 继续展开时的回答结构\n\n'+e for e in extras)
    follow=[body_text(s) for s in ORIGINALS[i][1] if classify(s)=='follow']
    if follow and not custom:
        interview.append('### 🔍 继续追问与下一步\n\n'+'\n\n'.join(follow))
    tests='\n\n'.join(f'<details><summary>{k}. {q}</summary>\n\n{a}\n\n</details>' for k,(q,a) in enumerate(quizzes,1))
    return [('HUMAN-A 信号',human),('面试怎么答','\n\n'.join(interview)),('高频易错点','\n\n'.join(pits)),('本章自测',tests)]

# Path rewrites only touch repository navigation, never source-code URLs or
# the compatible research file research/questions/agent-harness.md.
PATH_MAP={p:'agent/docs/'+NAMES[(i if i<=16 else i+1)-1] for i,p in OLD_PATHS.items()}
NAME_MAP={Path(p).name:Path(n).name for p,n in PATH_MAP.items()}

def links(text):
    def f(m):
        t=m[1]
        if t.startswith(('http:','https:','mailto:')):return m[0]
        for old,new in PATH_MAP.items():t=t.replace(old,new)
        t=t.replace('agent-harness/','agent/')
        for old,new in NAME_MAP.items():t=t.replace(old,new)
        return ']('+t+')'
    return re.sub(r'\]\(([^\n)]*)\)',f,text)

def corrections(t):
    t=t.replace('Tool Execution 是一个 Runtime Transaction，而不是函数调用语法糖。','Tool Execution 是一个受控调用生命周期，而不是函数调用语法糖；它不天然提供跨系统原子事务。')
    t=t.replace('成熟 Compaction 更接近一次 Runtime Transaction，而不是一次普通 Summary。','成熟Compaction不仅生成摘要，还要选择输入、安装替代历史、保存必要记录并继续执行；它不是天然的跨系统数据库事务。')
    t=t.replace('至少记录模型实际看到的 context evidence、provider/model、tool call/result、permission、state transition、checkpoint/compaction、subagent relation、latency/token/cost。','先记录阶段、状态、耗时、错误类别及必要关联引用；按具体故障取得授权的输入和工具证据，不默认复制全部原始内容。')
    t=t.replace('能重建“模型看见了什么、决定了什么、Runtime 执行了什么、状态如何变化”的结构化执行轨迹。','能关联模型调用、工具结果与状态变化，先定位阶段，再按问题取得必要证据的执行轨迹。')
    t=t.replace('Trace 应保留足够结构，能还原模型实际看到的输入、Tool Runtime Boundary 和信息流，而不是只有拼接后的日志文本。','Trace应保留足够的关联结构来定位信息流；需要深查时按授权取得输入证据，不默认保存全部原文。')
    t=t.replace('State\n= Runtime 当前执行事实','State\n= 程序用于决定下一步的当前工作情况，如进度、等待、预算和动作结果')
    t=t.replace('后续 21 个知识板块','后续知识板块').replace('前两章的 Security 模型','权限与提示注入章节的安全模型')
    t=t.replace('AGENT-024/025','AGENT-024` / `AGENT-025')
    t=re.sub(r'`(AGENT-\d{3}) ([^`]+)`',r'`\1` \2',t)
    t=t.replace('Instructions      10k\nGoal / State       8k\nRecent History    20k\nMemory / RAG      30k\nTool Definitions  20k\nTool Results      20k\nReserve Output    20k','Instructions       8k\nGoal / State       6k\nRecent History    20k\nMemory / RAG      24k\nTool Definitions  14k\nTool Results      28k\n---------------------\nInput subtotal   100k\nReserve Output    20k\nSafety Margin      8k\nTotal window     128k')
    t=re.sub(r'```python\n(@dataclass)',r'```python\nfrom dataclasses import dataclass\n\n\1',t)
    return t

GLOSSARY={'Runtime':'运行时执行系统','Orchestrator':'编排器','State':'状态','Persistence':'持久化','Checkpoint':'检查点','Resume':'恢复执行','Replay':'重放','Memory':'记忆','History':'历史记录','Registry':'注册表','Router':'路由器','Executor':'执行器','Invocation':'调用实例','Observation':'观察结果','Artifact':'产物','Sandbox':'沙箱','Permission':'权限','Approval':'批准','Compaction':'上下文压缩','Summary':'摘要','Trace':'执行追踪','Latency':'时延','Budget':'预算','Fallback':'备用或降级路径','Retry':'重试','Provider':'模型服务方','Tenant':'租户','Regression':'回归测试','Benchmark':'基准测试','Data Flywheel':'数据反馈迭代闭环','Handoff':'控制权交接','Subagent':'子Agent','Hook':'生命周期钩子','Skill':'技能包','Production':'生产环境','Correlation ID':'关联标识','Containment':'限制故障或攻击影响范围'}
def gloss(t):
    seen=set();lines=[];fence=False
    for line in t.splitlines():
        if re.match(r'^\s*(```|~~~)',line):fence=not fence
        if fence or line.startswith(('#','<','[←','[↑')):lines.append(line);continue
        pieces=re.split(r'(`[^`]*`|\[[^\]]*\]\([^)]*\)|https?://\S+)',line)
        for j in range(0,len(pieces),2):
            for word in sorted(GLOSSARY,key=len,reverse=True):
                if word in seen:continue
                m=re.search(r'(?<![A-Za-z_])'+re.escape(word)+r'(?![A-Za-z_])',pieces[j])
                if m:
                    seen.add(word)
                    if pieces[j][m.end():m.end()+1] not in ('（','('):pieces[j]=pieces[j][:m.end()]+'（'+GLOSSARY[word]+'）'+pieces[j][m.end():]
        lines.append(''.join(pieces))
    return '\n'.join(lines)

DISPOSITIONS=[]
def render(i,new,edits,intro_override=None):
    intro,sections_=ORIGINALS[i]
    intro=re.sub(r'^# [^\n]*','# '+f'{new:02}. '+TITLES[new-1],intro,count=1)
    intro=re.sub(r'> 本章(?:合并|把旧)[^\n]*\n?','',intro)
    if intro_override:intro='# '+f'{new:02}. '+TITLES[new-1]+'\n\n'+intro_override
    body=[];evidence=[]
    for s in sections_:
        key=s['id'];kind=classify(s);patch=edits.get((i,key),{})
        if i==16 and key in (5,6,7):
            DISPOSITIONS.append((i,key,s['title'],16,'protocol','MCP原标准化、三原语与传输边界移到完整协议章节'))
            continue
        if kind in ('human-a','interview','pitfalls','self-test','follow'):
            DISPOSITIONS.append((i,key,s['title'],new,kind,'保留到对应章末部分，原有自测独立归位'))
            continue
        original=body_text(s)
        text=patch.get('replace',original)
        text='\n\n'.join(p.strip() for p in (patch.get('before',''),text,patch.get('after','')) if p.strip())
        title=patch.get('title',s['title'])
        text=f'<a id="legacy-{i:02}-{key:02}"></a>\n\n'+text
        if kind=='source' or patch.get('source'):
            text=re.sub(r'<details>\s*<summary>(.*?)</summary>',r'### \1',text,flags=re.S).replace('</details>','')
            evidence.append((title,text))
        else:body.append((title,text))
        status='corrected' if 'replace' in patch else ('source' if kind=='source' or patch.get('source') else 'retained')
        DISPOSITIONS.append((i,key,s['title'],new,status,patch.get('reason','保留原机制、例子、步骤和失败边界；增补解释单列')))
    if evidence:
        body.append(('产品实现与官方资料对照（按需展开）','\n\n'.join(box(h,t) for h,t in evidence)+'\n\n具体实现以[固定源码与官方索引](../../research/agent-sources/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。'))
    return document(new,intro,body,footer(i))

def document(n,intro,body,ending):
    chunks=[]
    for k,(h,t) in enumerate(body+ending,1):
        anchor={'HUMAN-A 信号':'human-a','面试怎么答':'interview','高频易错点':'pitfalls','本章自测':'self-test'}.get(h,f'section-{k}')
        t=re.sub(r'(?m)^(#{3,4}) \d+\.(\d+)',lambda m:m[1]+' '+str(k)+'.'+m[2],t)
        chunks.append(f'<a id="{anchor}"></a>\n\n## {k}. {h}\n\n{t.strip()}')
    nav=(f'[← 上一章]({NAMES[n-2]}) · ' if n>1 else '')+'[Agent 目录](../README.md)'+(f' · [下一章 →]({NAMES[n]})' if n<24 else ' · [综合复习 →](../review/README.md)')
    return links(gloss(corrections(intro+'\n\n'+nav+'\n\n---\n\n'+'\n\n---\n\n'.join(chunks)+'\n\n---\n\n'+nav))).rstrip()+'\n'
