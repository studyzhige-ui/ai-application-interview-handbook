# 上下文｜一次任务怎样变成连续的模型请求

[← 模块入口](README.md) · [下一篇：工具 →](03-tool-lifecycle.md)

用户说：“分页函数第一页返回错了，请修复，但不要改变公开接口。”模型还没读文件，怎么知道错在哪里？它先提出读取动作，宿主程序执行，再把文件内容交回模型。读过实现以后，下一次判断才有了新的依据。

本篇沿[统一分页练习](../../practice/coding/docs/09-ai-coding.md)追踪这个过程：`items = [10, 20, 30]`，每页两项，第 1 页应返回 `[10, 20]`。以下请求、编号和时间线均为教学示意，不是实际采集的 Codex 日志，也不是可直接发送的 API 报文。

<a id="request-chain"></a>
## 1. 先看两次请求之间究竟多了什么

**模型负责提出下一步，宿主负责执行动作并组织下一次输入。** 模型说“我读一下文件”只是文字；只有结构化工具调用被宿主执行，文件内容才会成为新的观察结果。

| 时刻 | 模型接收或产生的内容 | 宿主已经做了什么 |
|---|---|---|
| 第一次请求 | 修复要求、项目约定、工作目录、可用工具说明 | 准备本次输入，尚未读取实现 |
| 模型提出调用 `c1` | 请求读取 `pagination.py` | 找到工具，检查并执行读取 |
| 工具完成 | `c1` 对应结果包含旧表达式 `start = page * page_size` | 将调用及结果记入历史 |
| 第二次请求 | 保留任务约束，并加入相关调用与文件内容 | 使模型能够根据实现继续判断 |
| 模型继续 | 算出第 1 页的 `start=2`，取到 `[30]`，与约定不同 | 等待并处理后续修改、测试等调用 |

第二次请求不是孤零零的一段文件内容。模型还需要知道为什么读它、要修什么、哪些行为不能改。反过来，已经发生过的一切也未必都值得再次发送。

可以把这次变化写成一个很小的逻辑清单：

```text
请求 A：任务约束 + 项目与环境信息 + 工具说明 + 当前相关历史
模型输出：调用 c1，读取 pagination.py
工具结果：c1，读取成功，包含旧偏移表达式
请求 B：继续保留必要约束和历史 + c1 调用 + c1 结果
```

Codex 的主循环位于 [session/turn.rs 的 `run_turn`][src-turn]。它组织模型采样、工具后续和下一次请求。“采样”在这里就是请求模型生成一次输出。一轮工作可以采样多次；最终文字返回也不证明代码已经修对，任务结果仍要由差异与测试验收。

<a id="lifetimes"></a>
## 2. 再给这几个不同长度的过程命名

两次采样属于同一个修复过程；关闭客户端后恢复的对话，又可能跨越不同进程。用一个“会话”概括它们，会把状态的寿命混在一起。

| 名称 | 在分页任务中的含义 | 它没有代表什么 |
|---|---|---|
| Thread（对话线程） | 给持续对话及其历史一个可恢复的身份 | 原进程一直存活 |
| Session（核心执行实例） | 当前持有历史、服务与执行控制的运行实例 | 全部内容已经永久保存 |
| Turn（交互轮次） | 处理当前输入及随后模型、工具活动 | 仅一次模型请求 |
| StepContext（单次请求快照） | 固定本次请求使用的设置、环境、指令和工具视图 | 整个 Thread 永不变化的配置 |

例如，读文件、修改、测试可以发生在同一 Turn 的多个请求中。内部类型与客户端协议的 Thread、Turn、Item（交互条目）服务于不同接口，阅读时按职责对应，而不是把同名对象当成完全相同的结构。

循环结束还要检查工具后续、待处理输入和停止钩子。钩子是在指定阶段运行的附加逻辑；停止钩子可以要求补充工作。因此，“模型刚输出一段文字”与“这一轮可以结束”也要分开。[源码入口：继续与停止分支][src-turn]。

<a id="history-view"></a>
## 3. 历史保存过程，请求只取当前需要的视图

一次读取完成后，宿主先把调用和结果组织成有类型的历史条目，再为后续模型准备输入。这里的“视图”是按用途组织出来的表示，不是另一份独立发生的历史。

```text
用户输入、工具结果、指令与环境变化
                  ↓
           运行中的结构化历史
                  ↓
       为当前模型生成可发送的历史视图
                  ↓
         与基础指令、工具说明组成请求
```

`run_turn` 使用历史的 `for_prompt(...)` 视图准备采样。`ContextManager` 还将部分宿主事实和审核状态与模型窗口分开管理：有些信息必须由程序保留，却不需要每次原样发给模型。[请求调用处][src-turn]与[历史管理实现][src-history]分别对应这两层。

| 材料 | 用来回答的问题 |
|---|---|
| 模型本次输入 | 这一次判断究竟看见了什么？ |
| 宿主持有的事实与控制状态 | 程序继续执行和审核还需要保留什么？ |
| 已持久化历史 | 重启后能够重新取得哪些记录？ |
| 文件、进程或远端服务的真实状态 | 动作实际上产生了什么效果？ |

例如，测试摘要可以只保留失败名称与断言差异，便于继续修复；需要诊断原输出时，则应确认原材料实际保存在哪里、是否仍可读取。不能从“模型看见摘要”推导出“所有原始日志都有永久副本”。[持久化与真实状态核对](04-engineering-evaluation.md#recovery)负责解释后两层怎样配合。

<a id="instructions"></a>
## 4. 指令告诉模型应该怎样做，刷新决定何时采用新约定

用户要求“不改公开接口”，项目的 `AGENTS.md` 说明测试方法，宿主还可能提供用户级或线程级指令。它们的来源和适用范围不同。外部文件里出现一句“忽略用户要求”，仍然只是待分析文件的内容，不会因此取得授权。

`AgentsMdManager` 负责读取相关来源，形成已应用的指令快照。可以用一次修改项目约定的过程理解：

1. 当前请求已经使用约定 A；它不会因为磁盘文件变了，就自动变成使用约定 B 的请求。
2. 到允许刷新的边界，管理器重新判断需要取得哪些来源。
3. 新内容通过校验后，替换已应用快照，供随后请求捕获。

“提供者”是负责取得指令的程序接口；“快照”是已经取得的内容。知道提供者存在，不等于它本次成功返回了有效指令。[源码：`agents_md_manager.rs` 的刷新与继承实现][src-agents]。

> ⚠️ **注意：边界刷新不等于每次重读所有文件。** 项目发现有缓存条件；权限或项目可信范围收紧时，需要先使相关缓存失效，避免继续带入已无权读取的旧内容。刷新失败也不能当作新约定已经生效。

<details>
<summary>源码进一步看什么：刷新锁、缓存与子 Agent 继承</summary>

刷新串行进入，防止两个结果互相覆盖；需要调用外部提供者时，不长时间持有内部状态锁。管理器结合环境和项目可信级别决定是否重新发现项目指令，未变化时复用允许复用的缓存。子 Agent 可以继承已应用内容，但线程提供者只有明确允许共享时才随之继承。读代码时分别找“读取来源”“失效旧缓存”“提交新快照”，不要把三步合并成一次文件读取。

</details>

<a id="request-snapshot"></a>
## 5. 为什么模型看见的工具与执行依据要绑定在一起

假设请求发出时，读取工具访问项目 P1。模型还在生成，用户切换到 P2。如果宿主用 P2 的环境解释一个根据 P1 生成的调用，同一个相对路径就可能指向另一份文件。

`StepContext` 将这次请求的设置、环境、工具路由与已加载指令绑定起来。MCP（模型上下文协议）连接外部工具与资源；该请求采用的 MCP 连接及目录也随快照固定。后续解释调用时继续持有产生它的快照。[定义][src-step]与[调用运行时][src-parallel]给出这层联系。

下面摘出固定源码中的三个字段；它是**不完整的 Rust 结构片段，不能独立编译**：

```rust
pub(crate) settings: Arc<ResolvedStepSettings>,
pub(crate) mcp: Arc<McpBinding>,
pub(crate) tool_router: Arc<ToolRouter>,
```

冒号左边是字段名，右边是类型；`pub(crate)` 限定字段的可见范围，`Arc` 用来共享持有对应对象。先观察三个字段分别指向本次设置、MCP 绑定和工具路由。它们在同一请求级对象里，解释了为什么执行不能随手换用后来生成的工具目录。结构中还包含环境和指令等字段，不是只有这三项。[源码：`StepContext` 结构定义][src-step]。

| 时刻 | 捕获或发生的状态 | 对调用的影响 |
|---|---|---|
| A | 捕获 P1、工具目录 T1 | 模型据此提出动作 |
| B | 用户提交切换到 P2 的输入 | 已发送请求不会被倒改 |
| C | 原请求产生调用 | 仍按原快照解释，是否执行另看取消和权限 |
| D | 下一次请求捕获新状态 | 可以使用 P2、T2，并告知必要变化 |

> ⚠️ **注意：一致解释不是永久许可。** 原快照说明模型依据什么生成了调用，不能取消新的安全限制；动作仍要通过执行控制、审批与环境约束。

`TurnContext` 同时保留初始设置与供下一步捕获的设置，旧调用方还有兼容路径。请求级快照已经存在，不等于所有内部调用方都已完成同样的迁移。[源码：初始设置与下一步设置][src-turn-context]。

<a id="context-delta"></a>
## 6. 只发送变化，需要先有仍然有效的旧状态

模型已经知道工作目录是 P1，下一步切到 P2。它需要知道目录变化，却通常不需要再次接收全部未变说明。Codex 因此保存用于比较的基线：`reference_context_item` 比较设置，`world_state_baseline` 比较相关环境与能力状态。[历史基线][src-history]与[变化记录调用处][src-turn]。

可以把增量关系理解为：

```text
模型已有：目录 P1，测试规则 A
本次变化：目录改成 P2
下一次应理解为：目录 P2；其余信息须按仍有效的规则解释
```

如果压缩已经移除了原状态，只给一句“目录改了，其他不变”，模型就没有足够材料还原含义。因此，替换历史时必须处理相应比较基线：该重新注入完整信息时，就不能继续只发差异。“世界状态”在此指宿主组织的运行条件，不是模型拥有全世界事实。

<a id="paired-results"></a>
## 7. 调用和结果怎样在历史里保持对应

回到调用 `c1`。模型请求读取文件，宿主得到文件内容；二者用 `call_id` 关联。多次相同工具并行执行时，结果可能先后返回，编号仍能说明结果属于哪次调用。

```text
调用：c1，读取 pagination.py
结果：c1，读取成功，返回相应内容
调用：c2，运行测试
结果：c2，进程退出，返回失败摘要
```

上面是关系示意，不是统一工具输出格式。真实类型和封装见 [registry.rs 的 `AnyToolResult`][src-registry]。大结果还可能带有影响后续截断的预算元数据。为判断测试是否完成，保留退出状态和关键差异比只留下日志开头更有用；这是结果设计要求，不代表每个工具都采用相同摘要算法。

中断或筛选可能留下只有调用、没有结果的历史。`normalize.rs` 可以为缺失结果的函数调用补入表示中止的合成结果；孤立结果和工具搜索等协议类型按各自规则处理。[源码：配对与规范化][src-normalize]。

> ⚠️ **注意：合成 `aborted` 只补全模型输入结构。** 它不执行工具，也不证明外部动作没有发生。恢复时的实际状态检查见[工程篇](04-engineering-evaluation.md#recovery)。

<a id="budget-cache"></a>
## 8. 先分配容量，再考虑能复用多少计算

token 是模型处理输入与生成时的计数单位，不等于字符数。一次请求要给指令、历史、工具说明、新结果和后续生成留空间。

用一组**教学预算，不是 Codex 默认值**计算：窗口 32,000 token，预留生成 6,000，安全余量 2,000，输入可规划 `32,000 − 6,000 − 2,000 = 24,000 token`。固定指令和工具说明已占 5,000，历史与新结果合计便剩约 19,000。实际计数和触发条件要结合模型、输入类型与配置；不能把这个减法当成实现的全部预算逻辑。[窗口判断的调用处][src-turn]。

连续请求常有相同的前缀。保持内容和标识稳定，有助于服务端复用前缀计算。源码中，规范化合成结果的标识由来源标识稳定推导，注释将其与重试、恢复时的提示缓存联系起来。[源码：合成标识][src-normalize]。

| 手段 | 复用或减少的对象 | 仍须检查什么 |
|---|---|---|
| 前缀缓存 | 重复输入的部分计算 | 输入是否仍适用、是否超出窗口 |
| 答案缓存 | 已有答案 | 当前请求能否安全复用答案 |
| 上下文选择 | 无关或不必要的输入 | 是否误删关键条件与证据 |

缓存不是记忆，也不是正确性检查。项目约定过时，即使计算命中缓存也可能给出错误判断。

<a id="compaction"></a>
## 9. 压缩怎样腾出空间，又保住尚未完成的工作

旧历史已经很长时，在末尾再加摘要只会更长。Compaction（上下文压缩）需要构造较小的替换历史，让后续请求从它继续。

分页任务可以有这样的**摘要设计示意**：

| 压缩前的重要信息 | 替换后需要保留的含义 |
|---|---|
| 用户不允许改变公开接口 | 后续修改仍受这个约束 |
| 已修正偏移表达式 | 不必再次把同一修改当作未开始 |
| 参数校验尚未完成 | 不能仅凭第一页正确就结束 |
| 某些测试没成功启动 | 不能将“尝试运行”写成“已通过” |

具体压缩结果由相应实现和模型产生，上表不是 Codex 保证生成的固定字段。它帮助判断“分页已处理”为什么不足以支持继续工作。

```text
旧历史 → 准备压缩输入 → 生成替换材料
                            ↓
            替换历史并处理检查点与比较基线
                            ↓
              补回必要指令、环境和当前任务
                            ↓
                      继续模型请求
```

压缩流程包含前后钩子、替换历史和检查点元数据，普通路径与远端路径也随提供者能力而不同。[`compact.rs`][src-compact]中，`InitialContextInjection` 区分必要上下文何时补回：采样前或手动压缩可以使相关基线失效，让随后常规流程重新注入；轮次中途压缩则要直接把当前步骤需要的信息放回合适位置，不能等一个并不存在的新用户输入。

失败也要看发生位置：采样前的新输入尚未进入通常历史路径，核心需要专门保留；轮次中失败可能阻止继续采样；本轮完成后的压缩失败，不自动撤销已完成的任务结果。[源码：`run_turn` 的各阶段处理][src-turn]。

> ⚠️ **注意：结构一致不代表摘要语义无损。** 调用配对正确、历史能恢复，仍可能漏掉“不能改接口”。宿主保留事实与审核状态提供另一层支持，但不是所有任务细节都自动获得同样保护。

## 本篇小结

同一任务会发出多次请求，工具结果使下一次判断获得新依据。Codex 用运行历史组织过程，用 StepContext 固定单次请求的条件，再处理指令刷新、状态差异、调用配对、容量和压缩。模型输入、宿主状态、持久历史与外部现实各有职责。

## 🎯 面试怎么回答

**问：Codex 怎样管理长任务上下文？**

> 🎯 核心是把“持续历史”和“本次请求”分开。每次请求固定设置、环境与工具视图，再把必要历史和结果交给模型。长到需要压缩时，替换历史并补回继续任务所需的约束，而不是不断追加文本。正确性要同时检查结构配对和语义保留。

**追问：恢复历史为什么不代表任务已经恢复正确？**

> 🎯 历史说明记录过什么，文件和远端服务说明实际发生过什么。动作已完成但结果未记录时，两者可能不同；恢复后要先核对实际状态，再决定继续或重试。

## ⚠️ 易错点回顾

- ⚠️ **Turn 与一次采样混淆：** 先按调用—结果—再次请求数清步骤，一轮可以包含多次采样。
- ⚠️ **快照与权限混淆：** 原快照保留解释依据，动作仍需通过取消、审批和环境限制。
- ⚠️ **压缩与追加混淆：** 压缩产生替换历史；还要检查约束、未完成工作和比较基线。

## 自测：改变条件，再推导下一步

**任务一。** 请求 A 捕获 P1 与 T1；模型生成期间切到 P2。A 的调用按哪份视图解释？下一次请求用什么？旧调用是否必定执行？

<details>
<summary>提示</summary>

分别判断已经发送的内容、下一次准备的内容和实际执行许可。

</details>
<details>
<summary>答案与解释</summary>

A 保留原 StepContext，下一次可以捕获 P2 的新环境与目录。原快照不能倒改，但动作可以因取消、审批或环境约束被阻止；一致解释不等于必须执行。

</details>

**任务二。** 历史只有调用 `c7`，磁盘文件却已变化；规范化补出 `aborted`。它证明什么？恢复时至少检查什么？

<details>
<summary>答案与解释</summary>

它只修复可发送的调用—结果关系，不证明未发生修改。读取文件或差异确认实际改动，再核对可靠测试记录或运行相关测试，分别判断“改过”和“改对”。

</details>

**任务三。** 教学窗口 40,000 token，生成预留 8,000，安全余量 2,000，指令与工具占 7,000。历史与新结果可规划多少？容量足够能否继续沿用过时约定？

<details>
<summary>答案与解释</summary>

`40,000 − 8,000 − 2,000 − 7,000 = 23,000 token`。这是教学预算，实际按模型核验。容量只说明装得下，过时约定仍要更新。

</details>

## 知识回看与源码阅读

回看 [Coding 的 AI 修复过程](../../practice/coding/docs/09-ai-coding.md)，核对任务约定、失败与最小修改的关系；回看 [Agent 通用课程](../../curriculum/09-agent/README.md)，区分通用概念与产品命名。

| 阅读目的 | 固定源码入口 | 先找什么 |
|---|---|---|
| 两次请求怎样衔接 | [session/turn.rs][src-turn] | `run_turn` 中输入、`for_prompt`、采样与工具后续 |
| 哪些条件绑定在同一步 | [step_context.rs][src-step] | `StepContext`，对照本篇的三个字段 |
| 项目约定何时更新 | [agents_md_manager.rs][src-agents] | 刷新、缓存失效、校验与继承分支 |
| 历史与基线是什么 | [history.rs][src-history] | `ContextManager`、两个比较基线 |
| 缺结果怎样补结构 | [normalize.rs][src-normalize] | 调用配对、合成中止、稳定标识 |
| 压缩后补回什么 | [compact.rs][src-compact] | `InitialContextInjection` 与历史替换 |

[← 模块入口](README.md) · [下一篇：工具 →](03-tool-lifecycle.md)

[src-turn]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/session/turn.rs
[src-history]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/context_manager/history.rs
[src-agents]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/agents_md_manager.rs
[src-step]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/session/step_context.rs
[src-parallel]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/parallel.rs
[src-turn-context]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/session/turn_context.rs
[src-registry]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/tools/registry.rs
[src-normalize]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/context_manager/normalize.rs
[src-compact]: https://github.com/openai/codex/blob/67a709665ac7b50311b93e32612c9a8281684787/codex-rs/core/src/compact.rs


<a id="fixed-implementation-comparison"></a>
## 固定快照实现对照

以下保留产品实现选读中的原文片段，供对照具体字段与调用路径；片段内的“第几章”指 [Agent 通用课程](../../curriculum/09-agent/README.md)的对应章节。

Codex 片段固定于 `fc948f8c473e5d11e780ffcf1fd7f812a2020932`，与本篇主线的 `67a709665ac7b50311b93e32612c9a8281684787` 分开阅读，不跨快照拼接结论。

<a id="implementation-chapter-03"></a>
### 03｜Agent Loop：观察怎样改变下一步

同一问题的其他实现片段：[Claude Code · 01](../claude-code/01-context-lifecycle.md#implementation-chapter-03)。

<details>
<summary>固定源码实现片段</summary>

Codex App Server 对正在运行的 Turn 提供 `turn/steer`（追加引导输入），并用预期 Turn 标识避免把新输入送给已结束或被替换的一轮；`turn/interrupt`用于中断。固定源码的 `session/turn.rs`检查待处理输入，决定是否还有后续工作。这个接口语义不同于“开始第二个同时修改同一状态的执行”。

</details>

<details>
<summary>源码证据：Codex</summary>

固定 Codex 快照中，Context Compaction（上下文压缩） 相关代码直接引用：

```text
Session
StepContext
TurnContext
WorldState
EventMsg
```

Tool Router（路由器） 中 `ToolCall` 也携带 `call_id`，再构造带 Session / StepContext / CancellationToken 的 Invocation（调用实例）。

这说明成熟 Runtime 会显式区分：

```text
长期 Session
→ 当前 Turn
→ 当前 Step / Invocation
→ Event / Tool Call
```

而不是把一切折叠成 Chat History（历史记录）。

产品对照不能把同名词硬套教学树：Codex公开交互以Thread/Turn/Item表达，一次Turn可含多次推理和工具交互；Item的开始、增量、完成可以形成多个事件。

</details>

<details><summary>4. 一次 Codex Turn 可否读取文件三次？</summary>

可以。Turn 包含用户请求后的一段 Agent 工作，模型可多次请求工具。每个工具项目及其事件有各自身份；不能把三次调用解释成必然三个 Codex Turn。

</details>


<a id="implementation-chapter-08"></a>
### 08｜计划与停止：让每一步朝目标推进

同一问题的其他实现片段：[Claude Code · 04](../claude-code/04-engineering-evaluation.md#implementation-chapter-08)。

<details><summary>9. Codex update_plan返回确认，模型还能知道清单内容吗？</summary>

它刚提交的工具调用包含计划参数，历史中有这段信息；确认结果不必重复整个清单。不能从短确认推断计划丢了，也不能推断它被固定在System Prompt。

</details>


<a id="implementation-chapter-09"></a>
### 09｜上下文编排：模型这一刻到底收到什么

同一问题的其他实现片段：[Claude Code · 01](../claude-code/01-context-lifecycle.md#implementation-chapter-09)。

<details>
<summary>固定源码实现片段</summary>

### 固定源码路径：初始上下文、消息追加、工具说明、计划更新与压缩后重建

依据固定Codex的`session/mod.rs`和`session/turn.rs`，可以沿以下顺序理解，**不是声称所有开关都输出同一串文字**：

1. `build_initial_context_with_world_state`收集开发者指令、扩展提供的线程/当前轮信息和环境状态。按片段角色聚合，普通路径先形成开发者消息，再放需要单独保留的开发者片段和模式信息，然后形成上下文用户消息。Guardian等分支另有独立指令位置。
2. 初次进入或压缩后的新上下文窗口需要完整注入；日常执行通过上下文更新与参考状态生成必要变化，不应每步无条件重建全部前缀。
3. 用户输入、模型输出、函数调用与函数结果进入执行历史。`build_prompt`把历史投影作为`input`，工具来自`tool_router.model_visible_specs()`，`base_instructions`另行传入，输出约束也独立。最终API序列化还在供应商适配层。
4. `update_plan`调用参数本身写明计划，处理器发出`PlanUpdate`事件，回填确认；新计划更新继续走调用/结果链，不要求每次移到最前面。
5. 压缩会换一个历史视图。前轮/手动路径与当前轮中压缩的初始信息重注入不同，下一章给出完整过程。

你可以据此描述一条实在的链：**初始上下文与环境信息→追加用户/模型/工具项→选当前可见工具说明→独立基础指令→模型请求**。这比“系统、计划、记忆总是固定按某八个位置摆放”更接近该快照。

</details>


<a id="implementation-chapter-10"></a>
### 10｜上下文压缩：缩短输入以后，怎样继续做对

同一问题的其他实现片段：[Claude Code · 01](../claude-code/01-context-lifecycle.md#implementation-chapter-10) · [Codex · 04](04-engineering-evaluation.md#implementation-chapter-10)。

<details>
<summary>Codex `compact.rs` 给出的实现证据</summary>

### 固定源码：触发判定 → 摘要请求 → 替代历史 → 后续调用

**触发。** `session/turn.rs`在正常推理前检查是否需要自动压缩，推理后若仍需继续工具/输入循环，也会结合使用量检查。`session/context_window.rs`区分全窗口计数与扣除前缀的主体预算，还维护完整上下文上限；模型切换等路径有额外判定。因此不能写“Codex永远到90%就压缩”。手动请求另有独立入口。

**分支。** 该固定快照在`run_auto_compact`里按功能配置选择Token Budget（预算）管理、供应商支持的远端压缩或本地`compact.rs`。以下完整描述只针对本地摘要路径；远端输出与实现不能从本地提示推断。

**输入和提示。** `compact.rs`复制当前历史视图，加入压缩指令构造模型输入，基础指令单独提供，压缩请求不照搬正常工具执行循环。默认提示来自`codex-rs/prompts/templates/compact/prompt.md`，也允许配置覆盖。原文以“CONTEXT CHECKPOINT COMPACTION”标识这项交接任务。用中文概括，它要求为接替执行的模型写交接摘要，重点是：已做工作与决定、重要约束和偏好、剩余步骤、关键资料与引用，并要求简洁、有组织。它不是要求固定JSON Schema；局部小标题是结构化写作，不等于机器已校验字段。

**结果。** 本地路径提取助手返回的摘要字符串，添加summary prefix，并通过`build_compacted_history`组合选取的真实用户消息与摘要。源码有保留用户消息的预算上限；不能据此声称所有历史逐条不丢，也不能说输出就是原字段状态的无损备份。

**安装。** `replace_compacted_history`更新执行中的历史并记录压缩项，重新计算使用量。前轮/手动压缩使用`DoNotInject`，清掉初始上下文参考，使后续正常轮重新注入；轮中压缩使用`BeforeLastUserMessage`，把初始上下文放到最后真实用户消息之前，让摘要位于规定位置。两种路径不能画成同一个无条件顺序。

**失败。** 摘要请求本身过长时有移除旧项后再试的处理；短暂故障有有限退避。技术上能继续不代表摘要语义完整，仍需要长任务回归。此处没有承诺整个外部世界与替代历史构成原子事务。

</details>


<a id="implementation-chapter-20"></a>
### 20｜执行追踪：先定位卡在哪，再取需要的证据

同一问题的其他实现片段：[Codex · 04](04-engineering-evaluation.md#implementation-chapter-20)。

<details>
<summary>补充：Context Management 自己也需要 Observability</summary>

### Context Management 自己也需要 Observability

Codex `compact.rs` Source Index 已确认有 Compaction（上下文压缩） Analytics：

```text
trigger
reason
phase
status
context tokens
summary tokens
latency
```

这支持一个重要原则：

> **Context Management 不是黑盒 preprocessing，它本身也要被 Trace / Metric。**

例如可以看：

```text
compaction_rate
post_compaction_failure_rate
context_tokens_before/after
```

---

</details>

