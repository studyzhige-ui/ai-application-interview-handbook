# 05. Lambda、推导式与常用内置函数

这一章主要解决两个问题：一是面试中常问的 Pythonic 写法；二是日常 Coding 题里非常常见的内置工具。

## 1. lambda 匿名函数

基本格式：

```python
lambda 参数: 表达式
```

例子：

```python
square = lambda x: x * x
print(square(5))  # 25
```

等价于：

```python
def square(x):
    return x * x
```

### lambda 的特点

- 没有显式函数名；
- 适合短小、一次性的函数逻辑；
- 函数体只能写表达式，不适合复杂多步骤逻辑。

### 常见场景：排序 key

```python
users = [
    {"name": "A", "age": 23},
    {"name": "B", "age": 19},
]

users.sort(key=lambda x: x["age"])
```

🎯 **面试回答**：lambda 是一种创建匿名函数的简洁语法，适合短小逻辑，例如作为 `sorted()`、`map()` 等函数的参数。复杂逻辑更推荐正常 `def`，可读性更好。

---

## 2. 列表推导式

```python
squares = [x * x for x in range(5)]
```

等价于：

```python
squares = []
for x in range(5):
    squares.append(x * x)
```

### 带条件

```python
evens = [x for x in range(10) if x % 2 == 0]
```

### 条件表达式 + 推导式

```python
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
```

⚠️ 不要把太复杂的逻辑塞进一行推导式。Pythonic 不等于“越短越好”，可读性更重要。

---

## 3. 集合推导式与字典推导式

```python
squares = {x * x for x in range(5)}

mapping = {x: x * x for x in range(5)}
```

元组没有“元组推导式”这种对应语法：

```python
g = (x * x for x in range(5))
```

这得到的是**生成器表达式**，不是 tuple。

要变成 tuple：

```python
t = tuple(x * x for x in range(5))
```

---

## 4. `enumerate`

不要手动维护索引：

```python
names = ["Alice", "Bob", "Carol"]

for i, name in enumerate(names):
    print(i, name)
```

指定起始值：

```python
for i, name in enumerate(names, start=1):
    print(i, name)
```

相比：

```python
for i in range(len(names)):
    print(i, names[i])
```

`enumerate` 通常更直接、更易读。

---

## 5. `zip`

将多个可迭代对象按位置配对：

```python
names = ["A", "B", "C"]
scores = [90, 80, 70]

for name, score in zip(names, scores):
    print(name, score)
```

```python
print(list(zip(names, scores)))
# [('A', 90), ('B', 80), ('C', 70)]
```

⚠️ 默认情况下，长度不一致时会按较短的一方停止。

### 解压

```python
pairs = [(1, "a"), (2, "b")]
nums, chars = zip(*pairs)
```

---

## 6. `sorted` 与 `list.sort`

```python
nums = [3, 1, 2]

new_nums = sorted(nums)
print(nums)      # 原列表不变
print(new_nums)  # [1, 2, 3]
```

```python
nums.sort()
print(nums)      # 原地排序
```

| 对比 | `sorted()` | `list.sort()` |
|---|---|---|
| 接收对象 | 任意可迭代对象 | 仅 list |
| 是否原地修改 | ❌ | ✅ |
| 返回值 | 新 list | `None` |

### key 参数

```python
words = ["aaa", "b", "cc"]
print(sorted(words, key=len))
# ['b', 'cc', 'aaa']
```

### 字典按 key 排序

```python
d = {'b': 2, 'a': 3, 'c': 1}
print(sorted(d.items()))
# [('a', 3), ('b', 2), ('c', 1)]
```

按 value：

```python
print(sorted(d.items(), key=lambda item: item[1]))
```

---

## 7. `map`

对每个元素应用函数：

```python
nums = [1, 2, 3]
result = map(lambda x: x * x, nums)
print(list(result))  # [1, 4, 9]
```

现代 Python 中 `map()` 返回惰性迭代对象。

很多情况下列表推导式更直观：

```python
[x * x for x in nums]
```

---

## 8. `filter`

保留函数判断为真的元素：

```python
nums = [1, 2, 3, 4]
result = filter(lambda x: x % 2 == 0, nums)
print(list(result))  # [2, 4]
```

等价风格：

```python
[x for x in nums if x % 2 == 0]
```

---

## 9. `reduce`

来自 `functools`：

```python
from functools import reduce

nums = [1, 2, 3, 4]
product = reduce(lambda a, b: a * b, nums)
print(product)  # 24
```

它会把序列元素不断累计为一个结果。

⚠️ 面试知道含义即可。真实代码中如果有 `sum()`、`max()`、`min()` 等更直接的表达方式，通常优先使用可读性更好的工具。

---

## 10. `any` 与 `all`

```python
values = [True, True, False]

print(any(values))  # 至少一个为真 -> True
print(all(values))  # 全部为真 -> False
```

Coding 题中很常见：

```python
nums = [2, 4, 6]
print(all(x % 2 == 0 for x in nums))
```

---

## 11. `min` / `max` 的 key

```python
users = [
    {"name": "A", "age": 20},
    {"name": "B", "age": 30},
]

oldest = max(users, key=lambda x: x["age"])
```

---

## 12. 面试常见对比

### map/filter vs 推导式

二者都能完成映射与筛选。推导式往往更符合 Python 常见代码风格、可读性较好；`map/filter` 在已有函数可直接复用时也很自然，而且返回惰性对象。

### 生成器表达式 vs 列表推导式

```python
[x * x for x in range(1000000)]  # 一次构造整个列表
(x * x for x in range(1000000))  # 按需生成
```

如果不需要一次保存全部结果，生成器表达式通常更节省内存。

下一章：[06. 迭代器、生成器与 yield](06-迭代器-生成器-yield.md)
