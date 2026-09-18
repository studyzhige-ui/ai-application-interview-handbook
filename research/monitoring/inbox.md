# HUMAN-A Monitoring Inbox

更新日期：2026-09-18

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

2026-09-17 22:00 Finalize 后：

- 正式 Batch：`batch-01.md` ～ `batch-28.md`，共 **28** 个；
- HUMAN-A：`S001–S287`，共 **287** 个；
- 最大编号：`S287`；
- 下一保留编号：**`S288`**；
- 最近正式新增：`S287`，共 **1** 个；
- `S280–S287` 的 Canonical 映射留待 periodic review，不因单日热点修改 Curriculum。

## 当前 Inbox

### 2026-09-18 Afternoon — 蚂蚁｜AI Native / Agent 应用方向（实际面试内容明确）｜一面

- 状态：**已通过 HUMAN-A + Role Scope + 全历史去重，等待 22:00 Finalize；暂不分配 `Sxxx`。**
- 作者：`Decadeqqq`
- 面试日期：2026-09-15
- 原帖发布：2026-09-17 21:17
- 来源：https://www.nowcoder.com/feed/main/detail/754ac010a05e4090a05d7ba4d06c757f?sourceSSR=enterprise

真人 / 第一人称证据：原帖现在可稳定直接回读，作者明确写“发面经攒人品”“被问穿了”，随后按现场顺序列出 24 个连续问题，没有标准答案或教学包装。作者主页可连续核验本人 9/8、9/10 Shopee、9/12 得物、PDD、字节等求职记录，长期个人候选人 Timeline 成立，不是批量面经内容号。

Role Scope：帖子没有公开稳定的正式岗位 Title / BU，因此不猜组织信息；但整场技术主体持续围绕 Agent 写链路、Long-task Harness、Agent Framework 定制、AI Native Platform API、Agent Evaluation / Gate / Review Agent，实际职责明确属于本库允许的 AI Application / Agent 范围。

代表性技术链：

1. 为什么引入 Agent；有写操作时怎样治理 Side-effect / Risk？
2. 如果让 Agent 完全接管整个写链路，Architecture 与确定性保护怎样设计？
3. Agent 本身还需要哪些约束，写能力应该通过什么接口 / Tool 暴露？
4. Long-running Task 怎样管理；除了 Plan / TodoList，还要分别从 Harness 与 Backend API 角度设计什么？
5. 当前 Agent 怎样实现，技术选型如何比较？
6. 为什么基于开源 Agent Framework 定制，而不是完全自研？
7. 定制 Framework 与 Claude Hooks / Plugins / Extensions 的边界是什么？
8. 直接修改 Framework Kernel 与基于 Extension 机制扩展，各自有哪些 Trade-off？
9. 怎样从用户、开发者、平台三个维度理解 AI Native？
10. AI Native 平台对外 API 的设计原则应发生什么变化？
11. Zod / 参数校验与 Error Handling 怎样适配 Agent 调用；业务语义错误而不是格式错误时怎样处理？
12. Agent Evaluation / Iteration 怎样做；Gate 是什么、看哪些指标？
13. Review Agent 怎样工作；Review Agent 自身 Hallucination 怎样治理？
14. 这些方案如何做 Alternatives / Trade-off 验证，而不是事后包装？
15. 遇到新技术时怎样学习并形成可落地实践？

全历史去重：进入 Inbox 前已重新逐个直接回读 `batch-01.md`～`batch-28.md`。未发现当前 URL、作者 `Decadeqqq`，也未发现“Agent 写链路风险 → Harness / Backend 双视角长任务 → Framework Kernel vs Hooks / Plugins → AI Native API / Zod / 业务错误 → Eval Gate / Review Agent”的连续独特题序同场来源。GitHub Search 对作者 / URL 的 0 命中只作辅助，不作为未收录证明。

22:00 规则：晚间第三次检索后必须再次直接回读全部历史 Batch，并重新核验作者 / 公司 / 日期 / 轮次 / 题序 / Timeline / 复制链；若仍成立，再按当时仓库真实下一编号归档。若发现同流程后续轮次，合并进同一来源，不按轮次虚增。

---

2026-09-17 Afternoon 暂存的字节 Agent 秋招一面候选已在 22:00 再次直接回读全部历史 Batch并完成最终去重，归入 `batch-28.md`：

`S287` 字节跳动 Agent 开发秋招一面（作者 `吃饱了撑的容器`）。

未通过稳定原帖 / 作者归属 / Role Scope / 技术密度 / 去重 Gate 的高密度线索继续不进入 Inbox；如后续补齐证据，必须从头重新执行 HUMAN-A 与全历史去重，而不是沿用旧搜索摘要直接升级。
