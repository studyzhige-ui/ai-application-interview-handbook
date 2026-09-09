# Batch 02 — 规范化问题增量

只记录 Batch 02 相比 Batch 01 新出现或明显细化的 canonical questions。

## Agent Harness / Runtime

### A031 Tool Result Cache 如何设计可缓存性、TTL、失效和副作用边界？
- 来源：S016
- 标签：Tool Runtime / Cache / Reliability

### A032 多用户 Agent 如何做 Context / Session 隔离，避免串话和状态污染？
- 来源：S016
- 标签：Context / Session / Multi-tenant

### A033 Agent 如何防止敏感信息泄露？输入过滤、上下文裁剪、Tool 权限、输出脱敏如何协同？
- 来源：S016
- 标签：Security / Data Boundary / Guardrail

### A034 如何记录可复盘的 Agent Trace，而不仅是普通应用日志？
- 来源：S016
- 标签：Observability / Trace / Evaluation

### A035 Reflection / Critic 环节什么时候值得引入？如何限制成本和循环预算？
- 来源：S016
- 标签：Control Loop / Reflection / Cost

### A036 工具数量很大时，如何做渐进式 Tool Discovery / Schema Loading？
- 来源：S016
- 标签：Tool Discovery / Context Budget

### A037 Coding Agent 如何实现可恢复的 Checkpoint / Resume？
- 来源：S017
- 标签：Checkpoint / Persistence / Failure Recovery

### A038 服务重启后恢复 Agent 时，如何保证状态一致性并避免重复副作用？
- 来源：S017
- 标签：Checkpoint / Idempotency / Consistency

### A039 多 Agent / 多 Worker 修改同一文件时，如何进行冲突检测、锁与语义合并？
- 来源：S017
- 标签：Filesystem / Concurrency / Merge

### A040 Codebase Memory 如何初始化、增量更新和失效？
- 来源：S017
- 标签：Memory / Codebase Index / Lifecycle

### A041 10 万+文件代码库如何建立面向 Agent 的可更新索引？
- 来源：S017
- 标签：Retrieval / Codebase / Scale

### A042 Agent 如何按子任务动态路由不同模型，在质量、延迟和成本间权衡？
- 来源：S020
- 标签：Model Routing / Cost / Runtime

### A043 Tool 连续失败时如何设计 Circuit Breaker / Degrade？
- 来源：S020
- 标签：Reliability / Circuit Breaker

### A044 基础模型服务卡死或不可用时如何 Failover？
- 来源：S020
- 标签：Model Runtime / Failover / Availability

## RAG / Evaluation

### R016 Chunk 策略如何用 Recall@K、MRR 等离线指标验证，而不是只靠经验？
- 来源：S018
- 标签：Chunking / Evaluation / Experiment

### R017 Tool 调用成功率应该如何定义，如何形成可优化指标？
- 来源：S018
- 标签：Agent Eval / Tool Success / Metric

## Backend / Production

### B005 AI Agent 流式/并发 Tool 调用如何做线程池、协程或异步资源控制？
- 来源：S016, S018

### B006 Tool 超时、脏数据和重复执行三类失败应该分别如何处理？
- 来源：S018

## 对 Agent 课程目录的新增约束

后续 Agent Harness 课程必须明确出现以下一级或二级章节：

- Tool Result Cache
- Multi-tenant Session / Context Isolation
- Sensitive Data & Secret Boundary
- Trace / Rollout / Decision Replay
- Reflection Budget
- Progressive Tool Discovery
- Checkpoint / Resume
- External Side-effect Idempotency
- Filesystem Concurrency & Merge
- Codebase Memory / Repository Index
- Model Routing
- Circuit Breaker / Model Failover
