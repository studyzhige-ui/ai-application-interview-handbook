# 2026 AI 应用 / Agent 真人面经持续监控 Inbox

用途：只保存尚未归入正式 Batch、但已经达到 **HUMAN-A** 标准的候选来源。

## 固定准入标准

平台一视同仁。牛客、小红书、知乎、脉脉、CSDN、Bilibili、抖音、个人博客及其他公开来源全部执行同一门槛，不设平台配额。

新的 Inbox 候选必须同时满足：

1. **真人面试官**：人与人进行的技术面 / Leader 面 / 项目深挖；
2. **候选人本人第一人称**：不是整理、搬运或二次转述；
3. **高信息密度**：具体技术问题足够丰富；
4. **真实现场痕迹**：追问、答题状态、轮次、结果、互动、Coding / Demo 等可验证线索；
5. **Role Scope Gate**：AI 应用、Agent、LLM 应用、RAG、AI Backend、AI Full-stack、Applied AI、FDE、Agent Runtime / Harness / Coding Agent 等目标方向；
6. **正文稳定可核验**：原始正文与 URL 可以实际访问并验证；
7. **非重复**：不是转载、合集、跨平台同场重复或后发近似复制。

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

任意一项不满足都不进入 Inbox、正式 Batch、Canonical Question、频率统计或课程优先级。

## 通过岗位准入后：整场全知识保留

确认是一场目标 AI 岗 HUMAN-A 后，真实出现的以下知识全部一视同仁记录：

```text
Python
FastAPI
Backend Engineering
MySQL
Redis
Vector DB
LLM Foundation
RAG
Agent Harness / Runtime
System Design
```

以及 OS / Network / MQ / Kafka / Concurrency / HTTP / SSE / WebSocket / Coding / Debug / Security / Evaluation。

**不使用普通后端、数据分析、BI、推荐算法等 Role Scope 外面经人为补基础题。**

## 平台范围

持续主动搜索：

```text
牛客 / 小红书 / 知乎 / 脉脉
CSDN / 掘金 / 个人博客 / 独立站
Bilibili / 抖音
其他公开可稳定核验来源
```

平台只影响核验难度，不影响质量标准。登录态、App 跳转、动态加载、企业 / 话题页和搜索摘要都可以用于发现，但最终必须回到可稳定核验的正文 / 作者 / 招聘流程。

## 默认排除

- AI 自动面试 / 模拟面试；
- 低信息密度第一人称；
- 合集 / 整理 / 搬运 / 后发近似复制；
- 标准答案 / 高频题 / 面试宝典 / 完整解析；
- SEO、课程、资源导流；
- 内容账号批量模板化“真人叙事”，无法可靠确认候选人本人经历；
- 只有标题、截图、Search Snippet 或评论传言；
- 付费墙只露少量内容，无法核验完整上下文；
- 普通后端 / 前端、传统数据分析 / BI、纯推荐 / 纯训练 Infra 等 Role Scope 外场次；
- 仅因标题或个别问题出现 AI / Agent 字样，但无法证明实际职责属于目标方向；
- 无法确认原作者归属的逐题复制链：宁可整链排除，不按发布时间猜原帖。

临时线索只用于寻找真正 HUMAN-A 原帖，线索本身零贡献。

## 固定搜索方法

```text
公司
×
岗位别名（AI应用开发 / Agent开发 / 智能体开发 / 大模型应用开发 /
LLM应用 / RAG开发 / AI后端 / AI全栈 / Applied AI / FDE / Coding Agent）
×
月份（重点回扫 2026-03～09，同时追最新发布）
×
技术关键词（Python / FastAPI / asyncio / MySQL / Redis / Vector DB /
RAG / MCP / Skill / Harness / Runtime / Context / Memory / Tool / Coding）
```

并继续：

```text
企业 / 话题页
→ 精确标题 / 精确轮次
→ 作者主页 / 个人博客
→ 原始正文
→ 跨平台重复核验
```

## 固定三层去重

```text
URL 精确去重
+
题序 / 项目语义去重
+
作者 / 招聘流程时间线去重
```

- 同候选人同流程多轮 → 合并计为一个来源，但保留所有轮次真实问题；
- 跨平台同步、镜像、后发近似复制 → 只保留更原始、更稳定、更有现场证据的一份；
- 不同候选人独立遇到相同问题 → 分别计为独立 HUMAN-A 命中；
- 无法可靠确认谁是原场次的逐题复制链 → 整链排除。

## 保存字段

每个候选至少记录：发现日期、面试日期 / 轮次、公司 / 岗位、原始 URL、真人 / 第一人称 / 现场证据、5～12 条左右高信息量问题的简洁转述、三层去重结论。

问题只能记录原帖能够确认真实问到的内容，不把合理推导写成面试问题。

## 当前基线

- 更新日期：2026-09-10
- 正式来源：`S001–S254`，共 **254 个 HUMAN-A**
- 当前正式批次：`batch-01.md` ～ `batch-11.md`
- 最新正式批次：Batch 11（`S226–S254`，新增 29 个）
- Canonical Question：只从当前干净 HUMAN-A 来源累计；低质量来源继续保持零贡献
- 当前最大来源编号：`S254`，下一条正式来源从 **`S255`** 开始
- 下一轮优先级：继续回扫 2026 年 3–9 月未覆盖公司 / 二三面 / Leader 面，重点 Agent Runtime / Harness / Coding Agent / AI Backend / AI Full-stack；持续追最新 9 月原帖；继续主动搜索牛客外的高质量原始来源
- 继续完整记录目标岗位实际出现的 Python / FastAPI / Backend / MySQL / Redis / Vector DB / LLM / RAG / Agent Harness / System Design，不只摘 AI 关键词
- 持续监控指标：**新增 HUMAN-A 绝对数量、新增 HUMAN-A 占全部候选比例、已收录重复比例、二次整理 / 低质量 / Role Scope 外比例**
- 当前停止判断：**仍未达到来源饱和。Batch 11 在已有 225 个 HUMAN-A 后仍新增 29 个独立高质量来源；泛搜索重复率虽高，但精确公司 / 岗位 / 轮次搜索仍有明显产出。**
- 停止条件：只有连续多轮扩大公司、岗位、月份、轮次、平台 Recall 后，新增 HUMAN-A 数量与占比都持续接近零，精确公司 / 轮次 / 作者页 / 原帖搜索也难以发现新来源，并且新增知识模块 / 追问深度分布稳定收敛，才进入收尾；不以 Batch 或 `Sxxx` 数量为阈值。

---

## 待整理新来源

暂无。
