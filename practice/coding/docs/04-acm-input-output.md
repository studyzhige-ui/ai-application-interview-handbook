# 04｜完整输入输出：把数据协议翻译成程序

[← 上一章：基础练习](03-basic-exercises.md) · [Coding 首页](../README.md) · [下一章：数据结构 →](05-data-structures.md)

> 前面已能写接收参数并返回结果的函数。本章增加输入解析和输出格式两层责任。split、join、解包、格式化、列表构造都已在第 02 章学习；这里组合它们，不把输入模板当成新的算法。

## 1. 函数模式与完整程序模式

函数模式由平台准备 nums、target 等参数，调用你的函数并检查返回值。完整程序模式则把文字送入标准输入 stdin，你必须读取、转换、调用算法，再把答案写到标准输出 stdout。

```text
输入文字 → 解析为 Python 数据 → 算法函数 → Python 结果 → 格式化输出
```

LeetCode 有时给 `class Solution` 包装。它是平台约定的接口，不是解题算法；类、实例和 self 在第 05 章统一学习。这里不要求先学类，先用已经掌握的普通函数把输入输出写清楚。

## 2. map 与迭代：逐项转换不等于立即生成列表

先不用键盘输入，观察类型变化。map(function, source) 每次从 source 取得一项，调用 function 转换。参数传 int，不写 int()，因为要交给 map 一个可调用操作，而不是提前执行一次转换。

```python
line = "10 20 30"
parts = line.split()         # ['10', '20', '30']，仍是字符串
converted = map(int, parts) # 可逐项取值的转换结果，不是列表
nums = list(converted)      # [10, 20, 30]：消费转换结果并收集
print(nums)                 # [10, 20, 30]
print(list(converted))      # []：同一个 map 对象已经消费完
```

因此 `list(map(int,input().split()))` 应从内向外读：读取一行，切成文字项，每项转换成整数，最后收集。需要反复使用结果就保留列表，不反复消费同一个 map。

```python
parts = ["3", "5"]
a, b = map(int, parts)      # 解包也会消费结果，a=3，b=5
print(a + b)               # 8
```

解包需要项数匹配；不是任意长度的输入都能交给两个变量。

## 3. 单组输入：先定义每一行的意义

**契约：** 第一行是非负整数 n，第二行恰好 n 个整数，输出它们的和。即使 n=0，本练习也规定存在第二个空行。样例输入为 `3` 与 `10 20 30`，输出 60。

<!-- run: {"stdin":"3\n10 20 30\n","stdout":"60\n"} -->
```python
n = int(input())
nums = list(map(int, input().split()))
assert len(nums) == n        # 本地核对协议；评测按题目保证的格式读取
print(sum(nums))             # 60
```

不要把所有“第一行一个数”都解释成 n。它也可能是组数、目标值或终止条件；含义来自题面，不来自你习惯的模板。

## 4. T 组、EOF 与哨兵：三种结束依据

### 4.1 已知组数

**契约：** 第一行 T，随后 T 行，每行两个整数，逐行输出和。样例输出 3、11、30，各一行。

<!-- run: {"stdin":"3\n1 2\n5 6\n10 20\n","stdout":"3\n11\n30\n"} -->
```python
T = int(input())
for _ in range(T):          # _ 是不用的循环变量，不是特殊语法
    a, b = map(int, input().split())
    print(a + b)
```

每组内部需要新建的状态放到循环内。把计数或字典留在外面，可能把上一组带到下一组。

### 4.2 不知道组数，读到输入源结束

EOF 是 End Of File，表示输入源已经没有更多数据，不等于读取到空白行。`import sys` 引入标准库模块，`sys.stdin` 是标准输入流；遍历流可以逐行读取并自然在 EOF 结束。

**契约：** 每个非空数据行两个整数，本例没有空行，直到 EOF；输入 `1 2`、`3 4`，输出 3、7。

<!-- run: {"stdin":"1 2\n3 4\n","stdout":"3\n7\n"} -->
```python
import sys

for line in sys.stdin:
    a, b = map(int, line.split())
    print(a + b)
```

另一种写法用 try/except。try 内正常执行，匹配的异常发生才进入 except；这里只捕获读取结束，不把格式错误也吞掉。

<!-- run: {"stdin":"1 2\n3 4\n","stdout":"3\n7\n"} -->
```python
while True:
    try:
        line = input()
    except EOFError:
        break
    a, b = map(int, line.split())
    print(a + b)
```

`input()` 遇到一个空白行会得到空字符串；`sys.stdin.readline()` 在空白行得到 `"\n"`，在 EOF 得到 `""`。是否跳过空行取决于协议；不能统一 strip 后把合法空字符串数据当成 EOF。

### 4.3 读到了特殊数据才结束

**契约：** 每行两个整数，遇到 0 0 停止，且不输出该行的和；输入保证含哨兵。

<!-- run: {"stdin":"1 2\n3 4\n0 0\n","stdout":"3\n7\n"} -->
```python
while True:
    a, b = map(int, input().split())
    if a == 0 and b == 0:
        break
    print(a + b)
```

哨兵是题目定义的数据值，不是 EOF。三种协议不能靠代码长得像就互换。

## 5. 数组、矩阵、字符串与边列表

### 5.1 矩阵：先行数列数，再逐行读取

**契约：** 第一行 n m，随后 n 行，每行 m 个整数；输出所有数字总和。样例是两行三列，输出 21。

<!-- run: {"stdin":"2 3\n1 2 3\n4 5 6\n","stdout":"21\n"} -->
```python
n, m = map(int, input().split())
matrix = []
for _ in range(n):
    row = list(map(int, input().split()))
    assert len(row) == m
    matrix.append(row)
answer = 0
for row in matrix:
    answer += sum(row)
print(answer)                 # 21
```

matrix[r][c] 先取行再取列；行数不是列数。矩阵是否允许空行、零列，应以题目约束为准，不凭样例猜。

### 5.2 字符串里的空格是否有意义

**契约：** 读取一行文字，原样输出。样例保留首尾空格。

<!-- run: {"stdin":"  hello world  \n","stdout":"  hello world  \n"} -->
```python
text = input()
print(text)
```

整行是数据时不能先 split；需要保留首尾空格时也不能 strip。输入是多个空白分隔字段时才按字段拆。第 02 章已讲两种 split 的不同规则。

### 5.3 图先作为边的数据读取

**契约：** 第一行点数 n、边数 m，随后 m 行 u v 表示无向边；这里只读取并输出边数，不提前要求图算法。

<!-- run: {"stdin":"4 3\n1 2\n2 3\n2 4\n","stdout":"3\n"} -->
```python
n, m = map(int, input().split())
edges = []
for _ in range(m):
    u, v = map(int, input().split())
    edges.append((u, v))
print(len(edges))              # 3
```

有向、无向、带权与点编号从 0 还是 1 开始都会影响解释。树也没有统一 ACM 模板，可能给父子边、层序序列、遍历序列或孩子编号；先读清表示，再构造第 05 章的结构。

## 6. 输出与程序入口

`print(*nums)` 中的星号在调用位置展开各项，相当于把元素分别作为参数传给 print。它与 `a,b=pair` 都涉及拆分，但语法位置和用途不同。

```python
nums = [1, 3, 5]
print(*nums)                  # 1 3 5，而不是 [1, 3, 5]
print(" ".join([str(x) for x in nums]))  # 1 3 5
print(f"{3.14159:.2f}")       # 3.14
```

join 版本先用第 02 章的列表推导式把各项转成字符串，再拼接。两种输出写法依赖的基础操作都已经解释，选择更容易读清的一种即可。

模块被直接运行时 `__name__` 是 `"__main__"`；被其他文件导入时，它是模块名。入口判断避免导入算法时意外开始读输入。def 只定义函数，下面的调用才真正执行。

**练习契约：** 第一行 n target，第二行 n 个整数；有且仅有一组答案时输出两个不同下标，无解扩展输出 -1 -1。样例输出 0 1。

<!-- run: {"stdin":"4 9\n2 7 11 15\n","stdout":"0 1\n"} -->
```python
def two_sum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return seen[need], i
        seen[x] = i
    return -1, -1

def solve():
    n, target = map(int, input().split())
    nums = list(map(int, input().split()))
    assert len(nums) == n
    i, j = two_sum(nums, target)
    print(i, j)

if __name__ == "__main__":
    solve()
```

算法没变，只增加 parse → algorithm → output 的边界。调试时才能分别检查输入、算法和输出。

## 7. 大量输入：按行还是一次读取

`sys.stdin.buffer` 是底层二进制输入流；read() 读取剩余全部字节。bytes、字节切分和整数转换已在第 02 章字符串末尾讲过；这里新增的是输入流一次读取的选择，而不是再引入一个陌生数据类型。

**契约：** 所有内容是整数，换行没有业务含义，输出其和。

<!-- run: {"stdin":"1 2\n3 4\n","stdout":"10\n"} -->
```python
import sys

tokens = sys.stdin.buffer.read().split()
nums = list(map(int, tokens))
print(sum(nums))               # 10
```

一次读取占用更多内存，还可能同时保留字节片段和整数列表；交互式程序未到 EOF 时可能继续等待。不能用它处理“每一行是一条完整文字”的协议，也不能靠快读挽救本身 O(n²) 的超时算法。

## 8. 自测、易错点与训练入口

**任务：** 第一行 T，之后每组先给 n，再给一行 n 个整数。每组输出和。样例输入 `2 / 3 / 1 2 3 / 2 / 4 5`，输出 6、9，各一行；斜杠表示换行，不属于输入。

<details><summary>查看完整答案</summary>

<!-- run: {"stdin":"2\n3\n1 2 3\n2\n4 5\n","stdout":"6\n9\n"} -->
```python
T = int(input())
for _ in range(T):
    n = int(input())
    nums = list(map(int, input().split()))
    assert len(nums) == n
    print(sum(nums))
```

</details>

**口述自测：** 为什么 EOF 不等于空行？为什么不能给所有 input 加 strip？为什么地图、树的输入不能照抄数组模板？

<details><summary>查看参考答案</summary>

EOF 是来源结束，空行仍是读到的一条数据。空白可能是文字内容；图和树的输入规定了实体关系，不只是数字列表，必须先理解协议。

</details>

常见错误来自把 T 当 n、少读组数、把矩阵行列反过来、丢空白、输出额外文字以及算法和解析混在一起。练习先从[牛客输入输出](https://www.nowcoder.com/exam/oj?page=1&tab=%E7%AE%97%E6%B3%95%E7%AC%94%E9%9D%A2%E8%AF%95%E7%AF%87&topicId=372)或 [CodeFun ACM](https://codefun2000.com/acm) 入手，再改写已经会的数组、字符串、矩阵、网格和数值 DP 题。链表和复杂树不强制改写，以免序列化抢走当前目标。

验收不是背模板，而是给定协议能预测每次 input 消费哪一行、每次转换后是什么、何时停止、输出什么。语义依据：[Python 输入输出](https://docs.python.org/3/tutorial/inputoutput.html)、[内置函数](https://docs.python.org/3/library/functions.html)、[sys](https://docs.python.org/3/library/sys.html)。
