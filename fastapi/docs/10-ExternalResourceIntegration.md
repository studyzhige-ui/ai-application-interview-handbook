# 10｜DB、Redis、Vector DB 与 LLM Client 集成：资源边界与 Service Layer

FastAPI 真正进入 AI Application 后，很快会同时连接：

```text
MySQL
Redis
Vector DB
LLM Provider
External Tool API
```

这一章不重复数据库内部机制，而是讲：

> **这些外部资源怎样安全地接入 Request Lifecycle。**

---

## 1. Route 不应该直接承担所有集成逻辑

推荐结构：

```text
Router
→ Service
→ Repository / Provider Adapter
```

例如：

```python
@app.post("/chat")
async def chat(req: ChatRequest, user: CurrentUser):
    return await chat_service.run(req, user)
```

Router 只负责：

- HTTP Contract；
- Request Context；
- Response Mapping。

业务编排放 Service。

---

## 2. Application-scoped Client vs Request-scoped Session

典型划分：

```text
HTTP Client / Redis Client / Vector Client / LLM Client
→ Application scoped

DB Session / Transaction
→ Request or business-operation scoped
```

原因：Client/Pool 适合复用；Transaction 通常要和业务操作边界对齐。

---

## 3. HTTP / LLM Client 为什么要复用

如果每次请求都创建新 Client：

```text
new TCP/TLS
→ no connection reuse
→ more sockets
→ latency / resource overhead
```

更合理：

```text
lifespan startup
→ create provider client / pool
→ many requests reuse
→ shutdown close
```

---

## 4. DB Session 的常见 Dependency

```python
async def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        await session.close()
```

但 Transaction 不应该隐含得让人看不懂。

要明确：

```text
谁 begin？
谁 commit？
异常谁 rollback？
事务跨几个 Repository？
```

这些是 Service Boundary 的一部分。

---

## 5. FastAPI 不决定你用 sync 还是 async Driver

选择取决于：

- Driver 能力；
- Workload；
- 团队栈；
- Pool / Transaction 语义；
- 性能与稳定性验证。

不能简单说：

> FastAPI 是 async，所以数据库必须全部 async。

如果同步 Driver 稳定成熟，也可以通过合适执行边界使用。

---

## 6. Redis Client 生命周期

Redis 常承担：

- Cache；
- Session；
- Rate Limit State；
- 短期 Agent State。

FastAPI 层要关心：

```text
client / pool reuse
request timeout
key contains tenant dimension
serialization boundary
```

Redis 内部 TTL、Cluster、Lock 等细节回到 Redis 模块。

---

## 7. Vector DB / RAG Client

FastAPI Query API 可能：

```text
Request
→ validate tenant / kb
→ query rewrite
→ vector / hybrid retrieval
→ rerank
→ build context
→ model generation
```

FastAPI 只负责 API/Transport。

不要把 RAG Pipeline 所有函数都塞进 Route。

---

## 8. LLM Provider Adapter

如果业务里到处：

```python
await openai_client...
await other_provider...
```

会让 Service 和供应商接口耦合。

更清晰：

```text
ChatService
→ ModelProvider interface
→ ProviderAAdapter / ProviderBAdapter
```

FastAPI 只注入或访问统一 Service。

---

## 9. Timeout / Retry 不要散落每个 Route

坏模式：

```python
@app.post(...)
async def a():
    for _ in range(3): ...

@app.post(...)
async def b():
    for _ in range(5): ...
```

更合理：

```text
Provider Adapter / Backend Policy
→ timeout
→ retry
→ error classification
```

这些通用可靠性机制会在 AI Backend Engineering 系统讲解。

---

## 10. Data Mapping Boundary

不要让 API Schema、ORM Object、Domain Object、Provider Payload 全部混成一个对象。

推荐认识：

```text
API DTO
→ Domain / Service Model
→ Persistence / Provider Model
```

小项目可以简化，但边界意识要有。

---

## 11. Pool Exhaustion 怎么定位

假设 P99 突然上涨：

```text
FastAPI latency high
↓
CPU normal
↓
DB query itself fast
↓
connection acquisition slow
```

问题可能不是 SQL，而是：

```text
DB Pool Exhaustion
```

所以 Trace 最好区分：

```text
acquire connection
query
serialize
```

---

## 12. Transaction 和 Streaming 不要随便绑在一起

如果 Stream 持续 60 秒，同时一直持有 DB Transaction：

```text
long transaction
→ lock / version retention
→ pool pressure
```

更常见：

```text
短事务读取 / 写入
→ commit / release
→ start long stream
```

除非业务明确要求长事务。

---

## 13. 🎯 面试怎么回答

> FastAPI 接外部系统时我会先区分 Application-scoped Client/Pool 和 Request/Operation-scoped Session。HTTP、Redis、Vector、LLM Client 通常通过 Lifespan 复用连接池；DB Session 用 Dependency 管理并由 Service 定义 Transaction Boundary。Route 保持薄，业务编排进入 Service，Provider/Repository 负责具体外部协议。这样 Timeout、Trace、测试和后续 Provider 替换都更清晰。

---

## 14. 本章自测

<details>
<summary>1. 为什么 LLM HTTP Client 不适合每个请求都重新创建？</summary>

会丢失连接复用，增加 TCP/TLS 和 socket 开销，也使高并发下资源管理更抖动。

</details>

<details>
<summary>2. DB Session 和 Redis Client 为什么常有不同生命周期？</summary>

DB Session/Transaction 往往绑定单次业务操作；Redis Client 更像长期可复用连接池入口。

</details>

<details>
<summary>3. 为什么 Streaming 前最好释放不再需要的 DB Transaction？</summary>

长时间 Stream 会延长事务和连接占用，增加锁、版本和 Pool 压力。

</details>
