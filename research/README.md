# 2026 AI 应用 / Agent 面经研究

这里不是“面试题大全”，而是整套知识体系的 **招聘现实校准层**。

## 当前进度（2026-09-09）

- 已归档 `Sxxx` 来源记录：**128 个（S001–S128）**。
- 已形成规范化问题：**约 205 道 canonical questions**（按当前工作去重口径）。
- 当前仍处于“扩展召回 + 分层校准”阶段，**远未认为样本饱和**；后续继续按 **平台 × 公司 × 目标岗位别名 × 技术关键词** 滚动搜索。
- 从 Batch 06 起正式执行更严格的 **“宁缺毋滥”准入规则**：新增正式样本优先要求第一人称、元数据明确、技术问题具体；水短视频、SEO 答案博客、模拟题库和无法追溯原帖的拼接内容不进入正式频率统计。
- 从 Batch 07 起增加 **基础工程校准 Lane**：在继续寻找 Agent Harness / Runtime 深挖的同时，主动检查 Python、FastAPI、MySQL、Redis、MQ、并发等基础是否因搜索策略和 canonical 去重而被低估。
- 从 Batch 08 起新增 **Role Scope Gate**：正式样本必须服务于 AI Application / Agent 求职方向。传统数据分析 / BI、纯推荐算法、纯模型训练/Infra、以及与 AI 应用无实质关系的传统后端场次默认排除。
- Batch 09 开始明确出现 **应用工程深度的 LLM Foundation**：Transformer / Attention / Decoding / Token 与推理行为，但不滑向 CUDA、RLHF、分布式训练等训练 Infra 主线。
- Batch 10 继续把这一层推进到 **KV Cache / Inference Runtime**，同时新增 Agent Token/Cost Accounting、Agent 数据访问治理、Bi-Encoder vs Cross-Encoder、Redis Cluster 下 Lua 原子性边界等 Production 问题。
- 从 Batch 10 起开始记录 `interviewer_type` 信号。真人面试与自动化 AI 面试都可以提供岗位信息，但后续频率分析不应默认等权。
- 128 条来源记录 **不等于 128 场等权真实面试**：仍区分第一人称高置信、低信息密度真实复盘、整理/合集、面试题信号和待核实平台线索。
- 持续监控发现的新来源先写入 `research/monitoring/inbox.md`，再按质量与岗位范围门槛决定是否进入正式 Batch。

详细准入规则：

- [`quality/source-quality-policy.md`](./quality/source-quality-policy.md)：来源真实性 / 信息密度。
- [`quality/role-scope-policy.md`](./quality/role-scope-policy.md)：岗位是否属于我们的 AI Application / Agent 目标方向。

基础能力信号校准见：[`analysis/foundation-signal-after-batch-07.md`](./analysis/foundation-signal-after-batch-07.md)。

> 上述数量是当前研究数据库的工作计数，不代表“2026 全互联网全部面经”。我们的目标是尽可能扩大**高质量、可核验、且岗位方向正确**的公开样本，并在新增 canonical question 增速显著下降时判断接近信息饱和。

## 研究目标

- 尽可能覆盖 2026 年公开可访问的 AI 应用开发、AI Agent 开发、RAG / LLM 应用、Applied AI 等相关面经。
- 保留“原始面经来源”和“规范化问题库”两层，避免去重后丢掉真实面试官的问法。
- 用真实问题反向检查 Python、FastAPI、AI Backend、MySQL、Redis、Vector DB、RAG、Agent Harness 等系统课程是否有缺口。
- 扩展牛客之外的平台，降低单个平台在岗位、公司和题型上的采样偏差；但**跨平台不等于降低质量门槛**。
- 后续统计按岗位、轮次和 `interviewer_type` 分层，避免把 Agent Harness 二面、AI 应用一面、自动化 AI 面试混成一个失真的总频率。
- 基础知识频率只从通过 Role Scope Gate 的 AI 岗样本中统计，避免拿数据分析师或普通后端题库人为抬高 MySQL / Redis / Python 比例。

## 数据层次

### 1. Sources / Interviews

每份来源记录：

- source_id
- 平台
- 日期
- 公司
- 岗位
- 轮次（若已知）
- `interviewer_type`（若能确认：human / automated）
- 来源类型
- 原始链接或可搜索原标题
- 可访问状态
- 问题的简洁转述

第三方面经不整篇复制，只保存研究所需的事实性元数据与问题转述。

### 2. Canonical Questions

将语义等价问题归一化为 canonical question，例如：

- “上下文窗口满了怎么办？”
- “Context 超过限制怎么处理？”
- “Agent 长上下文如何压缩？”

可以归到“Agent 上下文接近/超过窗口限制时，如何设计压缩与保真机制？”，但仍保留来源与变体。

### 3. Taxonomy

问题至少标注：

- 一级模块：Python / FastAPI / Backend / MySQL / Redis / Vector DB / RAG / Agent Harness / LLM / System Design / Project
- 二级知识点
- 问题类型：Definition / Principle / Comparison / Debugging / Design / Project Deep Dive / Coding
- 深度：Basic / Intermediate / Advanced

## 来源类型与频率权重

### A. 原始 / 第一人称

候选人直接复盘真实面试。作为最终“公司实际问过什么”的最高权重证据。

### B. 第一人称 / 低信息密度

能确认是真实面试，但公开页面只有少量题目、面试结构，或属于自动化面试等需要单独分层的场次。可以证明某类能力被考察，但不从缺失正文中猜题，也不默认与高密度真人 A 级场次等权。

### C. 整理 / 合集

二次整理、专题合集或跨多场聚合。用于扩大召回、发现原帖和提炼题型；如果能追到第一人称原帖，最终频率只计一次。

### D. 面试题信号 / 二次创作

例如短视频中的“面试官问你这个场景怎么办”、高频题讲解、模拟面试。它们可以暴露有价值的 Production / System Design 边界，但不能证明某家公司真实问过，因此：

- 可以进入课程 Gap Analysis；
- 极少数独特问题可作为系统设计训练题；
- **不增加真实面经频率**；
- 从 Batch 06 开始，默认不会仅因为二次创作就新增大量 canonical question。

### E. 平台线索 / 待核实

典型是小红书：搜索引擎或第三方索引能够发现原标题，但公开直链依赖登录态 / 签名、正文不能稳定验证。只进入 `research/leads/`，找到稳定原帖、原作者同步帖或其他证据后再升级为正式来源。

## 去重规则

1. **转载重复**：同一面经被重复搬运，只计一次。
2. **语义重复**：问法不同但核心问题相同，归并到同一 canonical question。
3. **同主题不同问题**：不合并。例如“Redis 为什么快？”与“Redis 为什么常用单线程执行命令？”属于相关但不同问题。
4. **来源权重**：第一人称原始面经优先；合集/整理页用于扩展召回和发现原帖，但最终频率统计时不与其原帖重复计数。
5. **跨平台同步**：同一作者把一场面试同步到牛客、小红书、CSDN、抖音，只算一个独立面试样本，其他 URL 作为关联来源。
6. **来源质量优先于覆盖率**：不能稳定核验的高频标题，不因为“看起来很热门”就进入统计。
7. **岗位范围优先**：不是目标 AI Application / Agent 岗的题，即使技术上有价值，也不进入正式面试频率样本。
8. **面试官类型分层**：自动化 AI 面试与真人技术面单独标记，避免固定题库/自动生成追问影响真人面试频率结论。

## 搜索策略

持续组合以下关键词：

- AI Agent 开发 / Agent 开发 / 智能体开发
- AI 应用开发 / 大模型应用开发 / LLM 应用开发
- RAG 开发 / Applied AI / AIGC 应用 / AI 全栈 / AI 后端 / FDE
- Agent Harness / Runtime / Coding Agent
- 公司名 + 上述岗位名
- Python / FastAPI / LangGraph / MCP / Skills / RAG / Redis / MySQL / Vector DB / Harness / Context Engineering 等高价值术语

### 两条搜索 Lane

- **Lane A — Agent / Harness Frontier**：Harness、Runtime、Context、Memory、Tool、MCP、Security、Evaluation、Coding Agent、Claude Code、Codex。
- **Lane B — AI Application Foundation**：Python、FastAPI、MySQL、Redis、MQ、网络、异步、并发、缓存、数据库与系统设计。

两条 Lane 都只收高质量、可核验且通过 Role Scope Gate 的真实来源。这样既不会因为“只搜基础”错过新 Harness 能力，也不会因为“只搜 Harness”错误低估后端基础。

### 平台范围

不局限于牛客，持续覆盖：

- 牛客
- 小红书（稳定原帖 + 标题线索池）
- 抖音 / Bilibili（**只有第一人称、信息密度足够的内容才可能升级为正式来源；普通短视频直接过滤**）
- 知乎
- 脉脉的公开可索引内容
- CSDN / 博客园 / 掘金等技术社区（优先第一人称长篇复盘，过滤 SEO/标准答案文）
- GitHub 上的公开面经索引与题库（仅作为发现入口 / 参考资料，不能自动视为真实场次）
- 其他搜索引擎能够稳定索引和核实的公开来源

## 批次

- **Batch 01**：2026-09-09，建立搜索框架并收集第一批高密度样本，`S001–S015`。
- **Batch 02**：2026-09-09，补充 Tool Cache、Security、Trace、Checkpoint/Resume、Codebase Memory、Model Routing 等工程主题，`S016–S020`。
- **Batch 03**：2026-09-09，补充京东、滴滴、去哪儿、商汤、拓竹、华为等样本，并显著强化 MCP Lifecycle、Deterministic Replay、RAG Versioning、Hybrid Retrieval、MySQL/Redis/Backend 工程交叉问题，`S021–S034`。
- **Batch 04**：2026-09-09，重点补充 8 月下旬～9 月上旬的新鲜样本，新增 Long-running Agent Latency、Cancellation、Runtime Message Model、Codex/Claude Code 源码级追问、TB 级 RAG、可靠异步任务与 HotKey 等主题，`S035–S047`。
- **Batch 05**：2026-09-09，正式扩展到 CSDN、抖音、Bilibili 和小红书线索；新增 Context Compaction Lifecycle、Memory Retrieval Gating、Risk-based Approval、Goal Versioning、Tool Compensation、Cross-session Reconciliation、MCP Transport/Version、Agent Persistence Schema、RAG Retrieval Audit 等主题，`S048–S063`。小红书待核实标题单独存于 `research/leads/xiaohongshu-batch-05.md`。
- **Batch 06**：2026-09-09，切换到严格高置信准入；正式收录百度 Agent Harness/Agent、MINISO、小鹏、美团、懂车帝、字节、快手、腾讯 CSIG、法本信息、上海 Agent 初创等第一人称高密度样本，`S064–S076`。新增 Tool Executor、Memory/Skill Write Safety、Checkpoint Crash Window、Compaction 保真评测、Coding Repo Navigation、Agent Topology Governance、Observability Evidence Quality、Tool Result Compression、Coding Verification 等主题。
- **Batch 07**：2026-09-09，在保持 A 级来源门槛的前提下做基础能力校准，`S077–S086`。重点证明 Python/GIL/FastAPI、MySQL 索引/MVCC/慢查询、Redis ZSet/Cluster/HotKey/一致性仍大量出现在 AI Agent / AI 应用真实面试中，并新建 Python canonical questions 与多层缓存一致性等问题。
- **Batch 08**：2026-09-09，加入 Role Scope Gate 后的第一批全链路样本，`S087–S100`。全部来自 AI 应用 / Agent / AI 全栈 / AI 后端目标岗位，新增 FastAPI Middleware vs DI、ASGI Runtime、asyncio Fan-out、Python 混合并发、Vector DB 多租户数据组织、私有化 RAG、人评一致性、AI 技术选型、AI Application Version Bundle、A2A Loop Prevention 与 Harness Self-improvement Governance 等问题。
- **Batch 09**：2026-09-09，继续按目标岗位扩展整条能力链，`S101–S114`。新增 LLM Foundation 应用深度、RAG Knowledge Gap / Corpus Data Audit、`AGENTS.md` / Project Rules、Execution Truth、Pre-prod/Canary/A-B Release Validation、Transcript vs Working Context、Bounded Concurrency 等问题。
- **Batch 10**：2026-09-09，继续收录目标 AI 应用 / Agent / AI 后端全链路样本，`S115–S128`。新增 KV Cache 应用层理解、Bi-Encoder vs Cross-Encoder、层级 Agent Token/Cost Accounting、Agent Database Access Boundary、Redis Cluster 下 Lua/多 Key 原子性边界，并引入 `interviewer_type` 分层信号。