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

不使用普通后端、数据分析、推荐 / 广告算法等 Role Scope 外场次人为补基础题。

## 默认排除

- AI 自动面试 / Mock Interview / 模拟题；
- 低信息密度第一人称；
- 合集 / 整理 / 搬运 / 帮转 / 投稿；
- 标准答案 / 高频题 / 面试宝典 / 完整解析；
- SEO、课程、资源导流、付费墙无法完整核验；
- 内容账号批量模板化真人叙事；
- 只有标题、截图、Search Snippet 或评论传言；
- 普通 Backend / Frontend 只顺带问 AI 项目，但岗位 Role Scope 无法确认；
- 数据分析 / BI、纯推荐 / 广告、纯训练 Infra、AI 测试等目标范围外岗位；
- 同作者同公司相邻多帖但招聘流程关系无法确认；
- 无法确认原作者归属的逐题复制链；
- 原始正文最终无法稳定访问、只能依赖 Search Cache / Snippet。

## 固定搜索方法

继续执行**热门公司优先 + 高搜索量**：

```text
字节 / 抖音 / 阿里系 / 腾讯 / 美团 / 快手 / 小红书 / 百度 / 蚂蚁 /
拼多多 / 京东 / 滴滴 / Bilibili / OPPO / vivo / 小米
×
岗位别名
×
最新 2026-08～09 + 补漏 2026-03～07
×
技术关键词
×
作者 Timeline / 原始正文
```

岗位别名包括 AI 应用开发、AI 应用研发、Agent、智能体、大模型应用、LLM Application、RAG、AI Backend、Agent Backend、AI Full-stack、Applied AI、FDE、Coding Agent、Agent Runtime、Agent Harness。

搜索不能停在结果页：继续追精确公司 + 岗位 + 日期 / 轮次、作者主页、候选人其它帖子、原始正文、评论区和跨页面复制关系。

## 强化去重流程

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
外部原帖 / 后发复制链核验
```

至少检查 URL、作者、公司、岗位、日期 / 轮次、项目关键词和 5～10 个独特连续题序。

- 同候选人同公司同流程多轮 → 合并一个来源；
- 同候选人不同公司 / BU、招聘流程独立 → 可以分别计数；
- 不同 URL 但题序 / 项目语义高度一致 → 继续追源；
- 无法确认复制链原场 → 整链排除；
- 正文最终不能稳定打开 → 零贡献；
- 不同候选人独立遇到相同常见问题 → 分别计数。

Batch 24 的应用：阿里 Token Foundry 三轮与字节 TikTok Agent 8/9 都在 Code Search 0 命中的情况下被直接历史回读识别为已收录；小红书 Agent 服务端 9/8 在最终复核时确认与历史 `S033` 为同 URL / 同场；PDD 同候选人 8/31 属于历史已收同公司同流程后续轮次；7 月字节一条强候选因与历史其它公司罕见连续题序高度同构且复制链归属不稳而整链排除。上述全部零贡献。

## 当前基线

- 更新日期：2026-09-10
- 正式来源：`S001–S369`，共 **369 个 HUMAN-A**
- 当前正式批次：`batch-01.md` ～ `batch-24.md`
- 最新正式批次：Batch 24（`S366–S369`，新增 4 个）
- 当前最大来源编号：`S369`
- 下一条正式来源从 **`S370`** 开始
- Canonical Question：只从正式 HUMAN-A 累计
- 当前停止判断：**热门结果页局部饱和进一步加深，但热门公司全年真人来源整体尚未证明饱和。Batch 24 完整高搜索量扫描新增 4 个，新增边际继续下降；与此同时 8 月独立流程与 4 月长尾仍有新来源，下一轮继续观察最新层、历史长尾与作者 Timeline 三条路径是否同时持续低新增。**

## 下一轮搜索优先级

1. 从 `S370` 开始，编号前直接回读 `S001–S369`；
2. 继续保持高搜索量，最新层与 3～7 月历史长尾同时跑；
3. 热门公司优先：腾讯、字节 / 抖音、美团、快手、小红书、拼多多、京东、滴滴、B站、OPPO / vivo / 小米；百度 / 阿里 / 蚂蚁继续补长尾；
4. 沿已核验真人作者 Timeline 深挖，同公司同流程后续轮次只合并，不新增；不同公司 / BU 独立流程继续逐条验真；
5. 继续记录强候选数、最终放行数以及历史重复 / 复制链 / 内容账号 / 正文不稳定 / Timeline 冲突淘汰原因；
6. 深挖 Agent Runtime Verification、Context / Memory Correctness、RAG Evaluation、AI Coding Verification、Harness / AgentOS；
7. 继续补 Java / Python / FastAPI / Go / MySQL / Redis / MQ / Network / Concurrency 与 Agent 同场的大厂样本；
8. 内容账号、投稿 / 答案、付费专栏、后发扩写、流程不清和换公司标题同序链继续零容忍；
9. 特别警惕 Code Search 0 命中但历史正文已收录的假阴性，必须以直接历史回读为准。

## 当前 Inbox

暂无待归档 HUMAN-A。