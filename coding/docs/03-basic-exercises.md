# 03｜Basic Coding Exercises：从“看得懂”到“不给模板也能写”

[← 上一章：Python Coding Basics](02-python-coding-basics.md) · [Coding 首页](../README.md) · [下一章：ACM Input / Output →](04-acm-input-output.md)

> 这一章不是为了多刷题，而是解决一个很具体的问题：**为什么示例代码一看就懂，关掉答案以后却不知道第一行写什么？**

---

## 1. “会看”和“会写”之间差了什么

阅读代码时，很多决策已经替你做完了：

```text
变量叫什么
循环遍历什么
什么时候判断
结果放哪里
什么时候 return
```

空白文件没有这些提示。

所以基础 Coding 练习不能只做：

```text
看题
→ 看答案
→ 觉得懂了
```

而要重复：

```text
理解任务
→ 自己给数据命名
→ 先写最笨但正确的步骤
→ 运行
→ 看错误
→ 修改
→ 关掉答案重写
```

这一章只练“把很小的问题完整写出来”。

---

## 2. 每道基础题统一用四句话拆

拿到题先不写代码，先说：

```text
输入是什么？
输出是什么？
我要重复做什么？
我要保存什么状态？
```

例如“统计数组中偶数个数”：

```text
输入：一组整数 nums
输出：偶数的数量

重复：
逐个查看 nums 中的 x

状态：
count，表示目前发现多少个偶数
```

于是代码自然出现：

```python
count = 0

for x in nums:
    if x % 2 == 0:
        count += 1
```

这比先想“应该套哪个模板”可靠。

---

# 3. 第一组：循环、判断、累积

这些题没有算法技巧，目标只是把最基础动作写熟。

## 3.1 求和

给：

```python
nums = [3, 5, 2, 7]
```

不用 `sum()`，求总和。

<details>
<summary>参考答案</summary>

```python
total = 0

for x in nums:
    total += x

print(total)
```

</details>

## 3.2 计数

统计正数数量：

```python
nums = [-2, 0, 5, 3, -1]
```

<details>
<summary>参考答案</summary>

```python
count = 0

for x in nums:
    if x > 0:
        count += 1

print(count)
```

</details>

## 3.3 最大值

不用 `max()`。

<details>
<summary>参考答案</summary>

```python
nums = [4, 9, 2, 8]

best = nums[0]

for x in nums:
    if x > best:
        best = x

print(best)
```

</details>

这里第一次遇到一个重要边界：

> 如果 `nums = []` 呢？

`nums[0]` 会报错。

以后算法题必须先看题目是否保证数组非空，而不是默认所有输入都“刚刚好”。

---

# 4. 第二组：构造一个新结果

## 4.1 过滤

把所有偶数放进新列表：

<details>
<summary>参考答案</summary>

```python
nums = [1, 2, 3, 4, 5, 6]

result = []

for x in nums:
    if x % 2 == 0:
        result.append(x)

print(result)
```

</details>

## 4.2 每个元素做转换

把每个数字平方：

<details>
<summary>参考答案</summary>

```python
nums = [1, 2, 3]

result = []

for x in nums:
    result.append(x * x)

print(result)
```

</details>

## 4.3 反转字符串

先允许用切片：

```python
s = "hello"
answer = s[::-1]
```

然后再手写：

<details>
<summary>参考答案</summary>

```python
s = "hello"

result = ""

for ch in s:
    result = ch + result

print(result)
```

</details>

这个版本不是最高效的工程写法，目的只是训练“每一步结果怎样变化”。

---

# 5. 第三组：dict / set

## 5.1 频次统计

```python
nums = [1, 2, 1, 3, 2, 1]
```

输出每个数字出现次数。

<details>
<summary>参考答案</summary>

```python
count = {}

for x in nums:
    count[x] = count.get(x, 0) + 1

print(count)
```

</details>

## 5.2 第一个重复元素

按从左到右的顺序，找到第一个“之前已经出现过”的值。

<details>
<summary>参考答案</summary>

```python
nums = [3, 1, 4, 1, 5]

seen = set()
answer = None

for x in nums:
    if x in seen:
        answer = x
        break

    seen.add(x)

print(answer)
```

</details>

这里开始出现 `break`：

> `break` = 立即结束当前循环。

---

# 6. 第四组：索引

## 6.1 找目标值第一次出现的位置

```python
nums = [8, 3, 7, 3]
target = 3
```

<details>
<summary>参考答案</summary>

```python
answer = -1

for i, x in enumerate(nums):
    if x == target:
        answer = i
        break

print(answer)
```

</details>

这里 `-1` 是人为约定的“没找到”。

题目如果另有要求，就按题目输出。

## 6.2 相邻元素比较

找出相邻两个元素之差最大的值。

<details>
<summary>参考答案</summary>

```python
nums = [2, 8, 5, 12]

best = 0

for i in range(1, len(nums)):
    diff = abs(nums[i] - nums[i - 1])

    if diff > best:
        best = diff

print(best)
```

</details>

注意为什么从 `1` 开始：

```text
当前 i
需要访问 i - 1

如果 i = 0
→ i - 1 = -1
→ 在 Python 里反而会访问最后一个元素
```

这种“代码能跑但逻辑错”的 Bug 比直接报错更需要警惕。

---

# 7. 第五组：函数化

不要永远把所有代码写在最外层。

## 7.1 判断回文

```python
def is_palindrome(s):
    ...
```

例如 `"level"` 返回 `True`。

<details>
<summary>参考答案</summary>

```python
def is_palindrome(s):
    left = 0
    right = len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False

        left += 1
        right -= 1

    return True
```

</details>

这是第一次自然看到“两边向中间走”的两个下标。

先理解过程，不急着给它贴“双指针模板”标签。

---

# 8. Hot100 Bridge 1：两数之和

这道题已经出现三次：

```text
01：
看懂两层循环

02：
理解 dict 优化

03：
现在要求关掉答案独立写
```

练习要求：

1. 先写 `O(n²)` 暴力版本；
2. 说出它为什么慢；
3. 再写 dict 版本；
4. 手工追踪 `seen` 每一轮是什么。

不要只提交最优解。

你真正要练的是：

```text
正确解
→ 看见瓶颈
→ 优化
```

---

# 9. Hot100 Bridge 2：移动零

同样先不要追求一次写出最优版。

## Level 1：额外列表

```text
遍历 nums
→ 收集非零
→ 补 0
```

## Level 2：覆盖原数组

```text
先把所有非零依次写回前面
→ 剩余位置填 0
```

## Level 3：双指针

留到第 06 章正式推导。

如果你 Level 1 都不能稳定从空白写出，强行背 Level 3 只会制造“会背答案”的错觉。

---

# 10. Hot100 Bridge 3：只出现一次的数字

`136. 只出现一次的数字` 最经典的最优解会用异或。

但现在如果你还没学位运算，不要为了 Hot100 强塞 XOR。

可以先用计数理解问题：

```python
def single_number_basic(nums):
    count = {}

    for x in nums:
        count[x] = count.get(x, 0) + 1

    for x, freq in count.items():
        if freq == 1:
            return x
```

到第 07 章技巧专题再学习：

```text
x ^ x = 0
x ^ 0 = x
```

这就是本课程“Hot100 优先，但不强行提前知识”的具体规则。

---

# 11. 学会自己制造测试

写完函数，不要只测试一个漂亮样例。

以“判断回文”为例：

```python
print(is_palindrome("level"))  # True
print(is_palindrome("hello"))  # False
print(is_palindrome("a"))      # True
print(is_palindrome(""))       # True
```

测试至少考虑：

```text
普通情况
边界情况
最小输入
重复元素
全相同
可能为空
```

题目保证不可能出现的情况，不需要擅自改变题意；但要先读清楚约束。

---

# 12. Debug 训练：先预测，再运行

看下面代码：

```python
nums = [1, 2, 3]
total = 0

for i in range(len(nums) + 1):
    total += nums[i]

print(total)
```

不要马上运行。

先问：

```text
len(nums) = 3
range(4) 产生 0, 1, 2, 3

nums[3] 存在吗？
→ 不存在
```

因此会在最后一轮 `IndexError`。

Debug 的一个核心能力就是：

> 在运行前就能模拟出关键状态。

---

# 13. 从今天开始记录“错误类型”，不是抄整份答案

推荐 Error Log 只记：

```text
题目 / 任务：
我错在哪里：
为什么会错：
下次看到什么信号要警觉：
```

例如：

```text
任务：相邻元素最大差

错误：
for i in range(len(nums))，然后访问 nums[i - 1]

原因：
没有先定义“第一对相邻元素从索引 1 才开始”

警觉：
只要访问 i-1 / i+1，就先检查循环边界
```

这种记录比复制完整题解更有价值。

---

# 14. 本章练习清单

下面这些应该能从空白文件写出来：

| 类型 | 练习 |
|---|---|
| 累积 | 数组求和、偶数求和 |
| 计数 | 正数个数、字符频次 |
| 极值 | 最大值、最小值 |
| 构造 | 过滤偶数、平方列表 |
| 字符串 | 统计字符、回文判断 |
| set | 首个重复值、去重 |
| dict | 频次表、值到下标 |
| 索引 | 首次出现位置、相邻比较 |
| Hot100 | 两数之和基础版 / 哈希版 |
| Hot100 | 移动零 Level 1 / Level 2 |

如果这些仍然高度依赖复制，暂时不要用“刷更多 Hot100”解决。先把基本操作变成肌肉记忆。

---

## 15. Exit Gate

进入 ACM 之前，你应该：

- 能从空白文件创建 list / dict / set；
- 能写 `for`、`if`、`while`；
- 能正确使用索引并主动检查边界；
- 能自己设计 `total`、`count`、`best`、`result`、`seen` 这类状态变量；
- 能把小任务拆成函数；
- 能为一个函数写 3～4 个测试；
- 能独立写出两数之和的暴力版本；
- 能解释并重写 dict 版本；
- 能写出移动零的非最优基础版本；
- 知道有些 Hot100 技巧现在不学，是因为前置知识还没到，而不是“这题跳过”。

---

下一章：[04. ACM Input / Output](04-acm-input-output.md)
