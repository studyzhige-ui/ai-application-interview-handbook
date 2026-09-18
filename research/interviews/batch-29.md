# Batch 29 — 2026-09-18 Daily HUMAN-A Continuous Monitoring

采集日期：2026-09-18

> 本批合并当天 10:00 / 17:00 / 22:00 三次最近 72 小时持续检索。正式归档前重新直接回读 `batch-01.md`～`batch-28.md` 全历史执行最终去重。
>
> 本批正式新增 **1 个 HUMAN-A 独立招聘流程：`S288`**。新增先进入 Research 证据层；Canonical / Curriculum 不因单日新增自动调整。

---

## S288 蚂蚁｜AI Native / Agent 应用方向｜一面｜面试 2026-09-15 · 发布 2026-09-17｜HUMAN-A

作者：`Decadeqqq`

来源：https://www.nowcoder.com/feed/main/detail/754ac010a05e4090a05d7ba4d06c757f?sourceSSR=enterprise

真人 / 第一人称证据：原帖稳定可直接回读；作者以“发面经攒人品”“被问穿了”记录本人一面，随后按现场顺序列出 24 个连续问题，没有标准答案或教学包装。作者 Timeline 还能串起 Shopee、得物、PDD 等本人求职流程，个人候选人身份稳定。

Role Scope：正式岗位名称 / BU 没有稳定公开，因此不猜组织信息；但整场技术主体持续围绕 Agent 写链路、Long-task Harness、开源 Agent Framework 定制、AI Native Platform API、Agent Evaluation / Gate / Review Agent，实际职责明确属于本库允许的 AI Application / Agent 范围。

代表性技术链：

1. 为什么引入 Agent；带副作用的写操作有哪些风险？
2. 如果 Agent 完全接管写链路，怎样设计确定性保护与完整执行链？
3. 写能力应以怎样的 Tool / Interface 暴露给 Agent？
4. Long-running Task 怎样管理；Plan / Todo 之外，Harness 与 Backend API 分别承担什么？
5. 当前 Agent 怎样实现，为什么基于开源 Agent Framework 做定制？
6. 自定义能力与 Claude Hooks / Plugins / Extensions 有什么区别？
7. 直接修改 Framework Kernel 与围绕既有 Extension 机制扩展，各自 Trade-off 是什么？
8. AI Native 应从用户、开发者和平台哪些维度定义？
9. 平台外部 API 在 AI Native 场景下要怎样重新设计？
10. Zod / Schema 只能解决参数格式时，跨字段隐性业务约束怎样校验并向 Agent 暴露错误？
11. Agent Eval / Iteration 怎样做；Gate 是什么、看哪些 Metric？
12. Review Agent 怎样工作；Review Agent 自己 Hallucinate 时怎样约束？
13. 这些方案是否做过 Alternatives / Trade-off 对比，怎样证明不是拍脑袋？
14. 面对新技术怎样学习、验证并真正落地？

去重：正式编号前再次逐个回读 `batch-01.md`～`batch-28.md`。未发现当前 URL、作者 `Decadeqqq`，也未发现“写链路风险 → Harness / Backend 双视角长任务 → Framework Kernel vs Extensions → AI Native API / Zod / 业务语义错误 → Eval Gate / Review Agent”的 5–10+ 连续独特题序同场来源。GitHub / Search 的 0 命中只作辅助，不作为未收录证明。

---

# 当日最终清洗 / 明确排除

- **千问技术部 9/16 一面｜同作者 `Decadeqqq`**：原帖稳定、1h15min、Plan / Replan、Tool Calling、Context、Reconnect、Evaluation、Review Agent 等技术密度很高；但前一日已因岗位主体无法稳定确认属于 AI Application / Agent Role Scope 而排除。晚间没有获得新的职位 / 招聘主体证据，因此维持原判断，不因同作者已有合格蚂蚁流程而顺带放行。
- **4399 Agent 开发 9/18｜`AAA野生原子弹批发`**：搜索结果与作者主页能确认当天确有 `agent开发` 面试和个人求职 Timeline，但当前稳定入口只暴露前几道问题及“14 道真题”提示，直接原帖详情仍无法稳定回读，无法完整核验 A-grade 技术链；保留为后续追源线索，零贡献。
- **快手 9/17 AI 应用开发一 / 二面**：继续没有补到稳定可直接回读的候选人原帖；企业页 / 搜索片段不能替代原始正文，零贡献。
- **水滴 9/17 AI 全栈**：当前可核验的是笔试，不是 Human Interviewer，排除。
- **百度 9/17 后端一面**：真人第一人称且问到 AI 应用平台、Agent 与 Workflow，但岗位主体仍是普通后端，Role Scope 排除。
- **JD / 企业页 / 聚合 / 题库 / 面经索引 / 标准答案页**：只作为市场旁证或 Recall，不贡献 HUMAN-A。

# 当日三轮监测摘要

- Three-round search effort：**至少 245 组 Query / Query 变体**（Morning ≥60 + Afternoon ≥85 + Evening ≥100）。
- Three-round verification effort：**至少 70 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试；这是工作量次数，不代表 70 个唯一 URL。
- Final additions：**1 个 HUMAN-A，`S288`**。
- Current formal library：**29 Batch / 288 HUMAN-A / `S001–S288`**。
- Next ID：**`S289`**。
- Inbox：归档后清空。
- Canonical / Curriculum：**本日不修改**；`S288` 进入后续 periodic mapping / review。

当日主要市场信号：

1. Agent 安全正在从“输出会不会幻觉”继续下沉到**有副作用写操作、权限、Tool / API Contract 与业务语义 Validation**；
2. Long-task / Harness 不只考 Loop，而开始与 Backend API、恢复、扩展机制和 Framework Kernel Trade-off 联动；
3. Eval 从“做过评测”进入 Gate / Metric / Review Agent 可靠性；
4. Agent / Skill / AI Coding 已明显向普通 Backend、Data、Test 岗扩散，因此 Role Scope Gate 必须比过去更严格；
5. Foundation / Production Engineering 仍是最新 Agent 能力的承载层，不能被新名词替代。

饱和度 / 盲区：最近 72 小时公开热门层继续表现为**局部饱和 + provenance 成本高**。牛客仍最容易拿到可核验原帖，但新结果大量落在笔试、聚合、内容账号、普通岗位 AI 项目追问或原帖不可稳定回读；腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo 等目标公司以及小红书 / 知乎 / 脉脉 / 独立博客，在严格 Gate 下仍缺新的目标岗高密度第一人称样本。下一轮继续追 4399 9/18 Agent、快手 9/17 AI 应用一 / 二面及跨平台作者源，不降低 Gate。
