# 03｜基础练习：读题、实现、测试、解释

[← 上一章：数据类型与容器](02-python-coding-basics.md) · [Coding 首页](../README.md) · [配套 Notebook](../exercises/03-basic-exercises.ipynb) · [下一章：输入输出 →](04-acm-input-output.md)

看示例时，每一行似乎都懂；关掉答案，光标停在空白文件里，却不知道第一行该写什么。这种落差很常见：**读代码时，别人已经替你选好了变量和步骤；自己写时，这些选择要由你来做。**

本章就是把这一步练出来。题目很小，不需要猜巧妙算法。你会先练累积与计数，再构造结果、记录历史、处理索引，最后把这些动作组合起来。一次只增加一点难度，先写出朴素但正确的程序，再考虑简洁。

## 1. 不知道第一行写什么，先把任务说成四句话

以“统计正数个数”为例，先回答四个问题：

1. **输入是什么？** 一组整数，例如 `[-2, 0, 5, 3, -1]`。
2. **输出是什么？** 正数的数量，本例是 2。
3. **重复做什么？** 从左到右检查每个数是否大于 0。
4. **记住什么？** 已经发现的正数个数。

因此需要一个变量 `count` 保存数量。还没开始检查时，数量为 0。每发现一个正数，数量增加 1。

> ⚠️ “统计个数”更新的是 `count += 1`，不是 `count += x`。后者是在求和。先把输出的含义分清，更新语句才不会选错。

本章题目都用函数接收数据、返回结果。函数本身已经学过，你要练的是如何决定函数体里的步骤，而不是同时学习新的函数技巧。

## 2. 怎样使用题目、编写区和测试

每题按这个顺序练习：

1. 读任务和边界，确认返回什么、是否修改输入。
2. 手算给定样例，写下关键变量应该怎样变化。
3. 在编写区完成函数。
4. 运行测试，比较实际结果和预期结果。
5. 需要时展开答案，理解后关掉答案重写。

`pass` 是让空函数具有合法语法的占位语句。把它替换成自己的实现，才是在完成题目。

测试里的 `assert` 是可以由程序检查的预期。如果预期返回 6，实际得到 `None`，先检查自己的函数有没有执行 `return`。

> ⚠️ 空白函数不能通过测试，是预期情况，不表示练习文件损坏。实现后仍失败，应调查原因，不要为了通过而修改题目预期。

[配套 Notebook](../exercises/03-basic-exercises.ipynb)中，每题由四个相邻单元组成：题目、编写区、测试、折叠答案。

运行时先执行自己的函数定义，再执行测试。

> ⚠️ 修改代码后，要重新运行函数定义单元。否则测试可能仍在调用内核里保存的旧函数。状态不确定时，重启 Python 3 内核，再按顺序执行。

答案是默认折叠的文字，不会在“运行全部”时自动完成题目。需要帮助时先想清卡在何处，再展开；看完后关掉答案重写。GitHub 提供静态预览，实际运行使用 JupyterLab 等 Notebook 环境。

## 3. 练习主线

**第一组：让一个变量记住已经处理的结果**

E01–E05 先不构造复杂容器，只练“总和、数量、最好或最小的值”。每题先用一句话解释状态，初始化和更新就更容易决定。

<!-- exercise:E01 -->
### E01｜数组求和

**任务与边界：**

返回整数列表 `nums` 的总和。

不使用 `sum()`。空列表返回 0。

**给定样例与预期：**

- 输入：`nums = [3, 5, 2, 7]`。
- 预期：`17`。

**编写区（待完成）：**

<!-- starter -->
```python
def array_sum(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert array_sum([3, 5, 2, 7]) == 17
assert array_sum([]) == 0
assert array_sum([-2, 2]) == 0
```

<details>
<summary>查看 E01 参考答案与解释</summary>

<!-- solution -->
```python
def array_sum(nums):
    total = 0
    for x in nums:
        total += x
    return total
```

`total` 保存已经处理部分的和。处理 3、5、2、7 后，它依次变成 3、8、10、17。

> ⚠️ 初始化和 `return` 都在循环外。每轮重新初始化会丢掉旧结果，循环内直接返回则可能只处理第一项。

</details>
<!-- /exercise -->

<!-- exercise:E02 -->
### E02｜偶数求和

**任务与边界：**

只累加整数列表中的偶数，返回总和。

0 和负偶数也属于偶数。没有偶数时返回 0。

**给定样例与预期：**

- 输入：`nums = [1, 2, 3, 4]`。
- 预期：`6`。

**编写区（待完成）：**

<!-- starter -->
```python
def even_sum(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert even_sum([1, 2, 3, 4]) == 6
assert even_sum([-2, 0, 3]) == -2
assert even_sum([]) == 0
```

<details>
<summary>查看 E02 参考答案与解释</summary>

<!-- solution -->
```python
def even_sum(nums):
    total = 0
    for x in nums:
        if x % 2 == 0:
            total += x
    return total
```

每轮先判断 `x % 2 == 0`。为真时，把当前数 `x` 加到 `total`；为假时，不更新总和。

本例只有 2 和 4 被累加，所以返回 6。这里求的是偶数之和，不是偶数个数。

</details>
<!-- /exercise -->

<!-- exercise:E03 -->
### E03｜正数个数

**任务与边界：**

返回整数列表中正数的个数。

只统计严格大于 0 的元素。0 不算正数，空列表返回 0。

**给定样例与预期：**

- 输入：`nums = [-2, 0, 5, 3, -1]`。
- 预期：`2`。

**编写区（待完成）：**

<!-- starter -->
```python
def positive_count(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert positive_count([-2, 0, 5, 3, -1]) == 2
assert positive_count([0, -1]) == 0
assert positive_count([]) == 0
```

<details>
<summary>查看 E03 参考答案与解释</summary>

<!-- solution -->
```python
def positive_count(nums):
    count = 0
    for x in nums:
        if x > 0:
            count += 1
    return count
```

本例只有 5 和 3 大于 0。遇到它们时，各让 `count` 增加一次，最后得到 2。

> ⚠️ 每次加的是 1，不是元素值。`count += x` 会得到正数之和 8，不符合题意。

</details>
<!-- /exercise -->

<!-- exercise:E04 -->
### E04｜最大值

**任务与边界：**

返回非空整数列表中的最大值。

不使用 `max()`。题目保证列表非空，不需要定义空列表的返回值。

**给定样例与预期：**

- 输入：`nums = [4, 9, 2, 8]`。
- 预期：`9`。

**编写区（待完成）：**

<!-- starter -->
```python
def largest(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert largest([4, 9, 2, 8]) == 9
assert largest([-5, -2, -8]) == -2
assert largest([7]) == 7
```

<details>
<summary>查看 E04 参考答案与解释</summary>

<!-- solution -->
```python
def largest(nums):
    best = nums[0]
    for x in nums:
        if x > best:
            best = x
    return best
```

1. 先用第一项 4 初始化 `best`。
2. 遇到 9，比 4 大，更新 `best = 9`。
3. 后面的 2 和 8 都没有更大，`best` 保持 9。

> ⚠️ 不要随手初始化成 `best = 0`。输入全是负数时，0 并不在列表里，却会被错误地保留为最大值。

</details>
<!-- /exercise -->

<!-- exercise:E05 -->
### E05｜最小值

**任务与边界：**

返回非空整数列表中的最小值。

不使用 `min()`。题目保证列表非空。

**给定样例与预期：**

- 输入：`nums = [4, 9, 2, 8]`。
- 预期：`2`。

**编写区（待完成）：**

<!-- starter -->
```python
def smallest(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert smallest([4, 9, 2, 8]) == 2
assert smallest([5, 2, 8]) == 2
assert smallest([-7]) == -7
```

<details>
<summary>查看 E05 参考答案与解释</summary>

<!-- solution -->
```python
def smallest(nums):
    best = nums[0]
    for x in nums:
        if x < best:
            best = x
    return best
```

`best` 从第一项 4 开始。遇到 9 不更新，遇到 2 更新成 2，遇到 8 仍保持 2。

与求最大值相比，状态仍表示已处理部分的极值，只是比较条件改成 `x < best`。

</details>
<!-- /exercise -->

**第二组：不只算一个数，还要逐步构造结果**

E06–E08 把注意力从 total 移到 result。处理一个元素后，结果里应该多出什么？原输入是否需要保留？先把这两个问题说清楚。

<!-- exercise:E06 -->
### E06｜过滤偶数

**任务与边界：**

构造只包含偶数的新列表并返回。

保持原有顺序和重复次数，不修改原列表。空列表返回空列表。

**给定样例与预期：**

- 输入：`nums = [1, 2, 3, 4, 5, 6]`。
- 预期：`[2, 4, 6]`。

**编写区（待完成）：**

<!-- starter -->
```python
def filter_even(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
source = [1, 2, 3, 4, 5, 6]
assert filter_even(source) == [2, 4, 6]
assert source == [1, 2, 3, 4, 5, 6]
assert filter_even([2, 2, -4]) == [2, 2, -4]
assert filter_even([]) == []
```

<details>
<summary>查看 E06 参考答案与解释</summary>

<!-- solution -->
```python
def filter_even(nums):
    result = []
    for x in nums:
        if x % 2 == 0:
            result.append(x)
    return result
```

依次检查每个元素，只在它为偶数时追加到 `result`。原列表不被修改，追加顺序也就保留了原顺序。

> ⚠️ 不能用集合代替结果列表。本题要求保留重复次数，集合会丢失这部分信息。

</details>
<!-- /exercise -->

<!-- exercise:E07 -->
### E07｜平方列表

**任务与边界：**

返回一个新列表，其中每项是原元素的平方。

保留顺序，不修改原输入。空列表返回空列表。

**给定样例与预期：**

- 输入：`nums = [1, 2, 3]`。
- 预期：`[1, 4, 9]`。

**编写区（待完成）：**

<!-- starter -->
```python
def squared(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
source = [1, 2, 3]
assert squared(source) == [1, 4, 9]
assert source == [1, 2, 3]
assert squared([-2, 0]) == [4, 0]
assert squared([]) == []
```

<details>
<summary>查看 E07 参考答案与解释</summary>

<!-- solution -->
```python
def squared(nums):
    result = []
    for x in nums:
        result.append(x * x)
    return result
```

这题不是筛选：每一项都要参与转换，所以不需要 `if`。

每轮计算 `x * x`，然后追加到新列表。能解释普通循环后，可以尝试改写为列表推导式。

</details>
<!-- /exercise -->

<!-- exercise:E08 -->
### E08｜反转字符串

**任务与边界：**

返回字符串的倒序结果。

先写切片版，再写循环版。空字符串返回空字符串。

**给定样例与预期：**

- 输入：`s = "hello"`。
- 预期：`"olleh"`。

**编写区（待完成）：**

<!-- starter -->
```python
def reverse_text(s):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert reverse_text("hello") == "olleh"
assert reverse_text("") == ""
assert reverse_text("a") == "a"
```

<details>
<summary>查看 E08 参考答案与解释</summary>

<!-- solution -->
```python
def reverse_text(s):
    result = ""
    for ch in s:
        result = ch + result
    return result
```

循环把当前字符放到已有结果前面，因此结果依次是 `h`、`eh`、`leh`、`lleh`、`olleh`。切片版直接写 `return s[::-1]`。

> ⚠️ 这个循环用于练习状态追踪。长字符串反复在前面拼接，会重复复制已有内容；实际处理较长文本时，应考虑先收集字符再连接。

</details>
<!-- /exercise -->

**第三组：记住历史，再查询它**

E09–E14 开始用已处理的信息帮助后续判断。先区分任务要问什么：

- 出现过吗？只需保存成员。
- 出现几次？需要保存次数。
- 出现在哪里？需要保存下标。

需要保存的信息不同，状态的含义和更新方式也不同。

<!-- exercise:E09 -->
### E09｜字符频次

**任务与边界：**

返回一个字典，记录每个字符出现的次数。

空格参与统计，区分大小写。空字符串返回空字典。

**给定样例与预期：**

- 输入：`s = "banana"`。
- 预期：`{"b": 1, "a": 3, "n": 2}`。

**编写区（待完成）：**

<!-- starter -->
```python
def char_counts(s):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert char_counts("banana") == {"b": 1, "a": 3, "n": 2}
assert char_counts("a A") == {"a": 1, " ": 1, "A": 1}
assert char_counts("") == {}
```

<details>
<summary>查看 E09 参考答案与解释</summary>

<!-- solution -->
```python
def char_counts(s):
    count = {}
    for ch in s:
        count[ch] = count.get(ch, 0) + 1
    return count
```

每次读到字符，都执行“读旧次数、加一、写回”。第一次遇到字符时，旧次数按 0 处理。

> ⚠️ 空格和大小写也是本题输入的一部分。不要自行删除空格或转换大小写，否则改变了统计对象。

</details>
<!-- /exercise -->

<!-- exercise:E10 -->
### E10｜数字频次

**任务与边界：**

返回一个字典，记录每个整数出现的次数。

不使用 `Counter`。空列表返回空字典。

**给定样例与预期：**

- 输入：`nums = [1, 2, 1, 3, 2, 1]`。
- 预期：`{1: 3, 2: 2, 3: 1}`。

**编写区（待完成）：**

<!-- starter -->
```python
def number_counts(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert number_counts([1, 2, 1, 3, 2, 1]) == {1: 3, 2: 2, 3: 1}
assert number_counts([-1, -1, 0]) == {-1: 2, 0: 1}
assert number_counts([]) == {}
```

<details>
<summary>查看 E10 参考答案与解释</summary>

<!-- solution -->
```python
def number_counts(nums):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    return count
```

字典的键是数字，值是出现次数。三次读到 1 时，`count[1]` 依次变成 1、2、3。

字符计数和数字计数使用相同的更新过程，只是键的类型不同。

</details>
<!-- /exercise -->

<!-- exercise:E11 -->
### E11｜第一个再次遇到的值

**任务与边界：**

从左到右扫描，返回最先被第二次遇到的整数。

不存在重复时返回 `None`。不是找“第一次出现位置最靠前的重复值”。

**给定样例与预期：**

- 输入：`nums = [3, 1, 4, 1, 5]`。
- 预期：`1`。

**编写区（待完成）：**

<!-- starter -->
```python
def first_repeat(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert first_repeat([3, 1, 4, 1, 5]) == 1
assert first_repeat([2, 1, 1, 2]) == 1
assert first_repeat([1, 2]) is None
assert first_repeat([]) is None
```

<details>
<summary>查看 E11 参考答案与解释</summary>

<!-- solution -->
```python
def first_repeat(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)
    return None
```

`seen` 只保存当前这一项之前见过的值。查询到当前值已经存在，就立即返回。

例如 `[2, 1, 1, 2]`：第三项 1 已经重复，因此返回 1。不能因为 2 在列表中出现得更早，就返回 2。

</details>
<!-- /exercise -->

<!-- exercise:E12 -->
### E12｜去重但保留首次顺序

**任务与边界：**

返回一个新列表，只保留每个值第一次出现的记录。

保留首次出现顺序，不修改输入。空列表返回空列表。

**给定样例与预期：**

- 输入：`nums = [3, 1, 3, 2, 1, 4]`。
- 预期：`[3, 1, 2, 4]`。

**编写区（待完成）：**

<!-- starter -->
```python
def unique_in_order(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
source = [3, 1, 3, 2, 1, 4]
assert unique_in_order(source) == [3, 1, 2, 4]
assert source == [3, 1, 3, 2, 1, 4]
assert unique_in_order([2, 2]) == [2]
assert unique_in_order([]) == []
```

<details>
<summary>查看 E12 参考答案与解释</summary>

<!-- solution -->
```python
def unique_in_order(nums):
    seen = set()
    result = []
    for x in nums:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result
```

两个容器各自保存不同的信息：

- `seen` 保存已经出现的值，用来判断重复。
- `result` 按首次遇到的顺序收集结果。

> ⚠️ 直接写 `list(set(nums))` 不保证保留首次出现顺序，不能替代本题的这两个步骤。

</details>
<!-- /exercise -->

<!-- exercise:E13 -->
### E13｜第一次出现的位置

**任务与边界：**

返回目标值 `target` 第一次出现的下标。

手写遍历，不使用 `index()`。没找到时返回 -1。

**给定样例与预期：**

- 输入：`nums = [8, 3, 7, 3]`，`target = 3`。
- 预期：`1`。

**编写区（待完成）：**

<!-- starter -->
```python
def first_index(nums, target):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert first_index([8, 3, 7, 3], 3) == 1
assert first_index([8, 3], 8) == 0
assert first_index([8, 3], 9) == -1
assert first_index([], 3) == -1
```

<details>
<summary>查看 E13 参考答案与解释</summary>

<!-- solution -->
```python
def first_index(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
```

`enumerate` 同时提供下标 `i` 和元素值 `x`。用 `x == target` 判断是否命中，命中后返回 `i`。

> ⚠️ -1 是本题约定的“未找到”标记。不能不检查结果就拿它继续索引列表，因为 `nums[-1]` 在 Python 中会读取最后一项。

</details>
<!-- /exercise -->

<!-- exercise:E14 -->
### E14｜相邻最大绝对差

**任务与边界：**

返回相邻两项之差的绝对值中的最大值。

少于两个元素时返回 0。只比较相邻项，不比较首尾。

**给定样例与预期：**

- 输入：`nums = [2, 8, 5, 12]`。
- 预期：`7`。

**编写区（待完成）：**

<!-- starter -->
```python
def max_adjacent_gap(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert max_adjacent_gap([2, 8, 5, 12]) == 7
assert max_adjacent_gap([9, 2]) == 7
assert max_adjacent_gap([7]) == 0
assert max_adjacent_gap([]) == 0
```

<details>
<summary>查看 E14 参考答案与解释</summary>

<!-- solution -->
```python
def max_adjacent_gap(nums):
    best = 0
    for i in range(1, len(nums)):
        diff = abs(nums[i] - nums[i - 1])
        if diff > best:
            best = diff
    return best
```

本例依次比较相邻的三对：2 与 8，8 与 5，5 与 12。绝对差分别是 6、3、7，所以答案为 7。

> ⚠️ 循环从 `i = 1` 开始，让 `i - 1` 和 `i` 组成第一对位置 0、1。从 0 开始会用到位置 -1，错误地比较首尾两项。

</details>
<!-- /exercise -->

**第四组：把基础动作组合成完整任务**

E15–E21 不需要突然换一套语法。回文、两数之和、移动零都由熟悉的判断、循环、查询和写回构成；难点是把状态与题目要求对应起来。

<!-- exercise:E15 -->
### E15｜回文判断

**任务与边界：**

判断字符串正读和反读是否相同，返回布尔值。

大小写和空格都参与比较。空字符串约定为回文，不要求最优空间。

**给定样例与预期：**

- 输入：`s = "level"`。
- 预期：`True`；`s = "hello"` 时返回 `False`。

**编写区（待完成）：**

<!-- starter -->
```python
def is_palindrome(s):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert is_palindrome("level") is True
assert is_palindrome("hello") is False
assert is_palindrome("a") is True
assert is_palindrome("") is True
assert is_palindrome("Aa") is False
```

<details>
<summary>查看 E15 参考答案与解释</summary>

<!-- solution -->
```python
def is_palindrome(s):
    return s == s[::-1]
```

`s[::-1]` 构造倒序字符串，再用 `s == s[::-1]` 比较两者是否相同。

本例 `level` 倒过来仍是 `level`，得到 `True`。空字符串倒过来也仍是空字符串，符合本题约定。

> ⚠️ 切片会构造反向副本。这题允许这样做，不能据此宣称额外空间是常数。

</details>
<!-- /exercise -->

<!-- exercise:E16 -->
### E16｜两数之和：暴力版

**任务与边界：**

返回两个不同下标，使对应数字之和等于 `target`。

有解时保证唯一，无解时返回 `[]`。只用两层循环。

**给定样例与预期：**

- 输入：`nums = [2, 7, 11, 15]`，`target = 9`。
- 预期：`[0, 1]`。

**编写区（待完成）：**

<!-- starter -->
```python
def two_sum_brute(nums, target):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert two_sum_brute([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_brute([3, 3], 6) == [0, 1]
assert two_sum_brute([3], 6) == []
assert two_sum_brute([], 0) == []
```

<details>
<summary>查看 E16 参考答案与解释</summary>

<!-- solution -->
```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

外层固定位置 `i`，内层让 `j` 依次取它后面的位置。找到满足条件的一对，就返回两个下标。

> ⚠️ `j` 从 `i + 1` 开始，才能避免同一位置与自己配对，也避免反向重复。这里返回的是下标，不是那两个数。

</details>
<!-- /exercise -->

<!-- exercise:E17 -->
### E17｜两数之和：字典版

**任务与边界：**

返回两个不同下标，使对应数字之和等于 `target`。

有解时保证唯一，无解时返回 `[]`。用字典保存历史，只扫描一次。

**给定样例与预期：**

- 输入：`nums = [2, 7, 11, 15]`，`target = 9`。
- 预期：`[0, 1]`。

**编写区（待完成）：**

<!-- starter -->
```python
def two_sum_hash(nums, target):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert two_sum_hash([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_hash([3, 3], 6) == [0, 1]
assert two_sum_hash([3], 6) == []
assert two_sum_hash([], 0) == []
```

<details>
<summary>查看 E17 参考答案与解释</summary>

<!-- solution -->
```python
def two_sum_hash(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []
```

每轮处理当前的 `x`：

1. 计算需要的另一个数 `need = target - x`。
2. 查询 `need` 是否在字典中，存在就返回它的历史下标和当前下标。
3. 没找到时，记录当前数字与下标，继续下一轮。

> ⚠️ 先查再记录。只有一个 3、目标为 6 时，没有两个不同位置，不能把同一项用两次。

</details>
<!-- /exercise -->

<!-- exercise:E18 -->
### E18｜移动零：返回新列表

**任务与边界：**

保持非零值的相对顺序，把零移到末尾，返回新列表。

原输入保持不变，允许空列表。

**给定样例与预期：**

- 输入：`nums = [0, 1, 0, 3, 12]`。
- 预期：`[1, 3, 12, 0, 0]`。

**编写区（待完成）：**

<!-- starter -->
```python
def move_zeroes_copy(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
source = [0, 1, 0, 3, 12]
assert move_zeroes_copy(source) == [1, 3, 12, 0, 0]
assert source == [0, 1, 0, 3, 12]
assert move_zeroes_copy([0, 0]) == [0, 0]
assert move_zeroes_copy([1, 2]) == [1, 2]
assert move_zeroes_copy([]) == []
```

<details>
<summary>查看 E18 参考答案与解释</summary>

<!-- solution -->
```python
def move_zeroes_copy(nums):
    result = []
    for x in nums:
        if x != 0:
            result.append(x)
    while len(result) < len(nums):
        result.append(0)
    return result
```

先收集得到 `[1, 3, 12]`，再补零直到长度等于输入，得到 `[1, 3, 12, 0, 0]`。

> ⚠️ 本题要求返回新列表。验证结果内容的同时，还要检查原列表没有变化。

</details>
<!-- /exercise -->

<!-- exercise:E19 -->
### E19｜移动零：覆盖原列表

**任务与边界：**

保持非零值的相对顺序，把零移到末尾，修改传入列表。

函数返回 `None`。允许使用额外列表，不要求常数空间，允许空列表。

**给定样例与预期：**

- 输入：`nums = [0, 1, 0, 3, 12]`。
- 预期：调用后 `nums` 为 `[1, 3, 12, 0, 0]`，调用结果为 `None`。

**编写区（待完成）：**

<!-- starter -->
```python
def move_zeroes_inplace(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
source = [0, 1, 0, 3, 12]
assert move_zeroes_inplace(source) is None
assert source == [1, 3, 12, 0, 0]
zeros = [0, 0]
move_zeroes_inplace(zeros)
assert zeros == [0, 0]
empty = []
move_zeroes_inplace(empty)
assert empty == []
```

<details>
<summary>查看 E19 参考答案与解释</summary>

<!-- solution -->
```python
def move_zeroes_inplace(nums):
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

函数先收集非零数字，再逐个赋值给原列表的前几个位置，剩余位置填零。这样调用方仍然持有原对象，但内容已经改变。

> ⚠️ `nums = non_zero` 只会给函数内的局部名字换一个对象。要修改调用方的原列表，应写入 `nums[i]` 等实际位置。

</details>
<!-- /exercise -->

<!-- exercise:E20 -->
### E20｜只出现一次的数字：计数版

**任务与边界：**

返回非空整数列表中只出现一次的那个数字。

恰好一个数字出现一次，其余各出现两次。使用计数字典，不使用异或。

**给定样例与预期：**

- 输入：`nums = [4, 1, 2, 1, 2]`。
- 预期：`4`。

**编写区（待完成）：**

<!-- starter -->
```python
def single_number_basic(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert single_number_basic([4, 1, 2, 1, 2]) == 4
assert single_number_basic([7]) == 7
assert single_number_basic([-1, 0, 0]) == -1
```

<details>
<summary>查看 E20 参考答案与解释</summary>

<!-- solution -->
```python
def single_number_basic(nums):
    count = {}
    for x in nums:
        count[x] = count.get(x, 0) + 1
    for x, freq in count.items():
        if freq == 1:
            return x
```

这道题分两次遍历完成：

1. 遍历原列表，建立“数字对应次数”的字典。
2. 遍历 `count.items()`，同时取得数字和次数，返回次数等于 1 的数字。

第二次遍历的是字典记录，不是在重新扫描原列表。

</details>
<!-- /exercise -->

<!-- exercise:E21 -->
### E21｜值到首次下标

**任务与边界：**

返回一个字典，记录每个整数第一次出现的下标。

重复值不能覆盖最初记录。空列表返回空字典。

**给定样例与预期：**

- 输入：`nums = [5, 8, 5]`。
- 预期：`{5: 0, 8: 1}`。

**编写区（待完成）：**

<!-- starter -->
```python
def first_positions(nums):
    # 请按任务要求实现
    pass
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert first_positions([5, 8, 5]) == {5: 0, 8: 1}
assert first_positions([2, 2]) == {2: 0}
assert first_positions([]) == {}
```

<details>
<summary>查看 E21 参考答案与解释</summary>

<!-- solution -->
```python
def first_positions(nums):
    positions = {}
    for i, x in enumerate(nums):
        if x not in positions:
            positions[x] = i
    return positions
```

先检查 `x not in positions`，条件为真才记录下标。第二次遇到 5 时，键已经存在，跳过写入，因此保住了首次下标 0。

> ⚠️ 每轮都执行 `positions[x] = i`，保存的就会变成最后一次出现的位置。

</details>
<!-- /exercise -->

**第五组：写错以后，恢复出错时的状态**

最后一题的代码故意有错误。先不要修改，预测它会在哪一轮失败、此前算到了多少，再运行验证。能解释失败，比碰巧改对一行更重要。

<!-- exercise:E22 -->
### E22｜Debug：越界求和

**任务与边界：**

修复编写区里故意设置的越界错误，使函数按下标求和。

先预测报错轮次与报错前的 `total`，再修改。空列表返回 0。

**给定样例与预期：**

- 输入：`nums = [1, 2, 3]`。
- 预期：修复后返回 `6`；原代码在 `i = 3` 时抛出 `IndexError`。

**编写区（待完成）：**

<!-- starter -->
```python
def sum_by_index(nums):
    total = 0
    for i in range(len(nums) + 1):
        total += nums[i]
    return total
```

**验证（先完成实现，再运行）：**

<!-- tests -->
```python
assert sum_by_index([1, 2, 3]) == 6
assert sum_by_index([]) == 0
assert sum_by_index([-1, 1]) == 0
```

<details>
<summary>查看 E22 参考答案与解释</summary>

<!-- solution -->
```python
def sum_by_index(nums):
    total = 0
    for i in range(len(nums)):
        total += nums[i]
    return total
```

1. 长度是 3，合法非负下标只有 0、1、2。
2. 原代码用 `range(4)`，前三轮算出 `total = 6` 后，还会进入 `i = 3` 这一轮。
3. 访问 `nums[3]` 时越界。改成 `range(len(nums))`，让范围只提供合法下标。

> ⚠️ 应修正循环范围，而不是吞掉异常。吞掉错误会隐藏边界问题，也可能掩盖其他失败。

</details>
<!-- /exercise -->

## 4. 本章小结与面试怎么答

这些题反复训练的是四类决定：

- 结果表示数量、总和，还是某个极值？
- 返回一个值，还是构造一组值？
- 只处理当前元素，还是需要记住之前的信息？
- 返回新对象，还是修改调用方的原对象？

能把这些选择与题目要求对应起来，就知道函数体为什么要这样写。

**问：拿到一道不熟悉的小题，你怎样开始？**

> 🎯 先复述输入、输出和边界，再手算样例，明确重复动作与需要保存的状态。先实现最直接的正确方案，再分析是否存在重复工作，最后补边界测试。

## 5. ⚠️ 容易混淆的地方

- “统计正数”加的是 1；“正数求和”加的是 x。先定义结果含义，再写更新。
- 未找到标记 -1 不是一个可以直接继续访问的有效答案；在 Python 中，它会真的取到最后一项。
- 对原地修改题，只检查返回值不够；对返回新列表题，也要检查原输入没有改变。
- 测试失败后先恢复实际状态，不删除测试，也不靠继续刷更难题掩盖基础缺口。

## 6. 章节自测与复盘

<details><summary>E17 为什么先查再记录？</summary>

字典里应当只保存当前位置之前的信息。先查询需要的数字，再记录当前数字，才不会把当前位置使用两次。

</details>

<details><summary>E19 为什么没有 return 也能改变列表？</summary>

参数关联的是调用方传来的列表对象。给 `nums[i]` 赋值是在修改这个对象，调用方能够观察到变化。返回值与对象变化是两件事，要分别检查。

</details>

**复写任务：** 从累积、构造、查询三组各选一道，关掉答案重新写，并增加一个原测试没有覆盖的合法输入。解释新增输入在检查什么，而不是仅仅换一组数字。

复盘不必复制整份答案。可以记录：

- 当时的任务和错误输入。
- 错误发生时的变量状态。
- 原因，以及下一次该先检查什么。

例如：“访问 `nums[i - 1]` 前，先检查 `i` 的起点。”这样的提醒可以直接用于下一题。

## 7. 知识课程回看

先区分自己卡在任务步骤，还是语言机制：

- 步骤已想清，但不懂参数和返回值：[Python：函数与参数](../../../curriculum/01-python/docs/04-函数-参数-作用域-闭包.md)。
- 不清楚列表为什么被一起修改：[Python：可变对象与深浅拷贝](../../../curriculum/01-python/docs/03-可变对象-对象身份-深浅拷贝.md)。

维护者说明：题目、测试与答案以本章为唯一来源，运行 `python tools/build_coding_practice.py` 同步 Notebook，再用 `--check` 验证。学习者不需要执行生成脚本。
