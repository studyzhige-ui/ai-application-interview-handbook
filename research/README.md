# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，而是用 **HUMAN-A 真人高质量第一人称面经**校准 AI Application / Agent Engineer 的真实面试市场：公司实际问什么、追到多深、怎样验真项目，以及哪些能力要求 Coding / Debug / System Design / AI Coding。

> **完整知识体系决定应该学什么；HUMAN-A 面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 最终主动采集基线

- 正式 HUMAN-A 来源：**279 个**
- 来源编号：`S001–S279`
- 当前最大编号：`S279`
- 若未来人为重开采集，下一条保留编号：**`S280`**
- 正式 Batch：`batch-01.md` ～ `batch-26.md`
- 最新 / 最终主动搜索 Batch：[`interviews/batch-26.md`](interviews/batch-26.md)，全库去重后本批保留 **5 个 HUMAN-A（S275–S279）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 主动搜索状态：**已按 2026-09-10 的收官要求结束。**

Batch 26 是最终一次扩大搜索量的主动扫描：只看 **2026 年大公司**，重新直接回读 `batch-01.md` ～ `batch-25.md`、覆盖 `S001–S274` 全历史后，再系统搜索字节 / 抖音、阿里 / 阿里云 / 蚂蚁、腾讯、美团、快手、小红书、百度、拼多多、京东、滴滴、Bilibili、OPPO、vivo、小米等公司，并主动覆盖牛客、小红书、知乎、脉脉、个人博客、独立站、技术社区与企业面经页。搜索阶段曾放行 6 个候选流程；全库去重后，阿里云 4/22 后端 AI 开发与更早已收来源为同一场，已并回最早 canonical，因此 Batch 26 最终保留 5 个来源：百度 AI 应用工程师、蚂蚁国际 AI 应用开发，以及 3 个不同候选人的快手大模型应用 / AI 应用服务端流程。

当前停止判断：**8～9 月大厂热门结果层已经高度局部饱和，3～7 月仍可能理论上存在残余长尾，但主动搜索的边际收益已经显著低于 Provenance / 去重成本。** 本项目因此按用户决定冻结主动采集基线；这不是宣称公开互联网已被数学意义上完全穷尽。

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
非转载 / 非合集 / 非内容账号 / 非答案帖 / 非重复
=
HUMAN-A
```

详细规则：

- [`quality/source-quality-policy.md`](quality/source-quality-policy.md)
- [`quality/role-scope-policy.md`](quality/role-scope-policy.md)

**平台一视同仁。** 牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客、独立站与技术社区都可以成为来源；平台只影响核验难度，不影响准入标准，也不存在平台配额。搜索索引、二次转载和 Search Snippet 只用于寻找原始 HUMAN-A，不能单独贡献题目。

---

## 3. Role Scope

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

岗位标题不是唯一依据。标题叫 Backend，只要岗位职责和整场招聘流程明确属于 Agent / RAG / LLM Service / Runtime，可以进入；反之，普通 Backend / Frontend / SRE 仅顺带问候选人的 Agent 项目、但岗位本身无法确认属于目标方向时，不收。

最终批次继续体现这一边界：阿里云 `S254` 标题是后端 AI 开发，但 Agent Code Execution、RAG Knowledge Permission、Tool Security 是明确考察主体；快手 `S278` 明确是 AI 应用服务端开发，即使 Redis Cluster、MQ 与 Java 占据较高权重，也仍属于目标 AI Backend / Application 工程样本。

---

## 4. 通过 Role Scope 后，整场真实技术问题全部保留

确认是一场目标 AI 岗 HUMAN-A 后，真实出现的基础和 AI 技术问题都保留：

```text
Python / FastAPI / ASGI / asyncio
Java / Spring / Go / JavaScript / React
MySQL / Redis / Vector Database
LLM Foundation / RAG
Agent / MCP / Skill / Tool / Memory
Agent Harness / Runtime
System Design
OS / Network / Concurrency
MQ / Kafka / RabbitMQ / RocketMQ
HTTP / SSE / WebSocket
Coding / Debug / Security / Evaluation
AI Coding / Vibe Coding
```

不使用普通 Backend、普通 Frontend、数据分析、推荐 / 广告算法、纯训练 Infra 等 Role Scope 外场次人为抬高基础题频率；但目标 Agent / AI Backend 场次真实考到的工程基础必须保留。

---

## 5. 去重：任何未来新增都必须先直接回读全历史

固定执行：

```text
全部历史 Batch 直接回读
+
URL 精确去重
+
公司 / 岗位 / 日期 / 轮次比对
+
题序 / 项目语义去重
+
作者 / 招聘流程 Timeline 去重
+
外部原帖 / 后发复制链 / 跨平台镜像核验
```

强制规则：

- GitHub Code Search / 搜索引擎“0 命中”只能辅助，不能证明未收录；
- 每个候选至少检查 URL、作者、公司、岗位、日期 / 轮次、项目关键词和 5～10 个独特连续题序；
- 同一候选人同一公司同一招聘流程的一面 / 二面 / 三面 / Leader 面必须合并为一个 `Sxxx`；
- 同一候选人不同公司 / BU、招聘流程独立时可以分别计数；
- 不同 URL / 不同平台但题序 / 项目语义高度一致时必须继续追源；
- 作者是真人也不能自动证明每一篇帖子都是本人原场；
- 无法确认复制链原场时整链排除；
- 搜索摘要、公开索引只负责发现，正文最终不能稳定核验则零贡献；
- 不同候选人的独立流程即使出现相同常见问题，仍分别计数。

最终批次的典型去重：一条 3 月 18 日快手“大模型应用”强候选最终被追到更早的 3 月 5 日原始一面，连续 20+ 道题从 Knowledge QA、Function Calling、Execute Plan、Redis Lua、ThreadPool 到百万 / 千万商品 Knowledge Base 基本同序，因此后发页排除，只保留更早且能由同作者串起 3/5 一面、3/9 二面与 OC 的 `S277`。这再次证明“新 URL + 高技术密度”远远不足以证明独立来源。

---

## 6. 已完成的主动搜索方法

本项目主动采集阶段最终采用：

```text
大公司优先
×
岗位别名
×
2026 最新层 + 历史长尾
×
多平台主动召回
×
技术关键词
×
作者 Timeline / 原始正文
×
跨年份复制链反查
```

重点公司：字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、拼多多、京东、滴滴、Bilibili、OPPO、vivo、小米等。

重点时间层：

- **最新层：2026-08～09**，秋招新增和后续轮次；
- **历史补漏层：2026-03～07**，大厂长尾与作者 Timeline；
- 最终收官批次额外按 2026 全年大公司范围扩大检索，不以热门第一页作为停止条件。

平台层主动搜索过牛客、小红书、知乎、脉脉、Bilibili、抖音、CSDN、博客园、掘金、个人博客、独立站和公开技术社区。最终非牛客正式新增仍为零，主要原因是原始正文、作者归属或转载链无法满足 Gate，而不是未主动搜索。

---

## 7. 收官后的研究判断

1. **8～9 月大厂热门结果层高度局部饱和。** 最新搜索中历史重复、内容账号、付费答案、后发扩写、同场多 URL 和 Role Scope 模糊内容占比很高。
2. **3～7 月长尾仍曾持续贡献增量。** Batch 25 的 4 条全部来自 3～6 月；最终 Batch 26 的 6 条中，4 条来自 3～4 月，说明“热门第一页饱和”不等于全年历史来源绝对搜尽。
3. **Provenance / 去重成本已经成为主要成本。** 搜索到新页面并不难，难的是证明“这是候选人本人、这是原场、这不是后发复制、这不是同一招聘流程的另一页”。
4. **AI Application / Agent 与传统工程底座深度耦合。** 最终批次同时出现 Retrieval / Memory / Tool / Agent Benchmark 与 Fair Queue、Redis、Kafka、RabbitMQ、Java ThreadPool、Container / Web Security 等真实同场考察。
5. **AI Coding 正从工具偏好变成现场交付验证。** `S279` 明确要求在约 30 分钟内使用 AI 完成浏览器插件；面试更关注能否把 AI 生成结果收敛成可交付产物。
6. **主动采集在此结束。** 当前 `S001–S279` 作为研究基线进入冻结状态。未来若因新的研究目标人为重开，不从旧搜索摘要直接续号，而应先重新读取当前 README、Inbox、质量规则和 `batch-01.md` ～ `batch-26.md` 全历史，再从保留编号 `S380` 开始。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-25.md
│   └── batch-26.md
├── monitoring/
│   └── inbox.md
├── quality/
│   ├── source-quality-policy.md
│   └── role-scope-policy.md
└── questions/
    └── README.md
```

`interviews/` 是正式 HUMAN-A；`monitoring/inbox.md` 只保存已经满足 HUMAN-A、但尚未归入正式 Batch 的候选。普通线索、低质量帖子和待核验摘要不进入 Inbox。

Canonical Question 只允许由正式 HUMAN-A 产生证据。

---

## 9. 冻结状态 / 未来若重开

当前不再安排下一轮主动搜索。若未来人为重开采集：

- 保留下一编号 `S380`；
- 先直接回读 `S001–S279` 全历史，而不是相信 Code Search 0 命中；
- 继续执行完全相同的 HUMAN-A 与 Role Scope Gate；
- 同公司同候选人同流程多轮继续合并，不虚增样本；
- 多平台继续只作为 Recall 手段，不设置平台配额；
- 任何新增都必须能稳定回到候选人原始正文，并完成作者 / Timeline / 连续题序 / 复制链核验。


---

## 10. 全库去重审计（2026-09-10）

本库已对去重前的 **379** 个正式来源完成一次全量同场审计，并统一重排编号。

- 去重前：`S001–S379`，379 个；
- 精确 / 归一化来源 URL 连通组件：**82 组**；
- 同 URL / 同来源组件中删除靠后重复成员：**99 个**；
- 不同 URL 但经公司、日期、轮次和连续题序确认属于同一实际面试：**1 个**（审计前 `S060` / `S219`，保留较早 `S060`）；
- 总删除重复来源：**100 个**；
- 去重后：`S001–S279`，共 **279 个 HUMAN-A**；
- 若未来人为重开采集，下一编号：`S280`。

本次“同场去重”的口径是**同一实际面试**，不是“同一候选人同一公司同一招聘流程”。因此明确的一面、二面、三面只要是不同实际面试，仍保留；已经被历史条目合并为一个来源的多轮流程也继续作为一个来源。对于“早期只记录其中一轮、后期重复条目补全了同一候选人的其它轮次”的 URL 组件，保留最早来源编号，但将后期更完整正文合并回最早 canonical，避免去重造成信息损失。
