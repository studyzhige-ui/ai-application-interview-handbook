# 01. MySQL 在 AI Application 中负责什么

很多人第一次做 AI 项目时，会产生一个错觉：

> “我已经有大模型、向量数据库和 Redis 了，还需要 MySQL 吗？”

需要，而且一旦系统从 Demo 进入真实用户环境，MySQL 往往很快就会重新出现。

这一章先不讲 B+Tree，也不讲 MVCC。我们先回答一个更基础的问题：**MySQL 在完整 AI Application / Agent Backend 里到底负责什么。**

---

## 1. 先讲人话：MySQL 更像“业务事实账本”

假设你做一个企业 Agent 平台。

模型负责“推理”，Vector DB 负责“相似检索”，Redis 很适合“缓存 / Session / 短期状态”，但系统仍然需要长期、结构化、可查询、可事务化地保存很多事实：

```text
谁创建了这个 Agent？
属于哪个 Tenant？
这个用户有什么权限？
某次 Agent Run 当前是什么状态？
这个订单到底有没有支付？
一条 Tool Execution 是否已经成功？
某个知识库文档是什么版本？
这次运行消耗了多少 Token？
Evaluation 结果是什么？
```

这些信息的共同特点是：

- 有明确 Schema；
- 经常有实体之间的关系；
- 需要条件查询、排序、聚合；
- 某些更新必须一起成功或一起失败；
- 出错后必须知道“最终事实是什么”；
- 不能因为进程重启就消失。

这正是关系数据库擅长的区域。

💡 **新手理解**：

> LLM 像“大脑”，Vector DB 像“语义检索目录”，Redis 像“高速工作台”，MySQL 更像“正式业务账本”。

这个比喻不完全等价，但非常适合先建立边界感。

---

# 2. 一个 AI Application 里常见的 MySQL 数据

## 2.1 用户与租户

```text
users
tenants
memberships
roles
permissions
```

例如：

```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL
);
```

这里你通常关心：

- email 是否唯一；
- 用户属于哪个 Tenant；
- 权限更新能否可靠落库；
- 删除一个用户时关联数据怎么办。

这些问题不是 Embedding 相似度问题。

---

## 2.2 Conversation / Message

AI Chat 常见：

```text
conversation
  ├─ message 1
  ├─ message 2
  ├─ message 3
  └─ ...
```

你可能会存：

```sql
CREATE TABLE conversations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tenant_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    title VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    INDEX idx_user_updated (user_id, updated_at)
);
```

然后高频查询是：

```sql
SELECT id, title, updated_at
FROM conversations
WHERE user_id = 10001
ORDER BY updated_at DESC
LIMIT 20;
```

这类 Query Pattern 会直接决定后面索引怎么建。

---

## 2.3 Agent Run / Task State

例如：

```sql
CREATE TABLE agent_runs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    tenant_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    status VARCHAR(32) NOT NULL,
    model_name VARCHAR(64) NOT NULL,
    token_cost INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    INDEX idx_tenant_user_created (tenant_id, user_id, created_at),
    INDEX idx_status_created (status, created_at)
) ENGINE=InnoDB;
```

一次 Run 可能经历：

```text
PENDING
  ↓
RUNNING
  ↓
SUCCEEDED
```

也可能：

```text
RUNNING
  ↓
FAILED
  ↓
RETRYING
  ↓
SUCCEEDED
```

这个状态如果涉及计费、任务领取、幂等、并发 Worker，就会自然进入事务与锁。

---

## 2.4 Tool Execution / 外部副作用记录

Agent 调用：

- 发邮件；
- 修改数据库；
- 创建订单；
- 调支付接口；
- 修改代码库；
- 创建工单。

这些动作可能产生不可重复的副作用。

因此系统常需要持久化：

```text
run_id
tool_name
idempotency_key
request_hash
status
external_request_id
started_at
finished_at
```

后面你会发现：

> **MySQL 事务解决数据库内部原子性，但跨外部 API 的副作用不能只靠一个本地事务解决。**

这部分完整语义属于 AI Backend Engineering / Agent Runtime，但 MySQL 是其中非常重要的一块持久化基础。

---

## 2.5 Knowledge Base Metadata

RAG 中，大文件正文 / Chunk Vector 未必存在 MySQL，但很多“管理事实”很适合放关系库：

```text
document_id
knowledge_base_id
tenant_id
filename
content_hash
version
parse_status
index_status
permission
created_at
updated_at
```

例如：

```sql
CREATE TABLE documents (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    kb_id BIGINT NOT NULL,
    tenant_id BIGINT NOT NULL,
    content_hash CHAR(64) NOT NULL,
    version INT NOT NULL,
    parse_status VARCHAR(32) NOT NULL,
    index_status VARCHAR(32) NOT NULL,
    created_at DATETIME NOT NULL,
    UNIQUE KEY uk_kb_hash_version (kb_id, content_hash, version)
);
```

向量可以存在 Vector DB，原文件可以存在 Object Storage，但“这个版本是不是当前有效版本”仍然需要可靠的数据模型。

---

# 3. MySQL、Redis、Vector DB、Object Storage 到底怎么分工

不要记成“谁快用谁”。先看数据语义。

| 存储 | 更擅长什么 | 典型 AI 场景 |
|---|---|---|
| MySQL | 结构化事实、关系、事务、查询 | User、Tenant、Run、Permission、Billing、Metadata |
| Redis | 低延迟 KV / 数据结构、Cache、短期状态 | Session、Rate Limit、Hot Cache、临时 Run State |
| Vector DB | ANN / Semantic Similarity | Chunk Vector、语义检索 |
| Object Storage | 大对象 / 文件 | PDF、图片、音视频、导出结果 |
| Search Engine | 倒排、全文检索、复杂搜索 | Keyword Search、日志搜索、文档全文 |

### 一个常见组合

```text
                       ┌─────────── MySQL
                       │            用户 / 权限 / 元数据 / 状态
User → API → Service ──┼─────────── Redis
                       │            Cache / Session / Rate Limit
                       ├─────────── Vector DB
                       │            Embedding / ANN
                       └─────────── Object Storage
                                    PDF / Image / Artifact
```

🎯 **面试怎么答**：

> 我不会按“某数据库更高级”来选，而是先看数据访问模式和一致性要求。结构化业务事实、事务和关系查询通常优先 MySQL；高频临时状态和 Cache 用 Redis；语义向量检索交给 Vector DB；大文件交给对象存储。真正的生产系统通常是组合，而不是一个数据库包打天下。

---

# 4. 为什么本手册主要讲 InnoDB

现代 MySQL 可以有多种 Storage Engine，但业务系统里最核心的是 InnoDB。

官方文档明确说明，MySQL 8.4 中 InnoDB 是默认存储引擎，并提供：

- ACID Transaction；
- Commit / Rollback；
- Crash Recovery；
- Row-level Locking；
- Consistent Nonlocking Read；
- Clustered Index；
- Foreign Key。

所以后面如果没有额外说明：

> 本手册里的“事务、MVCC、聚簇索引、Record / Gap / Next-Key Lock”等，都默认讨论 **InnoDB**。

⚠️ **易错点**：

不要说：

> “MySQL 本身就是 B+Tree / MVCC。”

更准确的说法是：

> “在我们讨论的 MySQL + InnoDB 语境中，InnoDB 提供事务、MVCC、聚簇索引和相关锁机制。”

MySQL Server 层和 Storage Engine 层要慢慢学会区分。

---

# 5. MySQL Server 与 InnoDB 不是一层

先建立一个非常重要的粗略分层：

```text
Client
  ↓
MySQL Server
  ├─ Connection / Session
  ├─ Parser
  ├─ Optimizer
  └─ Executor
       ↓
Storage Engine API
       ↓
InnoDB
  ├─ Buffer Pool
  ├─ B+Tree Index
  ├─ Transaction / MVCC
  ├─ Lock
  ├─ Redo / Undo
  └─ Physical Storage
```

这个图以后会不断出现。

例如：

- “SQL 怎么解析 / 优化”更多属于 Server 层；
- “数据页怎么组织”属于 InnoDB；
- “B+Tree 怎么找数据”属于 InnoDB Index；
- “Optimizer 为什么没选这个索引”又回到 Server Optimizer 的成本选择。

🧠 **为什么一定要区分？**

因为很多低质量八股会把所有东西都说成“MySQL 做的”，最后遇到：

> “Optimizer 不用索引，是不是索引失效了？”

就只能背口诀。

真正理解以后，你会知道：

```text
Index 存在
≠
Index 一定可用于当前 Access Path
≠
Optimizer 一定认为走 Index 成本最低
```

这是后面第 8、9 章的核心。

---

# 6. 一条数据从“业务对象”变成关系表

假设 Agent Run 在代码里长这样：

```python
class AgentRun:
    id: int
    user_id: int
    tenant_id: int
    status: str
    model_name: str
    token_cost: int
    created_at: datetime
```

进入数据库以后，不是简单“把对象存进去”，而是开始面对：

```text
Schema
→ Data Type
→ Constraint
→ Primary Key
→ Index
→ Transaction
→ Query Pattern
→ Scale
```

例如：

```sql
SELECT id, status, model_name, created_at
FROM agent_runs
WHERE tenant_id = 7
  AND user_id = 10001
ORDER BY created_at DESC
LIMIT 20;
```

这条查询会反过来决定：

```sql
INDEX idx_tenant_user_created (tenant_id, user_id, created_at)
```

也就是说：

> **表设计不是先凭感觉建字段，再到慢了以后乱加索引。Query Pattern 本身就是 Schema / Index Design 的输入。**

---

# 7. AI 系统里最常见的几个误区

## 误区一：所有聊天记录都丢 Redis

Redis 可以做 Session / Hot Conversation Cache，但长期历史、审计、筛选、统计未必应该只依赖 Redis。

问题包括：

- 生命周期；
- 成本；
- 查询模式；
- 持久化语义；
- 数据治理。

---

## 误区二：有 Vector DB 就不需要关系库

Vector DB 回答的是：

> “哪些向量和 Query 最像？”

MySQL 经常回答的是：

> “这个 Document 属于谁？当前版本是多少？用户有没有权限？是不是已删除？Index Job 是否完成？”

完全不是一类问题。

---

## 误区三：事务能解决所有分布式一致性

本地事务可以保护同一个数据库内的一组操作，但不能自动让：

```text
MySQL
+ Redis
+ Message Queue
+ Payment API
+ External Tool
```

一起具备一个全局 ACID 事务。

因此后续会把：

- MySQL 事务机制；
- MySQL + Redis 最终一致性；
- MQ / Outbox；
- Tool Idempotency；

放在各自正确的层里，而不是全塞进“MySQL 事务”。

---

# 8. 从真实面试看，这一模块最终会追到哪里

冻结 HUMAN-A 数据中，MySQL 不是只问定义。

常见递进是：

```text
你的表怎么设计？
    ↓
为什么建这个 Index？
    ↓
数据多了以后为什么变慢？
    ↓
EXPLAIN 看什么？
    ↓
并发事务会不会读错 / 锁住？
    ↓
量再大要不要 Sharding？
```

这也是本手册为什么不从“100 道 MySQL 面试题”开始，而从系统执行路径开始。

---

# 9. 本章面试表达

### Q：AI 应用里 MySQL 通常存什么？

🎯 可以这样回答：

> 我会把 MySQL 主要当成结构化业务事实和事务状态的持久层，例如 User/Tenant、Conversation Metadata、Agent Run、Tool Execution、Permission、Billing、Knowledge Base Metadata 等。Vector DB 更适合语义向量，Redis 更适合 Cache、Session 和短期状态，大文件放 Object Storage。生产系统通常根据数据语义组合多种存储，而不是用一个数据库解决所有问题。

### Q：为什么默认讨论 InnoDB？

🎯 可以这样回答：

> 因为现代 MySQL 业务表通常使用默认的 InnoDB。InnoDB 提供事务、行级锁、一致性读、MVCC、聚簇索引和 Crash Recovery。后面讲隔离级别、MVCC、Gap/Next-Key Lock 等机制时，本质上是在讲 InnoDB 的实现与语义。

---

# 10. 面试官可能继续追问

🔍 **追问 1：MySQL 和 Redis 怎么保证一致？**

先不要急着回答“双删”。完整问题放在 AI Backend Engineering，并在第 22 章建立边界。

🔍 **追问 2：Agent Run 状态存在 MySQL，多个 Worker 同时抢任务怎么办？**

会进入事务、锁、幂等和任务调度。

🔍 **追问 3：Knowledge Base Metadata 为什么不全部放 Vector DB？**

从事务、权限、关系查询、版本治理和检索职责边界回答。

🔍 **追问 4：什么时候应该分库分表？**

不要回答“数据超过 500 万就分”。第 19 章会专门解释为什么不能用一个固定行数阈值代替容量分析。

---

# 11. 本章自测

<details>
<summary>1. 为什么说 MySQL 更像 AI Application 的“业务事实账本”？</summary>

因为它适合保存结构化、关系明确、需要事务和长期持久化的业务事实，例如用户、权限、任务状态、计费和文档元数据。这个比喻不是说 MySQL 只能做账本，而是用来和 Redis / Vector DB / Object Storage 建立职责边界。

</details>

<details>
<summary>2. Agent 的 Memory 是否应该全部存在 MySQL？</summary>

不一定。Memory 是 Agent Runtime 的语义模型，具体 Storage 可以按访问模式选择 MySQL、Redis、Vector DB 或文件等。MySQL 适合其中结构化、需要事务或长期管理的部分，但“Memory 怎样写入 / Recall / Compaction”本身属于 Agent Harness。

</details>

<details>
<summary>3. 为什么“有 Vector DB 就不需要 MySQL”是错误的？</summary>

因为向量检索解决相似度搜索，而真实业务还需要身份、权限、版本、状态、事务、聚合和关系查询。两者解决的问题不同。

</details>

<details>
<summary>4. MySQL Server 与 InnoDB 应怎样粗略区分？</summary>

Server 层负责连接、SQL 解析、优化与执行等；InnoDB 是存储引擎，负责数据页、索引、事务、MVCC、锁、redo/undo 等核心存储能力。真实执行过程中两层会协作。

</details>

---

# 12. 官方资料

本章事实基线：

- MySQL 8.4 Reference Manual — The InnoDB Storage Engine  
  <https://dev.mysql.com/doc/refman/8.4/en/innodb-storage-engine.html>
- MySQL 8.4 Supported Storage Engines  
  <https://dev.mysql.com/doc/refman/8.4/en/storage-engines.html>
- MySQL Releases: Innovation and LTS  
  <https://dev.mysql.com/doc/refman/8.4/en/mysql-releases.html>

下一章开始真正进入：

> **一条 SQL 从 Client 发给 MySQL，到底经历了什么。**
