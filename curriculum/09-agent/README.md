# Agent｜从任务到可解释、可验证的执行系统

[← RAG](../08-rag/README.md) · [↑ Handbook 总目录](../../README.md) · [Learning Path](../../guide/learning-path.md) · [System Design →](../10-system-design/README.md)

> **课程范围：24 篇正式正文**  
> **教材：24 个连续知识小板块** · **HUMAN-A Canonical：44** · **独立来源覆盖：166**  
> **教学结构：展开式解释 + 过程图 + 连续例子 + Failure 边界 + 章末四部分训练。**

从任务与执行角色出发，理解工具、上下文、记忆、状态、安全和恢复；用可核对的产品过程与每章训练把概念落地。

---

## 1. 这个模块解决什么

从任务与执行角色出发，理解工具、上下文、记忆、状态、安全和恢复；用可核对的产品过程与每章训练把概念落地。

学习目标不是记住一组名词，而是能稳定回答：

```text
为什么需要它？
→ 核心机制怎样工作？
→ 正常路径怎样流动？
→ Failure / Trade-off 在哪里？
→ Production 场景怎样验证与排障？
→ 面试官继续追问时怎样解释边界？
```

---

## 2. 在十板块中的位置

[Python Foundation](../01-python/README.md) → [FastAPI](../02-fastapi/README.md) → [MySQL](../04-mysql/README.md) → [Redis](../05-redis/README.md) → [AI Backend Engineering](../03-backend-engineering/README.md) → [Vector Database](../06-vector-db/README.md) → [LLM Foundation（应用工程深度）](../07-llm-foundation/README.md) → [RAG](../08-rag/README.md) → **Agent** → [System Design](../10-system-design/README.md)

模块角色：**Agent Runtime / 从任务与执行角色出发，理解工具、上下文、记忆、状态、安全和恢复；用可核对的产品过程与每章训练把概念落地。**

---

## 3. 固定课程原则

> **知识依赖顺序优先；真人面经只调整复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

同时固定区分：

```text
Canonical Question = 可独立追问的面试能力
Capability Primitive = 更细的工程机制
教材 Markdown = 一个完整认知闭环
Section = 参数 / 变体 / Failure / 深挖追问
```

所以本模块是 **44 道 Canonical → 24 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
任务与执行角色 → 工具契约、发现与受控执行 → 计划、上下文与记忆 → 状态、持久化与恢复 → 安全、协议、扩展与协作 → 诊断、评测与工程落地
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

章节按认知依赖与内容边界组织。MCP 独立讲清协议往返；Skill / Hook / Plugin 单独讲扩展生命周期；其余主题在章内依次说明定义、过程、失败边界与实现对照。

### A｜先认识任务与执行系统

1. [Agent 系统的全貌：模型之外，谁把任务做完](docs/01-AgentSystemAndResponsibilities.md)

2. [Workflow、Agent 与自主权：执行角色的边界](docs/02-WorkflowAutonomyAndRuntimeBoundary.md)

3. [Agent Loop：Session、Run、Turn、Step 与执行事件](docs/03-AgentLoopAndExecutionScopes.md)

### B｜工具调用怎样受控完成

4. [Tool Contract：工具说明、参数与语义校验](docs/04-ToolContractAndValidation.md)

5. [Tool Registry：工具注册、模型可见说明与按需发现](docs/05-ToolRegistrationAndDiscovery.md)

6. [Tool Execution：结果回填、错误分类与有限恢复](docs/06-ToolExecutionAndFailure.md)

7. [Tool Control：副作用、并发、取消与进度](docs/07-ToolConcurrencyAndCancellation.md)

### C｜控制方向与模型可见信息

8. [Planning / ReAct：计划、目标、停止与预算](docs/08-PlanningGoalAndControl.md)

9. [Context Assembly：上下文编排、缓存与结果外部化](docs/09-ContextAssemblyAndCache.md)

10. [Context Compaction：压缩、替代历史与继续执行](docs/10-CompactionAndContinuation.md)

11. [Memory：提取、召回、更新、纠错与遗忘](docs/11-MemoryLifecycle.md)

### D｜执行状态与跨中断恢复

12. [State / Persistence：程序怎样记住当前工作](docs/12-StateHistoryAndPersistence.md)

13. [Checkpoint / Resume：检查点、恢复、分叉与重放](docs/13-CheckpointResumeAndRecovery.md)

### E｜安全、能力接入与协作

14. [Permission / Approval / Sandbox：政策、批准与隔离](docs/14-PermissionApprovalAndSandbox.md)

15. [Guardrails：提示注入、秘密保护与风险控制](docs/15-InjectionAndContainment.md)

16. [MCP：从 Host / Client / Server 到完整协议往返](docs/16-MCPArchitectureAndLifecycle.md)

17. [Skills / Hooks / Plugins：能力扩展与生命周期](docs/17-SkillsHooksAndExtensions.md)

18. [Routing：意图、模型适配与供应商容错](docs/18-RoutingAndProviderResilience.md)

19. [Multi-Agent / A2A：内部协作与跨系统任务](docs/19-MultiAgentAndA2A.md)

### F｜诊断、评测与工程落地

20. [Trace / Replay：记录必要证据，定位具体问题](docs/20-TraceReplayAndDiagnosis.md)

21. [Agent Evaluation、Benchmark 与 Data Flywheel](docs/21-EvaluationBenchmarkAndImprovement.md)

22. [Coding Agent：Repo Understanding → Patch → Test → Verify](docs/22-CodingAgentDelivery.md)

23. [Production Agent：从单进程到可运营执行系统](docs/23-ProductionRuntime.md)

24. [Framework Mapping：按核心语义比较框架与自研](docs/24-FrameworkSelection.md)

---

## 6. 真人面经怎样影响本模块

Canonical 统计基线（`S001–S279`）：本模块有 **44 道 Primary Canonical、166 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- Context Compaction
- Agent Loop
- Memory Architecture
- Tool Calling / Failure
- Multi-Agent
- Agent Evaluation
- Framework Selection

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- Prompt Engineering 归 LLM Foundation；Harness 负责跨轮、跨 Tool、跨 State 的执行。
- RAG 负责 Evidence Quality；Agent Harness 决定何时检索、如何继续执行。
- 通用 MQ / Retry / Idempotency 归 AIBE；Agent 只讲其 Runtime 特化语义。

跨模块问题只保留理解所需的桥梁；完整机制在 Primary Module 维护一份。

---

## 8. Review、Interview、Products 与证据入口

| 入口 | 链接 | 用途 |
|---|---|---|
| Review | [总图与综合自测](review/README.md) | 第二遍复习：从空白纸重建主线 |
| 成熟产品源码 | [Agent Products](../../products/agent/README.md) | 沿固定源码快照学习完整 Production Agent 怎样组合本模块机制 |
| 高频面试题 | [进入](interview/高频面试题.md) | 用真实问法训练口述与追问 |
| 面试易错点 | [进入](interview/面试易错点.md) | 校正绝对化、过时或边界错误表达 |
| 面试前速查 | [进入](interview/面试前速查表.md) | 面试前快速回忆 |

研究与质量证据：

- [Canonical Questions](../../interview/canonical/agent-harness.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../../market/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../../market/analysis/frequency-ranking.md)：复习热度参考；
- [权威技术 / 源码资料索引](../../references/agent/README.md)：只校准技术事实，不改变 HUMAN-A 频率；
- [Curriculum Granularity Audit](../../guide/audits/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../../guide/audits/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

每章采用轻松引入、逐层解释、过程图、例子与失败边界，不压成结论提纲。章末固定**HUMAN-A信号 → 面试怎么答 → 高频易错点 → 本章自测**：🎯面试答案直接显示，⚠️易错点逐条提醒，只有自测答案和可选产品实现折叠。代码只用于明确的教学目的，并有注释及适用边界。

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../../guide/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 24` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：进入成熟实现。** 进入 [Agent Products](../../products/agent/README.md)，选择 Codex、Claude Code、DeepSeek Harness、DeerFlow 中的一套或多套，按 Context → Memory → Tool → Engineering & Evaluation 连续阅读，把通用概念映射到真实源码。
4. **第四遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答，并把成熟产品源码实现作为工程例证。
5. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 教材状态

```text
docs/      ✅ 01–24 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Technical Validation 以证据索引标注的固定源码快照与官方版本为准
```

读者可理解性专项记录：[Agent Reader Revision](../../guide/project/agent-reader-revision.md)。

下一环：[System Design](../10-system-design/README.md)。
