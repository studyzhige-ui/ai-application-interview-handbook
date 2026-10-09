# Batch 28 一手面试流程

采集日期：2026-09-17

## S287 字节跳动｜Agent 开发｜秋招一面 + 二面（同一招聘流程）｜发布 2026-09-16 / 09-24｜HUMAN-A

作者：`吃饱了撑的容器`

来源：https://www.nowcoder.com/discuss/929731481189044224

真人 / 第一人称证据：作者页面显示当前身份为“小红书 Agent 开发（实习员工）”；正文明确记录本人字节 Agent 秋招一面，并写“当天下午已约二面”。面试过程中保留与真人面试官讨论 Computer Use、Pi Agent、DeepSeek Harness、AI Coding 方式与团队业务的现场互动，属于候选人本人第一人称招聘流程，不是答案帖、合集或内容账号整理。

Role Scope：标题直接为“字节 Agent 秋招一面”，技术主体围绕企业 AI 助手、Memory / Context、Agent Harness、Computer Use、AI Coding 与 Agent 工程集成展开，明确通过 AI Application / Agent Role Scope Gate。

代表性技术链：

1. 实习项目真实做了什么，本人负责哪些部分？
2. 企业 AI 助手的滑动窗口 + 摘要压缩 Memory 怎样实现？
3. 滑动窗口大小如何决定，什么场景应切换到 Summary / Compaction？
4. 文档在线自动更新怎样保证并发幂等、避免多个任务互相覆盖？
5. RocketMQ 放在更新链路哪里；为什么选择 MQ，而不是直接用定时任务处理？
6. 怎样理解 Agent / Agent Harness；DeepSeek Harness、Pi Agent 分别有哪些值得迁移的能力？
7. 如果把现有实习 Agent 替换 / 接入新的 Harness，系统哪些层需要改变，是否真的值得替换？
8. Claude Code Context Compression 怎样理解，长会话为什么需要 Context Engineering？
9. Computer Use 在本地电脑与云端电脑上分别怎样执行，执行环境和控制边界有什么差异？
10. 日常怎样真正使用 AI Coding，从需求、理解代码、修改、验证到 Review 的完整 Workflow 是什么？
11. MySQL B+Tree 为什么适合作为索引结构？
12. Coding：判断二叉树子结构。
13. Coding：两个有序 List 求交集，并继续追无限序列、Bitmap 大值域限制与分批 / Streaming 处理。
14. 反问 Agent 垂类业务与团队 AI Coding 文化；面试官反向追问是否存在更 AI Native 的开发工作流。

去重：晚间归档前已再次逐个直接回读 `batch-01.md`～`batch-27.md`。当前 URL、作者，以及“滑动窗口 / 摘要记忆 → 文档并发幂等 + RocketMQ → DeepSeek Harness / Pi Agent → Computer Use → AI Coding Workflow → 无限序列交集”连续链均未在历史正式来源形成同场重复。GitHub / Search 对 URL、作者或罕见组合的 0 命中只作为辅助，不作为未收录证明。


### 2026-10-07 回读补充：同流程二面

二面来源：https://www.nowcoder.com/discuss/932657562825027584

作者、公司与秋招招聘 Timeline 和原一面一致；原一面已记录约二面，本帖又记录二面通过 / 三面横向。因此只回并 S287，不分配新编号。
二面实际面试日未披露，原帖发布显示为 9/24；不把发布日当面试日。

二面已披露题序：

1. （原题1）RAG链路
2. （原题2）Markdown切块
3. （原题2.1）标题父块/小块召回回填
4. （原题2.2）聚合及重叠
5. （原题2.3）1000token按400切，尾200如何补齐
6. （原题2.4）实际是否很少补块
7. （原题2.5）切块/聚合大小
8. （原题3）图片/ul处理
9. （原题3.1）逐图推理导致入库延迟
10. （原题4）Embedding/向量库
11. （原题5）Query改写
12. （原题5.1）改写实例
13. （原题5.2）子问题拆分目的
14. （原题5.3）改写拆分一次或多次推理
15. （原题5.4）非流式前处理等待时间
16. （原题6）混合检索
17. （原题6.1）重排
18. （原题7）企业级与Demo
19. 编码 均匀random5构造random7

本次补充不改写下方 9/17 的历史统计或排除记录，不改变当日新增1个Source的事实。

---

