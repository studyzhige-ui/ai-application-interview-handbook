# 2026 AI 应用 / Agent 面经持续监控 Inbox

用途：保存自动监控发现、但尚未归入正式 `batch-xx.md` 的新来源。

## 规则

1. 不局限于单一平台：持续检查牛客、小红书、Bilibili、抖音、知乎、脉脉公开可索引内容、技术社区与其他可稳定核验的公开来源。
2. 正式候选必须同时通过：
   - `research/quality/source-quality-policy.md`：来源真实性、信息密度与可核验性；
   - `research/quality/role-scope-policy.md`：岗位属于 AI 应用开发 / Agent 开发 / 大模型应用 / RAG / AI 后端 / AI 全栈 / Applied AI / FDE / Agent Runtime 等目标方向。
3. 排除传统数据分析 / BI、纯推荐广告算法、纯训练 / RLHF / CUDA / 训练 Infra、纯研究岗，以及只顺带问一句 AI 的普通传统后端岗位。
4. 对通过岗位准入的 AI 岗，保留它真实问到的完整能力链：Python、FastAPI、MySQL、Redis、MQ、网络、并发、Vector DB、RAG、Agent、System Design 等，不只摘“AI 题”。
5. 与 `research/interviews/batch-01.md` ～最新 Batch 中已有 URL、原标题、公司/岗位/日期和问题语义比较，禁止重复写入。
6. 每个候选来源记录：发现日期、页面发布日期/面试日期、公司、岗位、轮次、来源 URL、来源质量、3～10 条最有信息量的问题转述；若能确认，再记录 `interviewer_type: human / automated`。
7. 第一人称 A/B 级来源优先。整理/合集、二次创作与不稳定平台标题原则上只作为 Lead，不参与真实面试频率。
8. 自动化 AI 面试可以提供岗位信号，但与真人技术面分层统计，不默认等权。
9. 不复制第三方帖子全文，只保存研究所需的元数据与问题简洁转述。
10. Inbox 中来源在集中批次中完成真实性核验、转载/语义去重和 canonical question 更新后，再进入正式 Batch。

## 当前基线

- 初始化日期：2026-09-09
- 正式归档范围：`S001–S128`
- 最新正式批次：`research/interviews/batch-10.md`
- 当前 canonical questions：约 **205 道**
- 当前判断：**尚未接近饱和，继续扩展高质量目标岗位样本。**

---

## 待整理新来源

### 2026-09-09｜小红书｜Agent 服务端开发实习｜一面｜A

- 发现日期：2026-09-09
- 面试日期：2026-09-08
- interviewer_type：human
- 来源：https://www.nowcoder.com/discuss/926917172448759808
- 去重：未在 `S001–S128` 中检出相同 URL / 标题；正式入批前继续检查作者跨平台同步。
- 高价值问题：
  1. SSE 与 MCP Streamable HTTP 的职责和传输差异是什么？
  2. Agent / MCP Client 如何同时适配 stdio、HTTP、SSE、Streamable HTTP 等不同 Transport？
  3. MCP 协议/Server 版本变化时，客户端如何处理兼容、能力发现和降级？
  4. 类 ChatGPT 对话 Agent 的 Conversation / Message 数据模型应该如何设计字段与关联关系？
  5. Coding：最长递增子序列。
- 价值：信息密度不算极高，但来源第一人称、公司/岗位/面试日期明确，且 `MCP Transport + Version Compatibility + Agent Persistence Schema` 三个问题具有明显服务端 / Runtime 工程特征。

### 2026-09-09｜字节跳动（生活服务）｜AI 全栈工程师｜二面｜B

- 发现日期：2026-09-09
- 面试日期：2026-09-08
- 面试时长：约 50 分钟
- interviewer_type：human
- 来源：https://www.nowcoder.com/feed/main/detail/0a926033572f4a68b8c537f20a013503
- 去重：未在 `S001–S128` 中检出相同 URL。
- 高价值问题：
  1. 面试前给出一份开放式前置作业，要求使用 AI 辅助完成，并自行梳理需求、边界和实现方案；面试中继续深挖设计取舍。
  2. 如何解释并验证前置作业的架构设计，而不是只展示 AI 生成代码？
  3. Kafka 消息一致性如何保证？
  4. 接口幂等如何设计？
  5. 如果从零设计通知平台，核心模块、可靠性与扩展性如何考虑？
  6. Coding：树的最大独立集。
- 价值：公开题量有限，降为 B；但它明确体现 `AI-assisted take-home → 设计复盘 → Kafka / Idempotency / System Design` 的 AI 全栈考察方式，适合作为 Foundation Lane 的面试形态信号。

### 2026-09-09｜美团｜AI 后端工程师｜一面｜B

- 发现日期：2026-09-09
- 面试日期：2026-09-02
- 面试时长：约 50 分钟
- interviewer_type：human
- 来源：https://www.nowcoder.com/discuss/924679647910993920
- 去重：未在 `S001–S128` 中检出相同 URL / 标题。
- 高价值问题：
  1. 实习项目被连续深挖约 30 分钟，重点确认是否真正参与完整业务链路，而不是只负责局部模块。
  2. MySQL MVCC 的实现与作用是什么？
  3. Kafka 的核心机制如何解释？
  4. Kafka 以 `user_id` 作为固定分区键会带来哪些热点、分布和扩展问题？
  5. Spring Bean 生命周期如何工作？
  6. Coding：二叉树层序遍历。
- 价值：虽然 Agent/RAG 题目公开得不多，但岗位明确为 AI 后端，且真实面试将 `业务项目真实性 + MVCC + Kafka 分区设计 + Spring` 放在同一场，属于 Foundation Lane 的有效 B 级样本；不应因“AI 题少”而丢弃。
