# Batch 32 一手面试流程

采集日期：2026-09-21
恢复归档：2026-09-22 22:00 Finalize

## S292 小红书｜Agent 平台研发｜一面｜发布 2026-09-20 14:15｜HUMAN-A

作者：`SOLDIER_627`

来源：https://www.nowcoder.com/discuss/931189826643066880?sourceSSR=enterprise

真人 / 第一人称证据：post-specific 原帖稳定可直接回读，作者明确记录本人一面，净时长约 29 分钟；评论区楼主补充“面试官迟到 + 面完秒挂”。作者主页持续记录多家公司本人招聘流程，个人 Candidate Timeline 连续，不是批量内容账号。

Role Scope：标题直接为 `小红书 Agent 平台研发一面`，候选人也明确被问后续更偏 Agent 还是 Backend，属于目标 Agent / AI Application 范围。

整场问题：

1. 自我介绍。
2. 上一段实习体验如何，真实工作状态是否与预期一致？
3. 所在团队的业务主线是什么，本人负责内容与团队主线有什么差异？
4. 后续更希望做 Agent 相关岗位还是 Backend？
5. 如何评价团队协作与优秀同事，哪些能力真正构成“优秀”？
6. 最近有什么让自己有成就感 / 幸福感的事情？
7. System Design：底层只有一张 MySQL 商品详情表，怎样设计可支撑 **10 万 QPS** 且可继续水平扩展的商品详情查询服务？
8. 管理端修改价格后，如何完整设计 Cache Update / Invalidation 链路，让 C 端及时看到新价格？
9. Coding：Longest Palindromic Substring / 最长回文字符串。

最终去重：分配编号前再次直接回读 `batch-01.md`～`batch-31.md`。历史确有同一作者的美团 / 快手等其它公司流程，但不同公司、不同招聘流程不跨公司合并；未发现当前 URL、小红书同流程，或“Agent 平台岗位 → 10 万 QPS 商品详情 → Cache Price Freshness → Longest Palindrome”连续题序的历史同场来源。

---

## S293 字节跳动｜AI 全栈（飞书）｜一面｜发布 2026-09-21 14:28｜HUMAN-A

作者：`SOLDIER_627`

来源：https://www.nowcoder.com/discuss/931555466247700480?sourceSSR=users

真人 / 第一人称证据：该 post-specific 原帖在进入 9 月 21 日 Inbox 前已稳定直接回读，标题明确为 `字节 AI 全栈一面（飞书）`，净时长约 1 小时；同一作者主页连续记录小红书、百度、度小满、快手、美团等本人求职流程。2026-09-22 Finalize 时该详情页出现暂时性 Cache Miss，但此前已经完成 Stable Original + Candidate Timeline 核验，且没有出现转载 / 镜像 / 复制链的新反证，因此不因单次抓取波动撤销已经通过的来源质量结论。

Role Scope：标题直接为 AI 全栈，Agent / Skill 项目验真是主线之一，属于目标 AI Full-stack / Application 范围。

整场技术链：

1. 自我介绍。
2. 介绍 Agent 项目的整体 Architecture 与工作原理。
3. Agent 不遵守 Skill 中的限制 / 描述时怎样治理？
4. 是否应把 Skill 规则提升到更底层、更高优先级的规范，适用边界是什么？
5. 视频分析项目的完整处理链路是什么？
6. 海量监控视频如何避免高内存 / OOM，多长视频串行还是并行，时延怎样控制？
7. 分块上传如何保证成功，断点续传与一致性怎样设计？
8. 视频合并失败时，中间状态 / 文件如何清理？
9. MySQL Index 使用什么数据结构，如何组织与工作？
10. SQL 数百毫秒时怎样定位和优化？
11. SQL 从 800ms 降到 50ms 后整体接口仍慢，怎样继续做端到端定位？
12. 总接口约 80ms、单 SQL 约 10ms 时，还能从 Cache / Concurrency / 其它链路怎样优化？
13. Coding：两个最长可达 10 万位的十进制大整数字符串相加。
14. 最大堆 / 最小堆原理。
15. HashMap 机制。
16. Consistent Hashing / 一致性哈希。

最终去重：分配编号前再次直接回读 `batch-01.md`～`batch-31.md`。同一作者的其它公司流程不跨公司合并；未发现当前字节 / 飞书 URL、同公司同流程，或“Agent Skill 遵从性 → 海量视频 OOM / 分块上传 / 失败清理 → SQL 端到端性能 → 大数 / Heap / HashMap / Consistent Hashing”的历史同场来源。

---

