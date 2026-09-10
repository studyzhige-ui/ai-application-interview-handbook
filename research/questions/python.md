# Python Canonical Questions — S001–S279 全库纵向扫描 v2

更新日期：2026-09-10

> 一级板块：**Python**。本文件只记录冻结 HUMAN-A 中真实出现的 Python 语言与 Python Runtime 问题。通用 Network / MQ / Distributed System 归 `AI Backend Engineering`；FastAPI / ASGI 框架行为归 `FastAPI`。
>
> 本文件所有条目的 `Primary Module = Python`。FastAPI 语境下出现的 `await` / Event Loop / CPU / Thread 语义已统一并入 `PY-012`，避免重复建题。

## 1. 当前扫描结论

- ACTIVE Canonical Questions：**15**
- 证据范围：仅 `S001–S279`
- 频率口径：独立 HUMAN-A 来源数
- 当前版本：`v2`（十板块归属审计版）

当前信号很明确：Python 在这批面经里的“纯语言八股”频率远低于 Agent / RAG / Backend，但一旦团队明确使用 Python，会直接追到参数绑定、Duck Typing、Iterator / Generator、GIL、`asyncio` 和运行时语义，而不只是“会不会写脚本”。

---

## 2. Canonical Questions

### PY-001 · 为什么 AI Application / Agent 工程常使用 Python？与 Java / Go 相比，语言选择应依据什么？

- **Primary Module**：Python
- **Related Modules**：AI Backend Engineering, Agent Harness / Runtime
- **Topic**：Language Choice
- **Question Type**：Comparison / Trade-off
- **Language / Ecosystem**：Python / Java / Go
- **Depth**：L3
- **Interview Heat**：🔥🔥
- **Source Count**：**4**
- **Evidence Sources**：`S026`, `S047`, `S176`, `S238`

**真实问法变体：**
- Java 与 Python 做 Agent 开发各有什么优势？
- 为什么很多 Agent 工程使用 Python？
- Go / Java / Python 分别在哪些真实项目里使用过？
- 如果面试官认为 Python 理解不深，怎样证明 Python 能力？

### PY-002 · Python `list` 与 `tuple` 的语义、可变性、典型使用场景和成本有什么差异？

- **Primary Module**：Python
- **Topic**：Built-in Containers
- **Question Type**：Concept / Comparison
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S054`

**真实问法变体：**
- Python list / tuple 有什么区别？
- 哪些数据结构可变，哪些不可变？

### PY-003 · Python `dict` 的 Hash、冲突处理、删除与底层表结构怎样工作？

- **Primary Module**：Python
- **Topic**：dict / Hash Table
- **Question Type**：Concept / Deep Dive
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S035`

**真实问法变体：**
- Python dict 的 Hash 怎么做？
- 冲突怎样处理，删除元素后底层会发生什么？

### PY-004 · Python Function Parameters 有哪些形式？位置参数、关键字参数、默认参数、`*args` / `**kwargs` 的绑定规则是什么？

- **Primary Module**：Python
- **Topic**：Function Parameters
- **Question Type**：Concept / Coding
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S226`

### PY-005 · Duck Typing 如何理解？它给接口设计、可替换性和错误暴露带来什么收益与风险？

- **Primary Module**：Python
- **Topic**：Dynamic Typing / Protocol Thinking
- **Question Type**：Concept / Why
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S226`

### PY-006 · Iterator 与 Generator 有什么区别？Generator 为什么能保存执行状态并按需产出数据？

- **Primary Module**：Python
- **Related Modules**：AI Backend Engineering
- **Topic**：Iterator / Generator
- **Question Type**：Concept / Deep Dive
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S032`, `S226`

### PY-007 · Python Decorator 怎样工作？如何用它实现 Logging、Tracing 或横切逻辑？

- **Primary Module**：Python
- **Related Modules**：AI Backend Engineering
- **Topic**：Decorator
- **Question Type**：Concept / Coding
- **Language / Ecosystem**：Python
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S032`, `S054`, `S120`

**真实问法变体：**
- Python 装饰器是什么？
- 手写一个 Logging Decorator。
- 装饰器怎样用于 Runtime 横切逻辑？

### PY-008 · Python Context Manager 的协议与资源生命周期怎样理解？什么时候应使用 `with` 管理资源？

- **Primary Module**：Python
- **Topic**：Context Manager
- **Question Type**：Concept / Why
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S032`

### PY-009 · Python Slicing 的语义是什么？切片在时间、空间与对象复制上有什么成本？

- **Primary Module**：Python
- **Topic**：Slicing
- **Question Type**：Concept / Coding
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S226`

### PY-010 · Python GIL 是什么？它怎样影响 CPU-bound 与 I/O-bound 并发设计？

- **Primary Module**：Python
- **Related Modules**：AI Backend Engineering
- **Topic**：GIL
- **Question Type**：Concept / Why / Trade-off
- **Language / Ecosystem**：Python
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S008`, `S251`

### PY-011 · `threading` 与 `multiprocessing` 应怎样选择？大量 PDF / CPU 密集与 I/O 密集任务分别适合什么并发模型？

- **Primary Module**：Python
- **Related Modules**：AI Backend Engineering
- **Topic**：Threading / Multiprocessing
- **Question Type**：Comparison / Trade-off
- **Language / Ecosystem**：Python
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**2**
- **Evidence Sources**：`S064`, `S184`

### PY-012 · `asyncio` Event Loop 怎样工作？`gather`、`as_completed`、`await` 与 Timeout / Fallback 怎样组合高并发 I/O？

- **Primary Module**：Python
- **Related Modules**：FastAPI, AI Backend Engineering
- **Topic**：asyncio
- **Question Type**：Concept / Comparison / Troubleshoot
- **Language / Ecosystem**：Python
- **Depth**：L3
- **Interview Heat**：🔥
- **Source Count**：**3**
- **Evidence Sources**：`S064`, `S184`, `S241`

**真实问法变体：**
- `asyncio.gather` 与 `as_completed` 有什么差异？
- FastAPI 异步调用 LLM 时，`await` 等待期间 CPU / Event Loop / Thread 在做什么？
- Timeout / Fallback 怎样与异步调用结合？

### PY-013 · `Lock`、`RLock`、`Semaphore` 分别解决什么并发问题，什么时候使用？

- **Primary Module**：Python
- **Related Modules**：AI Backend Engineering
- **Topic**：Synchronization Primitives
- **Question Type**：Concept / Comparison
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S008`

### PY-014 · Python 中怎样解析、校验并约束 LLM 产生的 JSON / Structured Output？

- **Primary Module**：Python
- **Related Modules**：FastAPI, Agent Harness / Runtime
- **Topic**：Structured Data Validation
- **Question Type**：Coding / Reliability
- **Language / Ecosystem**：Python
- **Depth**：L3
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S238`

### PY-015 · Python Closure 是什么？闭包在真实项目中适合什么场景？

- **Primary Module**：Python
- **Topic**：Closure
- **Question Type**：Concept / Project
- **Language / Ecosystem**：Python
- **Depth**：L2
- **Interview Heat**：单点真实信号
- **Source Count**：**1**
- **Evidence Sources**：`S210`

---

## 3. 十板块归属审计结论

Python 侧没有需要迁出的 ACTIVE Canonical。唯一明确的跨模块重复来自旧 `FASTAPI-003`，其核心是 Python `asyncio` Runtime，已迁入 `PY-012`。

通用 ThreadPool、Network、MQ、Service Deployment 等问题不因实现语言是 Python 而进入本模块；它们继续由 `AI Backend Engineering` 维护。

---

## 4. 对课程结构的直接信号

这批真人面经不支持把 Python 教材写成“面试八股大全”。高频仍然发生在 AI Backend / RAG / Agent；Python 更像底层语言前置。课程应完整覆盖语言基础，但复习加权应优先放在：

1. Generator / Iterator / Decorator 这类真实工程抽象；
2. GIL + `threading` / `multiprocessing`；
3. `asyncio` 与后续 FastAPI Async Service 的衔接；
4. JSON / Structured Data Validation 与 LLM Service 的工程连接。
