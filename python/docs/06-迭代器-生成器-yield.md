# 06. 迭代器、生成器与 yield

这组概念经常连着考：**可迭代对象 → 迭代器 → 生成器 → `yield` → 惰性求值**。

## 1. 可迭代对象 Iterable

💡 **新手理解**：能放进 `for` 循环里逐个取元素的对象，通常就是可迭代对象。

常见例子：

- list
- tuple
- str
- dict
- set
- range
- generator

```python
for x in [1, 2, 3]:
    print(x)
```

`iter(obj)` 会尝试获取该对象的迭代器。

```python
lst = [1, 2, 3]
it = iter(lst)
```

---

## 2. 迭代器 Iterator

迭代器提供“一个一个取值”的能力。

```python
lst = [10, 20, 30]
it = iter(lst)

print(next(it))  # 10
print(next(it))  # 20
print(next(it))  # 30
```

再继续：

```python
next(it)  # StopIteration
```

🎯 **面试表达**：迭代器对象支持 `__iter__()` 和 `__next__()` 协议；`next()` 每次取下一个值，没有值时抛出 `StopIteration`。

## 3. `for` 循环背后发生了什么

可以把：

```python
for x in data:
    print(x)
```

近似理解成：

```python
it = iter(data)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    print(x)
```

所以 `for` 能遍历对象，本质上依赖的是迭代协议，而不是必须知道对象内部如何存储。

---

## 4. 可迭代对象和迭代器的区别

| 对比 | Iterable | Iterator |
|---|---|---|
| 能否用于 `for` | ✅ | ✅ |
| `iter(obj)` | 返回迭代器 | 通常返回自身 |
| `next(obj)` | 不一定支持 | ✅ |
| 是否保存遍历状态 | 通常不是重点 | ✅ |

```python
lst = [1, 2, 3]
# next(lst)  # TypeError

it = iter(lst)
next(it)     # 可以
```

---

## 5. 生成器 Generator

生成器是一种特殊的迭代器。

最常见创建方式有两种：

### 方式一：生成器函数

```python
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1
```

调用：

```python
g = count_up_to(3)
print(g)          # generator object
print(next(g))    # 1
print(next(g))    # 2
```

### 方式二：生成器表达式

```python
g = (x * x for x in range(5))
```

---

## 6. `yield` 和 `return` 的区别

### `return`

函数执行到 `return` 就结束：

```python
def f():
    return 1
```

### `yield`

```python
def f():
    yield 1
    yield 2
    yield 3
```

每次取值时，函数运行到 `yield` 暂停，并保存当前执行状态；下一次 `next()` 时从暂停的位置继续。

💡 可以把生成器想成“可以暂停和继续的函数”。

| 对比 | `return` | `yield` |
|---|---|---|
| 是否结束函数 | ✅ | 暂停 |
| 是否保存状态 | 不需要 | ✅ |
| 是否适合连续产出多个值 | ❌ | ✅ |
| 结果 | 普通返回值 | 生成器迭代过程 |

---

## 7. 为什么生成器省内存

列表：

```python
nums = [x * x for x in range(1_000_000)]
```

通常会一次构造并保存大量元素。

生成器：

```python
nums = (x * x for x in range(1_000_000))
```

结果按需产生，不需要一次保存全部结果。

这叫**惰性求值 / lazy evaluation**。

适合：

- 大文件逐行读取；
- 大数据流；
- 流式处理；
- 无限序列；
- 管道式处理。

---

## 8. 生成器只能消费一次吗？

很多情况下是的。

```python
g = (x for x in range(3))

print(list(g))  # [0, 1, 2]
print(list(g))  # []
```

因为迭代状态已经走到末尾。

⚠️ 这和 list 不同：list 可以重复调用 `iter(list)` 得到新的迭代器。

---

## 9. 自定义迭代器

```python
class Counter:
    def __init__(self, limit):
        self.current = 0
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        self.current += 1
        return self.current
```

使用：

```python
for x in Counter(3):
    print(x)
```

---

## 10. 高频面试题

### Q1：Iterable 和 Iterator 区别？

🎯 可迭代对象可以通过 `iter()` 获取迭代器；迭代器保存遍历状态并支持 `next()`。一个对象可以是 Iterable 但不是 Iterator，例如 list。

### Q2：生成器和迭代器什么关系？

生成器是迭代器的一种，自动实现迭代协议，并通过 `yield` 或生成器表达式按需产生值。

### Q3：生成器为什么省内存？

因为采用惰性求值，不一次性把所有结果存入内存，而是使用时逐个计算和产生。

### Q4：`yield` 到底做了什么？

产生一个值，并暂停当前生成器函数，保留执行现场；下一次请求值时从上次暂停的位置恢复执行。

下一章：[07. 装饰器与上下文管理器](07-装饰器-上下文管理器.md)
