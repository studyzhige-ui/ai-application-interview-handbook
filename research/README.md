# 2026 AI 应用 / Agent 面经研究

这里不是“面试题大全”，而是整套知识体系的 **招聘现实校准层**。

## 当前进度（2026-09-09）

- 已归档 `Sxxx` 来源记录：**63 个（S001–S063）**。
- 已形成规范化问题：**155 道 canonical questions**（按当前去重口径）。
- 当前仍处于“扩展召回”阶段，尚未认为样本饱和；后续会继续按 **平台 × 公司 × 岗位别名 × 技术关键词** 滚动搜索。
- 63 条来源记录 **不等于 63 场等权真实面试**：从 Batch 05 开始显式区分第一人称真实面经、低信息密度真实复盘、二次整理、面试题信号和待核实平台线索。
- 从 Batch 04 开始额外重点追踪 8 月下旬～9 月的新发布内容，并把持续监控发现的新来源先写入 `research/monitoring/inbox.md`，再定期归入正式 Batch。

> 上述数量是当前研究数据库的工作计数，不代表“2026 全互联网全部面经”。我们的目标是尽可能扩大公开可访问样本，并在新增 canonical question 增速显著下降时判断接近信息饱和。

## 研究目标

- 尽可能覆盖 2026 年公开可访问的 AI 应用开发、AI Agent 开发、RAG / LLM 应用、Applied AI 等相关面经。
- 保留“原始面经来源”和“规范化问题库”两层，避免去重后丢掉真实面试官的问法。
- 用真实问题反向检查 MySQL、Redis、Vector DB、RAG、Agent Harness 等系统课程是否有缺口。
- 扩展牛客之外的平台，降低单个平台在岗位、公司和题型上的采样偏差。

## 数据层次

### 1. Sources / Interviews

每份来源记录：

- source_id
- 平台
- 日期
- 公司
- 岗位
- 轮次（若已知）
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

- 一级模块：MySQL / Redis / Vector DB / RAG / Agent Harness / Python / Backend / LLM / System Design / Project
- 二级知识点
- 问题类型：Definition / Principle / Comparison / Debugging / Design / Project Deep Dive / Coding
- 深度：Basic / Intermediate / Advanced

## 来源类型与频率权重

### A. 原始 / 第一人称

候选人直接复盘真实面试。作为最终“公司实际问过什么”的最高权重证据。

### B. 第一人称 / 低信息密度

能确认是真实面试，但公开页面只有少量题目、面试结构或项目描述。可以证明某类能力被考察，但不从缺失正文中猜题。

### C. 整理 / 合集

二次整理、专题合集或跨多场聚合。用于扩大召回、发现原帖和提炼题型；如果能追到第一人称原帖，最终频率只计一次。

### D. 面试题信号 / 二次创作

例如短视频中的“面试官问你这个场景怎么办”、高频题讲解、模拟面试。它们可以暴露很有价值的 Production / System Design 边界，但不能证明某家公司真实问过，因此：

- 可以进入课程 Gap Analysis；
- 可以成为 canonical system-design question；
- **不增加真实面经频率**。

### E. 平台线索 / 待核实

典型是小红书：搜索引擎或第三方索引能够发现原标题，但公开直链依赖登录态 / 签名、正文不能稳定验证。只进入 `research/leads/`，找到稳定原帖后再升级为正式来源。

## 去重规则

1. **转载重复**：同一面经被重复搬运，只计一次。
2. **语义重复**：问法不同但核心问题相同，归并到同一 canonical question。
3. **同主题不同问题**：不合并。例如“Redis 为什么快？”与“Redis 为什么常用单线程执行命令？”属于相关但不同问题。
4. **来源权重**：第一人称原始面经优先；合集/整理页用于扩展召回和发现原帖，但最终频率统计时不与其原帖重复计数。
5. **跨平台同步**：同一作者把一场面试同步到牛客、小红书、CSDN、抖音，只算一个独立面试样本，其他 URL 作为关联来源。

## 搜索策略

持续组合以下关键词：

- AI Agent 开发 / Agent 开发 / 智能体开发
- AI 应用开发 / 大模型应用开发 / LLM 应用开发
- RAG 开发 / Applied AI / AIGC 应用 / AI 全栈 / AI 后端 / FDE
- 公司名 + 上述岗位名
- LangGraph / MCP / Skills / RAG / Redis / MySQL / Vector DB / Harness / Context Engineering / Coding Agent 等高价值术语

### 平台范围

不再局限于牛客，持续覆盖：

- 牛客
- 小红书（稳定原帖 + 标题线索池）
- 抖音
- Bilibili
- 知乎
- 脉脉的公开可索引内容
- CSDN / 博客园 / 掘金等技术社区
- GitHub 上的公开面经索引与题库（仅作为发现入口 / 参考资料，不能自动视为真实场次）
- 其他搜索引擎能够稳定索引和核实的公开来源

## 批次

- **Batch 01**：2026-09-09，建立搜索框架并收集第一批高密度样本，`S001–S015`。
- **Batch 02**：2026-09-09，补充 Tool Cache、Security、Trace、Checkpoint/Resume、Codebase Memory、Model Routing 等工程主题，`S016–S020`。
- **Batch 03**：2026-09-09，补充京东、滴滴、去哪儿、商汤、拓竹、华为等样本，并显著强化 MCP Lifecycle、Deterministic Replay、RAG Versioning、Hybrid Retrieval、MySQL/Redis/Backend 工程交叉问题，`S021–S034`。
- **Batch 04**：2026-09-09，重点补充 8 月下旬～9 月上旬的新鲜样本，新增 Long-running Agent Latency、Cancellation、Runtime Message Model、Codex/Claude Code 源码级追问、TB 级 RAG、可靠异步任务与 HotKey 等主题，`S035–S047`。
- **Batch 05**：2026-09-09，正式扩展到 CSDN、抖音、Bilibili 和小红书线索；新增 Context Compaction Lifecycle、Memory Retrieval Gating、Risk-based Approval、Goal Versioning、Tool Compensation、Cross-session Reconciliation、MCP Transport/Version、Agent Persistence Schema、RAG Retrieval Audit 等主题，`S048–S063`。小红书待核实标题单独存于 `research/leads/xiaohongshu-batch-05.md`。
