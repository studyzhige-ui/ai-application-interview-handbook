# Python Foundation｜秋招面试知识手册

> **Status：🟠 v1 完整可用，但当前统一标准的二次整改尚未完成。** 现有 `12` 章正文 + Review + Interview 可以正常学习；后续不推倒重写，而是在 FastAPI / AI Backend Engineering 补齐后，对照最新 `15` 道 Python Canonical 做 Coverage / Depth Remediation。详见 [`../roadmap/foundation-status-audit.md`](../roadmap/foundation-status-audit.md)。

> 本模块由原独立仓库 `python-interview-handbook` 迁入，现作为 **AI Application Interview Handbook** 的 Python 基础层继续维护。
>
> 目标不是只会 Python 语法，而是建立后续 FastAPI、异步服务、RAG 与 Agent Runtime 所需要的语言与运行时基础。

## 为什么 Python 是整套 AI 应用求职体系的第一环

真实 AI 应用 / Agent 面试里，Python 不一定总以“list 和 tuple 区别”这种传统八股出现，但经常会换成更工程化的追问：

- `dict` / 哈希表与常用数据结构；
- GIL、线程、进程、协程；
- `async` / `await` 与事件循环；
- 生成器、上下文管理器；
- 大文件流式处理；
- FastAPI / Pydantic / SSE；
- CPU-bound 与 I/O-bound 的隔离；
- Agent Runtime 中的异步 Tool 调用和资源管理。

因此这里仍然从 0 建立完整 Python 知识体系，但会把与 AI Backend / Agent 工程关系最密切的章节提高复习优先级。

## 这份手册适合谁

- 学过几遍 Python 基础，但知识不够系统、容易遗忘；
- 需要为秋招/实习面试快速建立完整 Python 知识框架；
- 不希望只背“八股”，而是希望能理解概念、看懂例子、回答追问；
- 后续希望继续学习 FastAPI、RAG、Agent Harness 等 AI 应用开发能力。

## 推荐使用方式

1. **第一遍：建立框架。** 按 `docs/` 顺序通读，不要求一次记住所有细节。
2. **第二遍：重点理解。** 对可变/不可变、深浅拷贝、作用域、迭代器、生成器、装饰器、OOP、GIL/并发等高频点动手跑代码。
3. **每章读完：图解 + 自测。** 进入 [`review/`](review/README.md)，先看图，再自己口述；参考答案默认折叠。
4. **第三遍：面试化表达。** 使用 [`interview/高频面试题.md`](interview/高频面试题.md)，先说答案再核对。
5. **面试前：快速复习。** 使用 [`interview/面试前速查表.md`](interview/面试前速查表.md)。
6. **学完 Python 主体后：进入 [`FastAPI`](../fastapi/README.md)**，把语言能力真正落到 AI 后端服务。

## AI 应用岗复习优先级

| 知识区域 | AI 应用 / Agent 面试建议 |
|---|---:|
| `dict` / set / 哈希 | ⭐⭐⭐⭐⭐ |
| 可变对象、引用、参数传递 | ⭐⭐⭐⭐ |
| 生成器 / `yield` | ⭐⭐⭐⭐ |
| 装饰器 / 上下文管理器 | ⭐⭐⭐⭐ |
| 异常与资源清理 | ⭐⭐⭐⭐ |
| GIL | ⭐⭐⭐⭐⭐ |
| 线程 / 进程 / 协程 | ⭐⭐⭐⭐⭐ |
| `async` / `await` / Event Loop | ⭐⭐⭐⭐⭐ |
| 数据结构 / Top K | ⭐⭐⭐⭐ |
| OOP / 魔术方法 | ⭐⭐⭐⭐ |
| Lambda / Pythonic 工具 | ⭐⭐⭐ |

> 这张表只是**复习权重**，不是删除低频章节。完整知识体系仍然保留。

## 内容结构

| 模块 | 内容 |
|---|---|
| Python 基础 | 对象、变量、类型、运算、真值判断 |
| 核心容器 | list / tuple / set / dict / str |
| 对象与拷贝 | 可变不可变、`==`/`is`、浅拷贝深拷贝 |
| 函数 | 参数、`*args`/`**kwargs`、作用域、闭包、lambda |
| Pythonic 写法 | 推导式、`enumerate`、`zip`、`sorted`、`map/filter` |
| 迭代体系 | Iterable / Iterator / Generator / `yield` |
| 装饰器与上下文 | decorator、`with`、context manager |
| OOP | 类与对象、继承、多态、方法、魔术方法 |
| 稳健代码 | 异常、文件、模块与导入 |
| 运行机制 | 内存、垃圾回收、GIL |
| 并发 | 线程、进程、协程、`async`/`await` |
| 数据结构 | 数组、链表、栈、队列、哈希、树、堆、Top K |

## 文档导航

### 基础与核心语法

- [01. Python 基础与对象模型](docs/01-python基础与对象模型.md)
- [02. 核心数据类型与容器](docs/02-核心数据类型与容器.md)
- [03. 可变对象、对象身份与深浅拷贝](docs/03-可变对象-对象身份-深浅拷贝.md)
- [04. 函数、参数、作用域与闭包](docs/04-函数-参数-作用域-闭包.md)
- [05. Lambda、推导式与常用内置函数](docs/05-lambda-推导式-常用内置函数.md)

### Python 进阶核心

- [06. 迭代器、生成器与 yield](docs/06-迭代器-生成器-yield.md)
- [07. 装饰器与上下文管理器](docs/07-装饰器-上下文管理器.md)
- [08. 面向对象与魔术方法](docs/08-面向对象-魔术方法.md)
- [09. 异常、文件、模块与导入](docs/09-异常-文件-模块与导入.md)
- [10. 内存管理、垃圾回收与 GIL](docs/10-内存管理-垃圾回收-GIL.md)
- [11. 线程、进程、协程与 async/await](docs/11-线程-进程-协程-async-await.md)
- [12. 常见数据结构与复杂度](docs/12-常见数据结构与复杂度.md)

### 图解与章节自测

- [12 章图解复习与自测总入口](review/README.md)

每章配有 Mermaid 图解和 GitHub `<details>` 折叠答案。建议先完整回答，再展开参考答案。

### 面试专项

- [Python 高频面试题](interview/高频面试题.md)
- [Python 高频 Coding 小题](interview/Python高频Coding小题.md)
- [面试易错点](interview/面试易错点.md)
- [面试前速查表](interview/面试前速查表.md)

## 每个知识点的写法

> **先讲人话 → 准确定义 → 代码示例 → 对比表格 → 为什么 → 图解串联 → 面试怎么答 → 常见追问 → 章节自测**

文档中的标记：

- 💡 **新手理解**：先用直观语言建立感觉；
- 🧠 **为什么**：补充底层逻辑；
- ⚠️ **易错点**：面试中容易说错或写错的地方；
- 🎯 **面试怎么答**：适合口述的答案框架；
- 🔍 **追问**：面试官可能继续深入的问题。

## Python 与后续模块如何衔接

```text
Python 对象 / 容器
        ↓
函数 / 装饰器 / 上下文管理器
        ↓
GIL / 线程 / 进程 / asyncio
        ↓
FastAPI / Pydantic / ASGI
        ↓
数据库 / Redis / 外部 HTTP / Streaming
        ↓
RAG Service / Agent Runtime
```

例如：

- `yield` → Streaming / SSE / 流式 LLM 输出；
- 上下文管理器 → 数据库 Session、连接、锁、资源清理；
- 装饰器 → 路由、鉴权、Trace 等框架机制的理解基础；
- asyncio → FastAPI 高并发 I/O、并行 Tool 调用；
- GIL / 进程池 → Agent 中 CPU 密集型解析、Embedding 前处理、文件处理的隔离。

## 关于版本

本模块以现代 **Python 3** 为基础。涉及具体实现细节（尤其 CPython、GIL、内存管理）时会明确区分语言语义与 CPython 实现。

## 下一环：FastAPI

Python 学完后，不再停留在“会写脚本”。下一步进入：

> [FastAPI｜AI 应用服务层](../fastapi/README.md)

目标是把 `asyncio`、类型系统、资源生命周期和 HTTP 服务真正串成可部署的 AI Backend。
