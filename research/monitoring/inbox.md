# HUMAN-A Monitoring Inbox

更新日期：2026-09-17

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

2026-09-16 22:00 Finalize 后：

- 正式 Batch：`batch-01.md` ～ `batch-27.md`，共 **27** 个；
- HUMAN-A：`S001–S286`，共 **286** 个；
- 最大编号：`S286`；
- 下一保留编号：**`S287`**；
- 最近正式新增：`S280–S286`，共 **7** 个；
- `S280–S286` 的 Canonical 映射留待 periodic review，不因单日热点修改 Curriculum。

## 当前 Inbox

### 2026-09-17 Afternoon — 字节｜Agent｜秋招一面｜发布 2026-09-16 15:09

来源：https://www.nowcoder.com/discuss/929731481189044224

作者：`吃饱了撑的容器`。原帖页面显示作者当前身份为“小红书 Agent 开发（实习员工）”，正文明确记录“当天下午已约二面”，并写出与真人面试官讨论 Computer Use、Pi Agent、DeepSeek Harness 的现场感受；属于候选人本人第一人称招聘流程，不是答案帖 / 合集。

Role Scope：标题直接为“字节 Agent 秋招一面”，整场围绕企业 AI 助手、Agent Harness、Computer Use、AI Coding 展开，明确通过目标岗位 Gate。

高密度连续题序：

1. 实习项目深挖；
2. 企业 AI 助手的滑动窗口 + 摘要压缩记忆怎样实现；滑动窗口大小如何决定、什么场景改用摘要压缩；
3. 文档在线自动更新怎样保证并发幂等、避免任务覆盖；RocketMQ 放在更新链路哪里；为什么使用 MQ 而不是定时任务直接处理；
4. 对 Agent / Agent Harness 的理解；DeepSeek Harness、Pi Agent；如果接入当前实习 Agent 应怎样改、是否值得替换；
5. 其它厂商 Agent 产品；Claude Code Context Compression；
6. Computer Use 的本地电脑 / 云端电脑执行机制；
7. AI Coding 工具真实使用问题与完整开发工作流；
8. 数据库类型、MySQL B+ Tree；
9. Coding：二叉树子结构；
10. Coding：两个有序 List 交集，并继续追无限序列、Bitmap 大值域与分批流式处理；
11. 反问 Agent 垂类业务与团队 AI Coding 文化，面试官反向追问是否存在更 AI Native 的开发工作流。

去重：本轮已逐个直接回读 `batch-01.md`～`batch-27.md` 全历史。当前 URL、作者以及“滑动窗口/摘要记忆 → 文档并发幂等 + RocketMQ → DeepSeek Harness / Pi Agent → Computer Use → AI Coding Workflow → 无限序列交集”连续链均未在历史正式来源形成同场重复；GitHub Search 对 URL / 作者 / 罕见组合的 0 命中只作为辅助，不作为未收录证明。22:00 仍需重新直接回读全历史后做最终去重，届时才允许分配 `Sxxx`。

---

2026-09-16 Morning / Afternoon 暂存的 7 个候选已经在 22:00 再次直接回读全部历史 Batch 并完成最终去重，统一归入 `batch-27.md`：

`S280` 美团 AI 后端（同候选人一 / 二面合并） · `S281` 科大讯飞 Agent Harness · `S282` 快手 AI 全栈 · `S283` 美团 AI Agent · `S284` 美团 AI 后端开发 · `S285` 智谱 AI Native Builder · `S286` 小红书 AI 应用研发。

未通过稳定原帖 / 作者归属 / Role Scope / 去重 Gate 的高密度线索继续不进入 Inbox；如后续补齐证据，必须从头重新执行 HUMAN-A 与全历史去重，而不是沿用旧搜索摘要直接升级。