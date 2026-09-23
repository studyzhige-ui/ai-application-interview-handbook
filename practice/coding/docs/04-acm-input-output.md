# 04｜完整输入输出：把数据协议翻译成程序

[← 上一章：基础练习](03-basic-exercises.md) · [Coding 首页](../README.md) · [下一章：数据结构 →](05-data-structures.md)


你已经能写 `two_sum(nums, target)`，给它一个列表和目标，它就能返回两个下标。但笔试页面可能只把两行文字交给程序：第一行写长度与目标，第二行写各个数字。**这些文字还不是函数需要的参数，谁来把它们变过去？**

这一章补上这段连接。把输入读成正确的数据，再把计算结果按要求输出，你才拥有一份能独立运行的完整程序。算法没有换一套，只是原来由平台代劳的工作，需要自己接过来了。

## 1. 函数模式与完整程序模式

把评测平台想成调用你函数的另一段程序。在函数模式里，它已经准备好了 nums、target，你只负责计算并返回结果；在完整程序模式里，它只把文字送来，读取、转换和输出也由你负责。

文字进入程序的通道叫**标准输入 stdin**；`print` 默认写入的通道叫**标准输出 stdout**。本地可以通过键盘提供输入，评测时则由系统把测试数据送进来。

```text
输入文字 → 解析为 Python 数据 → 算法函数 → Python 结果 → 格式化输出
```

LeetCode 有时给出的 `class Solution` 是平台约定的函数包装。此时先分清“平台怎样调用代码”与“算法怎样处理数据”，不需要为了理解输入输出，先展开整套面向对象语法。

## 2. 把一行数字拆开：先看过程，再看紧凑写法

给你字符串 `"10 20 30"`，想得到整数列表 `[10,20,30]`，一次 `int` 不能转换整行，因为里面有多个数字。先拆开，再逐项转换，事情就简单了。

```python
line = "10 20 30"
parts = line.split()       # ['10', '20', '30']
nums = []
for part in parts:
    nums.append(int(part))
print(nums)               # [10, 20, 30]
```

现在每次交给 int 的只有 `"10"`、`"20"` 或 `"30"`，都是合法的整数文字。`split` 负责拆，`int` 负责转，列表负责收集，三个动作不要混成一个。

同样的逐项转换可以交给 `map`：

```python
line = "10 20 30"
parts = line.split()
converted = map(int, parts) # 准备逐项调用 int
nums = list(converted)     # 取出转换结果，收集成列表
print(nums)                # [10, 20, 30]
```

`map(int, parts)` 可以读成“对 parts 的每一项使用 int”。传入 `int`，是把转换这个操作交给它；不是写 `int()` 提前调用一次。

于是，常见的 `list(map(int, input().split()))` 就只是把四步嵌在一起：读一行、拆成文字项、逐项变整数、收集成列表。学会展开后，再使用紧凑写法就不必死记括号。

<details><summary>为什么同一个 map 再转一次 list，可能得到空列表？</summary>

map 的结果会逐项被取走。第一次 list 已经消费完同一个 map 对象，第二次不会自动重新生成：

```python
converted = map(int, ["10", "20"])
print(list(converted)) # [10, 20]
print(list(converted)) # []
```

需要重复使用数据，就保存第一次得到的 nums。解包也会消费结果，因此 `a,b=map(int,parts)` 要求恰好有两项，不能把任意长度输入交给两个变量。

</details>

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

做多组输入时，先别急着写循环。要先知道：**程序凭什么判断“这一批已经读完”？** 有时提前告诉你组数，有时直到输入源结束，有时约定遇到特殊值停止。三种依据不同，循环写法才会不同。

### 4.1 已知组数

**契约：** 第一行 T，随后 T 行，每行两个整数，逐行输出和。样例输出 3、11、30，各一行。

本例输入如下。第一行的 3 不参与求和，只告诉程序后面要处理三组：

```text
3
1 2
5 6
10 20
```

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

空行仍然是一行数据，EOF 则表示已经没有下一行。`input()` 读到空行得到 `""`，遇到 EOF 则抛 EOFError；`sys.stdin.readline()` 是另一种按行读取方式，空行为 `"\n"`，EOF 才是 `""`。

这里不必同时背所有读法。先选一种按任务正确处理；特别不要把“读到了空字符串”不加区别地当成输入结束。

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

读一张两行三列的表，程序要先知道有几行，再把每行读成一个列表，逐行放入外层列表。这样第一层下标选行，第二层下标选这一行的列。

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

`.strip()` 会去掉文字两端的空白，不会去掉中间的空格。只有题目说这些首尾空白可以忽略时，才应该使用它。

这里要求原样输出，所以既不 split，也不 strip。代码更短不是判断标准，**读完后的数据是否仍然保留题目所需信息**才是。

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

有向、无向、带权与点编号从 0 还是 1 开始都会影响解释。树也没有统一 ACM 模板，可能给父子边、层序序列、遍历序列或孩子编号；先读清表示，才知道一个整数描述的是值、节点编号还是一条连接。

## 6. 输出与程序入口

`print(*nums)` 中的星号在调用位置展开各项，相当于把元素分别作为参数传给 print。它与 `a,b=pair` 都涉及拆分，但语法位置和用途不同。

```python
nums = [1, 3, 5]
print(*nums)                  # 1 3 5，而不是 [1, 3, 5]
print(" ".join([str(x) for x in nums]))  # 1 3 5
print(f"{3.14159:.2f}")       # 3.14
```

join 版本先用列表推导式把每个数字转成文字，再用空格连接。`print(*nums)` 则把元素分别交给 print，它默认用空格分隔。

`f"{3.14159:.2f}"` 是格式化字符串：花括号放要显示的值，`.2f` 表示按小数形式保留两位。它解决的是显示格式，不是让所有小数计算从此变成精确十进制。

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

## 7. 数据很多时，再考虑一次读取

按行读懂题目以后，如果输入量较大，而且换行本身没有意义，可以一次读取。它是输入方式的选择，不是每道题必须使用的“高级模板”。

<details><summary>需要大量数值输入时再看：read 与 bytes</summary>

`sys.stdin.buffer` 是二进制输入流，`.read()` 读取剩余全部内容。这里得到 `bytes`（字节），例如 `b"10 20"`；它不是普通 str，但可以按空白 split，`int` 也能转换这种数字字节项。

**契约：** 所有内容都是整数，只需要它们的总和，换行不区分记录。

<!-- run: {"stdin":"1\n2 3\n4\n","stdout":"10\n"} -->
```python
import sys

tokens = sys.stdin.buffer.read().split()
nums = list(map(int, tokens))
print(sum(nums)) # 10
```

这会一次保留较多输入，还可能同时保留字节片段和整数列表。若每行是一条必须原样保留的文字记录，就不能为了快读而把换行含义丢掉；交互输入未结束时，read 还可能继续等待。先确认协议，再决定读法。

</details>

## 8. 本章小结与面试怎么答

输入格式本质上是双方的约定：哪些行是组数，哪些字段是数据，什么时候结束，怎样表示结果。每次 input 消费了哪一行、转换以后是什么类型，说清这些就能写出完整程序。

**问：LeetCode 函数题会做，为什么换成 ACM 模式还可能失败？**

> 🎯 函数模式由平台构造参数并读取返回值；完整程序还要自己解析标准输入、处理多组与结束条件，并按格式输出。算法不变，但输入和输出也成为正确性的一部分。

## 9. ⚠️ 容易混淆的地方

- 第一行一个整数不一定是 n，也可能是 T、目标值或其他参数，含义只能来自题面。
- EOF、空行、哨兵值是三件事；不要把不同输入协议套成同一个循环。
- 字符串中的空格可能就是数据，split 与 strip 都可能丢掉不该丢的信息。
- 算法返回列表，不代表输出可以带 Python 的方括号；输出格式必须单独核对。

## 10. 章节自测与动手练习

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

练习先从[牛客输入输出](https://www.nowcoder.com/exam/oj?page=1&tab=%E7%AE%97%E6%B3%95%E7%AC%94%E9%9D%A2%E8%AF%95%E7%AF%87&topicId=372)或 [CodeFun ACM](https://codefun2000.com/acm) 入手，再改写已经会的数组、字符串、矩阵、网格和数值 DP 题。链表和复杂树不强制改写，以免序列化抢走当前目标。

## 11. 知识课程回看

想理解文件、输入流、导入和入口判断的关系，可以看 [Python：异常、文件与模块](../../../curriculum/01-python/docs/09-异常-文件-模块与导入.md)。遇到 map 消费一次以后为空，则可用 [Python：迭代器与生成器](../../../curriculum/01-python/docs/06-迭代器-生成器-yield.md)深入理解“逐项取得数据”。

语义依据：[Python 输入输出](https://docs.python.org/3/tutorial/inputoutput.html)、[内置函数](https://docs.python.org/3/library/functions.html)、[sys](https://docs.python.org/3/library/sys.html)。
