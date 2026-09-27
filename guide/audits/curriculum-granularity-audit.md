# Curriculum Granularity｜教材粒度与职责边界

[← Handbook](../../README.md) · [知识地图](../knowledge-map.md) · [正文深度](content-depth-audit.md)

研究粒度、能力粒度和教材文件粒度不是同一层级。Canonical 可以是一个独立追问单元；教材 Markdown 应围绕一个完整问题形成可学习、可画图、可推演失败的认知闭环。

## 拆分与合并的依据

一个主题有自己的问题、前置模型、机制和验证过程时，可以单独成章。参数、变体和补充例子通常留在该章；不要按 API 数量、源码文件数量或市场题目数量机械拆篇。

反过来，合并后让读者同时承担多个尚未建立的核心模型，也应重新拆分。数量是内容设计的结果，不是必须保持的质量目标。下面列的是现有正文，不是永久固定的“最终章数”。

## 路径与阅读顺序

文件名前缀是稳定引用标识，不一定等于阅读顺序。Backend 按其 README 先学习请求责任与持久状态，再进入网络与执行；Codex 产品按上下文、工具、记忆、工程的主线阅读。不得用文件名字典序覆盖已有依赖安排。

## 统计保护

重组正文不改变 HUMAN-A、Source Count、Primary Ownership 或 Verified Follow-up Chain。历史输入粒度与原版章节数量见[专项项目记录](../project/README.md)和[历史审计](history/README.md)，不能混入下面的当前正文合计。

<!-- current-scope:start -->
## 现有模块与认知主线

| 顺序 | 模块 | 正文 | 认知主线 |
|---:|---|---:|---|
| 01 | [Python](../../curriculum/01-python/README.md) | 13 | 数据与对象 → 函数与执行 → 对象协作与输入边界 → 运行机制、并发与成本 |
| 02 | [FastAPI](../../curriculum/02-fastapi/README.md) | 16 | 请求与数据契约 → 依赖、资源与执行 → 流式交付与访问控制 → 外部工作、取消与退出 → 测试、部署与综合实践 |
| 03 | [MySQL](../../curriculum/04-mysql/README.md) | 19 | 表与 SQL → 关系、约束与统计 → 索引与执行计划 → 事务、MVCC、锁与恢复 → 分页、结构演进与批量写入 → 复制、CDC 与分片 → 应用数据建模与跨系统边界 |
| 04 | [Redis](../../curriculum/05-redis/README.md) | 18 | 数据与生命周期 → 缓存读取、更新与失效 → 执行成本与多步修改 → 持久化、复制与分片 → 消息、状态与故障判断 |
| 05 | [Backend](../../curriculum/03-backend-engineering/README.md) | 22 | 请求责任与持久状态 → 网络与流式交付 → 执行者、容量与等待预算 → 操作身份、幂等与重试 → 消息、可靠任务与一致性 → 安全、观测、部署与演进 |
| 06 | [Vector DB](../../curriculum/06-vector-db/README.md) | 16 | 向量、距离与精确基线 → 图、倒排与压缩索引 → 索引选择 → 数据、过滤与版本 → 分布式执行、评测与维护 |
| 07 | [LLM Foundation](../../curriculum/07-llm-foundation/README.md) | 14 | Token 与上下文 → Transformer、注意力与位置 → 生成与解码 → KV 缓存与推理服务 → 模型接口、检索模型与多模态 → Prompt、事实性与训练干预 |
| 08 | [RAG](../../curriculum/08-rag/README.md) | 14 | 任务与语料 → 解析、清洗与切分 → 查询与检索 → 融合、重排与证据组装 → 回答、引用与评测 → 权限、版本和生产治理 |
| 09 | [Agent](../../curriculum/09-agent/README.md) | 24 | 任务与执行角色 → 工具契约、发现与受控执行 → 计划、上下文与记忆 → 状态、持久化与恢复 → 安全、协议、扩展与协作 → 诊断、评测与工程落地 |
| 10 | [System Design](../../curriculum/10-system-design/README.md) | 19 | 需求与容量 → API、状态和数据 → 缓存、分区与协作 → 一致性、队列、安全与可靠性 → 观测、评估和演进 → 综合系统方案 |

合计 **175 篇**；章节标题和顺序可回到各模块入口逐项核对。
<!-- current-scope:end -->
