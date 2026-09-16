#!/usr/bin/env python3
"""Final branch-local editorial and integrity pass; removed after use."""
from pathlib import Path
import importlib.util
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE='0266cbfa131ff4157cad9f4c18b75fe153c0b846'

def edit(rel, fn):
    p=ROOT/rel
    before=p.read_text(encoding='utf-8')
    after=fn(before)
    if before!=after:
        p.write_text(after.rstrip()+'\n',encoding='utf-8')
        print('EDIT',rel)

edit('agent/README.md',lambda t: re.sub(r'^> 本模块已由.*$', '> 主线从任务设计开始，沿四层职责展开，再以安全、质量和生产演进收口。Harness 是运行层中的执行系统，不再代指整个 Agent 模块。',t,flags=re.M))

session_section='''## 2. Session / Thread / Run / Turn / Item / Step / Task / Job

先说明语境，再定义对象关系。以下保留 Codex 的交互对象，并区分教材采用的任务/执行工作定义；不把 Session→Run→Turn 规定为行业统一层级。

| 术语 | 本仓库工作定义 | 备注 |
|---|---|---|
| **Agent Session / Thread** | 跨多个交互持续存在的会话容器。 | Codex Thread 是会话，不是操作系统线程 |
| **Run** | 围绕目标的一次受管理执行，可以暂停与恢复。 | 教材工作定义；与 Thread / Turn 的关联由应用协议决定 |
| **Turn** | Codex 中一次用户请求及其后续 Agent 工作。 | 可以包含多次模型推理与工具交互，不等于一次模型调用 |
| **Item** | Codex 中有类型的输入输出单元，例如消息、工具执行、文件修改。 | 一个 Item 可以产生多个生命周期 Event |
| **Step** | 运行时自行定义的可记录推进单位。 | 不同框架可能采用不同粒度 |
| **Agent Task** | 有目标、范围、权限边界和验收条件的工作对象。 | 应用层管理；可以关联多个 Run |
| **Backend Task / Job** | 可以排队、领取、重试或恢复的后台工作单元。 | AI Backend Engineering；不默认等于用户任务 |
| **DB Session** | 数据库连接/事务使用语境中的 Session。 | MySQL / FastAPI Integration |
| **Login Session** | 用户认证登录态。 | FastAPI / AI Backend Engineering |

写作规则：不能唯一确定含义时，写明 Agent Session、DB Session 或 Login Session。执行实例、进程、会话和业务任务也不是同一个实体。详细机制见 [Agent 执行循环](../agent/docs/04-AgentLoopAndControl.md)与[执行状态](../agent/docs/07-StateAndRecovery.md)。

---

'''

def glossary(t):
    start=t.index('## 2. Session')
    end=t.index('## 3. Timeout',start)
    t=t[:start]+session_section+t[end:]
    t=t.replace('Agent Harness','Agent')
    marker='## Agent 分层课程的统一约定（2026-09-16）'
    if marker in t:
        t=t[:t.index(marker)]
    t+='''## 14. Agent 系统、层与 Harness 的边界

Agent 模块覆盖任务设计、四层职责、安全质量与生产演进；Harness / Runtime 只指以运行层为核心的执行系统，实现可以包含接入代码，不等于完整产品。

架构 L1 / L2 / L3 / L4 分别是应用 / 运行 / 接入 / 资源，与研究题库的 Depth 编号无关。层表示职责，模块承担职责，机制实现职责，协议连接对象，资源承载真实能力和事实。

完整解释只维护在[Agent 正式课程](../agent/README.md)。新增术语先说明类型、主责、动机与边界，不另增一套分类或学习路线。
'''
    return t
edit('roadmap/terminology-glossary.md',glossary)

def learning(t):
    t=t.replace('Agent Harness','Agent')
    lines=[]
    for line in t.splitlines():
        if re.match(r'^\| 9 \| Agent',line):
            line='| 9 | Agent：任务契约、自主权、四层职责、应用交互与执行循环 |'
        elif re.match(r'^\| 10 \| Agent',line):
            line='| 10 | Agent：运行层的上下文、记忆、状态恢复与协作；接入层的模型和工具契约 |'
        elif re.match(r'^\| 11 \| Agent',line):
            line='| 11 | Agent：工具执行、知识接入、资源环境、安全质量与生产演进 |'
        lines.append(line)
    return '\n'.join(lines)
edit('roadmap/learning-path.md',learning)
edit('research/questions/module-index.md',lambda t:t.replace('与 177 个 Curriculum Markdown 的最终结论见','与旧版184个 Curriculum Markdown 的历史结论见'))

def depth(t):
    return '\n'.join(line.replace('✅ PASS','结构迁移已验证；深度为原版记录') if line.startswith('| [Agent]') else line for line in t.splitlines())
edit('roadmap/content-depth-audit.md',depth)

# All original question identities and metadata must remain unchanged except the module display name.
files=['python.md','fastapi.md','ai-backend-engineering.md','mysql.md','redis.md','vector-db.md','llm-foundation.md','rag.md','agent-harness.md','system-design.md']
field_re=re.compile(r'^- \*\*(Topic|Question Type|Depth|Source Count|Evidence Sources|Related Modules|Language / Ecosystem|Primary Module)\*\*')
def metadata(t):
    return [line.replace('Agent Harness / Runtime','Agent') for line in t.splitlines()
            if re.match(r'^###\s+(?:PY|FASTAPI|AIBE|MYSQL|REDIS|VDB|LLM|RAG|AGENT|SD)-\d{3}\s+·',line) or field_re.match(line)]
for name in files:
    rel='research/questions/'+name
    old=subprocess.check_output(['git','show',BASE+':'+rel],cwd=ROOT,text=True)
    current=(ROOT/rel).read_text()
    assert metadata(old)==metadata(current),'Question metadata changed: '+name
print('PASS: canonical question wording, IDs, source counts, evidence and depth unchanged; only module display name migrated')
assert not subprocess.check_output(['git','diff',BASE,'--','research/interviews','research/monitoring'],cwd=ROOT,text=True).strip()
print('PASS: original interview evidence and monitoring unchanged from base')

spec=importlib.util.spec_from_file_location('market_analysis_check',ROOT/'tools/build_market_analysis.py')
module=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=module
spec.loader.exec_module(module)
questions=module.parse_questions()
assert len(questions)==235
assert sum(q.module=='Agent' for q in questions)==44
print('PASS: existing analysis parser reads 235 canonical questions, including 44 Agent questions, and validates source counts')
result=subprocess.run(['python3','tools/validate_source_coverage.py'],cwd=ROOT,text=True,capture_output=True)
print('SOURCE COVERAGE CHECK',result.returncode)
print(result.stdout[-7000:])
print(result.stderr[-2000:])
assert result.returncode==0, 'Source coverage validator failed'

# Check all explicit anchors in the new learning module.
for p in (ROOT/'agent').rglob('*.md'):
    t=p.read_text()
    explicit=re.findall(r'<a id="([^"]+)"',t)
    assert len(explicit)==len(set(explicit)), 'Duplicate explicit anchors: '+str(p)
    for ref in re.findall(r'\]\(#(part-\d+)\)',t):
        assert ref in explicit, (p,ref)
print('PASS: chapter section-anchor links')
check=subprocess.run(['python3','tools/validate_agent_curriculum.py'],cwd=ROOT,text=True,capture_output=True)
print(check.stdout)
assert check.returncode==0,check.stderr

# Search remnants for editorial review; historical snapshots and genuine technical Harness terms may remain.
print('=== CURRENT AGENT COURSE FILES ===')
for p in sorted((ROOT/'agent').rglob('*.md')):
    print(p.relative_to(ROOT),p.stat().st_size)
print('=== NAVIGATION / SUMMARY REMNANTS ===')
for rel in ['README.md','roadmap/learning-path.md','roadmap/knowledge-map.md','roadmap/content-depth-audit.md','roadmap/integration-status.md','research/questions/module-index.md','research/questions/progress.md','research/agent-sources/README.md']:
    for i,line in enumerate((ROOT/rel).read_text().splitlines(),1):
        if 'Agent Harness' in line or ('Agent' in line and ('23' in line or '01–23' in line)):
            print(rel,i,line[:500])

p=ROOT/'roadmap/final-quality-audit.md'
t=p.read_text()
t+='''
### 同轮内容与证据复核

已修正跨模块术语表中旧 Turn 定义，与新课程的 Codex Thread / Turn / Item 一致；学习路线与模块名同步。

以重构前 main 提交 `0266cbfa131ff4157cad9f4c18b75fe153c0b846` 比较，十个研究题库的问题正文、ID、Depth、Source Count、Evidence Sources及归属元数据仅发生模块展示名变更；原始 interviews 与 monitoring 未改。既有分析解析器通过235题/44道Agent题及Source Count一致性检查，既有 source coverage 校验器通过。章内显式锚点、章节顺序、导航、折叠自测、代码围栏和仓库本地文件链接再次通过检查。

```text
'''+check.stdout.strip()+'''\n```
'''
p.write_text(t,encoding='utf-8')
print('Editorial and integrity pass complete.')
