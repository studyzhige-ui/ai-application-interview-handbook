# Batch 02 — 2026 AI 应用 / Agent 真实面经（新增样本）

采集日期：2026-09-09

> 与 Batch 01 相同：只保存来源元数据和问题简洁转述，不整篇复制第三方帖子。

## S016 快手｜AI 应用 / Agent 开发｜2026-09（公开可见部分）

来源：https://www.nowcoder.com/discuss/925527256145883136

可见问题：

1. Cursor/Codex 等 AI Coding 工具如何协作，并保证生成代码质量？
2. Tool 调用结果缓存怎么设计：哪些可缓存、缓存多久、怎么失效？
3. 用户长期偏好（语言、地点等）如何持久化？
4. Agent 如何避免泄露敏感信息，输入过滤和输出脱敏怎么做？
5. 如何系统设计一个“智能合同/文档审阅 Agent”？
6. 会话上下文如何隔离，避免不同用户串话？
7. 意图识别用分类模型、规则还是 LLM，怎么提升准确率？
8. Tool 调用失败率高时，从描述、参数、重试、降级哪些维度优化？
9. LangGraph 与 LangChain 的差别，什么时候适合图状态机？
10. Agent 成本如何通过减少调用与结果复用优化？
11. 人工评测如何组织并保证标注质量？
12. LLM 请求超时/报错时如何做用户友好的异常处理？
13. 多 Tool 并行调用如何控制并发？
14. 日志/Trace 如何记录以便复盘 Agent 决策链路？
15. Reflection 步骤的收益、成本和终止条件怎么权衡？
16. Tool 很多时是否需要渐进式加载（先描述、后 Schema）？

## S017 拼多多｜AI Agent 开发｜2026-08（工程链路/提前批样本）

来源：https://www.nowcoder.com/discuss/926970140204204032

关联来源：https://www.nowcoder.com/discuss/925163213870612480

可见问题：

1. Coding Agent 从用户需求到最终代码交付的全链路是什么？
2. 长流程任务 Context 超限如何解决？即使 1M Context 也不够怎么办？
3. Agent 断点恢复怎么做？服务重启后恢复哪些状态、状态存哪里？
4. 恢复后如何保证状态一致性，恢复失败怎么处理？
5. 多 Agent 同时修改同一文件如何处理冲突？
6. 乐观锁/悲观锁是否适合 Agent 文件协作？
7. 两个 Agent 修改同一方法不同行时，如何做语义合并？
8. Codebase Memory 如何初始化和更新？
9. 10 万+文件代码库如何建立可更新的索引？
10. MySQL / Redis 基础和缓存性能问题如何解释？

## S018 拼多多｜AI Agent 两轮技术面｜2026-08-16

来源：https://www.nowcoder.com/discuss/918542384726540288

可见问题：

1. RAG 离线建库和在线检索分别包含哪些阶段？
2. 文档 Chunk Size 和 Overlap 如何确定？
3. 是否用 Recall@K、MRR 等指标验证 Chunk 策略？
4. 短期/长期记忆怎么设计，何时摘要、何时检索？
5. Tool 调用成功率如何定义和提升？
6. Tool 超时、脏数据、重复执行如何重试与兜底？
7. 进程、线程、协程分别适合什么任务？
8. 并发与并行的区别是什么？
9. 为什么需要进程隔离，为什么线程切换更轻？
10. LRU Cache 如何实现 O(1) get/put？

## S019 网易｜Agent 后端｜2026-08

来源：https://www.nowcoder.com/discuss/919906431476719616

可见问题：

1. Agent 项目如何从业务问题、链路、关键模块、指标四层拆解？
2. LangChain 与 LlamaIndex 各适合什么场景？
3. Agent 后端接入层、编排层、模型层的职责如何划分？
4. 传统后端能力如何支撑 Agent 的并发、缓存、数据库和稳定性？

## S020 第四范式｜Agent 开发实习｜2026（公开可见部分）

来源：https://www.nowcoder.com/feed/main/detail/77a81a03b55143c89d1caf76833676d9

可见问题：

1. Memory 上下文功能的整体处理逻辑是什么？
2. 长期记忆用 RAG 保存哪些高价值信息？
3. 短期记忆如何触发 Context 压缩？
4. LLM 摘要式压缩与规则/正则式机械压缩分别适合什么内容？
5. 多 Agent 是否需要按任务动态选不同能力/成本的模型？
6. Coding Agent 的 Spec-driven / AI 原生开发模式如何理解？
7. Tool Calling 连续失败时如何熔断？
8. 基础模型服务卡死时 Agent 后端如何做故障转移？

## Batch 02 新增信号

相比 Batch 01，这一批进一步强化了几个此前不能只放在“高级扩展”的主题：

- **Tool Cache**：结果可缓存性、TTL、失效与副作用边界。
- **Security**：敏感信息、Prompt/Tool 数据边界、输入过滤和输出脱敏。
- **Trace / Observability**：不只是日志，而是可复盘决策链、工具轨迹、成本与延迟。
- **Context Isolation**：多用户隔离、会话边界、状态污染。
- **Checkpoint & Resume**：断点恢复、状态一致性、重复副作用。
- **Filesystem Concurrency**：文件锁、语义合并、冲突检测。
- **Codebase Memory / Repository Index**：大规模代码库索引、增量更新、检索与压缩。
- **Circuit Breaker / Model Failover**：Tool 层与模型服务层都要有熔断/降级。
- **Model Routing**：不同子任务按能力/成本选择不同模型，属于 Harness 的资源调度能力。
