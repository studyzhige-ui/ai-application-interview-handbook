# Python Foundation｜Python 语言与运行时基础

[↑ Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md) · [FastAPI →](../fastapi/README.md)

> **状态：✅ 第一版系统教材完成**  
> **教材：13 个连续知识小板块** · **HUMAN-A Canonical：15** · **独立来源覆盖：15**  
> **质量：Granularity / Coverage / Content Depth 已验收**

建立 AI Application / Agent Engineer 所需的 Python 语言、对象模型、结构化数据与并发 Runtime 基础。

---

## 1. 这个模块解决什么

建立 AI Application / Agent Engineer 所需的 Python 语言、对象模型、结构化数据与并发 Runtime 基础。

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

**Python Foundation** → [FastAPI](../fastapi/README.md) → [AI Backend Engineering](../backend-engineering/README.md) → [MySQL](../mysql/README.md) → [Redis](../redis/README.md) → [Vector Database](../vector-db/README.md) → [LLM Foundation（应用工程深度）](../llm-foundation/README.md) → [RAG](../rag/README.md) → [Agent](../agent/README.md) → [System Design](../system-design/README.md)

当前模块角色：**Foundation / 建立 AI Application / Agent Engineer 所需的 Python 语言、对象模型、结构化数据与并发 Runtime 基础。**

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

所以本模块是 **15 道 Canonical → 13 个教材知识块**，两者不需要一一对应。

---

## 4. 正式学习主线

```text
Object Model / Containers → Function / Scope → Iterator / Context Manager → OOP / Protocol → Structured Data → Memory / GIL → Thread / Process / asyncio → Data Structure
```

这个顺序按知识依赖组织，而不是按面经频率排序。

---

## 5. 正式课程目录

### Part A｜对象、容器与函数

1. [Python 基础与对象模型](docs/01-python基础与对象模型.md)
2. [核心数据类型与容器](docs/02-核心数据类型与容器.md)
3. [可变对象、对象身份与深浅拷贝](docs/03-可变对象-对象身份-深浅拷贝.md)
4. [函数、参数、作用域与闭包](docs/04-函数-参数-作用域-闭包.md)
5. [Lambda、推导式与常用内置函数](docs/05-lambda-推导式-常用内置函数.md)

### Part B｜Python 工程抽象

6. [迭代器、生成器与 yield](docs/06-迭代器-生成器-yield.md)
7. [装饰器与上下文管理器](docs/07-装饰器-上下文管理器.md)
8. [面向对象与魔术方法](docs/08-面向对象-魔术方法.md)
9. [异常、文件、模块与导入](docs/09-异常-文件-模块与导入.md)
10. [结构化数据、JSON 与校验](docs/10-结构化数据-JSON与校验.md)

### Part C｜Runtime、并发与复杂度

11. [内存管理、垃圾回收与 GIL](docs/11-内存管理-垃圾回收-GIL.md)
12. [线程、进程、协程与 async/await](docs/12-线程-进程-协程-async-await.md)
13. [常见数据结构与复杂度](docs/13-常见数据结构与复杂度.md)

---

## 6. 真人面经怎样影响本模块

冻结基线 `S001–S279` 中，本模块有 **15 道 Primary Canonical、15 个独立 HUMAN-A 招聘流程覆盖**。

重点市场信号包括：

- dict / Hash / Slicing 成本
- GIL 与 Thread / Process
- asyncio / Timeout / Cancellation
- Lock / RLock / Semaphore
- Structured Output / JSON Validation

这些信号决定**哪里必须讲得更深、真实面试会怎么问、Failure / Scale / Evaluation 会追到哪一层**；它们不负责决定章节先后，也不会删除低频但必要的前置知识。

---

## 7. 模块边界

- Python 负责语言与 Runtime 语义；HTTP / ASGI Service 进入 FastAPI。
- Timeout / Retry / MQ / Backpressure 等跨服务机制进入 AI Backend Engineering。
- Agent Loop / Tool / Memory / Checkpoint 进入 Agent Harness / Runtime。

遇到跨模块问题时，正文会保留必要桥梁，但完整机制只在 Primary Module 维护一份。

---

## 8. Review、Interview 与证据入口

| 入口 | 链接 | 用途 |
|---|---|---|
| Review | [总图与综合自测](review/README.md) | 第二遍复习：从空白纸重建主线 |
| 高频面试题 | [进入](interview/高频面试题.md) | 用真实问法训练口述与追问 |
| 面试易错点 | [进入](interview/面试易错点.md) | 校正绝对化、过时或边界错误表达 |
| 面试前速查 | [进入](interview/面试前速查表.md) | 面试前快速回忆 |
| Python 高频 Coding 小题 | [进入](interview/Python高频Coding小题.md) | 额外专项训练 |

研究与质量证据：

- [Canonical Questions](../research/questions/python.md)：市场真实问法与 Source Count；
- [Verified Follow-up Chains](../research/analysis/follow-up-chains.md)：回到原始 HUMAN-A 核验的真实递进；
- [Frequency Ranking](../research/analysis/frequency-ranking.md)：复习热度参考；
- [Curriculum Granularity Audit](../roadmap/curriculum-granularity-audit.md)：为什么教材文件数不等于 Canonical 数；
- [Content Depth Audit](../roadmap/content-depth-audit.md)：完成与深度验收口径。

---

## 9. 推荐学习方式

> 可选：如需整体学习节奏与复习方法，可参考 [Learning Path](../roadmap/learning-path.md)；也可以按自身基础调整进度，首次学习建议保持本模块章节顺序。

1. **第一遍：建立因果链。** 按 `docs/01 → 13` 连续阅读，不按高频题跳章。
2. **第二遍：重画主线。** 进入 [Review](review/README.md)，不看正文先自己解释正常路径、Failure 与 Trade-off。
3. **第三遍：面试化。** 用高频题、易错点和速查表训练 30 秒回答与深挖回答。
4. **项目复盘：** 把自己的真实项目映射到本模块主线，说明为什么这样设计、哪里会坏、怎样验证。

---

## 10. 完成状态

```text
docs/      ✅ 01–13 连续
review/    ✅
interview/ ✅
Canonical Coverage ✅
Content Depth       ✅
```

下一环：[FastAPI](../fastapi/README.md)。
