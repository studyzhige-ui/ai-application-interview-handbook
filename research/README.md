# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，而是用 **HUMAN-A 真人高质量第一人称面经**校准 AI Application / Agent Engineer 的真实面试市场：公司实际问什么、追到多深、怎样验真项目，以及哪些能力要求 Coding / Debug / System Design / AI Coding。

> **完整知识体系决定应该学什么；HUMAN-A 面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**369 个**
- 来源编号：`S001–S369`
- 当前最大编号：`S369`
- 下一条正式来源：**`S370`**
- 正式 Batch：`batch-01.md` ～ `batch-24.md`
- 最新 Batch：[`interviews/batch-24.md`](interviews/batch-24.md)，新增 **4 个 HUMAN-A（S366–S369）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**热门结果页局部饱和进一步加深，但热门公司全年真人来源整体仍不能判定饱和。Batch 24 是完整高搜索量扫描，最终只新增 4 个；与此同时 8 月仍能找到新的独立大厂流程，3～7 月长尾也继续出现未收录来源，因此更准确的结论是“新增边际下降 + Provenance / 去重成本显著上升”，而不是已经搜尽。**

Batch 24 在编号前重新直接回读 `batch-01.md` ～ `batch-23.md`，覆盖 `S001–S365` 全历史。最终只保留 4 个独立招聘流程：阿里云 Agent Infra（Data Infra）、阿里淘天 AI 应用研发、字节抖音 Agent 开发、字节安全与风控后端研发（AI Agent）。本轮多次出现 GitHub Code Search 0 命中但历史正文实际已经收录的情况，进一步确认 Code Search 只能辅助，不能承担去重判定。

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

平台一视同仁。牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客与独立站都执行同一 Gate；平台只影响核验难度，不影响准入门槛。

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

岗位标题不是唯一依据。标题叫 Backend，只要实际职责和整场面试主体明确围绕 Agent / RAG / LLM Service / Runtime，可以进入；反之，普通 Backend 仅深挖候选人的 Agent 项目、但岗位本身无法确认属于目标方向时，不收。

Batch 24 的典型案例：`S369` 标题是字节安全与风控后端研发实习生，但原帖明确标注 AI Agent，面试前半段连续围绕 Vector Retrieval、Hybrid Retrieval、RRF、Vector DB、OpenClaw / Context Engineering，因此按 AI Backend / Agent Role Scope 通过；通过后继续保留 HTTP / TCP、Redis Persistence、Process / Thread、Python GIL 和 Coding 等整场基础问题。

---

## 4. 通过 Role Scope 后，整场技术问题全部保留

确认是一场目标 AI 岗 HUMAN-A 后，真实出现的基础和 AI 技术问题都保留：

```text
Python / FastAPI / ASGI / asyncio
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

不使用普通 Backend、数据分析、推荐 / 广告算法等 Role Scope 外场次人为抬高基础题频率。

---

## 5. 去重：必须在分配 `Sxxx` 前完成

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
外部原帖 / 后发复制链核验
```

强制规则：

- GitHub Code Search / 搜索引擎“0 命中”只能辅助，不能证明未收录；
- 每个候选至少检查 URL、作者、公司、岗位、日期 / 轮次、项目关键词和 5～10 个独特连续题序；
- 同一候选人同一公司同一招聘流程的一面 / 二面 / 三面 / Leader 面必须合并为一个 `Sxxx`；
- 同一候选人不同公司 / BU、招聘流程独立时可以分别计数；
- 不同 URL 但题序 / 项目语义高度一致时必须继续追源；
- 无法确认复制链原始候选人时整链排除；
- 搜索摘要只负责发现，正文最终不能稳定打开则零贡献；
- 不同候选人的独立流程即使出现相同常见问题，仍分别计数。

Batch 24 的典型去重：阿里 Token Foundry 8/17 → 8/24 → 9/3 三轮在 Code Search 中无命中，但直接历史回读确认就是 `S148`；字节 TikTok Agent 8/9 同样被历史正文确认已收录；小红书 Agent 服务端 9/8 在搜索末段一度看起来是新候选，再次对历史正文后确认就是历史 `S033`；PDD 同一候选人的 8/31 后续轮次则因同公司同流程而不新增。上述页面全部零贡献。

---

## 6. 搜索策略

持续执行：

```text
热门公司优先
×
岗位别名
×
最新月份 + 历史长尾
×
技术关键词
×
作者 Timeline / 原始正文
```

热门公司优先：字节 / 抖音、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、拼多多、京东、滴滴、Bilibili、OPPO、vivo、小米等。

时间线继续双跑：

- **最新层：2026-08～09**，追秋招新增和后续轮次；
- **补漏层：2026-03～07**，深扫热门公司历史长尾。

岗位别名：AI 应用开发、AI 应用研发、Agent 开发、智能体开发、大模型应用、LLM Application、RAG、AI Backend、Agent Backend、AI Full-stack、Applied AI、FDE、Coding Agent、Agent Runtime、Agent Harness。

搜索不能停在结果页：

```text
搜索引擎 / 企业页 / 话题页
→ 精确公司 + 岗位 + 日期 / 轮次
→ 作者主页 / 候选人 Timeline
→ 原始正文 / 评论区
→ 跨页面复制关系
→ 全历史 Batch 最终去重
```

---

## 7. 当前饱和度判断

1. **最新热门结果页局部饱和已经很强。** 8～9 月泛搜中历史重复、内容账号、答案版、后发扩写、同流程后续轮次和 Role Scope 模糊页面占比继续升高。
2. **热门公司全年来源仍未证明整体饱和。** Batch 24 做了完整高搜索量扫描后仍能从 8 月独立流程和 4 月长尾各拿到新 HUMAN-A；说明 Recall 尚未归零。
3. **新增边际正在下降。** Batch 21 / 22 分别新增 11 / 12 个，Batch 23 为候选池收尾新增 5 个，Batch 24 完整扫描新增 4 个。单批下降不能直接宣布饱和，但需要连续观察。
4. **Provenance / 去重成本已经高于搜索成本。** 很多“新 URL”最终是历史样本、复制链、答案包装或同一招聘流程；作者、流程、题序和原始正文核验成为主要工作量。
5. **下一轮仍继续扩量，但更加偏向作者 Timeline 与历史长尾。** 只有当最新层、3～7 月长尾、作者 Timeline 三条路径连续多轮都明显低新增，才判断热门公司 HUMAN-A 接近饱和。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-23.md
│   └── batch-24.md
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

## 9. 下一轮优先级

- 从 **`S370`** 开始；
- 继续高搜索量，不因 Batch 24 只有 4 个就降低 HUMAN-A 门槛或停止长尾搜索；
- 热门公司优先，尤其继续深挖腾讯、字节 / 抖音、美团、快手、小红书、PDD、京东、滴滴、B站、OPPO / vivo / 小米，以及百度 / 阿里 / 蚂蚁历史长尾；
- 最新 8～9 月与 3～7 月长尾同时搜索；
- 优先沿已核验真人作者 Timeline 找同公司后续轮次与不同公司 / BU 的独立招聘流程；
- 继续重点观察 Agent Runtime Verification、Context / Memory Correctness、RAG Evaluation、AI Coding Verification、Harness / AgentOS；
- 继续补 Java / Python / FastAPI / Go / MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场的大厂样本；
- 内容账号、投稿 / 答案、付费墙、后发扩写、同作者流程不清、换公司标题同序链继续零容忍；
- 分配编号前再次直接回读 `S001–S369` 全历史。