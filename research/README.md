# 2026 AI Application / Agent 真人面经研究库

更新日期：2026-09-10

本目录不是“面试题大全”，也不按来源数量机械扩张。它负责为完整的 AI Application / Agent Engineer 知识体系提供一层**真实市场校准**：真实面试官究竟问什么、追到多深、怎样验真项目、哪些能力要求口述 / Coding / Debug / System Design。

> **完整知识体系决定应该学什么；HUMAN-A 真人面经负责告诉我们真实市场怎么问、问多深。**

---

## 1. 当前进度

- 正式 HUMAN-A 来源：**264 个**
- 来源编号：`S001–S264`
- 当前最大编号：`S264`
- 下一条正式来源：**`S265`**
- 正式 Batch：`batch-01.md` ～ `batch-12.md`
- 最新 Batch：[`interviews/batch-12.md`](interviews/batch-12.md)，新增 **10 个 HUMAN-A（S255–S264）**
- Monitoring Inbox：[`monitoring/inbox.md`](monitoring/inbox.md)，当前无待归档 HUMAN-A
- 当前停止判断：**仍未达到来源饱和**

Batch 12 在已有 254 个正式样本后仍新增 10 个独立真人场次；与此同时，泛搜索中的重复链、内容账号、付费答案 / 题库和 Role Scope 外结果明显增多。新增率下降说明搜索正在进入更深水区，但精确公司 / 岗位 / 轮次 / 作者时间线仍有产出，因此还不能停止。

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

任何一项不满足，都不能进入正式 Batch，也不能贡献 Canonical Question、问题频率、知识优先级、课程内容或市场趋势统计。

平台一律平等。牛客、小红书、知乎、脉脉、CSDN、掘金、Bilibili、抖音、个人博客、独立站、GitHub Pages 或其他公开来源都执行同一标准；平台只影响核验难度，不影响准入门槛。

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

岗位标题不是唯一依据。标题叫“后端开发”，但实际职责和整场面试明显围绕 Agent / RAG / LLM Service / AI Platform / Runtime，可以收录；反之，标题带 AI 但实际是 BI、传统推荐、广告排序、纯训练、CUDA、RLHF Infra、普通后端顺带问 AI Coding 等，不进入正式样本。

---

## 4. 一旦通过 Role Scope，整场技术问题全部保留

研究目标不是做一个只剩 Agent 名词的题库。

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

Batch 12 的多益网络 `S259` 即按这一规则把同一作者的一面与三面合并；拼多多提前批一面的两个高度近似 URL 因无法可靠确认原场次而整链排除。

---

## 6. 搜索策略

不只搜索“AI Agent 面经”。持续执行：

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

技术关键词轮换：Python、FastAPI、asyncio、MySQL、Redis、Kafka、MQ、Vector DB、Milvus、RAG、Embedding、Rerank、MCP、Skill、Tool、Memory、Context、Harness、Runtime、Checkpoint、Resume、Coding Agent、Claude Code、Codex、AI Coding、System Design。

搜索路径继续深入到：

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

## 7. Batch 12 的现实信号

本轮新增 `S255–S264` 后，出现几个值得继续追踪的趋势：

1. **“为什么用 Agent”正在替代“会不会 Agent”。** 腾讯直接把 Prompt / RAG / Fine-tuning / Workflow / Agent 放在同一条决策链里，考的是边界判断与成本收益，而不是框架名词。
2. **Harness / Runtime 正进入具体控制机制。** 长耗时异步 Tool、结构化 Tool Result、Hook 回填 Context、任务隔离、Queue 状态可靠性、Context Compression、Skill Progressive Disclosure 都来自真实追问。
3. **项目验真越来越具体。** 面试官会追“20 轮后 90% 信息保留如何证明”“PDF 31 分钟到 2.5 分钟怎么测”“团队里你本人写了什么”，并直接共享屏幕看代码。
4. **AI Coding 从工具偏好变成研发流程题。** 需求澄清、Plan、实现、编译、单测、浏览器验证，以及 AI 生成代码由谁兜底都开始进入正式面试。
5. **AI 应用岗仍然要求完整后端工程能力。** Redis、MySQL、线程池、JVM、鉴权、Webhook 最终一致性、Docker、SSE / WebSocket 与 Agent / RAG 同场出现。
6. **污染率在上升。** 后发近似复制、内容账号“真人叙事”、付费完整答案、SEO 学习路线越来越多，必须继续把 HUMAN-A Gate 放在问题“漂亮程度”之前。

---

## 8. 目录结构

```text
research/
├── README.md
├── interviews/
│   ├── batch-01.md
│   ├── ...
│   ├── batch-11.md
│   └── batch-12.md
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

- 从 **`S265`** 开始；
- 持续追 2026-09 最新原帖；
- 回扫 2026-03～09 尚未充分覆盖的公司、二 / 三面、Leader 面；
- 优先补 Agent Runtime / Harness / Coding Agent / AI Backend / AI Full-stack 的真实深挖；
- 沿本轮 HUMAN-A 作者页继续找同招聘流程后续轮次，并按同候选人合并；
- 继续主动搜索牛客之外的原始正文，但不设平台配额；
- 继续观察新增 HUMAN-A 数量 / 候选总量、重复比例、低质量 / 二次整理比例和 Role Scope 外比例。

只有连续多轮扩大公司、岗位、月份、轮次、平台、作者页、企业 / 话题页和个人博客后，同时出现新增 HUMAN-A 持续接近 0、精确搜索也很难产生新样本、公司 / 岗位 / 轮次覆盖和 Python → Agent Harness 的问题深度分布趋于稳定，才判断接近来源饱和。
