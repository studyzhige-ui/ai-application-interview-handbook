# Batch 30 — 2026-09-19 Daily HUMAN-A Continuous Monitoring

采集日期：2026-09-19

> 当天 10:00 / 17:00 / 22:00 三次检索合并为一个正式日批次。主动发现窗口严格限定为运行时最近 3 天；正式归档前再次逐个直接回读 `batch-01.md`～`batch-29.md` 全历史执行去重。
>
> 本批正式新增 **1 个 HUMAN-A 独立招聘流程：`S289`**。新增来源只进入 Market Evidence；`interview/canonical/` 的 Frozen Canonical Baseline 与 Curriculum 不因单日新增自动调整。

---

## S289 阳光电源｜AI 应用开发工程师｜一面｜面试 2026-09-18 10:00，发布 2026-09-18｜HUMAN-A

作者：`小红不是绿`

来源：https://www.nowcoder.com/feed/main/detail/122fd928ee824ed99c8f834233d1ac23?sourceSSR=enterprise

真人 / 第一人称证据：原始 post-specific 详情页可稳定直接回读，作者以 `#发面经攒人品 #秋招面试记录` 发布本人阳光电源一面，明确给出面试公司、时间与岗位；作者 Timeline 还能连续串起 BIGO、上海华力、阳光电源等本人求职流程，符合个人候选人账号特征，不是批量内容号、合集或答案帖。

Role Scope：标题直接标注 `AI应用开发工程师`。整场从 Production Incident Diagnosis 进入 RAG Failure Attribution、异构 PDF Parsing、Function Calling 边界和端到端 Ownership，明确属于本库 AI Application Role Scope。

整场技术问题（按原文语义保留）：

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

原文保真：第 6 题原帖确实写作 `MPC`，本库不自行修正为 `MCP`；若后续作者原文明确更正，再按来源更新。

去重：22:00 Finalize 前已再次逐个直接回读 `batch-01.md`～`batch-29.md` 全历史，并核验 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义与连续题序。未发现同 URL、同作者、同公司同流程，亦未发现“支付失败全链路 → Network → RAG 低召回 → 异构 PDF → Function Calling 边界 → 端到端 Ownership”的同场来源。GitHub Code Search 对 URL / 作者 / 独特组合的 0 命中仅作为辅助证据，不代替全历史回读。

---

# 当日最终清洗 / 明确排除

以下近期高密度线索在 22:00 仍然 **零贡献**，没有为了新增数量降低 Gate：

- **4399 Agent 开发 9/18｜作者 `AAA野生原子弹批发`**：作者 Timeline、目标 Role Scope 与 14 道连续题序都很强，可见 Harness Architecture、10 万级日志、Agent 生成 SQL 错误检测、90% 测试通过率来源以及“如何证明不是只依赖 AI 工具”等问题；但仍未稳定拿到 post-specific 原始详情页，作者索引 / Search Snippet 不能替代 Stable Original，继续待追源。
- **快手 9/17 AI 应用开发一 / 二面**：推荐 / 企业入口仍能看到长任务崩溃恢复、并发修改会话记忆等高价值问题，但候选人原始详情正文与 provenance 仍不够稳定，且部分展示片段混入解释 / 答案式展开；继续排除。
- **PDD / B站 / 腾讯等“面经 06/07/08”“完整答案”“Agent 面经总结”页面**：属于合集、内容账号或答案化整理，不是候选人本人单一招聘流程原始证据。
- **OPPO 9/18 线下面、9/17 数据 / 测试等普通工程岗位**：真人面试中已经出现 AI Memory、AI Development Flow 等内容，但岗位主体并非 AI Application / Agent；继续按 Role Scope 排除。
- **小红书近期多模态算法 / 端侧推理等结果**：岗位主体落在模型 / 算法 / 推理优化边界，不因为出现 Agent 术语扩大本库范围。
- **招聘 JD、企业职位页、聚合页、内推、题库与新闻**：仅用于发现线索或理解市场，不贡献 HUMAN-A。

# 2026-09-19 Final Summary

- Three-round search effort：**至少 300 组 Query / Query 变体**（Morning ≥90 + Afternoon ≥110 + Evening ≥100）。
- Three-round verification effort：**至少 65 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 20+ + Afternoon 25+ + Evening 20+）；这是工作量次数，不代表 65 个唯一 URL。
- Final additions：**1 个 HUMAN-A：`S289`**。
- Current formal Market library：**30 Batch / 289 HUMAN-A / `S001–S289`**。
- Next ID：**`S290`**。
- Inbox：归档后清空。
- Frozen Canonical / Curriculum：**本日不修改**；`S289` 只进入后续 periodic canonical mapping / review candidate。

当日主要市场信号：

1. **AI Application 项目验真继续落到 Production Diagnosis。** 面试官不只问 RAG / Function Calling 名词，而是要求从线上支付失败完整链路解释系统如何定位问题，并追 Network 为什么存在。
2. **Retrieval Failure Attribution 与异构文档处理仍是稳定工程问题。** RAG 低召回要能分层定位原因；PDF 表格 / 图片需要给出实际解析链路，而不是只报 Parser 名称。
3. **End-to-end Ownership 被直接验证。** 候选人会被问更偏局部 Component 还是全链路参与，以及资源充分时下一步怎样演进系统。
4. **Harness + AI-assisted Engineering Authenticity Verification 是值得继续追的弱信号。** 4399 线索已经把 Harness、SQL 验错、测试指标和“AI 帮你完成后是否真正掌握”放在一起，但 provenance 尚未闭环，因此当前只作为观察，不进入正式频率。
5. **Agent / AI 术语继续向普通 Backend / Data / Test 岗扩散。** 这使 Role Scope Gate 更重要，而不是更宽松；出现 Memory / Agent / AI Coding 不能替代目标岗位证据。

饱和度 / 盲区：最近 72 小时公开结果层继续呈现**局部饱和 + provenance 成本高**。牛客仍是最容易拿到稳定第一人称原帖的平台，但内容合集、答案化页面、普通岗位 AI 深挖与原帖不稳定占比较高；4399 9/18 Agent、快手 9/17 AI 应用一 / 二面仍是最值得继续补 provenance 的近端线索。腾讯 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米等目标公司，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客平台，在当前窗口内仍缺新的高质量、稳定可核验目标岗第一人称来源。继续补盲，但不降低 Gate。
