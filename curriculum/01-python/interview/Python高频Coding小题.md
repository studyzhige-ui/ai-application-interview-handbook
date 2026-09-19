# Python 高频 Coding 小题

> 这些题不是为了刷算法难题，而是让你熟悉 Python 常用写法。面试时先保证正确和可读，再考虑一行写法。

## 1. 列表去重

### 不要求保序

```python
nums = [1, 2, 2, 3]
result = list(set(nums))
```

### 要求保留第一次出现顺序

```python
result = list(dict.fromkeys(nums))
```

也可以手写：

```python
def deduplicate(nums):
    seen = set()
    result = []
    for x in nums:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result
```

---

## 2. 判断列表是否存在重复元素

```python
def has_duplicates(nums):
    return len(nums) != len(set(nums))
```

如果元素不可哈希，则不能直接放进 set，需要换思路。

---

## 3. 反转字符串

```python
s = "hello"
print(s[::-1])
```

---

## 4. 判断回文字符串

```python
def is_palindrome(s):
    return s == s[::-1]
```

如果题目要求忽略大小写和非字母数字：

```python
def is_palindrome(s):
    chars = [c.lower() for c in s if c.isalnum()]
    return chars == chars[::-1]
```

---

## 5. 删除字符串中的所有空白

```python
s = "a b\n c\t"
result = "".join(s.split())
print(result)  # abc
```

---

## 6. 统计字符频率

```python
from collections import Counter

s = "banana"
count = Counter(s)
print(count)
```

手写版：

```python
count = {}
for c in s:
    count[c] = count.get(c, 0) + 1
```

---

## 7. 找出现次数最多的元素

```python
from collections import Counter

nums = [1, 1, 2, 2, 2, 3]
value, freq = Counter(nums).most_common(1)[0]
```

---

## 8. 两个列表组合

```python
names = ["A", "B", "C"]
scores = [90, 80, 70]

pairs = list(zip(names, scores))
```

---

## 9. 两个列表生成字典

```python
keys = ["a", "b", "c"]
values = [1, 2, 3]

d = dict(zip(keys, values))
```

---

## 10. 字典按 key 排序

```python
d = {'b': 2, 'a': 3, 'c': 1}
result = sorted(d.items())
```

按 value：

```python
result = sorted(d.items(), key=lambda item: item[1])
```

---

## 11. 合并两个字典

现代 Python：

```python
a = {"x": 1}
b = {"y": 2}

c = a | b
```

通用解包写法：

```python
c = {**a, **b}
```

key 冲突时，后面的值覆盖前面的值。

---

## 12. 找两个列表的交集

```python
a = [1, 2, 3]
b = [2, 3, 4]

result = list(set(a) & set(b))
```

如果要保留顺序/重复次数，需要按题目要求设计，不能无脑 set。

---

## 13. 列表展开一层

```python
matrix = [[1, 2], [3, 4], [5]]
flat = [x for row in matrix for x in row]
```

更复杂任意深度嵌套不能直接用这一行，需要递归或栈。

---

## 14. 找列表最大值及其索引

```python
nums = [10, 99, 30]
idx, value = max(enumerate(nums), key=lambda item: item[1])
```

---

## 15. 同时遍历索引和值

```python
for i, value in enumerate(nums):
    print(i, value)
```

---

## 16. 两数之和

题目：返回和为 target 的两个元素索引。

```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
```

复杂度：时间 O(n)，额外空间 O(n)。

---

## 17. 找 Top K 最大元素

数据量不大：

```python
result = sorted(nums, reverse=True)[:k]
```

数据量大且 k 小：

```python
import heapq
result = heapq.nlargest(k, nums)
```

面试追问“海量数据 Top K”时要说堆思路，而不是只给排序。

---

## 18. 统计单词频率

```python
from collections import Counter

text = "python is good python is simple"
count = Counter(text.split())
```

---

## 19. 分组

按奇偶分组：

```python
from collections import defaultdict

groups = defaultdict(list)
for x in range(10):
    groups[x % 2].append(x)
```

`defaultdict` 很适合“key 不存在就先创建默认容器”的场景。

---

## 20. 安全读取嵌套字典

简单两层：

```python
city = user.get("address", {}).get("city")
```

如果层级非常深或结构复杂，最好设计专门的数据模型/校验逻辑，而不是无限 `.get()`。

---

## 21. 交换两个变量

```python
a, b = b, a
```

利用 Python 的打包/解包机制，无需临时变量。

---

## 22. 找第二大不同值

```python
def second_largest(nums):
    unique = set(nums)
    if len(unique) < 2:
        raise ValueError("need at least two distinct values")
    unique.remove(max(unique))
    return max(unique)
```

面试时可继续优化为一次遍历、O(1) 额外空间。

---

## 23. 读取大文件

不推荐：

```python
content = f.read()
```

如果文件非常大，逐行：

```python
with open("big.log", encoding="utf-8") as f:
    for line in f:
        process(line)
```

---

## 24. 将函数执行时间做成装饰器

```python
import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(time.perf_counter() - start)
        return result
    return wrapper
```

---

## 25. 生成斐波那契数列：生成器版

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

这是理解生成器和无限序列的经典例子。

---

# 面试写代码时的检查清单

写完后至少快速检查：

1. 空输入怎么办？
2. 是否有重复值？
3. 是否需要保持原顺序？
4. 输入元素是否可哈希？
5. 有没有无意修改原数据？
6. 时间复杂度是多少？
7. 空间复杂度是多少？
8. 题目要“值”还是“索引”？
9. 能否先写正确版本，再优化？
10. Python 内置函数是否让代码更清晰，而不是更炫技？
