# HUMAN-A Monitoring Inbox

更新日期：2026-09-16

本文件只保存**已经满足 HUMAN-A、但尚未归入当天正式 Batch** 的候选。普通搜索线索、摘要、低质量面经、答案型文章、Role Scope 外来源和待核验复制链都不进入 Inbox。

> **当前状态：🟢 Continuous Monitoring。** 每天 10:00 / 17:00 / 22:00 搜最近 3 天的新面经；当天三次检索只形成一个日批次。10:00 / 17:00 只暂存已通过 Gate 的候选，22:00 重新做全历史去重后再统一分配 `Sxxx`。

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

**任何候选在分配 `Sxxx` 前必须直接回读全部历史 Batch。** GitHub Code Search / 搜索引擎 0 命中只能辅助，不能作为未收录证明。

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

## 历史冻结基线

- 截至 2026-09-10：`S001–S279`，共 **279 个 HUMAN-A**；
- 正式批次：`batch-01.md` ～ `batch-26.md`；
- 历史最大来源编号：`S279`；
- 恢复持续监测时的下一保留编号：`S280`；
- 全库历史曾从 379 个候选中删除 100 个同场 / 同源重复，说明“不同 URL”绝不能当作“不同面试”。

以上只是恢复监测时的历史基线。每次运行必须以当前 `main` 重新计算最新 Batch、总数、最大 ID 和下一编号。

## 每日运行规则

### 10:00 / 17:00

- 搜索最近 3 天；
- 高搜索量覆盖不同公司、岗位叫法、平台与作者 Timeline；
- 候选必须先完成 HUMAN-A + Role Scope + 全历史去重，才进入 Inbox；
- 不分配最终 `Sxxx`；
- 不创建当天多个 Batch；
- 将搜索覆盖和典型排除写入 `daily-log.md`。

### 22:00

- 先进行当天第三次最近 3 天搜索；
- 汇总 Inbox + 当日搜索结果；
- **重新**直接回读全部历史 Batch，对当日候选进行最终全库去重；
- 只对最终通过者按当前下一编号连续分配 `Sxxx`；
- 当天只创建一个正式 Batch；
- 更新 Research README / 本 Inbox / daily-log 以及当前仓库规定的相关研究状态入口；
- 0 个正式新增也是合法结果，不为凑数降低 Gate。

## 当前 Inbox

> 2026-09-16 10:00 Morning Search：**3 个候选已通过 HUMAN-A + Role Scope + 全历史去重 Gate**。这里只暂存候选，不分配 `Sxxx`；22:00 仍需重新回读全历史做最终去重。

### 美团｜AI 后端｜一面 + 二面（同一候选人同一流程，待晚间合并归档）

- 作者：`SOLDIER_627`（同济大学，个人求职 Timeline 可核验）
- 一面来源：https://api-cdn.nowcoder.com/discuss/927579574932705280?sourceSSR=post
- 二面来源：https://www.nowcoder.com/discuss/929087871779110912
- 一面明确日期：2026-09-10；二面帖子在本次最近 3 天发现窗口内发布。
- HUMAN-A 证据：候选人连续发布本人招聘流程；一面约 76 分钟、二面约 59 分钟，问题围绕本人实习项目连续深挖，不是答案帖或内容账号。
- 代表性题序：云服务器故障诊断 Skill → 错误路由 / 幻觉兜底 → 渐进式开放 Tool 与校验门禁 → 分层取证 / Evaluation → Workflow 迁移 Skill → 多 Skill 路由冲突 → Skill 增长导致 Context 膨胀 → 历史 Case 回放 / 故障注入 → PI Agent / DeepSeek Harness → Agent Loop 停止条件 → AI 代码生成速度超过人工 Review 的治理 → 云服务器 Region / AZ 容灾 → Coding。
- 去重：已直接回读 `batch-01.md`～`batch-26.md`。历史 `S228` 是**同一候选人的快手 AI 全栈独立招聘流程**，公司与招聘流程不同，因此不能误合并；当前美团两条 URL、公司流程与连续题序均未在历史正式库出现。当前一 / 二面必须合并为一个未来来源，不能按轮次拆号。

### 科大讯飞｜Agent 研发工程师 · Harness 方向｜线下一面 + 二面 + HR

- 作者：`Tale2229`（北京邮电大学，个人主页当前仅该本人求职帖）
- 来源：https://www.nowcoder.com/feed/main/detail/671d2fa1d7c04322837ee1f5788dd69d
- 面试：2026-09-11 武汉线下半天完成三场；帖子在本次最近 3 天发现窗口内发布。
- HUMAN-A 证据：作者明确记录从北京到武汉参加线下面试，一面多个问题答不上、意外进入二面、二面 / HR 自评以及等待结果；项目、基础、算法、HR 问题按真实顺序保留。
- 代表性题序：即时通信架构 → 多节点消息处理 / 负载均衡 → Agent 项目是否真实使用 → Short / Long-term Memory → 知识库增量更新 → Agent Loop 停止条件 → Harness → LangGraph Node 划分 → 项目代码量与 AI Coding 参与度 → HTTP / Python Decorator / IPC / Deadlock / RWLock / User-Kernel → AVL vs Red-Black → Memory Fragmentation → Algorithm；二面继续问 Agent 最新进展。
- 去重：已直接回读全历史。历史科大讯飞 `S178 / S179` 为不同作者、不同月份与不同项目 / 题序；当前 URL、作者、9/11 招聘流程与长题序均未在历史库出现。

### 快手｜AI 全栈｜秋招一面

- 作者：`明天会有好天气`（个人秋招进度与其它本人面试 Timeline 可核验）
- 来源：https://www.nowcoder.com/feed/main/detail/60d833cbae7f4a668a0bed9e18a428f1
- 发布：2026-09-15 左右（页面显示“昨天 23:03”，属于本次最近 3 天窗口）。
- HUMAN-A 证据：岗位标题明确 AI 全栈；作者保留“八股好久没看、很多说不上来”的现场状态，其个人 Timeline 还可核验 9 月多家公司笔面进度，不是批量内容号。
- 代表性题序：实习 → MySQL Insert 执行过程 → 两阶段事务提交 → GC / ZGC → Slow SQL → AI Coding 流程 → AI Coding 上线代码遗漏 Bad Case 如何处理 → Object Creation → Repeatable Read → Coding（最大岛屿面积）。
- 去重：已直接回读全历史；当前 URL / 作者未收录，历史快手 AI 全栈 / Agent 样本均为其它候选人和不同招聘流程。虽然 AI 专项问题数量不多，但岗位本身通过 Role Scope，因此整场真实 Backend + AI Coding 问题应保留。
