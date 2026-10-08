# 全量面经分析

[← 面经业务](../README.md) · [统计规则](../03-strategy/normalization-policy.md) · [完整数据说明](../01-data/README.md)

输入为 **399 个独立招聘流程、38 个批次**。多轮与补充不另加来源。没有沿用旧冻结题数。

## 数据覆盖与计数边界

- 源内记录 6104 条，其中编号记录 6083，原始无编号列表记录 21
- 确定技术问法记录 3982；技术主题短记 1489。两者均保留复合问题，不拆造子题
- 背景、反问、推断、占位或待复核记录 633 条，不贡献技术题族频率
- 保守字面规范化得到 5431 组问法；另有 87 个细粒度问题族、77 个较宽主题。三者分开计数
- 398 / 399 个流程至少命中细粒度问题意图族；3135 条技术记录暂未匹配该层规则，原文照常保留

细粒度题族仍是问题意图或能力范围的归组，不是已核验的同义原子问题。例如 Memory 实现、更新和召回不能因同属一组而声称是同一道题。字面规范化、题族归组与尚未完成的逐题语义同义审核严格分开。宽主题只是检索线索，不进入知识域频率。当前统计不外推为招聘市场概率。

## 细粒度问题族频率

| 题族 | 知识域 | 独立流程 | 原始技术记录 |
|---|---|---:|---:|
| AI Coding 如何拆任务并验证生成代码？ (`Q-AGENT-AICODING`) | agent | 145/399 | 200 |
| MCP 与普通 Tool / API 的边界和通信是什么？ (`Q-AGENT-MCP`) | agent | 105/399 | 136 |
| 何时拆分 Sub-agent，多 Agent 如何协作通信？ (`Q-AGENT-MULTI`) | agent | 98/399 | 131 |
| 短期与长期 Memory 如何存储、更新和召回？ (`Q-AGENT-MEMORY`) | agent | 97/399 | 130 |
| Skill 与 Tool / Prompt 如何分工和加载？ (`Q-AGENT-SKILL`) | agent | 87/399 | 109 |
| Agent Loop / ReAct 的状态、循环与终止如何设计？ (`Q-AGENT-LOOP`) | agent | 83/399 | 103 |
| Tool / Function Calling 的完整协议如何工作？ (`Q-AGENT-TOOLCALL`) | agent | 72/399 | 82 |
| Harness / Runtime 需要哪些职责和模块？ (`Q-AGENT-HARNESS`) | agent | 62/399 | 76 |
| 超时、重试、熔断和降级如何配合？ (`Q-BE-RESILIENCE`) | backend-engineering | 55/399 | 68 |
| Context 超窗如何压缩并验证信息没有丢失？ (`Q-AGENT-COMPACT`) | agent | 53/399 | 66 |
| 从文档到生成答案的完整 RAG 链路是什么？ (`Q-RAG-PIPELINE`) | rag | 52/399 | 53 |
| Agent 如何构造评测集、回放失败并验证收益？ (`Q-AGENT-EVAL`) | agent | 50/399 | 60 |
| LangGraph 等框架与自研 Runtime 如何取舍？ (`Q-AGENT-FRAMEWORK`) | agent | 49/399 | 54 |
| RAG 如何评测并分层归因 Bad Case？ (`Q-RAG-EVAL`) | rag | 49/399 | 54 |
| 长任务如何持久化、重试并从中断恢复？ (`Q-AGENT-RECOVERY`) | agent | 48/399 | 58 |
| 高 QPS 场景如何估算容量并扩展？ (`Q-SD-SCALE`) | system-design | 48/399 | 60 |
| 幻觉如何定位、约束和验证？ (`Q-LLM-HALLUCINATION`) | llm-foundation | 44/399 | 48 |
| Context 中各类信息如何组织、隔离与注入？ (`Q-AGENT-CONTEXT`) | agent | 42/399 | 46 |
| Embedding 和向量相似度如何选择与评估？ (`Q-VDB-EMBEDDING`) | vector-db | 42/399 | 54 |
| Dense / Sparse / BM25 与混合检索如何取舍？ (`Q-RAG-HYBRID`) | rag | 41/399 | 47 |
| Prompt 的目标、约束、示例与输出格式如何设计？ (`Q-LLM-PROMPT`) | llm-foundation | 36/399 | 38 |
| Rerank 为什么有效，变差时如何诊断？ (`Q-RAG-RERANK`) | rag | 34/399 | 40 |
| Chunk 大小、边界与切分策略如何选择？ (`Q-RAG-CHUNK`) | rag | 33/399 | 36 |
| 向量数据库如何选型，和关系库怎样分工？ (`Q-VDB-MILVUS`) | vector-db | 33/399 | 37 |
| SSE 与 WebSocket 的差异和适用场景是什么？ (`Q-BE-SSE`) | backend-engineering | 32/399 | 41 |
| TCP 如何建连、断连并保证可靠传输？ (`Q-BE-TCP`) | backend-engineering | 30/399 | 38 |
| 进程、线程与协程如何区分？ (`Q-BE-PROCESS`) | backend-engineering | 26/399 | 30 |
| 线程池的参数、队列与拒绝策略如何设计？ (`Q-BE-THREADPOOL`) | backend-engineering | 26/399 | 32 |
| Java 锁、volatile 与并发容器怎样工作？ (`Q-BE-JAVALOCK`) | backend-engineering | 25/399 | 34 |
| Prompt Injection、工具执行与沙箱如何防护？ (`Q-AGENT-SANDBOX`) | agent | 23/399 | 27 |
| 链表反转、重排与合并怎样实现？ (`Q-CODING-LIST`) | coding | 23/399 | 24 |
| 重复请求或回调如何保证幂等？ (`Q-BE-IDEMPOTENCY`) | backend-engineering | 21/399 | 23 |
| 慢 SQL 如何通过执行计划定位与优化？ (`Q-MYSQL-EXPLAIN`) | mysql | 21/399 | 24 |
| PDF、表格和多模态文档如何解析？ (`Q-RAG-PARSING`) | rag | 21/399 | 25 |
| 如何路由到正确 Skill 并处理冲突？ (`Q-AGENT-ROUTE`) | agent | 20/399 | 32 |
| 二叉树如何遍历、序列化或重建？ (`Q-CODING-TREE`) | coding | 20/399 | 20 |
| MySQL 为什么使用 B+ 树，查询如何进行？ (`Q-MYSQL-BTREE`) | mysql | 20/399 | 26 |
| 如何权衡响应延迟、质量与成本？ (`Q-SD-TRADEOFF`) | system-design | 20/399 | 20 |
| Agent 写操作、权限和用户确认怎样划分？ (`Q-AGENT-APPROVAL`) | agent | 19/399 | 23 |
| 限流算法及其分布式实现如何选择？ (`Q-BE-RATELIMIT`) | backend-engineering | 19/399 | 22 |
| 数据库与缓存如何保证更新一致性？ (`Q-REDIS-CONSISTENCY`) | redis | 19/399 | 21 |
| Agent 与 Workflow 的边界及适用场景是什么？ (`Q-AGENT-BOUNDARY`) | agent | 18/399 | 19 |
| Transformer / Attention / QKV 的机制是什么？ (`Q-LLM-ATTENTION`) | llm-foundation | 18/399 | 27 |
| Redis 分布式锁怎样获取、续期和安全释放？ (`Q-REDIS-LOCK`) | redis | 18/399 | 20 |
| JVM 内存与垃圾回收如何排查和调优？ (`Q-BE-JVM`) | backend-engineering | 17/399 | 20 |
| 联合索引与最左前缀如何影响查询？ (`Q-MYSQL-COMPOSITE`) | mysql | 17/399 | 21 |
| 消息队列如何避免丢失、重复和乱序？ (`Q-BE-MQ`) | backend-engineering | 16/399 | 18 |
| 缓存穿透、击穿、雪崩怎样区分与处理？ (`Q-REDIS-FAILURE`) | redis | 16/399 | 16 |
| 知识库更新如何处理增量、失效和回滚？ (`Q-RAG-UPDATE`) | rag | 15/399 | 18 |
| HTTPS / TLS 如何建立安全连接？ (`Q-BE-TLS`) | backend-engineering | 14/399 | 16 |
| 事务隔离级别与并发异常如何区分？ (`Q-MYSQL-ISOLATION`) | mysql | 14/399 | 15 |
| 分库分表后如何处理路由与跨分片查询？ (`Q-MYSQL-SHARD`) | mysql | 14/399 | 18 |
| 何时进行查询改写、分解或 HyDE？ (`Q-RAG-REWRITE`) | rag | 14/399 | 14 |
| 秒杀系统怎样防止超卖并保持可靠性？ (`SD-FLASHSALE`) | system-design | 14/399 | 16 |
| Chunk Overlap 与父子索引解决什么问题？ (`Q-RAG-OVERLAP`) | rag | 13/399 | 13 |
| RRF 怎样融合多路检索结果？ (`Q-RAG-RRF`) | rag | 13/399 | 15 |
| RAG、Prompt 与微调如何选择？ (`Q-LLM-TUNING`) | llm-foundation | 12/399 | 13 |
| undo、redo 与 binlog 各自承担什么？ (`Q-MYSQL-LOG`) | mysql | 12/399 | 15 |
| MVCC 如何实现快照读和事务隔离？ (`Q-MYSQL-MVCC`) | mysql | 12/399 | 13 |
| 系统如何消除单点并实现故障恢复和容灾？ (`Q-SD-RELIABLE`) | system-design | 12/399 | 13 |
| 如何实现 O(1) LRU Cache？ (`Q-CODING-LRU`) | coding | 11/399 | 12 |
| 回文与无重复子串如何求解？ (`Q-CODING-SUBSTRING`) | coding | 11/399 | 11 |
| 聚簇索引、二级索引与回表如何区分？ (`Q-MYSQL-COVERING`) | mysql | 11/399 | 16 |
| Go GMP、Channel 与 Goroutine 如何协作？ (`Q-BE-GO`) | backend-engineering | 10/399 | 12 |
| 如何约束并校验模型结构化 JSON 输出？ (`Q-LLM-JSON`) | llm-foundation | 10/399 | 11 |
| LLM 为什么分词，Token 如何影响成本和窗口？ (`Q-LLM-TOKEN`) | llm-foundation | 10/399 | 12 |
| Top-k、堆与选择算法如何控制复杂度？ (`Q-CODING-TOPK`) | coding | 9/399 | 9 |
| Redis 集群、复制和故障切换怎样工作？ (`Q-REDIS-CLUSTER`) | redis | 9/399 | 10 |
| Redis ZSet 与跳表如何实现有序访问？ (`Q-REDIS-ZSET`) | redis | 9/399 | 10 |
| Redis 的 RDB 与 AOF 如何取舍？ (`Q-REDIS-PERSIST`) | redis | 8/399 | 8 |
| 枚举、排列与图遍历问题怎样求解？ (`Q-CODING-SEARCH`) | coding | 7/399 | 7 |
| HNSW、IVF 等近似索引如何取舍？ (`Q-VDB-HNSW`) | vector-db | 7/399 | 7 |
| React / Vue 的组件、状态与生命周期如何工作？ (`Q-FRONTEND-REACT`) | frontend | 6/399 | 6 |
| LoRA 与全量微调的机制和成本有何不同？ (`Q-LLM-LORA`) | llm-foundation | 6/399 | 6 |
| 深分页为何变慢，如何用游标优化？ (`Q-MYSQL-PAGINATION`) | mysql | 6/399 | 8 |
| GIL 如何影响 Python 并发与并行？ (`Q-PY-GIL`) | python | 6/399 | 6 |
| asyncio / await 与事件循环怎样工作？ (`Q-PY-ASYNCIO`) | python | 5/399 | 5 |
| Temperature、Top-p 和 Top-k 如何影响生成？ (`Q-LLM-SAMPLING`) | llm-foundation | 4/399 | 4 |
| 装饰器如何实现并用于横切逻辑？ (`Q-PY-DECORATOR`) | python | 4/399 | 4 |
| Redis 单线程与 I/O 多线程的边界是什么？ (`Q-REDIS-THREAD`) | redis | 4/399 | 4 |
| KV Cache 如何降低推理开销？ (`Q-LLM-KVCACHE`) | llm-foundation | 3/399 | 3 |
| FastAPI 流式端点如何处理连接与取消？ (`Q-FASTAPI-STREAM`) | fastapi | 2/399 | 2 |
| Python list、tuple、dict 的机制与边界是什么？ (`Q-PY-CONTAINERS`) | python | 2/399 | 2 |
| 迭代器与生成器的协议和差异是什么？ (`Q-PY-GENERATOR`) | python | 2/399 | 2 |
| 请求如何经过 ASGI / Uvicorn 到达 FastAPI？ (`Q-FASTAPI-ASGI`) | fastapi | 1/399 | 1 |
| FastAPI 依赖注入与中间件分别负责什么？ (`Q-FASTAPI-DI`) | fastapi | 1/399 | 1 |
| Python 参数绑定、默认值与可变性怎样工作？ (`Q-PY-PARAMETERS`) | python | 1/399 | 2 |

## 主题检索层

较宽主题仅用于资料检索，不属于已确认的独立问题频率，也不进入知识域频率；可能与细粒度问题族重叠。见[主题检索覆盖](topic-frequency.json)。

## 可追溯接口

- [细粒度问题族频率](question-family-frequency.json)：来源集合、命中记录与代表问法
- [包含 granularity 的全量分组 JSON](family-frequency.json) / [CSV](family-frequency.csv)：区分 question_family 与 topic
- [知识域频率](module-frequency.json)：对域内来源取并集，不相加题族频数
- [覆盖报告](coverage.json)：包含所有 399 个流程及未映射项
- [逐流程顺序](flow-traceability.json)：保留原小节、序号与追问标记；相邻不等于因果
- [排除登记](exclusion-register.json)：逐项保留理由和原文定位
- [完整问法记录](../01-data/question-occurrences.json) / [规范化问法](../01-data/normalized-questions.json)

## 重建

在仓库根目录执行：

```sh
python market/interview-experience/04-scripts/build_interview_analysis.py
python market/interview-experience/04-scripts/build_interview_analysis.py --check
python -m unittest discover -s market/interview-experience/04-scripts -p "test_*.py"
```
