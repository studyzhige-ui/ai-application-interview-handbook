# 05｜数据结构：从操作需求到结构选择

[← 上一章：输入输出](04-acm-input-output.md) · [Coding 首页](../README.md) · [下一章：算法推导 →](06-problem-solving-and-algorithms.md)


想象有一叠待处理的任务。你可能要先做最早到达的那个，也可能要先做优先级最高的那个，还可能随时撤销刚做的一步。**任务都可以放进列表，但“下一步最想取哪个”不同，合适的组织方式也不同。**

前面学的是怎样操作 Python 容器；这里进一步问：为什么要这样组织数据，这种操作在数据变多时会付出什么代价。先把常用的栈、队列、节点和堆用起来，再理解树与图怎样表达关系。遇到一种新结构，先抓它最擅长的事情，不必背完它的所有接口。

## 1. 选择结构之前先定义最常发生的操作

先把需要的操作说清楚：

- 按到达顺序处理任务，需要方便地取出最早到达的一项。
- 随时处理最紧急的任务，需要不断找到当前最高优先级的一项。
- 撤销刚完成的操作，需要先取出最近保存的记录。

这些需求看起来都在“取一项”，但选择顺序不同。

另一个问题是规模：十个任务时不明显的反复移动，到了十万个可能就成为瓶颈。这正是我们要学习操作成本的原因。

**复杂度**描述输入规模增加时，所需工作量怎样增长。设元素数量为 `n`，先建立下面几种数量关系：

| 表达 | 初步理解 | 直观例子 |
|---|---|---|
| `O(1)` | 工作量不随 `n` 增长 | 已知下标，读取列表中的一个位置 |
| `O(n)` | 工作量随元素数量增长 | 从头到尾检查每个元素 |
| `O(log n)` | 每一步缩小一大部分候选 | 候选数从 8 变成 4、2、1 |
| `O(n log n)` | 可理解为约 `log n` 层、每层处理 `n` 份数据 | 某些比较排序的常见增长量级 |

同一个列表，按下标读取与从头查找某个值，成本也不同。

> ⚠️ 复杂度描述的是增长趋势，不是精确秒数。必须说明哪个操作、什么输入规模，不能笼统地说“list 是 `O(n)`”。

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

> ⚠️ 表中的成本采用常用 CPython 模型，并把键的哈希与比较视为基本操作。复杂键本身的处理也可能有成本；使用字典不代表任何输入下都一定更快。

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

这段代码包含两步：

1. `from collections import Counter` 从标准库模块引入计数工具。
2. `Counter("banana")` 读取各个字符，直接建立频次记录。

得到的 `count` 仍能按键查值，也能用 `items()` 遍历。它替代的是手写“取旧次数、加一、写回”的那段循环，计数的含义没有改变。

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

`defaultdict(list)` 的 `list` 是一个创建默认值的函数。按 `groups[key]` 读取不存在的键时，它会：

1. 调用 `list()` 创建新的空列表。
2. 把这个列表保存为该键的值。
3. 返回这个列表，让后面的 `.append()` 继续使用。

> ⚠️ 传的是 `list`，不是 `list()`。每个新键应创建自己的列表。另外，`.get()` 不触发这个自动创建过程，不存在的键仍不会因此被加入。

它与普通字典解决的是同一个分组问题。是否使用，取决于它有没有让你的处理过程更清楚，不是越短就越高级。

## 3. 栈：最近进入的状态先处理

把盘子一只只叠起来，最后放上去的最容易先拿下来。栈就是这种**后进先出**的顺序，英文缩写是 LIFO。

用列表的末尾作为**栈顶**，就能表达这种顺序：

- `append(x)` 把新元素压入栈顶。
- `pop()` 取走栈顶元素。
- `stack[-1]` 只查看栈顶，不取走。

```python
stack = []
stack.append(10)            # [10]：入栈
stack.append(20)            # [10, 20]
top = stack[-1]             # 20：只查看栈顶，不删除
removed = stack.pop()       # 20：出栈；stack=[10]
print(top, removed, len(stack))  # 20 20 1
assert bool(stack) is True
```

> ⚠️ 空栈不能执行 `pop()`，也不能读取 `stack[-1]`。需要时先检查 `if stack:`，确认有元素再操作。

栈适合处理括号匹配、撤销和嵌套表达式，因为这些任务经常要先处理最近一个尚未完成的状态。

**括号匹配任务：** 输入只包含 `()[]{}` 中的字符，判断它们是否按正确顺序闭合，返回布尔值。空字符串约定为 `True`。

处理规则是：遇到左括号就压栈；遇到右括号，就与栈顶最近的左括号配对。所有字符处理完以后，栈还必须为空。

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

用 `([])` 追踪栈：

| 读到的字符 | 动作 | 动作后的栈 |
|---|---|---|
| `(` | 左括号，压栈 | `['(']` |
| `[` | 左括号，压栈 | `['(', '[']` |
| `]` | 与栈顶 `[` 配对并取走 | `['(']` |
| `)` | 与栈顶 `(` 配对并取走 | `[]` |

字符处理完时，栈为空，返回 `True`。代码最后的 `not stack`，在空栈时就是 `True`。

> ⚠️ 括号数量相等不代表顺序正确。`([)]` 读到 `)` 时，栈顶是 `[`，已经匹配失败。栈要保存顺序，而不只是数量。

这个例子对应 Hot100 20。

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

作为普通队列使用时，先掌握这一条路线：

1. `append(x)` 从右端加入新项。
2. `popleft()` 从左端取出最早加入的一项。

本例加入 10、20、30，再取出一项，得到的是 10，队列剩下 `[20, 30]`。

`deque` 也支持另一个方向：`appendleft` 从左加入，`pop` 从右取出。两端增删通常按 `O(1)` 估算，中间访问与查找不是它的优势。

> ⚠️ 空队列不能执行 `popleft()`。`if queue:` 在队列非空时为真，可以用它确认还有待处理项。

## 5. 在节点之前先学 class、实例和属性

列表把值放在一排位置上；链表则让每个“小节点”记住自己的值和下一个节点。要写节点，先认识一个最小的类，不需要立刻学习完整面向对象体系。

**类定义一类对象需要保存的信息和可以执行的操作。** 这里用 `ListNode` 定义链表节点，每个节点保存：

- `val`：自己的值。
- `next`：下一个节点，或表示没有下一节点的 `None`。

调用 `ListNode(10)` 得到一个具体的节点对象，这个对象叫作类的**实例**。先看代码，再逐步看它怎样创建：

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

执行 `node = ListNode(10)` 时：

1. 创建一个 `ListNode` 实例。
2. 调用 `__init__` 初始化它，`self` 代表这个正在初始化的实例。
3. `val` 接收 10，`next` 没有另外提供，使用默认值 `None`。
4. `self.val = val`、`self.next = next` 把这两项信息保存到实例上。
5. 外面的名字 `node` 关联创建好的实例。

`node.val` 是读取属性，`node.val = 20` 是修改属性。它们都不是调用函数。

> ⚠️ `next` 保存的是另一个节点的引用或 `None`，不是“下一个位置的数字编号”。修改 `next` 改的是连接方向，不是给一个下标加一。

## 6. 链表：改变值与改变连接是两种操作

链表从头节点开始，沿着每个节点的 `next` 向后走。下面先构造 `10 → 30`，把节点 20 插在中间，再让连接绕过它：

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

插入和绕过节点，都是修改连接：

1. 让新节点 20 的 `next` 指向原来的节点 30。
2. 让节点 10 的 `next` 指向 20，得到 `10 → 20 → 30`。
3. 再把节点 10 的 `next` 改为节点 20 的 `next`，就绕过了 20，恢复成 `10 → 30`。

已知要改的前驱节点时，局部重连可以按 `O(1)` 估算。但从头找到第 `k` 个节点，通常还需要 `O(k)` 的遍历。

> ⚠️ 节点值相同不表示是同一个节点。判断两条链表是否相交，需要比较节点身份。绕过一个节点也不代表对象立即销毁，别的变量仍可能引用它。

反转 `1 → 2 → 3` 时，已经处理的部分逐渐反向连接，未处理的部分仍要能够找回来。先明确三个变量：

- `previous`：已反转部分的头节点，开始时为 `None`。
- `current`：这一轮正在处理的节点。
- `following`：改动连接前，暂存原来的下一节点。

每轮先保住后面的链条，再把当前节点接到已反转部分前面：

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

| 本轮处理节点 | 先保存的 `following` | 改动后的连接 | 这轮结束后 |
|---|---|---|---|
| 1 | 节点 2 | `1 → None` | `previous` 为 1，`current` 为 2 |
| 2 | 节点 3 | `2 → 1` | `previous` 为 2，`current` 为 3 |
| 3 | `None` | `3 → 2` | `previous` 为 3，`current` 为 `None` |

当 `current` 是 `None`，说明没有剩余节点。返回 `previous`，它就是反转后链表的头。这是 Hot100 206 的核心过程。

> ⚠️ 必须先保存原来的 `current.next`，再修改它。顺序反过来，会丢掉继续遍历原链表所需的连接。

## 7. 树与二叉搜索树：关系约束决定能做什么

文件夹里面还能有文件夹，层级关系就很适合用树表示。二叉树进一步限制每个节点最多有两个孩子，我们把它们称为 left 和 right。

先认清三个术语：

- **根（root）**：整棵树的起点。
- **叶子（leaf）**：没有孩子的节点。
- **子树（subtree）**：一个节点及其所有后代组成的树。

子树与整棵树具有相同的结构。正因为如此，处理一棵树时，常能把同类任务交给它的子树。

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

**二叉搜索树（BST）是一种带有序约束的二叉树。** 本例采用无重复值的约定，对每个节点都要求：

- 左子树的所有值小于当前节点值。
- 右子树的所有值大于当前节点值。

> ⚠️ 约束作用于整棵子树，不只是直接两个孩子。普通二叉树没有这个大小顺序要求，不能照用下面的查找方式。

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

每次只需根据当前值选择方向：

1. 与目标相等，返回 `True`。
2. 目标更小，进入左子树。
3. 目标更大，进入右子树。
4. 一直走到 `None` 仍未命中，返回 `False`。

例如根为 2，目标为 3，就直接到右子树，不必再检查左侧的 1。排除另一侧的依据，正是二叉搜索树的有序约束。

查找最多沿树高 h 走 O(h) 步。树比较平衡时可能是 O(log n)，退化成一条链时则是 O(n)。认识节点与学会完整遍历是不同层次：遍历还要决定先走哪边、走完怎样返回。

## 8. 堆：持续取优先项，不等于全序列表

**最小堆用于反复取得当前最小项。** 它维护“父节点的值不大于孩子”的关系，因此 `heap[0]` 是最小值，但整个列表并不一定从小到大排列。

`heapq` 是在普通列表上维护堆关系的标准库模块。先认识四个操作：

- `heapify`：把已有列表整理成堆。
- `heappush`：加入新元素，并保持堆关系。
- `heappop`：取走最小元素，并保持剩余部分的堆关系。
- `heap[0]`：只查看最小元素。

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

常用成本估算如下：建堆 `heapify` 为 `O(n)`，入堆和出堆为 `O(log n)`，查看堆顶为 `O(1)`。

> ⚠️ 空堆不能取堆顶或执行 `heappop`。也不要随意修改底层列表的中间位置，否则可能破坏堆关系，使下一次取出的不再是最小项。

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

图的表示必须保留题目需要的信息：

- 有孤立点时，也要为这些点保留记录，不能只根据边创建出现过的点。
- 带权边可以保存为 `(邻居, 权重)`，权重不能丢掉。
- 允许重复边时，列表可能比集合更符合题意。

> ⚠️ 把邻居列表改成集合，会去重并改变顺序约定。不能仅为了方便查询，就擅自改变图的含义。

网格也可以看成图：每个格子是一个点，允许的移动关系就是边。下面采用上下左右四个方向，不需要提前保存所有边，只按当前位置计算相邻坐标。

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

每次尝试一个方向，按下面的顺序进行：

1. 取得位移。例如 `(1, 0)` 表示行号加一，`(0, -1)` 表示列号减一。
2. 位移加到当前位置，得到候选坐标。
3. 检查候选行列是否在网格范围内。
4. 按题目要求，再检查该格是否有障碍、是否可以访问。

> ⚠️ 坐标合法不表示一定能走进去。是否允许斜向、是否有障碍，都要以题目规定为准。

## 10. Trie：字符串共享前缀路径

**Trie（前缀树）按字符路径组织单词，让具有相同前缀的词共享路径。** 例如 `cat` 和 `car` 共享 `c → a`，之后才分成 `t` 和 `r`。

下面限定小写英文字母，用特殊键 `#` 记录“这里是一个已插入单词的末尾”。这个标记用于区分前缀和完整单词。

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

插入 `cat` 后，查询 `ca` 会出现两种答案：

- 查询前缀 `starts_with("ca")`：沿 `c`、`a` 都能走通，所以为真。
- 查询整词 `search("ca")`：路径虽然存在，但末尾没有结束标记，所以为假。

> ⚠️ 路径走得通，只能说明前缀存在。判断完整单词，还要检查结束标记。

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

分别判断下面三种任务适合什么结构，并说明选择依据：

1. 不断加入整数，频繁取当前最小值。
2. 按到达顺序逐项处理。
3. 只判断某个值此前是否出现过。

<details><summary>查看参考答案</summary>

1. 最小堆：持续维护当前最小项。
2. 队列：按先进先出的顺序处理。
3. 集合：保存是否出现的信息。

若第三项还要查询位置或次数，就需要字典保存这些关联信息。

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

两个回看方向分别解决不同问题：

- 不清楚类、实例、属性与 `self`：[Python：面向对象](../../../curriculum/01-python/docs/08-面向对象-魔术方法.md)。
- 不清楚各类操作的成本：[Python：数据结构与复杂度](../../../curriculum/01-python/docs/13-常见数据结构与复杂度.md)。

语义依据：[collections](https://docs.python.org/3/library/collections.html)、[heapq](https://docs.python.org/3/library/heapq.html)、[Python 类教程](https://docs.python.org/3/tutorial/classes.html)。
