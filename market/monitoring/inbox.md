# HUMAN-A Monitoring Inbox

更新日期：2026-09-19

本文件只保存**已经满足 HUMAN-A、但尚未归入当天正式 Batch** 的候选。普通搜索线索、摘要、低质量面经、答案型文章、Role Scope 外来源和待核验复制链都不进入 Inbox。

> **当前状态：🟢 Continuous Monitoring。** 每天三次搜最近 3 天的新面经；当天三次检索只形成一个日批次。10:00 / 17:00 只暂存已通过 Gate 的候选，22:00 重新做全历史去重后再统一分配 `Sxxx`。

## 固定准入与去重

正式候选必须同时满足：

```text
真人面试官
+ 候选人本人第一人称
+ 高技术密度
+ 真实现场 / 招聘流程痕迹
+ AI Application / Agent Role Scope
+ 原始正文稳定可核验
+ 非转载 / 合集 / 内容号 / 答案帖 / AI 自动面试 / 重复
= HUMAN-A
```

通过岗位准入后，整场真实技术问题都保留，包括 Python / Java / Go、FastAPI、MySQL、Redis、MQ、Network、Concurrency、Vector DB、LLM、RAG、Agent、MCP / Skill / Memory / Harness、AI Coding、System Design 等；不使用普通后端 / 普通前端 / 纯训练 Infra 面经人为补频率。

任何候选进入 Inbox 或分配 `Sxxx` 前，都必须直接回读全部历史 Batch，并同时核验 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义、至少 5–10 个连续独特题序、招聘 Timeline、跨平台镜像与复制链。GitHub / Search 的 0 命中不能证明未收录。

- 同候选人同公司同招聘流程多轮 → 合并一个来源；
- 同候选人不同公司 / 独立流程 → 可以分别计数；
- 不同 URL 但题序 / 项目语义高度一致 → 继续追源；
- 复制链原场不确定 → 整链排除；
- 原文不能稳定打开 → 零贡献。

## 当前正式基线

2026-09-18 22:00 Finalize 后：

- 正式 Batch：`batch-01.md` ～ `batch-29.md`，共 **29** 个；
- HUMAN-A：`S001–S288`，共 **288** 个；
- 最大编号：`S288`；
- 下一保留编号：**`S289`**；
- 最近正式新增：`S288`，共 **1** 个；
- `S280–S288` 的 Canonical 映射留待 periodic review，不因单日热点修改 Curriculum。

## 当前 Inbox

### 2026-09-19 Afternoon — 待 22:00 Finalize（1 个流程）

#### 阳光电源｜AI 应用开发工程师｜一面｜面试 2026-09-18 10:00｜HUMAN-A candidate

作者：`小红不是绿`

来源：https://www.nowcoder.com/feed/main/detail/122fd928ee824ed99c8f834233d1ac23?sourceSSR=enterprise

准入证据：

- 原始详情 URL 在本轮可通过 exact URL 检索并完整回读正文；面试时间、公司、岗位均明确，正文以 `#发面经攒人品 #秋招面试记录` 发布。
- 作者主页显示为大连大学 2027 Java 候选人，近期连续记录 BIGO、上海华力、阳光电源等本人求职流程，符合个人 Candidate Timeline，非批量内容账号。
- Role Scope 由标题直接确认 `AI应用开发工程师`；问题主体覆盖 Production Incident Diagnosis、RAG、异构 PDF Parsing、Function Calling 与端到端 Ownership。
- 在进入 Inbox 前已逐个直接回读 `batch-01.md`～`batch-29.md` 全历史；未发现同 URL、同作者、同公司 / 日期 / 岗位，或相同的连续独特题序。GitHub Search 0 命中只作辅助，不作为未收录证明。

完整现场问题（按原文语义保留）：

1. 自我介绍。
2. 项目里如果线上支付失败，整个执行 / 诊断链路怎样走？
3. 为什么链路中需要 Network 这一层？
4. RAG 召回率低可能有哪些原因，怎样改进？
5. PDF 中同时存在表格和图片时怎样解析？
6. 原文写作：`MPC和Function Calling的区别`。
7. 实习做客户端、项目更偏 AI 应用 / 后端，为什么这样选择，未来职业规划是什么？
8. 更喜欢专注一个局部 Component，还是端到端参与整个产品 / 系统？
9. 如果时间和资源更充足，当前实习 / 项目下一步会怎样改进？
10. 反问。

备注：原文第 6 题写作 `MPC`，当前不自行修正为 `MCP`，留待后续若作者正文有明确更正再处理。

状态：已通过 17:00 HUMAN-A + Role Scope + 全历史去重；**暂不分配 `S289`**。22:00 Finalize 必须重新直接回读全部历史 Batch，再决定是否正式编号和进入当日日 Batch。

## 最近一次已归档

2026-09-18 Afternoon 暂存的蚂蚁 AI Native / Agent 应用方向一面已在 22:00 再次直接回读全部历史 Batch并完成最终去重，归入 `batch-29.md`：

`S288` 蚂蚁 AI Native / Agent 应用方向一面（作者 `Decadeqqq`）。

未通过稳定原帖 / 作者归属 / Role Scope / 技术密度 / 去重 Gate 的高密度线索继续不进入 Inbox；如后续补齐证据，必须从头重新执行 HUMAN-A 与全历史去重，而不是沿用旧搜索摘要直接升级。
