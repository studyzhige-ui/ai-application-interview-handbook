# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它为 AI Application / Agent Engineer 知识体系提供**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目，以及哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**360 个**
- 来源编号：`S001–S360`
- 当前最大编号：`S360`
- 下一条正式来源：**`S361`**
- 正式 Batch：`batch-01.md` ～ `batch-22.md`
- 最新 Batch：[`interviews/batch-22.md`](interviews/batch-22.md)，新增 **12 个 HUMAN-A（S349–S360）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**尚未整体达到来源饱和。Batch 21 扩大 Recall 后新增 11 个，Batch 22 在同等严格 Gate 下继续新增 12 个；但 8～9 月热门结果页本身已经明显局部饱和，新增主要来自 3～7 月热门公司长尾与真人作者 Timeline。**

Batch 22 延续“高搜索量 + 热门公司优先 + 最新层 / 历史长尾双线 + 作者 Timeline”。搜索阶段形成约 15 个流程级强候选，最终再次直接回读 `batch-01.md` ～ `batch-21.md` 覆盖 `S001–S348`，并经过作者 / 日期 / 轮次 / 项目 / 题序 / 正文稳定性最终校验后，只放行 12 个独立 HUMAN-A。

本轮最重要的新增判断是：**热门公司全年真人来源仍未饱和，但 Provenance 成本持续上升。** 腾讯模糊流程、灵犀不稳定一面、美团复制链、百度内容化题单等都在最后编号前被撤出；新增主要来自滴滴、快手、阿里系、小红书、美团、京东物流等 3～4 月长尾原场。

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

Batch 22 再次体现这一规则：滴滴 `S349` 标题没有显式 Agent 岗名，但整场主体是 OpenClaw / Agent 扩容 / Context / RAG / WebFlux / ES Vector / AI Coding；京东物流 `S356` 标题是后端，但二面明确“主要拷打 Agent 项目”，并从 Spring AI、Memory、RAG 追到真实物流业务落地，因此均通过实际职责 Gate。

---

## 4. 通过 Role Scope 后，整场技术问题全部保留

确认是一场目标 AI 岗 HUMAN-A 后，面试官实际问到的所有技术问题都保留，包括：

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

Batch 22 中，阿里云 `S351` 同场出现 Go / Java、Spring、gRPC、TCP、MySQL、Redis、HNSW、Transformer、Rerank 与 LLM Generation；京东物流 `S356` 同场出现 Redis BigKey、ThreadLocal、Spring AI、三级 Memory 与 AI Coding，均完整保留。

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
- 搜索摘要只负责发现；正文最终不能稳定打开 → 不进入正式来源，也不能贡献问题。
- 不同候选人的独立招聘流程即使出现相同常见问题 → 分别计数。

Batch 22 的应用实例：

- 京东物流 04-08 一面 + 04-14 二面同作者同流程，合并为 `S356`；
- 小红书 04-06 一面 + 04-08 二面同作者同流程，合并为 `S352`；
- 阿里灵犀 04-03 一面在最终校验时正文再次不稳定，因此零贡献，只保留稳定的 04-10 二面 `S353`；
- 腾讯 `Akhasi` Timeline 同日出现“一面过 / 二面横向挂”，一个月后又出现“腾讯二面”，无法安全确认流程关系，整链排除；
- 美团 5 月候选向前追到 04-20 高度同序链，原始归属不清，整链排除；
- 阿里平头哥 04-29 后续轮次属于历史 `S122` 同流程，不另增编号，也不修改历史 Batch。

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

时间线继续分两层：

- **最新层：2026-08～09**，追秋招新流程、后续轮次和刚发布原帖；
- **补漏层：2026-03～07**，继续深扫热门公司实习 / 暑期长尾，直到扩大搜索量后边际新增明显下降。

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

## 7. Batch 22 的现实信号 / 饱和度诊断

1. **连续两轮高搜索量仍能产生双位数新增。** Batch 21 新增 11，Batch 22 新增 12；因此当前没有证据支持“热门公司全年 HUMAN-A 已接近整体饱和”。
2. **主要新增仍来自 3～4 月长尾。** 最新热门页的边际新增低，但滴滴、快手、阿里云、阿里国际、小红书、美团、京东物流的春季实习原场仍有未采尽来源。
3. **作者 Timeline 既提高 Recall，也提高去重能力。** 同一候选人的不同公司流程可被发现，同一公司的连续一二面也能正确合并；反过来，Timeline 冲突能及时阻止误收。
4. **去重 / Provenance 成本已经显著高于普通搜索成本。** 新 URL 很多，但必须结合历史正文和题序才能识别后发复制、换皮、同流程后续轮次。
5. **AI Coding 正从“会不会用”变成现场工程验证。** 美团 `S354` 要求共享屏幕直接实现需求；快手 `S350` 追 AI Coding 最大失败；京东 `S356` 追模型 / IDE 到底写了哪些真实代码以及质量怎样提升。
6. **RAG / Agent 必须有量化证明。** 快手直接追指标、提升幅度和强模型对照；京东追 Recall / Accuracy 是否实测；只会讲标准 Pipeline 的区分度继续下降。
7. **Harness / AgentOS 开始进入业务岗位。** 快手 `S359` 把安全风控 Agent、Skill、Harness 与 AgentOS 基础能力投资判断放在同一轮，显示 Agent Engineering 与产品 / 业务架构正在合流。
8. **Backend Foundation 仍然是 AI Application 的核心组成。** gRPC、TCP、Redis、MySQL、ThreadLocal、WebFlux、ES、JVM、Network 等在目标 AI 岗中持续高频出现。

当前判断仍是：**热门结果面局部饱和；热门公司全年真人来源整体未饱和。** 只有当“最新层 + 3～7 月长尾层 + 作者 Timeline”连续多轮在相近搜索强度下都只剩接近 0 的新增，才应调整为整体饱和判断。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-21.md
│   └── batch-22.md
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

- 从 **`S361`** 开始；
- **继续保持 Batch 21 / 22 的高搜索量，不退回只刷 8～9 月热门页**；
- 热门公司继续优先：腾讯、字节 / 抖音、美团、快手、小红书、拼多多、京东、滴滴、B站、OPPO / vivo / 小米；百度、阿里系、蚂蚁继续补长尾与后续轮次；
- 同时跑最新层和 3～7 月历史长尾层，并继续沿已核验真人候选人的 Timeline 深挖；
- 新来源分配编号前继续直接回读 `S001–S360` 对应历史 Batch，不依赖 Code Search 0 命中；
- 每轮记录候选流程级强池、最终 HUMAN-A、新发现历史重复、复制链、内容账号、正文稳定失败和流程归属不清的淘汰情况；
- 深挖 Agent Runtime Verification、Context / Memory Correctness、RAG Evaluation / Rerank / Citation、AI Coding Verification、Harness / AgentOS；
- 继续补 Python / FastAPI / ASGI / asyncio、Java / Spring / Go、MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场的大厂样本；
- 内容账号、答案帖、付费专栏、后发扩写、同作者相邻流程不清、换公司标题同序链继续零容忍。
