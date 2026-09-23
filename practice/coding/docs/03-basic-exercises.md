# 03｜基础练习：读题、实现、测试、解释

[← 上一章：数据类型与容器](02-python-coding-basics.md) · [Coding 首页](../README.md) · [配套 Notebook](../exercises/03-basic-exercises.ipynb) · [下一章：输入输出 →](04-acm-input-output.md)

> 本章把已经学过的操作变成独立实现能力。每题都给输入、结果契约、样例、边界、编写区、测试和折叠答案。使用本课程自述任务，不复制外部平台完整题面。

## 1. 从读题到第一行代码

先说四句话：输入是什么，返回或修改什么，重复做什么，保存哪些状态。比如“正数个数”保存数量，不是数字和；“保序去重”同时需要存在性与顺序。

第 01 章已讲函数定义、参数与返回，第 02 章已讲容器参数。本章只用统一接口包装已会的操作，不突然增加新的函数技巧。E01–E05 练累积与极值，E06–E08 练构造，E09–E14 练映射和索引，E15–E21 组合任务，E22 练调试。

## 2. 怎样完成与验证

编写区里的 pass 是空语句，让尚未实现的函数具有合法语法，不表示题目完成。先执行自己的函数定义，再执行测试。assert 已在第 01 章解释；失败时调查实际结果，不修改正确测试来迎合错误实现。

[Notebook](../exercises/03-basic-exercises.ipynb) 与以下题号对应：题目 → 可编辑代码单元 → 测试单元 → 折叠答案。答案是 Markdown 内容，不会在“运行全部”时自动替你完成题目；查看后需复制到编写区才能运行。空白练习的测试失败是预期行为，不是 Notebook 损坏。

GitHub 只能静态预览，运行需在 JupyterLab 等环境选择 Python 3 内核。不同查看器对折叠 HTML 的支持可能不同。遇到旧结果，重启内核再按顺序运行；独立完成是关掉答案重写，不是仅运行参考答案。

## 3. 练习主线

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

total 保存已处理部分的和；初始化在循环外，return 在循环结束后。

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

不能默认 best=0，否则全负数时错误。先确认非空才能读取 nums[0]。

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

不要未经题目允许先 strip/lower。get 读旧次数，赋值写入新次数。

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

先查再加入；命中立即返回，不需要继续统计。

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

set 负责是否出现，list 负责顺序，两者不是重复职责。

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

第一对位置是 0 与 1，因此 i 从 1 开始。i=0 时 i-1 是最后一个位置，程序能跑但题意错。

</details>
<!-- /exercise -->

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

先独立写对函数和契约；第 06 章再用两端向中间的两个下标优化，不把首次函数练习同时变成新算法考试。

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

先查再记录才保证配对来自以前位置；键是数字，值是下标，不是频次。

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

两个阶段分别完成保序过滤与补足长度，不声称满足官方题目的最优空间限制。

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

nums=non_zero 只重新绑定局部名字，不会修改调用方对象；按位置写回才满足契约。

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

items 给出“数字、次数”的二元组，再解包。第 01 章已介绍整数位运算，第 07 章再用异或性质推导空间优化；这里先独立完成计数解法。

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

与保存最后位置相比，多出的存在性判断恰好表达“首次”。

</details>
<!-- /exercise -->

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

长度为 3 的合法下标为 0、1、2。原 range(4) 多出 3，出错前 total=6。删除 +1，或改为遍历值。

</details>
<!-- /exercise -->

## 4. 练后复盘与验收

不看答案选一题重写，再换普通、最小与容易混淆的输入。原地修改题同时检查对象内容和返回值；查询题检查找到和未找到；题目保证非空时，不私自改变输入契约。

**口述自测：** E17 为什么先查再记录？E19 没有 return 为什么也能改变列表？E14 为什么从索引 1 开始？

<details><summary>查看参考答案</summary>

E17 只允许与此前位置配对。E19 通过参数修改了共享对象，返回值与修改是两回事。E14 第一对相邻位置是 0、1，i=0 时 i-1 指向末尾，并非要比较的相邻关系。

</details>

错误记录只写任务、错误状态、原因和下次检查信号。访问 i-1 前检查起点，比抄整份答案更容易迁移。若卡在 API，回所属容器小节；若卡在执行顺序，回第 01 章追踪，不以更多难题掩盖缺口。

能独立完成累积、过滤、判重、频次、索引、返回新结果与修改原对象后，进入第 04 章。下一章新增的是标准输入输出责任，不是另一套算法。

维护：本章为练习内容的权威来源。运行 `python tools/build_coding_practice.py` 生成 Notebook；`python tools/build_coding_practice.py --check` 检查同步状态并运行全部参考答案测试。不得分别手工维护两套不同题目。
