# DeepSeek Harness｜读者优先修订与验证记录

[学习入口](../../products/agent/deepseek-harness/README.md) · [审计目录](README.md)

日期：2026-09-27。交付状态：**文件修改稿，未提交、未创建 PR、未合并。** 本记录不改写旧审计、来源准入规则或冻结统计。

## 1. 基线、范围与访问事实

| 对象 | 固定基线 | 收尾重新读取结果 |
|---|---|---|
| Handbook `main` | `41c42937c720517781cf29bd61566260766d7729` | 仍为同一提交 |
| 上游 `master` | `477b4f420553e8a52c2fbccc464d7561b239c443` | 仍为同一提交 |
| 上游包版本 | `0.1.7-rc.2` | 根据根 `package.json`，不是推测发布标签 |
| 课程原引用快照 | `ddefc45fbc7f8e46dd73185e68295696d1297887` | 仅用作旧稿背景，不与新源码混用 |

先通过 GitHub 连接器读取分支和目录，再按实际文件读取内容。上游默认分支是 `master`；`main` 的单次 404 已通过仓库元数据定位。容器因 DNS 限制无法克隆 GitHub，与连接器已经成功读取私有仓库是两件事。没有把本地克隆失败解释成权限失效，也未尝试改变权限。

目标目录原有 README 与四篇正文，没有独立的本模块 review、interview 或 labs 目录。本轮保留五个一级 Markdown 路径，新增一个嵌套实验目录和本记录，不扩写为 API 百科。未修改其他产品正文、市场证据、Canonical、冻结分析、历史快照或公共测试。

### 实际阅读范围

**连续完整阅读：** 目标 README 及 `01-context-lifecycle.md`、`02-memory-lifecycle.md`、`03-tool-lifecycle.md`、`04-engineering-evaluation.md` 全部正文。此前没有把搜索摘要或文档时间当作正文验收。

**入口、规范与质量参照：** 读取根入口、`products/README.md`、`products/agent/README.md`、`curriculum/README.md`、`curriculum/09-agent/README.md`、`guide/knowledge-map.md`、`references/agent/README.md`、`guide/project/README.md`、`guide/audits/README.md`；读取写作规范分段及学习路线相关部分。Coding 参照为其 README、`01-programming-fundamentals.md` 的 1–180 行和 `09-ai-coding.md` 的 1–220 行；继承具体输入、错误结果、规则推导和独立验证的组织方式，不声称阅读了整套 Coding 教材。

**前后关联与维护：** 阅读 Agent 通用第 04 章工具说明与校验的 1–115 行、第 13 章检查点与恢复的 1–160 行，确认最小前提与职责分工；读取 `guide/project/agent-reader-revision.md` 的可见前段、模块近期提交记录及仓库语义校验脚本。前置课程不是本轮全文修订范围；历史维护表的存在也不作为本轮 PASS。

**上游源码：** 完整回读主循环 `agent.ts`、Inbox、工具调度、恢复补全、格式目录生成源、检查点策略和子 Agent 创建/委派政策；工具注册表与 schema 按具体调用链读取相关区间。另读取架构、基础组合、压缩、项目规则、会话引用、持久化、MCP 记忆、MCP 客户端、Skill 与子 Agent 的相关官方说明。没有宣称逐文件阅读整个上游。旧新比较接口报告大量提交差异，但返回列表截断；它只说明快照变化大，不证明这些变化都已审查。

## 2. 内容处理：保留、精修、补充与归位

| 原有价值或问题 | 本轮处理 | 交付位置 |
|---|---|---|
| Context、Memory、Tool、Engineering 四个生命周期已有明确分工 | 保留文件与顺序，不为展示工作量重命名 | 模块 README 与四章 |
| 日志与 Surface、规则与记忆、结果与副作用的区分值得保留 | 用同一分页任务串起输入、状态、操作和结果 | 四章主线 |
| README 承担了过多正文说明，读者需要先背抽象名词 | 入口只保留最小对象模型、组合方式、路线与版本；细节回到主讲章 | README；01–04 |
| 大量短条目缺少因果关系，章末训练不完整 | 先说明问题，再解释谁做什么、何时生效及失败条件；增补可见 Q/🎯 回答、误区、任务式自测 | 四章 |
| 没有实验与实际验证层次 | 增加只读源码/环境门槛与真实上游实验任务；不复制一份假 Harness | `labs/` |
| 技术证据索引容易变成包名清单 | 引用贴近结论，章末按待核对问题列源码入口 | 四章源码索引 |
| 面经来源编号会打断学习过程 | 正文只讲机制；真实问法、知识去向和核验层次放到本记录 | 本记录 §4–5 |

### 关键技术修正与证据

| 需要修正或限定的结论 | 已写入的精确边界 | 主要证据 |
|---|---|---|
| 请求已经记入日志，等于模型收到 | 输入接纳、请求准备、日志提交、持久化、网络发送与远端结果分别判断 | [Agent Loop](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/agent-loop/src/agent.ts)、[检查点策略](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/session/session-checkpoint-policy/src/index.ts) |
| 重试就重新组装并重复加入用户消息 | 同一步保留组装结果；`firstAttempt` 只追加一次用户输入；重试不重新调用 `preStep()` | [主循环](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/agent-loop/src/agent.ts) |
| Inbox 只是进程内队列，或落盘即等于消息已被模型消费 | `agent/inbox/spliced` 可重建待处理状态，但领取与模型消息提交之间有独立边界 | [Inbox](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/agent-loop/src/inbox.ts) |
| 参数校验、审批和 guard 可任意排列 | 无损 JSON 物化与工具特定结构校验分开；`ask` 获批后仍检查 guard；`defineTool` 在业务函数前校验 | [工具注册表](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/tools/src/index.ts)、[defineTool](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/tools/src/schema.ts) |
| 禁用审批意味着自动放行 | `never` 拒绝需要审批的请求；不是自动批准，也不是禁止所有普通工具 | [审批](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/interaction/user-approval/README.md) |
| 工具返回被屏蔽就等于没有改动；只改展示就保护全部数据 | 后处理不能撤销已发生副作用；只改 `content` 可保留原 `value` | [结果处理链](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/tools/src/index.ts) |
| 定义超时数值就自动有截止时间 | `timeoutMs` 是声明，需超时策略包装器实施 | [工具层限制](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/tools/README.md) |
| 引用是实时共享记忆 | 同一捕获边界的不可变快照；预览与外置来自同一份捕获；过滤普通工具结果 | [会话引用](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/context/session-reference/README.md)、[投影](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/context/session-reference/src/projection.ts) |
| 持久化说明示意里的 V3 就是当前写格式 | 当前格式目录源码明确 `currentVersion: 4`；README 部分示意滞后，未据此否定新格式 | [实际生成源](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/session/session-format-catalog/src/generated.ts)、[存储说明](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/session/session-persistence-jsonl/README.md) |
| 恢复补齐调用/结果就保证业务成功且可盲重试 | 区分未启动、未知结果与可靠回执；合成结果只修复日志解释；外部状态另行核验 | [恢复规则](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/core/session/src/repair.ts) |
| fork 自动带走父任务当前轮的全部信息与全部权限 | 委派 fork 取已完成轮次前缀；子对象重新组合预设及自己的限制；显式任务约束与权限种子分别处理 | [fork](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/subagent/subagent-fork-in-process/README.md)、[child-agent.ts](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/subagent/subagent/src/child-agent.ts) |
| 一次性子任务释放后就不存在任何持久历史；所有并行子任务统一受容量 8 限制 | Session 与进程 Activation 分开；容量 8 针对特定 continuable 池，不包含所有 one-shot/外部提供方 | [子 Agent](https://github.com/deepseek-ai/deepseek-harness/blob/477b4f420553e8a52c2fbccc464d7561b239c443/packages/subagent/subagent/README.md) |

公式与单位也单独核对：上下文 Token、AGENTS 字节、裁剪字符、会话引用 JSON UTF-8 字节、溢出 Token 不能互换。正文 `128000/8000/65536` 与评测 `100 个任务、70→90` 均明确是教学假设，不伪装为真实生产测量。

## 3. 阅读主线与内容边界

第一章建立输入时机和本次请求；第二章据此区分哪些信息可以在下一次任务重新使用；第三章把“模型提出工具调用”追到权限、执行、结果与传播；第四章组合前三章，讨论中断后能相信什么、怎样核验真正完成。

必要前提在当前主线中直接解释：Session、Surface、规范值、作用域、Step、Turn、流结算、幂等风险等不只放在词表或答案里。深度来自实际机制，不来自给每个新包增加独立章节。

### 主体独立检查与迁移检查口径

验收时先隐藏章末面试回答、自测提示、答案与第二遍复习，只检查正文是否能够支持以下不同条件的判断。此检查是编辑者沿主线的推导检查，不是用户学习效果实验，也不把关键字出现当成理解证明。

| 新条件 | 必须从主线得到的依据 | 对应解释位置 |
|---|---|---|
| 输入刚入队就崩溃，与请求提交后崩溃不同 | 队列持久状态、领取、请求提交与远端接收有不同边界 | 01 输入与接纳；02 恢复；04 检查点 |
| 小窗口沿用 65,536 Token 余量 | 代入公式后预算非正，不能按普通压力继续；需要配置核对 | 01 压缩预算 |
| 源会话更正后，旧引用仍给出旧结论 | 快照不可变与外部记忆更新是不同机制 | 02 引用与冲突归属 |
| 批准通过但 guard 拒绝 | 真实执行顺序决定业务函数没有调用，不是写后回滚 | 03 执行链 |
| 只隐藏 content，程序仍输出秘密 | 规范值与可见文字双通道 | 03 结果传播 |
| 文件成功写入后丢失结果 | 结构修复不证明外部状态，先只读核验后续动作 | 04 恢复与核对 |
| 父当前轮约束没有进入 fork 种子 | 已完成轮次前缀与显式子任务输入不同 | 04 子任务历史 |
| 新格式不可读、旧格式可读 | 不允许静默退回更旧状态掩盖新事实 | 04 格式选择 |

## 4. 面经覆盖的三个层次

**第一层：正式库范围的检索。** 使用仓库代码搜索在 `market/interviews` 全范围检索 Agent，接口返回 35 个命中文件、`incomplete_results=false`；这表示文件命中，不是 35 个独立面经，也不是 35 个 Batch 全文已读。结合实际 Canonical 与新批次定位候选，未按旧 S279 上限截止检索。

**第二层：正式收录上下文回读。** 完整回读目标 Canonical 的 44 个 ACTIVE 项，并区分四个已移交项；正式原始条目完整回读 S240、S241、S242、S288、S292–S297，共 10 个流程。S241 与 S288 的不同轮次不重复算新流程。S240–S242 来自 Batch 19 的可见完整条目，其余来自 Batch 29、32–35；不把这些回读扩大成全库逐条审查。

明确检查了 S288 在旧编号下新增的 9 月 21 日二面：它影响读写授权、长任务方向、插件化及能力边界，但不增加独立来源数。S292–S297 包括同一候选人在不同公司的流程，按库内现有规则保留，不重算或冻结新统计。旧模块近期修改记录不能证明“上次面经审查到哪一个来源”；因此本轮不声称已经穷尽此前所有未审的新来源。

**第三层：外部原帖复核。** 本轮实际打开 S242、S296、S297 的原帖。S242 的主体问题可读取，关键故障与上下文追问仍可见；但页面作者显示为“可乐roue”，正式记录写“北巷南街”。未完成账户标识与更名历史追踪，不能擅自认定同一用户名变更，亦未修改受保护证据。S296 与 S297 打开返回错误，不能标成原帖全文复核通过。其他正式条目只完成库内回读，没有冒充本轮外部复核。

S242 原帖额外可见反问中的通用 Agent 加 Skill/编排层选型讨论；这里只登记给 Market 维护者检查的补充上下文，不增改正式条目或题数。

外部入口：[S242 原帖](https://www.nowcoder.com/feed/main/detail/bdebbb6088b6405e9eb2bd2c345acb6e)、[S296 原帖](https://www.nowcoder.com/feed/main/detail/97ee6dec31b14d12a1f800b709e21a4c)、[S297 原帖](https://www.nowcoder.com/discuss/932587389027962880)。正文技术结论只由产品源码和官方说明支撑，不由这些面经证明。

## 5. 已确认问题的知识去向

### 5.1 Canonical 归属核对

下表覆盖实际 Agent Canonical 的全部 ACTIVE 编号；表示本产品作为工程例证的去向，不是重新分配主责、重新计算来源频率或声称全部原帖复核完成。

| Canonical 编号 | 共性机制 | 本轮处理与位置 |
|---|---|---|
| 001、002、003、004 | Agent/Harness、循环、执行事件 | README 最小系统；01 输入、Turn/Step、视图；保留并精修 |
| 005、006、007 | 规划范式、停止、目标偏离 | 本产品只解释真实循环及约束注入、停止与验证；通用规划体系仍属 Agent 08，未补画不存在的规划器 |
| 008、009、010、011、012 | 请求组装、压缩正确性、大结果、缓存 | 01 主讲；03 结果外置；补单位与路由边界，不保证缓存命中 |
| 014、015、016、017 | 记忆架构、生命周期、纠错、隔离 | 02 解释规则/会话/引用/外部存储；自动提取、冲突合并、租户 ACL 不冒充本产品默认完整实现 |
| 018、019、020、021、022 | 工具生命周期、校验、失败、发现 | 03 主讲；04 重试边界与结构化结果提交；修正审批和 schema 顺序 |
| 023、024、025 | MCP、Skill 与其他扩展的边界、按需加载 | 03 真实 Skill 和 MCP 路径；协议全貌仍属通用 Agent 16–17 |
| 026、027、028、029 | 取消、恢复、权限、外部成功但本地写失败 | 03 取消与授权；04 检查点/修复/核验；补充关键安全边界 |
| 030、031、032 | 多 Agent、共享工作区、任务分派 | 04 真实子对象与释放；共享 Session 不等于共享文件隔离；通用拓扑与智能分派归 Agent 19、18 |
| 034、035、036 | 评测、数据集、代码验证 | 04 完成标准、轨迹、对照评测；labs 连续任务；不编造默认内置全套 Benchmark |
| 037 | 代码仓库理解、RAG/AST/LSP/grep 组合 | 保留“按证据定位文件”的桥梁；完整方法归 RAG 与 Agent 22，不在本模块扩写检索课程 |
| 038 | 容错与服务韧性 | 01 请求重试；03 MCP 连接代际；04 故障分层；跨服务策略归后端与系统设计 |
| 041 | 自进化与反馈循环 | 04 验证和评测建立必要证据；自动学习/上线并非本模块证明的默认能力，交通用 Agent 21 |
| 042、043、044 | 运行中追加要求、Trace/Replay、注入风险 | 01 输入时机；02 引用信任；03 结果/权限；04 轨迹；不能把回放当真实重执行 |
| 045、046、047、048 | 意图路由、A2A、自研选型、AI Coding | 真实入口与子能力作为对照；A2A 不能与内部委派混同；普适选型归 Agent 18–19、24；代码交付归 Coding 与 Agent 22 |

已移交编号 013、033、039、040 保持原归属：模型长上下文、网络传输、服务并发背压和分布式扩展，不因在产品中出现术语而重新收入主责。

### 5.2 正式原始问题逐组去向

编号严格按本轮回读的正式条目内部顺序；它们是问题范围，不是新增 Canonical 或来源数量。招聘动机等非知识问题也显式排除，不默默只挑容易补写的题。

| 正式来源及问题范围 | 从问题到能力 | 处理位置或移交 |
|---|---|---|
| S240：1、2、3、5–11 | 代码诊断、职责分离、请求/工具重试、上下文、并发与幂等、Trace、记忆隔离、检查点/子任务 | 01–04；通用租户隔离与副作用幂等仅作必要桥梁，不冒充默认产品实现 |
| S240：4、12–24 | Streaming 网络协议；RAG 摄取/切分/混合检索/融合/评测/金融证据；MySQL、网络、Top-K | 主讲交后端、RAG、MySQL、Coding；04 只保留证据与完成核验的共同边界 |
| S241：一面 1–5、7、9、13；二面 15–17、22 | 本地操作安全、能力扩展、安全失败、记忆冲突、工具生命周期、应用记忆、可观测、自研与源码证明 | README、02–04 与 labs；资源强隔离明确为部署职责 |
| S241：一面 6、8、10–12、14；二面 18–21 | 企业 QA、模型参数、Linux/Docker/TCP、Coding、RAG、FastAPI、K8s/Windows | 对应 RAG、LLM Foundation、后端、Coding/系统设计；未重写这些模块 |
| S242：1–17、19 | 多层协作约束、成本收益、工程底座、记忆与检查点、未知副作用、Skill 加载、新指令、评测与日志证据 | README 与 01–04；其中具体 Claude Code 源码归对应产品，不能用 DSH 实现代答 |
| S242：18、20–22 | 充值退款异步幂等；RAG 全链、异构切分、跨表关联 | 后端/RAG 主讲；04 用于说明跨系统副作用不是本地日志事务 |
| S288：一面 1–7、10–13；二面 1–4、9–10 | 写安全、Harness 与 API、扩展、自研、格式与业务约束、评测 Gate、长任务方向、插件职责 | README、03–04；未用 Skill 提示替代硬权限，未声称 Review Agent 可自证正确 |
| S288：一面 8–9、14；二面 5–8、11 | AI Native 平台产品/API/研发流程/规划、学习方法与职业问题 | 平台路线与组织流程交系统设计/项目实践；学习方法与职业问答不扩成本产品机制 |
| S292：1–6、7–9 | 招聘与协作；10 万 QPS 商品详情、缓存时效、最长回文 | 非技术招聘题排除；技术主讲属系统设计、Redis、Coding，无本模块新增正文 |
| S293：2–4 | Agent 架构、Skill 不遵从、何时需要更强约束 | README 与 03 权限/Skill，明确规则文字不等于强制执行 |
| S293：1、5–16 | 自我介绍；视频 OOM/并行/上传续传/清理；SQL 与全链性能；大数/堆/HashMap/一致性哈希 | 非技术题排除；后端/MySQL/Coding/系统设计负责，04 仅复用“节点快不等于端到端快”的评价原则 |
| S294：1–3、4–13、16 | 经历与分工；网络、OS、Go、MySQL、Redis、CSS/CORS/前端与防抖节流；恢复 IP | 经历题不扩写；技术归对应基础/实践模块，未在 DSH 重讲 |
| S294：14–15 | AI 协作真实收益与局限；问答功能的全栈/安全/体验 | 04 验证与评测可作例证；完整问答设计移交系统设计与 RAG |
| S295：1–6、14 | 动态知识质量、关系/向量存储、精准上下文、实际采纳、Milvus及后续自动化 | 02 说明默认记忆的界限，04 说明下游任务评价；主讲归 RAG、向量库和 Agent 21 |
| S295：7–13 | Plan/Action 精简后的能力损失、Skill 串联 Gate、质量—时延、组件/集成责任 | 04 同条件对照及约束验收；03 Skill 与工具职责；不把题设的 20–30 个百分点当生产结论 |
| S296：1–3、14–15 | 自我介绍、使用经历、框架与学习方法、岗位反问 | README 提供产品定位；非机制问题不新增章节 |
| S296：4–8、10–13 | Agent/Harness、Skill/MCP、数量膨胀、无框架上下文与记忆、Coding Agent、多 Agent | README、01–04；03 补目录成本与按需加载边界，而不是加工具清单 |
| S296：9 | Knowledge Base 建设经历 | RAG 主讲，不把会话引用误称知识库全文检索 |
| S297：1–3、11 | 项目目标、节点偏差、生成代码正确性、效果评价与责任 | 04 验证层与流程证据；具体知识检索归 RAG；经历问题不编造案例 |
| S297：4–10 | 数据漏斗与 Doris/Hive/ES、倒排索引、MQ 用户隔离/最近消息、Redis/MySQL持久一致性、重复消费、重连、SQL | 后端、Redis、MySQL、RAG/检索与系统设计；本模块只保留状态/副作用核验桥梁，不声称这些主体已补齐 |

## 6. 共享文件、并行安全与跨模块事项

收尾重读 `main` 后，仅为以下两行提供精确替换规则：`products/agent/README.md` 的 DeepSeek Harness 快照行，以及 `references/agent/README.md` 的同产品快照行。其他产品行、全局日期、冻结统计和旧记录都不改。章节路径和一级文件数量未变，不需要用旧总数增减全局派生数字。

交付中的 `prepare_diff.py` 只读取已有检出，核对目标五文件的基线 Git blob，并在仓库之外生成 staging 与真实 unified diff；共享行从调用时的现有内容作一次精确替换。目标文件漂移、共享行不唯一、新文件已存在或输出目录落在检出内都会拒绝。涉及文件还必须与调用时的 HEAD 一致，避免把其他对话尚未提交的修改带进本轮 diff；生成前再次核对 HEAD 和输入字节。它不执行 checkout/reset/commit/push，也不创建远端分支。原稿未在容器取得完整 Git 检出，因此未伪造完整旧新逐行 diff；本轮直接交付的是修改稿、语义差异及这套受保护的实际差异生成器。

**待其他范围处理的具体事项：**

- `curriculum/09-agent/README.md` §2，以及本轮为核实链接读取的 `curriculum/03-backend-engineering/README.md` 前 45 行，仍把 Backend 放在 MySQL/Redis 前，与已读取的全局知识地图“先 MySQL/Redis、后 Backend”不一致。本轮不顺手重写另一模块入口，也不声称全仓库路线一致性已完成。
- S242 原帖作者显示名差异与反问补充，交 Market 维护者追踪同账户证据；未改准入规则或来源快照。
- 跨租户认证、业务幂等键、数据库事务、网络重连和知识库质量的完整主讲在其他模块；上述登记不是声称接收模块已新增或通过验收。

## 7. 验证状态

本轮实际运行环境为 Python 3.13.5、Node 22.16.0，未安装 pnpm；Node 低于目标下限。没有取得可运行上游完整检出，也未配置真实模型或外部 MCP 服务。因此上游单元测试、产品端到端、真实模型/工具/记忆、跨系统与生产验证都属于**未执行**，不是跳过后通过。

可在当前环境完成的是稿件结构检查、正文与链接检查、本次交付脚本测试、公式核算以及本地 HTML 阅读预览。具体运行计数、异常和渲染结果以交付包 `validation/` 的机器输出与最终交付说明为准，不借用历史 PASS。本地 Chromium 预览不等于 GitHub 桌面端、GitHub 移动端或真实用户理解实验。

全仓库语义脚本已阅读，但没有在完整整合后的仓库执行；只检查了本模块仍为五个一级 Markdown 且 README 保留 `## 核心设计` 等相关结构要求，没有改测试或硬改预期。共享导航改动尚未进入 main，整体集成仍待明确发布授权后在最新检出核验。
