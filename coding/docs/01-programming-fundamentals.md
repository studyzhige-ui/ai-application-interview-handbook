# 01｜Programming Fundamentals：先理解“程序在发生什么”

[← Coding 首页](../README.md) · [下一章：Python Coding Basics →](02-python-coding-basics.md)

> 本章不假设你已经会编程。目标不是背 Python 语法，而是先建立一条最基础的执行模型：**代码从哪里开始、每一行改变了什么、数据从哪里来、结果到哪里去、出错时怎么看。**

---

## 1. 先把“代码”和“程序”分开

一个 Python 文件可以写：

```python
x = 2
y = 3
answer = x + y
print(answer)
```

你看到的是四行**源代码**。

当 Python 解释器执行它时，才变成一次真实的**程序运行**：

```text
第 1 行：让名字 x 指向整数 2
第 2 行：让名字 y 指向整数 3
第 3 行：读取 x 和 y 的值，计算 2 + 3，让 answer 指向 5
第 4 行：把 5 输出到标准输出
```

初学时最重要的习惯不是“看起来我懂了”，而是能逐行回答：

1. 这一行读了哪些值？
2. 做了什么计算或调用？
3. 哪个变量发生了变化？
4. 有没有产生输出？
5. 下一行执行前，当前状态是什么？

---

## 2. 表达式、赋值和函数调用

先看：

```python
2 + 3
```

它会产生一个值 `5`。这种“计算后产生值”的东西可以先理解成**表达式**。

再看：

```python
x = 2 + 3
```

右边先计算出 `5`，然后把名字 `x` 绑定到这个值。

再看：

```python
print(x)
```

这里调用了函数 `print`。

可以先形成这个简单模型：

```text
表达式
→ 得到值

赋值
→ 把名字和一个值关联起来

函数调用
→ 把输入交给一个已经定义好的操作
→ 它可能返回结果，也可能产生副作用，例如打印
```

更完整的 Python 对象模型在 [Python Foundation 01](../../python/docs/01-python基础与对象模型.md) 学；这里先确保你能追踪程序。

---

## 3. 变量不是“装数字的盒子”

初学教材经常把变量说成盒子。这个比喻能入门，但很快会产生误解。

先把变量理解成：

> **一个名字，当前关联到某个对象。**

```python
x = 10
x = 20
```

可以先画成：

```text
执行 x = 10 后
x → 10

执行 x = 20 后
x → 20
```

为什么这个区别以后重要？因为：

```python
a = [1, 2]
b = a
b.append(3)

print(a)
```

输出也是：

```text
[1, 2, 3]
```

这里 `a` 和 `b` 可以指向同一个 list 对象。完整的“引用、可变对象、对象身份”放在 Python 模块里，本章只先建立：**变量名和对象不是一回事。**

---

## 4. 程序怎样获得输入

### 4.1 `input()` 读取一整行

运行：

```python
name = input()
print(name)
```

如果输入：

```text
Alice
```

那么 `name` 得到字符串：

```python
"Alice"
```

关键规则：

> **Python 的 `input()` 默认返回字符串。**

所以：

```python
age = input()
```

输入：

```text
18
```

此时 `age` 是字符串 `"18"`，不是整数 `18`。

### 4.2 为什么经常看到 `int(input())`

如果想参与数字计算：

```python
age = int(input())
print(age + 1)
```

过程是：

```text
input()
→ "18"

int("18")
→ 18

18 + 1
→ 19
```

以后遇到很长的一行：

```python
nums = list(map(int, input().split()))
```

不要背。第 02、04 章会逐层拆开。

---

## 5. 输出：`print` 和 `return` 不是一回事

```python
print(3 + 4)
```

把 `7` 打印到输出。

但函数：

```python
def add(a, b):
    return a + b
```

这里 `return` 的意思不是“打印”。

```python
result = add(3, 4)
print(result)
```

调用过程：

```text
add(3, 4)
→ return 7
→ result = 7
→ print(result)
→ 屏幕出现 7
```

记住：

```text
return
→ 把结果交回调用者

print
→ 把内容输出给人或评测系统
```

LeetCode 经常要求 `return`；ACM 笔试最终通常要求 `print`。后面会专门比较。

---

## 6. 布尔值和条件判断

程序为什么需要 `if`？

因为同一段程序需要对不同情况做不同操作。

```python
age = 20

if age >= 18:
    print("adult")
else:
    print("minor")
```

先算：

```python
age >= 18
```

结果是 `True`，于是进入 `if`。

如果是：

```python
age = 16
```

则比较结果是 `False`，执行 `else`。

你可以把 `if` 理解成：

```text
先得到一个 True / False
        ↓
True  → 走 if 分支
False → 跳过 if，可能进入 elif / else
```

---

## 7. 循环：为什么需要重复执行

假设要打印 1 到 5：

```python
print(1)
print(2)
print(3)
print(4)
print(5)
```

可以运行，但没有可扩展性。

### 7.1 `for`

```python
for x in [1, 2, 3, 4, 5]:
    print(x)
```

可以理解成：

```text
第一次：x = 1
第二次：x = 2
第三次：x = 3
第四次：x = 4
第五次：x = 5
结束
```

### 7.2 `range`

```python
for i in range(5):
    print(i)
```

会输出：

```text
0
1
2
3
4
```

`range(5)` 不是 1 到 5，而是从 `0` 开始到 `5` 之前。

### 7.3 `while`

```python
x = 1

while x <= 5:
    print(x)
    x += 1
```

`while` 的核心是：

```text
条件为 True
→ 执行循环体
→ 再次判断
→ ...
→ 条件变 False
→ 停止
```

如果循环体永远不能让条件变 False，就可能出现死循环。

---

## 8. 用“变量追踪表”读循环

先不要靠脑补。

```python
nums = [3, 1, 4]
total = 0

for x in nums:
    total += x

print(total)
```

手工写表：

| 轮次 | x | 执行前 total | 执行后 total |
|---:|---:|---:|---:|
| 1 | 3 | 0 | 3 |
| 2 | 1 | 3 | 4 |
| 3 | 4 | 4 | 8 |

最后输出 `8`。

这就是以后理解双指针、动态规划之前必须具备的基本功：

> **你能准确说明每一轮状态怎么变化。**

---

## 9. 函数：把一个小任务命名

如果多次求和：

```python
def add(a, b):
    result = a + b
    return result

x = add(2, 3)
y = add(10, 20)

print(x)
print(y)
```

函数至少有四个概念：

```text
def
→ 定义函数

a, b
→ 参数

add(2, 3)
→ 调用函数

return
→ 把结果交回调用位置
```

以后算法题里很常见：

```python
def solve(nums):
    ...
    return answer
```

先把算法放进 `solve`，输入输出放在外面，是非常好的习惯。

---

## 10. 第一次 Hot100 预览：移动零

现在还不讲最优双指针。

只用当前已经会的：

- list；
- for；
- if；
- append；
- while。

目标可以简化理解为：

> 给一组数字，把非零数字的相对顺序保留下来，零放到末尾。

例如：

```python
nums = [0, 1, 0, 3, 12]

result = []

for x in nums:
    if x != 0:
        result.append(x)

while len(result) < len(nums):
    result.append(0)

print(result)
```

输出：

```text
[1, 3, 12, 0, 0]
```

这里先不讨论：

- 为什么原题要求原地修改；
- 怎么做到 O(1) 额外空间；
- 双指针是什么。

当前目标只有：

> **能逐行解释这段程序怎样把输入状态变成输出状态。**

等到第 06 章，我们再回来优化 `283. 移动零`。

---

## 11. 第二个 Hot100 预览：两数之和的暴力思路

给：

```python
nums = [2, 7, 11, 15]
target = 9
```

最直接的想法不是“哈希表”，而是：

> 把每一对都试一遍。

```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            print(i, j)
```

你现在只需要看懂：

```text
外层固定一个 i
        ↓
内层尝试 i 后面的每一个 j
        ↓
如果两个数之和等于 target
        ↓
输出两个下标
```

之后学习 dict 时再问：

> “为什么一定要两两试？我真正需要快速知道的是什么？”

那时才自然进入哈希优化。

---

## 12. 错误不是“代码坏了”，而是信息

### 12.1 SyntaxError：语法都无法解析

```python
if x > 3
    print(x)
```

少了 `:`。

### 12.2 NameError：用了不存在的名字

```python
print(score)
```

但从未定义 `score`。

### 12.3 TypeError：操作和数据类型不匹配

```python
age = "18"
print(age + 1)
```

字符串和整数不能这样直接相加。

### 12.4 IndexError：列表下标越界

```python
nums = [10, 20]
print(nums[2])
```

合法下标只有 `0` 和 `1`。

---

## 13. Traceback 怎么读

遇到报错：

```text
Traceback (most recent call last):
  File "main.py", line 4, in <module>
    print(nums[3])
IndexError: list index out of range
```

不要只看红色。

最先抓三个信息：

```text
1. 哪个文件？
main.py

2. 哪一行？
line 4

3. 什么异常？
IndexError: list index out of range
```

然后回到那一行，问：

> 当前 `nums` 到底多长？这个下标为什么会出现？

Debug 的基本动作不是“随机改代码”，而是**恢复出错那一刻的真实状态**。

---

## 14. 本章小练习

先自己写，再展开参考答案。

### 练习 1：读入一个整数，输出它的平方

<details>
<summary>参考答案</summary>

```python
n = int(input())
print(n * n)
```

</details>

### 练习 2：给定列表，计算所有偶数之和

```python
nums = [1, 2, 3, 4, 5, 6]
```

<details>
<summary>参考答案</summary>

```python
nums = [1, 2, 3, 4, 5, 6]

total = 0

for x in nums:
    if x % 2 == 0:
        total += x

print(total)
```

</details>

### 练习 3：不用 `max()`，自己找最大值

```python
nums = [4, 2, 9, 1, 7]
```

<details>
<summary>参考答案</summary>

```python
nums = [4, 2, 9, 1, 7]

best = nums[0]

for x in nums:
    if x > best:
        best = x

print(best)
```

</details>

### 练习 4：给定字符串，统计字母 `a` 出现多少次

<details>
<summary>参考答案</summary>

```python
s = "abracadabra"

count = 0

for ch in s:
    if ch == "a":
        count += 1

print(count)
```

</details>

---

## 15. 本章 Exit Gate

先不要看答案，确认自己能做到：

- 能解释 Python 文件大致怎样从上到下执行；
- 知道 `input()` 默认返回 `str`；
- 知道 `print` 和 `return` 的区别；
- 能解释 `if` 判断的是一个真假条件；
- 能逐轮追踪 `for` / `while` 中变量变化；
- 能自己写一个求和、计数、最大值的小程序；
- 遇到 traceback 时先找文件、行号、异常类型；
- 能看懂“移动零”的基础版本；
- 能看懂“两数之和”的两层循环暴力版本。

如果其中任何一项仍需要靠背代码完成，就先继续写小程序，不急着进入算法模板。

---

下一章：[02. Python Coding Basics](02-python-coding-basics.md)
