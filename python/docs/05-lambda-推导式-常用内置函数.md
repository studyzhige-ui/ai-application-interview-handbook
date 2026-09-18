# 05. Lambda、推导式与常用内置函数

[← 上一章：函数与作用域](04-函数-参数-作用域-闭包.md) · [模块主页](../README.md) · [下一章：迭代与生成器 →](06-迭代器-生成器-yield.md)

已经会写循环和函数以后，再学简洁表达才有意义。本章不是让你把程序尽量压成一行，而是认识几类反复出现的数据处理任务：**逐项转换、筛选、配对、排序、汇总**。

```text
先用普通循环说清楚要做什么
→ 用短函数描述处理规则
→ 选择对应工具
→ 判断是否立即生成全部结果
→ 最后检查可读性、边界和副作用
```

## 1. lambda：把一个短规则作为函数传出去

### 1.1 先对照熟悉的 def

```python
def square(x):               # 定义一个有名字的函数
    return x * x             # 返回输入的平方

print(square(5))             # 25
```

同样的计算可以写为：

```python
square = lambda x: x * x     # 创建匿名函数，再把名字 square 绑定到它
print(square(5))             # 25：仍然需要调用才会计算
```

**Lambda / Anonymous Function（匿名函数）** 的结构是 `lambda 参数: 表达式`。冒号左边是输入参数，右边是一条表达式，其结果就是返回值，不写 `return`。

“匿名”指这种语法创建函数时没有 `def` 后的函数名，并不是说这个函数对象不能再被变量引用。它的函数体只能是一条表达式，不适合需要多条语句、复杂异常处理或多步业务的场景；这些情况用 `def` 更容易阅读和调试。

### 1.2 排序中的 key 是“比较依据提取器”

```python
users = [{"name": "A", "age": 23}, {"name": "B", "age": 19}]  # 两条记录
users.sort(key=lambda user: user["age"])  # 对每条记录取年龄作为排序依据
print(users)                 # [{'name': 'B', 'age': 19}, {'name': 'A', 'age': 23}]
```

这里没有把记录替换成年龄。`key` 函数提供用于比较的值，排序结果保留原来的记录对象。`user` 是每次传给短函数的一条记录，不是 Python 内置名字。

🎯 **面试回答**：lambda 是一种创建匿名函数的简洁语法，适合短小逻辑，例如作为 `sorted()`、`map()` 等函数的参数。复杂逻辑更推荐正常 `def`，可读性更好。

## 2. 推导式：从循环到“生成一个结果集合”

### 2.1 列表推导式按什么顺序阅读

先写普通循环：

```python
squares = []                 # 创建保存结果的列表
for x in range(5):           # x 依次取得 0、1、2、3、4
    squares.append(x * x)    # 对每个 x 算平方并追加
print(squares)               # [0, 1, 4, 9, 16]
```

再合起来：

```python
squares = [x * x for x in range(5)]  # 对 range(5) 中每个 x 计算平方，收集成列表
```

**List Comprehension（列表推导式）** 可以按“先读 `for` 的来源，再读最前面的结果表达式”理解。它通常立即遍历输入，构造整个结果列表。

### 2.2 筛选元素与选择结果，是两种不同的 if

```python
evens = [x for x in range(10) if x % 2 == 0]  # 只保留能被 2 整除的 x
print(evens)                                 # [0, 2, 4, 6, 8]

labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]  # 每个 x 都生成一个标签
print(labels)                                # ['even', 'odd', 'even', 'odd', 'even']
```

`%` 是求余数，`x % 2 == 0` 判断偶数。`for` 后的 `if` 是 **Filter（筛选）**，可能让结果变短；最前面的 `A if 条件 else B` 是 **Conditional Expression（条件表达式）**，为每项选择生成 A 还是 B，不因为选择了 B 就丢掉这一项。

### 2.3 集合和字典推导式，只是结果容器不同

```python
unique_squares = {x * x for x in [-2, -1, 1, 2]}  # 生成集合，相等的平方值只保留一份
print(unique_squares == {1, 4})                   # True：不依赖集合打印顺序

mapping = {x: x * x for x in range(3)}  # x 作键，x 的平方作值
print(mapping)                         # {0: 0, 1: 1, 2: 4}
```

字典的键和集合成员仍然需要可哈希；重复的字典键会关联最后一次赋给该键的值。推导式并不会取消第 02 章讲过的容器约束。

### 2.4 圆括号不是“元组推导式”

```python
g = (x * x for x in range(5))       # 生成器表达式：创建按需计算结果的对象
values = tuple(x * x for x in range(5))  # tuple 消费生成器，把所有结果保存为元组
print(values)                       # (0, 1, 4, 9, 16)
```

**Generator Expression（生成器表达式）** 暂时不保存全部结果，只在需要下一项时计算。`tuple(...)` 会消费它，最终仍保存全部结果，所以转成 tuple 之后不能继续声称“没有保存全部数据”。第 06 章会解释这个按需取值过程。

### 2.5 什么时候退回普通循环

一条推导式如果包含多层嵌套、难读的条件、修改外部状态或复杂异常处理，就该考虑拆成循环或辅助函数。**Pythonic（符合 Python 表达习惯）** 的重点是清晰地表达意图，不是行数越少越好。

例如第 03 章的独立行列表，可以在已经理解原理后写成：

```python
rows = [[0, 0] for _ in range(3)]  # 每轮都创建一个新的内部列表，不是重复同一个引用
rows[0][0] = 1                     # 修改第一行
print(rows)                        # [[1, 0], [0, 0], [0, 0]]
```

## 3. 遍历工具：拿编号、配对数据，而不是手动管理状态

### 3.1 enumerate：同时得到编号和元素

```python
names = ["Alice", "Bob", "Carol"]  # 要逐项处理的名字
for i, name in enumerate(names):   # 每轮得到一个 (编号, 元素) 并解包
    print(i, name)                 # 依次输出 0 Alice、1 Bob、2 Carol

for rank, name in enumerate(names, start=1):  # 编号从 1 开始
    print(rank, name)                        # 依次输出 1 Alice、2 Bob、3 Carol
```

`enumerate` 的计数不改变原列表的索引；`start=1` 常用于显示序号，不会让 `names[1]` 变成第一个元素。

手动写 `for i in range(len(names))` 再访问 `names[i]` 也合法，但只需要编号与元素时，`enumerate` 直接表达二者一起来，更少维护一套下标逻辑。

### 3.2 zip：按相同位置把多组数据配成元组

```python
names = ["A", "B", "C"]      # 第一组数据
scores = [90, 80, 70]        # 第二组数据
for name, score in zip(names, scores):  # 每轮得到并解包一个 (名字, 分数)
    print(name, score)                  # A 90、B 80、C 70

print(list(zip(names, scores)))  # [('A', 90), ('B', 80), ('C', 70)]
```

`zip` 返回按需产出元组的迭代器；`list(...)` 把结果消费并存起来。默认到最短输入结束就停止，不会自动填补缺项：

```python
print(list(zip([1, 2], ["a"])))  # [(1, 'a')]：第二个输入先结束
# list(zip([1, 2], ["a"], strict=True))  # 错误示例：要求等长时，会在消费到不匹配处抛 ValueError
```

业务要求一一对应时，Python 3.10+ 可以使用 `strict=True` 及时暴露长度不匹配，而不是悄悄丢掉尾部。这个检查随着迭代进行，不一定在创建 `zip` 对象的瞬间完成。

### 3.3 zip 配合星号，可以把行重新组织成列

```python
pairs = [(1, "a"), (2, "b")]  # 两行，每行两项
nums, chars = zip(*pairs)     # 先展开为 zip((1, 'a'), (2, 'b'))，再把两列解包
print(nums)                  # (1, 2)
print(chars)                 # ('a', 'b')
```

这里综合了上一章的“调用时展开”和第 01 章的“赋值解包”。空的 `pairs` 没有两列可解包，实际代码要先决定空输入应该返回什么，不能只背这一行而不看输入形状。

## 4. 排序与极值：先确定是否需要改变原对象

### 4.1 sorted 返回新列表，list.sort 修改原列表

```python
nums = [3, 1, 2]             # 原始顺序
new_nums = sorted(nums)      # 构造新的已排序列表
print(nums, new_nums)        # [3, 1, 2] [1, 2, 3]
result = nums.sort()         # 原地排序 nums；方法返回 None
print(nums, result)          # [1, 2, 3] None
```

| 对比 | `sorted()` | `list.sort()` |
|---|---|---|
| 输入 | 可迭代对象 | 列表对象本身 |
| 是否修改原列表 | 否 | 是 |
| 返回 | 新列表 | None |
| 合适场景 | 保留原顺序，同时得到结果 | 明确要重新组织现有列表 |

⚠️ 错误：`nums = nums.sort()`。正确：原地排序写 `nums.sort()`；需要新结果写 `new_nums = sorted(nums)`。

### 4.2 key 选依据，reverse 选方向

```python
words = ["aaa", "b", "cc"]   # 长度分别为 3、1、2
print(sorted(words, key=len)) # ['b', 'cc', 'aaa']：传入 len 函数，不是提前调用 len()
print(sorted(words, key=len, reverse=True))  # ['aaa', 'cc', 'b']：按长度降序
```

内置排序是稳定的：排序依据相等时，保留原来的相对顺序。这可以帮助理解“先按次要字段排，再按主要字段稳定排序”；不要把“稳定”误解为任何类型的元素都能互相比较。

### 4.3 字典排序：你需要的是键、值，还是键值对

```python
d = {"b": 2, "a": 3, "c": 1}  # 插入顺序不是按字母排序
print(sorted(d))              # ['a', 'b', 'c']：直接迭代字典取得的是键
print(sorted(d.items()))      # [('a', 3), ('b', 2), ('c', 1)]：二元组按首项等顺序比较
print(sorted(d.items(), key=lambda item: item[1]))  # [('c', 1), ('b', 2), ('a', 3)]
```

`d.items()` 提供 `(键, 值)`，所以 `item[1]` 是值。`sorted` 返回列表，不会把字典原地改成另一种遍历顺序；需要新字典时，再明确构造。

### 4.4 min / max：只取极值，不必排序全部数据

```python
users = [{"name": "A", "age": 20}, {"name": "B", "age": 30}]  # 两条记录
oldest = max(users, key=lambda user: user["age"])  # 根据年龄选出原记录
print(oldest)                                     # {'name': 'B', 'age': 30}
```

`max` 返回被选中的元素，不是 `key` 算出的年龄。`min` 同理。空输入且没有默认值时会抛 `ValueError`；业务允许“没有结果”时可以对可迭代对象使用 `max(values, default=None)` 等明确约定。

## 5. 映射、筛选、汇总：把每种工具放回任务里

### 5.1 map：把同一个函数应用到每个元素

```python
nums = [1, 2, 3]                      # 原数据
result = map(lambda x: x * x, nums)    # 创建逐项计算平方的迭代器，尚未保存全部结果
print(list(result))                   # [1, 4, 9]：消费并收集
print([x * x for x in nums])           # [1, 4, 9]：列表推导式直接构造结果
```

已有现成函数时，`map(int, ["1", "2"])` 很直观；需要临时写一个复杂 lambda 才能使用时，推导式或普通循环可能更容易读。

### 5.2 filter：保留判断为真的元素，不替换元素

```python
nums = [1, 2, 3, 4]                          # 原始数据
result = filter(lambda x: x % 2 == 0, nums)   # 按是否为偶数筛选
print(list(result))                          # [2, 4]：留下原来的元素
print([x for x in nums if x % 2 == 0])        # [2, 4]：等价的列表构造意图
```

`filter` 也是惰性迭代器。其判断函数返回值会做真值判断，不要求只能返回恰好 `True` 或 `False`；这与第 01 章的真值规则一致。

### 5.3 reduce：把多项逐步折叠成一个累计值

```python
from functools import reduce       # reduce 位于标准库 functools，不是无需导入的内置函数

nums = [1, 2, 3, 4]                 # 要累计的数据
product = reduce(lambda acc, x: acc * x, nums, 1)  # 初始累计值为 1，每次乘上下一个 x
print(product)                     # 24
```

```text
初值 1 → 1×1 → 1×2 → 2×3 → 6×4 → 24
          每一步的结果成为下一步的 acc（累计值）
```

不提供初始值时，会从前两个元素开始合并；空输入且没有初始值会失败。初始值不仅改变空输入行为，也定义累计的起点。求和用 `sum`、极值用 `min/max` 往往更直接，不必为了使用 `reduce` 而绕远。

### 5.4 any 与 all：只需要一个真假结论

```python
values = [True, True, False]  # 一组判断值
print(any(values))           # True：至少有一个真值
print(all(values))           # False：不是全部都是真值

nums = [2, 4, 6]                            # 三个偶数
print(all(x % 2 == 0 for x in nums))         # True：逐个检查是否都为偶数
print(any([]), all([]))                     # False True：空输入的规则
```

`any` 一旦发现真值就能停止，`all` 一旦发现假值就能停止，这叫短路。空输入没有一个真值，所以 `any([])` 为 False；也没有反例违反“全部为真”，所以 `all([])` 为 True。

需要“至少有一个元素且全部符合规则”时，必须同时检查非空；不能把 `all` 结果直接当成“输入存在”的证据。

## 6. 最后检查：立即保存结果，还是按需消费

**Eager（立即求值）** 与 **Lazy（惰性求值）** 不是速度排名，而是“什么时候计算、是否保存所有结果”的区别。

| 写法 | 主要行为 |
|---|---|
| 列表／集合／字典推导式、`sorted()` | 消费输入并构造结果容器 |
| 生成器表达式、`map()`、`filter()`、`zip()`、`enumerate()` | 提供可逐项消费的迭代器 |
| `sum()`、`reduce()` | 消费输入并产生累计结果 |
| `any()`、`all()` | 消费到足以判断结果时可能提前停止 |

```python
all_results = [x * x for x in range(1_000_000)]  # 保存一百万个结果
on_demand = (x * x for x in range(1_000_000))     # 保留按需计算过程，不先存全部平方值
```

需要反复访问所有结果，就得保存或重新计算；不需要全部保存时，按需消费有助于降低结果存储。迭代器消费后是否还能重新来一遍、为什么能暂停，下一章继续回答。

本章依据：[内置函数](https://docs.python.org/3.14/library/functions.html)、[数据结构与推导式](https://docs.python.org/3.14/tutorial/datastructures.html)、[排序指南](https://docs.python.org/3.14/howto/sorting.html)、[functools](https://docs.python.org/3.14/library/functools.html)。

---

## 7. 🎯 面试常见对比

### map/filter vs 推导式

二者都能完成映射与筛选。推导式往往更符合 Python 常见代码风格、可读性较好；`map/filter` 在已有函数可直接复用时也很自然，而且返回惰性对象。

### 生成器表达式 vs 列表推导式

```python
[x * x for x in range(1000000)]  # 一次构造整个列表
(x * x for x in range(1000000))  # 按需生成
```

如果不需要一次保存全部结果，生成器表达式通常更节省内存。

## 8. ⚠️ 易错点

- 错误：`(x for x in data)` 是元组推导式。正确：它创建生成器；需要元组时用 `tuple(...)` 消费结果。
- 错误：两个输入长度不同，zip 会自动补齐。正确：默认到较短者结束；必须等长时使用 `strict=True`。
- 错误：排序 key 会替换原元素。正确：它只提供比较依据，输出中仍是原元素。
- 错误：`list.sort()` 返回排序后的列表。正确：它返回 None；需要新列表用 `sorted()`。
- 错误：有了生成器就一定不占大量内存。正确：后面再 `list(...)` 仍会保存全部结果；过程也可能持有大输入引用。
- 错误：`all` 为真就说明输入非空。正确：空输入的 `all` 也是 True，需要单独表达非空条件。

## 9. 本章自测

<details>
<summary>1. 为什么复杂业务逻辑不应该为了“Pythonic”强塞进一条列表推导式？</summary>

可读性和可调试性比行数更重要。包含多层条件、副作用或复杂异常处理时，普通循环通常更清晰。

</details>

<details>
<summary>2. `sorted()` 与 `list.sort()` 的核心区别是什么？</summary>

`sorted()` 接收任意可迭代对象并返回新 list；`list.sort()` 只作用于 list，原地排序并返回 `None`。

</details>

下一章：[06. 迭代器、生成器与 yield](06-迭代器-生成器-yield.md)
