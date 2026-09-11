# 16｜Graph DB vs Vector DB，以及 Vector DB 在 AI 系统中的位置

学到这里，我们已经知道 Vector DB 能做什么：

```text
Vector
→ Similarity / Distance
→ Exact / ANN
→ HNSW / IVF
→ Metadata Filter
→ Lifecycle / Shard / Replica
```

最后一个问题不是“Vector DB 还能多存什么”，而是：

> **它在完整 AI 系统里到底负责什么，又不负责什么？**

这也是为什么面试里经常出现：

- Vector DB 和 Graph DB 有什么区别？
- 为什么不把所有数据都塞进 Vector DB？
- MySQL、Redis、Vector DB 怎么分工？
- Knowledge Graph 和 Vector Retrieval 能不能一起用？

这一章用来收住边界。

---

# 1. 先讲人话：两种数据库在回答不同问题

假设我们有企业知识库。

用户问：

> “有没有和员工报销标准相关的文档？”

这更像：

```text
找语义相近的内容
```

Vector DB 擅长。

但如果用户问：

> “这个制度由哪个部门维护？这个部门归哪个 VP？该制度引用了哪些上位政策？”

这更像：

```text
实体之间是什么关系？
沿关系可以走到哪里？
```

Graph DB 更自然。

一句话：

```text
Vector DB：按“像不像”找邻居
Graph DB：按“谁和谁有什么关系”走图
```

---

# 2. Vector DB 的核心数据模型

Vector DB 常见逻辑形态：

```text
ID
+
Vector
+
Metadata
+
Payload / Reference
```

例如：

```text
chunk_id = c_001
vector = [0.13, -0.28, ...]
doc_id = d_100
tenant_id = t_01
category = policy
created_at = ...
```

查询重点通常是：

```text
给定 query vector
→ 找最近邻
→ 可带 metadata filter
→ 返回 Top-K candidate
```

核心能力是：

> **高维向量的高效相似性搜索。**

---

# 3. Graph DB 的核心数据模型

Graph DB 更强调：

```text
Node / Vertex
Edge / Relationship
Property
```

例如：

```text
[Policy]
   |
   | OWNED_BY
   v
[Finance Department]
   |
   | REPORTS_TO
   v
[VP Finance]
```

或者：

```text
Document --CITES--> Policy
Policy   --APPLIES_TO--> EmployeeType
Person   --MEMBER_OF--> Department
```

查询重点更像：

```text
从这个实体出发
→ 沿某类关系走 1 / 2 / N 跳
→ 找符合 pattern 的节点
```

核心能力是：

> **显式关系建模与图遍历。**

---

# 4. 两者最关键的区别

| 维度 | Vector DB | Graph DB |
|---|---|---|
| 核心问题 | 谁和 Query 最相似 | 谁与谁存在什么关系 |
| 核心结构 | Vector + Metadata | Node + Edge + Property |
| 查询方式 | Nearest Neighbor / ANN | Traversal / Pattern Match |
| 关系是否显式 | 通常不是 | 是 |
| 语义近似 | 强 | 不是主要能力 |
| 多跳关系 | 不是强项 | 强项 |
| 典型用途 | Semantic Retrieval | Knowledge Graph / Relationship Query |

⚠️ 不要把区别说成：

> “Vector DB 存向量，Graph DB 存图。”

这句话没错，但面试里更重要的是：

> **两者优化的是不同的查询模型。**

---

# 5. Embedding 中“关系近”不等于图关系存在

这是非常重要的边界。

假设：

```text
A = 报销制度
B = 财务政策
```

它们 Vector 很近，说明：

```text
语义相似 / 相关
```

但不等于：

```text
A --OWNED_BY--> B
A --CITES--> B
A --SUPERSEDES--> B
```

Embedding 通常把大量信息压缩进连续向量空间，擅长表达“整体语义接近”。

Graph Edge 则表达：

```text
关系类型
方向
约束
业务语义
```

所以：

> **Similarity 不能替代显式关系。**

---

# 6. Graph DB 也不能替代 Vector DB

反过来也一样。

如果用户问：

> “有没有讲员工异地出差住宿标准的文档？”

知识图谱里可能没有：

```text
Query Text
→ 精确实体
```

尤其用户使用自然语言、同义词或模糊表达时。

Vector Retrieval 更适合先完成：

```text
自然语言 Query
→ Semantic Candidate Discovery
```

所以：

```text
Graph 强关系
Vector 强语义邻近
```

不是谁完全替代谁。

---

# 7. 两者可以组合吗？

可以，而且这正是很多复杂知识系统的自然方向。

一种思路：

```text
User Query
   ↓
Embedding
   ↓
Vector Retrieval
   ↓
找到候选 Entity / Document
   ↓
Graph Expansion
   ↓
沿引用 / 所属 / 依赖 / 时间关系扩展
   ↓
形成更完整 Context
```

另一种：

```text
Query
 ↓
先识别 Entity / Relation
 ↓
Graph Query
 ↓
得到候选实体集合
 ↓
Vector Similarity
 ↓
在候选集合中做语义排序
```

也可以叫：

```text
Vector + Graph Hybrid Retrieval
```

但它不是本模块的 RAG Retrieval 主线。

完整：

```text
GraphRAG
Knowledge Graph Retrieval
Hybrid Retrieval Evaluation
```

应该在 RAG / System Design 中继续深化。

---

# 8. 为什么不能“什么都放 Vector DB”

一个 AI Application 里可能有：

```text
User
Tenant
Conversation
Document
Chunk
Permission
Agent Run
Tool Execution
Embedding
Session
Billing
```

如果全部塞进 Vector DB，就会把不同数据语义混在一起。

## 8.1 业务 Source of Truth

例如：

```text
用户余额
订单
Tenant 权限
Agent Run 状态
```

需要：

- Transaction；
- Constraint；
- 精确查询；
- 更新语义；
- 可靠持久化。

通常 MySQL / PostgreSQL 更自然。

## 8.2 短期高速状态

例如：

```text
Session
Rate Limit Counter
Cache
短 TTL 状态
```

Redis 更自然。

## 8.3 语义检索

例如：

```text
Chunk Embedding
FAQ Embedding
Image Embedding
```

Vector DB 更自然。

## 8.4 显式关系

例如：

```text
Person → Department
Document → Policy
Service → Dependency
```

复杂多跳时 Graph DB 更自然。

所以数据库选型的第一原则不是：

> 哪个最先进？

而是：

> **当前数据的核心查询模型是什么？**

---

# 9. 一个 AI Application 中的数据分工

可以先建立一个简单心智模型：

```text
                         AI Application
                               │
             ┌─────────────────┼──────────────────┐
             ▼                 ▼                  ▼
           MySQL             Redis            Vector DB
             │                 │                  │
     Business Truth      Hot / Ephemeral      Semantic Index
     User / Tenant       Session / Cache      Chunk Vector
     Permission          Rate Limit           ANN Search
     Run Metadata        Short State          Metadata Filter
```

如果还存在复杂显式知识关系：

```text
                         Graph DB
                            │
                      Entity / Relation
                      Multi-hop Traversal
```

这不是固定架构模板，而是职责划分思维。

---

# 10. Vector DB 通常不是 Source of Truth

这是 AI 系统设计里一个很重要的原则。

例如：

```text
Document
→ Parse
→ Chunk
→ Embedding
→ Vector DB
```

真正的原始文档可能在：

```text
Object Storage
```

文档元数据、版本、权限可能在：

```text
MySQL / PostgreSQL
```

Vector DB 保存的是：

```text
Derived Search Representation
```

也就是：

> **从原始内容派生出来、用于检索的索引状态。**

这带来非常重要的工程判断：

如果 Vector Index 损坏或模型升级，理想情况下系统应该能够：

```text
Source Data
+ Version Metadata
+ Embedding Model
→ Rebuild Vector Index
```

而不是：

> “Vector DB 没了，原始知识也彻底没了。”

---

# 11. 为什么 Vector DB 和 RAG 必须分模块学习

很多教程直接：

```text
文档
→ Embedding
→ Milvus
→ TopK
→ LLM
```

然后把所有东西都叫 Vector DB。

但实际上至少有两层：

## Vector Infrastructure

```text
Vector Storage
Distance
ANN
Index
Filter
Lifecycle
Scale
```

这是本模块。

## Retrieval System

```text
Query Rewrite
Dense / Sparse
Hybrid
RRF
Rerank
Top-K Strategy
Context Build
Evaluation
Bad Case Attribution
```

这是 RAG。

为什么要拆？

因为可能出现：

```text
Vector DB 很快
ANN Recall 很高
```

但：

```text
最终 RAG 还是答错
```

原因可能在：

- Chunk；
- Embedding Model；
- Query Rewrite；
- Hybrid Retrieval；
- Reranker；
- Context Construction；
- Generation。

不能把一切问题都归因于 Vector DB。

---

# 12. Vector DB 的 Production 检查清单

真正选一个 Vector DB，不应该只问：

> 支不支持 HNSW？

还要问：

```text
数据规模是多少？
维度多大？
更新频率多高？
Delete 多不多？
Filter 复杂吗？
多租户怎么隔离？
P95 / P99 要多少？
Recall 目标多少？
内存预算多少？
索引能不能在线 Build / Rebuild？
备份恢复怎么做？
Shard / Replica 怎么做？
版本升级怎么迁移？
Embedding Model 换了怎么办？
```

这正是前 22 章最终汇合的地方。

---

# 13. 面试怎么答

## Q：Vector DB 和 Graph DB 有什么区别？

🎯 **建议回答**：

> Vector DB 的核心查询模型是高维向量的近邻搜索，解决“哪些对象在语义空间里最相似”；Graph DB 的核心是显式 Node/Edge 关系和图遍历，解决“实体之间有什么关系以及如何多跳连接”。Embedding 中语义接近不能替代显式业务关系，反过来 Graph 也不擅长直接解决模糊自然语言的语义近邻，因此复杂知识系统里两者可以组合，而不是简单互相替代。

## Q：为什么不把所有数据都放 Vector DB？

> 因为不同数据有不同的核心查询和一致性需求。用户、权限、订单等业务事实更需要关系数据库的事务和约束；Session、Cache 等短期状态适合 Redis；Vector DB 更适合作为语义索引基础设施。很多情况下 Vector DB 存的是可重建的 Derived Index，而不是最终 Source of Truth。

## Q：Vector DB 在 RAG 里负责到哪里？

> 它负责 Vector Storage、Similarity Search、ANN Index、Metadata Filter、Index Lifecycle 和 Scale；Dense/Sparse 组合、Query Rewrite、RRF、Rerank、Top-K 策略、Retrieval Evaluation 属于更上层的 RAG Retrieval System。

---

# 14. 高频易错点

⚠️ **Vector Similarity = 显式关系。**  
错误。相似不等于 `CITES / OWNED_BY / DEPENDS_ON`。

⚠️ **Graph DB 可以天然替代 Vector DB 做 Semantic Search。**  
不是它的核心查询模型。

⚠️ **Vector DB 应该保存系统全部业务数据。**  
通常职责过载。

⚠️ **Vector DB 一定是 Source of Truth。**  
很多 AI 系统里它更像可重建的 Derived Semantic Index。

⚠️ **RAG 的 Retrieval Quality = Vector DB Quality。**  
RAG 是更长的 Pipeline。

⚠️ **用了 Graph + Vector 就一定比单独 Vector 好。**  
引入 Graph 会增加 Extraction、Schema、维护与查询复杂度，必须证明收益。

---

# 15. 本章自测

<details>
<summary>1. Vector DB 和 Graph DB 最本质的区别是什么？</summary>

它们优化的是不同查询模型。Vector DB 优化高维相似性近邻搜索；Graph DB 优化显式实体关系建模和图遍历。

</details>

<details>
<summary>2. 为什么两个向量很近，不能说明它们存在明确业务关系？</summary>

Embedding 的距离主要表达连续语义空间中的相似或相关程度，而业务关系通常具有明确的类型、方向和约束，例如 `CITES`、`MEMBER_OF`、`DEPENDS_ON`，需要显式建模。

</details>

<details>
<summary>3. Vector DB 为什么经常更适合做 Derived Index，而不是 Source of Truth？</summary>

因为 Vector / ANN Index 常由原始文档、Metadata 和 Embedding Model 派生出来。模型升级、Index 损坏或版本迁移时，理想系统可以由权威源重新生成向量和索引。

</details>

<details>
<summary>4. MySQL、Redis、Vector DB 在 AI 系统里可以怎样粗略分工？</summary>

MySQL 保存长期结构化业务事实和事务状态；Redis 保存低延迟、短生命周期 Cache / Session / Counter 等；Vector DB 保存语义向量和 ANN Index。最终仍应按具体查询、一致性和规模需求选型。

</details>

<details>
<summary>5. 为什么 Vector DB 模块不直接把 Hybrid Search、RRF、Rerank 全讲完？</summary>

因为这些属于完整 Retrieval Strategy，需要和 Query、Sparse Retrieval、Reranker、Context Build、Evaluation 一起理解，Primary 更适合放在 RAG。Vector DB 先把向量基础设施自身闭环。

</details>

---

# 16. 到这里，你应该形成的最终认知

Vector DB 的完整因果链不是：

```text
Embedding
→ Milvus
→ TopK
```

而是：

```text
语义对象
→ Vector Representation
→ Dimension / Normalization
→ Similarity Metric
→ Exact Nearest Neighbor
→ Scale Problem
→ ANN
→ HNSW / IVF / Quantization
→ Index Selection
→ Schema / Metadata / Filter
→ Update / Delete / Compaction
→ Re-embedding / Rebuild
→ Shard / Replica
→ Capacity / Troubleshooting
→ Product Selection
→ System Boundary
```

下一模块开始补上模型侧基础：

> **LLM Foundation（应用工程深度）**

随后在 RAG 中再把：

```text
Embedding
+ Vector Infrastructure
+ Sparse Retrieval
+ Hybrid
+ Rerank
+ Evaluation
```

组合成真正的检索系统。
