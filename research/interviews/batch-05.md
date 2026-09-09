# Batch 05 — 2026 AI 应用 / Agent 面经与跨平台问题信号

采集日期：2026-09-09

> 本批开始主动扩展到牛客之外的平台：CSDN / 技术博客、抖音、B 站以及小红书线索。
>
> 为避免把“博主整理题 / 模拟面试”误当成真实公司场次，本批进一步细分来源类型：
>
> - `原始/第一人称`：候选人直接复盘真实面试，最终频率统计可计入。
> - `第一人称/低信息密度`：真实面试，但公开内容只给出少量问题，低权重计入。
> - `整理/合集`：二次整理，主要用于发现题目和原始来源，避免与原帖重复计数。
> - `面试题信号/二次创作`：短视频/文章围绕“面试官会问什么”展开，但无法证明对应某一真实场次；**不计入真实面试频率**，只用于补充课程边界、场景题和搜索关键词。
>
> 仍然只保存来源元数据与问题简洁转述，不复制第三方正文。

---

## S048 月之暗面 Kimi｜Agent 开发｜2026-07-22｜CSDN｜原始/第一人称

来源：https://agent.csdn.net/6a812cee10ee7a33f29ba328.html

可见问题：

1. 用 ReAct 搭 Agent 时，核心执行循环如何组织？
2. 短期记忆具体怎么实现，滑动窗口、摘要和任务状态分别承担什么职责？
3. Context 快到上限的“快”如何量化，Token 是如何随轮次和 Tool Result 逐步膨胀的？
4. 多轮对话过长时，System / 近期完整上下文 / 历史摘要如何分层？
5. Compaction 什么时候触发？软阈值、硬阈值和提前异步准备如何设计？
6. 为什么不能每轮都重新总结？成本、延迟和摘要信息衰减如何权衡？
7. 已有历史摘要后，新一轮对话应该增量合并还是全量重算？
8. 被压缩掉的原始上下文是否仍需要持久化？如何用于审计、摘要重建与记忆回溯？
9. 长期记忆什么时候才应该检索？是否每轮都应该注入？
10. 工具很多时，如何通过意图路由 / Progressive Disclosure 减少 Tool Schema Token？
11. RAG 从 Chunk、Embedding、Vector Index、TopK、Rerank 到生成的链路如何解释？
12. Cosine 与 Euclidean Distance 在向量归一化前后有什么工程差异？
13. 如何记录检索审计日志，区分“召回问题 / 排序问题 / 生成问题”？
14. 项目中不同模型（Embedding / Router / Main LLM / Reranker）如何分工？
15. 如何分层抑制模型幻觉？
16. Claude Code / Coding Agent 的 Tool、权限、状态与 Harness 架构如何理解？

> 价值：这是当前少见的非牛客第一人称长篇 Agent 面经，尤其强化了 Context Compaction、Memory Retrieval Gating、RAG Observability 和 Harness 源码理解。

---

## S049 字节跳动｜AI Agent 实习｜2026-06-10｜抖音｜第一人称/低信息密度

来源：https://www.douyin.com/video/7649584931873493839

公开描述可确认的面试结构：

1. 一面重点检查计算机 / 开发基础是否扎实。
2. 二面集中深挖项目真实贡献与工程细节。
3. 三面转向 Agent 系统设计和业务落地。
4. 作者明确表示实际面试并非只问八股或 Prompt，而是逐步进入项目和系统能力。

> 该视频目前可公开索引到的是面试结构而非完整题目，因此只作“真实场次结构信号”，不从评论区推断不存在的题目。

---

## S050 某小厂｜Agent 开发｜2026-08-14｜抖音｜第一人称/低信息密度

来源：https://www.douyin.com/video/7673870826139127046

公开描述可确认：

1. 技术面主要围绕两个 Agent 项目展开，并未大量考纯八股。
2. 项目介绍不熟会直接影响表达，尤其是第二个项目容易出现“想到哪说到哪”的问题。
3. 仍包含基础算法手撕，因此 Agent 岗不能完全放弃算法 / 基础开发能力。
4. 作者复盘认为应把每个项目可能被追问的问题提前组织成可回答的结构。

---

## S051 Agent 生产环境工程化题集｜2026-07-29｜抖音｜面试题信号/二次创作

来源：https://www.douyin.com/video/7667735259081506659

可见题目信号：

1. Agent 并发崩溃、goroutine / task 泄漏怎么排查？
2. 超时、熔断、分布式限流应该如何分层？
3. 如何用 P95/P99、QPS、错误率而不是平均值评价线上 Agent？
4. 哪些数据 / Tool Result 可以缓存，哪些绝不能缓存？
5. Prompt 精简、大小模型分级调用如何降低 Token 成本？
6. 会话、租户和权限如何隔离？
7. 长任务 Checkpoint、任务队列和动态模型调度怎么做？
8. 向量库规模扩大后如何做分片与容量规划？
9. Agent 服务如何做蓝绿 / 灰度发布与优雅停机？
10. 多模型 / 多厂商接口如何做故障兜底？

> 不计入“真实公司场次频率”，但用于 Production / Reliability 课程边界校验。

---

## S052 Agent 高风险动作确认分级｜2026-08-07｜抖音｜面试题信号/二次创作

来源：https://www.douyin.com/video/7671213669401965482

核心场景题：

> Agent 每一步都让用户确认体验很差，但完全不确认又危险，如何设计 Human-in-the-loop / Approval 分级？

题目信号：

1. 动作类型与业务风险如何分类？
2. 可逆 / 不可逆操作是否采用不同审批策略？
3. 用户意图明确程度如何影响是否需要二次确认？
4. 怎样兼顾安全、体验、审计与回放？

---

## S053 用户执行中途改变 Agent 目标｜2026-08-07｜抖音｜面试题信号/二次创作

来源：https://www.douyin.com/video/7671103231371635850

核心场景题：

> Agent 执行到一半时用户改变目标，旧 Plan / 已排队步骤应该如何判定继续、部分失效或全部作废？

题目信号：

1. Task Goal 是否需要显式版本号？
2. Plan / Subtask 依赖关系如何表示？
3. 新目标到来后如何做 Dependency Invalidation？
4. 已产生副作用的旧步骤如何处理？
5. 什么时候必须再次向用户确认？
6. 旧 Context / Memory 中已经失效的目标如何清理或降权？

---

## S054 阿里三面权限隔离题｜2026-08-16｜抖音｜面试题信号/二次创作

来源：https://www.douyin.com/video/7672976796299644210

可见题目信号：

1. 企业员工让 Agent 查报表、改配置时，权限判断应该由哪一层负责？
2. 为什么不能让 LLM 自己决定“有没有权限”？
3. Read / Write / Execute 权限如何拆分？
4. 模糊授权、代操作、权限不足时如何反馈？
5. Agent 权限策略如何做回归测试与审计？

---

## S055 阿里三面企业 RAG 知识冲突｜2026-08-11｜抖音｜面试题信号/二次创作

来源：https://www.douyin.com/video/7672717119754095913

核心场景题：

> 企业知识库同时存在多版本、互相冲突的制度文档时，RAG / Agent 应该信哪一份？

题目信号：

1. 文档版本、有效期、来源权威级别如何建 Metadata？
2. 检索到冲突证据后怎么排序与裁决？
3. 什么时候应该拒答 / 提示用户存在冲突，而不是强行生成单一答案？
4. 最终回答如何做到可追溯？
5. 线上如何监控“旧文档被召回 / 冲突文档共同命中”这类 Bad Case？

---

## S056 Agent 跨会话任务恢复｜2026-08-06｜抖音｜面试题信号/二次创作

来源：https://www.douyin.com/video/7670596908704728994

核心场景题：

> 用户关闭会话后再次回来，Agent 如何恢复长任务进度，而不是简单重放聊天记录？

题目信号：

1. 应保存哪些“任务指针 / 当前阶段 / 用户偏好 / 已完成副作用”？
2. Resume 前为什么需要和外部系统重新对账？
3. 订单、权限、库存等外部事实已经变化时，旧 Checkpoint 能否直接恢复？
4. Memory / Checkpoint 是否需要版本控制？
5. 恢复失败时如何降级与请求人工确认？

---

## S057 Tool 局部失败：重试、回滚还是补偿｜2026-08｜抖音｜面试题信号/二次创作

来源：https://www.douyin.com/video/7669850238371236006

同主题补充来源：https://www.douyin.com/video/7673884883844696422

核心场景题：

> Agent 调用 10 个 Tool，9 个成功、1 个失败，系统应该 Retry、Rollback、Compensate 还是整体失败？

题目信号：

1. 先区分瞬时错误、永久错误、业务拒绝和脏数据。
2. 前序成功 Tool 是否有外部副作用？副作用是否可逆？
3. 幂等重试和补偿事务的边界如何定义？
4. 为什么跨外部系统的 Agent Workflow 往往更接近 Saga / Compensation，而不是数据库式全局回滚？

---

## S058 2026 AI 大模型应用开发面试合集｜2026-08-13｜Bilibili｜整理/合集

来源：https://www.bilibili.com/video/BV1Nkgn6hEug/

公开选集可见的重点问题包括：

1. Prompt Engineering 与 Context Engineering 区别？
2. Transformer 处理超长文本为什么会退化？
3. RAG 召回率低时 Query Rewrite 为什么重要？
4. Agent / RAG / LangGraph 工程落地有哪些常见面试坑？

> 该来源是整理题库而非单一真实面试，用于发现高频专题，不计真实公司场次频率。

---

## S059 19 场 AI 应用开发春招复盘｜2026-03-31｜CSDN｜原始/第一人称（跨公司汇总）

来源：https://agent.csdn.net/6a4e074410ee7a33f289301a.html

来源自述：作者从 Java 后端转 AI 应用层，春招投递后集中参加多场 AI 应用开发面试，并以个人面试记忆进行复盘。

本轮可见的稳定信号：

1. 面试不再满足于“知道 RAG”，而会追 Chunk Size、Rerank、评估指标、线上踩坑。
2. 简历项目会被要求给出准确率 / 延迟 / 成本等指标，而不是只描述“做了一个 Agent”。
3. 后端转 AI 的优势仍然来自接口、数据库、缓存、部署和可靠性等工程能力。
4. 企业关心的是可落地的完整链路，不是单纯模型 API 调用。

> 因为文章将 19 场面试合并复盘，未逐一可靠映射公司 / 轮次，本项目把它视为“高价值第一人称聚合样本”，但不会把一篇文章当成 19 个独立来源计频。

---

## S060 大疆｜AI Agent 开发岗｜2026-08-21｜CSDN｜整理/待核实

来源：https://adg.csdn.net/6a87b666662f9a54cb9f1356.html

可见问题信号：

1. 从 0 搭 Agent 时哪些核心模块不可缺少？
2. 短期 / 长期 Memory 分别怎么设计？
3. 外部 Tool / API 报错或超时，容错与恢复链路怎么做？
4. 日常 AI Coding 工具如何使用并验证结果？
5. Agent 系统设计与 Java / 数据库工程基础如何结合？

> 页面标题明确写“面经整理”，因此先按二次整理处理，后续若追到第一人称原帖再升级来源权重。

---

## S061 小红书｜Agent 服务端开发实习｜2026-09-08｜牛客｜原始/第一人称

来源：https://www.nowcoder.com/enterprise/715/interview （小红书企业面经页，标题“小红书Agent服务端开发实习一面（已挂）”）

公开可见问题：

1. SSE 与 Streamable HTTP 有什么区别？
2. Agent / MCP Client 如何同时适配 stdio、HTTP、SSE、Streamable HTTP？
3. 如何处理 MCP 协议版本兼容问题？
4. 类似 ChatGPT 的对话 Agent，Session 表和 Message 表应该有哪些核心字段？
5. 仍然包含算法题（最长递增子序列）。

> 这是非常新的 9 月样本，说明 MCP 已从“协议定义”进入 Transport / Compatibility / Persistence 级别追问。

---

## S062 小红书｜Agent 开发二面｜2026-08-17｜牛客｜原始/第一人称

来源：https://www.nowcoder.com/enterprise/715/interview （标题“小红书Agent开发二面面经”）

公开可见问题：

1. 是否真实参与过 Agent 内部流程编排？
2. 分析型 Agent 的结论如何验证正确性，结构化输出用什么格式？
3. Agent 从输入到返回的完整 Runtime 链路是什么？
4. 为什么选 OpenManus，不选 LangGraph 做 orchestration？
5. 多 Agent 并行时会争抢哪些资源，State / Context 如何隔离？
6. Workflow 与自治 Agent 的区别？
7. Prompt Injection 诱导 Agent 泄露 System Prompt 或绕过指令时如何防？
8. Tool 调用完全不加限制会产生什么风险，如何治理？
9. 为什么某些项目不应该做 Multi-Agent？如果拆成 Multi-Agent 会新增哪些风险？
10. Agent 同时扩展到大量设备、本地 Agent 与云端 Agent 时如何设计？

---

## S063 小红书 + 百度｜Agent 开发实习｜2026-08 下旬｜牛客｜原始/第一人称

来源：https://www.nowcoder.com/enterprise/715/interview （标题“小红书Agent开发实习生一面凉经，附百度Agent凉经”）

小红书部分可见问题：

1. 7 步 Agent Pipeline 如何组织？
2. LangGraph 中多个子图 / Agent 之间怎么传递数据？
3. 为什么拆子图而不是一条 Pipeline？
4. Skills 知识进化流程怎么搭？为什么不直接把同样内容塞进 Prompt？
5. MySQL B+Tree 索引、乐观锁 / 悲观锁、表锁 / 行锁怎么解释？
6. AI Coding / Claude Code 平时如何使用，如何总结可复用工作流？

百度部分可见问题：

1. Agent 子图中节点如何设计，为什么不用单一大 Agent 或纯脚本？
2. Agent Node 输入输出如何对接、上下文怎么传？
3. Skill 产生幻觉 / 文件路径错误时如何恢复？
4. 子图 Agent 跑偏时是否重跑，如何重新路由？
5. Human-in-the-loop 如何从图中介入 / 退出？
6. 是否调研过其他 Agent Framework，长链路任务如何选 Runtime？

---

## Batch 05 观察

### 1. 跨平台之后，题目类型明显被分成两层

真实第一人称面经更适合统计“招聘到底在问什么”；短视频 / 专题文章则很适合暴露 **Production 场景题**，例如：

- 风险分级与 Human Approval
- 用户中途改目标
- 跨会话任务恢复
- Tool 部分成功、部分失败后的补偿
- 企业 RAG 多版本冲突
- Agent 权限隔离

这些二次创作题 **不用于提高真实面试频次**，但可以反过来检查课程是不是缺少真实工程边界。

### 2. MCP 的学习深度继续提高

新样本已从：

`MCP 是什么 → Host/Client/Server → Tool Discovery`

进一步进入：

`stdio / HTTP / SSE / Streamable HTTP → Transport Adapter → Protocol Version Compatibility → Dynamic Capability`

因此后续 Agent Harness 的 MCP 章节必须包含 Transport 与版本生命周期，而不能只讲 Tool Calling Demo。

### 3. Context / Memory 的问题已经从“分层”进入“生命周期”

需要明确讲清：

- Compaction 的软 / 硬触发水位
- 摘要的增量更新
- 原始历史持久化
- Long-term Memory Retrieval Gating
- Cross-session Resume 前的外部状态对账
- Goal / State Versioning

### 4. 安全题越来越接近传统操作系统 / 后端权限模型

面试不再接受“Prompt 里告诉模型不要做危险操作”。真正需要的是：

`认证 → 授权 → Capability / Scope → Approval → Sandbox → Audit → Replay → Revocation`

这与 Codex / Claude Code 的成熟 Agent Runtime 设计方向高度一致。
