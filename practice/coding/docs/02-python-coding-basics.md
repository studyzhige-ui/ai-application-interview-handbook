# 02｜Python Coding Basics：把基础语法变成真正能写代码的工具

[← 上一章：Programming Fundamentals](01-programming-fundamentals.md) · [Coding 首页](../README.md) · [下一章：Basic Coding Exercises →](03-basic-exercises.md)

> 本章目标：看到一个小问题时，你不再只知道“Python 有 list / dict / set”，而是知道**数据应该放在哪里、怎样遍历、怎样查询、怎样积累结果**。

---

## 1. 先建立一个 Coding 视角

写小程序时，经常只有四件事：

```text
输入数据
↓
保存数据
↓
遍历 / 查询 / 修改
↓
产生结果
```

Python 常见容器不是一堆孤立语法，而是在回答：

```text
我需要按位置保存？
→ list

我需要按键查值？
→ dict

我只关心一个元素出现没出现？
→ set

我需要一段字符序列？
→ str

我需要固定的一组值？
→ tuple
```

更深的底层机制见 [Python Foundation 02](../../python/docs/02-核心数据类型与容器.md)。这里先练使用。

---

## 2. list：算法题最常见的顺序容器

```python
nums = [10, 20, 30]
```

可以用下标访问：

```python
print(nums[0])  # 10
print(nums[1])  # 20
```

Python 下标从 `0` 开始。

### 2.1 修改

```python
nums[1] = 99
print(nums)
```

得到：

```text
[10, 99, 30]
```

### 2.2 追加

```python
nums.append(40)
```

### 2.3 删除最后一个

```python
last = nums.pop()
```

### 2.4 长度

```python
n = len(nums)
```

---

## 3. 遍历 list：值、下标和两者同时要

### 3.1 只需要值

```python
for x in nums:
    print(x)
```

### 3.2 只需要下标

```python
for i in range(len(nums)):
    print(i)
```

### 3.3 下标和值都要：`enumerate`

```python
for i, x in enumerate(nums):
    print(i, x)
```

如果：

```python
nums = [10, 20, 30]
```

则：

```text
0 10
1 20
2 30
```

不要看到算法题就条件反射写 `range(len(nums))`。如果根本不需要下标，直接 `for x in nums` 更清楚。

---

## 4. str：字符串也是可以按顺序遍历的

```python
s = "hello"
```

### 4.1 下标

```python
print(s[0])  # h
```

### 4.2 遍历字符

```python
for ch in s:
    print(ch)
```

### 4.3 切片

```python
print(s[1:4])  # ell
```

先记：

```text
s[start:end]
包含 start
不包含 end
```

### 4.4 字符串不能像 list 那样原地改某个字符

下面会报错：

```python
s[0] = "H"
```

需要构造新字符串。

---

## 5. dict：当问题变成“根据一个键快速找到东西”

```python
score = {
    "Alice": 90,
    "Bob": 85,
}
```

访问：

```python
print(score["Alice"])
```

新增 / 修改：

```python
score["Carol"] = 95
score["Bob"] = 88
```

判断某个键是否存在：

```python
if "Alice" in score:
    print("found")
```

这句：

```python
if key in my_dict:
```

是算法题里非常重要的操作。

---

## 6. dict 最常见的两个算法用途

### 6.1 计数

统计字符出现次数：

```python
s = "banana"
count = {}

for ch in s:
    if ch not in count:
        count[ch] = 0

    count[ch] += 1

print(count)
```

得到：

```python
{"b": 1, "a": 3, "n": 2}
```

也可以写：

```python
count[ch] = count.get(ch, 0) + 1
```

先理解展开版本，再追求简洁。

### 6.2 记录“某个值在哪里出现过”

```python
nums = [5, 8, 2]

position = {}

for i, x in enumerate(nums):
    position[x] = i
```

得到：

```python
{
    5: 0,
    8: 1,
    2: 2,
}
```

这就是“两数之和”优化的基础。

---

## 7. Hot100：从两层循环推导“两数之和”的 dict 解法

上一章写的是：

```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]
```

它做了很多重复尝试。

现在站在 `nums[i] = x` 的位置问：

```text
我要找另一个数 y

x + y = target

所以：
y = target - x
```

真正的问题变成：

> `target - x` 之前出现过吗？

这正适合 dict。

```python
def two_sum(nums, target):
    seen = {}

    for i, x in enumerate(nums):
        need = target - x

        if need in seen:
            return [seen[need], i]

        seen[x] = i
```

手工追踪：

```text
nums = [2, 7, 11, 15]
target = 9
```

第一轮：

```text
i = 0
x = 2
need = 7
seen = {}

7 不在 seen

记录：
seen[2] = 0
```

第二轮：

```text
i = 1
x = 7
need = 2
seen = {2: 0}

2 在 seen
→ 返回 [0, 1]
```

现在“用哈希表”不再是答案，而是从问题需求推导出来的选择。

---

## 8. set：只关心“有没有”，不关心对应值

```python
seen = set()

seen.add(10)
seen.add(20)

print(10 in seen)
```

得到：

```text
True
```

如果只需要：

> “这个元素以前出现过吗？”

通常 set 比 dict 的语义更直接。

例子：判断是否有重复元素。

```python
def has_duplicate(nums):
    seen = set()

    for x in nums:
        if x in seen:
            return True

        seen.add(x)

    return False
```

---

## 9. tuple：一组固定组合

```python
point = (3, 5)
```

常见于：

- 坐标 `(row, col)`；
- 字典键；
- 一次返回多个值；
- 堆中的 `(priority, item)`。

例如：

```python
row, col = (3, 5)
```

叫做解包。

---

## 10. `range`、`enumerate`、`zip`

### 10.1 range

```python
for i in range(3):
    print(i)
```

输出 `0 1 2`。

### 10.2 enumerate

```python
for i, x in enumerate(["a", "b", "c"]):
    print(i, x)
```

### 10.3 zip

如果两组数据一一对应：

```python
names = ["Alice", "Bob"]
scores = [90, 85]

for name, score in zip(names, scores):
    print(name, score)
```

不要为了“高级写法”强行用这些工具。原则仍然是：**让代码表达当前问题最清楚。**

---

## 11. 排序：`sorted` 和 `.sort()`

### `sorted(nums)`

```python
nums = [3, 1, 2]
new_nums = sorted(nums)

print(nums)      # [3, 1, 2]
print(new_nums)  # [1, 2, 3]
```

返回一个新的排序结果。

### `nums.sort()`

```python
nums = [3, 1, 2]
nums.sort()

print(nums)
```

直接修改原列表。

以后做算法题前先问：

> 我允许改变原输入吗？

这比“哪个函数更短”重要。

---

## 12. 列表推导式：先会普通循环，再学压缩写法

普通写法：

```python
result = []

for x in nums:
    if x % 2 == 0:
        result.append(x)
```

推导式：

```python
result = [x for x in nums if x % 2 == 0]
```

初学阶段，如果推导式让你无法追踪执行顺序，就先写普通循环。

算法面试里“清楚”通常比“少两行”更重要。

---

## 13. 函数：把输入、处理、输出分开

一个非常推荐的结构：

```python
def solve(nums):
    total = 0

    for x in nums:
        total += x

    return total


nums = [1, 2, 3]
answer = solve(nums)
print(answer)
```

它把：

```text
输入准备
↓
算法处理
↓
最终输出
```

分开了。

第 04 章进入 ACM 后，会进一步变成：

```python
def solve():
    # 读输入
    # 算
    # print
    pass


if __name__ == "__main__":
    solve()
```

现在暂时不用背 `__name__`。

---

## 14. Hot100：移动零的第二种写法

上一章用了额外 `result`。

现在先尝试一种“先收集非零，再覆盖原数组”的写法：

```python
def move_zeroes(nums):
    non_zero = []

    for x in nums:
        if x != 0:
            non_zero.append(x)

    k = len(non_zero)

    for i in range(k):
        nums[i] = non_zero[i]

    for i in range(k, len(nums)):
        nums[i] = 0
```

它已经满足“最终修改 `nums`”。

但是我们仍然创建了 `non_zero`。

第 06 章会问：

> 其实 `nums` 自己已经有足够的位置，能不能只用几个下标完成？

那才进入双指针。

---

## 15. Hot100：字母异位词分组为什么和“构造 key”有关

`49. 字母异位词分组` 的核心不是背某段代码，而是先理解：

```text
"eat"
"tea"

虽然顺序不同，
但它们可以得到同一个“标准形式”
```

一种容易理解的做法是把排序后的字符串作为特征：

```python
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
groups = {}

for word in words:
    key = "".join(sorted(word))

    if key not in groups:
        groups[key] = []

    groups[key].append(word)

print(list(groups.values()))
```

这里只需要理解：

```text
原字符串
↓
构造一个能代表这一组的 key
↓
dict[key]
↓
把属于同一 key 的字符串放在一起
```

以后你会看到“字母频次作为 key”等优化，但不是现在的目标。

---

## 16. 复杂度第一次入门：先问“随着 n 变大，做了多少次”

暂时不用背复杂符号大全。

### 一个循环

```python
for x in nums:
    print(x)
```

如果 `nums` 有 `n` 个元素，大约做 `n` 次，记作 `O(n)`。

### 两层循环

```python
for i in range(n):
    for j in range(n):
        ...
```

大约是：

```text
n × n
= n²
= O(n²)
```

### dict / set 查询

平均情况下：

```python
x in seen
```

可以把它理解成接近 `O(1)`。

所以“两数之和”才可能从两层循环的 `O(n²)` 变为一次遍历的平均 `O(n)`。

完整复杂度与数据结构成本在第 05 章展开。

---

## 17. 常见初学错误

### 错误 1：把下标和值混在一起

```python
for i in nums:
    print(nums[i])
```

这里 `i` 是元素值，不一定是合法下标。

如果想按下标：

```python
for i in range(len(nums)):
    print(nums[i])
```

如果只想要值：

```python
for x in nums:
    print(x)
```

### 错误 2：边遍历边随意删除

```python
for x in nums:
    if x == 0:
        nums.remove(x)
```

容器长度和位置同时变化，很容易跳过元素。

先构造新结果通常更容易理解。

### 错误 3：忘记 return

```python
def add(a, b):
    result = a + b
```

调用后得到 `None`。

### 错误 4：把 `.sort()` 的返回值当成排序结果

```python
nums = [3, 1, 2]
result = nums.sort()

print(result)
```

得到 `None`。

---

## 18. 本章练习

### 练习 1：统计每个数字出现次数

```python
nums = [1, 2, 1, 3, 2, 1]
```

<details>
<summary>参考答案</summary>

```python
count = {}

for x in nums:
    count[x] = count.get(x, 0) + 1

print(count)
```

</details>

### 练习 2：去重但保留第一次出现顺序

<details>
<summary>参考答案</summary>

```python
nums = [3, 1, 3, 2, 1, 4]

seen = set()
result = []

for x in nums:
    if x not in seen:
        seen.add(x)
        result.append(x)

print(result)
```

</details>

### 练习 3：独立重写“两数之和”

要求：关掉本章代码，只保留一句提示：

> 对当前 `x`，需要的是 `target - x`。

<details>
<summary>参考答案</summary>

```python
def two_sum(nums, target):
    seen = {}

    for i, x in enumerate(nums):
        need = target - x

        if need in seen:
            return [seen[need], i]

        seen[x] = i
```

</details>

### 练习 4：把所有非零元素放到新列表，再补零

不要看 `283. 移动零` 的最优题解。

<details>
<summary>参考答案</summary>

```python
def move_zeroes_simple(nums):
    result = []

    for x in nums:
        if x != 0:
            result.append(x)

    while len(result) < len(nums):
        result.append(0)

    return result
```

</details>

---

## 19. 本章 Exit Gate

你应该能在不查语法的情况下完成：

- 创建、访问、修改一个 list；
- 正确区分“遍历值”和“遍历下标”；
- 用 dict 做计数；
- 用 dict 记录某个值对应的位置；
- 用 set 判断是否出现过；
- 遍历字符串；
- 解释 `enumerate` 的两个结果分别是什么；
- 解释 `sorted(nums)` 和 `nums.sort()` 的区别；
- 写一个接收 list 并 `return` 结果的函数；
- 从暴力两数之和解释为什么 dict 可以减少重复搜索；
- 说出一层循环和两层循环最基本的复杂度区别。

如果这些操作仍然需要频繁复制模板，下一章的基础小题就是专门解决这个问题的。

---

下一章：[03. Basic Coding Exercises](03-basic-exercises.md)
