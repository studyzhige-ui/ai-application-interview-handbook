# HUMAN-A Monitoring Inbox

更新日期：2026-09-10

本文件只保存**已经满足 HUMAN-A、但尚未归入正式 Batch** 的候选。普通搜索线索、摘要、低质量面经、答案型文章、Role Scope 外来源和待核验复制链都不进入 Inbox。

## 固定准入标准

新的 Inbox 候选必须同时满足：

1. **真人面试官**：真人技术面 / Leader 面 / 项目深挖；
2. **候选人本人第一人称**：不是整理、搬运、代发、投稿或内容账号包装；
3. **高信息密度**：具体技术问题和追问足够丰富；
4. **真实现场痕迹**：答题状态、引导、打断、轮次、结果、Coding / Demo / 屏幕共享等可核验；
5. **Role Scope Gate**：AI Application、Agent、RAG、AI Backend、AI Full-stack、Applied AI、FDE、Agent Runtime / Harness / Coding Agent 等目标方向；
6. **正文稳定可核验**：原始正文和 URL 可实际访问；
7. **非重复**：不是转载、合集、跨平台同场、后发复制、换公司标题同序或不确定复制链。

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

任意一项不满足都不进入 Inbox、正式 Batch、Canonical Question、频率统计或课程优先级。

## 通过岗位准入后：整场真实技术问题保留

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

不使用普通后端、普通前端、数据分析、推荐 / 广告算法、纯训练 Infra 等 Role Scope 外场次人为补基础题；但目标 Agent / AI Backend 流程真实出现的工程基础题必须保留。

## 全量去重规则

**任何未来候选在分配 `Sxxx` 前必须直接回读全部历史 Batch。** GitHub Code Search / 搜索引擎 0 命中只能辅助，不能作为未收录证明。

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

至少检查 URL、作者、公司、岗位、日期 / 轮次、项目关键词和 5～10 个独特连续题序。

- 同候选人同公司同流程多轮 → 合并一个来源；
- 同候选人不同公司 / BU、招聘流程独立 → 可以分别计数；
- 不同 URL / 不同平台但题序 / 项目语义高度一致 → 继续追源；
- 作者本人是真人也不能自动证明每一篇帖子都是本人原场；
- 无法确认复制链原场 → 整链排除；
- 正文最终不能稳定打开 → 零贡献；
- 不同候选人独立遇到相同常见问题 → 分别计数。

最终 Batch 26 的典型去重：快手 3 月 18 日一条高密度“大模型应用”页面最终追到更早的 3 月 5 日原场，连续 20+ 道题高度同序，因此后发页零贡献；只保留能由同一候选人串起 3 月 5 日一面、3 月 9 日二面和当晚 OC 的原始招聘流程 `S277`。

## 最终主动采集基线

- 更新日期：2026-09-10
- 正式来源：`S001–S279`，共 **279 个 HUMAN-A**
- 正式批次：`batch-01.md` ～ `batch-26.md`
- 最终主动搜索批次：Batch 26（全库去重后本批保留 `S275–S279`，共 5 个）
- 当前最大来源编号：`S279`
- 若未来人为重开采集，下一条保留编号：**`S280`**
- Canonical Question：只从正式 HUMAN-A 累计
- 主动搜索状态：**已按用户要求在 Batch 26 后结束。**
- 当前判断：**8～9 月大厂热门结果层高度局部饱和；3～7 月仍可能理论上存在残余长尾，但继续主动搜索的边际收益已经显著低于 Provenance / 去重成本。冻结主动采集不等于宣称互联网绝对没有遗漏。**

Batch 26 只搜索 2026 年大公司，并显著扩大搜索量；搜索阶段曾放行百度、蚂蚁国际、阿里云以及三个不同候选人的快手流程。全库去重后，阿里云 4/22 流程与更早来源同场并回最早 canonical，因此 Batch 26 当前净保留 5 个来源。牛客、小红书、知乎、脉脉、博客、独立站、技术社区继续使用同一 Gate；本批非牛客正式新增为零，是原始正文 / 作者归属 / 复制链核验结果，不是平台配额。

## 全库去重结果

- 去重前：379 个来源；
- 删除同一实际面试的重复条目：100 个；
- 去重后：`S001–S279`，共 **279 个 HUMAN-A**；
- 其中 99 个来自归一化 URL 重复组件，另 1 个为不同 URL 但同公司 / 同日期 / 同轮次 / 连续题序确认同场；
- 不同实际轮次不会因为属于同一招聘流程而被删除；后期更完整的同源复盘已合并回最早 canonical。

## 收官后规则

当前不再安排下一轮主动搜索。若未来人为重开采集：

1. 先读取当前 `research/README.md`、本文件、两份 quality policy；
2. 再直接回读 `batch-01.md` ～ `batch-26.md`，覆盖 `S001–S279` 全历史；
3. 只有完成 URL、作者、公司 / 岗位 / 日期 / 轮次、题序、项目语义、Timeline 与复制链核验后，才可从保留编号 `S280` 开始；
4. 同公司同候选人同流程多轮继续合并，不虚增样本；
5. 多平台只作为 Recall 手段，不设置平台配额，也不降低 HUMAN-A 门槛。

## 当前 Inbox

暂无待归档 HUMAN-A。
