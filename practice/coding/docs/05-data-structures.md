# 05｜数据结构：从操作需求到结构选择

[← 上一章：输入输出](04-acm-input-output.md) · [Coding 首页](../README.md) · [下一章：算法推导 →](06-problem-solving-and-algorithms.md)

> 第 02 章已教 Python 容器的基本操作。本章解释操作成本，并完整引入栈、队列、链表、树、堆、图和前缀树。先建立数据表示，再学对它的操作，最后才连接算法题。

## 1. 选择结构之前先定义最常发生的操作

同样一组数据，需要按位置取值、按键查记录、不断取最小值、表达父子关系时，合适结构并不相同。先问数据保存什么关系，再问最频繁的操作和规模，最后权衡成本。

复杂度描述某个操作随规模增长的成本，不是给整个容器贴标签。O(1) 表示不随 n 增长的量级，不是只执行一条机器指令；O(n)、O(log n)、O(n log n) 描述增长趋势，不是精确秒数。

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

### 2.1 Counter：字典计数的标准库形式

先会第 02 章的普通计数字典，再使用 Counter。它是带计数语义的字典子类，缺失项读作 0；键、值、items 的含义仍然不变。

```python
from collections import Counter

count = Counter("banana")
print(count["a"], count["x"])  # 3 0；读取 x 不把它加入
print(count.most_common(2))  # [('a', 3), ('n', 2)]
count.update("ab")           # a 变 4，b 变 2：累加，不是普通 dict.update 的覆盖
count.subtract("aa")         # a 变 2；允许零和负计数
print(dict(count))           # {'b': 2, 'a': 2, 'n': 2}
print(sorted(count.elements())) # ['a', 'a', 'b', 'b', 'n', 'n']
```

most_common 返回由“元素、次数”组成的列表；elements 按正整数次数重复元素，忽略非正计数。Counter 的相加、相减等多重集合运算与普通字典不同，不需要时不强行使用。

### 2.2 defaultdict：缺失下标读取时建立默认值

```python
from collections import defaultdict

groups = defaultdict(list)     # list 是工厂；缺失时调用 list() 创建新列表
print(groups.get("missing"))   # None：get 不触发工厂
assert "missing" not in groups
groups["a"].append(1)          # 先创建 []，再变成 [1]
groups["a"].append(2)          # 已有列表变成 [1, 2]
groups["b"].append(3)          # b 得到另一份列表 [3]
print(dict(groups))            # {'a': [1, 2], 'b': [3]}
```

传 list，不是 list()：要交给 defaultdict 一个“需要时再创建”的操作。`defaultdict(int)` 常用于从 0 累加，`defaultdict(set)` 常用于邻接成员去重。普通字典、get、setdefault 和 defaultdict 的区别要落到“何时创建、何时写入”上理解。

## 3. 栈：最近进入的状态先处理

后进先出称为 LIFO。用 list 的末尾作为栈顶即可，不需要新的 Python 容器类型。

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
        elif not stack or stack.pop() != pairs[ch]:
            return False
    return not stack

assert valid_brackets("([])") is True
assert valid_brackets("([)]") is False
assert valid_brackets("") is True
assert valid_brackets(")") is False
```

右括号必须匹配最近未完成的左括号，不能只统计数量。`not stack or ...` 利用短路，防止空栈 pop。对应 Hot100 20；最小栈 155、字符串解码 394 和单调栈留到状态设计继续展开。

## 4. 队列与 deque：先进入的状态先处理

先进先出称为 FIFO。list.pop(0) 会移动后续元素，频繁从头取值时使用 deque。它是双端队列，两端都能增删；不是所有操作都常数时间。

```python
from collections import deque

queue = deque([10, 20])
queue.append(30)           # [10, 20, 30]：右端加入
queue.appendleft(5)        # [5, 10, 20, 30]：左端加入
first = queue.popleft()    # first=5；[10, 20, 30]
last = queue.pop()         # last=30；[10, 20]
queue.extend([40, 50])    # [10, 20, 40, 50]
queue.extendleft([1, 2])  # [2, 1, 10, 20, 40, 50]：逐项往左加，顺序反转
print(first, last, list(queue))  # 5 30 [2, 1, 10, 20, 40, 50]
queue.rotate(1)            # [50, 2, 1, 10, 20, 40]：最右项转到左边
print(queue[0], queue[-1], len(queue))  # 50 40 6
queue.remove(10)           # 删除首个匹配项，不保证 O(1)
queue.clear()
assert not queue
```

两端 append/pop 通常 O(1)，中间查找、删除和索引不应当成 O(1)。空队列 pop/popleft 报 IndexError。`deque(maxlen=k)` 是限长队列，满时从另一端自动丢弃，不适合必须保留全部任务的场景。

```python
from collections import deque

recent = deque([1, 2], maxlen=2)
recent.append(3)
print(list(recent))        # [2, 3]：1 被自动丢弃
```

第 06 章 BFS 使用队列组织层次；数据结构操作已在这里学完，届时新增的是遍历策略。

## 5. 在节点之前先学 class、实例和属性

类定义一类对象保存什么数据、提供什么方法。调用类得到实例，`__init__` 初始化它；self 表示正在操作的那个实例。`obj.val` 是读取属性，不是函数调用。

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

val、next 是这里选择的属性名；next 保存另一个节点引用或 None，不是要求递增的数字。普通函数接收节点，和接收列表一样，是通过名字找到对象再操作。

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

状态分别为“已反转部分头、待处理节点、剩余链条”。对应 Hot100 206；然后练 21 合并、141 环检测、160 相交，再进入入口推导和复杂复制，避免把所有指针技巧一次塞进节点介绍。

## 7. 树与二叉搜索树：关系约束决定能做什么

树表达层级。根 root 没有父节点；孩子 child 位于下一层；没有孩子的是叶子 leaf；以某节点为根的部分叫子树 subtree。深度按边数还是层数要在题目中明确。

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

查找 O(h)，h 是树高；平衡时可能 O(log n)，退化成链条时 O(n)。DFS 先沿一条路深入，BFS 逐层扩展，它们的完整执行与递归在第 06 章教学；94、104、226、102 是后续树算法练习，不要求只读节点定义就会解题。

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

```python
import heapq

heap = [2, 5, 8]
heapq.heapify(heap)
print(heapq.heappushpop(heap, 1)) # 1：先加后取最小，堆仍含 2、5、8
print(heapq.heapreplace(heap, 1)) # 2：先取原堆顶再加入，堆含 1、5、8
print(heapq.nlargest(2, heap))    # [8, 5]：返回结果，不清空原堆
print(heapq.nsmallest(2, heap))   # [1, 5]
```

heapreplace 要求非空；pushpop 与 replace 顺序不同，不是互换写法。数值最大优先可以存负数，取出再取负；Python 3.14 另有公开最大堆接口，但主线使用兼容较早 Python 3 的最小堆接口，考试环境应以实际版本为准。

优先级相同时，元组会继续比较后面的项。任务对象不可比较时，加入递增编号作第二项，避免走到对象比较。对应 215、347、295、23，算法组合在第 06、07 章继续。

## 9. 图与网格：先完整构造，再谈搜索

图由点和边组成。邻接表保存“从这个点能直接走到哪些点”，无向边要双向记录，有向边只记规定方向。

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

第 02 章已解释元组和解包；此处新增的是把位移加到坐标，以及先判断边界再访问。

## 10. Trie：字符串共享前缀路径

普通字典擅长整词查找；Trie 把字符逐层连接，使 cat、car 共享 c→a。下面限定小写英文字母，用特殊键 # 标记一个单词在这里结束，避免把“前缀存在”误当成“整词存在”。

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

每个字符推进一层，复杂度通常按文字长度估算，代价是额外节点存储。对应 208；不要求把它用到每个字符串问题上。

## 11. 自测与结构选择

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

验收时不仅说出名字，还要能建立结构、执行最常用操作、说明修改和返回、处理空结构，并解释操作成本。Hot100 按[映射表](../hot100-map.md)解锁，树遍历与搜索题在学完第 06 章后完成。

语义依据：[collections](https://docs.python.org/3/library/collections.html)、[heapq](https://docs.python.org/3/library/heapq.html)、[Python 类教程](https://docs.python.org/3/tutorial/classes.html)。
