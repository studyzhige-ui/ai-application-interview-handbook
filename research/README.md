# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它负责为完整的 AI Application / Agent Engineer 知识体系提供一层**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目、哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**308 个**
- 来源编号：`S001–S308`
- 当前最大编号：`S308`
- 下一条正式来源：**`S309`**
- 正式 Batch：`batch-01.md` ～ `batch-16.md`
- 最新 Batch：[`interviews/batch-16.md`](interviews/batch-16.md)，新增 **8 个 HUMAN-A（S301–S308）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**仍未达到来源饱和，但已进入高去重成本阶段**

Batch 16 在分配编号前重新直接回读 `batch-01.md` ～ `batch-15.md` 全历史，并逐个核对候选 URL、公司 / 岗位 / 日期 / 轮次、作者、项目语义、独特题序和招聘时间线。严格清洗后仍确认 8 个独立 HUMAN-A，说明精确公司 / 作者 / 轮次搜索仍有增量；同时自动 AI 面、内容账号、答案版与复制链的占比继续上升。

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

岗位标题不是唯一依据。标题叫“后端开发”，但实际职责和整场面试明显围绕 Agent / RAG / LLM Service / AI Platform / Runtime，可以收录；反之，标题带 AI 但实际是 BI、传统推荐、广告排序、纯训练、CUDA、RLHF Infra、普通后端顺带问 AI Coding、AI 测试等，不进入正式样本。

---

## 4. 通过 Role Scope 后，整场技术问题全部保留

确认一场面试属于目标岗位 HUMAN-A 后，面试官实际问到的所有技术问题都保留，包括：

```text
Python / FastAPI / Backend Engineering
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
- 不同候选人的独立招聘流程即使遇到相同常见问题 → 分别计为独立真人命中。

Batch 15 的写入前审查删除了 6 条重复 / 非独立候选；Batch 16 进一步把这套规则升级为真正的全历史直接回读：本轮在搜索新来源后，重新逐个检查 `batch-01.md` ～ `batch-15.md`，并把快手 AI 全栈同一作者的一面 / 二面合并为一个 `S305`。同作者字节 `S301` 与淘天 `S308` 因公司、时间和招聘流程不同，按独立真人命中分别计数。

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

技术关键词轮换：Python、FastAPI、asyncio、MySQL、Redis、Kafka、MQ、Vector DB、Milvus、PGVector、HNSW、IVF、RAG、Embedding、Rerank、RRF、MCP、Skill、Tool、Memory、Context、Harness、Runtime、Checkpoint、Resume、Cancel、Permission、Sandbox、Trace、Evaluation、Benchmark、Coding Agent、Claude Code、Codex、AI Coding、System Design。

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

## 7. Batch 16 的现实信号

1. **Agent Evaluation 正从结果指标升级为 Process / Benchmark Engineering。** 字节开始直接问从零设计 Defect-fix Benchmark；快手继续把 Routing、Tool、Document、Final Diagnosis 拆层评测，并追 Expected Output 是否经过 Domain Expert Review、Offline Case 是否代表线上真实故障。
2. **Skill vs Workflow 已进入 Production Governance。** 高合规场景中模型可能不遵循 Skill 文档，面试官会继续追 Hard Guarantee、Authentication / Authorization、Sensitive Context、SubAgent Isolation 和 Output Review。
3. **Python Foundation 是 AI Full-stack 的真实主线。** 阿里云同一场直接追 Function Parameters、`*args/**kwargs`、Duck Typing、Iterator / Generator、Slicing，再回到 Agent Generated Code Quality。
4. **AI Coding 从“会不会用工具”升级为现场交付与验证。** 快手直接要求做业务页面，淘天 Vibe Coding 追需求澄清；阿里云要求解释 Agent 生成代码如何验证与改进。
5. **业务思维成为 Agent 岗的独立能力。** 淘天明确区分 Business Agent Orchestration 与 Model Training，要求讲清每个 Agent 的职责、输入、输出和对应业务价值。
6. **经典 Backend / CS Foundation 权重没有下降。** MySQL、Redis、Distributed Lock、OOM、JMM、TCP/UDP、C Compilation / Linking、Topological Sort 继续与 Agent / Skill 同场。
7. **项目归属验真更直接。** 华为候选人坦言主要负责 Agent 外围服务而非 Core Implementation，但能清楚解释贡献边界；真实边界比包装“核心作者”更有研究价值。
8. **Provenance 成本继续上升。** 泛搜索中 AI 自动面、内容账号、完整答案 / 解析、后发复制明显增加。Batch 16 继续证明：宁可少收，也必须在 ID 分配之前完成跨 Batch 直接审查。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-15.md
│   └── batch-16.md
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

- 从 **`S309`** 开始；
- 新来源分配编号前继续直接回读 `S001–S308` 对应历史 Batch，不依赖代码搜索索引；
- 持续追 2026-09 最新 AI Application / Agent 原帖，优先直接正文而不是推荐 / 聚合页；
- 沿 Batch 16 新增候选人的作者主页继续寻找后续轮次，同公司同流程只合并不增号；
- 回扫 2026-03～09 尚未充分覆盖的公司和岗位别名；
- 重点补 Agent Benchmark / Evaluation：Task Construction、Process Metric、Failure Attribution、Domain Expert Review、Regression；
- 深挖 Skill / Workflow Governance：Hard Guarantee、Auth、Sensitive Context、SubAgent Isolation、Output Review；
- 继续补 Python / FastAPI / Async 与 Agent Runtime 同场的真人样本；
- 继续追 Context Runtime、Long-running Agent、Cancel / Checkpoint / Resume / Idempotence / State；
- 继续寻找 AI Backend / AI Full-stack 中 MySQL / Redis / MQ / Network / Concurrency / Coding 与 Agent 同场出现的真人样本；
- 牛客外继续主动搜索个人博客 / 独立站 / 稳定原始正文，不设置平台配额；
- 持续记录新增 HUMAN-A 绝对数与命中率、重复率、内容账号 / 二次整理率、Role Scope 外比例。

只有连续多轮扩大公司、岗位、月份、轮次、平台、作者页、企业 / 话题页和个人博客后，同时出现新增 HUMAN-A 持续接近 0、精确搜索也很难产生新样本、公司 / 岗位 / 轮次覆盖和 Python → Agent Harness 的问题深度分布趋于稳定，才判断接近来源饱和。
