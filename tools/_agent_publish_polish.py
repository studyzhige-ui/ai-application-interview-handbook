"""Last editorial pass after reconstruction; changes are explicit and scoped."""
from pathlib import Path
import re,json,difflib
ROOT=Path(__file__).resolve().parents[1]
DOCS=sorted((ROOT/'agent/docs').glob('*.md'))
COMMENTS={
1:'# 片段示意：只发起一次模型请求，尚未处理工具执行与反馈循环。',
2:'# 一次普通模型调用的示意，不等于完整Agent执行系统。',
3:'# 状态示意：只保存会影响下一步选择的信息，不代表全部字段都要永久持久化。',
4:'# 契约示意：名称/描述/参数可形成模型说明；风险信息与handler供宿主执行。',
5:'# 本地目录示意：名字映射到实现；这些函数对象不会直接序列化给模型。',
6:'# 调用数据示意：标识关联本次执行；期限与租户由宿主用于控制，并非都发给模型。',
7:'# 接口示意：程序根据本次参数及资源判断并发，不仅依赖工具名称。',
8:'# 控制示意：多维预算限制继续工作，耗尽预算不应被标成任务成功。',
9:'# 上下文条目示意：来源与成本用于选择；版本/失效时间只在需要复核时使用。',
11:'# 记忆记录示意：MemoryRecord由应用定义；来源/范围支持核对，置信度不是事实保证。',
13:'# 检查点示意：记录可恢复位置与必要引用；不是所有应用必须照抄的完整Schema。',
14:'# 策略数据示意：规则优先级由实现明确解释；此片段本身不执行授权。',
17:'# 能力目录示意：先用轻量摘要发现，再按load_key加载必要知识或工具定义。',
18:'# 能力声明示意：路由先检查实际支持范围，不能只替换模型名。',
20:'# 诊断事件示意：按排障需要选择关联字段；不默认附带全部消息或秘密。'}
for p in DOCS:
    n=int(p.name[:2]);s=p.read_text()
    def annotate(m):
        code=m[1]
        if 'runnable-example:' in code:return m[0]
        if n==6 and 'return await call_tool()' in code:
            return '''```python
# 反例：下面的函数形状有效，但重试策略错误。不要用于真实写入。
async def unsafe_retry(call_tool):
    for _ in range(3):
        try:
            return await call_tool()
        except Exception:
            # 错误点：吞掉异常且未区分授权、参数、未知副作用等失败。
            pass
```
'''
        if n==6 and code.strip()=='result = func(**args)':comment='# 仅展示裸函数调用：省略了授权、结果语义、超时和副作用判断。'
        elif n==5 and 'handler = tools[name]' in code:comment='# 示意查表分发；实际实现还需处理未知工具、版本和授权。'
        else:comment=COMMENTS.get(n,'# 数据/接口示意：说明结构或步骤，未声明可独立运行。')
        if n==3 and 'class RunState' in code:
            code=code.replace('    run_id: str','    run_id: str  # 关联这一次任务执行').replace('    step_count: int = 0','    step_count: int = 0  # 已推进步数，用于限制与诊断').replace('    artifacts: list[str]','    artifacts: list[str]')
        if n==4 and 'class ToolSpec' in code:
            code=code.replace('    input_schema: dict','    input_schema: dict  # 模型/程序共同约定的参数结构').replace('    handler: Callable[..., Any]','    handler: Callable[..., Any]  # 宿主的真实实现，不发送给模型')
        return '```python\n'+comment+'\n'+code+'```\n'
    s=re.sub(r'```python\n(.*?)```\n',annotate,s,flags=re.S)
    s=s.replace('Context 顺序应该是显式设计，不是 Dict / List 的偶然遍历结果。','Context选择与序列化应有明确规则，并尽量保持历史顺序；不是每轮任意重排旧消息。')
    if n==20:
        s=s.replace('一个 Agent Span 应该记录什么','一个 Agent Span 可按诊断需要记录什么')
        s=s.replace('至少要能重建：','按问题需要，逐步核对：')
    # Remove a duplicated newly-added pitfall only if it is near-identical;
    # preserve the original first occurrence and distinct failure situations.
    a=s.index('<a id="pitfalls"></a>');z=s.index('<a id="self-test"></a>')
    fragment=s[a:z];seen=[];out=[]
    for chunk in re.split(r'\n\s*\n',fragment):
        if chunk.startswith('⚠️'):
            key=re.sub(r'[^\w\u4e00-\u9fff]','',chunk).lower()
            if any(difflib.SequenceMatcher(None,key,old).ratio()>.91 for old in seen):continue
            seen.append(key)
        out.append(chunk)
    s=s[:a]+'\n\n'.join(out).rstrip()+'\n\n'+s[z:]
    p.write_text(s.rstrip()+'\n')

# These are current navigation labels, not changes to source-category metadata.
for name in ['roadmap/knowledge-map.md','roadmap/integration-status.md','roadmap/terminology-glossary.md']:
    p=ROOT/name;s=p.read_text().replace('Agent Harness / Runtime','Agent')
    if name.endswith('terminology-glossary.md'):s=s.replace('Agent Harness','Agent')
    if name.endswith('knowledge-map.md'):
        s=s.replace('23 blocks','24 blocks').replace('23 个知识','24 个知识').replace('23章','24章')
    p.write_text(s.rstrip()+'\n')
p=ROOT/'README.md';s=p.read_text().replace('| Agent Runtime |','| Agent System |');p.write_text(s.rstrip()+'\n')
p=ROOT/'roadmap/documentation-style-guide.md';s=p.read_text()
s+='''

## Agent章末的固定形式（2026-09-17）

HUMAN-A信号提供来源关联；面试回答以Q和🎯可见引用块展示；高频易错点用⚠️逐条提醒；自测以题目本身作为折叠标题。不能把四者统一成“查看参考答案”按钮。正文保留引入、分层解释、例子和失败推演；源码对照可选折叠，不用来源清单代替讲解。
''';p.write_text(s.rstrip()+'\n')
# Optional official sources near the actual lessons, not only one global index.
refs={
2:[('Workflow与Agent的控制方式','https://www.anthropic.com/engineering/building-effective-agents')],
9:[('OpenAI前缀缓存','https://developers.openai.com/api/docs/guides/prompt-caching')],
11:[('Claude Code记忆','https://code.claude.com/docs/en/memory')],
14:[('Claude Code沙箱','https://code.claude.com/docs/en/sandboxing'),('Docker安全','https://docs.docker.com/engine/security/')],
19:[('A2A官方规范','https://a2a-protocol.org/latest/specification/')],
20:[('Agents SDK Tracing','https://openai.github.io/openai-agents-python/tracing/')],
21:[('Anthropic Agent Evals','https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents')],
24:[('Agents SDK执行循环','https://openai.github.io/openai-agents-python/running_agents/'),('Sessions','https://openai.github.io/openai-agents-python/sessions/'),('LangGraph持久化','https://docs.langchain.com/oss/python/langgraph/persistence'),('LangGraph中断','https://docs.langchain.com/oss/python/langgraph/interrupts'),('LangChain Agents','https://docs.langchain.com/oss/python/langchain/agents')]}
for n,urls in refs.items():
    p=DOCS[n-1];s=p.read_text();pos=s.index('<a id="human-a"></a>')
    text='官方核对入口（2026-09-17，协议/产品按文中注明版本）：'+' · '.join(f'[{label}]({url})' for label,url in urls)+'。\n\n---\n\n'
    s=s[:pos]+text+s[pos:];p.write_text(s.rstrip()+'\n')
# Update exact structural counts after editorial de-duplication.
counts={'interviews':0,'self_tests':0,'pitfalls':0}
for p in DOCS:
    t=p.read_text();tail=t[t.index('<a id="interview">'):]
    counts['interviews']+=len(re.findall(r'^### Q：',tail,re.M));counts['self_tests']+=len(re.findall(r'<details><summary>\d+\.',tail));counts['pitfalls']+=len(re.findall(r'^⚠️',tail,re.M))
p=ROOT/'roadmap/agent-reader-revision.md';s=p.read_text();s=re.sub(r'当前24章共\d+个章内问答、\d+个自测、\d+条易错辨析',f'当前24章共{counts["interviews"]}个章内问答、{counts["self_tests"]}个自测、{counts["pitfalls"]}条易错辨析',s);p.write_text(s.rstrip()+'\n')
print('Final editorial counts:',counts)
