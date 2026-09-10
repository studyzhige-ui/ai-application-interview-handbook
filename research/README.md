# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它为 AI Application / Agent Engineer 知识体系提供**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目，以及哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**348 个**
- 来源编号：`S001–S348`
- 当前最大编号：`S348`
- 下一条正式来源：**`S349`**
- 正式 Batch：`batch-01.md` ～ `batch-21.md`
- 最新 Batch：[`interviews/batch-21.md`](interviews/batch-21.md)，新增 **11 个 HUMAN-A（S338–S348）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**尚未整体达到来源饱和。上一轮显著扩大搜索量后，新增长尾 HUMAN-A 从 6 提升到 11，说明此前存在 Recall 不足；但 8–9 月热门结果页本身已经明显局部饱和，重复、复制链、内容包装和正文不稳定比例很高。**

Batch 21 专门做“扩大搜索量后的饱和度诊断”。保守统计执行了 120+ 组热门公司 × 岗位别名 × 月份 × 平台 / 技术关键词检索组合，并从 8–9 月热门结果面向 2026-03～07 历史长尾与作者 Timeline 扩展；随后重新直接回读 `batch-01.md` ～ `batch-20.md`，覆盖 `S001–S337` 全历史。最终放行 11 个独立 HUMAN-A，明显高于此前连续两批各 6 个。

这轮最重要的结论不是“来源突然变多”，而是**来源结构发生了变化**：8–9 月热门关键词页的新增率已经很低，但腾讯、字节、小红书、阿里系、百度等热门公司的 3–7 月长尾原帖和真人作者 Timeline 仍能持续挖出独立招聘流程。因此当前应判断为“热门结果面局部饱和，热门公司全年真人来源整体未饱和”。

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
- 更早不同作者页面与候选帖几乎逐题同序，而无法证明独立场次 → 候选帖不入库。
- 无法确认复制链原始候选人 → **整条不确定链排除，不猜原帖。**
- 搜索摘要只负责发现；正文最终不能稳定打开 → 不进入正式来源。
- 不同候选人的独立招聘流程即使出现相同常见问题 → 分别计数。

Batch 21 的应用实例：阿里平头哥 4/28 页面虽然 Code Search 0 命中，但全历史直接回读后确认已经是 `S122`，因此撤出；拼多多 7/25 两轮也已是 `S061`；`Ariasu` 的字节 6/17 一面与 6/23 二面同作者、同公司、同招聘流程，合并为一个来源；另有不同作者页面与历史 `S310` 几乎整场同序，按复制 / 复用链风险排除；只能依赖搜索缓存、原始正文不稳定的强题单仍然零贡献。

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

重点月份调整为两层：

- **最新层：2026-08～09**，追新增秋招流程和后续轮次；
- **补漏层：2026-03～07**，继续深扫热门公司历史长尾，直到扩大搜索量后边际新增明显下降。

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

## 7. Batch 21 的饱和度诊断

1. **扩大 Recall 后新增从 6 提升到 11。** 说明此前连续两批每批 6 个不能直接解释为整体饱和，搜索覆盖深度也是限制因素。
2. **新增主要来自 3–7 月历史长尾，而不是 8–9 月热门第一页。** 腾讯、字节、小红书、阿里系、百度等大厂仍有早期独立原帖未被普通“最新 Agent 面经”查询召回。
3. **作者 Timeline 的边际价值很高。** 从真实候选人主页可以串起同一人的多家公司独立流程，同时也能识别同公司连续一二面应合并，显著降低漏召回与虚增样本。
4. **热门结果页已局部饱和。** 8–9 月泛搜中的历史重复、换 URL 同场、内容账号、后发答案版、招聘号帮转和正文不稳定越来越多。
5. **去重成本已经高于搜索成本。** 很多“新 URL”只有经过全历史正文、作者、日期、项目和 5–10 个连续题序对照后才能判定是否独立。
6. **当前不应停止扩量搜索。** 至少还需要连续若干轮保持接近 Batch 21 的搜索强度；只有在 3–7 月长尾和作者 Timeline 同样持续低新增时，才有资格判断热门公司整体接近饱和。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-20.md
│   └── batch-21.md
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

- 从 **`S349`** 开始；
- **继续保持 Batch 21 的高搜索量，不再退回只刷 8–9 月热门页**；
- 热门公司仍优先：腾讯、字节 / 抖音、美团、快手、小红书、拼多多、京东、滴滴、B站、OPPO / vivo / 小米；百度、阿里系、蚂蚁继续补长尾与后续轮次；
- 同时跑两条时间线：追 9 月最新新增 + 深扫 3–7 月历史长尾；
- 优先沿已核验真实候选人的 Timeline 深挖不同公司独立流程，以及同公司后续轮次；
- 每轮继续记录搜索组合数、候选数、正文稳定数、HUMAN-A 强候选数、历史重复 / 复制链 / 内容账号 / 正文不稳定淘汰数，形成可比较的饱和度漏斗；
- 新来源分配编号前继续直接回读 `S001–S348` 对应历史 Batch，不依赖代码搜索索引；
- 深挖 Agent Runtime Verification、Context / Memory Correctness、GraphRAG / Retrieval Evaluation、AI Coding Verification，以及 Python / FastAPI / Java / Go / MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场的大厂样本；
- 内容账号、答案帖、付费专栏、后发扩写、同作者相邻多帖、换公司标题同序链继续零容忍。

只有当**最新层 + 历史长尾层 + 作者 Timeline 三条路径**连续多轮都出现明显低新增，才判断热门公司 HUMAN-A 真正接近饱和。