# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它为 AI Application / Agent Engineer 知识体系提供**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目，以及哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**337 个**
- 来源编号：`S001–S337`
- 当前最大编号：`S337`
- 下一条正式来源：**`S338`**
- 正式 Batch：`batch-01.md` ～ `batch-20.md`
- 最新 Batch：[`interviews/batch-20.md`](interviews/batch-20.md)，新增 **6 个 HUMAN-A（S332–S337）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**尚未整体达到来源饱和。热门公司仍能找到新的独立 HUMAN-A，但普通热门结果页的历史重复、跨 URL 同场、换公司标题同序链、内容包装和正文不稳定比例已经很高。**

Batch 20 继续按“热门公司优先”搜索，最终只放行字节 / 抖音电商 2 个独立流程、快手 1 个、小红书 1 个、Bilibili 1 个、京东 1 个，共 6 个 HUMAN-A。分配编号前重新确认 `main` 为 `S001–S331` 基线，并直接回读相关历史 Batch 做 URL、作者、招聘流程、项目和连续题序对照。

本轮典型去重包括：OPPO 8/13 候选与历史 `S154` 几乎整段同序，因此不新增；小红书 OpenManus 候选与历史 `S260` 高度重合，排除；滴滴 AI Agent Backend 后半段与快手原场形成长连续同序链，排除；腾讯 4 月 AI Backend 虽技术密度高，但原始正文无法稳定完整打开，按 Verifiable Gate 排除；抖音电商同一作者一分钟附近发布两篇不同题序页面，流程关系无法确认，因此只收能独立成立的 Agent 全栈页面，另一页零贡献。

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
真实现场 / 招聘流程痕迹
+
目标 AI Application / Agent 岗位
+
正文稳定可核验
+
非转载 / 非合集 / 非内容账号 / 非重复
=
HUMAN-A
```

详细规则：

- [`quality/source-quality-policy.md`](quality/source-quality-policy.md)
- [`quality/role-scope-policy.md`](quality/role-scope-policy.md)

任意一项不满足，都不能进入正式 Batch，也不能贡献 Canonical Question、问题频率、知识优先级、课程内容或市场趋势统计。

平台一律平等。牛客、小红书、知乎、脉脉、CSDN、掘金、Bilibili、抖音、个人博客、独立站等公开来源都执行同一标准；平台只影响核验难度，不影响准入门槛。

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

岗位标题不是唯一依据。标题叫“后端开发”，但职责与整场面试明显围绕 Agent / RAG / LLM Service / AI Platform / Runtime，可以收录；反之，标题带 AI 但实际是 BI、传统推荐、广告排序、纯训练、CUDA、RLHF Infra、普通后端只顺带问 AI Coding、AI 测试等，不进入正式样本。

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

基础工程问题只能来自通过 Role Scope 的目标 AI 岗真人样本，不使用普通后端、数据分析、推荐算法等场次人为抬高频率。

Batch 20 再次体现这一原则：小红书 `S334` 一场 75 分钟面试大面积考 LRU、秒杀、RocketMQ、Redis、MVCC、Index、Deep Pagination，但后半场明确深问 Agent Architecture / Memory / RAG / Evaluation，因此整场基础问题全部保留。

---

## 5. 去重：必须在分配 `Sxxx` 之前完成

固定执行：

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

- GitHub Code Search / 搜索引擎“0 命中”不是未收录证明，必须直接读取历史 Batch。
- 新候选在编号前至少检查 URL、作者、公司、岗位、日期 / 轮次、项目关键词和 5～10 个独特题序特征。
- 同一候选人同一公司同一流程的一面 / 二面 / 三面 / Leader 面 → **合并为一个 `Sxxx`**。
- 同一候选人面试不同公司 → 若招聘流程独立，可以分别计数。
- 不同 URL 但题序、项目描述和措辞高度一致 → 必须继续追作者、发布时间和流程；不能因为 URL 不同就算新来源。
- 更早不同作者页面与候选帖几乎逐题同序、又无法证明独立场次 → 候选帖不入库。
- 无法确认复制链原始候选人 → **整条不确定链排除，不猜原帖。**
- 搜索摘要只负责发现；正文最终不能稳定打开 → 不进入正式来源。
- 不同候选人的独立招聘流程即使出现相同常见问题 → 分别计数。

Batch 20 的应用实例：Bilibili 8/11 + 8/13 同一作者连续两轮合并为 `S335`；快手原作者页面 `S333` 的招聘账号“帮转”页只作为转载证据；OPPO 8/13 跨 URL 页面与历史 `S154` 整段同序，直接排除；滴滴候选虽然公司不同，但后半段与 `S333` 快手连续同序，不按公司标题强行计新来源；抖音电商同作者相邻双帖流程归属不清，只收其中能独立成立的 `S336` 页面，另一页零贡献。

---

## 6. 搜索策略

持续执行：

```text
热门公司优先
×
岗位别名
×
月份
×
技术关键词
×
作者 Timeline / 原始正文
```

当前公司优先级：字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、拼多多、京东、滴滴、Bilibili、OPPO、vivo、小米等。高质量长尾公司仍可补充，但主要搜索预算继续优先热门公司。

重点月份：`2026-03` ～ `2026-09`，优先 `2026-08` ～ `2026-09` 秋招新流程。

岗位别名轮换：AI 应用开发、AI 应用研发、Agent 开发、智能体开发、大模型应用开发、LLM 应用、RAG 开发、AI 后端、Agent 后端、AI 全栈、Applied AI、FDE、Coding Agent、Agent Runtime、Agent Harness。

技术关键词轮换：Python、FastAPI、asyncio、Java、Spring、Go、MySQL、Redis、Kafka、MQ、Vector DB、Milvus、RAG、Embedding、Rerank、RRF、MCP、Skill、Tool、Memory、Context、Harness、Runtime、Checkpoint、Resume、Cancel、Permission、Sandbox、Trace、Evaluation、Benchmark、Coding Agent、Claude Code、Codex、AI Coding、System Design。

搜索不能停在结果页：

```text
搜索引擎 / 企业页 / 话题页
→ 精确公司 + 岗位 + 日期 / 轮次
→ 作者主页 / 候选人 Timeline
→ 原始正文 / 评论区
→ 跨平台同步 / 帮转 / 复制关系
→ 回到全部历史 Batch 做最终去重
```

---

## 7. Batch 20 的现实信号

1. **热门公司 AI 岗越来越强调先验真项目。** 快手 `S333` 开场直接确认项目是不是实习、是否上线、有没有真实用户和调用量，然后才进入 Memory / Context / Runtime。
2. **AI Backend 仍是 Backend + Agent 的一体化能力模型。** 小红书 `S334` 从 LRU、秒杀、RocketMQ、Redis、MVCC、Index、Deep Pagination 一直问到 Agent / RAG；京东 `S337` 同场考 MySQL、Redis Cluster、ReAct、SubAgent 和 Skill Trigger Reliability。
3. **Evaluation 从最终答案下钻到 Runtime 行为。** Bilibili `S335` 直接追 Deterministic Output Verification、Hook / Callback Validation 和 Bad Case Attribution。
4. **AI Coding 的考法持续工程化。** 字节 `S332` 追生成代码的质量保障与测试，不满足于“平时使用什么工具”；抖音 `S336` 继续追生成 Field / API Design 后怎样 Review / Verify。
5. **GraphRAG 必须证明实际增益。** 抖音 `S336` 追 Pure RAG Baseline、Metric、Judge Input，以及哪些 Query 真正适合 Graph DB。
6. **Context / Memory 与行为可靠性正在合流。** 快手追 Retrieval Conflict 和 Memory 分层，B站追 Compaction 后状态保真，京东直接问 Skill 是否能 100% 触发。
7. **热门公司 Provenance 成本继续升高。** 同场跨 URL、同作者一分钟双帖、换公司标题后大段同序、内容账号 / 付费包装均真实出现；热门公司优先必须继续配套严格作者 Timeline 与题序核验。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-19.md
│   └── batch-20.md
├── monitoring/
│   └── inbox.md
├── quality/
│   ├── source-quality-policy.md
│   └── role-scope-policy.md
└── questions/
    └── README.md
```

`interviews/` 是正式 HUMAN-A；`monitoring/inbox.md` 只保存已经满足 HUMAN-A、但尚未归入正式 Batch 的候选。普通线索、低质量帖子和待核验搜索摘要不进入 Inbox。

Canonical Question 的规则见 [`questions/README.md`](questions/README.md)：只允许由正式 HUMAN-A 产生证据。

---

## 9. 下一轮优先级

- 从 **`S338`** 开始；
- 继续以**热门公司优先**，重点补腾讯、美团、拼多多、滴滴、字节 / 抖音、快手、小红书、京东、B站，以及 OPPO / vivo / 小米；百度、阿里系继续追新轮次；
- 新来源分配编号前继续直接回读 `S001–S337` 对应历史 Batch，不依赖代码搜索索引；
- 继续追本批候选后续轮次：同候选人同公司同招聘流程只合并，不另增 `Sxxx`；
- 热门公司搜索优先使用“公司 + 岗位 + 日期 / 轮次 + 技术关键词 + 作者 Timeline”，减少热门结果页重复噪声；
- 深挖 Agent Runtime Verification：Hook / Callback、Trace、Deterministic Output、Tool Failure、Checkpoint / Resume / Idempotence；
- 深挖 Context / Memory Correctness：Conflict Resolution、Compaction Validation、Skill Trigger Reliability、Long-context Boundary；
- 继续补 GraphRAG / Hybrid Retrieval / Rerank / Evaluation / Judge / Citation 的真实指标验真；
- 继续补 Python / FastAPI / ASGI / asyncio、Java / Spring / Go、MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场的大厂样本；
- 对内容账号、答案帖、付费专栏、后发扩写、同作者相邻多帖和换公司标题同序链保持零容忍；
- 牛客外继续主动搜索小红书、知乎、脉脉、个人博客 / 独立站，但主要搜索预算仍优先热门公司；
- 持续记录热门公司新增率、历史重复率、复制链比例和正文稳定失败率，区分“热门结果面局部饱和”和“热门公司真实来源整体饱和”。

只有连续多轮对热门公司和跨平台原始来源做精确搜索后，新增 HUMAN-A 持续接近 0、作者 Timeline 也难以产生新独立流程，才判断热门公司来源真正接近饱和。