# 03｜基础练习：读题、实现、测试、解释

[← 上一章：数据类型与容器](02-python-coding-basics.md) · [Coding 首页](../README.md) · [配套 Notebook](../exercises/03-basic-exercises.ipynb) · [下一章：输入输出 →](04-acm-input-output.md)


看示例时，每一行似乎都懂；关掉答案，光标停在空白文件里，却不知道第一行该写什么。这种落差很常见：**读代码时，别人已经替你选好了变量和步骤；自己写时，这些选择要由你来做。**

本章就是把这一步练出来。题目很小，不需要猜巧妙算法。你会先练累积与计数，再构造结果、记录历史、处理索引，最后把这些动作组合起来。一次只增加一点难度，先写出朴素但正确的程序，再考虑简洁。

## 1. 不知道第一行写什么，先把任务说成四句话

以“统计正数个数”为例，不要先搜索模板，先问自己：输入是一组整数；输出是一个数量；重复动作是逐个检查；需要记住的是已经发现多少个正数。

这样，变量 `count` 才有了理由：它保存数量，所以初始值为 0；遇到正数时加 1，而不是把那个正数加进去。**代码是这些决定的结果，不是凭空写出来的一串语法。**

本章题目都用函数接收数据、返回结果。函数本身已经学过，你要练的是如何决定函数体里的步骤，而不是同时学习新的函数技巧。

## 2. 怎样使用题目、编写区和测试

先只看任务与样例，手算一次。再在编写区完成函数，最后运行测试。`pass` 是让空函数具有合法语法的占位语句，不代表题目已经完成；看到它时，正是你开始写代码的位置。

测试里的 `assert` 是一条可检查的预期。例如某个函数应该返回 6，却返回 None，先调查自己的 return 是否遗漏，不要急着改测试。测试失败是在提供线索，不是在给你的能力打分。

[配套 Notebook](../exercises/03-basic-exercises.ipynb)把每题放成四个相邻单元：可见题目、可编辑函数、测试、折叠答案。先运行自己的函数定义，再运行测试；修改实现后要重新运行定义，否则内核里可能仍是旧函数。遇到残留状态，可以重启 Python 3 内核后按顺序执行。

答案是默认折叠的文字，不会在“运行全部”时自动完成题目。需要帮助时先想清卡在何处，再展开；看完后关掉答案重写。GitHub 提供静态预览，实际运行使用 JupyterLab 等 Notebook 环境。

## 3. 练习主线

**第一组：让一个变量记住已经处理的结果**

E01–E05 先不构造复杂容器，只练“总和、数量、最好或最小的值”。每题先用一句话解释状态，初始化和更新就更容易决定。

<!-- exercise:E01 -->
### E01｜数组求和

**任务与边界：** 返回整数列表 nums 的总和，不用 sum；空列表返回 0。

**给定样例与预期：** `nums=[3,5,2,7] → 17`

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

 total 记住的是已经处理部分的和。读入 3、5、2、7 时，它依次变成 3、8、10、17。放在循环外初始化，才不会每轮把旧结果清掉；等所有元素处理完再 return。

</details>
<!-- /exercise -->

<!-- exercise:E02 -->
### E02｜偶数求和

**任务与边界：** 只累加整数列表中的偶数，0 和负偶数也算偶数；没有偶数时返回 0。

**给定样例与预期：** `nums=[1,2,3,4] → 6`

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

条件决定加不加，累加状态与普通求和一致。

</details>
<!-- /exercise -->

<!-- exercise:E03 -->
### E03｜正数个数

**任务与边界：** 返回严格大于 0 的元素个数，0 不算正数。

**给定样例与预期：** `nums=[-2,0,5,3,-1] → 2`

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

加的是 1 而不是 x，因为保存的是数量。

</details>
<!-- /exercise -->

<!-- exercise:E04 -->
### E04｜最大值

**任务与边界：** 接收非空整数列表，不使用 max，返回最大值；非空是本题保证。

**给定样例与预期：** `nums=[4,9,2,8] → 9`

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

先把第一项当作目前最大值，再用后面的比较不断修正。best=0 看起来方便，却偷偷假设了答案非负；输入全为负数时就会错。题目保证非空，才允许从 nums[0] 开始。

</details>
<!-- /exercise -->

<!-- exercise:E05 -->
### E05｜最小值

**任务与边界：** 接收非空整数列表，不使用 min，返回最小值。

**给定样例与预期：** `nums=[4,9,2,8] → 2`

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

比较方向改变，状态仍然是已处理部分的极值。

</details>
<!-- /exercise -->

**第二组：不只算一个数，还要逐步构造结果**

E06–E08 把注意力从 total 移到 result。处理一个元素后，结果里应该多出什么？原输入是否需要保留？先把这两个问题说清楚。

<!-- exercise:E06 -->
### E06｜过滤偶数

**任务与边界：** 返回只包含偶数的新列表，保持顺序和重复次数，不修改原列表。

**给定样例与预期：** `nums=[1,2,3,4,5,6] → [2,4,6]`

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

新列表避免遍历时删除导致跳项；集合会丢失重复次数。

</details>
<!-- /exercise -->

<!-- exercise:E07 -->
### E07｜平方列表

**任务与边界：** 返回每项平方的新列表，不修改原输入。

**给定样例与预期：** `nums=[1,2,3] → [1,4,9]`

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

每项都转换，无须 if。理解普通循环后，可改成列表推导式。

</details>
<!-- /exercise -->

<!-- exercise:E08 -->
### E08｜反转字符串

**任务与边界：** 返回倒序字符串。先写切片版，再用循环实现；空串返回空串。

**给定样例与预期：** `s="hello" → "olleh"`

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

结果依次为 h、eh、leh、lleh、olleh。切片版是 return s[::-1]。循环头部拼接只用于追踪，长字符串优先反向收集后 join，避免反复复制。

</details>
<!-- /exercise -->

**第三组：记住历史，再查询它**

E09–E14 开始处理频次、重复值和位置。特别留意“出现过吗”“出现几次”“出现在哪里”是三个不同问题，不要给它们机械套同一个字典。

<!-- exercise:E09 -->
### E09｜字符频次

**任务与边界：** 返回字符到次数的字典，空格参与统计，区分大小写。

**给定样例与预期：** `s="banana" → {"b":1,"a":3,"n":2}`

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

每次遇到字符，都先取得旧次数，再加一写回。空格和大小写也是原数据的一部分，题目没有要求清洗就不要擅自改变它们；这里练的是计数，不是文字归一化。

</details>
<!-- /exercise -->

<!-- exercise:E10 -->
### E10｜数字频次

**任务与边界：** 返回整数列表中每个数字出现的次数，不使用 Counter。

**给定样例与预期：** `nums=[1,2,1,3,2,1] → {1:3,2:2,3:1}`

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

从字符换成数字，映射与累积机制相同，不需要背第二份模板。

</details>
<!-- /exercise -->

<!-- exercise:E11 -->
### E11｜第一个再次遇到的值

**任务与边界：** 从左到右扫描，返回最先被第二次遇到的整数；不存在返回 None。不是返回首次位置最靠前的重复值。

**给定样例与预期：** `nums=[3,1,4,1,5] → 1；[2,1,1,2] → 1`

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

seen 只保存当前这一项之前见过的值。第二次遇到一个值时立刻返回，因此得到的是“最早再次遇到的值”，不是先统计全表以后任选一个重复值。

</details>
<!-- /exercise -->

<!-- exercise:E12 -->
### E12｜去重但保留首次顺序

**任务与边界：** 返回保留每个值第一次出现的新列表，不修改输入。

**给定样例与预期：** `nums=[3,1,3,2,1,4] → [3,1,2,4]`

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

列表保留首次出现的次序，集合快速回答是否出现。两者保存的信息不同：重复的值仍能被集合识别，但不会再追加进结果列表。直接 list(set(nums)) 则丢失了这条顺序要求。

</details>
<!-- /exercise -->

<!-- exercise:E13 -->
### E13｜第一次出现的位置

**任务与边界：** 返回 target 的首次下标，未找到返回 -1；手写遍历，不使用 index。

**给定样例与预期：** `nums=[8,3,7,3], target=3 → 1`

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

返回 i 而不是 x；-1 是未找到标记，不能直接再拿它索引列表。

</details>
<!-- /exercise -->

<!-- exercise:E14 -->
### E14｜相邻最大绝对差

**任务与边界：** 返回相邻两项差的绝对值的最大值；少于两个元素时返回 0。

**给定样例与预期：** `nums=[2,8,5,12] → 7`

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

先想第一对相邻元素是谁：位置 0 和 1。因此循环从 i=1 开始，让 i-1 与 i 组成一对。i=0 时 Python 会把 -1 解释成末尾位置，代码未必报错，却比较了题目没要求的一对。

</details>
<!-- /exercise -->

**第四组：把基础动作组合成完整任务**

E15–E21 不需要突然换一套语法。回文、两数之和、移动零都由熟悉的判断、循环、查询和写回构成；难点是把状态与题目要求对应起来。

<!-- exercise:E15 -->
### E15｜回文判断

**任务与边界：** 判断文字正读反读是否相同，大小写与空格都参与比较；空字符串约定为回文。先求清楚，不要求最优空间。

**给定样例与预期：** `s="level" → True；"hello" → False`

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

回文要求正着读和倒着读相同，因此把原字符串与 s[::-1] 比较，就能得到布尔结果。空字符串倒过来仍为空，也符合本题约定。先把这层判断写成可调用的函数，再研究怎样避免创建反向副本。

</details>
<!-- /exercise -->

<!-- exercise:E16 -->
### E16｜两数之和：暴力版

**任务与边界：** 返回两个不同下标，使数字和为 target。有解时保证唯一，无解扩展返回 []。只用两层循环。

**给定样例与预期：** `nums=[2,7,11,15], target=9 → [0,1]`

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

j 从 i+1 开始，排除同位置和反向重复配对。return 必须位于函数内。

</details>
<!-- /exercise -->

<!-- exercise:E17 -->
### E17｜两数之和：字典版

**任务与边界：** 返回两个不同下标，使数字和为 target。有解时保证唯一，无解扩展返回 []。用字典保存历史，只扫描一次。

**给定样例与预期：** `nums=[2,7,11,15], target=9 → [0,1]`

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

对当前 x，要找的是 target-x。字典记下以前的数字与下标，命中就能取到答案。先查再记录很重要：输入只有一个 3、目标为 6 时，不能把同一个位置使用两次。

</details>
<!-- /exercise -->

<!-- exercise:E18 -->
### E18｜移动零：返回新列表

**任务与边界：** 保持非零值相对顺序，把零移到末尾，返回新列表；原输入不变，允许空列表。

**给定样例与预期：** `nums=[0,1,0,3,12] → [1,3,12,0,0]`

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

先按原顺序收集非零数字，再补零直到长度与输入相同，两段循环各有一件明确的事。结果是新列表，原列表必须保持不变；是否最省空间不是这道基础练习的首要目标。

</details>
<!-- /exercise -->

<!-- exercise:E19 -->
### E19｜移动零：覆盖原列表

**任务与边界：** 保持非零顺序，把零移到末尾，修改传入列表，函数返回 None；允许额外列表，不要求常数空间。

**给定样例与预期：** `nums=[0,1,0,3,12] → 调用后 nums 为 [1,3,12,0,0]`

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

调用方拿着的是原列表对象。函数内写 nums=non_zero，只会给局部名字换个对象；逐个写 nums[i] 才是在改变调用方仍然持有的列表。因此本题既检查内容变化，也检查返回值为 None。

</details>
<!-- /exercise -->

<!-- exercise:E20 -->
### E20｜只出现一次的数字：计数版

**任务与边界：** 非空整数列表中恰有一个数字出现一次，其余各出现两次。用字典返回单次数字，不使用异或。

**给定样例与预期：** `nums=[4,1,2,1,2] → 4`

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

第一遍把数字映射到次数，第二遍通过 items 同时取出数字与次数，找到次数为 1 的那一项。这里没有借助“其余数成对”抵消的技巧，先用熟悉的计数把任务完整做出来。

</details>
<!-- /exercise -->

<!-- exercise:E21 -->
### E21｜值到首次下标

**任务与边界：** 返回各整数第一次出现下标的字典，重复值不能覆盖最初记录。

**给定样例与预期：** `nums=[5,8,5] → {5:0,8:1}`

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

同一个值再次出现时，不能覆盖已经记住的位置。先判断 x 是否不在 positions，再写入，正好把“第一次出现”翻译成了代码条件。

</details>
<!-- /exercise -->

**第五组：写错以后，恢复出错时的状态**

最后一题的代码故意有错误。先不要修改，预测它会在哪一轮失败、此前算到了多少，再运行验证。能解释失败，比碰巧改对一行更重要。

<!-- exercise:E22 -->
### E22｜Debug：越界求和

**任务与边界：** 编写区有故意的边界错误。先预测何时出错与出错前 total，再修复为按下标求和；空列表返回 0。

**给定样例与预期：** `nums=[1,2,3] → 应返回 6；原代码 i=3 时出错`

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

长度为 3 的合法下标是 0、1、2。前三轮 total 已经是 6，原来的 range(4) 却又提供 3，于是读取 nums[3] 才失败。删除多出的 +1，使遍历范围与合法下标一致；不要用吞掉异常的方式绕过去。

</details>
<!-- /exercise -->

## 4. 本章小结与面试怎么答

这些小题反复练习的是几种决定：结果是数量还是总和，是一个值还是一组值，需要记住历史还是只看当前位置，应该返回新对象还是修改原对象。能独立作出这些决定，就不再需要等题解替你写第一行。

**问：拿到一道不熟悉的小题，你怎样开始？**

> 🎯 先复述输入、输出和边界，再手算样例，明确重复动作与需要保存的状态。先实现最直接的正确方案，再分析是否存在重复工作，最后补边界测试。

## 5. ⚠️ 容易混淆的地方

- “统计正数”加的是 1；“正数求和”加的是 x。先定义结果含义，再写更新。
- 未找到标记 -1 不是一个可以直接继续访问的有效答案；在 Python 中，它会真的取到最后一项。
- 对原地修改题，只检查返回值不够；对返回新列表题，也要检查原输入没有改变。
- 测试失败后先恢复实际状态，不删除测试，也不靠继续刷更难题掩盖基础缺口。

## 6. 章节自测与复盘

<details><summary>E17 为什么先查再记录？E19 为什么没有 return 也能改变列表？</summary>

前者要保证只与此前位置配对，后者通过参数修改了调用方共享的对象。返回值与对象变化是两件事，应分别检查。

</details>

**复写任务：** 从累积、构造、查询三组各选一道，关掉答案重新写，并增加一个原测试没有覆盖的合法输入。解释新增输入在检查什么，而不是仅仅换一组数字。

错误记录只需要保留任务、当时的错误状态、原因、下次检查信号。例如“访问 i-1 前先看起点”，比收藏一整份答案更容易用在下一题。

## 7. 知识课程回看

状态已经想清楚却不会写函数时，回看 [Python：函数与参数](../../../curriculum/01-python/docs/04-函数-参数-作用域-闭包.md)；不清楚列表为什么被一起修改时，回看 [Python：可变对象与深浅拷贝](../../../curriculum/01-python/docs/03-可变对象-对象身份-深浅拷贝.md)。先区分是语言机制卡住，还是题目的步骤没有想清楚。

维护者说明：题目、测试与答案以本章为唯一来源，运行 `python tools/build_coding_practice.py` 同步 Notebook，再用 `--check` 验证。学习者不需要执行生成脚本。
