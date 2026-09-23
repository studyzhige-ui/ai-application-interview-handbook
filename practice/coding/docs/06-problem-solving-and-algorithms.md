# 06｜算法推导：从正确做法到减少重复工作

[← 上一章：数据结构](05-data-structures.md) · [Coding 首页](../README.md) · [下一章：Hot100 综合训练 →](07-hot100.md) · [题目映射](../hot100-map.md)


拿到一道新题时，你可能已经认识每种语法，却仍在想：“我怎么知道这里该用字典，那里该用两个下标？”问题往往不在语法，而在于还没把**题目要求、重复工作和要保存的状态**连起来。

这一章不从背模板开始，而从一个更容易回答的问题开始：最直接的办法怎样做？它反复做了什么？如果把某些信息记住，下次能不能少做一点？下面的算法都围绕这条推导线展开。较长的章节可以按小节逐次练习，不需要一次记住所有模式。

## 1. 每次优化都要回答：省掉了什么工作

拿到题先复述输入、输出、约束，再手算一个小例子，写最直接的正确办法。能运行以后，估算时间和额外空间，找出反复做的事，再选择要保留的历史信息。最后实现、验证边界，并解释每个状态的含义。这就是读题 → 手算 → 暴力 → 瓶颈 → 状态 → 优化 → 验证的主线。

以两数之和为例，每拿到一个数，重新扫描其他位置也能求解。重复之处是：刚才见过的数字，下一轮又得重新寻找。如果把“数字在哪里”留下来，遇到新数字时就可以直接查询它的补数。

所以优化不是把一个“笨算法”换成一个神奇名字，而是先认出浪费在哪里，再决定保存什么信息。

复杂度描述增长量级，不是精确秒数。n=100000 时，平方数量级约为 10^10，线性数量级约为 10^5；常数、运行环境、元素操作成本仍然影响实测。n 很小可能容许枚举，n 很大则要排除明显过慢的方案，但数据范围不能独自决定算法。

每个状态还应该有一句持续成立的解释。比如“两数之和的字典，在查询时只保存此前的位置”，就能说明为什么不会拿同一个位置配对。这种在每轮某个固定时刻都成立的事实，叫**循环不变量**。

不用一开始就写形式化证明。先能回答“最初为什么成立、这一轮怎样继续保持、最后怎样得到答案”，已经比只说‘这是哈希模板’更接近真正理解。

## 2. 哈希：把需要反复查询的历史保留下来

同样使用字典，两数之和记位置，分组题记同类数据，计数题记次数。真正决定算法的不是容器名字，而是**下一步会反复问什么**。

下面换一个例子：一组乱序数字里，最长的一段连续数值有多长？如果从 1 数过 1、2、3、4，再从 2 重新数 2、3、4，就做了重复工作。能否只从每段的起点开始？

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

每轮结束时，write 之前已经放好读过的非零数字，顺序不变；write 到 read 之间是零。read 只向前检查，write 只在遇到非零时前进，因此不会跳过尚未读到的数据。时间 O(n)，额外空间 O(1)。

两个下标在不同题里可以有不同职责：回文里是左右边界，这里是读取与写入进度。解释它们各自在做什么，比记住变量名更重要。

## 4. 滑动窗口：维护连续区间，而不是重复重建

如果已经知道 ab 没有重复，再读到一个 b，不需要把所有子串从头检查一遍。只要修复当前这段区间，让它重新没有重复，就能继续向右扩展。这个会移动边界的连续区间，就是窗口。

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

right 向右加入新字符，left 向右移走旧字符。虽然代码里有 while，但两端都不会退回重走，各自至多走完整个字符串，所以总工作仍是线性的，平均时间 O(n)，额外空间最坏 O(n)。

窗口的关键是能随着边界移动更新状态，不是题目写了“连续”就一定能套用。例如区间和含负数时，移走左端元素未必让总和变小，不能照搬“和太大就收缩”的理由。

## 5. 前缀和：先定义边界，再做相减

经常有人问“这几个连续数字的和是多少”，每次重新相加就很浪费。可以先记录从开头累加到各个边界的总和，再用两个总和相减。

对 `[2,3,1,4]`，前三项和是 6，前一项和是 2，相减得到中间两项 `3+1=4`。把“前 i 项的和”命名为 prefix[i]，就有 prefix[0]=0；左闭右开区间 [l,r) 的和是 prefix[r]-prefix[l]。这里 l、r 表示边界，不是两项都包含的下标。

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

用 `[1,1,1]`、k=2 追一遍：当前前缀和依次是 1、2、3。和为 2 时，查到此前的空前缀 0，得到第一个区间；和为 3 时，查到此前的前缀 1，得到第二个区间。

必须先查旧前缀，再记录当前前缀。否则 k=0 时，会把“当前前缀减自身”的空区间也算进去。平均 O(n) 时间，O(n) 额外空间；这个等式不怕负数，不依赖窗口和的单调变化。

## 6. 二分：每次排除一段不可能区域

在排好序的一排数字中寻找目标，看到中间值比目标小，就能把中间及其左侧全部排除。排序提供了排除依据，所以一次比较不只解决一个位置，而是缩小整段候选范围。

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
from bisect import bisect_left, bisect_right

nums = [1, 2, 2, 4]
left = bisect_left(nums, 2)      # 1：第一个不小于 2 的位置
right = bisect_right(nums, 2)    # 3：第一个大于 2 的位置
assert right - left == 2
assert bisect_left(nums, 3) == 3 # 插入位置，不代表 nums[3] 等于 3
assert nums == [1, 2, 2, 4]    # 查位置不会修改列表
```

查位置通常是 O(log n)，但“知道应插在哪里”与“真的在列表中间插入”不是同一个操作。调用 bisect 后，还要看返回位置有没有越界、对应元素是否相等，才能判断目标是否存在。

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

可以先用短序列 `[73,71,72,74]` 手算。73 等着更暖的一天，71 也等着；72 到来时，先解决最近的 71，却还不能解决 73。74 到来时，则把仍在等待的 72 和 73 都解决。

waiting 存的是这些“仍在等待”的下标，对应温度从栈底到栈顶不增。弹出下标后，今天减去那天就得到等待天数；相同温度不能算更暖。每个位置至多入栈一次、出栈一次，所以 O(n) 时间、O(n) 空间，并没有对每一天重新扫描全部右侧。

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

先把调用和返回分成两个方向看：

```text
向下提问：sum_to(3) 等 sum_to(2)，后者等 sum_to(1)，再等 sum_to(0)
向上交回：0 返回 0 → 1 得到 0+1 → 2 得到 1+2 → 3 得到 3+3
```

最容易误解的是，以为子函数 return 以后整个程序就结束了。其实只结束那一次子调用，等待它的父调用会接着执行。父调用需要记住自己停在哪里、n 是多少，这些未完成现场占用调用栈；此例时间和调用栈空间都是 O(n)。

Python 通常不做尾递归消除；深链、深网格可能超过递归深度，改迭代比无依据提高限制更稳妥。

### 8.1 树的递归：把同一个问题交给两棵小树

**任务：** 计算二叉树的最大层数，空树为 0。如果左子树有 2 层，右子树有 3 层，加上当前根节点，这棵树就是 4 层。

先给函数一句明确承诺：“max_depth(node) 返回以 node 为根的子树有多少层”。这样，父节点不必重写左右子树的全部处理，只需要接收它们的结果。

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

root = TreeNode(2, TreeNode(1), TreeNode(3))
assert max_depth(root) == 2
assert max_depth(None) == 0
```

叶子节点的两个孩子都是 None，分别返回 0，所以叶子得到 `1+max(0,0)=1`。根节点接到左右各 1，再算成 2。函数没有预先知道答案，它只是把同一规则沿结构重复应用，直到空节点这个停止条件。

<details><summary>理解返回过程后，再看中序遍历与翻转</summary>

中序遍历规定“左子树 → 当前节点 → 右子树”；翻转则是在每个节点交换左右子树。不是换了一套递归语法，而是改变每次调用要完成的任务。

```python
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder(root):
    answer = []
    def walk(node):
        if node is None:
            return
        walk(node.left)
        answer.append(node.val)
        walk(node.right)
    walk(root)
    return answer

def invert_tree(root):
    if root is None:
        return None
    old_left = root.left
    root.left = invert_tree(root.right)
    root.right = invert_tree(old_left)
    return root

root = TreeNode(2, TreeNode(1), TreeNode(3))
assert inorder(root) == [1, 2, 3]
invert_tree(root)
assert inorder(root) == [3, 2, 1]
```

walk 是写在 inorder 内部的辅助函数，可以操作这次调用创建的 answer 列表。中序遍历只向同一个结果列表追加，避免反复拼接越来越长的列表；不计返回结果时，递归栈空间取决于树高。翻转保存 old_left，是为了替换 root.left 后仍能找到原左子树。

这些树操作都要访问全部节点，时间 O(n)，递归栈最多 O(h)，其中 h 是树高。

</details>

## 9. DFS 与 BFS：走深一条路，还是先走完一层

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

返回结果本身有 n! 个排列，每个长度 n，所以输出相关时间、空间至少 O(n×n!)；不计结果的路径和递归栈 O(n)。题目允许重复数字或重复选取时，选择规则必须重新定义。

## 11. Top K：只维护需要的部分

**任务：** 返回整数列表第 k 大元素，重复值按位置计数，保证 1≤k≤len(nums)。先全排序再取下标 k-1 是正确起点；若只要前 k 大，可维护大小 k 的最小堆。

下面用到一个就地认识的小工具：`heapq.heapreplace(heap,x)` 取出原堆顶，再放入 x，堆大小保持不变，要求堆非空。在这里，我们只有确认 x 比门槛大时才替换，因此不会把更小的数错误地留下。

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

例如只留最大的 3 个数，当前留下 2、3、4，门槛就是 2。新来 1，可以忽略；新来 5，就替换 2，门槛变成 3。**我们维护的不是全部数字的排序，而是入选前 k 名所需的门槛。**

大小不足 k 时先加入，填满以后才比较并替换；扫描结束，堆顶就是第 k 大。额外空间 O(k)，时间可写 O(n log(k+1))，同时涵盖 k=1 的情况。

## 12. 贪心：当前选择为什么不损害将来

贪心不是“每次选看起来最大”。必须说明保留什么历史足以覆盖所有可能的未来最优答案。

**任务：** 最多买卖一次股票，先买后卖，不交易利润为 0。prices=[7,1,5,3,6,4] 返回 5，允许空列表。

```python
def max_profit(prices):
    if not prices:
        return 0
    lowest = prices[0]
    best = 0
    for i in range(1, len(prices)):
        price = prices[i]
        best = max(best, price - lowest)
        lowest = min(lowest, price)
    return best

assert max_profit([7,1,5,3,6,4]) == 5
assert max_profit([7,6,4,3,1]) == 0
assert max_profit([]) == 0
```

假设今天价格是 6，之前曾经出现过 7、1、5、3。若今天卖出，买入价 1 一定比其他更高买入价划算，因此历史里只需要保留最低价，而不必记住每一种交易组合。

先用此前最低价计算今天卖出的收益，再把今天纳入历史最低价。这样最低价不会来自尚未到达的未来。时间 O(n)，额外空间 O(1)；这里按下标遍历，没有用切片复制剩余价格。这个证明属于当前交易约束，不能把“永远选最小”推广成所有贪心题的答案。

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

右侧同时使用更新前的值。先理解数组状态，再压缩，避免把两个变量的交换背成咒语。数组版 O(n) 时间、O(n) 空间；压缩版额外空间 O(1)。初始化与遍历方向都要从状态依赖推出，不能看到题目写了“最优”就认定必须用 DP。

## 14. 本章小结与训练方式

每道题只保留一张解题卡：输入输出约束、朴素解与成本、瓶颈、优化依据、状态含义、最终复杂度、最易错边界。先尝试手算与暴力，卡住时先看一个提示，再看思路；看答案后关掉重写，并隔一段时间随机重做。不能把“知道这是滑窗”当成会解决。

把算法按“记住什么”串起来：哈希记历史，双指针与窗口记边界，前缀和记累积，栈记未完成项，搜索记访问与路径，DP 记子问题答案。它们不是互相孤立的标签，也可能在一道题里配合使用。

继续练习时，用[题目映射](../hot100-map.md)选择对应任务。每次只换一小部分问题条件，观察原状态还能不能用，比一口气背十个专题更容易建立联系。

## 15. 面试怎么答

**问：你是怎样从暴力解想到优化的？**

> 🎯 先找暴力解反复做的具体工作，再考虑能否保留历史、增量更新区间或利用有序性排除候选。选好状态以后，我会解释初始化、每轮更新和结束时为什么能得到答案，再分析实际代码的成本。

**问：递归、回溯和动态规划是什么关系？**

> 🎯 递归是函数调用自身的执行方式；回溯借助搜索尝试选择，并在返回时撤销选择；动态规划保存子问题结果，减少重复求解。它们关注的层面不同，不能只凭代码里有没有自调用来分类。

## 16. ⚠️ 容易混淆的地方

- 两层缩进不一定是平方复杂度，要数全部执行过程中每项被处理几次。
- 窗口遇重复可能要收缩多次；“只删一次”不保证恢复合法状态。
- 递归返回后父调用还要继续；回溯保存路径时要复制，撤销的是当前探索现场。
- 用了算法名字的最优写法，不代表实际代码没有切片、复制或隐藏的线性查找。

## 17. 章节自测

**自测：** abba 为什么不能只缩一次窗口？全排列为什么复制 path？前缀和为什么初始化 {0:1}？二分返回插入点是否代表找到了目标？

<details><summary>查看参考答案</summary>

删去 a 后旧 b 仍在窗口。path 会继续被修改，结果必须保留当时的列表快照。空前缀使从下标 0 开始的区间参与统计。插入点只描述边界，还需在界内检查相等才能确认存在。

</details>

实际验收：独立重写至少一个扫描状态题、一个递归搜索题和一个 DP 题；每题准备普通、最小和容易混淆的输入，解释为什么循环会结束、下标不会越界、返回值满足约定。测试是证据，不替代正确性解释。

## 18. 知识课程回看

如果卡在函数返回和局部状态，回看 [Python：函数与作用域](../../../curriculum/01-python/docs/04-函数-参数-作用域-闭包.md)；如果卡在“这一步到底做了多少工作”，回看 [Python：数据结构与复杂度](../../../curriculum/01-python/docs/13-常见数据结构与复杂度.md)。算法的选择依据仍需要结合本章的具体推导练习。

语义依据：[bisect](https://docs.python.org/3/library/bisect.html)、[控制流与函数](https://docs.python.org/3/tutorial/controlflow.html)、[heapq](https://docs.python.org/3/library/heapq.html)。
