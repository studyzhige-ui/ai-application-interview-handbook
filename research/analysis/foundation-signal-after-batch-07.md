# Python / MySQL / Redis 在 AI Agent 面试中的真实信号（Batch 07 校准）

更新时间：2026-09-09

## 先给结论

**它们没有消失，只是在不同岗位、不同轮次、不同搜索策略下“显眼程度”不同。**

前几批看起来 MySQL / Redis / Python 越来越少，主要有三种原因：

1. **Canonical 去重造成视觉偏差**：MySQL 索引、事务、MVCC、Redis 数据结构、HotKey、Python GIL 等题很早就已经存在。后面再出现，往往只记为“已有问题得到强化”，不会像新出现的 Harness / Runtime 问题一样连续新增 ID。
2. **搜索目标造成采样偏差**：Batch 04–06 为了探索 Agent Harness 的知识边界，主动偏向 Harness、Coding Agent、Runtime、Context、Tool、二面/深挖轮次；这类场次自然更少问通用语言八股。
3. **岗位分层明显**：AI 应用开发 / AI 后台 / Agent 后端的一面仍然大量问 Python、数据库、缓存、并发与网络；真正的 Agent Harness 专项二面/三面则更多转向 Runtime / Context / Reliability。

## Batch 07 的直接证据

本批刻意在不降质量的前提下寻找“Agent/AI 岗 + 基础工程能力”同场出现的第一人称面经，结果非常明确：

- PDD Agent 三面：Python 多线程 vs Java、多线程 GIL、FastAPI 路由，同时问 Qdrant/HNSW/RAG Eval。
- 字节 Agent 一面：Redis Lua、缓存失效、MySQL 数据职责，同时直接追 Python dict 哈希表内部实现。
- 平安银行 AI 开发：Redis ZSet / 持久化 / Cluster、Python 多线程 / 线程池 / 性能，同时问 Multi-Agent、Skill、RAG、权限、Kafka、微服务。
- 人马文化 AI 开发实习：MySQL 慢查询、Redis 数据类型、FastAPI、Python 语言特性，同时问 ReAct、Router、Skill。
- 360 Agent 开发：Python vs Java、MySQL B+Tree / 联合索引 / ACID、Redis 数据结构、MySQL-Redis 一致性，同时问 MCP、LLM 降级、多跳检索。
- 阿里云 Agent 研发：MySQL 锁 / MVCC、本地缓存 + Redis + MySQL 一致性、ZSet 限流，同时问 RAG、向量数据库、Planner/Executor/Supervisor、Context、SSE。
- 快手 Agent 一面：Redis 限流、MySQL 索引 / MVCC / ReadView / 锁、Python vs Go；二面则几乎全部转向 RAG / Agent。
- 字节 AI 后台：Redis 缓存 / 高并发、MySQL 数据职责 / B+Tree，同时问 Agent、MCP、RAG 评测。

## 对学习路线的影响

不能用“最近新问题少”推导“这一块不重要”。更合理的学习权重应该由三件事共同决定：

### 1. 知识体系必要性

Python / MySQL / Redis 都属于 AI 应用系统的基础设施知识，即使某些深挖轮次没有直接问，也决定你能否解释真实系统。

### 2. 面试命中频率

基础知识需要高熟练度，尤其是一面 / 后台开发 / 工程平台 / 社招。高频题应该能够 30～90 秒清楚回答。

### 3. 岗位条件概率

| 岗位 / 轮次 | Python | MySQL | Redis | Agent Harness / RAG |
|---|---:|---:|---:|---:|
| AI 应用开发一面 | 高 | 高 | 高 | 高 |
| AI 后台 / Agent 后端 | 高 | 高 | 高 | 中高 |
| Agent 开发一面 | 中高 | 中 | 中高 | 很高 |
| Agent Harness / Runtime 深挖 | 中 | 低～中 | 低～中 | 极高 |
| 二面 / 三面项目深挖 | 视简历而定 | 视项目而定 | 视项目而定 | 极高 |
| 社招 AI 工程 / 平台 | 中高 | 高 | 高 | 高 |

> 这是当前样本的定性归纳，不是精确概率统计。后续在完成 source-level 结构化数据后再生成真正的频率表。

## Python 应该学到什么程度

不是把所有 Python 八股无限扩展，而是形成两层：

**语言基础层**
- 对象 / 引用 / 可变不可变
- list / tuple / dict / set
- dict 哈希表
- 装饰器 / 生成器 / 上下文管理器
- 参数、作用域、异常
- GIL、线程 / 进程 / 协程

**AI 服务工程层**
- async / await
- FastAPI
- SSE / Streaming
- 并发资源控制
- 线程池 / 进程池
- Pydantic / Schema
- 超时 / Retry / Cancellation
- 测试、日志、配置、依赖管理

因此已有 `python-interview-handbook` 的方向是正确的，不需要因为最近 Harness 题增多就缩减 Python。

## MySQL / Redis 应该学到什么程度

MySQL：
- SQL 与表设计
- B+Tree、联合索引、覆盖索引、回表、索引失效
- EXPLAIN / Slow Log
- ACID、隔离级别、MVCC、锁
- redo / undo / binlog
- 并发更新与幂等
- Redis / 本地缓存一致性
- AI 业务数据建模

Redis：
- 数据结构及实现思路
- 为什么快、事件循环 / IO
- TTL、淘汰
- RDB / AOF
- BigKey / HotKey
- 穿透 / 击穿 / 雪崩
- 分布式锁 / Lease
- ZSet / 限流
- Cluster / 高可用
- Agent Session / Cache / State / Rate Limit 的实际用法

## 后续研究策略调整

后续每一批保持两条搜索 Lane：

- **Lane A：前沿 Agent / Harness 深挖** —— 防止遗漏 Runtime、Context、Tool、Memory、Security、Eval 等新能力。
- **Lane B：AI 应用工程基础校准** —— 专门确保 Python、FastAPI、MySQL、Redis、MQ、网络、并发、系统设计不会因为搜索偏向而被低估。

最终频率统计也会按岗位和轮次分层，而不是把所有面经混成一个总百分比。