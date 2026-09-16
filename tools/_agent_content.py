"""One-time reviewed content additions. All additions are teaching synthesis unless labelled otherwise."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
GUIDES={
1:'先完成任务契约，再看职责图。示例只是通用文件任务，不预设电商、Coding Agent 或任何个人项目。',
2:'先比较确定性流程和动态选择，再填写控制权决策表。学习目标是说明为什么不选更复杂方案，而不是记住所有可选组件。',
3:'先区分用户任务与一次执行，再看路由和交互。当前只需把运行层理解为可启动、查询、暂停和取消的执行服务，其内部循环在04章打开。',
4:'先走完一次观察—行动—反馈，再理解对象和事件。模型适配与受控工具执行暂作黑盒：前者返回候选决策，后者返回成功、失败或结果未知；09–11章再展开内部实现。',
5:'依次学输入组装、预算与外部化、压缩切换、正确性验证。可以分段学习，但不要只读压缩而跳过前面的选择和预算；源码对照用于第二遍核验，不是另一条课程。',
6:'按选择→写入→召回→纠错→失效走完生命周期。暂把 Memory Store 当成带作用域和版本的存取接口；12章讲接口，13章讲实际存储，不能把三个责任混成一个数据库。',
7:'分两段读：先理解状态/历史/检查点，再推演恢复与副作用。这里先采用最小动作契约：有稳定 operation_id，返回成功/失败/未知，可核对外部结果；11章再展开 Executor，不必先学完整实现才能理解故障窗口。',
8:'先判断任务能否独立分工，再理解交接、汇聚和共享资源。子 Agent 暂作返回状态与产物的执行单元；工具传输细节在后续接入层展开，不能因为尚未学协议就把失败当成不会发生。',
9:'先区分应用意图、运行策略与供应商适配，再学错误恢复。层的目录位置不是策略的唯一所有权：模型选择目标由L1/L2给定，L3兑现兼容调用。',
10:'先建立输入输出契约，再区分完整 Registry 与本轮可见集合，最后看发现、加载和版本。Schema、目录与权限是三个不同检查，不要合成一个“能调用”标志。',
11:'按 Invocation→结果→失败→并发/取消分段读。把07章的稳定逻辑动作标识带进来：一次重试可以有新 attempt_id，但不能因此变成新的业务操作。',
12:'先学信息与状态存取接口，再区分 MCP / Skill / Hook，最后用代码搜索作接口对照。协议、程序性知识和生命周期扩展不属于同一种抽象。',
13:'先问哪类资源保存什么事实，再选择执行环境及其生命周期。沙箱是有执行风险时采用的约束手段，不是每个 Agent 都必须部署一个容器。',
14:'先画信任边界，再看授权、审批绑定、隔离和外传。虽然本章后置展开，真实执行的每一步都必须先通过相应安全检查，而不是最终输出时补一层过滤。',
15:'分三段读：§1–2重建与定位过程，§3定义验证对象，§4把坏例变成改进。指标变好之前先固定任务、环境与评分口径，不能以日志完整代替任务成功。',
16:'这是系统收口，不是新的组件清单。§1–2把四层落成部署/故障边界，§3比较选型，§4以代码交付作实现对照，§5再重建完整设计。先掌握各段输入输出，再按需要深入框架与Coding细节；无须一次读完，也不另拆平行课程。'
}
INSERTS={
1:[('## 本章自测',r'''## 推导示例｜从一句需求到可验收的契约

下面是**教学构造**，不是某份真人面经，也不是产品默认行为。贯穿前几章只用同一个小任务：

> “帮我看一下这批文件，整理一份报告；不要修改原件。”

这句话还不足以直接执行。“这批”指哪些文件？报告交给谁？允许联网补充吗？原件间冲突怎么办？先澄清会改变权限、范围或验收的问题；不必为无关格式细节反复询问。

假设澄清结果如下。数字是示例预算，不是通用推荐值：

```yaml
task_id: report-01
contract_version: 1
requester: authenticated_user
input: authorized_manifest_v3
source_policy: original_files_read_only
network: disabled
output: report_draft_and_citation_manifest
write_scope: authorized_artifact_store_only
acceptance:
  - 每个事实性结论有可定位的来源和版本
  - 冲突及证据缺失显式列出，不编造结论
  - 原件未改变，交付物能够被请求者访问
limits:
  max_tool_calls: 20
  deadline_seconds: 300
```

这些字段解释了组件为什么存在，而不是反过来为既定组件找用途。

| 已明确的约束 | 推导出的责任 | 当前不必加入的东西 |
|---|---|---|
| 输入是有限授权清单 | L1固定范围；L3每次读取校验；L4提供真实文件 | 不自动扫描用户全部目录 |
| 文件内容可能冲突 | 模型提出调查方向；L2维护证据缺口；L1接受“待确认”结果 | 不靠生成语气强行消除冲突 |
| 不修改原件 | 只暴露必要能力，底层身份只读；新授权不得来自文件中的文字 | 不需要先做任意Shell再靠Prompt约束 |
| 需要可核对的报告 | Context带来源；保存产物与引用；完成前验证 | 不以模型输出final为唯一成功标准 |
| 任务规模尚小 | 先单执行单元、少量工具和明确预算 | 不默认长期Memory、多Agent或向量库 |

**反事实检查：** 如果所有文件总共只有很少文本，一次读取后生成就够了，先做确定性Workflow基线。如果需要根据中间证据决定读哪个文件、继续查什么，才比较受控Loop的收益。这两种方案共享同一任务契约；“用不用Agent”是可验证的选择，不是题目预设答案。

失败也要进入契约：文件无权限时不扩大搜索；来源缺失时交付缺口；超过预算时返回未完成事项。下一章继续决定上述每一个动作的控制权。

''')],
2:[('## 本章自测',r'''## 继续推导｜同一个任务，三种最小方案

沿用01章的只读文件报告。先做可以比较的基线，而不是一次上齐所有能力。

| 方案 | 谁决定下一步 | 适用前提 | 需要验证的代价 |
|---|---|---|---|
| 固定读取→生成→校验 | 程序 | 输入固定且可以一次装入 | 是否漏掉冲突、引用是否准确 |
| 固定阶段中加入动态检索 | 程序规定阶段，模型选查询 | 大部分流程已知，局部需要探索 | 动态检索是否增加有效证据 |
| 有限Agent Loop | 模型提候选，程序约束执行 | 后续调查明显依赖新观察 | 额外时延、调用数、越界及不停止风险 |

最后一种不是“最高级答案”。若三种方案质量接近，优先更简单、易验证的一种。比较时用相同输入、验收与预算，记录完成率、证据覆盖、违规动作、成本和耗时；这里不给虚构的提升百分比。

### 把决策权、执行权、验收权填到动作上

| 动作 | 模型可提出 | 可信程序/资源必须保证 | 是否允许自动执行 |
|---|---|---|---|
| 读授权清单内文件 | 选择读取对象与范围 | 身份、清单版本、路径与返回大小 | 允许范围内读取，但仍防敏感数据外传 |
| 增加资料来源 | 提出信息缺口 | 不得悄悄改变契约或联网 | 缺授权先澄清 |
| 生成报告草稿 | 组织材料、表达不确定性 | 保存版本、引用与产物访问控制 | 可以生成，但不自动视为已验证 |
| 改原件或对外发送 | 提出候选方案 | 新契约/具体批准、动作核对与审计 | 原契约禁止，不是“模型觉得安全就行” |
| 宣告完成 | 提交完成候选 | 验收引用、必需字段、原件未变等证据 | 由验收结果决定状态 |

如果用户后来要求修改原件，应先形成新契约版本，明确具体对象、改动范围与确认方式。旧的只读许可不会自动变成写入许可；未授权不是可通过多次重试解决的临时故障。

### 未采用方案也要能解释

当前没有跨任务复用需求，所以先不建长期Memory；没有清晰独立的子任务，所以先不建多Agent；没有任意代码执行需求，所以不为凑架构增加代码沙箱。以后出现规模或失败证据时再升级，并把新的正确性责任一起算进去。

Harness负责兑现循环、状态、工具与约束；Orchestrator描述任务/执行单元之间的组织责任；Workflow Engine可承载确定性或持久流程。这些名称可能在同一个库内重叠，不能把框架标签再当成四层之外的新层。

''')],
3:[('## 本章自测',r'''## 把交互落到一次可核对的任务轨迹

沿用文件报告：L1创建 `report-01` 后启动一次Run，前端订阅进度；输入文件缺权限时展示需要补充授权，而不是把任务标成成功。用户重新连接时，先读取权威任务状态，再补取事件，不仅恢复token动画。

```text
task_created(contract_v1)
→ run_started
→ evidence_ready(source_version)
→ report_draft_ready(artifact_ref)
→ acceptance_checked
→ task_delivered / needs_clarification / stopped_with_reason
```

这些是**教学事件名**，不是某个SDK接口。业务Task记录“报告是否被验收”；Run记录“某一次尝试怎样终止”；流式连接记录“客户端现在有没有连着”。三个生命周期相关，但不能共用一个布尔值。

若用户取消时草稿刚刚保存成功，L1应显示已停止继续工作及已产生的产物；是否删除产物属于明确的数据保留策略，不是假装保存动作没有发生。若修改了任务约束，新版本要送到L2的安全切换点；不能把新文字悄悄拼进一个已发出的模型请求。

''')],
4:[('## 本章自测',r'''## 将黑盒接到状态机：一次失败不等于整个任务失败

最小执行状态可用 `RUNNING / WAITING_TOOL / WAITING_INPUT / STOPPED` 表达；STOPPED还要携带成功、失败、取消或预算耗尽的原因。名称是工作定义，关键是允许的状态转换、谁持有执行权、恢复后如何确定唯一下一步。

`call_id`关联模型的一次调用及结果；`operation_id`标识需要核对的逻辑动作；`attempt_id`区分重试尝试。一个逻辑动作可以有多次尝试，不能因为超时就把它伪装成新动作。07章打开恢复语义，11章打开工具执行语义。

<details>
<summary>动手：一个可运行的最小控制循环（Python 3.11+，无网络、无真实副作用）</summary>

这是对旧版最小Loop的教学重写，不是Codex或Claude Code源码。模型用预设决策序列替代，文件用字典替代；它只测试调度、白名单、相关性与引用可解析，**不证明报告语义真实，也不提供生产级幂等或持久化**。

<!-- runnable: report-loop -->
```python
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Decision:
    kind: str
    value: str = ""
    citations: tuple[str, ...] = ()

def run_report(decisions: Iterable[Decision], max_steps: int = 4):
    sources = {"intro.txt": "范围说明", "notes.txt": "已确认的记录"}
    observations: dict[str, str] = {}
    events: list[tuple[str, str, str]] = []
    iterator = iter(decisions)
    for step in range(1, max_steps + 1):
        decision = next(iterator, None)
        if decision is None:
            return "incomplete", events
        if decision.kind == "read":
            call_id = f"call-{step}"
            if decision.value not in sources:
                events.append((call_id, "denied", decision.value))
                return "blocked", events
            observations[decision.value] = sources[decision.value]
            events.append((call_id, "tool_result", decision.value))
        elif decision.kind == "final":
            refs = decision.citations
            resolvable = bool(refs) and all(r in observations for r in refs)
            if not decision.value or not resolvable:
                events.append((f"step-{step}", "verification_failed", "citations"))
                return "unverified", events
            events.append((f"step-{step}", "draft_verified", "reference-check-only"))
            return "completed_reference_check", events
        else:
            return "invalid_decision", events
    return "budget_exhausted", events

ok = [Decision("read", "intro.txt"), Decision("read", "notes.txt"),
      Decision("final", "报告草稿", ("intro.txt", "notes.txt"))]
status, events = run_report(ok)
assert status == "completed_reference_check"
assert [e[0] for e in events[:2]] == ["call-1", "call-2"]
assert run_report([Decision("read", "secret.txt")])[0] == "blocked"
assert run_report([Decision("final", "草稿", ("intro.txt",))])[0] == "unverified"
assert run_report([Decision("read", "intro.txt")] * 5)[0] == "budget_exhausted"
assert run_report([Decision("delete", "intro.txt")])[0] == "invalid_decision"
print("report-loop: 5 cases passed")
```

下一步不是增加更多模型，而是逐一打开Context、持久状态和Tool Executor黑盒。本例返回的完成状态特意叫 `completed_reference_check`：通过有限检查不能夸称整个报告质量已被证明。

</details>

''')],
5:[('<a id="part-5"></a>',r'''### 固定源码对照：压缩不只是新增一个summary字段

这里恢复 `main` 原09–10章的实现阅读线索，依据仓库既有固定快照索引，**不是本轮重新遍历两个产品全部源码**。

| 实现记录 | 支持的观察 | 本课程据此保留的责任 |
|---|---|---|
| Codex `compact.rs`：manual/auto、pre-turn/mid-turn/standalone、replacement history | 压缩存在触发阶段和替换对象 | 触发、构建候选、验证与切换应分清 |
| 同文件：initial-context重新注入、live/persisted history、usage recomputation | 替换涉及状态与预算 | 检查关键上下文恢复、持久记录一致及新预算 |
| 同文件：hooks、analytics和准确率风险提示 | 压缩自己可失败、可观测 | 不把节省token当唯一成功标准 |
| Claude Code `QueryEngine.ts`、compact/snip与ToolUseContext记录 | 记忆注入、工具结果替换、投影有关联 | 压缩需与选择、外部化、去重一起设计 |

固定版本和已读/待读边界见[Codex索引](../../research/agent-sources/codex-source-index.md)、[Claude Code索引](../../research/agent-sources/claude-code-source-index.md)。源码支持某产品的具体观察；下文候选验证/回滚流程是教学设计，不等于源码逐行实现。

''')],
6:[('## 本章自测',r'''## 用一个记录推演纠错，而不是“再加一句忽略之前”

文件报告任务里，`目录A只读`是当前授权约束，应来自契约/策略，不应只存成可以被召回排名改变的Memory。`用户偏好按主题组织报告`则可能是未来可复用的记忆候选。

```text
m1: preference=按日期组织, source=用户此前确认, version=1
m2: preference=按主题组织, source=用户本次纠正, supersedes=m1
```

写入m2后，读取路径必须排除已失效的m1，缓存/向量索引也要最终对齐有效版本。只在新Prompt里说“忽略旧偏好”不能阻止下一次检索再次召回m1。

检验要覆盖错误偏好纠正、租户隔离、删除后不再召回和冲突未决；来源权威性及适用范围优先于单个相似度或模型置信度。与真实业务系统冲突时回查权威事实。

既有Claude Code索引记录了 `memdir/memdir.ts` 的memory prompt和 `loadedNestedMemoryPaths` 去重线索；它支持“Memory是Context来源之一”，**不支持凭空断言其完整写入、合并或TTL算法**。详见[已核验与待读范围](../../research/agent-sources/claude-code-source-index.md)。

''')],
7:[('## 本章自测',r'''## 恢复推演：操作标识先于可重试的副作用

本表是教学协议，用来打开“工具成功、检查点失败”的窗口，并不宣称跨系统恰好一次交付。

| 崩溃位置 | 已知事实 | 恢复动作 |
|---|---|---|
| 动作意图尚未持久化 | 未建立可恢复操作身份 | 不声称已经提交；重新按任务状态决策 |
| 意图/幂等键已保存，尚未发送 | 知道逻辑动作和授权边界 | 重新校验前置条件后才发送 |
| 已发送，回执未知 | 可能已产生副作用 | 用同一operation_id/幂等键核对，不盲建新动作 |
| 外部成功，本地检查点失败 | 权威结果可能已存在 | 补齐本地状态与回执，不再次执行成功动作 |
| 无幂等接口且不能查询 | 系统没有足够证据判断 | 保留UNKNOWN并转人工/业务核对；补偿也可能有风险 |

事件、审批和产物记录同样有版本。恢复时还要区分**指令来源**与**已应用快照**：Fork可以继承某个快照，却不自动获得实时来源、凭证或原任务批准。`ThreadInstructionsProvider` 的warm/cold resume、fork及快照差别见[固定Codex索引第8节](../../research/agent-sources/codex-source-index.md)。这些是产品实现观察；本课程不把Run与Codex Turn强绑为一棵通用树。

''')],
8:[('## 本章自测',r'''## 分工示例：同一报告的两个调查方向

只有当两个来源集合确实可以独立调查，才尝试让两个子执行单元分别返回证据。交接契约至少包含目标、授权范围、预算、截止时间、允许的产物形式和失败状态；不默认继承父级全部历史和写权限。

子A完成、子B超时时，父级要根据验收决定部分交付、继续单独调查或返回未完成，不能把A的成功算作整个任务成功。汇聚的是证据、来源和未决问题，不是把两份完整transcript重新塞回父Context。

共享产物写入采用唯一writer或隔离目录加版本化汇聚。上下文隔离只隔离信息，不会自动消除共享文件竞争。父级预算还需包含子任务占用，避免递归委派放大成本。

旧版 `Task.ts` 对照的价值在于任务具有状态、输出位置和取消语义；这些产品Task类型不等于本课程L1业务Task，见[Claude Code任务索引](../../research/agent-sources/claude-code-source-index.md)。

''')],
9:[('## 本章自测',r'''## 路由的三种决定：避免把所有Router放在同一层

| 决定 | 主责 | 失败后不能怎样处理 |
|---|---|---|
| 请求交给哪种应用流程/角色 | L1意图与任务分流 | 误路由不能顺便增加权限 |
| 当前任务需要何种模型能力与预算 | L2根据任务和运行状态选择策略 | 不能只按最便宜而忽略工具/上下文要求 |
| 如何调用匹配的供应商、如何规范化响应 | L3适配并兑现路由策略 | 不支持的协议必须显式暴露，不静默降级 |

Claude Code既有索引中的 `fallbackModel`、usage和budget配置可作为运行控制的实现线索，但不是“换model name就恢复成功”的证明。切换前核对工具schema、消息表示、上下文长度、多模态、已有外部动作与输出契约；切换后记录原因并按同一任务验收。模型响应缓存或切换都不能替代副作用核对。

''')],
10:[('## 本章自测',r'''## 源码对照与一个失配场景

旧版Tool章节保留的关键观察是：Claude Code `Tool.ts` 不只有输入schema和call，还暴露只读/破坏性/并发安全、interrupt、permission、progress与context影响；Codex工具层把schema、ToolCall、ToolExecutor、ToolOutput作为明确对象。出处与固定版本见[Claude Code索引](../../research/agent-sources/claude-code-source-index.md)、[Codex工具索引](../../research/agent-sources/codex-source-index.md)。

**教学失配场景：** 模型看到工具v1，执行端已升级到v2且参数语义变了。即使JSON仍可解析，也不能按新含义执行旧请求。Registry应解析稳定身份/版本，冻结或重载当前可见契约；无法兼容时把具体差异反馈给运行层，再决定修复参数或停止。

`model_visible_specs`表达的关键是“完整目录”和“当前模型可见投影”分离；曝光不是授权，发现召回率也不是执行正确率。测试需分别覆盖正确工具是否被发现、是否选对、版本是否匹配、权限是否被执行端拒绝。

''')],
11:[('## 本章自测',r'''## 把执行结果分成事实、建议与展示

响应里的 `retryable`只能是错误处理提示，不能独自授权重放。是否重试还取决于动作类型、是否已开始、可核对性、幂等保证与剩余预算；Tool返回的文字也不能覆盖可信权限策略。

旧版Codex对照明确区分 `FunctionCallError::RespondToModel` 与 `Fatal`，以及 `ToolOutput` 的日志/模型/Host表示。这里吸收的是“可向模型反馈的局部错误”与“必须停止/上报的运行时错误”不能混为一谈；名字和具体分支仍属于固定快照，不是所有框架标准。对照入口：[Codex工具层索引](../../research/agent-sources/codex-source-index.md)。

取消测试必须覆盖：提交前取消、等待执行时取消、执行中合作式取消、客户端断线但任务继续、取消后迟到成功回执。最后一种要回到07章核对动作，而不是丢弃事件并宣称没有发生。只读工具也可能泄露数据；可并发性由具体资源和输入决定，不由 `async` 关键字决定。

''')],
12:[('## 本章自测',r'''## 能力目录也有生命周期

目录可以保存稳定身份、版本、摘要、参数schema位置、来源/租户、可见条件、运行时handler及风险元数据；模型先拿少量候选，再按需加载完整契约。Skill可以先加载说明，真正需要脚本/资产时再读取，不等于永远全量塞入Prompt。

Claude Code索引里的 `searchHint`、`dynamicSkillDirTriggers`、`discoveredSkillNames`支持这种渐进加载观察；Codex索引记录了command、MCP tool、prompt、agent等Hook handler形式。**协议/扩展提供什么**和**运行层何时允许用它**仍是不同责任，详情见两个[固定源码索引](../../research/agent-sources/README.md)。

版本变化或插件卸载后，要让旧可见集合与当前执行目录一致。不要将安全门仅做成可被关闭的Hook；Hook失败策略依责任区分：诊断Hook可以受控降级，安全校验失败应拒绝或升级，而不能按普通日志错误忽略。

''')],
13:[('## 本章自测',r'''## 产物不是一个随时可用的字符串路径

文件报告至少有输入清单版本、读取证据、草稿产物和引用清单。产物引用应携带归属、版本/摘要、保留策略与授权范围；使用时重新检查可访问性，不把缓存的路径当成永久许可。

环境回收、工作区被修改或文件已删除时，Run仍可能存在。恢复必须验证引用是否可解析和内容是否仍对应旧证据；不成立则重建或明确阻塞，不能把空文件当成成功恢复。执行环境、模型服务、数据库和外部系统是不同资源，不要求同一进程或相同持久性。

''')],
14:[('## 本章自测',r'''## 审批推演：批准的究竟是哪一次动作

教学例子：用户批准修改 `report.md@v3` 的特定差异。执行前文件已到v4，或工具参数变成修改另一个文件，这不是原来的批准对象。批准记录需要绑定可信请求者、任务/契约版本、目标资源、参数或差异摘要、动作范围和有效期；执行时再核对当前策略与资源版本。

```text
形成动作候选 → 可信界面展示具体范围 → 保存批准
→ 执行时重校验 → 兑现动作 → 保存回执 → 验证结果
```

撤销、过期、Fork、换租户、换凭证或目标变化都应重新判断批准是否仍适用。批准不能提升调用者本来没有的资源权限。已发生的副作用不会因撤销批准自动回滚；必须停止后续动作并核对、补偿或转人工。

''')],
15:[('## 本章自测',r'''## 从同一个报告任务得到一组可复现验收

这是教学测试设计，不是宣称已经跑过真实Agent或获得某个线上提升。

| 用例 | 要观察的事实 | 通过标准/修改方向 |
|---|---|---|
| 正常授权文件 | 读取范围、引用、产物版本 | 引用可解析且结论可由证据支持；语义需独立核验 |
| 文件无权限 | 访问拒绝和后续动作 | 不越界、不无限重试；修接入/权限而不是加Prompt |
| 两个来源冲突 | 来源版本、冲突标记 | 保留不确定性，不伪造统一结论 |
| 压缩后继续 | 必保约束、外部操作、后续结果 | 允许不同合法路径，但不能丢约束/重复动作 |
| 保存后崩溃 | 稳定动作标识与真实产物 | 恢复后核对并补状态，不重复写新产物 |
| 新版本模型/工具 | 同一任务集的质量、成本、延迟 | 先固定实验条件，再做回归和受控发布 |

Continuation Test不要求压缩前后每个Tool Call逐字相同；评估等价约束与结果、失败恢复及预算，避免把合法探索路径差异误判为错误。日志脱敏后仍应留下足够关联与可受控解析的证据引用。

旧版的具体阅读线索也保留：Codex `rollout-trace/README.md` 区分原始payload、ConversationItem、ToolCall及信息流关系；它支持追踪“看见什么、调用什么、改变什么”，不要求暴露隐藏思维链。参见[Trace固定快照索引](../../research/agent-sources/codex-source-index.md)。

''')],
16:[('<a id="part-2"></a>',r'''### 把旧版Gateway与持久层职责放回四层

| 实现组件 | 承载职责 | 必须交接的事实 |
|---|---|---|
| API/Streaming Gateway | L1任务入口、身份绑定、进度与交付 | task/run关联、取消/确认请求、重连位置 |
| Harness Worker / Scheduler | L2循环、预算、状态与执行权 | 检查点、租约、未决动作和停止原因 |
| Tool Gateway | L3调用校验、凭证边界、执行适配 | 稳定operation、attempt、结果/回执、策略版本 |
| Model Gateway | L3供应商兼容、限流和容错 | 能力约束、调用usage、失败原因；不是全任务重跑 |
| State / Artifact / External Services | L4保存事实及真实副作用 | 版本、可核对状态、授权访问和保留策略 |
| Trace / Eval / Audit | 横切观测、验收和改进 | 贯穿各层的关联ID、证据与评分版本 |

这是同一张逻辑图的部署映射，不要求每行一个微服务。尤其不要让Gateway或浏览器保存唯一任务状态，也不能让Worker无协调地把同一个Run分配给两个writer。旧版专章的价值是明确这些边界，不是拓扑画得越复杂越好。

'''),('## 本章自测',r'''## 把最终方案讲回最初的任务

回到01章的文件报告，不要按工具清单汇报。先说授权输入与输出验收，再说明为什么选择固定读取或受控Loop，接着画应用/运行/接入/资源的交接、失败恢复和验证。最后才回答是否需要队列、多Worker、长期Memory、多Agent和独立沙箱。

当任务规模尚小时，一个进程可实现四层职责；当持续时间、隔离或并发需求变化时，再根据瓶颈和失败证据拆分。升级不只增加组件，也增加状态迁移、版本兼容、回滚和运营责任。

框架对照是旧版保留的实现参考，不是版本无关的功能保证。候选框架应在固定版本上实际验证工具调用、断点恢复、审批、取消、压缩、追踪与迁移，记录未支持能力；官方资料和源码只证明读到的部分，不替业务验收。

''')]
}
EXTRA_QUIZZES={
1:[('报告里缺一个关键来源，应编一个合理结论还是停止所有工作？','按契约区分可部分交付和必须补充的证据；显式标注缺口，禁止编造。是否停止由验收条件和剩余预算决定。'),('模型说“报告完成”，程序还应核验哪些证据？','来源与版本可定位、引用和产物可访问、原件未被修改、未决冲突已披露；结构验证不能替代语义核验。')],
2:[('相同输入下Workflow与Agent质量接近，该如何选？','在相同验收、预算下比较时延、成本、风险和维护复杂度，优先更简单且可验证的方案。'),('用户新增“顺便修改原文件”时能沿用只读授权吗？','不能；更新契约并绑定具体动作审批和资源权限，不能从原许可或模型文字推导写权限。')],
3:[('重复收到相同文本是否一定是重复任务？','不一定；用请求身份和幂等契约区分重传与用户主动重跑，不能仅凭文本相同去重。'),('用户重连时只重放token够吗？','不够；先读取权威Task/Run状态，再恢复事件位置，防止把旧进度误当当前事实。')],
4:[('同一工具再次调用是否一定是死循环？','不一定；分页、合法重试和新输入查询都可重复。结合动作签名、状态进展和同类错误判断。'),('教学Loop的引用检查通过，能证明自然语言结论真实吗？','不能；它只证明示例校验覆盖的有限属性，语义真实性需要更强证据核验。')],
5:[('Prompt Cache命中是否说明模型看到的资料没有过期？','不说明；前缀计算复用与应用选择了什么资料是不同问题，后者仍需source/version/freshness校验。'),('压缩候选生成失败时能先删除原History吗？','不能；候选验证和保存成功前保留旧活动视图，切换时维持可恢复性，失败明确回退或停止。')],
6:[('更新Memory但检索索引未更新会怎样？','旧记录可能继续被召回；读取端须核对有效版本/失效标记，并使派生索引和缓存最终对齐。'),('相似度最高的Memory可以覆盖当前审批吗？','不能；权限来自可信契约与执行策略，Memory不能产生授权。')],
7:[('换worker后应沿用哪个ID核对已提交的动作？','沿用逻辑operation_id及对应幂等键/外部引用；attempt_id可以变化，但不得冒充新业务动作。'),('没有幂等也没有查询接口，怎样保证未知动作只执行一次？','不能凭空保证；保留UNKNOWN并采取业务核对/人工处理，不能把重试或补偿宣称恰好一次。')],
8:[('子任务一半成功、一半超时，父任务如何汇聚？','根据验收判断部分交付、继续调查或失败，保留未决证据；不能用成功子任务覆盖失败部分。'),('父Agent的批准是否默认能传给所有子Agent？','不能；按任务范围、身份、参数和资源重新约束，不能因委派扩大权限。')],
9:[('模型切换后Tool格式不兼容，能丢字段继续吗？','不能静默丢语义；显式报告不支持或重新协商调用，保留状态与已执行副作用。'),('路由准确率相同的两个方案还比较什么？','风险加权错误、未知意图澄清、下游影响、时延、成本与恢复能力，而不只总体准确率。')],
10:[('Registry找到handler是否足以执行？','不够；还需匹配版本、schema、业务语义、身份权限与资源前置条件。'),('发现系统漏掉正确工具，换更强模型一定解决吗？','不一定；先测catalog覆盖和candidate recall，再分离选择错误与执行错误。')],
11:[('Timeout回包写了retryable=true就能重试吗？','不能；提示不是授权，仍需判断动作副作用、执行阶段、幂等/核对能力和预算。'),('取消后远程动作成功回执晚到，应该丢弃吗？','不能；记录并核对外部结果，停止后续动作，必要时补偿或转人工。')],
12:[('Hook失败可以统一忽略吗？','不可以；诊断与安全责任不同，安全关键检查失败应拒绝或升级，不能开放执行。'),('Skill包含脚本是否等于脚本自动获得执行许可？','不是；加载知识、读取资产、执行脚本是不同动作，各自受到权限与环境限制。')],
13:[('Checkpoint里的artifact路径存在就能复用吗？','还需核对身份、版本/摘要、有效期与可访问性；同一路径可能已经指向新内容。'),('运行状态存在而沙箱已回收，意味着无法恢复吗？','取决于持久状态与产物是否足以重建；重新验证环境、引用和未知副作用后决定继续或阻塞。')],
14:[('批准参数后目标文件版本发生变化怎么办？','重新校验批准是否仍匹配目标和差异；不匹配时重新确认或拒绝，防止检查到执行之间的变化。'),('Output Guardrail能撤销已经发送的外部消息吗？','不能；动作前必须有权限与风险门，事后发现只能核对、停止后续行动并采取可行补偿。')],
15:[('压缩后走了不同的合法Tool路径应判错吗？','不一定；比较约束、证据、结果、预算和失败恢复，不要求逐动作完全相同。'),('减少token但任务完成率下降，该如何做实验？','固定数据集、环境、工具和评分，定位上下文选择/压缩缺失，回滚或修正策略，再做回归。')],
16:[('四层图是否必须对应四个部署服务？','不是；逻辑职责与部署边界独立，按隔离、规模、生命周期和故障需求决定拆分。'),('框架支持Checkpoint就能宣称长任务可靠了吗？','不能；要验证业务状态、外部副作用、批准、环境引用、版本迁移与恢复实验。')]
}
def apply():
    for n in range(1,17):
        path=next((ROOT/'agent/docs').glob(f'{n:02}-*.md')); text=path.read_text()
        # A short section-level route, never a mandatory calendar.
        marker='<!-- enrichment: reading-guide -->'
        if marker not in text:
            loc=text.index('\n\n',text.index('> 本章产物'))
            text=text[:loc]+'\n\n'+marker+'\n> **阅读提示：** '+GUIDES[n]+text[loc:]
        for anchor,body in INSERTS.get(n,[]):
            if body.strip() not in text:
                assert text.count(anchor)==1,(path,anchor)
                text=text.replace(anchor,body+anchor,1)
        extra='\n'.join('<details>\n<summary>'+q+'</summary>\n\n'+a+'\n\n</details>\n' for q,a in EXTRA_QUIZZES[n])
        mark='<!-- enrichment: scenario-checks -->'
        if mark not in text:
            text=text.replace('## 回到主线',mark+'\n'+extra+'\n## 回到主线',1)
        if n==5:
            start=text.index('### Prompt / Context Cache 应该缓存什么')
            end=text.index('<a id="part-4"></a>',start)
            text=text[:start]+'''### 区分前缀计算缓存与应用层信息缓存\n\n| 对象 | 复用什么 | 不能替代什么 |\n|---|---|---|\n| Provider Prompt Cache | 符合供应商条件的相同输入前缀计算 | 不复用整个最终答案，不保证应用资料新鲜 |\n| 应用Context投影/模板缓存 | 已组装片段、指令或schema视图 | 仍需版本、权限和当前任务边界 |\n| Tool/检索结果缓存 | 某次查询的派生结果 | 要按来源更新、租户和权限失效 |\n| Artifact外部化 | 可寻址的完整结果 | 是保存/按需读取，不等于缓存命中 |\n\n[OpenAI Prompt Caching官方说明](https://platform.openai.com/docs/guides/prompt-caching)说明前缀匹配与计算复用。具体支持条件依模型/API版本，不在本章硬编码价格或保留时间。稳定指令和工具定义放在可复用前缀有助于命中；当前目标与新证据仍必须正确传入。\n\n所谓“旧Context被错误复用”，首先要查应用自己缓存了过期材料或省略了新版本，而不能把Provider前缀命中本身等同于读到旧答案。应用缓存需考虑身份/租户、来源版本、工具schema、策略、模型/供应商兼容性；命中率是性能指标，不是事实正确性指标。\n\n'''+text[end:]
            old='Instructions      10k\nGoal / State       8k\nRecent History    20k\nMemory / RAG      30k\nTool Definitions  20k\nTool Results      20k\nReserve Output    20k'
            new='Instructions      10k\nGoal / State       8k\nRecent History    20k\nMemory / RAG      30k\nTool Definitions  16k\nTool Results      20k\nReserve Output    16k\nSafety Headroom    8k\nTotal             128k'
            text=text.replace(old,new)
            text=text.replace('数字只是示意，真正值要结合模型和任务。','数字只是示意，真正值要结合模型和任务。输入上限应同时扣除输出预留与安全余量，并使用供应商兼容的计数方式校验；未发生的未来Tool结果不提前算入当前输入，但需预留下一步增长空间。')
        if n==11:
            text=text.replace('"retryable": true','"retry_hint": "requires_action_reconciliation"')
        path.write_text(text)
