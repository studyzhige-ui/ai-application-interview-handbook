# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它负责为完整的 AI Application / Agent Engineer 知识体系提供一层**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目、哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**276 个**
- 来源编号：`S001–S276`
- 当前最大编号：`S276`
- 下一条正式来源：**`S277`**
- 正式 Batch：`batch-01.md` ～ `batch-13.md`
- 最新 Batch：[`interviews/batch-13.md`](interviews/batch-13.md)，新增 **12 个 HUMAN-A（S265–S276）**
- 存量流程修正：Batch 13 搜索中发现小红书 `S260` 同一候选人的 8 月 17 日二面，已合并回原来源，不新增来源数量
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**仍未达到来源饱和**

Batch 13 在已有 264 个正式样本后仍确认 12 个独立 HUMAN-A，并额外发现一个已收录候选人的真实后续轮次。泛搜索中的内容账号、付费答案、自动 AI 面、重复 / 改写链继续增加，但精确公司 / 岗位 / 轮次、作者主页和历史月份回扫仍有实际产出，因此不能停止。

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

## 5. 三层去重

每个候选固定执行：

```text
URL 精确去重
+
题序 / 项目语义去重
+
作者 / 招聘流程时间线去重
```

- 同一候选人的一面 / 二面 / 三面 / Leader 面属于同一招聘流程 → **合并为一个 `Sxxx`**，保留所有轮次真实问题；
- 不同 URL 但公司、岗位、问题顺序、项目描述和措辞高度一致 → 继续核验作者、发布时间、评论和流程；
- 无法确认复制链原始候选人 → **整条链排除，不猜原帖**；
- 不同候选人的独立招聘流程，即使遇到相同问题 → 分别计为独立真人命中。

当前典型案例：Batch 12 的 `S259` 合并同作者一面 + 三面；Batch 13 维护中把小红书 `S260` 的二面回写原来源；Batch 13 的小红书 AI 全栈 `S268` 合并同作者业务交叉面 + 二面。

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

技术关键词轮换：Python、FastAPI、asyncio、MySQL、Redis、Kafka、MQ、Vector DB、Milvus、PGVector、HNSW、IVF、RAG、Embedding、Rerank、RRF、MCP、Skill、Tool、Memory、Context、Harness、Runtime、Checkpoint、Resume、Permission、Trace、Evaluation、Coding Agent、Claude Code、Codex、AI Coding、System Design。

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
```

搜索摘要只负责发现线索。最终无法稳定核验正文、候选人本人和真人面试，就不能进入 HUMAN-A。

---

## 7. Batch 13 的现实信号

1. **Long-running Agent 已从“知道 Resume”升级成 Runtime Diagnosis。** 数小时 / 数天任务的 Checkpoint / Resume、异常 API 后续跑、原本 5 分钟任务突然变成 15–20 分钟如何定位，开始进入真人追问。
2. **Token / Cost Budget 正在变成 Backend Concurrency 题。** Rate Limit、Token Budget、并发预算预留、Streaming 过程中预算耗尽后的业务策略，被放进同一个系统设计语境。
3. **Vector Retrieval 追问明显加深。** IVF、HNSW、FAISS、PGVector、Bi-Encoder / Cross-Encoder、BM25、RRF、Rerank、Recall / Precision Trade-off 都已从目标岗位真人场次出现。
4. **项目验真继续量化。** Intent Accuracy、Evaluation Set、用户数 / 日会话、30min→5min、数据库“提升 20%”等指标都被继续追验证方法、数据来源和本人贡献。
5. **AI Coding 与 Harness / SDD / Product Engineering 开始汇合。** 面试不再只问用了什么 Coding Agent，而是问自研 Agent、Self-bootstrap、Spec、MVP、上线、测试与人工兜底。
6. **AI Full-stack 仍然是完整工程岗位。** Agent / RAG 与 Frontend Performance、Backend、数据库一致性、Vector DB、Evaluation、Production Trade-off 同场出现。
7. **作者时间线越来越重要。** 内容账号与付费“真人叙事”污染增加后，单页文风不足以证明真实性；跨轮次更新、历史招聘时间线与评论互动已经成为 HUMAN-A Gate 和三层去重的重要证据。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-12.md
│   └── batch-13.md
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

- 从 **`S277`** 开始；
- 持续追 2026-09 最新 AI Application / Agent 原帖；
- 沿 Batch 13 新增来源的作者主页继续寻找二 / 三面 / Leader 面，并按同候选人同流程合并；
- 回扫 2026-03～09 尚未充分覆盖的公司和岗位别名；
- 优先补 Long-running Agent / Checkpoint / Resume / State、Tool Permission / Sandbox / Trace / Evaluation、Token / Cost Budget、Retrieval Evaluation；
- 继续补 AI Backend / AI Full-stack 中 MySQL / Redis / MQ / Network / Concurrency / Coding 与 Agent 同场出现的真人样本；
- 继续主动搜索牛客之外的稳定原始正文，但不设置平台配额；
- 持续观察新增 HUMAN-A 绝对数与命中率、重复率、内容账号 / 二次整理率、Role Scope 外比例。

只有连续多轮扩大公司、岗位、月份、轮次、平台、作者页、企业 / 话题页和个人博客后，同时出现新增 HUMAN-A 持续接近 0、精确搜索也很难产生新样本、公司 / 岗位 / 轮次覆盖和 Python → Agent Harness 的问题深度分布趋于稳定，才判断接近来源饱和。
