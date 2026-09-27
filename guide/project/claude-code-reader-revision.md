# Claude Code 模块读者修订记录

[↑ 项目记录](README.md) · [Claude Code 学习入口](../../products/agent/claude-code/README.md)

本记录对应 2026-09-27 的 Claude Code 产品学习模块 reader-first 修订。发布采用独立分支 → Pull Request → main 的标准流程；具体 commit、PR 与 merge 标识以 GitHub 历史为准，不在教材正文中固化一次性发布状态。

## 基线与范围

| 对象 | 核验状态 |
|---|---|
| 起草时教材 main | `41c42937c720517781cf29bd61566260766d7729` |
| 首次发布前重新读取的 main | `157bc4bfaa34efdf611b8fa2f858d9123ad22c13` |
| 最终发布分支基线 | `82d6c6c4dbcbc26da925b938ea6c378c0489fe9e`；这是 Vector DB PR #20 合并后的 main |
| 并发检查 | 发布前 main 已前进，但 Claude Code 五个目标文件 blob SHA 与起草基线完全一致，因此没有目标文件冲突 |
| 源码镜像 | `studyzhige-ui/claude-code-source-private` |
| 固定源码快照 | `58231dcce408f805c645cfbc352d2876b517223b` |
| 官方发行映射 | 未建立该镜像 SHA 与某个官方发行号的一一映射 |
| 修改范围 | Claude Code README、四篇生命周期正文与本记录；项目记录索引只增加入口 |
| 保护范围 | Market 原始面经、Frozen Canonical、来源规则及其他课程/产品正文不在本轮改写范围 |

正文讲固定快照中实际可见的实现；公开文档只用于核对产品边界。源码中存在某个分支、构建包含它、配置启用、当前入口调用以及服务端支持，是不同事实。

## 实际阅读与证据范围

本轮连续阅读了目标目录的五个教学文件，并读取 Agent 产品入口、Agent 课程入口、References/Agent、项目记录规范、文档风格规范、学习路线和仓库语义验证器。阅读质量参照采用仓库中 reader-first 的 AI Coding 教学方式：从具体任务出发，先建立对象与状态，再解释失败、权衡和验证，而不是从内部类名与字段清单开始。

固定源码快照重点核验了以下路径及其相关调用范围：

- `query.ts`、`QueryEngine.ts`：查询循环、模型视图、压缩与结束条件。
- `services/api/claude.ts`：模型请求、延迟工具集合、缓存相关请求处理。
- `services/tools/toolExecution.ts`、`StreamingToolExecutor.ts`：校验、Hook、权限、执行、并发、取消和结果交付。
- `memdir/memdir.ts`、`findRelevantMemories.ts`、`services/extractMemories/extractMemories.ts`、`services/autoDream/autoDream.ts`：长期记忆写入、选择、后台提取与整理。
- `utils/attachments.ts`、`sessionStorage.ts`、`sessionRestore.ts`：附件注入、会话持久化与恢复。
- `services/mcp/client.ts`、`ToolSearchTool.ts`、Skill 与 AgentTool 相关路径：MCP、工具发现、Skill 与子任务边界。
- `query/deps.ts`：可替换依赖的实际范围。

这是一轮关键路径源码核验，不宣称对私有镜像做了逐文件全库审计。

## Reader-first 重构

原有四篇顺序继续保留：

1. Context Lifecycle
2. Memory Lifecycle
3. Tool Lifecycle
4. Engineering & Evaluation

保留顺序的原因是它与 Agent 产品总入口的 Context → Memory → Tool → Engineering/Evaluation 主线一致，问题主要在章节内部表达，而不是目录数量不足。

主要修订如下：

| 原问题 | 本轮处理 |
|---|---|
| README 与正文重复大量源码细节 | README 改为学习对象、核心设计、阅读顺序和使用方法，机制归正文 |
| 内部名词和字段出现早于问题 | 每篇都从同一个分页修复任务开始，让读者先看到为什么需要该机制 |
| Context、Transcript、真实文件状态混在一起 | 明确区分会话消息、本轮模型输入、持久记录和外部副作用 |
| 压缩机制像固定流水线 | 改为条件调用关系，明确“调用入口存在”不等于每轮执行 |
| Memory 容易被概括为 `CLAUDE.md` | 区分项目指令、会话记录、Session Memory、Auto Memory 与子智能体记忆 |
| Tool/Skill/MCP/Hook 像组件清单 | 改为发现 → 参数 → 校验 → Hook → 权限/批准 → 执行 → 结果 → 验收 |
| “取消/失败/恢复”容易被理解成自动回滚 | 明确取消等待、停止工作、撤销副作用是三个独立问题 |
| Multi-Agent 容易只讲“分工” | 增加上下文、权限、工作树、生命周期和共同最终状态的边界 |
| Evaluation 容易只看日志或测试绿灯 | 将 Trace 与 Evaluation 分开，并用相同初始条件构造可检查分页案例 |
| 教学数字容易被误解为产品指标 | 所有容量、耗时与准确率例子标明为教学条件，并写出单位和计算关系 |

## 关键技术事实与边界

### Context

- `query()` 进入 `queryLoop()` 后由循环推进多次模型请求，不能描述成每个工具结果都递归调用一次 `query()`。
- Tool Result Budget、History Snip、Microcompact、Context Collapse、Auto Compact 等路径有不同条件；源码中的调用位置不等于每轮固定执行。
- Prompt Cache 是稳定前缀的计算复用，不是回答缓存，也不是持久记忆。
- 压缩后不仅要保住自然语言摘要，还要保住恢复父链、工具发现状态等继续执行需要的结构化状态。

### Memory

- 固定快照中入口索引的 `MAX_ENTRYPOINT_BYTES = 25_000` 名称与实现并不完全一致：实际第二道判断使用 JavaScript 字符串 `.length` 与 `slice()`，不能按 UTF-8 字节数解释所有中文输入。
- `hasMemoryWritesSince()` 检查 assistant 的 Write/Edit `tool_use` 及路径；该判断本身没有配对确认工具成功结果。因此“出现写入调用”不能证明记忆已经持久化。
- 自动记忆辅助查询的写入范围受到限制，但读取范围并不等同于“只能读记忆目录”；不能把这条回调泛化成 OS 沙箱。
- Relevant Memory 是异步预取路径。搜索启动、文件被选中、正文被读取和内容进入某次模型请求是不同事件，不能用机会性预取承载必须在动作前生效的安全约束。
- Auto Dream 的锁/时间标记回退用于后续重试，不等于已经写入的记忆文件发生事务回滚。

### Tool / Skill / MCP

- 工具要区分程序工具池、本次 API 请求的定义集合与模型本轮真正可见的说明。
- 固定镜像的 ToolSearch 包含名称、前缀、`searchHint` 和关键词评分路径；不能把它自动写成向量检索或辅助 LLM。记忆相关文件选择则是另一种实现。
- 工具执行包含结构解析、工具语义校验、执行前 Hook、权限/批准和真实调用。Hook/权限阶段如果改写输入，需要继续追踪最终执行对象，不能因为早期校验发生过就默认所有规则已对新输入重验。
- Permission、Approval、Sandbox 是三层不同机制。内置 Read/Edit/Write 不能描述为统一转换成 Bash 后再经过同一个 shell sandbox；远端 MCP 也不会自动继承本地 OS 沙箱。
- `discard()` 主要阻止旧执行器结果继续正常交付，不是通用回滚。文件或远端写入若已发生，必须核对真实状态。
- MCP 会话恢复与认证恢复按具体错误信号处理。网络层恢复不能证明上一笔业务写入没有发生，也不提供通用 exactly-once 保证。
- Skill 组织“怎样做”，Tool/MCP 提供可执行能力。提高 Skill 文本优先级可能改善遵从，但不能替代程序权限和最终验收。

### Recovery / Multi-Agent / Evaluation

- 恢复需要同时处理有效历史、执行环境和真实世界状态。消息恢复成功不等于远端写入、后台进程、凭据或当前工作目录全部恢复正确。
- Worktree 能隔离工作副本，但不是安全沙箱；两个子任务各自测试通过也不能证明整合后的共同最终状态正确。
- 子任务“已安排”、团队消息“已发送/入队”和任务“已完成”是不同状态。
- Trace 用来解释发生了什么，Evaluation 用来判断结果是否符合任务标准。存在埋点不等于存在完整端到端评测，更不等于某个正确率已经被证明。
- `query/deps.ts` 暴露的是有限依赖注入范围，不能因此宣称所有 I/O、工具、Hook、持久化都已被测试替身隔离。

## 面经证据怎样使用

面经只用于确认招聘过程真正会追问哪些能力，不作为技术事实来源。本轮检索并回读了与 Claude Code/Agent Harness 高相关的正式收录，包括早期 S080–S088，以及近期 S292–S297 和 S288 的二面扩展。

这些证据主要强化了以下教学位置：

- S080–S088：Agent Loop、Context/Memory、Tool Security、Checkpoint、Sub-agent、Workflow、人类验收。
- S293：Skill 不遵守限制、规则优先级与端到端性能定位，映射到 Tool/Skill、权限和工程评测。
- S295：知识质量、Skill 质量门、Plan/Action 简化和效率/准确率取舍，映射到记忆质量、阶段验收和共同条件下的评测。
- S296：大量 Skill/MCP 的发现与上下文压力、无框架压缩/记忆和 Multi-Agent，映射到 ToolSearch、Context、Memory 与子任务边界。
- S297：节点准确率、代码质量与事实准确率分别验证，映射到 Trace/Evaluation 与端到端任务标准。
- S288 二面扩展：读写鉴权、用户确认、长任务 Plan 和插件化，映射到权限、任务循环和运行时边界。

本轮没有重新访问这些条目的外部原帖，因此不把“已正式收录”扩大成对原帖最新状态的再次认证。

## 验证

发布前的修改稿执行了独立验证：

- Markdown 结构、标题、表格、`details` 折叠与模块导航检查。
- 相对链接和已读取关联路径检查。
- 教学 Node/JavaScript 字符串长度样例与算式检查。
- Chromium 桌面和窄视口阅读预览，检查横向溢出与折叠交互。
- 独立临时 Git fixture 检查补丁保护逻辑，避免目标文件并发修改被静默覆盖。

这些验证支持文档结构与局部教学例子，不等价于：

- 构建私有 Claude Code 镜像；
- 运行真实 Claude Code；
- 连接真实 MCP 服务做断线/认证/幂等实验；
- 完整仓库 CI、全局入站链接或生产验证。

因此正文使用“源码可见”“教学推演”“真实实验需要记录版本与配置”等措辞，避免把源码阅读结果冒充产品运行结果。

## 发布与并行保护

发布前重新读取 main 后，发现仓库已从起草基线前进到 `157bc4bfaa34efdf611b8fa2f858d9123ad22c13`。逐个回读 Claude Code 五个目标文件，其 blob SHA 仍分别是：

- README：`904e675efa69e90ffdec13f54b6b8fe1be63f7ca`
- 01：`2b314db373f31a6f0476495941a1e312cc8b8aae`
- 02：`c6b3409e19218ebc7b4a25a8678047fabe797479`
- 03：`6a9f908432445cee332f67a1220d3f5c9e609ea0`
- 04：`1ad55a29dbc2cfb65b21745e30fc5d0b34259991`

第一次发布分支创建后，Vector DB PR #20 将 main 推进到 `82d6c6c4dbcbc26da925b938ea6c378c0489fe9e`；旧 PR #21 因而被放弃，并从该新 main 创建第二个发布分支。再次核对五个 Claude Code 目标 blob 仍未变化，随后只重放本模块文件、修订记录和共享索引的一行入口。PR #22 创建后，Redis 跨模块链接修复 PR #23 又将 main 推进到 `9e18541f9252103e5890c480467b9e46cb0a5cdb`；该提交不修改本模块目标文件。最终通过 PR 合并而不是直接移动 main 引用，使 GitHub 在当前 base 上完成整合，不覆盖这些并发成果。若未来继续修改此模块，仍必须重新读取当时最新 main，并再次进行目标文件级冲突检查，不能沿用本记录的 SHA 直接覆盖。
