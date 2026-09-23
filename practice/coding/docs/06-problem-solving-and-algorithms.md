# 06｜算法推导：从正确做法到减少重复工作

[← 上一章：数据结构](05-data-structures.md) · [Coding 首页](../README.md) · [下一章：Hot100 综合训练 →](07-hot100.md) · [题目映射](../hot100-map.md)

> 本章前提是能写函数、操作容器、构造第 05 章的数据结构。新增的不是一批神秘模板，而是如何定义状态、利用问题性质、证明不漏答案。线性扫描之后再学递归，递归之后才学搜索与回溯；没有把“看过节点定义”当成“已经会遍历树”。

## 1. 每次优化都要回答：省掉了什么工作

拿到题先复述输入、输出、约束，再手算一个小例子，写最直接的正确办法。能运行以后，估算时间和额外空间，找出反复做的事，再选择要保留的历史信息。最后实现、验证边界，并解释每个状态的含义。这就是读题 → 手算 → 暴力 → 瓶颈 → 状态 → 优化 → 验证的主线。

第 02 章两数之和已经展示过这个过程：逐对检查没错，但对每个数字都重新寻找补数。保存“此前数字到下标”的字典，减少的是重复寻找，不是因为题名含数组就必须用哈希。

复杂度描述增长量级，不是精确秒数。n=100000 时，平方数量级约为 10^10，线性数量级约为 10^5；常数、运行环境、元素操作成本仍然影响实测。n 很小可能容许枚举，n 很大则要排除明显过慢的方案，但数据范围不能独自决定算法。

**循环不变量**是每轮在某个固定时刻都成立的事实。例如“字典只保存此前位置”。说明初始化为什么成立、一次更新为什么仍成立、结束时为什么得到答案，比只背模板更可靠。

## 2. 哈希：把需要反复查询的历史保留下来

两数之和保存位置，字母异位词保存标准特征到同组单词，频次统计保存次数。共同问题是“下一步会问什么，怎样使它不必重新扫描”。dict 与 set 的基础操作归第 02 章，本章只讨论保存什么。

以 128 最长连续序列为例，输入可能乱序且重复；要求连续的是数值，不是原下标。nums=[100,4,200,1,3,2] 的答案是 4，对应 1、2、3、4。

```python
def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:
            continue              # 不是起点，不重复从中间数
        end = x
        while end in values:
            end += 1
        best = max(best, end - x)
    return best

assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
assert longest_consecutive([1, 1, 2]) == 2
assert longest_consecutive([]) == 0
```

虽然有嵌套循环，每个连续段只从起点扩展一次，平均总时间 O(n)，额外空间 O(n)。这也说明“看到两层缩进就写 O(n²)”不成立，需要数总工作量。

## 3. 双指针：两个位置各自代表什么

第 03 章回文使用切片构造反向文字；这里先把它改成两端比较。left 与 right 表示尚未比较的区间，已经从两端排除的部分都配对成功。

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

assert is_palindrome("level") is True
assert is_palindrome("hello") is False
assert is_palindrome("") is True
assert is_palindrome("a") is True
```

level 先比较两端 l，再比较 e，最后只剩中间 v，不必拿同一位置再比较。每轮缩短未检查区间，所以会结束；遇到不相同的一对就可提前返回。时间 O(n)，额外空间 O(1)，不再构造长度 n 的反向字符串。

移动零中的两个下标则表示阅读进度与写入边界。共同点是两个位置合作维护状态，不是必须叫 left/right。

**任务：** 保持非零相对顺序，把 nums=[0,1,0,3,12] 改为 [1,3,12,0,0]，不创建随 n 增长的额外列表。

```python
def move_zeroes(nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1

nums = [0, 1, 0, 3, 12]
assert move_zeroes(nums) is None
assert nums == [1, 3, 12, 0, 0]
empty = []
move_zeroes(empty)
assert empty == []
```

交换使用第 02 章的多目标赋值：先取右侧旧值，再写左侧位置，不是先覆盖一个值再读取它。write 表示下一个非零应该落到的位置；read 扫描当前元素。

| read | 检查值 | 更新后的 write | 列表 |
|---:|---:|---:|---|
| 0 | 0 | 0 | [0,1,0,3,12] |
| 1 | 1 | 1 | [1,0,0,3,12] |
| 2 | 0 | 1 | [1,0,0,3,12] |
| 3 | 3 | 2 | [1,3,0,0,12] |
| 4 | 12 | 3 | [1,3,12,0,0] |

每轮结束时，write 之前是已处理部分的所有非零，顺序不变；write 到 read 是零。这解释了交换为什么不会把尚未读到的非零跳过。时间 O(n)，额外空间 O(1)。随后练 11 盛水容器的短板移动证明、15 三数之和的排序后夹逼；42 接雨水留到综合阶段。

## 4. 滑动窗口：维护连续区间，而不是重复重建

**任务：** 返回字符串中不含重复字符的最长连续子串长度。"abba" 返回 2，不是可以跳着选的子序列长度。

```python
def longest_unique(text):
    seen = set()
    left = 0
    best = 0
    for right, ch in enumerate(text):
        while ch in seen:
            seen.remove(text[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best

assert longest_unique("abba") == 2
assert longest_unique("abcabcbb") == 3
assert longest_unique("") == 0
```

更新 best 时，seen 恰好对应 text[left:right+1]，其中没有重复。读到 abba 的第二个 b 时，窗口是 ab：先删 a 仍有 b，所以还要删旧 b。这里必须 while，不能以为只删一次就恢复合法。

right 从左到右走一次，left 也只向右走，字符加入、移出次数总共线性，所以平均 O(n) 时间。438 字母异位词定位维护定长窗口频次，76 最小覆盖子串维护需求计数；不是所有“连续”问题都可用同样窗口条件，尤其带负数的区间和不能照搬正数的单调收缩理由。

## 5. 前缀和：先定义边界，再做相减

prefix[i] 定义为前 i 个元素的和，因此 prefix[0]=0。对 nums=[2,3,1,4]，prefix=[0,2,5,6,10]；左闭右开区间 [l,r) 的和为 prefix[r]-prefix[l]，因为共同的前 l 项抵消。

```python
nums = [2, 3, 1, 4]
prefix = [0]
for x in nums:
    prefix.append(prefix[-1] + x)
assert prefix == [0, 2, 5, 6, 10]
assert prefix[3] - prefix[1] == 4  # nums[1:3] = [3,1]
```

560 和为 K 的子数组再把等式改写成“过去有多少个前缀等于当前前缀减 k”。这里必须计数，不能只用 set 记录有没有。

```python
def subarray_sum(nums, k):
    frequencies = {0: 1}          # 空前缀，让从下标 0 开始的区间也被统计
    current = 0
    answer = 0
    for x in nums:
        current += x
        answer += frequencies.get(current - k, 0)
        frequencies[current] = frequencies.get(current, 0) + 1
    return answer

assert subarray_sum([1, 1, 1], 2) == 2
assert subarray_sum([0, 0], 0) == 3
assert subarray_sum([1, -1, 0], 0) == 3
assert subarray_sum([], 0) == 0
```

先查旧前缀，再记录当前前缀，避免 k=0 时把长度为零的区间算进去。平均 O(n) 时间，O(n) 额外空间；负数不破坏这个等式。

## 6. 二分：每次排除一段不可能区域

**任务：** 在严格递增整数列表中，返回目标位置；不存在时返回按序插入位置，允许空列表。这是 35 搜索插入位置的练习版本。

```python
def search_insert(nums, target):
    left = 0
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left

assert search_insert([1, 3, 5, 6], 5) == 2
assert search_insert([1, 3, 5, 6], 2) == 1
assert search_insert([1, 3, 5, 6], 7) == 4
assert search_insert([], 7) == 0
```

候选区间始终是 [left,right]，两端都包含。若 nums[mid] 小于目标，mid 以及左边都可排除；反过来排除右侧。循环结束时 left 越过 right，正好是目标应插入的位置。每步候选大约减半，时间 O(log n)，额外空间 O(1)。不要混用另一套 [left,right) 的边界更新。

### 6.1 bisect：理解边界之后再用标准库

有重复值时，“相等时随便返回一个”不能解决首次和末次位置。bisect_left 返回左插入点，bisect_right 返回右插入点，二者都不会修改列表，也不保证目标真的存在。

```python
from bisect import bisect_left, bisect_right, insort

nums = [1, 2, 2, 4]
left = bisect_left(nums, 2)      # 1：第一个不小于 2 的位置
right = bisect_right(nums, 2)    # 3：第一个大于 2 的位置
assert right - left == 2
assert bisect_left(nums, 3) == 3 # 插入位置，不代表 nums[3] 等于 3
returned = insort(nums, 3)      # 查位置并插入；nums 变 [1,2,2,3,4]
assert returned is None and nums == [1, 2, 2, 3, 4]
```

查位置 O(log n)，在列表中间插入仍 O(n)。后续练 74、34、33、153；4 两个有序数组中位数属于更复杂的分割位置二分，放在第 07 章综合训练。

## 7. 单调栈：保存还没有等到答案的位置

第 05 章普通栈处理最近未匹配的括号。739 每日温度的任务则是对每个下标，返回等待几天才遇到更高温度；等不到为 0。暴力对每一天向右重扫，最坏 O(n²)。

```python
def daily_temperatures(temperatures):
    answer = [0] * len(temperatures)
    waiting = []
    for today, temperature in enumerate(temperatures):
        while waiting and temperatures[waiting[-1]] < temperature:
            previous = waiting.pop()
            answer[previous] = today - previous
        waiting.append(today)
    return answer

assert daily_temperatures([73,74,75,71,69,72,76,73]) == [1,1,4,2,1,1,0,0]
assert daily_temperatures([30,30]) == [0,0]
assert daily_temperatures([]) == []
```

waiting 保存未解决下标，对应温度从栈底到栈顶不增。新温度能解决栈顶，就弹出并写等待天数；相等不算更暖。每个下标只入栈、出栈至多一次，所以总时间 O(n)，空间 O(n)。这里的 while 不是反复扫描全部历史。先稳住 20、155、394，再做 739，最后才用单调栈研究 84 柱状图面积。

## 8. 递归：子调用结束以后，父调用从哪里继续

递归是函数调用自身，每次调用有独立的参数和局部状态。必须有停止条件，并把输入推进到更小的问题；否则最终可能遇到 RecursionError，而不是自动“算出结果”。

```python
def sum_to(n):
    if n == 0:
        return 0
    smaller = sum_to(n - 1)
    return smaller + n

assert sum_to(3) == 6
assert sum_to(0) == 0
```

sum_to(3) 暂停在调用 sum_to(2) 的地方，后者又等待 sum_to(1)，一直到 sum_to(0) 返回 0，才逐层得到 1、3、6。子调用 return 只结束子调用，不会把整条调用链一起跳过。此例时间 O(n)，调用栈空间 O(n)，不是只有一个变量就空间 O(1)。

Python 通常不做尾递归消除；深链、深网格可能超过递归深度，改迭代比无依据提高限制更稳妥。

### 8.1 树的递归：先让“子树答案”有含义

**任务：** 计算二叉树最大层数，空树为 0。第 05 章的节点表示已经学过；这里重复最小定义，保证代码可独立运行。

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root):
    if root is None:
        return 0
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)
    return 1 + max(left_depth, right_depth)

def inorder(root):
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

root = TreeNode(2, TreeNode(1), TreeNode(3))
assert max_depth(root) == 2 and max_depth(None) == 0
assert inorder(root) == [1, 2, 3]
invert_tree(root)
assert inorder(root) == [3, 2, 1]
```

max_depth 的返回值是以这个节点为根的子树层数；inorder 按左、根、右组织结果，对应 94；invert_tree 交换左右子树，对应 226。这里 inorder 的列表拼接便于读懂，但在退化树上可能累计 O(n²) 复制；不能把“每节点访问一次”误当成函数整体一定 O(n)。用共享结果列表的遍历可以避免这些拼接，核心访问顺序不变。

## 9. DFS 与 BFS：搜索次序建立在完整数据表示之上

DFS 是深度优先，沿一条路径深入再返回；BFS 是广度优先，用队列按离起点的层次扩展。树、一般图、网格都能用，不是图专属术语。

### 9.1 网格 DFS：一次处理一个连通块

**任务：** 网格由字符串 "1" 表示陆地、"0" 表示水，按上下左右相邻，返回岛屿数；允许空网格，允许修改输入来标记访问。这是 200 的教学版本。

```python
def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])

    def visit(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != "1":
            return
        grid[r][c] = "0"
        visit(r + 1, c)
        visit(r - 1, c)
        visit(r, c + 1)
        visit(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                visit(r, c)
    return count

grid = [["1","1","0"], ["0","0","1"]]
assert num_islands(grid) == 2
assert grid == [["0","0","0"], ["0","0","0"]]
assert num_islands([]) == 0
```

visit 是定义在函数内部的辅助函数，能读取外层的 grid、rows、cols；它修改的是同一网格对象，不是重新绑定外层名字。先标记再探索邻居，避免两格互相重复调用。外层只在遇到尚未处理陆地时增加岛数。时间 O(rows×cols)，最坏递归栈也可线性增长；大网格应考虑显式栈版本。

### 9.2 图 BFS：入队时就记录已经发现

**任务：** 返回从 start 可到达节点的 BFS 顺序。邻接列表决定同层次的访问顺序；图可有环。

```python
from collections import deque

def bfs(graph, start):
    queue = deque([start])
    visited = {start}
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

graph = {1:[2,3], 2:[1,4], 3:[1], 4:[2]}
assert bfs(graph, 1) == [1, 2, 3, 4]
assert bfs({}, 9) == [9]
```

首次发现就加入 visited，而不是等出队，否则同一个节点可能从多个邻居重复入队。对可达部分，时间 O(V+E)，队列和已访问集合 O(V)。BFS 在无权图中能求最少边数；边权不相同时不能直接把层数当最短距离。994 腐烂橘子是多源 BFS：第 0 分钟所有腐烂格同时入队，再按层推进；207 课程表进一步涉及有向依赖和环。

## 10. 回溯：做选择以后，返回时必须恢复现场

**任务：** 给不重复的数字，生成所有排列。nums=[1,2] 得到 [[1,2],[2,1]]；空列表按本练习约定有一种空排列 [[]]。

```python
def permutations(nums):
    answer = []
    path = []
    used = [False] * len(nums)

    def visit():
        if len(path) == len(nums):
            answer.append(path.copy())
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            visit()
            path.pop()
            used[i] = False

    visit()
    return answer

assert permutations([1, 2]) == [[1, 2], [2, 1]]
assert permutations([]) == [[]]
```

path 是当前已经做的选择，used 记录位置是否已用。先选 1、再选 2，复制得到 [1,2]；子调用返回后 pop 2、恢复标记，再返回上一层 pop 1，才能走以 2 开头的分支。若直接 answer.append(path)，保存的是同一个可变列表引用，后续撤销会把已保存答案一起改变。

返回结果本身有 n! 个排列，每个长度 n，所以输出相关时间、空间至少 O(n×n!)；不计结果的路径和递归栈 O(n)。随后练 78 子集、17 电话组合、39 组合总和、22 括号生成、79 单词搜索、131 回文分割，51 N 皇后留到综合阶段。题目允许重复数字或重复选取时，选择规则必须重新定义。

## 11. Top K：只维护需要的部分

**任务：** 返回整数列表第 k 大元素，重复值按位置计数，保证 1≤k≤len(nums)。先全排序再取下标 k-1 是正确起点；若只要前 k 大，可维护大小 k 的最小堆。

```python
import heapq

def kth_largest(nums, k):
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        elif x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap[0]

assert kth_largest([3,2,1,5,6,4], 2) == 5
assert kth_largest([3,3,2], 2) == 3
assert kth_largest([7], 1) == 7
```

堆里保留已处理部分最大的 k 项，其中最小项就是第 k 大的门槛。新数字不超过门槛就无需保留，超过才替换。时间通常写 O(n log k)，更严谨兼顾 k=1 可写 O(n log(k+1))，额外空间 O(k)。347 先计频次再做 Top K，295 需要两个堆协调，留到第 07 章。

## 12. 贪心：当前选择为什么不损害将来

贪心不是“每次选看起来最大”。必须说明保留什么历史足以覆盖所有可能的未来最优答案。

**任务：** 最多买卖一次股票，先买后卖，不交易利润为 0。prices=[7,1,5,3,6,4] 返回 5，允许空列表。

```python
def max_profit(prices):
    if not prices:
        return 0
    lowest = prices[0]
    best = 0
    for price in prices[1:]:
        best = max(best, price - lowest)
        lowest = min(lowest, price)
    return best

assert max_profit([7,1,5,3,6,4]) == 5
assert max_profit([7,6,4,3,1]) == 0
assert max_profit([]) == 0
```

在今天卖出时，历史买入价越低越好，其他更高历史价不可能带来更大利润，所以只需最低价。此写法 O(n) 时间，但切片 prices[1:] 有 O(n) 额外空间；换成下标遍历可避免这份复制。不能为了宣称 O(1) 忽略代码真的创建了什么。55/45 跳跃游戏需要可达边界的证明，763 划分字母区间需要字符最后出现位置的约束，不能仅照搬本题状态。

## 13. 动态规划：先写状态含义，再写递推式

**任务：** 每次走 1 或 2 阶，爬到正整数 n 阶有几种方法。到第 i 阶的最后一步只能从 i-1 或 i-2 来，所以两类数量相加；二者按最后一步分类，不重不漏。

```python
def climb_stairs(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

assert climb_stairs(1) == 1
assert climb_stairs(2) == 2
assert climb_stairs(5) == 8
```

dp[i] 表示到第 i 阶的方法数，而不是含糊的“最优解”。n=5 时表依次得到 1、2、3、5、8。初始化与遍历方向来自依赖关系，不是模板偏好。

每一步只依赖前两个答案，才可以压缩成两个变量：

```python
def climb_stairs_compact(n):
    if n <= 2:
        return n
    previous, current = 1, 2
    for _ in range(3, n + 1):
        previous, current = current, previous + current
    return current

assert climb_stairs_compact(5) == 8
assert climb_stairs_compact(1) == 1
```

右侧同时使用更新前的值。先理解数组状态，再压缩，避免把两个变量的交换背成咒语。数组版 O(n) 时间、O(n) 空间；压缩版额外空间 O(1)。后续按 118、198、322、139、300、416 推进，逐步练状态、转移、初始化与循环方向；不把题目写了“最优”当成一定使用 DP 的证据。

## 14. 训练方式、题目组织与验收

每道题只保留一张解题卡：输入输出约束、朴素解与成本、瓶颈、优化依据、状态含义、最终复杂度、最易错边界。先尝试手算与暴力，卡住时先看一个提示，再看思路；看答案后关掉重写，并隔一段时间随机重做。不能把“知道这是滑窗”当成会解决。

本章代表题按哈希 → 双指针 → 窗口 → 前缀 → 二分 → 栈 → 递归 → DFS/BFS → 回溯 → 堆 → 贪心 → DP 排列。数组区间 53、56、238 与二维数组题，随相应状态与排序基础在[映射表](../hot100-map.md)解锁；组合性更强和 Hard 题进入第 07 章。没有为每个题号复制一份独立文档。

**自测：** abba 为什么不能只缩一次窗口？全排列为什么复制 path？前缀和为什么初始化 {0:1}？二分返回插入点是否代表找到了目标？

<details><summary>查看参考答案</summary>

删去 a 后旧 b 仍在窗口。path 会继续被修改，结果必须保留当时的列表快照。空前缀使从下标 0 开始的区间参与统计。插入点只描述边界，还需在界内检查相等才能确认存在。

</details>

实际验收：独立重写至少一个扫描状态题、一个递归搜索题和一个 DP 题；每题准备普通、最小和容易混淆的输入，解释为什么循环会结束、下标不会越界、返回值满足约定。测试是证据，不替代正确性解释。

语义依据：[bisect](https://docs.python.org/3/library/bisect.html)、[控制流与函数](https://docs.python.org/3/tutorial/controlflow.html)、[heapq](https://docs.python.org/3/library/heapq.html)。
