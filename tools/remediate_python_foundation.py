from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / "python"


def append_before(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if block.strip().splitlines()[0] in text:
        return
    if marker not in text:
        raise SystemExit(f"missing marker in {path}: {marker}")
    path.write_text(text.replace(marker, block.rstrip() + "\n\n" + marker, 1), encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"missing replacement anchor in {path}: {old[:100]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# ------------------------------------------------------------------
# 1. Add in-chapter folded self-tests to legacy chapters 03-07.
# ------------------------------------------------------------------
self_tests = {
    "03-可变对象-对象身份-深浅拷贝.md": """## 9. 本章自测

<details>
<summary>1. 为什么 `a = b`、浅拷贝、深拷贝不能混为一谈？</summary>

`a = b` 只增加一个名字绑定，不创建副本；浅拷贝创建新的外层对象，但嵌套对象仍可能共享；深拷贝递归复制需要复制的内部对象，隔离更强但成本也更高。

</details>

<details>
<summary>2. 函数收到 list 后执行 `lst.append()` 与执行 `lst = []` 为什么对调用方影响不同？</summary>

前者修改形参与实参共同引用的列表对象，外部可见；后者只是让函数局部名字重新绑定到新列表，不改变调用方变量的绑定。

</details>

<details>
<summary>3. 为什么可变默认参数容易产生跨调用状态污染？</summary>

默认参数对象在函数定义时创建一次，后续调用会复用同一个对象，因此对 list/dict 等默认值的原地修改会被后续调用看到。

</details>""",
    "04-函数-参数-作用域-闭包.md": """## 14. 本章自测

<details>
<summary>1. `def f(a, /, b, *, c)` 中三个参数分别允许怎样传递？</summary>

`a` 只能按位置传；`b` 可以按位置或关键字传；`c` 只能按关键字传。

</details>

<details>
<summary>2. 为什么循环里创建的多个 lambda 可能最后都读到同一个 `i`？</summary>

闭包通常在实际调用时读取自由变量，循环结束后 `i` 已是最终值；可以用默认参数等方式在定义时捕获当前值。

</details>

<details>
<summary>3. `global` 与 `nonlocal` 的作用域目标有什么区别？</summary>

`global` 指模块级名字；`nonlocal` 指最近的外层函数作用域名字，不会直接指向模块全局。

</details>""",
    "05-lambda-推导式-常用内置函数.md": """## 本章自测

<details>
<summary>1. 为什么复杂业务逻辑不应该为了“Pythonic”强塞进一条列表推导式？</summary>

可读性和可调试性比行数更重要。包含多层条件、副作用或复杂异常处理时，普通循环通常更清晰。

</details>

<details>
<summary>2. `sorted()` 与 `list.sort()` 的核心区别是什么？</summary>

`sorted()` 接收任意可迭代对象并返回新 list；`list.sort()` 只作用于 list，原地排序并返回 `None`。

</details>""",
    "06-迭代器-生成器-yield.md": """## 本章自测

<details>
<summary>1. Iterable 与 Iterator 的区别是什么？</summary>

Iterable 能通过 `iter()` 获得迭代器；Iterator 保存当前迭代状态并实现 `next()` 语义。list 是 Iterable，但不是它自己的 Iterator。

</details>

<details>
<summary>2. Generator 为什么适合流式处理大数据？</summary>

生成器按需产出元素并保存执行状态，不必一次把所有结果保存在内存中，因此适合大文件、批处理和 Streaming 场景。

</details>""",
    "07-装饰器-上下文管理器.md": """## 本章自测

<details>
<summary>1. 为什么装饰器常使用 `functools.wraps`？</summary>

它帮助保留被包装函数的名称、文档等元信息，对调试、反射、框架路由和 Trace 都更友好。

</details>

<details>
<summary>2. Context Manager 的核心价值是什么？</summary>

把资源的获取与释放绑定到结构化生命周期，即使代码块中抛异常，也能执行退出清理。文件、锁、数据库连接和 Trace Context 都常用这种模式。

</details>""",
}

for name, block in self_tests.items():
    path = PY / "docs" / name
    append_before(path, "下一章:", block)

# ------------------------------------------------------------------
# 2. Review 10-12 -> 11-13, add new review 10.
# ------------------------------------------------------------------
review = PY / "review"
renames = [
    ("12-常见数据结构与复杂度-图解与自测.md", "13-常见数据结构与复杂度-图解与自测.md", "# 12.", "# 13.", "../docs/12-常见数据结构与复杂度.md", "../docs/13-常见数据结构与复杂度.md"),
    ("11-线程-进程-协程-async-await-图解与自测.md", "12-线程-进程-协程-async-await-图解与自测.md", "# 11.", "# 12.", "../docs/11-线程-进程-协程-async-await.md", "../docs/12-线程-进程-协程-async-await.md"),
    ("10-内存管理-垃圾回收-GIL-图解与自测.md", "11-内存管理-垃圾回收-GIL-图解与自测.md", "# 10.", "# 11.", "../docs/10-内存管理-垃圾回收-GIL.md", "../docs/11-内存管理-垃圾回收-GIL.md"),
]
for old, new, old_h, new_h, old_link, new_link in renames:
    oldp, newp = review / old, review / new
    if oldp.exists() and not newp.exists():
        oldp.rename(newp)
    if not newp.exists():
        raise SystemExit(f"review rename missing: {newp}")
    text = newp.read_text(encoding="utf-8")
    text = text.replace(old_h, new_h, 1).replace(old_link, new_link)
    newp.write_text(text, encoding="utf-8")

review10 = review / "10-结构化数据-JSON与校验-图解与自测.md"
if not review10.exists():
    review10.write_text(r'''# 10. 结构化数据、JSON 与校验：图解与自测

对应正文：[10. 结构化数据、JSON 与校验](../docs/10-结构化数据-JSON与校验.md)

## 图解 1：从不可信文本到可信对象

```mermaid
flowchart LR
    A["LLM / External Input"] --> B["Parse JSON"]
    B --> C["Schema Validation"]
    C --> D["Business Validation"]
    D --> E["Permission / Approval"]
    E --> F["Typed Object / Execute"]
```

## 图解 2：错误应该在哪一层处理

```mermaid
flowchart TD
    A["Output"] --> B{"合法 JSON？"}
    B -->|否| C["Parse Error"]
    B -->|是| D{"满足 Schema？"}
    D -->|否| E["Validation Error"]
    D -->|是| F{"满足业务/权限？"}
    F -->|否| G["Reject"]
    F -->|是| H["Accept / Execute"]
```

## 章节自测

<details><summary>1. `json.loads()` 成功为什么仍然不能直接执行 Tool？</summary>

因为它只验证 JSON 语法；字段类型、业务 invariant、权限和高风险动作仍需要独立校验。

</details>

<details><summary>2. `TypedDict` 与 Pydantic 最大的运行时差异是什么？</summary>

`TypedDict` 主要服务静态类型检查；Pydantic 等模型可以在运行时验证不可信输入并产生结构化错误。

</details>

<details><summary>3. Parse Error 与 Permission Error 为什么不能统一“让模型重试”？</summary>

Parse/Schema 问题可能通过有限 Repair 修复；Permission/Business Reject 是策略边界，不能允许模型通过反复重试绕过。

</details>
''', encoding="utf-8")

review_readme = review / "README.md"
text = review_readme.read_text(encoding="utf-8")
text = text.replace("`docs/` 的 12 个正文章节", "`docs/` 的 13 个正文章节")
old_rows = """| 09 异常、文件、模块与导入 | [进入](09-异常-文件-模块与导入-图解与自测.md) |
| 10 内存管理、垃圾回收与 GIL | [进入](10-内存管理-垃圾回收-GIL-图解与自测.md) |
| 11 线程、进程、协程与 async/await | [进入](11-线程-进程-协程-async-await-图解与自测.md) |
| 12 常见数据结构与复杂度 | [进入](12-常见数据结构与复杂度-图解与自测.md) |"""
new_rows = """| 09 异常、文件、模块与导入 | [进入](09-异常-文件-模块与导入-图解与自测.md) |
| 10 结构化数据、JSON 与校验 | [进入](10-结构化数据-JSON与校验-图解与自测.md) |
| 11 内存管理、垃圾回收与 GIL | [进入](11-内存管理-垃圾回收-GIL-图解与自测.md) |
| 12 线程、进程、协程与 async/await | [进入](12-线程-进程-协程-async-await-图解与自测.md) |
| 13 常见数据结构与复杂度 | [进入](13-常见数据结构与复杂度-图解与自测.md) |"""
if old_rows in text:
    text = text.replace(old_rows, new_rows, 1)
review_readme.write_text(text, encoding="utf-8")

# Extra review questions for newly deepened Canonical points.
extras = {
    "01-python基础与对象模型-图解与自测.md": """

### 新增追问：为什么 AI 工程常用 Python，但不能说所有 AI 服务都应该用 Python？

<details><summary>查看参考答案</summary>

Python 在 AI/ML/Data 生态和快速集成上很强，也适合大量 I/O 型 orchestration；但高吞吐基础设施、已有 Java/Go 体系、极端 CPU/内存约束等场景可能有更合适的语言。语言选择由 workload、生态与团队约束决定。

</details>
""",
    "02-核心数据类型与容器-图解与自测.md": """

### 新增追问：Hash Collision 会不会覆盖原来的 dict key？

<details><summary>查看参考答案</summary>

不会。Hash 只帮助定位候选位置；发生碰撞后哈希表会继续探测其它位置并用 equality 区分真正 key。

</details>

### 新增追问：`lst[a:b]` 的时间和空间通常怎样理解？

<details><summary>查看参考答案</summary>

对常见 Python 内建序列，切片通常创建新对象，切出 k 个元素大致需要 O(k) 时间和额外空间，而不是零拷贝 view。

</details>
""",
    "08-面向对象-魔术方法-图解与自测.md": """

### 新增追问：Duck Typing 与 `typing.Protocol` 是什么关系？

<details><summary>查看参考答案</summary>

Duck Typing 强调对象是否具备需要的行为；Protocol 把这种隐式结构要求写成可供静态类型工具检查的契约，让大型工程的可替换性更明确。

</details>
""",
    "12-线程-进程-协程-async-await-图解与自测.md": """

### 新增追问：`gather` 与 `as_completed` 怎么选？

<details><summary>查看参考答案</summary>

需要一组任务全部结果时 `gather` 很自然；希望谁先完成先处理、渐进聚合或早停时 `as_completed` 更合适。二者都不会自动做并发限流。

</details>

### 新增追问：Lock / RLock / Semaphore 的区别？

<details><summary>查看参考答案</summary>

Lock 保护互斥临界区；RLock 允许同一线程重入同一把锁；Semaphore 允许最多 N 个并发执行者，更适合容量控制。

</details>
""",
}
for name, extra in extras.items():
    p = review / name
    t = p.read_text(encoding="utf-8")
    marker = extra.strip().splitlines()[0]
    if marker not in t:
        p.write_text(t.rstrip() + extra + "\n", encoding="utf-8")

# ------------------------------------------------------------------
# 3. Update module README from 12 -> 13 and mark remediation complete.
# ------------------------------------------------------------------
readme = PY / "README.md"
t = readme.read_text(encoding="utf-8")
t = re.sub(
    r"> \*\*Status：🟠[^\n]*\n",
    "> **Status：✅ Current-standard remediation 已完成。** 当前为 `13` 个连续知识小板块 + Review + Interview；最新 `15` 道 Python Canonical 已完成 Coverage / Depth 映射，只有 Structured Data / JSON Validation 因形成独立认知闭环新增一章，其余面经信号均并回原有 0→1 主干。\n",
    t,
    count=1,
)
t = t.replace("| 稳健代码 | 异常、文件、模块与导入 |", "| 稳健代码 | 异常、文件、模块与导入 |\n| 结构化数据 | JSON、Schema、Runtime Validation、Structured Output |").replace(
    "| `async` / `await` / Event Loop | ⭐⭐⭐⭐⭐ |",
    "| `async` / `await` / Event Loop | ⭐⭐⭐⭐⭐ |\n| Structured Output / JSON Validation | ⭐⭐⭐⭐ |",
)
old_nav = """- [09. 异常、文件、模块与导入](docs/09-异常-文件-模块与导入.md)
- [10. 内存管理、垃圾回收与 GIL](docs/10-内存管理-垃圾回收-GIL.md)
- [11. 线程、进程、协程与 async/await](docs/11-线程-进程-协程-async-await.md)
- [12. 常见数据结构与复杂度](docs/12-常见数据结构与复杂度.md)"""
new_nav = """- [09. 异常、文件、模块与导入](docs/09-异常-文件-模块与导入.md)
- [10. 结构化数据、JSON 与校验](docs/10-结构化数据-JSON与校验.md)
- [11. 内存管理、垃圾回收与 GIL](docs/11-内存管理-垃圾回收-GIL.md)
- [12. 线程、进程、协程与 async/await](docs/12-线程-进程-协程-async-await.md)
- [13. 常见数据结构与复杂度](docs/13-常见数据结构与复杂度.md)"""
if old_nav in t:
    t = t.replace(old_nav, new_nav, 1)
t = t.replace("[12 章图解复习与自测总入口]", "[13 章图解复习与自测总入口]")
coverage = """
## 2026 Canonical Coverage / Remediation 结果

最新 15 道 Python Canonical 没有被机械转换成 15 个文件，而是映射到 13 个知识块：

```text
PY-001  Language Choice                 → 01
PY-002  list / tuple                    → 02
PY-003  dict Hash / collision / delete  → 02
PY-004  Function Parameters             → 04
PY-005  Duck Typing / Protocol          → 08
PY-006  Iterator / Generator            → 06
PY-007  Decorator                       → 07
PY-008  Context Manager                 → 07
PY-009  Slicing Cost                    → 02
PY-010  GIL                             → 11
PY-011  Thread / Process                → 12
PY-012  asyncio / as_completed / timeout→ 12
PY-013  Lock / RLock / Semaphore        → 12
PY-014  Structured Output Validation    → 10（新增独立闭环）
PY-015  Closure                         → 04
```

这次整改强化了：Language Choice、dict 底层、Slicing 成本、Duck Typing / Protocol、Structured Output、asyncio Failure / Timeout / Cancellation 与同步原语，但没有改变 beginner-first 顺序。
"""
if "## 2026 Canonical Coverage / Remediation 结果" not in t:
    t = t.replace("## Python 与后续模块如何衔接", coverage + "\n## Python 与后续模块如何衔接", 1)
readme.write_text(t, encoding="utf-8")

# ------------------------------------------------------------------
# 4. Interview layer: append Canonical-specific additions.
# ------------------------------------------------------------------
interview = PY / "interview"
new_interview = r'''

---

# 2026 AI Application Canonical 补强

## Python、Java、Go 做 AI Application 应怎样选？

**答：** Python 的 AI/ML/Data 生态和迭代效率很强，适合模型、RAG、Agent orchestration 和大量 I/O 服务；Java 在大型企业后端生态、强类型和既有基础设施上有优势；Go 在高并发基础设施、静态编译和部署上常见。真实系统可以多语言协作，应该按 workload、团队资产和运维约束选择。

## dict 发生 Hash Collision 时会覆盖旧 key 吗？

**答：** 不会。hash 只帮助定位候选位置，碰撞后哈希表会继续探测其它槽位并使用 equality 判断真实 key。相等对象要求 hash 一致，但 hash 一致不代表对象相等。

## 删除 dict key 为什么不能简单把槽位当作“从未使用”？

**答：** 开放寻址类哈希表中的其它 key 可能依赖这条探测链；如果查找在被删除槽位提前停止，就可能错误地判断后续 key 不存在。

## Python 内建序列切片的成本？

**答：** 对常见 list/tuple/str，切片通常创建新序列，切出 k 个元素一般要 O(k) 时间和额外空间。`[::-1]` 很简洁，但通常也意味着复制；只想反向迭代可考虑 `reversed()`。

## Duck Typing 与 Protocol 有什么关系？

**答：** Duck Typing 强调对象是否具备需要的行为，不强制具体继承关系；`typing.Protocol` 把这种结构化行为要求写成静态可检查的契约。大型工程常结合 Duck Typing、Type Hint、Protocol/ABC 和测试。

## `asyncio.gather` 与 `as_completed` 有什么区别？

**答：** `gather` 适合并发启动一组任务并最终统一等待结果；`as_completed` 按实际完成顺序逐个产出结果，更适合最快结果先消费、渐进聚合和早停。两者都不会自动限流。

## Lock、RLock、Semaphore 怎么区分？

**答：** Lock 做互斥；RLock 允许同一线程重入；Semaphore 允许最多 N 个并发执行者，更适合容量限制。GIL 不能替代这些业务同步原语。

## Python 怎样安全处理 LLM Structured Output？

**答：** 先 parse JSON，再做 schema validation，再做 business / permission validation。`json.loads()` 成功只证明语法合法；TypedDict 主要是静态类型提示，不会自动运行时拒绝脏数据；外部输入可以使用 Pydantic 等做 runtime validation。模型输出不要直接 `eval()`，Repair/Retry 要有限次且不能绕过权限边界。
'''
p = interview / "高频面试题.md"
t = p.read_text(encoding="utf-8")
if "# 2026 AI Application Canonical 补强" not in t:
    p.write_text(t.rstrip() + new_interview + "\n", encoding="utf-8")

mistakes = r'''

---

# 2026 Canonical 新增易错边界

- ❌ “AI 后端都应该用 Python。” → ✅ 语言选择看生态、workload、团队栈和运维约束。
- ❌ “dict hash 一样就是同一个 key。” → ✅ collision 后仍需 equality 判断。
- ❌ “删除 dict key 就像这个槽位从没用过。” → ✅ 不能破坏后续 probe chain。
- ❌ “list 切片只是一个 view。” → ✅ 常见内建序列切片通常创建新对象并有 O(k) 时间/空间成本。
- ❌ “Duck Typing 就是什么类型都能传。” → ✅ 调用方仍依赖明确的行为契约；大型工程常用 Protocol/Type Hint/Test 显式化。
- ❌ “`gather` 会自动限流。” → ✅ 它负责等待/聚合，不替你控制并发上限。
- ❌ “Timeout 以后任务肯定停了。” → ✅ 调用方停止等待不代表底层任务或副作用停止，要考虑 Cancellation / Idempotency。
- ❌ “Semaphore 就是锁。” → ✅ Semaphore 更常用于最多 N 个并发的容量控制。
- ❌ “`json.loads` 成功就可以执行 Tool。” → ✅ 还需要 Schema、Business、Permission 校验。
- ❌ “TypedDict 会在运行时自动验证外部 JSON。” → ✅ TypedDict 主要服务静态类型检查。
'''
p = interview / "面试易错点.md"
t = p.read_text(encoding="utf-8")
if "# 2026 Canonical 新增易错边界" not in t:
    p.write_text(t.rstrip() + mistakes + "\n", encoding="utf-8")

quick = r'''

## 2026 AI Application 最后 2 分钟

```text
Language Choice：Python 生态/迭代强；Java/Go 看团队与 workload，不绝对化
Dict：hash → collision/probe → equality；平均 O(1) 不是最坏保证
Slicing：内建序列通常 copy，k 元素约 O(k) time + space
Duck Typing：行为契约；Protocol 把结构契约显式化
Structured Output：parse → schema → business → permission；never eval untrusted model text
asyncio：gather=统一等；as_completed=完成一个处理一个
Timeout：停止等待 ≠ 底层停止；考虑 cancellation / side effect
Sync Primitive：Lock=互斥，RLock=可重入，Semaphore=N 并发容量
```
'''
p = interview / "面试前速查表.md"
t = p.read_text(encoding="utf-8")
if "## 2026 AI Application 最后 2 分钟" not in t:
    p.write_text(t.rstrip() + "\n\n" + quick.strip() + "\n", encoding="utf-8")

# ------------------------------------------------------------------
# 5. Repository-level status sync.
# ------------------------------------------------------------------
root_readme = ROOT / "README.md"
replace_once(
    root_readme,
    "- [Python Foundation](python/README.md) 🟠 **v1 完整可用**；最新 15 Canonical / 当前统一深度标准的定向整改待完成",
    "- [Python Foundation](python/README.md) ✅ **13 个知识小板块**；v1 → current-standard Canonical Coverage / Depth Remediation 已完成",
)
replace_once(
    root_readme,
    "System Design 完成后的仓库补齐顺序是：**FastAPI → AI Backend Engineering → Python v1 定向整改**。",
    "Python v1 定向整改已完成；Foundation 接下来的仓库补齐顺序是：**FastAPI → AI Backend Engineering**。",
)
replace_once(
    root_readme,
    "| Python | 🟠 v1 完整可用；最新 Canonical / 当前深度标准定向整改待完成 |",
    "| Python | ✅ 13-block；15 Canonical Coverage / Depth Remediation 完成 |",
)

km = ROOT / "roadmap" / "knowledge-map.md"
replace_once(
    km,
    "## Python 🟠\n入口：[`../python/README.md`](../python/README.md) — v1 已有 12 章正文 + Review + Interview，可学习；最新 15 Canonical / 当前统一深度标准的定向整改待完成。",
    "## Python ✅ — 13 blocks\n入口：[`../python/README.md`](../python/README.md) — v1 已完成 current-standard Remediation；15 道 Python Canonical 已映射到 13 个 beginner-first 知识块，Review / Interview 同步完成。",
)
replace_once(km, "| Python | 🟠 v1 完整可用；定向整改待完成 |", "| Python | ✅ 13 blocks；Canonical Coverage / Depth PASS |")

progress = ROOT / "research" / "questions" / "progress.md"
replace_once(progress, "| Python | 🟠 v1 完整可用；最新 15 Canonical / 当前标准定向整改待完成 |", "| Python | ✅ **13 blocks**；15 Canonical Coverage / current-standard Depth Remediation 完成 |")
replace_once(
    progress,
    "FastAPI 正式教材\n→ AI Backend Engineering 正式教材\n→ Python v1 Canonical Coverage / Depth Remediation",
    "FastAPI 正式教材\n→ AI Backend Engineering 正式教材",
)

module_index = ROOT / "research" / "questions" / "module-index.md"
t = module_index.read_text(encoding="utf-8")
t = t.replace("Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架。", "Python 已完成 13-block current-standard remediation；FastAPI / AI Backend Engineering 仍只有课程骨架。")
if "Python ✅ 13 blocks" not in t:
    t = t.replace("当前教材结构：\n\n```text\n", "当前教材结构：\n\n```text\nPython ✅ 13 blocks；15 Canonical Coverage / Depth PASS\n")
module_index.write_text(t, encoding="utf-8")

qreadme = ROOT / "research" / "questions" / "README.md"
t = qreadme.read_text(encoding="utf-8")
t = t.replace("Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架。", "Python 已完成 current-standard Canonical Coverage / Depth Remediation；FastAPI / AI Backend Engineering 仍只有课程骨架。")
qreadme.write_text(t, encoding="utf-8")

foundation = ROOT / "roadmap" / "foundation-status-audit.md"
t = foundation.read_text(encoding="utf-8")
t = t.replace("## 3. Python Foundation — 🟠 v1 完整可用，但需要二次质量整改", "## 3. Python Foundation — ✅ v1 → current-standard Remediation 已完成")
t = t.replace("**结论：Python v1 = COMPLETE & USABLE；Current-standard Remediation = PENDING。**", "**结论：Python Foundation = 13 blocks；Canonical Coverage / Depth Remediation = PASS。**")
t = t.replace(
    "1. FastAPI：从 README 骨架写成正式 docs / review / interview\n2. AI Backend Engineering：从 README 骨架写成正式 docs / review / interview\n3. Python：保留 v1 主体，做 Canonical Coverage + Depth Remediation",
    "1. FastAPI：从 README 骨架写成正式 docs / review / interview\n2. AI Backend Engineering：从 README 骨架写成正式 docs / review / interview\n\nPython 的 current-standard remediation 已提前完成，不再列为待办。",
)
summary = """

### 3.5 本轮实际整改结果

```text
12-block v1
→ 13-block current curriculum
```

新增的唯一独立知识块是 `10-结构化数据-JSON与校验.md`。其它最新 Canonical 均并入已有主干：Language Choice→01、dict/Slicing→02、Duck Typing/Protocol→08、asyncio/Sync Primitive→12。正文、Review、Interview 和项目级状态已经同步。
"""
if "### 3.5 本轮实际整改结果" not in t:
    t = t.replace("---\n\n## 4. System Design 完成后的 Foundation 建设顺序", summary + "\n---\n\n## 4. System Design 完成后的 Foundation 建设顺序", 1)
foundation.write_text(t, encoding="utf-8")

# Granularity audit
cg = ROOT / "roadmap" / "curriculum-granularity-audit.md"
t = cg.read_text(encoding="utf-8")
if "## Python — COMPLETE：12 → 13" not in t:
    insertion = """
## Python — COMPLETE：12 → 13

Python v1 原 12 章 beginner-first 主干保持不变，只新增一个真正独立的 `Structured Data / JSON / Validation` 知识闭环；Language Choice、dict 底层、Slicing、Duck Typing、asyncio Failure / Synchronization 等最新 Canonical 通过加深原章节吸收。因此 **15 道 Canonical → 13 个教材知识块**，没有按题目机械增章。

"""
    t = t.replace("# 3. 最终整改结果\n", "# 3. 最终整改结果\n\n" + insertion, 1)
t = t.replace("| MySQL | 23 | 23 | ✅ PASS |", "| Python | 12 | 13 | ✅ COMPLETE |\n| MySQL | 23 | 23 | ✅ PASS |")
cg.write_text(t, encoding="utf-8")

# Content depth audit
cd = ROOT / "roadmap" / "content-depth-audit.md"
t = cd.read_text(encoding="utf-8")
if "# Python — ✅ PASS after current-standard remediation" not in t:
    py_audit = """
# Python — ✅ PASS after current-standard remediation

当前：**13 个连续知识小板块，`docs/01 → 13`。**

本轮不是按 15 道 Canonical 重建题库，而是保留原 0→1 主干并定向补强：

```text
01 Language Choice + Object Model
02 dict Hash / Collision / Delete + Slicing Cost
08 Duck Typing / Protocol Thinking
10 Structured Data / JSON / Runtime Validation（新增独立闭环）
11 Memory / GC / GIL
12 Thread / Process / asyncio / Timeout / Cancellation / Lock / RLock / Semaphore
```

同时旧 03–07 补齐正文内折叠自测，Review 迁移为 13 章，Interview 增加最新 AI Application Canonical 追问。

验收标准：13/13 正文连续、有 Interview 表达和折叠自测；README / Review 链接指向当前文件；旧 `10/11/12` 历史路径已删除。

**最终结论：Python Content Depth / Canonical Coverage PASS。**

---

"""
    t = t.replace("# 3. Redis — ✅ PASS", py_audit + "# 3. Redis — ✅ PASS", 1)
t = t.replace(
    "第一轮颗粒度整改后的四模块：68 篇\nSystem Design 首版独立验收：    19 篇\n--------------------------------\n合计：                          87 篇",
    "Python current-standard remediation：13 篇\n第一轮颗粒度整改后的四模块： 68 篇\nSystem Design 首版独立验收：     19 篇\n---------------------------------\n合计：                          100 篇",
)
cd.write_text(t, encoding="utf-8")

# ------------------------------------------------------------------
# 6. Mechanical validation.
# ------------------------------------------------------------------
docs = sorted((PY / "docs").glob("[0-9][0-9]-*.md"))
nums = [int(p.name[:2]) for p in docs]
if nums != list(range(1, 14)):
    raise SystemExit(f"python docs numbering invalid: {nums}")

for p in docs:
    text = p.read_text(encoding="utf-8")
    if "<details" not in text:
        raise SystemExit(f"missing folded self-test: {p}")
    if len(text.encode("utf-8")) < 3500:
        raise SystemExit(f"suspiciously short python doc: {p}")

# README local doc links must exist.
for target in re.findall(r"\]\((docs/[^)#]+\.md)\)", readme.read_text(encoding="utf-8")):
    if not (PY / target).exists():
        raise SystemExit(f"README broken doc link: {target}")

review_files = sorted(review.glob("[0-9][0-9]-*-图解与自测.md"))
review_nums = [int(p.name[:2]) for p in review_files]
if review_nums != list(range(1, 14)):
    raise SystemExit(f"python review numbering invalid: {review_nums}")

# Legacy paths must be gone.
legacy = [
    PY / "docs" / "10-内存管理-垃圾回收-GIL.md",
    PY / "docs" / "11-线程-进程-协程-async-await.md",
    PY / "docs" / "12-常见数据结构与复杂度.md",
    review / "10-内存管理-垃圾回收-GIL-图解与自测.md",
    review / "11-线程-进程-协程-async-await-图解与自测.md",
    review / "12-常见数据结构与复杂度-图解与自测.md",
]
for p in legacy:
    if p.exists():
        raise SystemExit(f"legacy path still exists: {p}")

# Temporary checkpoint is removed by this completed remediation.
checkpoint = PY / ".remediation-plan.md"
if checkpoint.exists():
    checkpoint.unlink()

print("Python Foundation remediation validated: 13 docs, 13 reviews, current Canonical coverage synced.")
