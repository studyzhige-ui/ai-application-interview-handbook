# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它负责为完整的 AI Application / Agent Engineer 知识体系提供一层**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目、哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**325 个**
- 来源编号：`S001–S325`
- 当前最大编号：`S325`
- 下一条正式来源：**`S326`**
- 正式 Batch：`batch-01.md` ～ `batch-18.md`
- 最新 Batch：[`interviews/batch-18.md`](interviews/batch-18.md)，新增 **6 个 HUMAN-A（S320–S325）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**尚未整体达到来源饱和，但牛客热门 Agent 关键词已明显进入局部来源饱和；新增独立 HUMAN-A 越来越依赖长尾日期 / 冷门公司 / FDE 等岗位别名与作者 Timeline 深挖。**

Batch 18 在分配编号前重新直接回读 `batch-01.md` ～ `batch-17.md`，覆盖 `S001–S319` 全历史。最终只新增 6 个独立 HUMAN-A。去重阶段识别到：07-12 PDD 内推导流帖几乎逐题复制 07-07 Coding Agent 原帖，只保留更早且作者评论区可核验本人现场的原帖；07-14 字节 AI 应用开发候选与历史 `S229` 的连续题序高度重合，因此不新增；09-04 淘天 Agent 专栏候选存在内容账号属性且正文约 60% 被付费墙截断，无法完整核验，排除。新增难度和 Provenance 成本继续上升。

---

## 2. 唯一正式来源标准：HUMAN-A

正式来源必须同时满足：

```text
真人面试官
+
候选人本人第一人称
+
高信息密度
+
真实现场痕迹
+
目标 AI Application / Agent 岗位
+
正文稳定可核验
+
非转载 / 非合集 / 非重复
=
HUMAN-A
```

详细规则：

- [`quality/source-quality-policy.md`](quality/source-quality-policy.md)
- [`quality/role-scope-policy.md`](quality/role-scope-policy.md)

任意一项不满足，都不能进入正式 Batch，也不能贡献 Canonical Question、问题频率、知识优先级、课程内容或市场趋势统计。

平台一律平等。牛客、小红书、知乎、脉脉、CSDN、掘金、Bilibili、抖音、个人博客、独立站、GitHub Pages 或其他公开来源都执行同一标准；平台只影响核验难度，不影响准入门槛，也不设置平台配额。

---

## 3. Role Scope：只校准目标岗位

核心研究方向：

```text
AI 应用开发 / AI 应用研发
Agent / 智能体开发
大模型 / LLM Application
RAG / 知识库应用
AI Backend / Agent Backend
AI Full-stack
Agent Harness / Agent Runtime
Coding Agent
Applied AI Engineer / FDE
AI-Native Application Engineer
```

岗位标题不是唯一依据。标题叫“后端开发”，但实际职责和整场面试明显围绕 Agent / RAG / LLM Service / AI Platform / Runtime，可以收录；反之，标题带 AI 但实际是 BI、传统推荐、广告排序、纯训练、CUDA、RLHF Infra、普通后端只顺带问 AI Coding、AI 测试等，不进入正式样本。

---

## 4. 通过 Role Scope 后，整场技术问题全部保留

确认一场面试属于目标岗位 HUMAN-A 后，面试官实际问到的所有技术问题都保留，包括：

```text
Python / FastAPI / Backend Engineering
Java / Spring / Go
MySQL / Redis / Vector Database
LLM Foundation / RAG
Agent / MCP / Skill / Tool / Memory
Agent Harness / Runtime
System Design
OS / Network / Concurrency
MQ / Kafka
HTTP / SSE / WebSocket
Coding / Debug / Security / Evaluation
AI Coding
```

基础工程问题只能来自通过 Role Scope 的目标 AI 岗真人样本，不使用普通后端面经人为抬高 MySQL / Redis / Python 等频率。

---

## 5. 去重：必须在分配 `Sxxx` 之前完成

每个候选固定执行：

```text
历史 Batch 直接回读
+
URL 精确去重
+
公司 / 岗位 / 日期 / 轮次比对
+
题序 / 项目语义去重
+
作者 / 招聘流程时间线去重
+
外部原帖 / 后发复制链核验
```

### 强制规则

- **GitHub Code Search / 搜索引擎“0 命中”不是未收录证明。** 最近 Batch 可能尚未被代码搜索索引，必须直接读取历史 Batch 内容核验。
- 新候选在分配编号前，至少检查：URL、公司、岗位、日期 / 轮次、作者、项目关键词、5～10 个独特题序特征。
- 同一候选人的一面 / 二面 / 三面 / Leader 面属于同一公司同一招聘流程 → **合并为一个 `Sxxx`**，保留所有轮次真实问题。
- 同一候选人面试不同公司 → 属于独立招聘流程，可以分别计数。
- 不同 URL 但公司、岗位、问题顺序、项目描述和措辞高度一致 → 必须继续核验作者、发布时间、评论和流程；不能因为 URL 不同就算新来源。
- 如果发现更早不同作者页面与候选帖几乎逐题同序，而无法证明候选帖属于独立真人场次 → **候选帖不入库**。
- 无法确认复制链原始候选人 → **整条不确定链排除，不猜原帖**。
- 搜索摘要只能用于发现。**正文最终无法稳定打开，即使前期看过摘要或缓存，也不进入正式 Batch。**
- 不同候选人的独立招聘流程即使遇到相同常见问题 → 分别计为独立真人命中。

Batch 18 的实际应用：07-07 匿名 B 端 Coding Agent 原帖与 07-12 带 PDD 内推的后发页面几乎逐题同序，通过发布时间、原帖第一人称开场与作者评论区进一步确认复制关系，因此只保留原帖为 `S320`；07-14 字节 AI 应用候选虽然真人痕迹充分，但题序与历史 `S229` 高度重合，不因为发布时间更早就回改历史编号，而是按“历史 Batch 不修改”的纪律直接排除本轮候选；虾皮二面 `S325` 与历史 `S081` 同公司但作者、日期、轮次和题序都不同，确认是独立候选人流程，因此分别计数。

---

## 6. 搜索策略

持续执行：

```text
公司
×
岗位别名
×
月份
×
技术关键词
```

重点月份：`2026-03` ～ `2026-09`，同时持续追最新发布。

岗位别名轮换：AI应用开发、AI应用研发、Agent开发、智能体开发、大模型应用开发、LLM应用、RAG开发、AI后端、Agent后端、AI全栈、Applied AI、FDE、Coding Agent、Agent Runtime、Agent Harness。

技术关键词轮换：Python、FastAPI、asyncio、Java、Spring、Go、MySQL、Redis、Kafka、MQ、Vector DB、Milvus、PGVector、HNSW、IVF、RAG、Embedding、Rerank、RRF、MCP、Skill、Tool、Memory、Context、Harness、Runtime、Checkpoint、Resume、Cancel、Permission、Sandbox、Trace、Evaluation、Benchmark、Coding Agent、Claude Code、Codex、AI Coding、System Design。

搜索路径不能停在结果页：

```text
搜索引擎
→ 企业 / 话题页
→ 精确标题 / 公司 + 轮次
→ 作者主页 / 候选人其他帖子
→ 个人博客 / 独立站
→ 原始正文
→ 评论区
→ 跨平台同步关系
→ 回到全部历史 Batch 做最终去重
```

搜索摘要只负责发现线索。最终无法稳定核验正文、候选人本人和真人面试，或无法证明相对已有来源的独立性，就不能进入 HUMAN-A。

---

## 7. Batch 18 的现实信号

1. **Coding Agent 的 Context / Memory 正确性从“怎么压缩”升级为“怎么防污染”。** `S320` 连续追过时 File Summary、错误结论写入 Memory、重复状态、压缩后约束丢失与修复，说明 Memory Lifecycle 已经成为工程验真点。
2. **AI Coding 进入现场操作考察。** `S321` 不是问“会不会 Cursor”，而是现场打开真实项目，用 AI 修 Bug、生成背景 / Root Cause / Solution 并汇报，面试官直接观察候选人如何读代码、约束模型和验收输出。
3. **FDE / Applied AI 正向 Runtime State 与可靠性下钻。** `S324` 把三个并行 SubAgent、Supervisor Conflict Merge、Checkpointer、Human-in-the-loop Timeout、MySQL / Redis State Consistency、Resume 后 Model Switch 放在同一条题链中。
4. **FastAPI / Python 的底层要求在上升。** `S322` 从 Agent 前端协议追到 FastAPI / ASGI / Web Server 组件，并直接要求候选人用具体知识点证明 Python 深度；只会写 GET / POST 已不足以覆盖 AI Application Runtime。
5. **Agent 岗仍然把传统 Backend 当核心能力。** `S323` 在 RAG / LangGraph 后继续追 CORS、Authentication / Authorization、Spring Boot、Nacos、Linux、Monitoring 和 Monolith → Microservice；AI Application 不是“只会调模型”。
6. **Runtime / Framework 选型开始强调生命周期。** `S325` 直接问新轮子出现后如何判断旧方案是否淘汰、Retry 应放在哪一层，以及 AI-native Platform 如何从零设计，说明框架选型不再是 LangChain / LangGraph 名词比较。
7. **Provenance 噪声继续增加。** 本轮同时遇到后发逐题复制、内容账号付费墙、推广型“精品面经”、历史同序换公司标签和模板化元数据帖；“能搜到”与“能进库”的差距进一步扩大。
8. **热门搜索面正在局部饱和。** 仍能找到高质量来源，但新增主要来自 7–8 月长尾回扫、冷门公司、FDE / AI Application 别名和作者 Timeline，而不是 9 月热门 Agent 搜索结果第一页。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-17.md
│   └── batch-18.md
├── monitoring/
│   └── inbox.md
├── quality/
│   ├── source-quality-policy.md
│   └── role-scope-policy.md
└── questions/
    └── README.md
```

`interviews/` 是正式 HUMAN-A 样本；`monitoring/inbox.md` 只允许保存已经达到 HUMAN-A、但尚未归入正式 Batch 的候选。普通线索、低质量帖子和待核验搜索摘要不进入 Inbox。

Canonical Question 的规则见 [`questions/README.md`](questions/README.md)：只允许由正式 HUMAN-A 产生证据。

---

## 9. 下一轮优先级

- 从 **`S326`** 开始；
- 新来源分配编号前继续直接回读 `S001–S325` 对应历史 Batch，不依赖代码搜索索引；
- 持续追 2026-09 最新 AI Application / Agent 原帖，但不因热门新帖数量增加而放松复制链 / 内容账号 / 付费墙审查；
- 沿 Batch 18 和历史候选人的后续轮次继续追踪，同候选人同公司同流程只合并不增号；
- 回扫 2026-03～09 尚未充分覆盖的公司和岗位别名，重点增加 FDE / Applied AI / AI Full-stack / Agent Runtime 等长尾标签；
- 深挖 Coding Agent Context Correctness：Summary Validation、Stale Memory、Incorrect Fact Correction、Loop Detection、Patch Rollback、Repo-scale Planning；
- 深挖 Agent Runtime State：Checkpoint / Resume / Cancel / Human-in-the-loop Timeout / Model Switch / External Side-effect Idempotence；
- 继续补 Python / FastAPI / ASGI / asyncio 与 Agent Runtime 同场真人样本；
- 继续补 Tool / MCP / Skill 的 Permission、Audit、Sandbox 与 Error Recovery；
- 继续补 RAG Hybrid Retrieval / Rerank / Evaluation 以及真实指标验真；
- 继续寻找目标 AI 岗中 Java / Spring / Go / MySQL / Redis / MQ / Network / Concurrency / Coding 与 Agent 同场出现的真人样本；
- 牛客外继续主动搜索小红书、知乎、脉脉、个人博客 / 独立站等稳定原始正文，不设置平台配额；
- 持续记录新增 HUMAN-A 数量、重复率、内容账号 / 二次整理率、Role Scope 外比例和最终正文稳定核验失败率，区分“牛客热门关键词局部饱和”与“全网真实来源整体饱和”。

只有连续多轮扩大公司、岗位、月份、轮次、平台、作者页、企业 / 话题页和个人博客后，同时出现新增 HUMAN-A 持续接近 0、精确搜索也很难产生新样本、公司 / 岗位 / 轮次覆盖和 Python → Agent Harness 的问题深度分布趋于稳定，才判断整体接近来源饱和。