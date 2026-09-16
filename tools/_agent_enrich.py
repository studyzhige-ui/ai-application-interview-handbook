from pathlib import Path
import re, subprocess, hashlib
import _agent_content, _agent_training
ROOT=Path(__file__).resolve().parents[1]
BASE='0266cbfa131ff4157cad9f4c18b75fe153c0b846'
BEFORE='2fbd42e65940b961e6c2edb17bc87940feb028ff'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
protected=[p for folder in ['research/interviews','research/questions','research/analysis','research/agent-sources'] for p in (ROOT/folder).rglob('*') if p.is_file() and p.name!='progress.md']
protected_before={str(p):digest(p) for p in protected}
for p in ['tools/_agent_survey.md','tools/_agent_missing.md']:
    (ROOT/p).unlink(missing_ok=True)
_agent_content.apply()
_agent_training.apply()
# A single table must not be split by paragraph separators used for the surrounding prose.
p=ROOT/'agent/interview/README.md'; t=p.read_text()
t=re.sub(r'(?m)(^\|[^\n]*\|\n)\n(?=\|)',r'\1',t); p.write_text(t)
p=ROOT/'agent/README.md'; t=p.read_text()
t=t.replace('**状态：分层重构版**','**状态：分层增强版｜教学与训练补强完成**')
t=t.replace('真人面经只调整复习权重，不打乱第一次学习顺序。','真人面经只校准复习权重、真实问法与追问深度，不打乱第一次学习顺序。')
t=t.replace('只用来决定复习深度','只用来校准复习权重、问法与追问深度')
t=t.replace('第一遍只按下面01→16阅读，不需要先读另一个总纲、术语百科或项目案例。每章都包含承接关系、核心机制、失败/取舍、自测与下一章链接。','第一遍按下面01→16阅读，不需要另读总纲或项目案例。前两章用同一个通用文件报告推导契约与控制权；后续先解释黑盒输入输出，再逐步展开实现。长章有分段提示，代码/源码对照用于核验机制，不构成第二条课程。')
t=t.replace('复习和面试页不再复制一份正式教材。','复习和面试页不复制正式教材：Review提供16章回忆检查与6个综合失败推演；Interview按同一主线保留main的56个细粒度练习，新增8个系统推导题，并在同一页提供86个易错辨析与速查。练习数量不等于真人Canonical数量。')
t=t.replace('正文16章连续；复习与面试各一个入口。','正文16章连续；复习与面试各一个入口。每章含阅读提示、至少4个折叠自测；第04章提供无网络、无真实副作用的最小循环练习。')
t=t.replace('第一次沿01→16建立因果链。','可按个人节奏学习，不绑定Week/Session。第一次沿01→16建立因果链。')
p.write_text(t)
p=ROOT/'README.md'; t=p.read_text().replace('Python 额外保留 Coding 小题；Agent / FastAPI / AIBE 还维护专门的权威资料或源码索引。','Python 额外保留 Coding 小题；Agent把高频练习、易错点与速查合并在一个 `interview/README.md`，不增加平行教材。Agent / FastAPI / AIBE 还维护专门的权威资料或源码索引。'); p.write_text(t)
# Freeze the research, not just its final counts.
assert protected_before=={str(p):digest(p) for p in protected},'research evidence changed'
subprocess.run(['python','tools/validate_agent_curriculum.py'],cwd=ROOT,check=True)
docs=sorted((ROOT/'agent/docs').glob('*.md'))
for p in docs:
    t=p.read_text(); assert 'enrichment: reading-guide' in t and t.count('<details>')>=4,p
inter=(ROOT/'agent/interview/README.md').read_text()
assert sorted(map(int,re.findall(r'legacy-question: (\d+)',inter)))==list(range(1,57))
assert len(re.findall(r'<summary>Q\d{2}｜',inter))==64
assert sorted(map(int,re.findall(r'^(\d+)\. ❌',inter,re.M)))==list(range(1,87))
assert '继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？' not in inter
# Run only the explicitly authored deterministic teaching example, not arbitrary documentation code.
loop=next((ROOT/'agent/docs').glob('04-*.md')).read_text()
example=re.search(r'<!-- runnable: report-loop -->\s*```python\n(.*?)\n```',loop,re.S)
assert example
result=subprocess.run(['python','-I','-c',example.group(1)],text=True,capture_output=True,timeout=10,check=True)
assert '5 cases passed' in result.stdout
print(result.stdout.strip())
# Explicit anchors are checked for Agent navigation (including chapter parts and question anchors).
for p in (ROOT/'agent').rglob('*.md'):
    text=re.sub(r'```.*?```','',p.read_text(),flags=re.S)
    for target in re.findall(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)',text):
        if target.startswith(('http:','https:')) or '#' not in target: continue
        path,frag=target.split('#',1); dest=(p.parent/path).resolve() if path else p
        if re.fullmatch(r'(part-\d+|q-\d+|concept-map)',frag):
            assert f'id="{frag}"' in dest.read_text(),(p,target)
# Reuse existing audit files, and distinguish semantic review from mechanical checks.
mark='## 2026-09-16｜Agent 分层增强：吸收 main 的机制与训练优势'
mapping='''| main旧章 | 当前主责 | 处理结果 |
|---|---|---|
| 01–02 | 01–04 | 契约/控制权推导、Model与Harness边界；不恢复另一套八平面总纲 |
| 03 | 04、07 | Loop/事件/状态保留；纠正通用Run/Turn树，替换为可运行教学Loop |
| 04–05 | 10 | Contract、schema/语义、Registry/曝光、发现/版本与源码对照 |
| 06–07 | 11 | 结果投影、错误、并发/取消、迟到回执与具体实现线索 |
| 08 | 04 | Planning、ReAct、停止、预算、Steering全部沿控制循环组织 |
| 09–10 | 05 | 组装/预算/外部化/压缩/正确性；补回源码阶段、澄清缓存类型 |
| 11 | 06 | Memory生命周期、纠错、来源与索引失效 |
| 12–13 | 07、13 | 状态、检查点、恢复、操作核对、Fork与环境引用 |
| 14–15 | 13–14 | 执行隔离、审批绑定、注入/凭证/外传与威胁边界 |
| 16 | 12 | MCP/Skill/Hook、目录/版本与渐进加载；安全门不可仅靠可选Hook |
| 17 | 03、09 | 意图路由与模型能力策略/供应商适配分开 |
| 18 | 08 | 交接、预算、取消、A2A、共享工作区与证据汇聚 |
| 19–20 | 15 | Trace、三种Replay、评分、回归与持续改进；补具体测试矩阵 |
| 21 | 12、13、16 | 资源搜索、工作区/patch、测试/diff/交付验证 |
| 22–23 | 16 | Gateway/持久层职责、部署/成本、框架选型/迁移与实现对照 |
'''
body=f'''\n\n{mark}\n\n对照来源：main `{BASE}`；增强前分支 `{BEFORE}`。保留任务→四层→治理16章主线，不恢复旧23章目录或另一套架构课程。\n\n{mapping}\n人工复核与修改依据：对23章旧正文和16章新正文做分节/段落保留候选扫描，再审阅差异；扫描只帮助定位，不把文本命中率当作语义覆盖率。核心机制已保留的段落不重复搬运；重点补回实现对照、最小循环与具体练习。前两章新增通用任务的完整推导；每章增加有边界的阅读提示与情景自测；16章长文按章节内部责任分段，而不是继续拆文件。\n\n**不照搬的内容：** 旧八平面不作为第二套架构；旧Session→Run→Turn树不当通用标准；旧不完整/缩进有问题的示例不冒称可运行；Tool Execution不是天然跨系统事务；Prompt Cache不等于缓存最终回答。教学补充和既有固定源码阅读记录分别标明；不声称本轮重新遍历全部产品源码。\n\n**训练迁移：** 旧main高频练习56/56保留能力范围并配具体追问与掌握标准，新增8道教学推导题，共64题；旧易错辨析实际86条（不是此前聊天里的90条）整合到同一面试入口；速查按新主线重组。44个ACTIVE Canonical映射保持一致；自拟追问不冒充Verified Follow-up Chains。\n\n**实际检查：** 16章连续、177篇全仓库正文计数；每章阅读提示和至少4个折叠自测；56个旧练习标识完整、64题和86辨析计数；旧目录/平行架构课程不存在；相对文件链接与Agent显式锚点；研究问题、面经、统计与固定源码索引本轮逐文件摘要不变。第04章唯一标记的纯Python教学Loop实际执行5个断言场景通过（正常、越界、未读引用、预算、未知决策）。\n\n**范围限制：** 这是一轮教材结构/机制迁移、例子与训练质量复核，不等于177篇逐句事实重审，也不等于真实模型、外部工具、沙箱或多worker生产故障测试。其余代码明确作为骨架/伪代码，产品版本细节仍按引用快照与官方资料核验。\n'''
for name in ['roadmap/content-depth-audit.md','roadmap/final-quality-audit.md']:
    p=ROOT/name; t=p.read_text()
    if mark not in t: t+=body
    if name.endswith('content-depth-audit.md'):
        t=t.replace('结构迁移已验证；深度为原版记录','分层增强与机制/训练迁移复核完成；范围见文末')
        t=t.replace('Agent为16章分层重构版，全仓库177篇正文。旧版深度与终局审计为历史记录；本次验证范围为结构、链接、迁移覆盖和证据不变性，详见既有质量记录。','Agent为16章分层增强版，全仓库177篇正文；本轮已完成机制迁移、通用推导示例、细粒度训练与结构验证，范围和限制见文末。旧全仓库终审仍是历史记录。')
    else:
        t=t.replace('> **结论：✅ PASS — 当前仓库可以作为 v1.0 Candidate。**','> **历史结论：✅ PASS — 适用于下述旧v1.0审计范围；当前Agent增强范围见文末。**',1)
    p.write_text(t)
p=ROOT/'roadmap/curriculum-granularity-audit.md'; t=p.read_text().replace('| Agent | 23章旧课程 / 44 Canonical | 16 | 分层重构 |','| Agent | 23章旧课程 / 44 Canonical | 16 | 分层增强与迁移复核完成 |'); p.write_text(t)
p=ROOT/'research/questions/progress.md'; t=p.read_text()
t=t.replace('Agent为16章分层重构版，全仓库177篇正文。旧版深度与终局审计为历史记录；本次验证范围为结构、链接、迁移覆盖和证据不变性，详见既有质量记录。','Agent为16章分层增强版，全仓库177篇正文；机制迁移、通用推导示例、64道细粒度训练及结构检查已完成，详见质量记录。真实模型与外部工具集成测试不在本轮范围。')
t=re.sub(r'\*\*v1\.0 Final Quality Audit：.*?详见.*?。', '**历史v1.0 Final Quality Audit：PASS，仅适用于旧版184篇审计。** 当前Agent16章增强的机制迁移、例子和训练检查另见[质量记录](../../roadmap/final-quality-audit.md)，不以历史PASS代替新版本验证。',t,count=1,flags=re.S)
p.write_text(t)
subprocess.run(['python','tools/validate_agent_curriculum.py'],cwd=ROOT,check=True)
assert protected_before=={str(p):digest(p) for p in protected}
print('PASS: 16 chapters, 64 interview drills, 56 legacy drill scopes, 86 pitfalls, unchanged research and 5 executed teaching cases')
