# 06｜Problem Solving & Algorithms：从“不会做”到一步步推导解法

[← 上一章：Data Structures](05-data-structures.md) · [Coding 首页](../README.md) · [下一章：Hot100 →](07-hot100.md) · [Hot100 Map](../hot100-map.md)

> 算法学习最危险的方式，是看到题目就问“这题是什么模板”。本章先建立一个更稳定的习惯：**先把问题说清楚，先得到一个正确解，再找到真正的瓶颈，最后才选择数据结构和算法。**

---

## 1. 拿到陌生题，先走固定九步

以后做题统一先走：

```text
1. Read Contract
   题目给什么？要求什么？
        ↓
2. Hand Example
   自己手算一个小样例
        ↓
3. Clarify Constraints
   n 多大？值域多大？允许修改输入吗？
        ↓
4. Brute Force
   最直接、最笨但正确的方法是什么？
        ↓
5. Complexity
   它为什么可能太慢 / 太占空间？
        ↓
6. Find Bottleneck
   重复做了哪件事？
        ↓
7. Choose State / Data Structure / Pattern
   怎样避免这部分重复工作？
        ↓
8. Implement + Invariant
   每个变量到底代表什么？什么时候保持成立？
        ↓
9. Test
   正常、最小、边界、重复、极端情况
```

这九步比记住几十个模板重要。

---

## 2. 为什么一定要允许自己先写暴力解

以 `1. 两数之和` 为例。

最自然的是：

```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

复杂度大约：

```text
O(n²)
```

它不是“错误解法”。

它帮我们确认：

```text
问题定义理解对了
→ 我能得到正确答案
→ 真正的瓶颈是：为了每个 x，我都在反复找 need
```

于是才自然出现：

```text
need = target - x

我能不能快速知道 need 以前出现过？
→ dict
```

这才是优化，而不是“题目出现数组，所以背哈希模板”。

---

## 3. 复杂度是“能不能跑得完”的粗模型

### 3.1 时间复杂度

如果 `n = 100000`：

```text
O(n)
≈ 10^5 级别操作

O(n²)
≈ 10^10 级别操作
```

这不是精确运行时间，但已经足以告诉你：两层全枚举通常危险。

### 3.2 空间复杂度

两数之和从：

```text
O(n²) 时间 + O(1) 额外空间
```

变为：

```text
O(n) 平均时间 + O(n) 额外空间
```

这叫 trade-off：用额外空间换时间。

### 3.3 数据范围是提示，不是答案

如果题目说：

```text
n <= 20
```

指数级搜索也许有机会。

如果：

```text
n <= 100000
```

`O(n²)` 往往不现实。

但不要只根据 n 猜算法；还要结合问题结构。

---

# 4. Hash：把“反复查找”变成“记住过去”

典型信号不是某个关键词，而是：

> **我不断重复问：某个值见过吗？它对应什么？它出现几次？**

Hot100：

- `1. 两数之和`：值 → 下标；
- `49. 字母异位词分组`：特征 → 同组字符串；
- `128. 最长连续序列`：快速判断相邻数字是否存在；
- `560. 和为 K 的子数组`：前缀和 → 出现次数。

### 4.1 从两数之和抽象

```text
当前信息不够
→ 把过去有用的信息存起来
→ 下一轮 O(1) 平均查询
```

这才是 Hash 的核心思路。

---

# 5. Two Pointers：两个位置共同描述当前状态

你在回文判断里已经用过：

```python
left = 0
right = len(s) - 1
```

双指针不是“必须有两个叫 left / right 的变量”，而是：

> **用两个位置共同维护一个区间、边界或读写进度。**

---

## 5.1 Hot100：移动零，从额外数组推导双指针

之前的思路：

```text
创建 non_zero
→ 收集非零
→ 写回 nums
```

瓶颈：

```text
额外创建 O(n) 列表
```

真正需要维护的是：

```text
left
= 下一个非零元素应该放的位置

right
= 当前正在检查的位置
```

一种稳定写法：

```python
def move_zeroes(nums):
    left = 0

    for right in range(len(nums)):
        if nums[right] != 0:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
```

手工追踪：

```text
nums = [0, 1, 0, 3, 12]

right = 0
nums[0] = 0
不动
left = 0

right = 1
nums[1] = 1
交换 nums[0], nums[1]
→ [1, 0, 0, 3, 12]
left = 1
...
```

核心 invariant（循环过程中始终成立的事实）可以描述为：

> `left` 之前已经放好了目前遇到的所有非零元素。

有了这句话，代码就不再是神秘模板。

### 5.2 其他 Hot100

- `11. 盛最多水的容器`：两端向中间缩；
- `15. 三数之和`：排序后固定一个数，再左右夹逼；
- `42. 接雨水`：Hard，等双指针 / 单调栈理解稳定后再做。

---

# 6. Sliding Window：维护一个连续区间，而不是重新计算每个区间

滑动窗口特别适合：

```text
连续子数组 / 子串
+
窗口左右边界移动时，状态可以增量更新
```

---

## 6.1 Hot100：无重复字符的最长子串

问题本质：

> 找一个最长的连续区间，使窗口内没有重复字符。

最暴力可以枚举所有子串，再检查重复，成本很高。

滑动窗口维护：

```text
[left, right]
+
窗口里有哪些字符
```

一种容易理解的版本：

```python
def length_of_longest_substring(s):
    seen = set()
    left = 0
    best = 0

    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1

        seen.add(ch)
        best = max(best, right - left + 1)

    return best
```

关键不是背代码，而是先说出窗口 invariant：

> 每次更新 `best` 时，`s[left:right+1]` 中没有重复字符。

其他 Hot100：

- `438. 找到字符串中所有字母异位词`；
- `76. 最小覆盖子串`，难度更高，放在收口阶段。

---

# 7. Prefix Sum：把“反复算区间和”变成“两个前缀相减”

假设：

```python
nums = [2, 3, 1, 4]
```

前缀和可以定义为：

```text
prefix[0] = 0
prefix[1] = 2
prefix[2] = 5
prefix[3] = 6
prefix[4] = 10
```

那么区间 `[l, r)` 的和：

```text
prefix[r] - prefix[l]
```

因为前面的共同部分被减掉。

Hot100 `560. 和为 K 的子数组` 更进一步把：

```text
prefix[j] - prefix[i] = k
```

改写为：

```text
prefix[i] = prefix[j] - k
```

于是问题又变成：

> 以前出现过多少次 `current_prefix - k`？

所以它是 **Prefix Sum + Hash** 的组合题。

---

# 8. Binary Search：每一步排除一半候选范围

最基础前提：

> 搜索空间存在可以利用的单调 / 有序性质。

Hot100 `35. 搜索插入位置` 是非常好的入门题。

一种左闭右闭写法：

```python
def search_insert(nums, target):
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return left
```

二分最容易出错的不是思想，而是边界：

```text
区间到底是 [left, right]
还是 [left, right)？

while 用 <= 还是 <？

mid 已经排除后，边界怎么更新？
```

不要混用两套区间定义。

后续 Hot100：`74 / 34 / 33 / 153`；`4. 两个正序数组中位数`属于 Hard，最后做。

---

# 9. Stack 与 Monotonic Stack

普通 Stack 解决“最近未完成状态”。

例如 `20. 有效的括号`：

```text
遇到左括号
→ 压栈

遇到右括号
→ 必须与最近一个未匹配左括号对应
```

而 `739. 每日温度` 的关键需求是：

> 对每个位置，找到右侧第一个更大的元素。

如果每个位置都向右扫描，是 O(n²)。

单调栈保存“还没等到答案的下标”，并通过维护单调关系让每个元素大致只进栈、出栈一次，于是可以做到 O(n)。

先理解 `20 / 155 / 394`，再进入 `739`，最后 `84`。

---

# 10. DFS / BFS：系统地走完状态空间

## 10.1 DFS

直觉：

```text
从当前点出发
→ 选一个方向一直走
→ 走不动再回来
```

递归版网格 DFS：

```python
def dfs(grid, r, c):
    if r < 0 or r >= len(grid):
        return
    if c < 0 or c >= len(grid[0]):
        return
    if grid[r][c] != "1":
        return

    grid[r][c] = "0"

    dfs(grid, r + 1, c)
    dfs(grid, r - 1, c)
    dfs(grid, r, c + 1)
    dfs(grid, r, c - 1)
```

`200. 岛屿数量` 的关键不是“背四个 dfs”，而是：

```text
发现一块尚未访问的陆地
→ 岛屿数 +1
→ 用 DFS 把与它连通的整块陆地标记掉
```

## 10.2 BFS

BFS 用 Queue 一层一层扩展。

`994. 腐烂的橘子` 天然有“第 0 分钟、第 1 分钟、第 2 分钟”的层次，所以 BFS 很自然。

基本骨架：

```python
from collections import deque

queue = deque([start])

while queue:
    node = queue.popleft()

    for nxt in neighbors(node):
        if nxt not in visited:
            visited.add(nxt)
            queue.append(nxt)
```

不要把 DFS/BFS 当成图专属。树和网格也经常使用。

---

# 11. Backtracking：DFS + 做选择 + 撤销选择

以 `46. 全排列` 为例：

```text
位置 0 选谁？
→ 继续决定位置 1
→ 继续决定位置 2
→ 得到一个完整答案
→ 回退，换另一个选择
```

核心状态：

```python
path = []
used = [False] * len(nums)
```

典型骨架：

```python
def backtrack():
    if 满足完成条件:
        保存答案
        return

    for choice in 可选项:
        做选择
        backtrack()
        撤销选择
```

这不是要求背这五行，而是理解：

> `path` 表示“当前已经做出的选择”，递归返回后必须恢复到进入这一层之前的状态。

Hot100 推荐顺序：`46 全排列` → `78 子集` → `17 电话号码字母组合` → `39 组合总和` → `22 括号生成` → `79 单词搜索` → `131 分割回文串` → `51 N 皇后`。

---

# 12. Heap / Top K：我不需要全部排序，只关心前 K 个

例如 `215. 数组中的第 K 个最大元素`。

最直观可以：

```python
sorted(nums, reverse=True)[k - 1]
```

这是正确起点。

然后问：

> 如果数据特别多，我真的需要把全部元素都排好序吗？

Heap 允许只维护当前最重要的一部分。

Hot100：

- `215. 第 K 个最大元素`；
- `347. 前 K 个高频元素`；
- `295. 数据流的中位数`，更复杂，后做。

---

# 13. Greedy：当前选择必须能被证明不会破坏全局最优

贪心不是：

> “每次选看起来最好的就行。”

真正难点是：

> **为什么这个局部选择不会让未来失去更优解？**

`121. 买卖股票的最佳时机` 可以理解为：

```text
扫描到今天时
只需要知道之前最低价格
→ 今天卖出的最佳利润 = 今天价格 - 之前最低价
```

状态：

```python
min_price
best_profit
```

这是很好的“边遍历边维护最有用历史状态”例子。

后续：`55 跳跃游戏`、`45 跳跃游戏 II`、`763 划分字母区间`。

---

# 14. Dynamic Programming：把重复子问题的答案保存下来

DP 不是先背：

```text
dp[i] = ...
```

而是先问：

```text
大问题能不能由更小的同类问题组成？
这些小问题会不会被反复计算？
我需要保存什么“状态”？
```

---

## 14.1 Hot100：爬楼梯

到第 `i` 阶的最后一步只有两种：

```text
从 i-1 走 1 步过来
从 i-2 走 2 步过来
```

所以：

```text
dp[i] = dp[i-1] + dp[i-2]
```

先定义：

> `dp[i]` = 到达第 i 阶一共有多少种方法。

这句状态定义比递推式更重要。

```python
def climb_stairs(n):
    if n <= 2:
        return n

    a = 1
    b = 2

    for _ in range(3, n + 1):
        a, b = b, a + b

    return b
```

后续从：

```text
70 爬楼梯
→ 198 打家劫舍
→ 322 零钱兑换
→ 300 最长递增子序列
→ 416 分割等和子集
```

逐步增加状态设计难度。

---

# 15. 不要靠关键词匹配算法

这些经验可以帮助你观察，但不是公式：

```text
“连续子串”
可能想到滑动窗口
但不一定

“有序数组”
可能想到二分 / 双指针
但不一定

“所有组合”
可能想到回溯
但仍要看数据规模

“最优”
不代表一定是 DP
```

正确顺序仍然是：

```text
问题结构
→ 暴力解
→ 瓶颈
→ 可利用性质
→ 算法选择
```

---

# 16. 每道算法题都写一张“解题卡”

不需要写长笔记，只写：

```text
题目：
输入 / 输出：

最直接解：
复杂度：

瓶颈：

优化关键：

核心状态 / invariant：

最终复杂度：

我最容易错的边界：
```

例如移动零：

```text
最直接解：额外数组收集非零
时间 O(n)，空间 O(n)

瓶颈：额外空间

优化关键：原数组前部就是非零元素最终应该落的位置

状态：
left = 下一个非零应该写入的位置

invariant：
left 之前已经是处理过部分的所有非零元素

最终：
O(n) 时间，O(1) 额外空间
```

这种卡片会把“我记得代码”升级成“我理解为什么”。

---

# 17. 卡住时的正确求助顺序

不要一不会就完整看题解。

建议：

```text
0–10 分钟
先真正读懂题 + 手算样例

10–20 分钟
写暴力 / 伪代码

仍卡住
只看一个 Hint：
“应该减少哪类重复工作？”

还卡
看核心思路，不直接复制完整代码

看完以后
关掉题解
从空白重新写

第二天 / 一周后
随机重写
```

“看过最优解”只能算 Learned，不能直接算 Solved。

---

# 18. 边界测试清单

算法写完至少检查：

```text
最小输入
一个元素
两个元素
全部相同
全部不同
已经有序
完全逆序
重复值
负数 / 0（如果题目允许）
空输入（如果题目允许）
最大数据范围下复杂度是否合理
```

还要检查：

```text
i-1 / i+1 会越界吗？
while 会停吗？
递归有 base case 吗？
visited 什么时候标记？
left / right 的区间定义一直一致吗？
```

---

# 19. 本章建议 Hot100 解锁顺序

这不是完整 100 题，只是第 06 章第一次集中学习算法模式的主干：

```text
Hash
1 → 49 → 128

Two Pointers
283 → 11 → 15

Sliding Window
3 → 438

Prefix Sum
560

Array / Interval
53 → 56 → 238

Binary Search
35 → 74 → 34 → 33 → 153

Stack
20 → 155 → 394 → 739

Tree
94 → 104 → 226 → 102 → 98 → 230

Graph
200 → 994 → 207

Backtracking
46 → 78 → 17 → 39 → 22

Heap
215 → 347

Greedy
121 → 55 → 45

DP
70 → 118 → 198 → 322 → 139 → 300
```

Hard 和组合性更强的题留到第 07 章收口。

完整 100 题映射见 [Hot100 Map](../hot100-map.md)。

---

## 20. Exit Gate

进入 Hot100 收口阶段前，你应该能够：

- 拿到题先复述输入、输出、约束；
- 不会最优解时先写出暴力解；
- 分析一层 / 两层循环的基本复杂度；
- 说出优化是在消除什么重复工作；
- 解释 Hash、双指针、滑窗、前缀和、二分分别利用了什么性质；
- 区分 DFS、BFS、Backtracking；
- 理解 Heap 是为 Top K / Priority 服务；
- 不把 Greedy 简化成“每次选最大”；
- 定义最简单 DP 的状态含义；
- 给自己的解法写出一个 invariant 或状态定义；
- 关掉答案后重新写至少一批代表性 Hot100；
- 算法写完主动测试边界。

如果你只能看到题名说“这题是滑窗 / DP”，却解释不出为什么，就还没有通过本章。

---

下一章：[07. Hot100](07-hot100.md)
