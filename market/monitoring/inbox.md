# HUMAN-A Monitoring Inbox

更新日期：2026-09-22

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

2026-09-22 17:00 Afternoon Search 在新增候选进入 Inbox 前，再次逐个直接回读 `market/interviews/batch-01.md` ～ `batch-31.md` 全历史，确认当前正式 Market 基线仍为：

- 正式 Batch：`batch-01.md` ～ `batch-31.md`，共 **31** 个；
- HUMAN-A：`S001–S291`，共 **291** 个；
- 最大编号：`S291`；
- 下一保留编号：**`S292`**；
- `interview/canonical/` Frozen Canonical、`market/analysis/` Frozen 统计与 Curriculum 本轮均不修改。

## 当前 Inbox

当前共有 **3 个独立招聘流程**通过 HUMAN-A + Role Scope + Stable Original + 全历史去重 Gate。Candidate A / B 为 2026-09-21 Afternoon 已通过但因当晚 Finalize 未落库而保留的 backlog；Candidate C 为 2026-09-22 Afternoon 新增。三条均来自真实候选人 `SOLDIER_627`，但公司不同，属于独立招聘流程；Afternoon 不分配 `Sxxx`，等待 22:00 Finalize 再次全历史去重。

### Candidate A — 小红书｜Agent 平台研发｜一面｜发布 2026-09-20 14:15

- 作者：`SOLDIER_627`（牛客用户 ID `523469060`，同济大学 2027 Java，上海）。
- 原始来源：https://www.nowcoder.com/discuss/931189826643066880?sourceSSR=enterprise
- 现场 / 招聘证据：post-specific 原帖可稳定直接回读，标题明确为 `小红书 Agent 平台研发一面`，净时长约 29 分钟；作者在评论中补充“面试官迟到 + 面完秒挂”。作者主页为连续个人求职 Timeline，不是内容账号。
- Role Scope：岗位标题直接为 Agent 平台研发；通过目标 Role Scope。
- 整场技术 / 现场问题：
  1. 自我介绍。
  2. 上一段实习实际体验如何，工作状态是否与预期一致？
  3. 所在团队主要做什么业务，候选人负责内容与团队主线有什么差异？
  4. 后续更想做 Agent 相关岗位还是后端岗位？
  5. 实习中有没有遇到认为不够好的同事；怎样定义真正优秀的同事？
  6. 最近有什么让自己幸福或骄傲的事情？
  7. System Design：底层只有一张 MySQL 商品详情表，设计可支撑 **10 万 QPS** 且可水平扩展的商品详情查询服务；直播间用户点击商品会调用该服务。
  8. 管理端修改商品价格后，怎样完整设计 Cache Update / Invalidation 链路，让 C 端及时看到新价格？
  9. Coding：Longest Palindromic Substring / 最长回文字符串。
- 全历史去重：已直接回读 `batch-01.md`～`batch-31.md`。历史确有同一候选人的其它公司流程，例如快手 AI 全栈与美团 AI 后端，但不同公司 / 不同招聘流程按规则独立计数；未发现当前小红书 URL、公司流程或“Agent 平台岗位 → 10 万 QPS 商品详情 + 缓存新鲜度 → 最长回文”连续题序的同场来源。GitHub Search 0 命中仅作辅助。
- Status：**PASSED → pending Evening Finalize；不分配 ID。**

### Candidate B — 字节跳动｜AI 全栈（飞书）｜一面｜发布 2026-09-21 14:28

- 作者：`SOLDIER_627`。
- 原始来源：https://www.nowcoder.com/discuss/931555466247700480?sourceSSR=users
- 现场 / 招聘证据：post-specific 原帖可稳定直接回读，标题明确 `字节 AI 全栈一面（飞书）`，净时长约 1 小时；同一作者主页在最近数日连续记录小红书、百度、度小满、快手、美团等本人求职流程，Candidate Timeline 稳定。
- Role Scope：标题直接为 AI 全栈，且 Agent / Skill 是项目验真主线之一；通过目标 Role Scope。
- 整场技术问题：
  1. 自我介绍。
  2. 介绍 Agent 项目的整体技术架构和工作原理。
  3. Agent 不遵循 Skill 中的限制 / 描述时怎样治理？
  4. 是否尝试把 Skill 规则放入更底层、优先级更高的规范以提高遵从性？这种做法的边界是什么？
  5. 视频分析项目完整处理链路是什么？
  6. 海量监控视频如何避免高内存占用 / OOM；多个长视频串行还是并行，处理时延如何？
  7. 分块上传如何保证成功；断点续传、一致性和清理逻辑怎样实现？
  8. 视频物理存储在哪里；合并失败时怎样清理中间状态 / 文件？
  9. MySQL Index 使用什么数据结构，如何组织与工作？
  10. SQL 需要数百毫秒时怎样定位 / 优化？
  11. SQL 已从 800ms 优化到 50ms，但整体接口仍慢，怎样继续端到端定位？
  12. 接口总耗时 80ms、单次 SQL 10ms 时，还能从 Cache、Concurrency、其它链路哪些部分优化？
  13. Coding：两个最长可达 10 万位的十进制大整数字符串相加。
  14. 最大堆 / 最小堆原理。
  15. HashMap 机制。
  16. Consistent Hashing / 一致性哈希。
- 全历史去重：已直接回读 `batch-01.md`～`batch-31.md`。同一候选人历史其它公司流程不跨公司合并；未发现当前字节 / 飞书流程、URL 或“Agent Skill 遵从性 → 海量视频 OOM / 断点续传 / 清理 → SQL 端到端性能 → 大数 / Heap / HashMap / Consistent Hashing”的连续题序同场来源。GitHub Search 0 命中仅作辅助。
- Status：**PASSED → pending Evening Finalize；不分配 ID。**

### Candidate C — 度小满｜AI 全栈｜一面｜发布 2026-09-20 17:39

- 作者：`SOLDIER_627`（同济大学 2027 Java，上海）。
- 原始来源：https://www.nowcoder.com/discuss/931241025345978368?sourceSSR=post&weFlow=true
- 备用同源入口：https://ac.nowcoder.com/discuss/1677258?type=0
- 现场 / 招聘证据：post-specific 原帖本轮已恢复为稳定可直接回读，标题明确 `度小满AI全栈一面`，作者给出净面试时长约 **53 分钟**；题目按真实面试顺序记录，Coding 要求先讲思路再现场编码并运行通过。作者主页与小红书、字节、百度、美团、快手等本人流程形成连续 Candidate Timeline，不是内容账号。
- Role Scope：岗位标题直接为 AI 全栈；面试官还明确围绕候选人“主要做后端和 Agent”追前端参与度，后段继续要求设计 AI 问答功能，属于目标 AI Full-stack / Application 范围。
- 整场技术问题：
  1. 自我介绍。
  2. 做过项目里最有挑战的功能是什么，Pain Point 与解决方式是什么？
  3. 候选人主要做 Backend 与 Agent，Frontend 实际参与到什么程度？
  4. 从输入 URL 到页面打开经历什么；TCP 三次握手为什么这样设计？
  5. HTTP 502 / 504 分别是什么；301 / 302 有什么区别？
  6. Process 与 Thread 的区别；浏览器为什么采用多进程架构？
  7. 是否了解 Go；GMP Scheduler 怎样工作？
  8. MySQL 为什么选择 B+Tree，而不是 Hash / Binary Tree / B-Tree；Index Invalid 常见形式有哪些？
  9. Redis 为什么快；Cache Avalanche / Breakdown / Penetration 怎样治理？
  10. CSS `flex: 1` 的含义是什么？
  11. CORS / 跨域是什么，如何处理？
  12. 常见 Frontend Framework 与工程选型怎样理解？
  13. Debounce 与 Throttle 的差异和适用场景是什么？
  14. AI-assisted Development 中最印象深刻的 Case 是什么；团队 / 个人采用度、收益、坑和 AI 最不擅长的部分怎样评价？
  15. System Design：从 Frontend / Backend、用户体验、安全和工程实现角度设计一个 AI Q&A 功能。
  16. Coding：Restore IP Addresses / 复原 IP 地址；先解释思路，再现场编码并运行通过。
- 全历史去重：写入 Inbox 前已逐个直接回读 `batch-01.md`～`batch-31.md` 全历史。历史存在同一作者的其它公司流程，但未发现度小满同公司 / 同招聘流程、当前 URL，或“浏览器 / 网络 → OS / GMP → MySQL / Redis → Frontend 基础 → AI-assisted Development → AI Q&A System Design → Restore IP”连续题序的同场来源。同作者不同公司按规则分别计数。GitHub 对标题、URL ID 与“作者 + 度小满”的 0 命中只作辅助，不替代全历史正文去重。
- Status：**PASSED → pending Evening Finalize；不分配 ID。**
