# Batch 31 — 2026-09-20 Daily HUMAN-A Continuous Monitoring

采集日期：2026-09-20

> 当天 10:00 / 17:00 / 22:00 三次最近 72 小时持续检索合并为一个正式日批次。正式归档前再次逐个直接回读 `market/interviews/batch-01.md`～`batch-30.md` 全历史执行最终去重。
>
> 本批正式新增 **2 个 HUMAN-A 独立招聘流程：`S290–S291`**。两条来源来自同一真实候选人，但公司不同、招聘流程独立，因此分别计数。新增只进入 Market Evidence；Frozen Canonical / Curriculum 不因单日新增自动调整。

---

## S290 小红书｜AI 全栈开发实习｜一面｜面试 2026-08-25，发布 2026-09-18 15:43｜HUMAN-A

作者：`中二的西红柿起床了`

来源：https://www.nowcoder.com/feed/main/detail/c712eda7fbf44ba69835b6dd2ff7fc4c?sourceSSR=enterprise

真人 / 第一人称证据：post-specific 原始正文可稳定直接回读。作者明确以本人“8.25 小红书实习 AI 全栈开发实习一面挂凉经”复盘，记录“大部分时间都在问项目”“面试官不断提问让我说服他”“我终于投降了”“一面挂”等现场状态；同一账号还存在长期个人学业 / 求职记录及本周 Shopee 本人面经，候选人 Timeline 连续，不是批量内容号。

Role Scope：标题直接标注 AI 全栈开发实习；约 40 分钟主体持续围绕 Multi-Agent、Skill、RAG / Vector DB、Harness、Evaluation / Outcome 与项目真实性验真，明确属于 AI Full-stack / Agent Application 范围。

整场技术问题：

1. 自我介绍。
2. 项目到底解决什么问题，为什么要做成 Multi-Agent？
3. Multi-Agent 怎样编排；为什么不能用更简单的 Single-Agent / Workflow？面试官持续追问，要求候选人真正证明 Architecture Choice。
4. Skill 是什么，在项目中承担什么职责？
5. 项目中的 RAG 怎样实现，Vector Database 怎样使用？
6. 是否了解 Harness；Harness 与当前项目架构是什么关系？
7. 项目怎样 Evaluation，真实成果是什么？
8. 同事 / 使用者是否给过真实反馈，准确率怎样，指标如何得到？
9. 是否做过面试官指定的进一步功能；候选人对未覆盖部分明确承认没有想到。
10. 反问；无手撕、无传统八股，项目深挖约 40 分钟，一面未通过。

去重：正式编号前再次逐个直接回读 `batch-01.md`～`batch-30.md`。未发现当前 URL、作者，或“Multi-Agent 必要性反复论证 → Skill → RAG / Vector DB → Harness → Evaluation / 同事反馈 / 准确率验真”的连续同场来源。历史虽已有多条小红书 AI Full-stack / Agent 来源，但作者、日期、项目和题序均不同。GitHub / Search 对 exact URL / 作者的 0 命中仅作辅助，不作为未收录证明。

---

## S291 Shopee｜Chatbot 研发实习｜一面｜面试 2026-09-18，发布 2026-09-19 16:25｜HUMAN-A

作者：`中二的西红柿起床了`

来源：https://www.nowcoder.com/feed/main/detail/9f02a7f8009d4aca9fc730a18b9f96cc

真人 / 第一人称证据：post-specific 原始正文可稳定直接回读。作者逐题记录本人回答、停顿和不会的状态：第 K 大先回答排序，被继续追 Quick Sort 复杂度、原理和手写，随后明确记录“不会”“发呆”，最后用 `sort` 两行完成；文末写全程 20 多分钟和面后自评，现场痕迹强。与 `S290` 为同一候选人，但公司不同、招聘流程独立，按规则分别计数。

Role Scope：岗位标题为 `chatbot研发实习`，技术主体连续覆盖 Agent、Function Call / Tool / MCP、RAG、AI Coding，并混合 Linux 与 Algorithm Foundation；实际职责明确属于 AI Application / Agent Chatbot 研发，不是普通 Backend 顺带问 AI。

整场技术问题：

1. 自我介绍。
2. 什么是 Agent？
3. Function Call、Tool、MCP 分别是什么，怎样区分？
4. 项目的 RAG 怎样做，承载多大文档？
5. Linux 常用命令有哪些，怎样查看 Process？
6. Coding：数组中第 K 大元素；候选人先回答排序后取第 K 个。
7. 继续追 Quick Sort：时间复杂度是多少、具体怎样排序、为什么是该复杂度、能否现场写出 Quick Sort？
8. 除 Quick Sort 外还有什么方法？候选人现场停顿，最终使用 `sort` 两行完成。
9. 平时是否 AI Coding，有什么实际方法？
10. 反问；整场约 20 多分钟。

去重：正式编号前再次逐个直接回读 `batch-01.md`～`batch-30.md`。历史已有 Shopee `S081`、`S239` 等 Agent 来源，但均为不同作者、不同月份 / 日期与独立流程；未发现当前 URL、作者或“Agent → Function Call / Tool / MCP → RAG 文档规模 → Linux Process → Kth Largest / Quick Sort 深追 → AI Coding”的连续同场来源。

---

# 当日最终清洗 / 明确排除

以下近期高密度结果仍然 **零贡献**，原因是 Stable Original / Candidate Provenance / Role Scope / 全历史去重 Gate 未完整通过：

- **字节广告团队 Agent 一 / 二面｜发布 2026-09-19 17:07**：搜索层可完整看到 Redis Distributed Lock、MySQL Clustered Index、内部 Skill 平台上传 / 下载 / 发布、本地 Runtime、AI 提效、营销秒杀 System Design、现场 Demo、Skill vs Function Call 与 Coding；但 post-specific 页面直接回读仍只返回页面壳，作者账号 / Timeline 无法稳定闭环。高价值但 provenance 不足，继续待追源，不因题目前沿而降低 Stable Original Gate。
- **4399 Agent 开发｜面试 2026-09-18｜`AAA野生原子弹批发`**：作者主页能稳定确认个人求职 Timeline，并能看到“证明不是只依赖 AI、十万级日志、Harness、Agent SQL 验错、90% 测试通过率”等 14 道问题；但仍未取得可长期稳定直接回读的 post-specific 原帖详情正文。作者索引 / Search Snippet 不替代原始详情页。
- **快手 AI 全栈 `明天会有好天气`**：全历史直接回读确认就是既有 `S282`，属于精确历史重复。
- **携程 9/18 AI 应用开发一 / 二面、腾讯 9/18 AI 全栈、小红书 9/20 Agent 平台研发**：当前主要依赖企业 / 话题索引或 Search Cache，post-specific 原始正文与作者 provenance 未完整闭环；零贡献。
- **B站 9/19 “大模型面试岗”**：正文明确是内容作者让一位学员复述面试，属于二手转述，不是候选人本人第一人称；且岗位偏算法。
- **普通 Backend / Data / Test 岗近期 Agent / Memory / AI Coding 深挖**：不能用“问到 AI”替代目标 Role Scope；继续排除。
- **合集 / 标准答案 / 内容号 / JD / 内推 / 聚合 / 新闻**：只用于发现与市场旁证，不贡献 HUMAN-A。

# 2026-09-20 Final Summary

- Three-round search effort：**至少 300 组 Query / Query 变体**（Morning ≥100 + Afternoon ≥100 + Evening ≥100）。
- Three-round verification effort：**至少 75 次**候选原帖 / 作者页 / 企业页 / provenance 入口的打开、回读或追源尝试（Morning 25+ + Afternoon 30+ + Evening 20+）；这是工作量次数，不代表 75 个唯一 URL。
- Final additions：**2 个 HUMAN-A：`S290–S291`**。
- Current formal Market library：**31 Batch / 291 HUMAN-A / `S001–S291`**。
- Next ID：**`S292`**。
- Inbox：归档后清空。
- Frozen Canonical / `market/analysis/` / Curriculum：**本日不修改**；`S290–S291` 只进入后续 periodic canonical mapping / review candidate。

当日主要市场信号：

1. **Architecture Choice 必须被证明。** “做了 Multi-Agent”已经不够；真实面试会持续追为什么必须 Multi-Agent、为什么不能更简单、怎样编排，以及结果 / 准确率 / 使用者反馈怎样证明架构值得存在。
2. **Agent / MCP / RAG 仍与 Foundation 同场。** Shopee Chatbot 把 Agent、Function Call / Tool / MCP、RAG 与 Linux Process、Quick Sort 深追和 AI Coding 放在一场面试里，说明应用岗基础工程与算法能力不能弱化。
3. **Skill / Runtime 正继续向平台级设计与现场验真下沉。** 字节广告团队待追源样本已经问内部 Skill Platform 的上传 / 下载 / 发布、本地 Runtime、现场 Demo 与 Skill vs Function Call；但 provenance 尚未闭环，因此当前只作为 Market Observation，不计正式频率。
4. **AI-assisted Engineering 的真实性验证继续增强。** 4399 待追源样本同时追 Harness、SQL 验错、测试通过率来源和“如何证明不是只依赖 AI 工具”，值得继续监测，但当前不进入正式 HUMAN-A。
5. **Role Scope Gate 需要继续收紧。** Agent / Memory / AI Coding 已扩散到普通 Backend / Data / Test 岗；术语出现本身越来越不能证明目标岗位职责。

饱和度 / 盲区：最近 72 小时公开热门层继续呈现**局部饱和 + 高 provenance 成本**。牛客仍是最容易取得稳定候选人原帖的平台，但企业聚合、Search Cache、答案化页面和 post-specific Cache Miss 占比较高；字节广告团队、4399、携程、腾讯 AI 全栈、小红书 Agent 平台研发仍是值得追 provenance 的近端线索。腾讯 / 美团 / 百度 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米等目标公司，以及小红书 / 知乎 / 脉脉 / 独立博客等非牛客平台，在当前窗口内仍缺更多稳定可核验的新目标岗第一人称来源。继续补盲，但不降低 Gate。
