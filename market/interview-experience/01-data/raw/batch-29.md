# Batch 29 一手面试流程

采集日期：2026-09-18

## S288 蚂蚁｜AI Native / Agent 应用方向｜一面 + 二面（同一招聘流程合并）｜面试 2026-09-15 / 09-21｜HUMAN-A

作者：`Decadeqqq`

一面来源：https://www.nowcoder.com/feed/main/detail/754ac010a05e4090a05d7ba4d06c757f?sourceSSR=enterprise

二面来源：https://www.nowcoder.com/feed/main/detail/52b419448b854e24bbdf41ca9e6ffe06?sourceSSR=enterprise

真人 / 第一人称证据：一面原帖稳定可直接回读；作者以“发面经攒人品”“被问穿了”记录本人现场，随后按顺序列出 24 个连续问题，没有标准答案或教学包装。2026-09-22 又稳定回读到作者本人 9.21 蚂蚁二面，标题直接标记二面并继续以“发面经攒人品”记录 13 个连续问题。作者 Timeline 还能串起 Shopee、得物、PDD 等本人求职流程，个人候选人身份稳定。两轮作者、公司与招聘时间线一致，按流程级去重规则合并为 `S288`，不因二面增加 Source Count。

Role Scope：正式岗位名称 / BU 没有稳定公开，因此不猜组织信息；但两轮技术主体持续围绕 Agent 写链路、Long-task Harness、Agent Runtime、Knowledge / Skill、Permission、AI Native Platform / SDLC、Agent Evaluation / Gate / Review Agent 与 Plugin 化，实际职责明确属于本库允许的 AI Application / Agent 范围。

一面代表性技术链：

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

二面新增追问深度：

1. 介绍最近做的 AI 项目，Agent Runtime 怎样设计？
2. Knowledge Base 与 Skills 分别承载什么，怎样验证它们覆盖真实业务场景？
3. Agent Read / Write Operation 分别怎样鉴权和控制风险；为什么写操作最终仍跳转工单由用户确认？
4. Long-running Task 中怎样用 Plan 防止盲目调用工具和丢失全局方向？
5. 如果继续推进一年的 AI Native 建设，应怎样分阶段规划 Roadmap？
6. 如何补齐平台 CLI / Skills 暴露，并把 Frontend Interaction 改造成 Agent-centric？
7. 研发、测试、验收和沟通流程如何进一步 AI Native 化？
8. 如果业务方只给 Service Goal 和 Traffic Intent，由 Agent 全面托管后续操作，系统怎样设计？
9. 面向具体业务自研 Agent 与基于通用 Base Agent 开发 Plugin，各有什么 Trade-off？
10. Tool / Memory / Permission Management / Agent Loop 全面 Plugin 化意味着什么？
11. 实习与职业规划等招聘流程问题。

去重：一面正式编号前已逐个回读 `batch-01.md`～`batch-28.md`，未发现当前 URL、作者 `Decadeqqq` 或同场连续题序。2026-09-22 Finalize 再次回读全历史并确认 9.21 二面与 `S288` 作者、公司、招聘 Timeline 明确一致，因此按“同候选人 + 同公司 + 同招聘流程多轮合并”规则回并到最早 Source；二面不分配新 `Sxxx`。

---

