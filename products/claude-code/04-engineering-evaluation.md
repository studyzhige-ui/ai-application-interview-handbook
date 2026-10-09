# 04. 恢复、协作与验证｜怎样证明长任务做对了

[← 工具](03-tool-lifecycle.md) · [模块入口](README.md) · [Agent 课程](../../curriculum/09-agent/README.md)

> 实现依据：本模块固定的私有源码快照。故障条件和耗时数字均为教学设定，不是产品实测成绩。

## 1. 把任务停在最容易误判的位置

分页源码已经改过，测试还在运行，用户关闭了界面。再次打开会话，模型说“我继续刚才的任务”。应该从哪里继续？

仅有聊天文本不够。程序需要知道有效历史在哪里、当前工作目录是什么、修改是否已经完成、测试结果还能不能取得。若把“没有收到结果”理解成“没有执行”，就可能重复操作；若把历史中的“测试通过”理解成当前文件通过，又会跳过必要验证。

前三篇分别说明了模型输入、记忆与工具执行。本章把它们合起来：**恢复工作条件，核对真实状态，再在同一份最终成果上验收。**

## 2. 恢复先找正确历史，再核对执行对象

镜像的消息使用 `uuid` 标识，用 `parentUuid` 表示接续关系。恢复时要选择有效链，不是把记录文件中的所有行依次拼起来。压缩摘要、历史裁剪和工具结果替换，都可能影响应该接回哪段历史。[会话存储][storage]

例如修改消息已持久化，测试只有“已启动”的进度。恢复时应该保留“文件已修改、验证待确认”，而不是补出一次从未记录的测试成功。

源码区分会话消息与临时进度：用户、助手、附件和系统消息可以参与持久历史；`progress` 主要用于临时显示。读取旧记录时仍保留跨过旧进度节点的兼容处理，所以停止某种写法不等于旧记录立即不可读。

恢复可以按三个对象分别进行：

| 步骤 | 本例要确认什么 | 得到的下一步条件 |
|---|---|---|
| 恢复有效历史 | 原约束、修改结果、尚未确认的测试 | 知道任务做到哪里 |
| 恢复执行环境 | 仓库、工作目录、工作树、代理和可用工具 | 知道接下来会操作哪份代码 |
| 核对真实状态 | 当前 diff、测试进程或输出、必要远端记录 | 决定继续等、重测还是修复 |

`sessionRestore.ts` 不只恢复消息，还处理文件历史、任务、代理、工作树和相关元数据；受功能控制的折叠状态也需在首次查询前恢复。[恢复入口][restore]

同一个 `src/pagination.py` 在两个目录里可以是不同文件。切换工作树后沿用旧目录的指令或缓存，可能让程序继续操作错误对象。恢复环境后重新核对实际文件，正是为了解决这个问题。

<details><summary>不同入口与文件历史的边界</summary>

交互式任务状态与部分非交互入口从旧 TodoWrite 消息恢复的路径不同，不能描述成统一的任务持久化策略。恢复记录需按实际入口解释。

文件历史快照可以帮助处理文件变更，不是整个系统的通用检查点。远端写入、后台进程、凭据等仍需要各自的查询与恢复办法。

</details>

## 3. 重试之前，先定位失败发生在哪一层

| 失败位置 | 已知事实 | 继续之前要确认什么 |
|---|---|---|
| 模型 API 没取得有效响应 | 模型通信失败 | 可否重试、剩余预算与等待条件 |
| 模型流开始后中断 | 部分工具可能已经启动 | 哪些动作发生过，怎样隔离旧结果 |
| MCP 认证或会话失效 | 连接条件出现问题 | 刷新认证、重建会话还是修正地址 |
| 工具返回业务错误 | 已取得一个错误结果 | 是否部分修改，应该换参数还是停止 |
| 工具可能成功但响应丢失 | 业务结果未知 | 查询真实状态，判断能否安全重复 |

模型 API 的分类与等待见 [`withRetry.ts`][retry]。前台用户等待与后台工作可以采用不同预算，容量错误与非法参数也需要不同处理。增加重试次数，只能帮助适合重试的故障，不能解决缺少授权或错误参数。

流失败后的旧执行器处理见 [工具篇](03-tool-lifecycle.md)：丢弃迟到结果防止消息混入新尝试，真实文件和外部写入仍需核对。

### 结果未知时，怎样决定是否重做

设远端工具创建了缺陷记录，但响应返回前断网。会话只有调用，没有成功结果。此时有三种合理去向：

1. 服务支持按业务唯一键查询：先查是否已经创建。
2. 服务提供可靠的幂等键语义：在有效范围内复用同一业务请求键。
3. 既不能确认，又不能安全重复：保留未知状态，取得必要人工判断。

Tool Call ID 用于配对模型调用与结果；只有远端服务将某个键持久地用于业务去重，才可能支持相应幂等。换一个调用标识再次创建，不会自动防重。这是从前述状态分层推导的工程处理原则，不声称镜像为所有服务实现了通用事务。

## 4. 子智能体怎样分工，哪些东西仍然共享

分页任务可以拆成定位缺陷、检查测试、审查接口三项子任务。子智能体有各自的任务输入与上下文，避免主任务携带每条探索细节；代价是额外模型调用、结果汇总与协调。

镜像通过 AgentTool 与 `runAgent.ts` 组织子任务并进入查询执行。复用 `query` 并不表示各自持有同一份完整消息，也不自动创建独立操作系统进程。[子任务入口][agent-tool] 与 [执行接入][run-agent]

| 边界 | 需要作出的明确安排 |
|---|---|
| 消息上下文 | 传给子任务哪些目标、约束和证据 |
| 执行权限 | 提供哪些工具，允许读取还是修改 |
| 工作文件 | 使用共同目录还是独立工作树 |
| 生命周期 | 谁收集结果，父任务取消后谁清理 |

给两个角色不同提示，只处理了消息输入的一部分，没有完成文件和安全隔离。

### Worktree 隔离工作副本，集成仍需共同验证

Git Worktree（工作树）为任务提供独立检出的目录，减少直接覆盖文件的机会；它不自动限制网络，也不替代权限沙箱。

假设 A 修改了分页参数，B 按旧参数补测试。两份补丁可以没有文本冲突，合在一起却不兼容。正确集成顺序是：确认共同基线，检查双方差异，合入同一最终状态，再运行接口与测试验证。**两个子任务各自通过，不等于合并后的结果通过。**

## 5. 后台任务和团队消息怎样走到完成

后台工具返回稳定任务标识，供后续查询、通知或取消。标识说明工作已登记，不说明成果已经可用；主任务仍要消费结果，失败时保留可诊断状态。

团队通信同样有阶段：发送、入队、接收、执行和返回结果。镜像的 `SendMessageTool` 负责路由到执行对象，接收者状态与相关能力条件影响后续工作。[团队消息入口][send-message]

例如审查子任务回复“准备检查接口”，主任务只能据此确认计划，不能宣布接口兼容。需要的是检查了哪些差异、发现什么，以及结论是否针对当前最终代码。

> ⚠️ 注意：清理工作树、进程或临时文件前，先确认归属、运行状态和结果位置。不能为了消除残留而删掉另一会话仍在使用的成果。

## 6. Trace 解释过程，Evaluation 判断结果

Trace（执行轨迹）关联模型请求、工具调用、状态变化与结果，回答“发生了什么”；Evaluation（评测）把结果和任务标准比较，回答“做得对不对”。

镜像有模型、工具、钩子耗时和失败事件等观察入口。例如工具执行层记录执行前钩子耗时，API 层记录缓存诊断信息。这些入口提供观察材料，但不自动构成完整端到端评测集。[工具观察入口][tool-execution] 与 [缓存诊断][cache-diagnosis]

| 证据 | 可以支持的判断 | 仍需其他证据的判断 |
|---|---|---|
| 调用及结果标识 | 哪次操作对应哪个结果 | 副作用是否只发生一次 |
| 最终 diff | 哪些文件与行改变了 | 修改是否符合业务语义 |
| 测试命令、目录、退出码与输出 | 实际运行了什么测试 | 未覆盖条件是否正确 |
| 压缩前后请求 | 约束是否进入后续输入 | 模型是否始终遵守约束 |
| 子任务记录 | 谁承担和返回了什么 | 集成后的共同结果是否正确 |

观察材料应足以判断当前问题，不必为了“可观测”收集所有敏感内容。需要保存哪些证据，还要服从任务、隐私和保留要求。

## 7. 把分页修复变成可检查的任务

本案例已有函数及原测试，页码从 1 开始，列表为 `[10, 20, 30]`，每页两个元素。要求公开参数与返回类型不变，不删除原测试。每次比较实验都从同一初始版本重新开始，不能让第二次实验直接使用第一次已经修好的代码。

| 检查项 | 操作 | 预期结果 |
|---|---|---|
| 正常分页 | 查询第 1、2、3 页 | `[10, 20]`、`[30]`、`[]` |
| 接口保持 | 比较函数签名与调用位置 | 未以改公开接口绕过缺陷 |
| 测试完整性 | 比较原测试与最终测试 | 有效断言未删除或削弱 |
| 真实执行 | 保存命令、目录与输出 | 能区分通过、失败、未运行 |
| 中断恢复 | 编辑后、验收前中断再恢复 | 先核查实际状态，再继续验证 |

前四项是基础案例，第五项增加恢复条件，不能由基础成功自动推出恢复成功。需要实现分页练习时使用 [AI Coding 章节](../../practice/coding/docs/09-ai-coding.md)，无需在产品解析中再维护一套相同算法。

### 一份有效记录要让证据指向同一对象

例如记录“初始提交 A；工作目录 W；最终 diff D；在 W 的最终状态执行命令 T，结果为 R”。字母只是记录角色，不是实际实验结果。关键是让被修改对象、被测试对象与交付对象一致。

测试通过后又改了文件，就需要重新判断原测试结果是否仍适用；在另一工作树测试通过，也不能直接覆盖本目录的验收。模型的解释可以帮助理解，不能替代这些对应关系。

即使最终测试偶然通过，过程中的越权操作仍违反任务条件。验收既看结果，也看不可违反的过程约束；多个 Skill 串联时，每阶段应有可检查交付，而非仅接收前一阶段“已完成”的自述。

## 8. 速度要沿关键路径计算，也要保持同一质量条件

以下是教学计算：第一次模型请求 900 毫秒，记忆检索 400 毫秒，后续工具 300 毫秒，第二次模型请求 700 毫秒，忽略其他开销。

串行执行为 `900 + 400 + 300 + 700 = 2300` 毫秒。若记忆检索与第一次请求同时开始，等二者完成再进行后续操作，则为：

```text
同时开始：模型请求 900 ms；记忆检索 400 ms
等待两者完成：max(900, 400) = 900 ms
随后执行：工具 300 ms，再请求模型 700 ms
总时间：900 + 300 + 700 = 1900 ms
```

减少的是本设定下 400 毫秒的等待，检索本身仍然做了。墙钟时间是从开始到结束实际经过的时间，并发各段的耗时不能直接相加。[记忆篇](02-memory-lifecycle.md) 中的机会性注入有自己的时序，不能将本计算假设套成真实产品的固定等待策略。

实际测量还要记录模型和工具消耗、后台工作、重试与验证成本。删掉测试可以变快，却改变了交付标准；少量案例也不足以证明代表性正确率或稳定的高分位延迟。完整评测设计回到 [Agent 评测课程](../../curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md)。

## 9. 验证做到哪一层，就报告哪一层

| 验证层 | 能确认什么 | 不能直接推广到什么 |
|---|---|---|
| 源码阅读与状态推演 | 可见分支在给定条件下的变化 | 镜像可构建、真实服务行为 |
| 语法或局部断言检查 | 该片段的语法与逻辑 | 整个生命周期运行 |
| 模拟故障 | 模拟依赖和故障下的行为 | 真实模型、网络和远端语义 |
| 真实产品单任务 | 指定版本与配置下的实际结果 | 其他环境或全部并发情况 |
| 跨系统与并发实验 | 所测组合的协调与恢复 | 任意规模和所有故障 |
| 生产观察 | 给定流量与窗口下的表现 | 尚未覆盖的未来条件 |

镜像的 `query/deps.ts` 提供模型调用、微压缩、自动压缩和 UUID 生成等有限可替换依赖。替换它们有利于测试对应分支，但工具、停止钩子、持久化和全部 I/O 并未因此一起隔离。[依赖入口][query-deps]

真实练习应使用独立、可丢弃的项目副本，记录 `claude --version`、入口、模型、权限、功能配置和初始提交，只授权必要范围。没有运行产品，就保留源码推演结论；不要借用他人工作树制造故障，也不要靠删除失败断言制造通过。

## 10. 第二遍从一张图重建整条任务

```text
任务与约束
  ↓
组织本轮输入 ← 按需读取记忆
  ↓
模型提出调用
  ↓
校验输入、处理改写、授权与调度
  ↓
改变真实文件或外部状态
  ↓
结果回填与持久记录
  ↓
中断时：恢复历史 → 恢复环境 → 核对真实状态
  ↓
在共同最终版本上验证
  ↓
交付结果、未确认事项与成本
```

图中每条关系都应能对应前文一个具体对象：哪条约束、哪份请求、哪个调用标识、哪个文件版本和哪次测试。源码学习的收获不是记住组件数量，而是可以沿这些对象找到状态第一次出错的位置。

通用数据库一致性、分布式消息投递和部署容量需要在后端与系统设计模块继续学习。这里的文件会话和恢复逻辑帮助建立问题意识，不替代那些系统的完整设计。

## 本章小结

恢复同时涉及历史、执行环境与真实副作用；多智能体还需明确消息、权限、工作文件和生命周期。最后将证据对齐到共同最终版本，分别验证结果、过程约束、恢复与成本，再说明实际完成到哪一层。

## 🎯 面试怎么回答

**问：Coding Agent 怎样从生成代码走到可靠交付？**

先确定任务、允许范围和验收规则。执行中区分模型输入、会话记录和真实副作用，中断后恢复环境并核对文件或远端状态。子任务要有明确的权限、工作树和结果归属，集成后在同一最终版本检查 diff、有效测试与过程约束。最后分别报告通过、失败和未运行，不把生成文本、任务入队或日志存在当作交付。

## ⚠️ 高频易错点

- 没有响应可以是结果未知，不能直接推导没有执行。
- 独立工作树不等于安全沙箱，各自通过也不等于集成通过。
- 任务已安排、消息已送达、结果已验收是不同阶段。
- 测试与被交付版本不一致时，原来的绿灯不能直接沿用。

## 本章自测

**任务一：换了工作树。** 子任务修改分页函数，主任务恢复后仍在原目录；报告只写“测试通过”，没有目录或提交。至少补查哪三项？

<details><summary>参考答案与解释</summary>

确认子任务工作树及基线、最终 diff、实际测试目录与对应代码版本，再在共同最终状态验证。测试可能针对旧目录，各自无文本冲突也不能证明接口兼容。

</details>

**任务二：并发数字。** 两个独立读取同时开始，各耗时 500、800 毫秒；随后编辑 200 毫秒，验证 600 毫秒，忽略其他开销。总时间是多少？

<details><summary>参考答案与解释</summary>

`max(500, 800) + 200 + 600 = 1600` 毫秒。删掉验证得到 1000 毫秒，但验收条件改变，不能直接声称同等质量下节省 600 毫秒。

</details>

**任务三：证据分级。** 只做了状态图推演、Markdown 检查和模拟工具测试，没有运行 Claude Code 或真实 MCP。怎样写验收结论？

<details><summary>参考答案与解释</summary>

报告固定快照、模拟条件及对应检查结果；明确未构建镜像、未运行真实产品、未验证真实 MCP 恢复或生产行为。局部通过不能合并成整个系统已全面验证。

</details>

## 知识回看与源码定位

- [会话存储][storage]、[恢复入口][restore]：分别核对保存与重新选择状态。
- [子任务入口][agent-tool]、[团队消息][send-message]：区分执行、路由和完成。
- [有限依赖替换][query-deps]、[Agent 评测课程](../../curriculum/09-agent/docs/21-EvaluationBenchmarkAndImprovement.md)：对齐测试边界与结论。

[回到 Claude Code 模块入口](README.md)

[storage]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionStorage.ts
[restore]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/sessionRestore.ts
[retry]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/withRetry.ts
[agent-tool]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/AgentTool.tsx
[run-agent]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/AgentTool/runAgent.ts
[send-message]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools/SendMessageTool/SendMessageTool.ts
[tool-execution]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/tools/toolExecution.ts
[cache-diagnosis]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/services/api/promptCacheBreakDetection.ts
[query-deps]: https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query/deps.ts


<a id="fixed-implementation-comparison"></a>
## 固定快照实现对照

以下保留产品实现选读中的原文片段，供对照具体字段与调用路径；片段内的“第几章”指 [Agent 通用课程](../../curriculum/09-agent/README.md)的对应章节。

Claude Code 片段固定于学习用私有镜像 `58231dcce408f805c645cfbc352d2876b517223b`；涉及 Codex 的对照片段使用 `fc948f8c473e5d11e780ffcf1fd7f812a2020932`，不代表当前产品发行版的共同默认行为。

<a id="implementation-chapter-01"></a>
### 01｜Agent 系统的全貌：模型之外，谁把任务做完

同一问题的其他实现片段：[Claude Code · 03](03-tool-lifecycle.md#implementation-chapter-01) · [Codex · 04](../codex/04-engineering-evaluation.md#implementation-chapter-01)。

<details>
<summary>固定源码实现片段</summary>

### 9.1 Claude Code：QueryEngine 明确拥有 Conversation Runtime

固定快照中的 `QueryEngine.ts` 直接写明：

- 一个 conversation 对应一个 `QueryEngine`；
- 每次 `submitMessage()` 开启一个新 turn；
- messages、file cache、usage 等状态跨 turn 保留；
- Runtime 配置中存在 tools、MCP clients、agents、`canUseTool`、`maxTurns`、`maxBudgetUsd`、fallback model 和 `AbortController`。

这说明成熟 Agent 产品不会把“会调用 Tool 的模型”当作全部 Runtime。

它还需要一个长期存在的 conversation execution object。

</details>


<a id="implementation-chapter-08"></a>
### 08｜计划与停止：让每一步朝目标推进

同一问题的其他实现片段：[Codex · 01](../codex/01-context-lifecycle.md#implementation-chapter-08)。

<details>
<summary>固定源码实现片段</summary>

Claude Code 固定源码索引里，`QueryEngine` 配置明确存在 `maxTurns`、`maxBudgetUsd`、`fallbackModel`、`abortController` 等边界。课程抽象因此是：

> **Budget 属于 Runtime 控制面，不只是 Provider（模型服务方） billing。**

</details>


<a id="implementation-chapter-12"></a>
### 12｜状态与持久化：程序怎样知道工作做到哪里

同一问题的其他实现片段：[Codex · 04](../codex/04-engineering-evaluation.md#implementation-chapter-12)。

<details>
<summary>固定源码实现片段</summary>

Claude Code用户快照的QueryEngine负责会话生命周期，`query.ts`有消息、工具上下文、重试/压缩跟踪等活动状态；`utils/sessionStorage.ts`承担记录路径。`compact.ts`通过边界和保留消息关系支持压缩后加载，而非序列化所有协程、网络连接和内存缓存。官方支持会话恢复，也不意味着恢复任意外部业务交易。

</details>


<a id="implementation-chapter-13"></a>
### 13｜检查点与恢复：保存之后、崩溃之前发生了什么

同一问题的其他实现片段：[Codex · 04](../codex/04-engineering-evaluation.md#implementation-chapter-13)。

<details>
<summary>固定源码实现片段</summary>

Claude Code Source Index 中 `Task.ts` 已确认有：

```text
pending / running / completed / failed / killed
start/end time
output file + offset
abort / kill semantics
```

这支持一个稳定抽象：

> **Task 应该是有身份、状态机、输出位置和终止语义的一等 Runtime 对象，而不是一个普通 async function。**

</details>


<a id="implementation-chapter-18"></a>
### 18｜路由与模型适配：换一条路径，不能丢掉任务保证

同一问题的其他实现片段：[Codex · 04](../codex/04-engineering-evaluation.md#implementation-chapter-18)。

<details>
<summary>固定源码实现片段</summary>

Claude Code用户快照QueryEngine配置包含fallbackModel，`query.ts`在流式fallback时处理旧尝试留下的助手项与工具结果，避免把孤立结果混进新尝试。这个实现提醒我们：模型切换不仅改名字，还涉及历史关联与已经执行的工作；不能从配置字段推断所有业务动作都能安全重跑。

</details>

<details>
<summary>补充：Claude Code 的实现信号</summary>

### Claude Code 的实现信号

固定 Source Index 确认 `QueryEngine` 配置存在：

```text
fallbackModel
```

这支持一个实现事实：

> 成熟 Runtime 会把 Model / Provider Failure 后的 fallback 纳入 Harness 控制面。

但具体 fallback 条件不能仅凭这一字段推断，本章只使用这个已核验边界。

---

</details>


<a id="implementation-chapter-19"></a>
### 19｜多 Agent 协作：交出去的是任务，不是全部控制权

<details>
<summary>固定源码实现片段</summary>

Claude用户固定`Task.ts`区分本地命令、本地/远程Agent等任务类型，维护状态和输出位置；这些是产品内部对象，不足以证明它们统一走A2A。Codex固定源码里的子Agent路径和上下文继承同样应按自己的运行时契约理解。

</details>

<details>
<summary>补充：Claude Code `Task.ts` 提供的实现信号</summary>

### Claude Code `Task.ts` 提供的实现信号

固定源码索引确认 Task 类型明确区分：

```text
local_bash
local_agent
remote_agent
in_process_teammate
local_workflow
monitor_mcp
dream
```

并且 Task state 包含：

```text
pending / running / completed / failed / killed
start/end time
output file + offset
abort / kill semantics
```

这直接支持课程抽象：

> Subagent / Background Task 应是有身份、状态机、输出位置、取消语义的一等 Runtime（运行时执行系统） 对象。

---

</details>

