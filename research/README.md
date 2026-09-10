# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它负责为完整的 AI Application / Agent Engineer 知识体系提供一层**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目、哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**292 个**
- 来源编号：`S001–S292`
- 当前最大编号：`S292`
- 下一条正式来源：**`S293`**
- 正式 Batch：`batch-01.md` ～ `batch-14.md`
- 最新 Batch：[`interviews/batch-14.md`](interviews/batch-14.md)，新增 **16 个 HUMAN-A（S277–S292）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**仍未达到来源饱和**

Batch 14 在已有 276 个正式样本后仍确认 16 个独立 HUMAN-A，说明精确公司 / 岗位、作者主页与历史月份回扫仍有明显产出。与此同时，复制链、内容账号、付费墙、自动 AI 面和只能看到 Search Snippet 的结果继续增加，来源核验成本正在上升，但尚未达到停止条件。

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
- 同一候选人面试不同公司 → 属于独立招聘流程，可以分别计数；
- 不同 URL 但公司、岗位、问题顺序、项目描述和措辞高度一致 → 继续核验作者、发布时间、评论和流程；
- 无法确认复制链原始候选人 → **整条链排除，不猜原帖**；
- 不同候选人的独立招聘流程，即使遇到相同问题 → 分别计为独立真人命中。

近期典型案例：`S287` 把同一候选人字节中国交易与广告一 / 二 / 三面合并为一个来源；`S288` 把同一作者连续发布的字节 Agent 一 / 二面合并；Batch 14 同时发现 B 端小公司 / 法本信息近似逐题复制链，因无法确认原场次而整链排除。

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
```

搜索摘要只负责发现线索。最终无法稳定核验正文、候选人本人和真人面试，就不能进入 HUMAN-A。

---

## 7. Batch 14 的现实信号

1. **Recovery 已进入“外部副作用幂等”层。** 面试不再满足于“有 Checkpoint 就能 Resume”，而是追问外部任务已成功、进程在持久化 Checkpoint 前崩溃时，恢复后如何避免重复执行。
2. **Long-running Agent 开始考真正的 Cancel / Timeout / State。** “是否真的实现过取消”、异常 Loop 怎样停止、恢复时状态怎么处理，都比单纯背 Resume 概念更接近 Runtime Engineering。
3. **Tool / Skill 的规模化治理成为高频深挖。** 100+ Tool 如何 Registry、Retrieval、Dynamic Injection / Lazy Load，Tool 不可用如何 Fallback，Skill 的 Metadata / Scripts / References / Assets 怎样 Progressive Loading，开始进入真实面试。
4. **Security 与 Runtime Boundary 正在合流。** Prompt Injection、Tool Permission、Sandbox、高风险写操作确认、Tool Result Compression / Validation 往往不再是独立安全题，而是 Agent 执行链的一部分。
5. **AI Coding 正从工具使用变成代码归属与质量验真。** 面试官会问代码到底是候选人写的还是 AI 写的，并通过现场修改、复杂度约束、页面实操、Compile / Test 和人工验收验证本人能力。
6. **项目指标必须能够被审计。** “准确率 90%+”“性能提升 20%”“节约多少人力”会继续追 Baseline、Dataset、测量方法、Failure Case 与本人贡献。
7. **AI Application / Agent 岗的 Backend 深度没有下降。** ThreadLocal、Redis Lock / HotKey、RocketMQ Delay、NIO / Reactor、Config Center 动态刷新 / Fallback、MySQL Index 与 DB / Cache Consistency 均继续和 Agent 同场出现。
8. **作者时间线正在成为质量基础设施。** 同一候选人同流程多轮可以可靠合并，不同公司流程可以独立计数；反过来，数百篇多公司高频发布、私域导流与模板化内容也能通过作者主页被识别并排除。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-13.md
│   └── batch-14.md
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

- 从 **`S293`** 开始；
- 持续追 2026-09 最新 AI Application / Agent 原帖，优先直接正文而不是推荐 / 聚合页；
- 沿 Batch 14 新增来源作者主页继续寻找二 / 三面 / Leader 面，并按同候选人同流程合并；
- 回扫 2026-03～09 尚未充分覆盖的公司和岗位别名；
- 重点补 Long-running Agent 的 Cancel / Checkpoint / Resume / Idempotence / State；
- 继续深挖 Tool Registry / Retrieval / Lazy Loading、Permission / Sandbox、Trace / Evaluation；
- 继续观察 Token / Cost Budget、Rate Limit、Backend Concurrency 与 Streaming Budget；
- 继续寻找 AI Backend / AI Full-stack 中 MySQL / Redis / MQ / Network / Concurrency / Coding 与 Agent 同场出现的真人样本；
- 牛客外继续主动搜索个人博客 / 独立站 / 稳定原始正文，不设置平台配额；
- 持续记录新增 HUMAN-A 绝对数与命中率、重复率、内容账号 / 二次整理率、Role Scope 外比例。

只有连续多轮扩大公司、岗位、月份、轮次、平台、作者页、企业 / 话题页和个人博客后，同时出现新增 HUMAN-A 持续接近 0、精确搜索也很难产生新样本、公司 / 岗位 / 轮次覆盖和 Python → Agent Harness 的问题深度分布趋于稳定，才判断接近来源饱和。
