#!/usr/bin/env python3
"""One-time, branch-local curriculum migration. Removed after verification.

No external data is fetched. Original interview evidence is immutable.
The final result has one Agent curriculum, not an extra architecture guide.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / 'agent-harness'
NEW = ROOT / 'agent'
assert OLD.is_dir() and not NEW.exists(), 'Refuse unexpected or already-migrated tree'
old_files = {int(p.name[:2]): p for p in sorted((OLD / 'docs').glob('*.md'))}
assert set(old_files) == set(range(1, 24))
original = {n: p.read_text(encoding='utf-8') for n, p in old_files.items()}
raw_evidence = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (ROOT / 'research/interviews').rglob('*') if p.is_file()}

CHAPTERS = [
 ('AgentSystemAndTaskContract', 'Agent 系统与任务契约', '设计输入'),
 ('CapabilityAndAutonomy', '能力设计与自主权分配', '设计决策'),
 ('ApplicationAndInteraction', 'L1 应用层：任务、流程与用户交互', 'L1 应用层'),
 ('AgentLoopAndControl', 'L2 运行层：执行循环与控制', 'L2 运行层'),
 ('ContextEngineering', 'L2 运行层：上下文组装、预算与压缩', 'L2 运行层'),
 ('MemoryLifecycle', 'L2 运行层：记忆的选择、使用与维护', 'L2 运行层'),
 ('StateAndRecovery', 'L2 运行层：执行状态、持久化与恢复', 'L2 运行层'),
 ('MultiAgentCoordination', 'L2 运行层：多 Agent 协作与调度', 'L2 运行层'),
 ('ModelAccessAndRouting', 'L3 接入层：模型适配、路由与容错', 'L3 接入层'),
 ('ToolContractAndDiscovery', 'L3 接入层：工具契约、注册与发现', 'L3 接入层'),
 ('ToolExecutionAndEffects', 'L3 接入层：工具执行、副作用与取消', 'L3 接入层'),
 ('KnowledgeAndCapabilityAccess', 'L3 接入层：知识、记忆与扩展能力接入', 'L3 接入层'),
 ('ResourcesAndEnvironments', 'L4 资源层：模型、数据与执行环境', 'L4 资源层'),
 ('IdentityPermissionsAndSafety', '横切治理：身份、权限、审批与安全', '安全治理，贯穿 L1–L4'),
 ('ObservabilityAndEvaluation', '横切治理：观测、评测与持续改进', '质量运营，贯穿 L1–L4'),
 ('ProductionArchitectureAndEvolution', '系统收口：部署、成本、选型与演进', '四层组合与工程落地'),
]
NAMES = {i: f'{i:02d}-{x[0]}.md' for i, x in enumerate(CHAPTERS, 1)}
OLD_TO_NEW = {1:1,2:2,3:4,4:10,5:10,6:11,7:11,8:4,9:5,10:5,11:6,12:7,13:7,14:14,15:14,16:12,17:9,18:8,19:15,20:15,21:16,22:16,23:16}
QUESTION_OWNER = {1:2,2:1,3:4,4:4,5:4,6:4,7:4,8:5,9:5,10:5,11:5,12:5,14:6,15:6,16:6,17:7,18:10,19:10,20:11,21:10,22:10,23:12,24:12,25:12,26:11,27:7,28:14,29:7,30:8,31:8,32:9,34:15,35:15,36:16,37:12,38:9,41:15,42:4,43:15,44:14,45:3,46:8,47:16,48:16}
DESC = '从任务契约与自主权出发，沿应用、运行、接入、资源四层组织 Agent，并贯通安全、质量与生产演进。'
MAP = '''设计输入：业务场景
    ↓
任务契约：为谁做什么、允许做什么、怎样算完成
    ↓
能力与自主权：哪些交给模型判断，哪些必须由程序控制
    ↓
L1 应用层：任务入口、业务流程、用户交互、结果交付、人工接管
    ↓ 使用
L2 运行层：执行循环、上下文、记忆策略、执行状态、调度与恢复
    ↓ 通过稳定接口使用
L3 接入层：模型适配、工具接口、检索接口、状态与记忆存取接口
    ↓ 连接
L4 资源层：模型服务、知识与数据库、外部系统、文件与执行环境

贯穿四层：安全治理（身份、权限、审批、隔离、审计）
贯穿四层：质量运营（观测、评测、成本、可靠性、持续改进）'''


def sections(text: str) -> dict[int, str]:
    result, current, buf, fence = {}, None, [], False
    for line_no, line in enumerate(text.splitlines()):
        if re.match(r'^\s*(```|~~~)', line):
            fence = not fence
        m = None if fence or line_no == 0 else re.match(r'^(#{1,3})\s+(\d{1,2})[.．、]\s+(.+)$', line)
        if m:
            if current is not None:
                result[current] = '\n'.join(buf).strip()
            current, buf = int(m.group(2)), [line]
        elif current is not None:
            buf.append(line)
    if current is not None:
        result[current] = '\n'.join(buf).strip()
    return result

PARTS = {n: sections(t) for n,t in original.items()}
USED: dict[int, set[int]] = {n:set() for n in original}
GROUPS: dict[int, list[tuple[str,str]]] = {n:[] for n in NAMES}


def clean_section(text: str) -> str:
    lines = text.splitlines()
    base = len(re.match(r'^(#+)', lines[0]).group(1))
    out, fence = [], False
    for idx, line in enumerate(lines):
        if re.match(r'^\s*(```|~~~)', line):
            fence = not fence
        if not fence:
            if line.strip() == '---':
                continue
            m = re.match(r'^(#{1,6})\s+(.+)$', line)
            if m:
                heading = re.sub(r'^\d+(?:\.\d+)*[.．、]?\s*', '', m.group(2))
                level = 3 if idx == 0 else min(6, max(4, len(m.group(1))-base+3))
                line = '#' * level + ' ' + heading
            if re.match(r'^(下一章|后续\s*\d+\s*个知识|这些直接进入下一章|多租户 State 下一章)', line.strip()):
                continue
        out.append(line)
    text = '\n'.join(out).strip()
    text = text.replace('Eval 分四层', '评测的四个验证视角（不是架构层）')
    text = text.replace('Routing 至少有三层', '三类路由对象（不是新增架构层）')
    text = text.replace('三层边界', '三种安全责任：Policy、Approval 与 Sandbox')
    text = text.replace('Provider Adapter 为什么是 Runtime 能力', 'Provider Adapter 的接入职责')
    text = text.replace('Tool Execution 是一个 Runtime Transaction，而不是函数调用语法糖。', 'Tool Execution 是受管理的调用生命周期，不自动具有跨系统原子事务语义。')
    text = text.replace('Production Architecture 必须放在最后', '生产部署需要在职责与机制清楚之后讨论')
    return re.sub(r'\n{3,}', '\n\n', text)


def take(old: int, nums: list[int] | range) -> str:
    out = []
    for num in nums:
        assert num in PARTS[old], (old, num, sorted(PARTS[old]))
        USED[old].add(num)
        out.append(clean_section(PARTS[old][num]))
    return '\n\n'.join(out)


def group(ch: int, title: str, text: str, *chunks: str) -> None:
    GROUPS[ch].append((title, '\n\n'.join([text.strip(), *chunks]).strip()))

# New conceptual spine: the old overview is replaced, not added as a second guide.
group(1, '先定义系统要对什么结果负责', '''本课程讨论 LLM 驱动的软件 Agent。Agent 是在目标与约束内，根据观察到的信息动态选择行动、接收反馈并推进任务的执行角色。Agent 系统还必须负责承接任务、组织执行、交付结果和治理风险。

不要从“需要 Memory、RAG、多个 Agent”开始。先写任务契约：它是设计输入和验收依据，不是要部署的一个服务。

| 契约字段 | 要明确的问题 | 为什么先于技术选择 |
|---|---|---|
| 服务对象与目标 | 谁把什么工作交给系统？ | 决定输入、交互和完成标准 |
| 范围与非目标 | 系统做什么、不做什么？ | 防止自动扩展任务与权限 |
| 输入与运行环境 | 有哪些数据、接口、文件、事件与执行条件？ | 决定能力是否可获得、能否验证 |
| 自主权与动作边界 | 可以建议、查询、修改到什么程度？谁确认？ | 决定控制与安全边界 |
| 输出与验收 | 交付文本、文件、结构化结果，还是外部状态变化？ | 决定完成证据而非只看回复 |
| 运行约束 | 时延、成本、并发、持续时间、隐私与恢复要求？ | 决定调度、持久化和部署方式 |

任务开始前不必知道全部中间步骤，但必须知道如何判定范围、风险和结果。任务契约可以因澄清而更新；更新要有版本，不能悄悄改变已获批准的动作。''')
group(1, '一张固定的职责图', '```text\n' + MAP + '\n```\n\n这四层是本教材的综合参考架构，不是 Codex 或行业统一颁布的标准。它们表达谁负责什么、通过什么接口协作，不表示所有数据都必须顺序经过四个网络服务。')
group(1, '四层之间分别交接什么', '''| 层 | 核心问题 | 向下一层交接 | 不应包办什么 |
|---|---|---|---|
| L1 应用 | 如何承接任务并交付可理解的结果？ | 目标、身份上下文、约束、任务配置、交互事件 | 不自行实现每种模型和工具协议 |
| L2 运行 | 如何持续、受控地推进执行？ | 模型请求、工具调用、检索请求、状态读写请求 | 不把模型建议视作已授权的真实动作 |
| L3 接入 | 如何把能力变成稳定且可校验的接口？ | 供应商请求、业务 API、查询、执行命令 | 不替代业务系统自己的授权和事务 |
| L4 资源 | 真实能力与事实在哪里，副作用在哪里发生？ | 返回结果、证据、回执、产物引用 | 不替上层定义任务成功 |

应用可以调用一个确定性流程，流程中的某一段使用 Agent；Agent 又可以通过接口调用另一个 Agent。层次不因这种组合而改变。身份与策略随调用传递，观测与审计覆盖整个过程。''')
group(1, '层、模块、机制、对象、协议与资源不要混排', '''| 类型 | 表达什么 | 示例 |
|---|---|---|
| 层 | 稳定的职责边界 | 应用层、运行层 |
| 模块 | 承担某项责任的软件单元 | Context Manager、Tool Registry、Run Manager |
| 机制或策略 | 模块完成工作的方法 | compaction、重试、规划、幂等、渐进加载 |
| 运行对象 | 系统需要标识和管理的实体 | Task、Run、Thread、Turn、Item、Operation |
| 协议或接口 | 不同单元如何交互 | 工具契约、MCP、模型适配接口 |
| 资源或环境 | 能力、事实与执行的承载者 | 模型服务、数据库、文件系统、沙箱 |
| 横切要求 | 多层共同满足的性质 | 安全、可靠性、可观测性、成本 |

Model 是能力来源；Harness / Runtime 是以 L2 为核心的执行软件，实现中可以包含 L3 适配代码；Agent Application 才是四层及治理的组合。框架和 SDK 是实现这些职责的工具，不是第五层。

仓库真人面经中的 Depth L1–L4 表示追问深度，与这里的架构 L1–L4 不是同一套分类。''')
group(1, '从契约推导能力，而不是由组件反推需求', '''把能力写成动词：理解输入、澄清目标、获取证据、选择下一步、执行动作、验证结果、管理长任务、必要时协作。每项能力都应有存在理由和验证方法。

查外部资料才需要信息获取方案；跨调用继续推进才需要执行循环；跨任务复用信息才考虑长期记忆；执行不可信代码才考虑相应隔离环境；确有可拆分子任务才考虑多 Agent。向量数据库、独立 Planner、长期记忆和代码沙箱都不是 Agent 身份的必选配置。

本章形成的产物是一份任务契约和四层职责草图。下一章要确定：哪些选择权可以交给模型，哪些控制必须留在程序里。''')

group(2, '先选择控制方式，再选择框架', '''使用 LLM 不自动意味着采用自主 Agent。固定流程里的一个分类、摘要或抽取节点，仍可以由程序决定全部后续路径。Agentic 区域允许模型根据新观察动态选择下一步。

```text
确定性程序 → 含模型节点的 Workflow → 有限动态路由 → 受控 Agent Loop
```

这是控制权配置的连续变化，不是从低级产品到高级产品的排名。简单、可验证的方案应成为比较基线。Anthropic 的 [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) 强调从简单可组合模式出发。''')
group(2, '为每项能力分配决策权、执行权与验收权', '''| 能力 | 模型可以做什么 | 程序必须控制什么 | 验证依据 |
|---|---|---|---|
| 理解与澄清 | 提取诉求、识别缺失信息 | 身份绑定、输入约束、澄清状态 | 任务契约是否明确 |
| 获取证据 | 选择查询和调查方向 | 数据权限、预算、结果来源 | 证据适用性与覆盖率 |
| 规划与行动选择 | 提出计划、选择工具、调整路线 | 可用动作集合、依赖、停止条件 | 进度与约束是否满足 |
| 外部写入 | 形成操作候选 | 真实授权、参数校验、确认、幂等 | 业务回执与最终状态 |
| 结果验证 | 解释证据、发现可能遗漏 | 验收规则、独立检查、失败状态 | 真实结果，而非自称完成 |
| 长任务与协作 | 建议拆分或继续方向 | 持久化、调度、取消、资源所有权 | 恢复和隔离测试 |

模型的“行动选择权”不等于最终授权权。后端不能从模型生成的 user_id、tenant_id 或“用户已同意”文字建立可信身份和批准记录。''')
group(2, '自主权不是一个全局开关', '''按动作和任务阶段规定授权范围，可以只建议、只读调查、生成待确认方案，或在已授权边界内自主执行。这里是教学设计选项，不是某个产品的固定权限枚举。

自主权决定要与可逆性、可观测性、错误代价及验证能力一起做。任务很长不必然需要更高权限；一个很短的外部写操作也可能需要强约束。

生产系统常把确定性流程包在 Agentic 区域外：入口校验与身份固定；中间允许探索；关键动作经过业务规则与必要确认；交付前验证结果。这不是“半成品 Agent”，而是明确的不确定性边界。''')
group(2, '从最小方案演进，避免提前堆模块', '''先建立单模型、少量受控工具和明确停止条件的基线，再用失败案例决定是否增加能力。

信息找不到，先检查检索与工具接口，不直接增加 Agent 数量。上下文太大，先检查选择、去重、外部化与压缩，不自动加入长期记忆。操作重复，先检查状态和副作用协议，不靠更长 Prompt。任务确有独立子目标且接口明确，才比较多 Agent 的收益和额外成本。

能力设计的产物应包含选择理由、未采用的替代方案、触发升级的证据。模型、框架与数据库选型在职责清楚后再落定。''')

group(3, '应用层先把输入组织成任务', '''本层面向用户和业务工作，不要求具体行业案例。入口可以是对话、API、文件上传、定时触发或外部事件；入口形式不能取代任务模型。

```text
接收输入 → 认证与范围校验 → 澄清/归类 → 建立任务契约
→ 选择确定性流程或 Agent 执行 → 展示状态 → 验收与交付
```

Task 记录目标、范围、请求者、验收条件和业务状态。Agent Definition 是可版本化的执行配置；Agent Instance 是执行中的实例。两者都不等于用户交给系统的任务。一个配置可以服务多个任务，一个任务也可以调用多个实例。

幂等的任务创建接口需要区分“重复收到同一个请求”和“用户确实要重新运行”；不能仅凭文本相同就去重。''')
group(3, '业务流程与运行循环分别编排什么', '''应用流程关心必须经过的任务阶段，运行循环关心为了推进当前阶段下一步获取什么信息、调用什么能力。一个应用流程可以在多个阶段调用同一个运行时。

Task / Run 的对照是业务与执行之间的契约，不必绑定为一种固定树。应用通过 start、status、events、steer、cancel、approval 等逻辑接口与运行层协作；具体 API 名称由产品定义。

Task 完成必须有验收证据。Run 停止可能是成功、失败、取消、预算耗尽或等待人工，不应统一显示为“任务已完成”。''')
group(3, '入口路由：决定请求交给谁', '意图路由负责选择任务类型、应用流程或执行角色。它与 L3 的供应商适配、工具分发不是同一个问题。', take(17,[2,3]))
group(3, '交互是执行协议的一部分', '''用户需要看到进度、阻塞原因、可操作的确认请求和真实的最终结果，而不只是模型生成的文本流。

| 用户动作 | 应用层责任 | 运行层责任 |
|---|---|---|
| 澄清与追加约束 | 关联原任务，记录新的契约版本 | 在安全边界让新指令生效 |
| 确认操作 | 展示具体对象、参数、范围和后果 | 暂停、保存批准记录并在执行时重校验 |
| 取消 | 告知请求已接收及可能尚未停止的动作 | 传播取消、核对结果、释放资源 |
| 断线重连 | 恢复事件位置，补取权威状态 | 保留必要事件与持久执行状态 |
| 转人工 | 提供上下文、证据、待办和未决风险 | 暂停或移交控制权，避免双方同时写入 |

界面断开不等于任务必须取消；取消请求收到也不等于外部动作已回滚。需要为这些语义制定清楚的产品行为。

流式 token 是体验信息，动作回执和审批结果是执行事实。两者可以一起展示，但不要用一个临时 WebSocket 连接承载唯一任务状态。''')
group(3, '交付、权限与本层的完成标准', '''结果可以包含文本、结构化数据、文件、差异、证据引用、外部操作回执及未完成事项。交付必须说明哪些已验证、哪些仍未知，不能把“已发送请求”解释为“目标状态已经实现”。

L1 提供认证、确认与接管入口，L2 维护它们的执行语义，L3 传递可信身份并校验调用，L4 执行真实授权和资源隔离。安全贯穿各层，不归某一个对话按钮独占。

本层应验证重复输入、缺失信息、断线重连、取消、审批过期和转人工等交互路径。完成本章后，你应能画出用户任务的阶段，再把其中需要动态决策的一段交给下一章的运行循环。''')

group(4, '先把执行对象说清楚', '''本课程采用工作定义：Task 是目标与验收对象；Run 是一次受管理执行；Step 是运行时定义的推进单位；Model Invocation 是一次模型请求；Tool Call 是一次调用请求；Operation 是需要识别和核对的外部逻辑动作。

Codex App Server 的 Thread 是持续会话容器，Turn 是一次用户请求及后续 Agent 工作，Item 是有类型的输入输出单元。一次 Turn 可以含多次推理与工具交互；一个 Item 可以产生 started、delta、completed 等多个生命周期事件，但不同 Item 支持的事件并不完全相同。

```text
交互视图：Thread → Turn → Item → Event
业务/执行视图：Task → Run → Step / Operation
```

不要强制把两棵树拼成 `Session → Run → Turn` 的行业统一层级。关联方式由应用协议明确。Thread 也不是操作系统线程。

依据：[Codex App Server](https://developers.openai.com/codex/app-server)。''')
group(4, '循环推进：模型提出候选，运行时决定怎样兑现', '''```text
载入目标与执行状态 → 组装上下文 → 调用模型
→ 解析候选动作 → 校验范围、预算与权限
→ 执行工具 / 等待人工 / 提交完成候选
→ 记录结果与状态 → 核验进度 → 继续、暂停或终止
```

下面是控制骨架，不是可直接部署的完整代码：

```python
async def advance(run, runtime):
    while runtime.can_continue(run):
        runtime.apply_pending_instructions(run)
        context = await runtime.build_context(run)
        decision = await runtime.decide(context)
        if decision.kind == 'final':
            evidence = await runtime.verify_candidate(run, decision)
            if evidence.accepted:
                return await runtime.complete(run, evidence)
            await runtime.record_verification_failure(run, evidence)
        elif decision.kind == 'tool':
            outcome = await runtime.execute_controlled(run, decision)
            await runtime.record_and_checkpoint(run, outcome)
        elif decision.kind == 'ask':
            return await runtime.pause_for_input(run, decision)
        else:
            await runtime.record_invalid_decision(run, decision)
    return await runtime.stop_with_reason(run)
```

这里的 execute_controlled 包含调用校验与必要授权；record_and_checkpoint 也不意味着与外部副作用存在一个跨系统原子事务。完成、错误、暂停、取消必须具有不同语义。''')
group(4, '用计划管理进度，而不是把计划当成功证明', 'Planning、ReAct、Plan–Execute–Replan 和 Critic 是运行层可以采用的策略，不必各自变成独立服务。模型可以隐式规划，也可以维护显式计划。', take(8,[1,2,3,4]))
group(4, '停止、预算、重复与方向修正', '运行层必须同时回答“还能不能做”和“有没有必要继续做”。达到限制是有原因的停止，不代表任务成功。', take(8,[5,6,7,8,9,10]))
group(4, '事件把循环变成可解释的执行', '模型消息是模型输入输出的表示；运行事件记录真实发生的调度、调用、批准、检查点与停止。记录可观察输入、动作、证据及结果，不要求暴露模型隐藏思维过程。', take(3,[5,6,7]))

group(5, 'Context Manager 管的是当前模型可见信息', '''运行层现在需要决定每一步给模型看什么。上下文只是当前模型输入，不是全部历史、全部执行状态或全部业务事实。Prompt 是其中的指令部分；RAG 与 Memory 可以提供材料；Context Manager 选择与组织这些材料。

可以把输入表示为带 source、version、scope、trust、priority 和 token estimate 的片段。权限过滤和可信指令边界先于相关性排序，不能因为一段外部文本“很相关”就把它升级成系统指令。''')
group(5, '从来源到可调用的上下文', '先选择与规范化，再排序、去重、分配预算，最后编码为模型接口支持的消息。', take(9,[2,3,4,5,11]))
group(5, '先处理增长，再考虑压缩', '大量工具输出应保留可重新读取的产物引用。截断、外部化和缓存解决不同问题，不能互相冒充。', take(9,[7,8,9]))
group(5, 'Compaction 是上下文管理机制', '压缩的目标是支持后续执行，而不是写一篇漂亮摘要。关键状态必须能从持久记录恢复；不能只有摘要里保留唯一业务回执。', take(10,[1,2,5,6,7,8]))
group(5, '验证继续执行是否仍然正确', '检查压缩后的结构、语义和后续行为。缓存命中或 token 下降不等于上下文质量提升。', take(10,[9,10,11,12,13]), take(9,[12]))

group(6, '记忆策略属于运行层，记忆数据库不属于运行层', '''这一章回答哪些信息值得未来再次使用。L2 决定何时写、何时读、如何更新和失效；L3 提供受控存取接口；L4 保存记录及索引。这是一项跨层能力的职责分解，不是三个互相重复的 Memory 模块。''', take(11,[1,2,3]))
group(6, '选择、提取、写入与按需召回', '把长期记忆作为有来源、作用域和生命周期的信息资产，不把所有聊天自动永久存入向量库。', take(11,[4,5,6,7]))
group(6, '纠错、冲突与失效是核心机制', '记忆是一份可被纠正的历史表示，不是现实世界的最终权威。', take(11,[8,9,10,14]))
group(6, '记忆的安全与验收', '保存和使用信息都要满足用户、租户与项目边界；召回后仍需依据任务风险验证其适用性。', take(11,[11,16]))

group(7, '哪些状态必须独立于上下文存在', '''运行层既要让模型“知道发生了什么”，更要让程序准确知道“做到哪里、谁在执行、哪些动作可能已经发生”。本章的 Run / 状态名是教学工作定义，Codex 的交互对象仍采用第04章的 Thread / Turn / Item 语义。

| 对象 | 保存的事实 | 不替代什么 |
|---|---|---|
| Context | 当前模型可见信息 | 不是唯一恢复依据 |
| Runtime State | 进度、待办、操作、审批、预算、版本 | 不是全部外部业务状态 |
| History / Event Log | 已发生的消息和执行事件 | 不自动等于可重放的外部动作 |
| Checkpoint | 恢复边界及关联状态/资源引用 | 不自动回滚外部世界 |
| Memory | 为未来复用而维护的信息 | 不替代操作回执和状态机 |
| Source of Truth | 外部系统的权威状态 | 不由 Agent 的总结决定 |
''', take(12,[3,4,5,6]))
group(7, '状态所有权、并发和租户边界', '读写状态必须绑定身份与版本。同一个会话可以选择排队、拒绝并发或隔离分支，但不能让两个写入者无协调覆盖状态。', take(12,[8,9,10,11]))
group(7, '检查点与恢复边界', '保存什么取决于怎样恢复；仅保存最后一句回复不足以安全接管任务。', take(13,[1,2,14]), take(12,[12]))
group(7, '先核对副作用，再继续推理', '动作提交与本地保存之间可能出现不确定窗口。恢复必须先核对、去重或保留未决状态，而不是先重新调用模型让它猜。', take(13,[4,5,6,7,8]))
group(7, '暂停、取消、分叉、重放和接管', '这些都是不同的生命周期操作。一个可继续的执行系统必须明确它们对已发生动作的影响。', take(13,[3,9,10,11,12,13]), take(12,[13]))

group(8, '多 Agent 是运行拓扑，不是新的架构层', '先有单 Agent 的目标、状态、工具与恢复语义，再判断是否值得分工。增加执行角色不能修复一个不清晰的任务契约。', take(18,[1,2,3,4,5]))
group(8, '隔离上下文并协调共享资源', '子任务可以并行，但共享写入不能默认安全。权限、预算、上下文与资源所有权要随委派明确。', take(18,[6,8,9,10]))
group(8, '调度、取消、预算与死锁', '委派关系必须有界。父任务结束、子任务超时或部分失败时，运行时应有可解释的汇聚与清理行为。', take(18,[11,12,13,16]))
group(8, '跨系统协作与内部子 Agent 不同', 'A2A 讨论跨 Agent 系统的发现、任务和消息交互；协议连接不会自动提供正确分工、可信结果或业务一致性。', take(18,[14,15]))

group(9, '先区分选择策略和供应商适配', '''L2 或平台策略决定选择什么模型，L3 把统一请求转换为具体供应商协议，L4 提供实际模型服务。本章放在 L3，是为了讲清调用边界，不是把全部路由决策从运行层搬走。

能力适配必须保留差异：模型可能不支持某种工具协议、多模态输入、上下文长度或结构化输出约束。不能把不支持伪装成支持。''', take(17,[4,5,6]))
group(9, '按错误语义恢复，而不是统一重试', '模型失败、工具失败和状态保存失败具有不同后果。恢复策略与运行预算、动作幂等和当前生命周期状态共同决定。', take(17,[8,9,10,11,12,13]))
group(9, '路由与模型变更也需要验收', '''路由可以按任务能力、上下文、隐私边界、成本和可用性筛选，但必须记录实际选中的模型、协议版本和降级原因。比较路由方案要用同一任务集和同一成功标准。

失败时可以暂停、排队、降级或更换模型；每种选择都要说明其语义影响。切换模型不应重放已执行工具；未完整结束的流式工具参数不能被当作可执行请求。

模型选择与训练、Transformer、推理服务内部机制仍回到 [LLM Foundation](../../llm-foundation/README.md)。本模块负责它们在 Agent 调用链上的契约。''')

group(10, '工具是模型与执行系统之间的正式契约', '工具描述帮助模型选择，运行接口负责真实调用，底层服务负责实际动作。三者必须分开；可见工具的安全元数据也不能由模型自述决定。', take(4,[1,2,3,4,5,6,7,8,9]))
group(10, '注册目录与本轮可见集合', '注册能力不代表每轮都把全部 Schema 给模型。先按权限和环境筛选，再考虑任务相关性与发现策略。隐藏一个工具也不能替代执行时的权限检查。', take(5,[1,2,3,4,5]))
group(10, '发现、加载与版本生命周期', '正确工具未被召回时，后续模型再强也难以完成任务；发现模块必须单独评测，并为不可用和版本变化提供明确语义。', take(5,[6,7,8,9,12]), take(4,[12]))

group(11, '从调用请求到可接受结果', '''L2 发出或批准调用、管理执行状态；L3 将调用转换为受控 Invocation 并连接执行后端；L4 产生真实结果。工具执行是跨层的一条链路，本章从接入边界展开。

它不是天然的分布式事务。即使所有步骤在一个 Executor 中实现，外部副作用与本地检查点仍可能不是原子的。''', take(6,[1,2,3,4,10]))
group(11, '错误分类与有限恢复', 'Repair 修改错误参数，Retry 重试有资格重试的请求，Fallback 更换能力，Fail 终止无法安全推进的动作。', take(6,[5,6,7,8,9,11]))
group(11, '并发必须围绕资源与副作用', '工具名称不同不代表资源不冲突，只读也不保证无额度消耗。调度依据应来自可信契约及当前资源范围。', take(7,[1,2,3,4]))
group(11, '取消、进度和最终结果', '取消是一套传播、确认、资源释放与结果核对协议，不是把状态字段改成 cancelled。进度信息不能代替最终回执。', take(7,[5,6,7,8,9,12]))

group(12, '把信息需求连接到可信来源', '''L2 决定何时检索、怎样形成查询以及如何使用结果；L3 负责连接检索、数据读取与记忆存取服务；L4 保存文档、索引、记忆记录及业务事实。

一个检索结果应尽量包含内容、来源标识、版本或时间、作用域、定位信息与访问权限。分数不等于真实性，也不能跨数据源直接当统一置信度。检索时的权限过滤与使用时的适用性核对都不可少。

```text
信息缺口 → 受控查询 → 权限过滤 → 候选证据 → 排序/核验
→ 证据引用 → L2 上下文组装 → 后续决策
```

RAG 是获取和使用证据的方案，不是第五层。Agent 可以通过普通接口、全文搜索、结构化查询、文件读取或向量检索获取信息，不应默认所有问题都要向量化。

State Store 接口关注恢复、版本与一致性；Memory Store 接口关注作用域、来源、更新与删除；Artifact Store 接口关注大对象与可验证引用。可以使用同一种数据库，但不能混用语义和生命周期。''')
group(12, '工具、协议、技能与钩子各负责什么', '这些概念跨越不同类型。协议接入主要在 L3；技能内容可以存于 L4；何时加载技能、何时运行钩子主要由 L2 控制。', take(16,[1,5,6,7,8,9,10]))
group(12, '能力扩展的失败、版本和安全', '接入协议提供互操作能力，不自动赋予权限，不替代数据可信度检查，也不保证所有扩展兼容当前运行环境。', take(16,[12,13,14]))
group(12, '用代码资源检索检查接口是否足够表达需求', 'Codex 这类编码 Agent 提供一个实现观察窗口：结构化符号、路径、文本、语义与依赖信息应按需求组合。这是信息接入方法的对照，不另开一个项目学习支线。', take(21,[2,3]))

group(13, '资源层保存事实并提供真实能力', '''模型服务提供推理与生成；业务系统产生真实状态变化；知识源和索引提供信息；持久化存储保存状态、事件、记忆与产物；执行环境承载文件、进程、浏览器或代码。

| 资源 | 主要承载内容 | 需要明确的边界 |
|---|---|---|
| 模型/Embedding/Reranker 服务 | 计算能力 | 能力、额度、版本、时延与数据边界 |
| 业务系统与 API | 权威记录、真实操作 | 身份、授权、事务、回执与幂等 |
| 文档、搜索与向量索引 | 原始资料和派生检索结构 | 来源、更新、ACL 和版本 |
| 状态与事件存储 | 恢复事实和执行记录 | 持久性、一致性、版本与保留期限 |
| 记忆与产物存储 | 可复用信息、大对象及引用 | 生命周期、完整性与租户范围 |
| 文件/进程/浏览器/沙箱 | 真实执行环境 | 资源额度、隔离、凭证与清理 |

把模型服务放在 L4 表达依赖关系，不代表模型在产品中不重要。把数据库放在 L4 也不意味着忽略数据模型；数据的语义由拥有相应责任的上层定义。

数据库和模型的内部原理分别回到 [MySQL](../../mysql/README.md)、[Redis](../../redis/README.md)、[Vector DB](../../vector-db/README.md) 和 [LLM Foundation](../../llm-foundation/README.md)。''')
group(13, '存储选择服从状态语义', '不要按组件名分配数据。先决定哪些记录是权威、哪些是派生、哪些允许丢失，再检查所选部署的持久化和一致性保证。', take(12,[7]))
group(13, '执行环境与隔离', '仅通过受控 API 行动的 Agent 不必具备任意代码执行能力。需要执行代码、命令或浏览器操作时，再设计与风险相称的隔离环境。普通进程或容器的存在本身不是完整安全保证。', take(14,[7,8,9,10]), take(22,[7]))
group(13, '环境生命周期、工作区与产物', '任务状态、工作区和运行进程不必同生共死。持久状态记录环境与产物引用，重建环境时验证版本、权限及未完成操作，而不是假设重新挂载就等于完全恢复。', take(21,[5,6,12,14]))

group(14, '安全是每层的责任，不是最后插入的过滤器', '''本章集中讲安全，实施却要从第01章的任务契约开始贯穿整个调用链。

```text
L1 认证、告知与确认入口
→ L2 权限快照、审批状态、动作约束与审计事件
→ L3 可信身份传递、凭证代理、参数与能力校验
→ L4 服务端授权、资源隔离与真实策略执行
```

模型可以被外部材料误导，所以安全设计不能只依赖它始终正确理解 Prompt。审批、规则与沙箱是不同防线；前置批准也不能替代执行时的权限与资源版本核对。''', take(14,[1,2,3,4,5,6]))
group(14, '先明确威胁与信任边界', '对每个入口说明攻击者能控制哪些文本、文件、工具结果或资源，再决定要保护哪些动作和数据。', take(15,[1,2,3,4]))
group(14, '约束秘密、能力与外传路径', '最小授权必须由可信系统执行。外部工具返回成功不代表内容可作为新指令，沙箱也不会自动保护一个远端业务 API。', take(15,[5,6,7,8,9,10,11]))
group(14, '用失败链检验安全设计', '检查一次恶意输入能够跨越哪些边界，而不是只统计是否命中了敏感词。', take(14,[11,12]), take(15,[12]))

group(15, '观测回答发生了什么，评测回答做得怎样', '两者是贯穿四层的质量闭环。执行轨迹应能关联任务、运行、模型、工具、上下文版本和外部动作，同时限制敏感数据记录。', take(19,[1,2,3,6,7]))
group(15, '可解释地回放、诊断与定位', '证据回放、模型重跑和副作用重放必须分开。默认回放不能重新执行生产写操作。', take(19,[8,9,10,11,12,13]))
group(15, '从任务契约推导验证对象', '结果、过程、组件、资源与安全是验证视角，不是重新划分四层架构。不能只看最后一句话是否自然。', take(20,[1,2,3,4,5,6,7,8,9]))
group(15, '评测推动修改，而不是只生成分数', '先用轨迹定位失败责任，再形成可复现样例、比较候选改动、做回归与上线检查。', take(20,[10,11,12,13,14,15,16]))

group(16, '把逻辑职责落成部署与故障边界', '''完成前15章后，才需要讨论一个进程还是多个服务。以下部署组件是前面职责的实现，不是需要另背的一套架构层：应用入口承载 L1，Harness Worker 承载 L2，模型/工具/数据适配承载 L3，各类服务、存储和执行环境承载 L4。

同一进程可以同时实现这些责任；长任务、隔离、扩容与故障需求出现后再拆开。接口、状态所有权和验收条件仍沿用同一张图。''', take(22,[1,2,3,5,6]))
group(16, '规模、成本、可靠性与升级', '把端到端成本和失败预算归到任务，而不只看 HTTP 时延或单次模型 token。', take(22,[11,12,13,14,15,16,17,18,19]))
group(16, '框架选型是职责匹配，不是架构起点', '用自己的任务契约、执行语义、故障测试和退出路径比较实现方案。产品 API 与默认行为随版本变化，下面的映射用于比较职责，不是永恒的功能承诺。', take(23,[1,2,3,4,5,6,7,8,9,10,11,12,14,17]))
group(16, '以 Codex 类工作过程检验交付闭环', '这里使用代码产物的验证方式作为成熟 Agent 的实现对照：理解资源、执行修改、独立验证、审阅差异、准确交付。不是新增一个行业项目，也不把测试通过等同于所有业务问题已被证明。', take(21,[1,4,7,8,9,10,11,13,16]))
group(16, '最终设计与讲解顺序', '''```text
任务契约 → 能力与自主权 → L1 应用流程 → L2 执行与状态
→ L3 接口契约 → L4 资源与环境 → 安全与质量 → 部署、成本与演进
```

讲一个机制时，先说明它位于哪项责任之下、补上什么缺口，再解释工作方式、失败边界和验证方法。讲一个项目时，先讲目标、环境与成功标准，再沿四层展开自己的实现和取舍。

一个可复用的面试开场：

> 我先明确目标、范围、环境、权限和验收，判断哪些步骤由程序控制、哪些交给模型动态判断。然后按应用、运行、接入、资源四层设计，说明任务怎样被承接，执行如何循环并恢复，信息和动作通过什么契约连接，真实状态保存在哪里。最后检查权限、副作用、故障、成本和评测，依据实际需求决定是否增加长期记忆、多 Agent 或独立执行环境。

最终验收不是能背出所有术语，而是面对新任务能推导必要能力、解释职责和状态流动，并说明如何证明系统有效且可控。''')

INTRO = {
1:('先看整个 Agent 系统，而不是先进入 Harness 内部。','任务契约与职责图'),
2:('目标与边界已有了，接着决定哪些控制权值得交给模型。','能力、控制权与最小方案的决策表'),
3:('自主权确定后，先设计用户如何把工作交给系统并拿到结果。','任务流程与交互契约'),
4:('应用已承接任务，现在展开负责推进它的运行层。','一次执行的闭环、对象与停止语义'),
5:('循环需要每步输入；先解决当前该给模型看什么。','上下文编译、预算与压缩的正常/失败路径'),
6:('当前上下文清楚后，再决定哪些信息值得跨步骤、跨任务复用。','记忆读写、来源、更新与失效策略'),
7:('信息可被使用还不够，任务中断后也要知道准确的执行事实。','可恢复的状态机与副作用核对协议'),
8:('先有一个可控执行单元，再讨论如何把工作分给多个执行单元。','委派、汇聚、共享资源与取消协议'),
9:('运行层的需求已经明确，开始设计它与外部能力的稳定接口。','模型能力矩阵、适配边界与恢复策略'),
10:('模型接入后，需要让它发现并正确描述可调用的外部动作。','工具契约、目录、可见集合与版本策略'),
11:('工具已被找到并形成请求，继续定义怎样可靠兑现这次调用。','调用生命周期、错误、并发、副作用与取消语义'),
12:('通用工具边界明确后，再接入知识、记忆与可扩展能力。','检索/存取契约与 MCP、Skill、Hook 的责任边界'),
13:('接口背后必须有真实资源，现在明确谁提供能力、保存事实与执行动作。','资源所有权、环境生命周期与隔离方式'),
14:('四层已展开，集中检验身份、权限与信任怎样贯穿每一条路径。','威胁模型与分层实施的安全控制链'),
15:('行动被约束后，还要知道系统做了什么、结果是否有效以及怎样改善。','可观测执行与评测驱动的改进闭环'),
16:('最后把同一套职责组合成可部署、可运营、可演进的系统。','完整设计、选型理由与验证方案'),
}
QUIZ = {
1:[('业务场景为什么不与 Memory 并列成模块？','场景是设计输入，决定目标、环境和验收；Memory 是根据复用需求选择的一项能力，类型不同。'),('四层是否意味着四个微服务？','不是。逻辑职责可以同进程实现，部署边界由隔离、规模、故障与运维需求决定。')],
2:[('模型判断某动作安全，能直接执行吗？','不能。模型建议不建立身份、授权或业务合法性；可信程序与后端须实施相应控制。'),('什么时候增加长期记忆或多 Agent？','当任务契约与失败证据显示跨任务信息复用或可分工协作确有价值，并能验证收益及额外风险时。')],
3:[('用户断线后任务应不应该取消？','由产品语义决定。连接生命周期与任务生命周期不同，必须明确定义继续、暂停、取消和重连补取状态的行为。'),('Run 结束是否足以显示任务完成？','不足。要区分成功、失败、取消、暂停等，并按任务验收条件核验结果。')],
4:[('Turn、模型调用、Item 是同一件事吗？','不是。Codex 的 Turn 包含一次请求及后续工作，可能包含多次推理和工具交互；Item 是有类型的输入输出单元。'),('final 文本能否直接触发成功状态？','应先按契约验证完成证据；结束回复、达到预算和完成任务是不同语义。')],
5:[('Compaction 为什么不能替代持久化？','它管理当前模型可见信息，可能有损；审批、回执、进度等恢复事实需要独立保存。'),('怎样验证压缩有效？','同时检查结构不变量、关键语义、后续执行表现、错误恢复和回归指标，而不只看节约 token。')],
6:[('Memory 为什么不是把 History 全部存起来？','Memory 是为未来复用选择并维护的信息，具有来源、作用域、版本和失效策略；History 是发生过的记录。'),('模型召回的记忆与真实系统冲突怎么办？','核对来源、版本和适用范围，必要时重新查询权威系统、保留未决状态并纠正过期记忆。')],
7:[('工具成功但检查点写入失败，恢复时先做什么？','核对已记录操作标识、幂等键和外部状态；确认已发生的副作用后再继续，不能盲重放写操作。'),('Fork 是否复制外部世界？','不会。分叉的是执行/交互状态及允许复制的引用；真实外部动作不能因分叉被假设撤销或重做。')],
8:[('子 Agent 分开上下文后，共享文件写入就安全了吗？','没有。信息隔离与资源并发是两件事，需要写入所有权、隔离工作区、锁或版本化合并。'),('A2A 是否自动解决多 Agent 分工？','不解决。互操作协议不代替目标分解、权限、预算、调度、汇聚和最终验收。')],
9:[('Adapter 是否应抹平所有供应商差异？','不应。必须保留能力差异和不支持情况，避免把不兼容的工具、多模态或状态协议静默伪装为支持。'),('模型切换后可以把整个任务再跑一遍吗？','不能默认这样做。必须保留已执行动作与状态，重新验证协议兼容和恢复语义。')],
10:[('Schema 合法为什么不等于操作合法？','Schema 主要检验形状，还需语义、身份、租户、权限、风险和业务约束检查。'),('Registry 与可见工具集合是什么关系？','Registry 是完整目录；可见集合是经过策略、环境和任务筛选后提供给当前模型的视图。')],
11:[('超时是否说明动作没有发生？','不说明。调用方可能只是未收到响应，必须根据执行阶段与外部结果判断重试资格。'),('取消请求得到确认是否说明副作用已回滚？','不是。取消传播、真正终止与外部结果核对是独立步骤，已完成动作可能需要补偿且不一定可逆。')],
12:[('RAG、MCP、Skill、Hook 是同一种抽象吗？','不是。RAG 是证据获取与使用方案，MCP 是协议，Skill 是程序性知识/资源包，Hook 是生命周期扩展机制。'),('为什么记忆策略与 Memory Store 接口分章？','前者决定保存和使用什么，后者兑现受控读写；分清职责能独立更换存储而保持运行语义。')],
13:[('只有受控 API 工具的 Agent 必须配代码沙箱吗？','不必须。没有任意代码执行需求时，不应为凑组件增加执行环境；API 仍需自身授权与隔离。'),('模型和数据库在 L4 是否意味着它们是次要的？','不意味着。分层表达能力与事实的提供关系，不对重要性排序。')],
14:[('所有工具都弹确认框是否足够安全？','不够。还要有真实身份、最小权限、审批绑定、执行时校验、环境隔离、凭证和外传控制。'),('外部文档能否修改系统权限？','不能。外部内容是待评估的数据，不能成为新的可信授权或覆盖上层策略。')],
15:[('Trace 和 Eval 各回答什么？','Trace 记录过程及关联事实；Eval 依据任务和约束判断结果、过程、组件与安全资源指标。'),('一个 bad case 应怎样变成改进？','用轨迹定位责任与原因，构建可复现用例，修改对应机制，做回归与受控上线，并保留回滚方案。')],
16:[('选框架前要有哪几项东西？','任务契约、控制权、四层职责、状态和副作用语义、失败测试及成本约束。'),('什么时候把 Harness 和执行环境拆开部署？','当隔离、长任务恢复、资源类型、独立扩容或故障边界提出需要时，而不是为了模仿某个产品目录。')],
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip()+'\n', encoding='utf-8')


def nav(n: int) -> str:
    prev = f'[← {n-1:02d}](%s)' % NAMES[n-1] if n>1 else '[← Agent 目录](../README.md)'
    nxt = f'[{n+1:02d} →](%s)' % NAMES[n+1] if n<16 else '[复习与自测 →](../review/README.md)'
    return prev + ' · [Agent 主线](../README.md) · ' + nxt

for n, (_, title, layer) in enumerate(CHAPTERS,1):
    intro, outcome = INTRO[n]
    text = f'# {n:02d}. {title}\n\n{nav(n)}\n\n> 主线位置：**{layer}**。{intro}\n>\n> 本章产物：**{outcome}**。\n\n'
    text += ' → '.join(f'[{t}](#part-{i})' for i,(t,_) in enumerate(GROUPS[n],1))+'\n\n'
    for i,(t,b) in enumerate(GROUPS[n],1):
        text += f'<a id="part-{i}"></a>\n\n## {i}. {t}\n\n{b}\n\n'
    text += '## 本章自测\n\n'
    for q,a in QUIZ[n]:
        text += f'<details>\n<summary>{q}</summary>\n\n{a}\n\n</details>\n\n'
    ids = [f'AGENT-{i:03d}' for i,c in QUESTION_OWNER.items() if c==n]
    text += '## 回到主线\n\n'
    text += f'现在应能独立说明：{outcome}。'
    text += (f'下一章：[{CHAPTERS[n][1]}]({NAMES[n+1]})。' if n<16 else '接下来闭卷重建总图，再进入面试训练。')+'\n\n'
    if ids:
        text += '对应真人问题：'+ '、'.join(f'`{i}`' for i in ids)+'。频率与完整问法只在[研究题库](../../research/questions/agent-harness.md)维护，不决定本章学习顺序。\n\n'
    text += '资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。\n\n'+nav(n)
    write(NEW/'docs'/NAMES[n], text)

# A single module homepage and learning sequence.
readme = '''# Agent｜从任务契约到生产级 Agent 系统

[← RAG](../rag/README.md) · [↑ Handbook](../README.md) · [学习路线](../roadmap/learning-path.md) · [System Design →](../system-design/README.md)

> **状态：分层重构版** · **16 章连续主线** · **44 道 ACTIVE Canonical**
>
> 本模块已由 `agent-harness/` 重构为 `agent/`。这不是增加一套导读：原23章按职责合并、重编，独立 architecture 笔记组已吸收并移除。Harness 仍作为运行层概念学习，不再代指整个 Agent 模块。

## 1. 这个模块解决什么

'''+DESC+'''

学习完成后，应该能从任务推导必要能力，解释每项机制的位置、输入输出、失败和验证，并把它们组合成可交付系统，而不是只会解释单个名词。

## 2. 在十板块中的位置

Python → FastAPI → AI Backend Engineering → MySQL / Redis / Vector DB → LLM Foundation → RAG → **Agent** → System Design。

本模块提供 Agent 专属的系统认知与执行机制。通用网络、数据库、事务、队列和容量算法回到对应基础模块；System Design 继续负责跨领域组合与完整场景训练。

## 3. 固定课程原则

**先目标，后职责；先整体，后机制；先单个执行单元，后协作；先逻辑边界，后部署选型。** 真人面经只调整复习权重，不打乱第一次学习顺序。

业务场景是设计输入，不是软件模块；四层是逻辑职责，不是四个微服务；层、模块、机制、对象、协议和资源是不同类型。这里的架构 L1–L4 与研究题库的 Depth L1–L4 无关。

## 4. 唯一正式学习主线

```text
'''+MAP+'''
```

第一遍只按下面01→16阅读，不需要先读另一个总纲、术语百科或项目案例。每章都包含承接关系、核心机制、失败/取舍、自测与下一章链接。

## 5. 正式课程目录

'''
for start,end,title in [(1,2,'起点｜任务与控制权'),(3,3,'L1｜应用如何承接和交付任务'),(4,8,'L2｜运行时怎样持续推进任务'),(9,12,'L3｜外部能力怎样被稳定接入'),(13,13,'L4｜真实能力、事实与行动在哪里'),(14,15,'横切治理｜安全与质量贯穿四层'),(16,16,'系统收口｜从逻辑架构到工程实现')]:
    readme += '### '+title+'\n\n'
    for n in range(start,end+1):
        readme += f'{n}. [{CHAPTERS[n-1][1]}](docs/{NAMES[n]})\n'
    readme += '\n'
readme += '''## 6. 真人面经怎样影响本模块

44 道 ACTIVE Canonical 和原有 Source Count 不因改名、合并章节或增加架构解释而变化。研究文件 `research/questions/agent-harness.md` 保留兼容标识，展示模块名统一为 Agent。

[真实问法与来源](../research/questions/agent-harness.md)只用来决定复习深度；本模块的完整设计责任不由面试频率决定。

## 7. 模块边界

RAG 负责证据获取与回答质量的完整工程链；这里讲何时需要信息、如何接入、如何进入执行。LLM Foundation 负责模型内部原理；这里讲模型在系统中的角色和调用契约。Backend Engineering 负责通用可靠性机制；这里讲 Run、Tool、Checkpoint 和副作用特有的执行语义。

<a id="concept-map"></a>

<details>
<summary>查找某个概念：按主责回到正式章节（不是第二条学习路线）</summary>

| 要查的内容 | 主责 / 章节 |
|---|---|
| Agent、Harness、层/模块/机制、任务契约 | 01–02 |
| 任务入口、业务编排、用户确认、人工接管、意图路由 | 03 |
| Thread / Turn / Item、Loop、Planning、ReAct、Stop、Budget、Steering | 04 |
| Prompt / Context、Compaction、Cache、Offloading | 05 |
| Memory、Write Policy、Consolidation、失效与纠错 | 06 |
| State、History、Checkpoint、Resume、Fork、Replay、幂等与动作核对 | 07 |
| Multi-Agent、Subagent、Handoff、A2A、共享工作区 | 08 |
| Model Routing、Provider Adapter、Failover | 09 |
| Tool Schema、Registry、Router、Discovery、版本 | 10 |
| Tool Execution、错误、副作用、并发、Cancel、Progress | 11 |
| RAG 接入、状态/记忆接口、MCP、Skills、Hooks、资源搜索 | 12 |
| 模型服务、数据库、文件、执行环境、Sandbox、Artifact | 13 |
| Auth、Permission、Approval、Guardrails、Injection、Secrets | 14 |
| Trace、Metrics、Replay、Evals、Benchmark、Data Flywheel | 15 |
| Deployment、Queue、Cost、Framework、Build-vs-Buy、代码验证 | 16 |

跨层能力按职责拆开，例如 Memory 的策略在06，存取接口在12，存储资源在13；不要把同一个词硬塞进唯一一层。

</details>

## 8. 复习、面试与资料入口

[复习与综合自测](review/README.md) · [面试训练](interview/README.md) · [官方资料](../roadmap/agent-authoritative-sources.md) · [源码索引](../research/agent-sources/README.md)。复习和面试页不再复制一份正式教材。

## 9. 推荐学习方式

第一次沿01→16建立因果链。每章结束，能说明当前责任、输入输出、至少一个失败窗口和验证方式，再进入下一章。第二遍用复习页闭卷重建同一张图，第三遍再用真实问题练习口述与追问。

## 10. 完成状态与下一环

正文16章连续；复习与面试各一个入口。旧23章迁移关系、课程计数和本次检查记录维护在既有[粒度记录](../roadmap/curriculum-granularity-audit.md)与[质量记录](../roadmap/final-quality-audit.md)，不另开学习文档。

下一环：[System Design](../system-design/README.md)。
'''
write(NEW/'README.md', readme)

review = '''# Agent 复习｜用同一条主线重建系统

[← Agent](../README.md) · [Handbook](../../README.md) · [面试训练](../interview/README.md)

这是第二遍复习，不是另一套教材。先闭卷回答，遇到缺口只回对应章节。

## 1. 从空白纸重建

```text
任务契约 → 能力与自主权 → L1 应用 → L2 运行 → L3 接入 → L4 资源
                       安全治理与质量运营贯穿全过程
```

画出一条输入到交付的执行路径，标出模型看见的信息、程序持有的状态、外部真实事实、每次写操作的授权与回执。再分别加入用户取消、模型失败、工具超时和进程重启。

## 2. 逐章闭卷检查

'''
for n in NAMES:
    review += f'### {n:02d}｜{CHAPTERS[n-1][1]}\n\n'
    q,a=QUIZ[n][0]
    review += f'<details>\n<summary>{q}</summary>\n\n{a}\n\n回到[第{n:02d}章](../docs/{NAMES[n]})。\n\n</details>\n\n'
review += '''## 3. 综合验收

能区分应用流程与 Agent Loop，能解释静态四层和动态状态如何对应；能把 Memory、RAG、Tool、Sandbox 等放回职责；能说明为什么某任务不需要某组件；能定位一次失败的责任边界，并提出验证而不是只换模型。

不要只检查能否复述术语。每个机制都应能回答：为什么存在、输入输出是什么、何时失效、如何测试。
'''
write(NEW/'review/README.md', review)

interview = '''# Agent 面试训练｜先回答系统，再展开机制

[← Agent](../README.md) · [综合复习](../review/README.md) · [真人问题与来源](../../research/questions/agent-harness.md)

这是第三遍训练入口。正式解释只维护在01–16章；完整真实问法、Depth、Source Count 只维护在研究题库。答案默认折叠。

## 1. 开放性设计题的开场

<details>
<summary>从零设计一个 Agent 系统，你会先考虑什么？</summary>

我先明确任务目标、范围、环境、权限与验收，判断哪些部分应由程序确定控制、哪些需要模型根据反馈动态决策。然后按应用、运行、接入、资源四层设计：应用承接与交付任务，运行层管理循环、上下文、状态和恢复，接入层提供模型、工具和数据接口，资源层提供真实能力和事实。安全与质量贯穿执行，并通过副作用核对、故障测试和结果评测验证设计。最后再选择框架、部署形态及是否需要多 Agent。

</details>

## 2. 按主线展开追问

'''
for n in NAMES:
    q,a=QUIZ[n][-1]
    interview += f'### {n:02d}｜{CHAPTERS[n-1][1]}\n\n<details>\n<summary>{q}</summary>\n\n{a}\n\n继续追问：输入输出是什么？哪个事实必须持久化？失败后谁负责？如何证明有效？\n\n完整机制：[第{n:02d}章](../docs/{NAMES[n]})。\n\n</details>\n\n'
interview += '''## 3. 不要这样回答

“用了模型就是 Agent”“Harness 等于整个产品”“Memory 就是所有状态”“Schema 合法就能执行”“超时表示没成功”“有沙箱就安全”“Checkpoint 保证外部动作只执行一次”“多个 Agent 一定更好”“模型说完成就是完成”。

纠正时说明具体责任和失败窗口，不用另一句口号替代。

## 4. 44 道真人问题回到哪里

下表只维护学习位置，不复制或重算研究证据。

| Canonical | 主责章节 |
|---|---|
'''
for q,n in sorted(QUESTION_OWNER.items()):
    interview += f'| `AGENT-{q:03d}` | [{n:02d} {CHAPTERS[n-1][1]}](../docs/{NAMES[n]}) |\n'
write(NEW/'interview/README.md', interview)

# Remove the old module only after every new chapter was constructed.
import shutil
shutil.rmtree(OLD)

# Rename learning paths, not frozen research filenames / question identifiers.
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or '.git' in p.parts or p == Path(__file__).resolve():
        continue
    if p.suffix not in {'.md','.py','.json','.csv','.yml','.yaml','.toml'}:
        continue
    rel = str(p.relative_to(ROOT))
    if rel.startswith(('research/interviews/','research/monitoring/','research/quality/')):
        continue
    text = p.read_text(encoding='utf-8')
    before = text
    # Keep the real Harness/Runtime term in technical mechanism prose. Rename module labels globally elsewhere.
    if not rel.startswith('agent/docs/'):
        text = text.replace('Agent Harness / Runtime', 'Agent')
    text = text.replace('agent-harness/', 'agent/')
    for oldn,newn in OLD_TO_NEW.items():
        text = text.replace(old_files[oldn].name, NAMES[newn])
    text = text.replace('agent/interview/高频面试题.md','agent/interview/README.md')
    text = text.replace('agent/interview/面试易错点.md','agent/interview/README.md')
    text = text.replace('agent/interview/面试前速查表.md','agent/interview/README.md')
    # Previous PR's standalone-guide entry points are removed, not retained as alternate courses.
    text = '\n'.join(line for line in text.splitlines()
        if not line.startswith('**Agent 架构前导：**') and not line.startswith('> **Agent 专题前导：**')) + '\n'
    text = text.replace('从 Agent Loop 出发，构建 Tool、Context、Memory、State、Permission、Checkpoint、Trace、Eval 与 Multi-Agent 的可恢复执行系统。', DESC)
    if p.name == 'README.md' or rel.startswith(('roadmap/knowledge-map','roadmap/content-depth','research/questions/module-index','research/questions/progress')):
        lines = []
        for line in text.splitlines():
            if ('| [Agent]' in line or '| Agent |' in line or '| 09 | [Agent]' in line or '| 09 | Agent |' in line):
                line = re.sub(r'\|\s*23\s*\|', '| 16 |', line)
                line = line.replace('Agent Runtime', 'Agent System').replace('01–23','01–16')
            lines.append(line)
        text = '\n'.join(lines)+'\n'
    if rel in {'README.md','roadmap/knowledge-map.md','roadmap/learning-path.md','roadmap/content-depth-audit.md','research/questions/README.md','research/questions/module-index.md','research/questions/progress.md'}:
        text = re.sub(r'(?<![\w/])184(?!\w)', '177', text)
    if rel == 'research/agent-sources/README.md':
        text = text.replace('23-block','16-chapter').replace('[← Agent Harness]', '[← Agent]')
    if rel == 'roadmap/agent-authoritative-sources.md':
        text = text.replace('[← Agent Harness]', '[← Agent]')
    if before != text:
        write(p,text)

# Correct curriculum-specific summaries, not unrelated statistics.
p=ROOT/'roadmap/knowledge-map.md'
t=p.read_text()
start = re.search(r'^## 09\..*$',t,re.M)
if start:
    end = re.search(r'^## 10\.',t[start.end():],re.M)
    endpos = start.end()+end.start() if end else len(t)
    replacement = '''## 09. [Agent](../agent/README.md) — 16 章

任务契约与自主权 → L1 应用 → L2 运行 → L3 接入 → L4 资源 → 安全与质量 → 系统演进。

01–02 定义任务与控制权；03 承接交互；04–08 建立循环、上下文、记忆、状态恢复和协作；09–12 连接模型、工具、知识及扩展；13 明确资源与执行环境；14–15 贯穿安全与质量；16 组合部署与选型。

这就是正式教材顺序，不另设 architecture 导读。Harness 是运行层概念，不是整个模块的名字。

'''
    t=t[:start.start()]+replacement+t[endpos:]
write(p,t)

p=ROOT/'roadmap/learning-path.md'; t=p.read_text()
s=re.search(r'^## Week 11[^\n]*',t,re.M); e=re.search(r'^## Week 13',t,re.M)
assert s and e
replacement='''## Week 11｜Agent：从任务到运行与接入

- S1：`01–02`，任务契约与自主权。
- S2：`03–04`，应用交互与执行循环。
- S3：`05–06`，上下文与记忆。
- S4：`07–08`，状态恢复与多 Agent 协作。
- S5：`09–10`，模型接入与工具契约。
- S6：`11–12`，工具执行与知识/扩展能力接入。

## Week 12｜Agent 收口 + System Design 起步

- S1：Agent `13–14`，资源环境与安全治理。
- S2：Agent `15–16`，观测评测与生产演进。
- S3：Agent Review + Interview + Exit Gate。
- S4：System Design `01–03`。
- S5：System Design `04–06`。
- S6：System Design `07–09`。

'''
t=t[:s.start()]+replacement+t[e.start():]
t=re.sub(r'^\| Agent \|.*$', '| Agent | 从任务契约与自主权画出四层职责，走通输入到交付；区分上下文、记忆、状态与外部事实；解释工具副作用、恢复、安全与评测；说明组件取舍和部署边界。 |',t,flags=re.M)
t=t.replace('→ Agent Runtime\n','→ Agent\n')
write(p,t)

p=ROOT/'roadmap/curriculum-granularity-audit.md'; t=p.read_text()
t=re.sub(r'^\| Agent Harness \|.*$', '| Agent | 23章旧课程 / 44 Canonical | 16 | 分层重构 |',t,flags=re.M)
t+='''
## 2026-09-16｜Agent 按系统职责重构

课程目录由 `agent-harness/` 改为 `agent/`；16章是唯一正式主线，原 architecture 笔记组吸收后移除。复习与面试各保留一个入口。不新增一级模块，不改变44道 ACTIVE Canonical、题目ID、来源与计数。

<details>
<summary>旧23章迁移关系（维护记录，不是第二条学习路线）</summary>

| 旧章 | 新课程中的归属 |
|---|---|
'''
migration={1:'01–04：系统边界、任务、应用与运行责任',2:'01–02：系统定义与控制权',3:'04、07：循环/事件与状态',4:'10：工具契约',5:'10：注册、路由与发现',6:'11：执行与错误',7:'11：副作用、并发、取消和进度',8:'04：规划、目标、停止与预算',9:'05：上下文组装、缓存与外部化',10:'05：压缩和继续执行正确性',11:'06：记忆全生命周期',12:'07、13：状态语义与存储资源',13:'07：检查点、恢复、分叉与副作用核对',14:'13–14：执行隔离与权限审批',15:'14：注入、秘密与风险约束',16:'12：协议、技能、钩子与扩展',17:'03、09：意图路由与模型适配',18:'08：协作、A2A与共享资源',19:'15：观测与回放',20:'15：评测与持续改进',21:'12、13、16：资源理解、环境与验证交付',22:'13、16：环境与生产部署',23:'16：框架、选型与迁移'}
for n in range(1,24):
    t+=f'| {n:02d} | {migration[n]} |\n'
t+='\n</details>\n\n合并去除重复的前言、频率说明和面试模板；核心机制、失败路径、取舍与验证按新职责编排。首次阅读只沿 Agent README 的01→16。\n'
write(p,t)

# Centralize the fresh architecture references in the existing source index.
p=ROOT/'roadmap/agent-authoritative-sources.md'; t=p.read_text()
t+='''
## 2026-09-16｜分层课程的参考边界

四层划分为教材综合抽象，不是厂商标准。Thread / Turn / Item 保留 Codex 语境；Task / Run / Step 采用教材工作定义。产品默认权限、API字段、模型能力和源码布局需要按使用版本重新核验。

| 参考 | 本课程使用范围 |
|---|---|
| [Codex App Server](https://developers.openai.com/codex/app-server) | 会话、轮次、输入输出与事件交互 |
| [Codex 固定源码快照](https://github.com/openai/codex/tree/5bf132cd527311eb61bbec46562e3890eb49df80/codex-rs) | 运行核心、工具协调、上下文与环境的职责对照 |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Workflow与动态控制、从简单模式演进 |
| [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 信息选择、上下文与长任务机制 |
| [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 执行过程、最终结果与评测驱动改进 |
| [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture) | Host、Client、Server 与互操作边界 |

学习入口统一为[Agent正式课程](../agent/README.md)，不再维护一份独立架构正文。
'''
write(p,t)

p=ROOT/'roadmap/terminology-glossary.md'; t=p.read_text()
t+='''
## Agent 分层课程的统一约定（2026-09-16）

| 名称 | 本课程约定 |
|---|---|
| Agent 模块 | 覆盖任务设计、四层职责、安全质量与生产演进；不是只讲 Harness |
| L1 / L2 / L3 / L4 | 应用 / 运行 / 接入 / 资源；与研究题库的 Depth 编号无关 |
| Harness / Runtime | 以运行层为核心的执行系统，实现可包含接入代码，不等于完整产品 |
| Task / Run | 任务目标与验收对象 / 一次受管理执行；关联由应用协议定义 |
| Thread / Turn / Item | Codex中的持续会话 / 单次请求及其后续工作 / 有类型输入输出单元 |
| Step / Event / Operation | 运行时推进单位 / 已发生的生命周期事实 / 可识别核对的外部逻辑动作 |
| Memory / State / Context | 未来复用的信息 / 程序执行事实 / 当前模型可见信息；不可互相替代 |

不把 Session→Run→Turn 宣称为通用固定层级。概念的完整解释回到[Agent](../agent/README.md)对应章节。
'''
write(p,t)

# Audit prose distinguishes current checks from the historical v1.0 deep review.
p=ROOT/'roadmap/final-quality-audit.md'; t=p.read_text()
lines=t.splitlines(); lines.insert(2, '\n> **版本说明（2026-09-16）：** 下文184篇/Agent23章的v1.0结论是历史审计，不覆盖新的章节排列。当前Agent已按任务→四层→治理重构为16章，全仓库正文177篇。本次结构、链接、计数与研究证据不变性检查记录见本文末尾；不将历史PASS伪装为一次新的逐项技术复审。\n')
t='\n'.join(lines)+'\n'
write(p,t)
for rel in ['research/questions/module-index.md','research/questions/progress.md','roadmap/content-depth-audit.md']:
    p=ROOT/rel; t=p.read_text()
    note='> **2026-09-16更新：** Agent为16章分层重构版，全仓库177篇正文。旧版深度与终局审计为历史记录；本次验证范围为结构、链接、迁移覆盖和证据不变性，详见既有质量记录。\n\n'
    lines=t.splitlines(); lines.insert(2,note); t='\n'.join(lines)+'\n'
    # Avoid reporting the historical complete audit as performed again on the new count.
    t=t.replace('177/177 Curriculum Markdown、235/235 Canonical、仓库内链接、Mermaid、跨模块 Ownership、术语与版本敏感事实风险审计均已完成', '旧版184/184 Curriculum Markdown与235/235 Canonical的历史审计已完成；新结构的检查范围以上述更新说明为准')
    write(p,t)

# Validate preserved question identities and evidence, and create a reusable structural check.
question_text=(ROOT/'research/questions/agent-harness.md').read_text()
active_ids={int(x) for x in re.findall(r'^###\s+AGENT-(\d{3})\s+·',question_text,re.M)}
assert active_ids == set(QUESTION_OWNER), (active_ids-set(QUESTION_OWNER),set(QUESTION_OWNER)-active_ids)
for rel,digest in raw_evidence.items():
    assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest, 'Interview evidence modified: '+rel

VALIDATOR = '''#!/usr/bin/env python3
"""Validate the single Agent learning route without fetching external content."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote
ROOT = Path(__file__).resolve().parents[1]

def prose(text):
    out=[]; fenced=False
    for line in text.splitlines():
        if re.match(r'^\\s*(```|~~~)',line):
            fenced=not fenced
        elif not fenced:
            out.append(line)
    return '\\n'.join(out)

def local_links():
    bad=[]; checked=0
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts: continue
        for match in re.finditer(r'(?<!!)\\[[^\\]\\n]*\\]\\(([^)\\n]+)\\)',prose(p.read_text(encoding='utf-8'))):
            target=match.group(1).strip().split(' "',1)[0].strip('<>')
            if not target or target.startswith(('#','http:','https:','mailto:','data:')): continue
            target=unquote(target.split('#',1)[0].split('?',1)[0])
            if not target: continue
            dest=(ROOT/target.lstrip('/')) if target.startswith('/') else p.parent/target
            checked+=1
            if not dest.exists(): bad.append((str(p.relative_to(ROOT)),target))
    return checked,bad

def main():
    errors=[]
    docs=sorted((ROOT/'agent/docs').glob('*.md'))
    if len(docs)!=16: errors.append(f'expected 16 Agent chapters, found {len(docs)}')
    if [p.name[:2] for p in docs] != [f'{i:02}' for i in range(1,17)]: errors.append('chapter numbers not continuous')
    if (ROOT/'agent-harness').exists(): errors.append('obsolete learning directory exists')
    if (ROOT/'agent/architecture').exists(): errors.append('parallel architecture course exists')
    home=(ROOT/'agent/README.md').read_text()
    for i,p in enumerate(docs):
        text=p.read_text()
        if home.count('](docs/'+p.name+')')!=1: errors.append('homepage chapter link not unique: '+p.name)
        if '主线位置' not in text or '本章产物' not in text: errors.append('missing chapter scaffold: '+p.name)
        if i and docs[i-1].name not in text: errors.append('missing previous link: '+p.name)
        if i<15 and docs[i+1].name not in text: errors.append('missing next link: '+p.name)
        if text.count('<details>')!=text.count('</details>') or re.search(r'<details\\s+open',text): errors.append('invalid/default-open quiz: '+p.name)
        if len(re.findall(r'^```',text,re.M))%2: errors.append('unclosed fence: '+p.name)
        if len(text.encode('utf-8'))<2500: errors.append('unexpectedly short chapter: '+p.name)
    q=(ROOT/'research/questions/agent-harness.md').read_text()
    ids=set(re.findall(r'^###\\s+(AGENT-\\d{3})\\s+·',q,re.M))
    if len(ids)!=44: errors.append('expected 44 ACTIVE Agent canonical questions')
    covered=set(re.findall(r'`(AGENT-\\d{3})`',(ROOT/'agent/interview/README.md').read_text()))
    if ids!=covered: errors.append('canonical learning map mismatch')
    total=sum(len(list((ROOT/d/'docs').glob('*.md'))) for d in ['python','fastapi','backend-engineering','mysql','redis','vector-db','llm-foundation','rag','agent','system-design'])
    if total!=177: errors.append(f'expected 177 curriculum files, found {total}')
    checked,bad=local_links()
    for path,target in bad: errors.append(f'broken local link: {path} -> {target}')
    print(f'Agent chapters: {len(docs)}; curriculum total: {total}; Agent canonical: {len(ids)}; local links checked: {checked}; broken: {len(bad)}')
    if errors:
        print('\\n'.join(errors)); return 1
    print('PASS: sequence, navigation, collapsed quizzes, fences, file links, counts and canonical map')
    return 0
if __name__=='__main__': sys.exit(main())
'''
write(ROOT/'tools/validate_agent_curriculum.py',VALIDATOR)

# Compile changed Python sources and run structural checks before any commit.
import subprocess
for p in (ROOT/'tools').glob('*.py'):
    compile(p.read_text(encoding='utf-8'),str(p),'exec')
check=subprocess.run(['python3','tools/validate_agent_curriculum.py'],cwd=ROOT,text=True,capture_output=True)
print(check.stdout)
print(check.stderr)
assert check.returncode==0, 'Structural checks failed; do not commit'

p=ROOT/'roadmap/final-quality-audit.md'; t=p.read_text()
t+='''
## 2026-09-16｜Agent分层重构检查

此次替换原课程，不新增架构学习支线。检查命令：`python3 tools/validate_agent_curriculum.py`。

- Agent正文16章连续，首页唯一目录、上下章导航、折叠自测及代码围栏通过检查。
- 旧agent-harness学习目录与独立architecture目录已移除。
- 全仓库正文177篇；44道ACTIVE Agent Canonical均有新章节位置。
- 旧23章的机制归属见既有粒度记录；原始interviews目录在迁移前后逐文件SHA-256相同。
- 本次为课程结构与内容编排重构，未宣称重新执行全部产品API实验或重做全仓库技术深度评级。

执行输出：

```text
'''+check.stdout.strip()+'''\n```
'''
write(p,t)
print('SOURCE CHAPTER MIGRATION:',json.dumps({str(k):sorted(v) for k,v in USED.items()},ensure_ascii=False))
print('Interview files preserved:',len(raw_evidence))
print('New Agent markdown files:',len(list(NEW.rglob('*.md'))))
print('Migration ready for branch-local commit.')
