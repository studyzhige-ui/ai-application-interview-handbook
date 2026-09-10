# 17. Schema Design：从访问模式设计表

前面一直在优化已经存在的表。

这一章开始换一个视角：

> **如果表还没建，怎样从业务访问模式出发，让后面的索引、事务、分页和扩展更自然？**

Schema Design 不是“字段类型背诵”，而是把：

```text
业务实体
+ 约束
+ 查询模式
+ 更新模式
+ 数据生命周期
```

翻译成关系模型。

---

## 1. 先讲人话：先问“怎么用”，再问“怎么存”

假设要存 Agent Run。

错误起点：

> “先建一张 `agent_runs`，以后缺字段再加。”

更好的起点是先列访问模式：

```text
按 tenant + user 查最近 Run
按 status 查待执行任务
按 run_id 精确查详情
按 created_at 清理历史数据
按 user 汇总 token_cost
```

这些访问模式会直接影响：

- 主键；
- 字段；
- 联合索引；
- 是否拆表；
- 是否冗余；
- 数据归档方式。

---

# 2. 一个基础表

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
    INDEX idx_tenant_user_created (tenant_id, user_id, created_at, id),
    INDEX idx_status_created (status, created_at, id)
) ENGINE=InnoDB;
```

为什么不是：

```text
一个 JSON 列把所有东西都塞进去？
```

因为关系数据库最擅长的就是：

```text
稳定字段
约束
查询
排序
Join
事务
索引
```

---

# 3. 第一原则：明确实体边界

AI Application 常见实体：

```text
User
Tenant
Conversation
Message
AgentRun
ToolExecution
KnowledgeBase
Document
Permission
UsageRecord
EvaluationCase
```

不要一开始就把它们全部塞进一张：

```text
ai_data
```

每个实体通常有自己的：

- 生命周期；
- 更新频率；
- 查询模式；
- 权限边界；
- 数据量级。

例如：

```text
Conversation
→ 数量中等，长期存在

Message
→ 数量很大，持续追加

ToolExecution
→ 更像事件日志，写多读少
```

把它们混在一起，索引和归档都会变得困难。

---

# 4. 第二原则：字段类型要反映真实语义

## ID

```sql
BIGINT
```

常见于高规模业务主键。

## 状态

```sql
VARCHAR(32)
```

或其它受控表达。

不要因为状态只有几个值，就机械地认为：

> “一定用 ENUM。”

要考虑：

- 状态会不会频繁演进；
- ORM / Migration 体验；
- 跨系统兼容；
- 约束是否由应用层维护。

## 时间

要明确：

```text
业务时区
UTC 约定
created_at / updated_at 语义
```

不要让不同服务各自猜时间含义。

---

# 5. `VARCHAR` 不是“越大越保险”

例如：

```sql
VARCHAR(65535)
```

看起来省事，但 Schema 设计要考虑：

- 最大长度是否真实需要；
- Row Size；
- Index Prefix / Key Size；
- 内存与临时操作；
- 数据是否应该拆到 Text / Object Storage。

尤其 LLM 输出很长时，不应简单把所有 Prompt / Response 全塞进核心 OLTP 行。

可以分层：

```text
MySQL
→ Metadata / Summary / Pointer

Object Storage
→ 大型原始内容 / 文件 / Artifact
```

---

# 6. NULL 到底该不该用

不要背：

> “MySQL 尽量不要 NULL。”

更应该问：

> **这个字段有没有明确的“未知 / 不存在”语义？**

例如：

```text
finished_at
```

Run 还没结束时：

```text
NULL
```

是非常自然的状态。

而：

```text
token_cost
```

通常可以：

```sql
NOT NULL DEFAULT 0
```

因为 0 有明确业务意义。

---

# 7. 主键要服务长期规模

前面已经讲过：

```text
短
稳定
最好单调
```

的聚簇主键通常对 InnoDB 更友好。

但业务还可能需要：

```text
Public ID
UUID
Snowflake ID
External Provider ID
```

可以考虑区分：

```text
内部 Clustered PK
vs
外部业务唯一标识
```

例如：

```sql
id BIGINT PRIMARY KEY AUTO_INCREMENT,
run_uuid BINARY(16) NOT NULL UNIQUE
```

是否这么做要看业务，不是固定模板。

---

# 8. Unique Constraint 是业务规则的一部分

假设同一个 Provider Request 不能重复创建 Usage Record。

可以：

```sql
UNIQUE KEY uk_provider_request(provider, request_id)
```

这样防重复不仅靠：

```text
Python if 查询
```

而是数据库层也表达：

> 这个业务 Key 必须唯一。

这对 Idempotency 很重要。

---

# 9. Index 要从 Query Pattern 反推

需求：

```text
查 tenant 下某 user 最近 50 条 Run
```

SQL：

```sql
SELECT ...
FROM agent_runs
WHERE tenant_id=?
  AND user_id=?
ORDER BY created_at DESC, id DESC
LIMIT 50;
```

索引：

```text
(tenant_id, user_id, created_at, id)
```

不是因为“四列联合索引比较高级”，而是它自然匹配：

```text
过滤
→ 排序
→ 分页
```

---

# 10. 高频更新列进索引要谨慎

假设：

```text
status
```

每个 Run 会：

```text
PENDING
→ RUNNING
→ TOOL_WAIT
→ RUNNING
→ SUCCESS
```

如果 status 出现在很多索引中，每次状态更新可能同时维护多个 B+Tree。

所以索引设计需要问：

```text
这个字段查询收益多大？
更新频率多高？
选择性如何？
索引会不会越来越宽？
```

---

# 11. Normalize：为什么要拆表

例如：

```text
Conversation
有 10000 条 Message
```

不要建：

```text
conversation.message_1
conversation.message_2
...
```

而是：

```text
conversations
      1
      ↓
      N
messages
```

关系模型让：

- 数据增长自然；
- 查询清晰；
- 权限明确；
- 单行不会无限变宽。

---

# 12. Denormalization：为什么有时又要冗余

规范化不是宗教。

假设 Message 列表每次都要显示：

```text
conversation_title
```

如果纯理论规范化要求每条 Message 都 Join 多张表，某些高频读路径可能很重。

可以考虑：

- 冗余一个稳定派生值；
- 维护 Summary Table；
- Cache；
- Read Model。

关键问题是：

> **冗余数据谁负责保持一致？**

所以 Denormalization 是：

```text
用写复杂度
换读性能
```

的 Trade-off。

---

# 13. 大字段和热字段为什么可能要拆

假设 `agent_runs` 里同时放：

```text
status
created_at
prompt 2MB
response 5MB
trace 10MB
```

列表查询虽然只需要：

```text
id + status + created_at
```

但核心表非常宽，存储与 Buffer Pool 局部性都会受到影响。

可以拆：

```text
agent_runs
→ 高频元数据

agent_run_payloads
→ 大型 Prompt / Response

Object Storage
→ 更大的 Artifact / File
```

这叫冷热 / 宽窄数据分离思想。

---

# 14. Soft Delete 不是免费功能

常见：

```sql
deleted_at DATETIME NULL
```

然后所有查询：

```sql
WHERE deleted_at IS NULL
```

如果数据长期只软删不清理：

```text
表越来越大
索引越来越大
查询都多一个过滤条件
唯一约束变复杂
```

所以 Soft Delete 要同时设计：

```text
保留周期
归档
物理清理
唯一键策略
审计需求
```

---

# 15. 多租户表的 Tenant Key

AI SaaS 非常常见：

```text
tenant_id
```

设计时要考虑：

```text
每个核心业务表是否都有 tenant_id？
所有 Query 是否必须带 tenant filter？
索引是否把 tenant_id 放在合适前缀？
权限层如何保证不会串租户？
```

例如：

```text
(tenant_id, user_id, created_at)
```

往往比单独：

```text
(user_id, created_at)
```

更符合 SaaS 数据隔离访问模式。

---

# 16. Constraint 能帮什么，不能帮什么

数据库可以表达：

```text
PRIMARY KEY
UNIQUE
NOT NULL
FOREIGN KEY
CHECK
```

但不能自动理解：

```text
Agent Run 一旦 SUCCESS 不允许回到 RUNNING
Enterprise Tenant 额度规则
某 Tool 只能特定 Role 调用
```

这些仍需要业务逻辑。

所以 Schema Constraint 是：

> **最后一道数据完整性防线之一，不是完整业务规则引擎。**

---

# 17. Schema Evolution 也要提前考虑

上线后一定会：

```text
加字段
改索引
加状态
迁数据
拆表
```

因此 Schema Design 还要考虑：

- Migration 是否 Online；
- Old / New Version 是否兼容；
- Backfill；
- Rollback；
- 大表 DDL 风险。

这属于从“设计一张表”升级到“维护一个长期系统”。

---

# 18. AI Application 场景：Conversation / Message

一个常见设计：

```text
conversations
- id
- tenant_id
- user_id
- title
- created_at
- updated_at

messages
- id
- conversation_id
- role
- content_ref / content
- token_count
- created_at
```

为什么分开？

```text
Conversation 是会话实体
Message 是 append-heavy 子实体
```

查询也不同：

```text
查最近会话
vs
查某会话的消息历史
```

对应不同索引。

---

# 19. 面试怎么答

## Q：你怎样设计一张业务表？

🎯 推荐回答：

> 我会先列实体边界和主要访问模式，再确定主键、业务唯一键、字段类型和约束，然后根据高频过滤、排序和分页路径设计联合索引，同时考虑更新频率、宽行、大字段、软删除、租户隔离和数据生命周期。最后再评估规模增长后的归档、Migration 和 Sharding，不会从字段列表直接开始。

## Q：为什么不能把 Agent 所有状态存一个 JSON？

> JSON 适合灵活、变化快、低频查询的扩展字段，但核心业务状态如果需要稳定约束、索引、排序、事务和统计，拆成明确关系字段更容易保证正确性和性能。大 Payload 也可以与高频元数据分层存储。

---

# 20. 高频易错点

⚠️ **Schema Design = 字段类型选择。**  
远不止。

⚠️ **越规范化越好。**  
读写 Trade-off 需要场景判断。

⚠️ **JSON 更灵活，所以所有 AI 数据都适合 JSON。**  
核心业务字段通常仍需要关系约束和索引。

⚠️ **加索引没有写成本。**  
每个 Secondary Index 都会增加写入维护。

⚠️ **Soft Delete 永远比物理删除安全。**  
它会累积数据和查询复杂度，必须有生命周期策略。

---

# 21. 本章自测

<details>
<summary>1. 为什么 Schema Design 应从访问模式开始？</summary>

因为主键、联合索引、排序、分页、宽窄表拆分和归档都由数据如何被读取和更新决定。只从字段列表出发，很容易建出“能存但不好用”的表。

</details>

<details>
<summary>2. 为什么高频更新字段进入很多索引会有成本？</summary>

字段每次修改都可能导致多个二级索引记录同步更新，增加 B+Tree 维护、Redo/Binlog 和写放大成本。

</details>

<details>
<summary>3. 为什么 Agent Run 的大 Prompt / Trace 可能适合从主表拆出去？</summary>

列表和状态查询通常只需要少量元数据。大字段会让核心行和相关页面变宽，降低 Buffer Pool 局部性并增加 I/O；拆分可以让高频路径更轻。

</details>

---

## 继续学习

单实例的表和索引设计好以后，下一步自然会出现：

> **读请求越来越多，一台 MySQL 扛不住怎么办？**

下一章：**Replication 与读写分离。**
