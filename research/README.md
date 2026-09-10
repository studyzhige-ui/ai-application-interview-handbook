# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它负责为完整的 AI Application / Agent Engineer 知识体系提供一层**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目、哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**300 个**
- 来源编号：`S001–S300`
- 当前最大编号：`S300`
- 下一条正式来源：**`S301`**
- 正式 Batch：`batch-01.md` ～ `batch-15.md`
- 最新 Batch：[`interviews/batch-15.md`](interviews/batch-15.md)，新增 **8 个 HUMAN-A（S293–S300）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**仍未达到来源饱和，但去重成本明显上升**

Batch 15 在分配编号前对候选做了更严格的跨 Batch 去重：原始候选中先删除 6 条已入库 / 高度重复 / 无法证明独立原场的来源，仅保留 8 个独立 HUMAN-A，再连续编号为 `S293–S300`。今后不再把 GitHub Code Search 或搜索引擎“0 命中”视为去重完成，必须直接回读历史 Batch 并核对 URL、题序、项目语义、作者与招聘时间线。

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

Batch 15 的写入前审查实际删除了 6 条候选：拼多多 7/25 已存在历史 `S061`；京东 5/7 与历史 `S217` 题序 / 语义高度一致；Moka 4/27 与历史 `S208` 高度一致；字节 8/6 URL 已入库；影石 3/11 已是 `S220`；米哈游 4/24 又发现更早不同作者、几乎逐题同序的 4/9 页面，因此不作为独立原场进入。

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

技术关键词轮换：Python、FastAPI、asyncio、MySQL、Redis、Kafka、MQ、Vector DB、Milvus、PGVector、HNSW、IVF、RAG、Embedding、Rerank、RRF、MCP、Skill、Tool、Memory、Context、Harness、Runtime、Checkpoint、Resume、Cancel、Permission、Sandbox、Trace、Evaluation、Coding Agent、Claude Code、Codex、AI Coding、System Design。

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

## 7. Batch 15 的现实信号

1. **Context 已经从“超窗怎么办”升级成显式 Runtime Data Structure。** 面试会逐层问 System Prompt、Memory、Chat History、Tool Result、Retrieval Evidence 各放哪里、顺序如何、何时压缩、怎样回填。
2. **RAG 与 Agent 原生文件 / Repository Search 的边界开始被直接挑战。** 面试官会问“大 Context 已很强，为什么不让 Agent 直接用文件搜索 / grep”，要求从索引、搜索空间、可控性、Latency、Evaluation 等维度回答，而不只是 Token Cost。
3. **TB 级垂直 RAG 已进入 System Design。** 600GB–1TB PDF、扫描件 / 电子件混合解析、跨页语义、Hybrid Retrieval、Embedding 初始化与增量成本成为真人追问。
4. **Context / Memory 与 Security 正在融合。** Red-team Agent、可修改 Skill / Role / Knowledge、Tool Result 注入位置等问题要求同时理解 Context Governance 与攻击面。
5. **AI Coding 继续作为本人能力验真。** AI 连续改坏代码怎样恢复、怎样通过 Test / Review / Sandbox / Spec 保证质量、候选人是否理解并能验证生成结果，越来越重要。
6. **指标必须可审计。** Accuracy、Regression、RRF 参数、Latency 降幅、真实用户量、节约人力、数据规模都要说明 Baseline、Dataset、测量方法和 Failure Case。
7. **AI 岗 Backend 深度没有下降。** Kafka、Distributed Lock、OOM、MySQL Index、HTTP/2/3、V8、Go Concurrency 继续和 Agent / RAG 同场出现。
8. **Provenance / 去重本身已经成为研究质量基础设施。** 本轮原始候选 14 条最终只保留 8 条；以后宁可少收，也不能让重复来源占用编号或影响频率统计。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-14.md
│   └── batch-15.md
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

- 从 **`S301`** 开始；
- **在搜索新来源前先建立 `S001–S300` 的直接去重基线**，至少覆盖 URL、公司 / 岗位 / 日期、作者和独特题序；
- 新来源在分配编号前必须直接回读历史 Batch，不依赖代码搜索索引；
- 持续追 2026-09 最新 AI Application / Agent 原帖，优先直接正文而不是推荐 / 聚合页；
- 沿 Batch 15 新增来源作者主页继续寻找后续轮次，同公司同流程只合并不增号；
- 回扫 2026-03～09 尚未充分覆盖的公司和岗位别名；
- 深挖 Context Runtime、Long-running Agent、Cancel / Checkpoint / Resume / Idempotence / State；
- 继续深挖 Tool Registry / Retrieval / Lazy Loading、Permission / Sandbox、Trace / Evaluation；
- 继续寻找 AI Backend / AI Full-stack 中 MySQL / Redis / MQ / Network / Concurrency / Coding 与 Agent 同场出现的真人样本；
- 牛客外继续主动搜索个人博客 / 独立站 / 稳定原始正文，不设置平台配额；
- 持续记录新增 HUMAN-A 绝对数与命中率、重复率、内容账号 / 二次整理率、Role Scope 外比例。

只有连续多轮扩大公司、岗位、月份、轮次、平台、作者页、企业 / 话题页和个人博客后，同时出现新增 HUMAN-A 持续接近 0、精确搜索也很难产生新样本、公司 / 岗位 / 轮次覆盖和 Python → Agent Harness 的问题深度分布趋于稳定，才判断接近来源饱和。
