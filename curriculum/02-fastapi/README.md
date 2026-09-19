# FastAPI｜AI 应用服务层

[← Python Foundation](../01-python/README.md) · [↑ Handbook 总目录](../../README.md) · [Learning Path](../../guide/learning-path.md) · [AI Backend Engineering →](../03-backend-engineering/README.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：16 个连续知识小板块** · **HUMAN-A Canonical：4** · **独立来源覆盖：3**  
> **质量：Granularity / Coverage / Content Depth 已验收**

把 Python Runtime 能力组织成可校验、可 Streaming、可部署的 HTTP / ASGI AI Service。

---

## 1. 这个模块解决什么

把 Python Runtime 能力组织成可校验、可 Streaming、可部署的 HTTP / ASGI AI Service。

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

[Python Foundation](../01-python/README.md) → **FastAPI** → [AI Backend Engineering](../03-backend-engineering/README.md) → [MySQL](../04-mysql/README.md) → [Redis](../05-redis/README.md) → [Vector Database](../06-vector-db/README.md) → [LLM Foundation（应用工程深度）](../07-llm-foundation/README.md) → [RAG](../08-rag/README.md) → [Agent](../09-agent/README.md) → [System Design](../10-system-design/README.md)

当前模块角色：**Foundation / 把 Python Runtime 能力组织成可校验、可 Streaming、可部署的 HTTP / ASGI AI Service。**

---

## 3. 固定课程原则

> **知识体系演进顺序优先；真人面经只调整复习权重、真实问法和追问深度，不能反过来打乱初学者从 0→1 的主干。**

同时固定区分：

```text
Canonical Question = 可独立追问的面试能力
Capability Primitive = 更细的工程机制
教材 Markdown = 一个完整认知闭环
Section = 参数 / 变体 / Failure / 深挖追问
```

所以本模块是 **4 道 Canonical → 16 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
ASGI Request Lifecycle → API Contract / Validation → DI / Middleware / Resource Lifecycle → Async Boundary → SSE / WebSocket → Security / External Resource → Cancellation → Testing / Observability / Deployment → AI Service Patterns
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜从 Python 到 ASGI Service

1. [FastAPI 的职责：HTTP → ASGI → Application Request Lifecycle](docs/01-FastAPI职责与ASGI请求链路.md)
2. [Routing、Request / Response 与 OpenAPI Contract](docs/02-Routing与APIContract.md)
3. [Pydantic、Validation、Serialization 与 Error Contract](docs/03-Pydantic与数据契约.md)
4. [Dependency Injection 与 Middleware](docs/04-Dependency与Middleware.md)
5. [Resource Lifecycle：yield Dependency、scope 与 Lifespan](docs/05-ResourceLifecycle.md)
6. [Async Execution：def / async def、Blocking Boundary 与并发保护](docs/06-AsyncExecution与BlockingBoundary.md)

### Part B｜AI Service Transport 与安全

7. [Streaming Fundamentals 与 Server-Sent Events（SSE）](docs/07-Streaming与SSE.md)
8. [WebSocket 与 AI Event Protocol](docs/08-WebSocket与EventProtocol.md)
9. [Authentication、Authorization、CORS 与 Tenant Context](docs/09-Security与TenantContext.md)

### Part C｜外部系统与可靠请求生命周期

10. [DB、Redis、Vector DB 与 LLM Client 集成](docs/10-ExternalResourceIntegration.md)
11. [BackgroundTasks、文件上传与 Long-running Task Boundary](docs/11-BackgroundTask与Upload.md)
12. [Timeout、Cancellation、Client Disconnect 与 Cleanup](docs/12-TimeoutCancellation与Disconnect.md)

### Part D｜Production FastAPI

13. [Testing：Dependency Override、Streaming、WebSocket 与错误路径](docs/13-Testing.md)
14. [Logging、Trace、Metrics 与性能诊断](docs/14-Observability与Performance.md)
15. [Deployment：Worker、Health Check 与 Graceful Shutdown](docs/15-Deployment与GracefulShutdown.md)
16. [AI Service Patterns：Chat、RAG、Ingestion 与 Agent Run API](docs/16-AIServicePatterns.md)

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **4 道 Primary Canonical、3 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- ASGI / Request Lifecycle
- Middleware vs Dependency
- FastAPI + SSE / Agent Streaming
- CRUD Framework 与 Production Agent Service 的边界

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- asyncio 的语言 Runtime 语义归 Python；FastAPI 只解释框架怎样承接它。
- 通用 Retry / Idempotency / MQ / Backpressure 归 AI Backend Engineering。
- Agent Loop / State / Tool Runtime 归 Agent Harness。

遇到跨模块问题时，正文会保留必要桥梁，但完整机制只在 Primary Module 维护一份。

---

## 8. Review、Interview 与证据入口

| 入口 | 链接 | 用途 |
|---|---|---|
| Review | [总图与综合自测](review/README.md) | 第二遍复习：从空白纸重建主线 |
| 高频面试题 | [进入](interview/高频面试题.md) | 用真实问法训练口述与追问 |
| 面试易错点 | [进入](interview/面试易错点.md) | 校正绝对化、过时或边界错误表达 |
| 面试前速查 | [进入](interview/面试前速查表.md) | 面试前快速回忆 |

研究与质量证据：

- [Canonical Questions](../../interview/canonical/fastapi.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../../market/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../../market/analysis/frequency-ranking.md)：复习热度参考；
- [权威技术 / 源码资料索引](../../references/fastapi/README.md)：只校准技术事实，不改变 HUMAN-A 频率；
- [Curriculum Granularity Audit](../../guide/audits/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../../guide/audits/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../../guide/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 16` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–16 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

下一环：[AI Backend Engineering](../03-backend-engineering/README.md)。
