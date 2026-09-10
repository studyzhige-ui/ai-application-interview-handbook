# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它负责为完整的 AI Application / Agent Engineer 知识体系提供一层**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目、哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**319 个**
- 来源编号：`S001–S319`
- 当前最大编号：`S319`
- 下一条正式来源：**`S320`**
- 正式 Batch：`batch-01.md` ～ `batch-17.md`
- 最新 Batch：[`interviews/batch-17.md`](interviews/batch-17.md)，新增 **11 个 HUMAN-A（S309–S319）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**仍未达到来源饱和，但已进入高去重 / 高 Provenance 核验成本阶段**

Batch 17 在分配编号前重新直接回读 `batch-01.md` ～ `batch-16.md`，覆盖 `S001–S308` 全历史。随后逐个核验 URL、公司 / 岗位 / 日期 / 轮次、作者、项目语义、独特题序和招聘时间线。初筛中有一条“某中厂 Agent 应用开发实习”候选原本达到大部分门槛，但最终正文连续无法稳定访问，只能依赖搜索摘要，因此在编号前撤出；本批最终只保留 11 个可稳定核验的独立 HUMAN-A。

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

Batch 17 的实际应用：快手 AI 应用服务端 `8/26 → 9/1 → 9/9` 三轮合并为 `S318`；阿里灵犀互娱 `8/31 → 9/2 → 9/7 → 9/8 意向` 合并为 `S319`。两者虽然是同一作者、都提到 `CR Agent`，但公司、面试官、业务和招聘流程均独立，因此分别计数。初筛中的不稳定正文候选在编号前撤出，没有占用 `Sxxx`。

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

## 7. Batch 17 的现实信号

1. **Tool Calling 正升级为协议 / Runtime 本质题。** 启云方会连续追 Tool 注册、Structured Output、JSON / Content Block、Model 与 Executor 的边界，并要求手画 `Agent Loop → Model → Tool → Filesystem` 完整执行链。
2. **RAG 面试开始使用反例验真。** “生成小摘要为什么反而降低 Recall”“为什么只 Embed 标题”“512 Token 分流为什么形成不了检索闭环”“充分必要条件被 Chunk 切断怎么办”，都要求解释设计因果，而不是背标准 Pipeline。
3. **Skill vs Tool 继续向实现层下钻。** 面试官会追 Skill 是否真的能替代 Function Call、替代的究竟是哪一层，以及 Progressive Disclosure 如何减少 Context 占用。
4. **Agent Backend 的传统工程权重仍然极高。** 腾讯 / 杭州小厂即使岗位明确叫 Agent 开发，一面仍可能大面积考 Java / Spring / MySQL / Redis / Kafka / Network；滴滴 AI Agent Backend 更把 Spring、Redis、Go GMP、Service Discovery、GC 与 Agent Memory 放在一条完整题链中。
5. **Context Engineering 正从“长度治理”变成信息生命周期设计。** ReAct 上一轮结果如何传递、哪些状态进入下一轮、陌生 Repo 如何建立 Context、两个月后旧需求演进如何恢复历史知识，开始成为真人追问。
6. **AI Coding 正进入长期维护与能力验真。** 面试不仅看是否会 Cursor / Codex，还会问本人是否能独立写、陌生仓库如何上手、后续需求变化如何安全修改、Coding 过程与工程表达为什么不够好。
7. **Domain Agent 设计比通用架构更重要。** 灵犀互娱直接要求区分 Backend Agent 与 Game Agent，并把架构映射到真实游戏业务；目标、状态、动作、限制和 Evaluation 需要一起讲。
8. **多轮 Timeline 是高价值 Provenance。** 快手三轮和灵犀三轮 + 意向都能沿同一作者闭环，真实性证据明显强于孤立、标准化、无法串招聘过程的题单。
9. **稳定正文仍是硬 Gate。** 候选即使前期已进入强候选池，最终只能依赖 Search Snippet 时也必须撤出，不因数量目标降低标准。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-16.md
│   └── batch-17.md
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

- 从 **`S320`** 开始；
- 新来源分配编号前继续直接回读 `S001–S319` 对应历史 Batch，不依赖代码搜索索引；
- 持续追 2026-09 最新 AI Application / Agent 原帖，优先直接正文和作者 Timeline；
- 沿 Batch 17 新增候选人的后续轮次继续追踪，同公司同流程只合并不增号；
- 回扫 2026-03～09 尚未充分覆盖的公司和岗位别名；
- 深挖 Tool Calling / Agent Runtime：Structured Tool Call、Message / Content Block、Executor、Tool Result、Error / Retry；
- 深挖 RAG 反例：Chunk Semantic Boundary、Summary-induced Recall Loss、Embedding Strategy、Parent-child / Neighbor Expansion、Evaluation；
- 继续补 Skill / Tool / Function Call 的真实实现边界与 Progressive Disclosure；
- 继续补 Python / FastAPI / Async 与 Agent Runtime 同场真人样本；
- 继续追 Context Runtime、Long-running Agent、Cancel / Checkpoint / Resume / Idempotence / State；
- 继续寻找 AI Backend / AI Full-stack 中 Java / Spring / Go / MySQL / Redis / MQ / Network / Concurrency / Coding 与 Agent 同场出现的真人样本；
- 牛客外继续主动搜索个人博客 / 独立站 / 稳定原始正文，不设置平台配额；
- 持续记录新增 HUMAN-A 数量、重复率、内容账号 / 二次整理率、Role Scope 外比例和最终正文稳定核验失败率。

只有连续多轮扩大公司、岗位、月份、轮次、平台、作者页、企业 / 话题页和个人博客后，同时出现新增 HUMAN-A 持续接近 0、精确搜索也很难产生新样本、公司 / 岗位 / 轮次覆盖和 Python → Agent Harness 的问题深度分布趋于稳定，才判断接近来源饱和。
