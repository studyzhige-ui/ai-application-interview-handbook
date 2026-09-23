# 05｜数据结构：从操作需求到结构选择

[← 上一章：输入输出](04-acm-input-output.md) · [Coding 首页](../README.md) · [下一章：算法推导 →](06-problem-solving-and-algorithms.md)


想象有一叠待处理的任务。你可能要先做最早到达的那个，也可能要先做优先级最高的那个，还可能随时撤销刚做的一步。**任务都可以放进列表，但“下一步最想取哪个”不同，合适的组织方式也不同。**

前面学的是怎样操作 Python 容器；这里进一步问：为什么要这样组织数据，这种操作在数据变多时会付出什么代价。先把常用的栈、队列、节点和堆用起来，再理解树与图怎样表达关系。遇到一种新结构，先抓它最擅长的事情，不必背完它的所有接口。

## 1. 选择结构之前先定义最常发生的操作

如果任务按到达顺序处理，就需要方便地取出最早的一项；如果要求随时处理最紧急的任务，就需要方便地找到当前最高优先级。选择结构前，先把这句需求说出来，才能知道它究竟要帮你节省什么工作。

另一个问题是规模：十个任务时不明显的反复移动，到了十万个可能就成为瓶颈。这正是我们要学习操作成本的原因。

**复杂度**描述的是：数据变多时，某个操作需要做的工作怎样增长。O(1) 表示在常用模型下不随 n 增长，O(n) 表示大致跟着元素数量增长；它们不是精确秒数，更不是给整个容器贴一个永久标签。

例如，通过下标取列表元素，与从头检查“某个值在不在”，虽然使用同一个列表，做的工作并不相同。

例如每一步把 8 个候选减成 4、2、1，大约三次缩减，对应 log₂8；O(log n) 常见于持续减半的过程。O(n log n) 可以先理解成 n 份数据参与约 log n 层处理。这里是增长模型，不是承诺准确执行多少条语句。

## 2. 数组、字符串与哈希：同一容器的操作成本不同

| 操作 | 常用复杂度估算 | 原因 |
|---|---|---|
| list 按下标访问 | O(1) | 直接找到位置 |
| list 尾部 append | 摊销 O(1) | 偶尔扩容较贵，分摊到一串追加上 |
| list 尾部 pop | 通常 O(1) | 无须整体移动后续元素 |
| list 中间插入、前端删除 | O(n) | 后续元素需要移动 |
| list 成员查找 | O(n) | 最坏检查整列 |
| 长度 k 的列表切片 | O(k) | 构造新外层列表 |
| sorted / list.sort | 最坏 O(n log n) | 比较排序；输入顺序会影响实际工作 |
| dict/set 查询、插入 | 平均 O(1) | 哈希定位；不承诺每次都绝对常数 |

以上是常用 CPython 使用模型，忽略了复杂键的哈希或比较自身成本。不能说“list 是 O(n)”或“用了 dict 就一定更快”。

字符串不可变，重复构造越来越长的结果可能累计复制大量内容。第 02 章的 join 就是把分散片段一次组织起来的工具，而不是纯粹的语法偏好。

### 2.1 Counter：已经会计数，再用现成工具

用字典统计 banana 中的字符次数，你已经能写。标准库的 Counter 把这种常见工作封装好了：

```python
from collections import Counter

count = Counter("banana")
print(count["a"])    # 3
print(count["x"])    # 0：未出现的字符按 0 次读取
print(dict(count))  # {'b': 1, 'a': 3, 'n': 2}
```

`from collections import Counter` 表示从标准库模块中取出这个工具。拿到的 count 仍然可以按键查值、遍历 items；这里最重要的变化是“构造时就完成计数”。先会普通字典版本，才能理解这个工具替你省掉了哪段循环。

### 2.2 defaultdict：第一次遇到一组时，自动准备容器

给单词分组时，你已经写过“如果 key 不存在，先放一个空列表”。defaultdict 可以负责这一步，但先观察它什么时候会创建：

```python
from collections import defaultdict

groups = defaultdict(list)
groups["a"].append(1)    # a 不存在，先创建 []，再追加 1
groups["a"].append(2)    # a 已存在，继续使用同一列表
groups["b"].append(3)    # b 得到另一份新列表
print(dict(groups))      # {'a': [1, 2], 'b': [3]}
```

传入 `list`，是告诉它“缺少键时，调用 list() 创建一份新列表”，不是让所有键共享某个预先创建的列表。只有这种按下标读取缺失键时才会触发；`get` 仍是普通读取，不会自动建组。

它与普通字典解决的是同一个分组问题。是否使用，取决于它有没有让你的处理过程更清楚，不是越短就越高级。

## 3. 栈：最近进入的状态先处理

把盘子一只只叠起来，最后放上去的最容易先拿下来。栈就是这种**后进先出**的顺序，英文缩写是 LIFO。

在 Python 中，用列表末尾作为栈顶就能表达：append 放上去，pop 拿下来。结构名字虽新，操作已经学过。

```python
stack = []
stack.append(10)            # [10]：入栈
stack.append(20)            # [10, 20]
top = stack[-1]             # 20：只查看栈顶，不删除
removed = stack.pop()       # 20：出栈；stack=[10]
print(top, removed, len(stack))  # 20 20 1
assert bool(stack) is True
```

空栈不能 pop 或读 [-1]，先检查。栈适合括号匹配、撤销、表达式嵌套和保存暂未完成的状态。

**完整例子：** 输入只含 `()[]{}`，返回括号是否正确闭合；空串为 True。

```python
def valid_brackets(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        else:
            if not stack:        # 没有等待匹配的左括号
                return False
            left = stack.pop()   # 取最近一个还没匹配的左括号
            if left != pairs[ch]:
                return False
    return not stack

assert valid_brackets("([])") is True
assert valid_brackets("([)]") is False
assert valid_brackets("") is True
assert valid_brackets(")") is False
```

读 `([])` 时，先把 `(` 放进栈，再把 `[` 放进去。遇到 `]`，最上面恰好是 `[`，匹配后取走；遇到 `)`，再匹配剩下的 `(`。

如果是 `([)]`，虽然左右括号数量相同，但 `)` 到来时栈顶是 `[`，顺序已经不对。**栈保留的是“最近还没有完成的状态”，不只是计数。** 这个例子对应 Hot100 20。

## 4. 队列：先来的先处理

排队取号时，先来的人应先被叫到，这叫**先进先出**，英文缩写 FIFO。它和栈的区别，不是保存了什么数据，而是从哪一端取出。

列表也能用 pop(0) 从头取，但每次取走头部，后面的元素需要移动。频繁这么做时，用 deque（双端队列）更合适：

```python
from collections import deque

queue = deque()           # 空队列
queue.append(10)          # 右端加入：[10]
queue.append(20)          # [10, 20]
queue.append(30)          # [10, 20, 30]
first = queue.popleft()   # 从左端取出 10
print(first, list(queue)) # 10 [20, 30]
print(queue[0])           # 20：看看下一个是谁，不删除
```

排队这个任务只需要先练熟 append 与 popleft。deque 两端都能操作，appendleft 从左加入，pop 从右取出；队列处理优先练熟“右边加入、左边取出”这一条路线。

两端增删通常按 O(1) 估算，查找中间成员或访问中间位置则不是它的优势。空队列不能 popleft；先判断 `if queue`，是在问“还有待处理项吗”。

## 5. 在节点之前先学 class、实例和属性

列表把值放在一排位置上；链表则让每个“小节点”记住自己的值和下一个节点。要写节点，先认识一个最小的类，不需要立刻学习完整面向对象体系。

类像一种对象的定义：这里每个 ListNode 都有 val 与 next 两项信息。调用 `ListNode(10)` 创建一个具体节点，这个具体对象叫实例；`__init__` 在创建时初始化它，self 表示正在初始化的那个实例。

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

node = ListNode(10)
print(node.val, node.next)  # 10 None
node.val = 20
print(node.val)             # 20：修改该实例属性
```

`node.val` 是读取 node 的 val 属性，不是调用函数；写 `node.val = 20` 则是改变这个对象保存的值。你可以把它与字典按键读取作对比，但类让“节点应有哪些信息”有了一个统一定义。

next 保存另一个节点引用或 None，不是一个需要加一的数字。普通函数接收节点，和接收列表一样，都是通过名字找到对象再操作。

理解节点以后，再看连接就不必同时猜 class 与箭头的含义了。下面每次修改 next，改的是“下一步走向谁”。

## 6. 链表：改变值与改变连接是两种操作

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

head = ListNode(10, ListNode(30))  # 10 → 30 → None
inserted = ListNode(20, head.next)
head.next = inserted              # 10 → 20 → 30 → None
head.next = head.next.next        # 10 → 30 → None：绕过 20
values = []
current = head
while current is not None:
    values.append(current.val)
    current = current.next
print(values)                      # [10, 30]
```

已知前驱时局部重连可 O(1)，但找到第 k 个节点通常需要 O(k)；不能因此说链表插入一律常数。多个变量可以指向同一个节点，所以相交链表比较的是身份，不是节点值相等。

反转链表要在改箭头前保存原来的下一节点，否则会丢失剩余链条：

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    previous = None
    current = head
    while current is not None:
        following = current.next
        current.next = previous
        previous = current
        current = following
    return previous

head = ListNode(1, ListNode(2, ListNode(3)))
new_head = reverse_list(head)
assert new_head.val == 3
assert new_head.next.val == 2
assert new_head.next.next.val == 1
assert new_head.next.next.next is None
assert reverse_list(None) is None
```

第一次处理节点 1：先记住原来的下一节点 2，再让 1 指向 None。此时已反转部分只有 1，待处理部分从 2 开始。

第二次处理 2：先保住 3，再让 2 指向 1。最后让 3 指向 2，就得到 3→2→1。previous、current、following 分别记住“已经反转好的头”“正在处理谁”“剩下的链从哪里继续”。这就是 Hot100 206 的核心，不是四行赋值的背诵题。

## 7. 树与二叉搜索树：关系约束决定能做什么

文件夹里面还能有文件夹，层级关系就很适合用树表示。二叉树进一步限制每个节点最多有两个孩子，我们把它们称为 left 和 right。

最上面的节点叫根 root，没有孩子的节点叫叶子 leaf。取一个节点和它下面的全部后代，仍然是一棵树，叫子树 subtree。这个“整体由同类小部分组成”的特点，会让递归特别自然。

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

root = TreeNode(2, TreeNode(1), TreeNode(3))
assert root.left.val == 1
root.right = TreeNode(4)   # 替换右子树引用，不是把所有 3 改成 4
assert root.right.val == 4
```

二叉树每个节点最多两个孩子；二叉搜索树 BST 还要求左子树所有值小于节点、右子树所有值大于节点。本例采用无重复值约定，不能只检查直接两个孩子。

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def contains(root, target):
    current = root
    while current is not None:
        if current.val == target:
            return True
        if target < current.val:
            current = current.left
        else:
            current = current.right
    return False

root = TreeNode(2, TreeNode(1), TreeNode(3))
assert contains(root, 3) is True
assert contains(root, 9) is False
```

例如根为 2，要找 3，就不必再检查左侧的 1，直接进入右子树；要找 9，也会往右走，直到没有节点时确认不存在。能排除哪一侧，来自二叉搜索树的有序约束，而不是所有二叉树都有这个能力。

查找最多沿树高 h 走 O(h) 步。树比较平衡时可能是 O(log n)，退化成一条链时则是 O(n)。认识节点与学会完整遍历是不同层次：遍历还要决定先走哪边、走完怎样返回。

## 8. 堆：持续取优先项，不等于全序列表

最小堆保证父节点不大于孩子，所以 heap[0] 是最小项；其他位置不是排序好的序列。heapq 在普通列表上维护这个关系。

```python
import heapq

heap = [5, 2, 8]
returned = heapq.heapify(heap) # 原地建堆；returned=None
assert heap[0] == 2 and returned is None
heapq.heappush(heap, 1)
assert heap[0] == 1
smallest = heapq.heappop(heap)
assert smallest == 1 and heap[0] == 2
print(sorted(heap))             # [2, 5, 8]：只为展示成员，不假装堆内部有全序
```

heapify 为 O(n)，push/pop 为 O(log n)，查看堆顶 O(1)。空堆 pop 报 IndexError。要保持堆性质，就通过堆操作修改，不任意对列表中间赋值。

堆适合“持续加入，同时不断拿出当前最小项”。如果只要一次性的全量排序，sorted 反而更直接。先区分这两种需求，才知道为什么不必把堆里其他位置也排成完整顺序。

若任务需要最大值优先，数值可以存成负数，让更大的原值对应更小的负值；拿出来再取负。主线使用常见的最小堆接口，不依赖特定环境的新版本扩展。

## 9. 图与网格：先完整构造，再谈搜索

若关系不再是一层层向下，而是多个地点之间互相有道路，就用图。地点是点，道路是边；图不要求每个点只有一个上级，也可能走一圈又回到原点。

邻接表回答的很具体：“从这个点，下一步能直接走到谁？”无向道路要在两边都记录，有向道路只记录允许走的方向。

```python
from collections import defaultdict

edges = [(1, 2), (1, 3), (2, 4)]
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)
print(graph[1])           # [2, 3]
print(graph[2])           # [1, 4]
assert graph.get(9, []) == []
assert 9 not in graph    # get 不增加节点
```

需表示孤立点时先创建所有点；需要去掉重复邻居可用 set，但它改变了重复边和顺序语义，必须按题目决定。带权边可以存 `(邻居, 权重)`，不是忽略第三个数。

网格是隐式图：每个格子是点，允许的移动规则定义边。矩阵不总是四方向连通；也可能允许斜向或有障碍。

```python
grid = [[1, 1, 0], [1, 0, 1]]
r, c = 0, 1
neighbors = []
for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    nr, nc = r + dr, c + dc
    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
        neighbors.append((nr, nc))
print(neighbors)          # [(1, 1), (0, 2), (0, 0)]：只检查边界，尚未过滤障碍
```

这里的 `(1,0)` 表示向下一行，`(0,-1)` 表示向左一列。先把位移加到当前位置，得到候选坐标，再判断它有没有走出网格。合法坐标不一定能通过：还要按题目要求检查障碍或陆地条件。

元组和解包依旧只是熟悉的数据操作，新内容是“坐标加位移”这层移动规则。

## 10. Trie：字符串共享前缀路径

普通字典擅长整词查找；Trie 把字符逐层连接，使 cat、car 共享 c→a。下面限定小写英文字母，用特殊键 # 标记一个单词在这里结束，避免把“前缀存在”误当成“整词存在”。

<details><summary>练习前缀查询时，展开看一个完整实现</summary>

```python
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node["#"] = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return "#" in node

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True

trie = Trie()
trie.insert("cat")
trie.insert("car")
assert trie.search("cat") is True
assert trie.search("ca") is False
assert trie.starts_with("ca") is True
assert trie.starts_with("dog") is False
```

查 ca 时，沿 c、a 两条连接都走得通，说明前缀存在；但没有遇到结束标记，不能因此说 ca 本身已经作为单词加入。这就是 search 与 starts_with 要区分的原因。

每个字符推进一层，操作时间通常按文字长度估算，代价是额外节点存储。这个实现对应 Hot100 208 的核心需求，不必在所有字符串题里都使用它。

</details>

## 11. 本章小结与面试怎么答

数据结构不是把同一份数据换个名字保存，而是让某类操作更容易表达、成本更合适。列表按位置取，哈希按键查，栈处理最近未完成项，队列按到达顺序处理，堆持续取优先项，链表、树和图表达不同的连接关系。

**问：为什么队列经常使用 deque，而不是一直 list.pop(0)？**

> 🎯 因为队列频繁从头部取出，list 需要移动后续元素；deque 为两端操作组织存储。它适合排队，但不因此意味着中间访问和查找也都是常数时间。

**问：链表插入是不是 O(1)？**

> 🎯 已经知道要修改的前驱节点时，局部重连可以是 O(1)；如果还要先找到第 k 个节点，查找过程也要计入。复杂度要针对完整操作，而不是只看最后两行赋值。

## 12. ⚠️ 容易混淆的地方

- 栈与队列的核心区别是取出顺序，不是元素长什么样。
- 修改节点的 val 与修改 next 改的是不同事情；反转前要保住剩余链条。
- 堆只保证堆顶最小与堆关系，不保证数组中其他位置已经全量排序。
- 二叉搜索树的约束作用于整棵左右子树，不能只检查直接孩子。

## 13. 章节自测：把需求翻译成操作

**任务：** 不断加入整数，频繁取当前最小值，选什么？需要原顺序按到达次序处理，选什么？需要判断此前是否见过，选什么？

<details><summary>查看参考答案</summary>

分别是最小堆、队列、集合。先明确操作，再选择结构；不是按照“看起来高级”排序。若还要关联位置或次数，用字典而不是仅有成员的集合。

</details>

**练习：** 用 deque 依次加入 10、20、30，连续取出两个，结果应为 10、20，剩余 [30]。解释若用 list.pop(0) 大量重复，为什么更贵。

<details><summary>查看代码与解释</summary>

```python
from collections import deque

queue = deque()
for x in [10, 20, 30]:
    queue.append(x)
assert queue.popleft() == 10
assert queue.popleft() == 20
assert list(queue) == [30]
```

list 前端删除需要移动后续元素；deque 按双端操作组织存储。中间访问仍不是它的优势。

</details>

## 14. 知识课程回看

对类、实例和 self 仍不熟悉，看 [Python：面向对象](../../../curriculum/01-python/docs/08-面向对象-魔术方法.md)；想系统核对各种操作成本，看 [Python：数据结构与复杂度](../../../curriculum/01-python/docs/13-常见数据结构与复杂度.md)。先能执行一个完整操作，再深挖实现机制，更容易把知识连接起来。

语义依据：[collections](https://docs.python.org/3/library/collections.html)、[heapq](https://docs.python.org/3/library/heapq.html)、[Python 类教程](https://docs.python.org/3/tutorial/classes.html)。
