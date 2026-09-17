"""Apply reviewed chapters to this checkout; ref publication is a separate step."""
from pathlib import Path
import re, json, subprocess, hashlib, shutil, sys
from _agent_publish_core import *
from _agent_publish_explanations import EDITS,INTROS,mcp_chapter

def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# Do not overwrite a concurrent curriculum edit or silently copy another branch.
for path in OLD_PATHS.values():
    assert (ROOT/path).read_text()==git_text(BASE,path), 'Agent baseline changed: '+path
protected={p:digest(p) for folder in ('research/interviews','research/monitoring','research/analysis') for p in (ROOT/folder).rglob('*') if p.is_file()}
for p in (ROOT/'research/questions').glob('*.md'):
    if p.name not in ('README.md','module-index.md','progress.md'):protected[p]=digest(p)
newtext={}
for i in sorted(OLD_PATHS):
    n=i if i<16 else i+1
    newtext[n]=render(i,n,EDITS,INTROS.get(i))
newtext[16]=mcp_chapter()
# Normalize backed research IDs without changing questions or Source Counts.
for n,t in newtext.items():
    t=corrections(t)
    if n==10 and '`AGENT-010`' not in t:
        t=t.replace('<a id="human-a"></a>','<a id="human-a"></a>\n\n压缩正确性同时对应`AGENT-010`，见研究题库。')
    if n==12:
        t=t.replace('<a id="human-a"></a>','<a id="human-a"></a>\n\n执行状态与历史持久化还对应`AGENT-016`、`AGENT-017`，见研究题库。')
    write('agent/docs/'+NAMES[n-1],t)

# Rich original review diagrams remain, with corrected retention/trace semantics.
review=git_text(OLD,'agent-harness/review/README.md')
review=review.replace('# Agent Harness / Runtime｜','# Agent｜').replace('23 个知识小板块','24 个知识小板块')
review=review.replace('Durable Truth\n├─ State\n├─ Event Log\n├─ Artifact\n└─ Memory','可核对/复用的信息来源\n├─ 必要状态与业务回执\n├─ 交互记录\n├─ 产物和外部事实\n└─ 经过筛选的记忆（仍可能过期或有误）')
review=review.replace('图 4｜安全四层','图 4｜同一次动作的不同安全检查')
review=review.replace('→ idempotent retry / compensation','→ 已确认则补齐记录；未执行且可安全重试才重试\n→ 无法确认则保持待核对，不自动重做或补偿')
review=review.replace('当时模型看到了什么、做了什么 Tool Call、环境真实结果是什么、State 怎样变化、为何失败/重试。','先定位阶段、耗时和错误，再按需要取得授权的输入与工具证据；关键回执独立保存，不默认永久全量Trace。')
review=review.replace('让 retry、budget、checkpoint、trace、cancel、approval 都有明确 scope。','声明本项目的会话、任务执行、反馈轮与步骤口径，让重试、预算、取消与恢复有明确范围；产品Turn需单独映射。')
review+='\n\n---\n\n## 按薄弱主题回到正文\n\n'+' · '.join(f'[{i:02}](../docs/{p})' for i,p in enumerate(NAMES,1))+'\n\n编号与正式课程一致，复习可独立按个人节奏使用。'
review+='\n\n## 综合失败推演\n\n'
scenarios=[
('同一工具连续失败，应该重试、修参数还是终止？','先区分结构、语义、权限、依赖与副作用阶段。缺参数可让模型有限修复；短暂依赖故障按预算重试；权限拒绝不绕过；结果未知先核对。'),
('压缩后忘了“不修改原件”，只修摘要就够吗？','上下文选择与压缩会影响决策，但禁止写入还应由真实权限与执行隔离保证。分别测试摘要是否保留约束、授权门是否拒绝越界，不能互相替代。'),
('工具成功后检查点未写，用户又取消，怎样恢复？','核对稳定操作身份和外部结果，补齐事实再决定继续或停止。取消不等于已执行动作回滚；没有核对能力时不能靠重复执行来确认。'),
('MCP断线是否意味着远端没有执行？','不意味着。协议连接与业务结果是不同问题。目录可以重新发现，已发出的写操作仍需核对；RPC请求ID本身不是幂等保证。'),
('子Agent循环等待并同时写一个文件，是同一种故障吗？','循环等待用依赖图、委派深度与超时处理；共享写入用所有权、隔离工作区或版本合并处理。上下文隔离不能自动解决两者。'),
('新模型Benchmark更高分，生产更慢，怎样判断？','分结果、过程、组件、成本和安全指标，核对任务分布与评分设置，再用Trace定位耗时和Provider兼容。单一分数不够证明适合本任务。')]
for k,(q,a) in enumerate(scenarios,1):review+=f'<details><summary>{k}. {q}</summary>\n\n{a}\n\n</details>\n\n'
write('agent/review/README.md',links(review))
# Keep the known 56-question drill, not replace it with just chapter summaries.
for file in ('高频面试题.md','面试易错点.md'):
    s=git_text(BASE,'agent-harness/interview/'+file)
    s=s.replace('# Agent Harness / Runtime','# Agent')
    write('agent/interview/'+file,links(corrections(s)))
quick=git_text(OLD,'agent-harness/interview/面试前速查表.md')
quick=quick.replace('# Agent Harness / Runtime','# Agent').replace('Run / Session\n└─ Turn\n   └─ Step','Session（持续会话）\n└─ Run（任务执行）\n   └─ Turn（本书的反馈轮）\n      └─ Step（具体步骤）\n\n产品Turn含义可能不同，先声明口径再映射。')
quick=quick.replace('Security 三层','Security 三种责任').replace('至少能重建：','按问题关联并取得足够的证据，不默认全量保留：')
quick+='\n\n**记录边界：** 恢复状态与关键回执按业务可靠性保存；Trace优先采集阶段、状态、耗时、错误与引用，敏感原文只在授权范围按需取得。ID不等于版本，保存数据不保证重演模型和外部世界。'
write('agent/interview/面试前速查表.md',links(corrections(quick)))

home=git_text(BASE,'agent-harness/README.md')
home=home.replace('# Agent Harness / Runtime｜Agent 执行系统','# Agent｜从任务到可解释、可验证的执行系统')
home=home.replace('23 个连续知识小板块','24 个连续知识小板块').replace('44 道 Canonical → 23 个教材知识块','44 道 Canonical → 24 个教材知识块')
home=re.sub(r'> \*\*质量：[^\n]*','> **质量：以丰富旧版为底稿保留机制、例子和失败处理，恢复展开式教学与章末四部分；本轮检查范围见修订记录。**',home)
home=home.replace('→ **Agent Harness / Runtime** →','→ **Agent** →')
start=home.index('## 5. 正式课程目录');end=home.index('\n## 6.',start)
toc=['## 5. 正式课程目录','章节数由认知依赖与内容边界决定，不以另一个分支的16章为目标。MCP独立讲清协议往返；Skill/Hook/Plugin另讲扩展生命周期。其余主题保留完整机制，在章内调整定义、过程、失败与实现对照的顺序。']
for h,ran in [('A｜先认识任务与执行系统',range(1,4)),('B｜工具调用怎样受控完成',range(4,8)),('C｜控制方向与模型可见信息',range(8,12)),('D｜当前状态与跨中断恢复',range(12,14)),('E｜安全、能力接入与协作',range(14,20)),('F｜诊断、评测与工程落地',range(20,25))]:
    toc.append('### '+h)
    toc.extend(f'{n}. [{TITLES[n-1]}](docs/{NAMES[n-1]})' for n in ran)
home=home[:start]+'\n\n'.join(toc)+'\n\n---\n'+home[end:]
home=home.replace('docs/01 → 23','docs/01 → 24').replace('01–23 连续','01–24 连续')
home=home.replace('每章先用中文和例子解释概念，再展开机制；产品实现放在可选折叠中。章末保留**面试怎么答、易错点、章节自测**，不是只链接到另一页。源码案例以固定提交为准，MCP/A2A与框架按明确官方版本讲解。','每章保留轻松引入、逐层解释、过程图、例子与失败边界，不压成结论提纲。章末固定**HUMAN-A信号 → 面试怎么答 → 高频易错点 → 本章自测**：🎯面试答案直接显示，⚠️易错点逐条提醒，只有自测答案和可选产品实现折叠。代码只用于明确的教学目的，并有注释及适用边界。')
home=home.replace('Reader Revision     ✅ 已完成讲解与训练修订','Reader Revision     已完成本轮保留式教学修订')
write('agent/README.md',links(home))
shutil.rmtree(ROOT/'agent-harness')

# Rewrite ordinary local links throughout the checkout. Preserve historical
# research texts and stable agent-harness.md metadata identifiers verbatim.
nav_questions={'README.md','module-index.md','progress.md'}
for p in ROOT.rglob('*.md'):
    if '.git' in p.parts or p in protected:continue
    s=p.read_text();before=s;rel=p.relative_to(ROOT).as_posix()
    s=links(s).replace('[Agent Harness / Runtime]','[Agent]').replace('[Agent Harness]','[Agent]')
    if rel in ('README.md','roadmap/knowledge-map.md','roadmap/integration-status.md','research/questions/progress.md','roadmap/content-depth-audit.md'):
        s=s.replace('184','185')
        lines=[]
        for line in s.splitlines():
            if 'agent/README.md)' in line and line.startswith('|'):line=re.sub(r'\|\s*23\s*\|','| 24 |',line)
            lines.append(line)
        s='\n'.join(lines)
    if rel=='README.md':
        s=s.replace('agent-harness/','agent/')
        s=s.replace('从任务与执行角色出发，理解工具、上下文、记忆、状态、安全和恢复；用可核对的产品过程与每章训练把概念落地。','从任务与执行角色出发，逐步理解工具、上下文、状态、安全、协议、协作与评测；保留完整机制、失败推演和章末训练。')
    if rel=='roadmap/learning-path.md':s=s.replace('184','185').replace('Agent Harness / Runtime','Agent').replace('Week 11｜Agent Harness 前半','Week 11｜Agent 前半').replace('Agent `22–23`','Agent `22–24`').replace('Agent 13–23','Agent 13–24')
    if rel=='research/questions/module-index.md':
        s=s.replace('| Agent Harness / Runtime |','| Agent |').replace('| 44 | 23 |','| 44 | 24 |').replace('→ Agent Harness；','→ Agent；')
        s=re.sub(r'> \*\*v1.0 Final Quality Audit[^\n]*','> 旧184篇终审为历史记录；当前185篇中Agent24章的保留核对与实际检查见[修订记录](../../roadmap/agent-reader-revision.md)。研究兼容标识与题目频次保持不变。',s)
    if rel=='research/questions/README.md':s=s.replace('| Agent Harness / Runtime |','| Agent |')
    if rel=='roadmap/terminology-glossary.md':s=s.replace('Agent Harness','Agent')
    if rel=='research/agent-sources/README.md':
        s=s.replace('# Agent Harness｜','# Agent｜').replace('23-block 教材','24章教材').replace('稳定为 23 个','当前为 24 个').replace('[`../../agent-harness/README.md`]','[Agent教材]')
    if rel=='roadmap/curriculum-granularity-audit.md':s=s.replace('| Agent Harness | 47 old blocks / 44 Canonical | 23 | ✅ |','| [Agent](../agent/README.md) | 原23章丰富版 / 44 Canonical；协议与扩展生命周期分别闭环 | 24 | 已重组并核对内容去向 |')
    if rel=='roadmap/content-depth-audit.md':
        s=re.sub(r'> \*\*2026-09-17[^\n]*','> **2026-09-17：** Agent24章已恢复展开式教学并核对旧版内容。185篇为当前结构计数；不以历史PASS或文件大小证明读者理解。详见[修订记录](agent-reader-revision.md)。',s,count=1)
        s=s.replace('| 24 | ✅ `01–23`','| 24 | ✅ `01–24`')
    if rel=='research/questions/progress.md':
        s=re.sub(r'> \*\*2026-09-17[^\n]*','> **2026-09-17 Agent更新：** 当前24章、全库185篇；以丰富旧版保留机制与失败处理，恢复章末四种形式。详见[修订记录](../../roadmap/agent-reader-revision.md)。',s,count=1)
    if s!=before:p.write_text(s.rstrip()+'\n')

# The capability map is navigation, not a parallel curriculum or changed research.
write('research/agent-sources/runtime-capability-map.md','# Agent｜能力与正式章节映射\n\n[← 源码与官方资料](README.md) · [Agent教材](../../agent/README.md)\n\n本页用于查主责位置，不另建学习路线。研究兼容标识`agent-harness.md`、44题ID和频次不变。\n\n| 正文章节 | 能力主责 |\n|---|---|\n'+''.join(f'| [{n:02}](../../agent/docs/{p}) | {TITLES[n-1]} |\n' for n,p in enumerate(NAMES,1))+'\n旧小节的去向见[保留核对](../../roadmap/agent-reader-revision.md)。')
# Don't erase historical audit evidence; explicitly supersede its scope.
p=ROOT/'roadmap/final-quality-audit.md';s=p.read_text();s=re.sub(r'(^# [^\n]*\n)',r'\1\n> **当前Agent为24章。** 旧23章/184篇结论为历史记录；本轮185篇结构及Agent保留检查见[修订记录](agent-reader-revision.md)，不以历史PASS替代新版本教学判断。\n',s,count=1);p.write_text(s)

counts={}
for n,p in enumerate(NAMES,1):
    t=(ROOT/'agent/docs'/p).read_text()
    tail=t[t.index('<a id="interview">'):]
    counts[n]={'interviews':len(re.findall(r'^### Q：',tail,re.M)), 'self_tests':len(re.findall(r'<details><summary>\d+\.',tail)), 'pitfalls':len(re.findall(r'^⚠️',tail,re.M))}
total={k:sum(v[k] for v in counts.values()) for k in ('interviews','self_tests','pitfalls')}
report='''# Agent 内容保留、教学修订与发布记录

[← Agent教材](../agent/README.md) · [Handbook](../README.md) · [历史终审](final-quality-audit.md)

## 1. 这次的底稿和边界

以用户认可的丰富旧main `37cbfd2b152c6a0aa5bbd8ca0c19820debc632b8`为教学底稿，以`83a3b96c10d8a3feb2c87d8fa2e59c02b8e8f178`为发布前基线。不再把压缩版当主要底稿，也不合并16章架构分支。

原23章调整为24章：MCP完整协议生命周期与Skill/Hook/Plugin扩展生命周期分别讲清；其余知识范围保留，在章内组织定义、过程、例子、失败与实现对照。章节数是边界判断结果，不是预设目标。

## 2. 保留的教学过程与明确修正

原编号小节的机制、例子、错误与失败推演逐项记录去向。不能用一个全局“重试/降级”清单替代某机制独有的故障窗口。章末保持HUMAN-A信号、可见的Q与🎯回答、⚠️易错提醒、题目可点击的折叠自测四种形式。源码对照可选折叠，面试答案不隐藏。

不是逐字保留错误：损坏缩进的旧循环代码换成有注释的教学例子；Session/Run/Turn/Step声明本书口径并与产品对象分别解释；128k预算表修正算术；工具调用不等于跨系统原子事务；前缀缓存与回答缓存分开；Trace与必要恢复记录分别留存；协议和框架按官方核心语义展开。这些改动的原因在下表标明。

## 3. 重点核对的失败机制

工具结构/语义错误、拒绝授权、临时故障、超时、未知/部分副作用；并发资源冲突、取消传播和迟到回执；重复行动、计划偏离；大结果、过期上下文、摘要遗漏与压缩失败；记忆错误/冲突/过期；检查点间崩溃、恢复核对、租约和分叉；批准对象变化、注入、凭证与外传；扩展失效和版本不兼容、供应商降级；子任务失败、循环委派、共享工作区；诊断不足、评测回归遗漏、代码验证与交付、生产故障域及框架升级迁移。

它们仍在对应主责章节，不是因主题重复出现就删除。需要重复的桥梁会说明各责任检查什么，避免多章都给同一段万能答案。

## 4. 原小节去向

下面是内容组织的可检查记录，不把锚点存在或文本命中率等同于技术质量。原章末形式合并回本章；源码实现放回可选对照。

<details>
<summary>展开原23章的编号小节与新位置</summary>

| 原章/节 | 原小节 | 新位置 | 处理 |
|---|---|---|---|
'''
label={'retained':'保留并增补解释','source':'保留到章内来源对照','corrected':'明确修正后讲解','protocol':'完整协议章','human-a':'HUMAN-A','interview':'面试回答','pitfalls':'易错辨析','self-test':'自测','follow':'追问'}
for i,k,title,n,kind,why in DISPOSITIONS:
    anchor={'follow':'interview'}.get(kind,kind) if kind in ('human-a','interview','pitfalls','self-test','follow') else f'legacy-{i:02}-{k:02}'
    report+=f'| {i:02}/{k:02} | {title.replace("|","/")} | [{n:02}](../agent/docs/{NAMES[n-1]}#{anchor}) | {label[kind]}'+('：'+why if kind in ('corrected','protocol') else '')+' |\n'
report+='\n</details>\n\n## 5. 训练与检查范围\n\n'+f'当前24章共{total["interviews"]}个章内问答、{total["self_tests"]}个自测、{total["pitfalls"]}条易错辨析。集中56题保留，44道Agent研究能力不变。题数不证明读者已经理解。\n\n'
report+='''运行`python tools/validate_agent_readability.py --run-examples`检查编号、四种章末结构、旧小节去向、44题覆盖、代码围栏、普通本地链接以及标记教学例子。源码对照使用原固定提交，MCP/A2A和框架按注明官方版本；教学补充不是新面经。

机械通过不等于所有外部URL/渲染器都验证，也不是模型、真实工具或生产数据库故障实验。只有实际执行的教学断言可声称通过。人工逐节对照和读者理解仍是不同质量维度，不能用大文件或旧PASS替代。

## 6. 发布与恢复

本轮发布目标是main，正式入口`agent/README.md`，全库185篇。原版备份`backup/agent-original-main-37cbfd2`及修订前备份`backup/agent-before-style-repair-83a3b96`保留。可仅恢复Agent及其必要导航，不需强制回退整仓库或新研究数据。16章架构分支不在本轮修改范围。
'''
write('roadmap/agent-reader-revision.md',report)
# Keep old question records and empirical source counts intact.
assert all(digest(p)==h for p,h in protected.items()), 'Protected research changed'
print('Original sections assigned:',len(DISPOSITIONS),'Chapter training:',total,'Protected research unchanged:',len(protected))
write('tools/_agent_publication_result.json',json.dumps({'baseline':BASE,'original':OLD,'chapters':24,'total_curriculum':185,'dispositions':DISPOSITIONS,'training':counts,'protected':len(protected)},ensure_ascii=False,indent=2))
