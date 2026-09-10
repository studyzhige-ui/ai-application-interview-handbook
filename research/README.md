# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它为 AI Application / Agent Engineer 知识体系提供**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目，以及哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**331 个**
- 来源编号：`S001–S331`
- 当前最大编号：`S331`
- 下一条正式来源：**`S332`**
- 正式 Batch：`batch-01.md` ～ `batch-19.md`
- 最新 Batch：[`interviews/batch-19.md`](interviews/batch-19.md)，新增 **6 个 HUMAN-A（S326–S331）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**尚未整体达到来源饱和。热门公司仍能找到独立高质量来源，但字节 / 腾讯 / 美团 / 快手等热门结果面的历史重复、复制链和内容包装比例已经很高；百度、阿里系本轮仍有明显新增。**

Batch 19 按本轮要求把搜索重心重新放到热门公司。分配编号前先确认 `main` 仍处于 Batch 18 的 `S001–S325` 基线；结合上一批刚完成的历史 Batch 直接回读结果，重新读取最新 Batch 18，并对每个候选回查相关历史来源。最终只放行百度 2 个独立流程、阿里 3 个独立流程和 OPPO 1 个独立流程，共 6 个 HUMAN-A。

本轮同时撤出多个“看起来很强”的热门来源：拼多多复活赛因作者属于 100+ 社招面经 / 订阅内容生态而触发非内容账号 Gate；快手 7 月候选向前追到 2 月原场和 3 / 4 月多个高度同序版本，原始归属无法可靠确认，整链排除；美团、腾讯、字节多条热门结果则已精确命中历史正式来源。

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
- 如果更早不同作者页面与候选帖几乎逐题同序，而无法证明独立场次 → 候选帖不入库。
- 无法确认复制链原始候选人 → **整条不确定链排除，不猜原帖。**
- 搜索摘要只负责发现；正文最终不能稳定打开 → 不进入正式来源。
- 不同候选人的独立招聘流程即使出现相同常见问题 → 分别计数。

Batch 19 的应用实例：百度 8/20 与 8/26 两轮由同一作者发布，合并为 `S327`；阿里控股 8/17 与 8/21 两轮同样合并为 `S329`。阿里云 `S330` 只保留 8/31 原场，09-07 后发页面因复用 SGX / EPC / PV / Coding 核心题序而排除。OPPO 后发“帮转”页面不计数，只保留 `S331` 原作者页。快手 7 月候选继续追到 2 月、3 月、4 月多个高度同序版本后无法确认独立性，整条不确定链排除。

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
```

当前公司优先级：字节、阿里系、腾讯、美团、快手、小红书、百度、蚂蚁、拼多多、京东、滴滴、Bilibili、OPPO、vivo、小米等；同时保留高质量长尾公司补充，但不再为了公司数量平均分配搜索预算。

重点月份：`2026-03` ～ `2026-09`，优先 `2026-08` ～ `2026-09` 最新秋招。

岗位别名轮换：AI 应用开发、AI 应用研发、Agent 开发、智能体开发、大模型应用开发、LLM 应用、RAG 开发、AI 后端、Agent 后端、AI 全栈、Applied AI、FDE、Coding Agent、Agent Runtime、Agent Harness。

技术关键词轮换：Python、FastAPI、asyncio、Java、Spring、Go、MySQL、Redis、Kafka、MQ、Vector DB、Milvus、RAG、Embedding、Rerank、RRF、MCP、Skill、Tool、Memory、Context、Harness、Runtime、Checkpoint、Resume、Cancel、Permission、Sandbox、Trace、Evaluation、Benchmark、Coding Agent、Claude Code、Codex、AI Coding、System Design。

搜索不能停在结果页：

```text
搜索引擎 / 企业页 / 话题页
→ 精确公司 + 岗位 + 轮次
→ 作者主页 / 候选人 Timeline
→ 原始正文 / 评论区
→ 跨平台同步与复制关系
→ 回到全部历史 Batch 做最终去重
```

---

## 7. Batch 19 的现实信号

1. **热门公司仍未完全饱和。** 回到热门公司精确搜索后仍新增 6 个独立流程，尤其百度和阿里系仍有高价值长链路面经。
2. **Observability 已经进入 Runtime Trace 层。** 百度 `S326` 会追 Trace Hook、请求到 Trace 的映射、节点级故障分析，不再停留在“有没有日志”。
3. **RAG 参数必须拿实验说话。** `S326` 会追 Hybrid 的真实收益、RRF 为什么不用线性权重、常数如何确定，以及最终 Citation / Verification 如何回链证据。
4. **Agent Infra 与 Data / System Infra 正在融合。** 阿里云 `S330` 同场出现 SGX / EPC、多租户安全、吞吐瓶颈、State Persistence 与 120min SLS → MySQL AI Coding。
5. **Agent Self-evolution 成为真实 Infra 问题。** 阿里控股 `S329` 连续追 Agent Pool、自进化机制、Evolution Metric、数据采集、DAU、Resource 和二面实现细节。
6. **Checkpoint + 外部副作用仍是可靠性高频深题。** 阿里 `S328` 直接追 Tool 已成功但 Checkpoint 写失败后的恢复与幂等。
7. **AI 应用项目验真更强调 Delivery / Regression。** OPPO `S331` 把个人贡献、效果指标、Tool Failure、Human Confirmation 与 AI 改码回归验证放在同一条链中。
8. **热门结果页复制 / 内容包装比例很高。** PDD 强候选因内容账号撤出，快手强候选因跨月份同序链撤出，美团 / 腾讯 / 字节大量结果已是历史样本。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-18.md
│   └── batch-19.md
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

- 从 **`S332`** 开始；
- 继续以**热门公司优先**：重点补字节、腾讯、美团、快手、小红书、拼多多、京东、滴滴、B站，以及 OPPO / vivo / 小米；百度 / 阿里系继续追新增轮次；
- 新来源分配编号前继续直接回读 `S001–S331` 对应历史 Batch，不依赖代码搜索索引；
- 对 `S326 / S327` 百度和 `S328 / S329 / S330` 阿里系的后续技术面继续追踪，同公司同流程只合并，不另增来源；
- 热门公司搜索优先使用“公司 + Agent / AI 应用 + 轮次 + 日期 + 作者 Timeline”，避免只刷热门关键词结果页；
- 深挖 Runtime Trace / Observability、Tool Runtime、Checkpoint / Resume / Idempotence、Agent Self-evolution、Enterprise Knowledge Permission、RAG Evaluation / Citation；
- 继续补 Python / FastAPI / ASGI / asyncio、Java / Spring / Go、MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场样本；
- 对内容账号、答案帖、付费专栏、后发扩写、跨月同序题单保持零容忍；
- 牛客外继续主动搜索小红书、知乎、脉脉、个人博客 / 独立站，但主要搜索预算优先热门公司；
- 持续记录热门公司新增率、历史重复率、复制链比例和内容账号比例，区分“热门结果面局部饱和”和“热门公司真实来源整体饱和”。

只有连续多轮对热门公司和跨平台原始来源做精确搜索后，新增 HUMAN-A 持续接近 0、作者 Timeline 也难以产生新独立流程，才判断热门公司来源真正接近饱和。