# 05｜Data Structures：先问“我需要什么操作”，再选结构

[← 上一章：ACM Input / Output](04-acm-input-output.md) · [Coding 首页](../README.md) · [下一章：Problem Solving & Algorithms →](06-problem-solving-and-algorithms.md)

> 数据结构不是一份需要背诵的名词表。它们存在，是因为不同问题需要不同的**保存、访问、查找、插入、删除、取最值、表达关系**方式。
>
> **阅读约束：** 第一次引入 `deque`、`heapq` 等标准库结构时，示例会说明“当前容器里有什么、这一行加入/删除了什么、返回了什么”，不把 API 当作默认背景。

---

## 1. 什么叫数据结构

同样是一组数据，如果最关心：

```text
第 3 个是多少？
→ 顺序数组很自然

用户 id=123 的资料是什么？
→ dict 很自然

当前最小优先级任务是谁？
→ heap 很自然

A 和 B 有没有道路相连？
→ graph 很自然
```

所以选择数据结构前先问：

```text
我要保存什么？
最频繁的操作是什么？
这个操作希望多快？
数据之间有没有顺序 / 层级 / 网络关系？
```

---

## 2. Array / Python list

Python 算法题里，`list` 经常承担动态数组角色：

```python
nums = [10, 20, 30]
```

常见操作成本：

| 操作 | 常见成本 |
|---|---:|
| `nums[i]` | O(1) |
| 末尾 `append` | 摊销 O(1) |
| 末尾 `pop()` | O(1) |
| 中间插入 / 删除 | O(n) |
| 查找某个值 | O(n) |

为什么中间插入慢？因为后面的元素可能需要整体移动。

Hot100 锚点：`283 移动零`、`53 最大子数组和`、`189 轮转数组`、`238 除了自身以外数组的乘积`。

---

## 3. String

字符串是字符序列：

```python
s = "hello"
```

常见操作：下标访问、切片、遍历、比较、查找、构造新字符串。

Python `str` 不可变，所以大量构造字符时经常先放进 list，再：

```python
answer = "".join(chars)
```

Hot100 锚点：`3 无重复字符的最长子串`、`438 找到字符串中所有字母异位词`、`76 最小覆盖子串`、`394 字符串解码`。

---

## 4. Hash Table：Python dict / set

核心需求：

```text
能不能快速知道一个 key 在不在？
能不能快速从 key 找到 value？
```

Python：

```python
d = {}
s = set()
```

平均情况下，常见查询 / 插入接近 O(1)。这里说的是平均情形，不是承诺“任何情况下绝对 O(1)”。

### dict

适合：

```text
key → value
```

例如：

```python
value_to_index[x] = i
count[x] = frequency
```

### set

适合：

```text
只关心存在性
```

Hot100 锚点：`1 两数之和`、`49 字母异位词分组`、`128 最长连续序列`、`560 和为 K 的子数组`。

---

## 5. Stack：后进先出

想象一摞盘子：最后放上去的最先拿下来。

> LIFO = Last In, First Out

Python 直接用 list：

```python
stack = []
stack.append(10)
stack.append(20)
x = stack.pop()
```

`x` 是 `20`。

典型用途：括号匹配、表达式、递归过程、撤销、处理“最近还没完成”的东西。

Hot100：`20 有效的括号`、`155 最小栈`、`394 字符串解码`。`739 每日温度`、`84 柱状图中最大的矩形`属于更进一步的单调栈。

---

## 6. Queue：先进先出

排队就是：

> FIFO = First In, First Out

Python 不建议长期用 `list.pop(0)` 充当队列，因为前端删除需要移动后续元素。

常用：

```python
from collections import deque

queue = deque()
queue.append(10)
queue.append(20)
x = queue.popleft()
```

`x` 是 `10`。

典型用途：BFS、任务排队、层序遍历。

Hot100：`102 二叉树的层序遍历`、`994 腐烂的橘子`。

---

## 7. Linked List：节点通过 next 串起来

数组像：

```text
[10][20][30][40]
```

链表更像：

```text
10 → 20 → 30 → 40 → None
```

最常见节点：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

一个节点保存自己的值和下一节点的引用。

链表最关键的问题不是语法，而是：

> **修改的是节点的值，还是节点之间的连接？**

例如反转链表，本质是把箭头方向改掉。

建议第一批 Hot100：

```text
206 反转链表
→ 21 合并两个有序链表
→ 141 环形链表
→ 160 相交链表
→ 234 回文链表
```

再进入 `142 / 19 / 2 / 24 / 25 / 138 / 148 / 23 / 146`。

---

## 8. Tree：层级和递归结构

最常见二叉树：

```text
       1
      / \
     2   3
    / \
   4   5
```

节点：

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

常见词：

```text
root    根
parent  父节点
child   子节点
leaf    叶子
depth   深度
subtree 子树
```

第一次先区分两种遍历视角：

```text
DFS → 一条路先走深
BFS → 一层一层走
```

建议第一批 Hot100：`94 中序遍历` → `104 最大深度` → `226 翻转二叉树` → `101 对称二叉树` → `102 层序遍历`。

---

## 9. Binary Search Tree：树上的有序规则

BST 的常见规则：

```text
左子树 < 当前节点 < 右子树
```

具体题目还要看是否允许重复值。

Hot100：`108 有序数组转 BST`、`98 验证 BST`、`230 BST 第 K 小`。

BST 是树的一种，不是所有二叉树都满足这个顺序关系。

---

## 10. Heap / Priority Queue：持续拿最小或最大优先项

Python：

```python
import heapq

heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 2)
heapq.heappush(heap, 8)

x = heapq.heappop(heap)
```

默认是最小堆，所以 `x == 2`。

初学时先抓需求：

> **不断加入元素，而且经常需要当前最小值。**

Hot100：`215 第 K 个最大元素`、`347 前 K 个高频元素`、`295 数据流的中位数`、`23 合并 K 个升序链表`。

---

## 11. Graph：很多点之间可以任意建立关系

基本元素：

```text
Vertex / Node → 点
Edge          → 边
```

表示方法之一是邻接表。

如果无向边：

```text
1 2
1 3
2 4
```

可以构造：

```python
from collections import defaultdict

graph = defaultdict(list)

for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)
```

有向图则只加指定方向。

Hot100：`200 岛屿数量`、`994 腐烂的橘子`、`207 课程表`。

---

## 12. Grid：矩阵为什么经常当成图

例如：

```text
1 1 0
1 0 0
0 1 1
```

每个格子可以看成一个点。如果允许上下左右移动，相邻格子之间就像存在边：

```text
矩阵 + 相邻移动规则 ≈ 隐式图
```

所以 `200. 岛屿数量` 是很好的 DFS / BFS 入门题。

---

## 13. Trie：按字符路径组织字符串

Hot100 有 `208. 实现 Trie（前缀树）`。

它解决的核心需求不是普通哈希查整词，而是：

> **大量字符串里，怎样共享前缀并快速判断某个前缀是否存在？**

例如 `cat / car / care` 会共享前面的 `c → a`。

第一次 DSA 学习不用让 Trie 干扰 Array / Hash / Stack / Queue / Tree / Graph 主线，等主结构稳定再学。

---

## 14. 数据结构选择表

| 需求 | 首先想到 |
|---|---|
| 按下标快速访问 | list / array |
| key → value | dict |
| 快速判断是否出现 | set |
| 后进先出 | stack |
| 先进先出 | deque / queue |
| 频繁操作节点连接 | linked list |
| 层级 / 递归关系 | tree |
| 持续取最小 / 最大优先项 | heap |
| 任意实体关系 / 连通性 | graph |
| 前缀查询 | trie |

这不是绝对规则，而是第一层方向感。

---

## 15. 复杂度不要脱离操作背

同一个结构有不同操作成本。

例如 list：

```text
nums[i]         → O(1)
x in nums       → O(n)
nums.append(x)  → 摊销 O(1)
nums.insert(0,x)→ O(n)
```

所以不能说“list 是 O(n)”。应该说：**哪个操作是什么复杂度。**

---

## 16. 本章 Hot100 解锁建议

先做“结构感强、算法技巧少”的：

```text
Hash
1 两数之和
49 字母异位词分组

Linked List
206 反转链表
21 合并两个有序链表
141 环形链表

Tree
94 中序遍历
104 最大深度
226 翻转二叉树
102 层序遍历

Stack
20 有效的括号

Heap
215 第 K 个最大元素（先理解 heap 用途）

Graph
200 岛屿数量（第 06 章正式学 DFS/BFS）
```

不适合当前阶段强啃的 Hard 题留到对应算法学完。

---

## 17. Exit Gate

你应该能闭卷回答：

- list 为什么按下标快、中间插入慢；
- dict 和 set 的区别；
- Stack 为什么叫后进先出；
- Queue 为什么叫先进先出；
- Python 为什么常用 `deque.popleft()`；
- 链表节点保存什么；
- Tree 的 root / child / leaf 是什么；
- DFS 和 BFS 在“走法”上的直观区别；
- heap 解决的核心操作需求是什么；
- graph 的点和边是什么；
- 为什么矩阵可以看成图；
- 为什么选择数据结构要从“我要频繁做什么操作”出发。

---

下一章：[06. Problem Solving & Algorithms](06-problem-solving-and-algorithms.md)
