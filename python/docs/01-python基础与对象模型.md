# 01. Python 基础、对象模型与语言选择

Python Foundation 的第一章不应该从语法表开始，而应该先回答两个问题：

1. **Python 里的变量、对象、类型到底是什么关系？**
2. **为什么 AI Application / Agent 工程经常选择 Python，它又不是所有场景的唯一答案？**

这样后面的可变性、函数参数、GIL、asyncio 才有统一的底层心智模型。

---

## 1. 变量更像“名字绑定”，不是固定盒子

```python
a = 10
b = a
```

可以理解为：名字 `a` 绑定到整数对象 `10`，随后 `b` 也绑定到同一个对象。

```python
a = [1, 2]
b = a
b.append(3)
print(a)  # [1, 2, 3]
```

这里不是 `b` 把值“传回”给 `a`，而是两个名字引用同一个列表对象。

这也是后面理解：

- 可变 / 不可变；
- 参数传递；
- 浅拷贝 / 深拷贝；
- 闭包；
- 共享状态；

的基础。

---

## 2. 对象可以从 Identity / Type / Value 三个角度理解

| 角度 | 含义 | 常见方式 |
|---|---|---|
| Identity | 是否为同一个对象 | `is`、`id()` |
| Type | 对象属于什么类型 | `type()`、`isinstance()` |
| Value | 对象表示的值 | 常用 `==` 比较 |

```python
a = [1, 2]
b = [1, 2]

print(a == b)  # True
print(a is b)  # False
```

⚠️ `is` 比较的是**对象身份**，不要机械说成“比较内存地址”。

---

## 3. Python 是动态类型、强类型

```python
x = 10
x = "hello"
x = [1, 2]
```

同一个名字可以在运行时绑定不同类型对象，因此是动态类型。

但：

```python
"1" + 1
```

不会偷偷把整数转成字符串，而是抛 `TypeError`，所以 Python 通常被描述为强类型语言。

🎯 面试回答：

> Python 是动态类型、强类型语言。类型属于对象，变量名不需要提前声明固定类型；但不兼容类型之间不会随意发生隐式转换。

---

## 4. `type()` 和 `isinstance()`

```python
print(type(1))
print(isinstance(True, int))
```

真实代码中判断对象“是否属于某类或其子类体系”时，`isinstance()` 通常更合适，因为它考虑继承关系。

`type(x) is SomeClass` 更强调“必须恰好就是这个具体类型”。

---

## 5. Truthy / Falsy

常见假值：

- `False`
- `None`
- `0` / `0.0`
- `""`
- `[]` / `()` / `{}` / `set()`

```python
items = []
if not items:
    print("empty")
```

这比 `len(items) == 0` 更符合 Python 常见表达。

---

## 6. `None` 推荐用 `is`

```python
if value is None:
    ...
```

因为这里关心的是那个唯一的 `None` 对象本身，而不是一般意义的值相等。

---

## 7. Python 为什么在 AI Application / Agent 工程里常见

这不是“Python 语法最简单”一句话能解释的。

更完整的原因包括：

```text
成熟 AI / ML / Data 生态
+ LLM / RAG / Agent SDK 密集
+ 快速实验与迭代
+ 动态语言适合胶水层集成
+ asyncio / Web Framework 足以承担大量 I/O 型 AI 服务
+ 数据处理工具丰富
```

例如很多工作都属于：

```text
HTTP
DB
Redis
Vector DB
LLM Provider
Tool API
```

它们大量时间在等待 I/O，Python 的开发效率和生态往往很有优势。

---

## 8. Python 不是所有服务的唯一最优解

语言选择应该看约束，而不是信仰。

### Java 常见优势

- 大型企业后端生态成熟；
- 强类型与大型工程工具链完善；
- JVM 生态、服务治理和已有组织资产丰富；
- 团队已有大量 Java 基础设施时迁移成本低。

### Go 常见优势

- 静态编译、部署简单；
- goroutine / channel 适合高并发服务；
- 运行时开销和单二进制交付有优势；
- 很适合基础设施、Gateway、网络服务。

### Python 常见优势

- AI 生态最强；
- 模型 / 数据 / Notebook / 推理工具联动方便；
- 迭代速度快；
- 适合 AI orchestration 和大量 I/O 服务。

所以真正的工程判断是：

```text
业务瓶颈在哪里？
团队已有栈是什么？
是否大量依赖 Python-only AI 生态？
吞吐 / 延迟 / 内存要求多严？
部署和运维体系是什么？
```

---

## 9. AI 项目里常见的语言组合，而不是“只能选一个”

现实项目完全可能：

```text
Python
→ RAG / Agent / Model-facing service

Go
→ Gateway / high-concurrency infra

Java
→ existing business service / transaction domain
```

服务间通过 HTTP / RPC / MQ 协作。

这比争论“Python vs Java 谁更高级”更符合生产系统。

---

## 10. Python 的 Trade-off

Python 的优势同时也带来代价：

### 动态类型

迭代灵活，但大型项目更依赖：

- Type Hint；
- Static Checker；
- Schema Validation；
- Test。

### 运行时性能

纯 Python CPU-heavy 场景可能不如编译型语言，需要：

- native library；
- process pool；
- 服务拆分。

### GIL / 并发边界

传统 CPython 的纯 Python CPU-bound 多线程并行受限，因此不能把“Python 会 async”理解成“所有负载都适合一个进程解决”。

这些后面会逐章展开。

---

## 11. 索引、切片与解包先建立直觉

```python
nums = [10, 20, 30, 40, 50]
print(nums[0])
print(nums[-1])
print(nums[1:4])
print(nums[::-1])
```

切片格式：

```text
sequence[start:stop:step]
```

这里先学语义；**切片的时间 / 空间和复制成本**会放到下一章容器里讲，因为它与 list / tuple / str 的数据结构更直接相关。

解包：

```python
a, b = 1, 2
first, *middle, last = [1, 2, 3, 4]
```

---

## 12. 🎯 面试怎么回答：为什么 AI 工程常用 Python

> 我不会只回答“Python 简单”。AI Application 里大量工作是在连接模型、RAG、数据系统和外部 API，Python 在 AI/ML/Data 生态、SDK 覆盖和快速迭代上优势明显，同时 asyncio 足以支撑大量 I/O 型服务。但语言选型仍要看现有团队栈、性能瓶颈、部署方式和基础设施要求；高吞吐 Gateway、强交易后端或已有大型 Java/Go 体系不一定需要强行改成 Python。

---

## 13. ⚠️ 易错点

- Python 动态类型 ≠ 没有类型；
- `is` ≠ 一般值比较；
- `id()` 的实现细节不要上升成语言规范；
- “Python 适合 AI”不能只回答“语法简单”；
- Python / Java / Go 不是非此即彼，真实系统可以多语言协作；
- 语言选择要由 workload、生态和团队约束决定。

---

## 14. 本章自测

<details>
<summary>1. `a = b` 是否复制了对象？</summary>

通常没有，它只是让两个名字绑定到同一个对象。是否产生新对象要看具体表达式和操作。

</details>

<details>
<summary>2. 为什么 Python 在 AI Application 中常见，但不能推出所有 AI 后端都应该用 Python？</summary>

Python 的 AI 生态和迭代效率很强，但语言选型仍受吞吐、延迟、团队栈、已有基础设施、部署方式和 CPU-heavy 比例影响；不同服务完全可以采用不同语言。

</details>

<details>
<summary>3. Python 为什么既是动态类型又是强类型？</summary>

动态类型表示名字不需要预先声明固定类型；强类型表示不兼容对象不会被任意隐式转换，例如字符串与整数不能直接相加。

</details>

下一章：[02. 核心数据类型与容器](02-核心数据类型与容器.md)
