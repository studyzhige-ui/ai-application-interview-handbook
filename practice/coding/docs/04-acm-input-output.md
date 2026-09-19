# 04｜ACM Input / Output：第一次把“完整程序”写明白

[← 上一章：Basic Coding Exercises](03-basic-exercises.md) · [Coding 首页](../README.md) · [下一章：Data Structures →](05-data-structures.md)

> 本章只解决一件事：**题目把数据通过标准输入交给你时，你怎样自己读出来，再把答案按要求写到标准输出。** ACM 模式不是一种新的算法体系。

---

## 1. LeetCode 模式和 ACM 模式差在哪里

LeetCode 常见：

```python
class Solution:
    def twoSum(self, nums, target):
        ...
        return answer
```

平台已经替你完成：

```text
读取测试数据
→ 构造 nums / target
→ 调用你的函数
→ 检查返回值
```

ACM / OJ 模式更像：

```text
标准输入 stdin
→ 你的完整程序
→ 标准输出 stdout
```

所以你自己负责：

```text
读输入
→ 解析
→ 调算法
→ 按格式输出
```

算法本身没有因为“ACM”三个字变成另一套。

---

## 2. stdin 和 stdout 是什么

当前先记：

```text
stdin  = 程序的标准输入来源
stdout = 程序的标准输出去向
```

本地终端里，你键盘输入的内容可以进入 stdin；OJ 上则是评测系统把测试数据交给程序。

`print()` 会写到 stdout，所以除非题目明确要求，不要额外输出：

```text
请输入 n：
答案是：
调试结果：
```

---

## 3. `input()`：一次读取一整行

输入：

```text
hello world
```

```python
s = input()
```

得到：

```python
"hello world"
```

如果：

```python
parts = input().split()
```

得到：

```python
["hello", "world"]
```

所以：

```text
input()
→ 读整行字符串

split()
→ 按空白把这一行切成多个字符串
```

---

## 4. 彻底拆开 `list(map(int, input().split()))`

假设输入：

```text
10 20 30
```

### Step 1

```python
input()
```

得到：

```python
"10 20 30"
```

### Step 2

```python
input().split()
```

得到：

```python
["10", "20", "30"]
```

### Step 3

```python
map(int, ...)
```

把每个字符串转换成整数：

```text
"10" → 10
"20" → 20
"30" → 30
```

### Step 4

```python
list(...)
```

把转换结果收集成：

```python
[10, 20, 30]
```

所以整句最终才是：

```python
nums = [10, 20, 30]
```

这句话以后会写很多次，但目标是**理解四步，不是背一串括号**。

---

## 5. 单组输入

输入：

```text
5
1 2 3 4 5
```

如果题目说第一行是数组长度，第二行是数组：

```python
n = int(input())
nums = list(map(int, input().split()))
```

这里就是一组测试数据。

---

## 6. T 组输入

输入：

```text
3
1 2
5 6
10 20
```

如果题目说第一行 `T` 表示测试组数：

```text
T = 3

第 1 组：1 2
第 2 组：5 6
第 3 组：10 20
```

代码：

```python
T = int(input())

for _ in range(T):
    a, b = map(int, input().split())
    print(a + b)
```

`_` 不是特殊语法，只是常用变量名，表达“这个循环计数我不会使用”。

---

## 7. EOF：不知道有几组，就读到输入结束

EOF = **End Of File**。

大白话：

> **没有更多输入了。**

题目可能写：

> 输入包含多组数据，每行两个整数，直到 EOF。

输入：

```text
1 2
3 4
5 6
```

没有第一行 `3` 告诉你有三组。

Python 可以：

```python
import sys

for line in sys.stdin:
    a, b = map(int, line.split())
    print(a + b)
```

理解成：

```text
还有下一行 → 读
还有下一行 → 读
...
没有下一行 → for 自然结束
```

也可能看到：

```python
while True:
    try:
        a, b = map(int, input().split())
        print(a + b)
    except EOFError:
        break
```

两种写法表达的是同一个结束条件。

---

## 8. “遇到 0 结束”不是 EOF

输入：

```text
1 2
3 4
0 0
```

如果题目规定 `0 0` 表示结束：

```python
while True:
    a, b = map(int, input().split())

    if a == 0 and b == 0:
        break

    print(a + b)
```

这里是读到了一个人为规定的**哨兵值（sentinel）**，不是输入源真的结束。

---

## 9. 常见数据怎么读

### 一行两个整数

```text
3 5
```

```python
a, b = map(int, input().split())
```

### 一维数组

```text
5
10 20 30 40 50
```

```python
n = int(input())
nums = list(map(int, input().split()))
```

题目也可能把长度和数据放成别的格式，所以永远以题面为准。

### n × m 矩阵

```text
3 4
1 2 3 4
5 6 7 8
9 10 11 12
```

```python
n, m = map(int, input().split())

matrix = []
for _ in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)
```

得到：

```python
[
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]
```

访问：

```python
matrix[row][col]
```

### 字符串

整行都是内容：

```python
s = input()
```

一行多个单词：

```python
words = input().split()
```

如果字符串中的空格本身是内容，就不能先 `.split()`。

---

## 10. 图的输入：先认识“点和边”

例如：

```text
4 3
1 2
2 3
2 4
```

如果题目说：

```text
4 个点
3 条边
```

可以先把边读进来：

```python
n, m = map(int, input().split())

edges = []
for _ in range(m):
    u, v = map(int, input().split())
    edges.append((u, v))
```

第 05、06 章再把它转换成邻接表并做 DFS / BFS。

图题输入不是固定模板；有向、无向、带权等都会改变含义。

---

## 11. 树没有统一的“ACM 输入模板”

LeetCode 二叉树经常直接给 `TreeNode`，但 ACM 题可能通过：

- 父子边；
- 层序序列；
- 前序 / 中序；
- 每个节点的左右孩子编号；
- 普通树的边；

来描述树。

所以不要背“树 = 某一句 input 模板”。先问：

> **这道题究竟用什么数据描述这棵树？**

---

## 12. 输出

### 输出一个列表

```python
nums = [1, 3, 5]
print(*nums)
```

输出：

```text
1 3 5
```

### 保留两位小数

```python
x = 3.1415926
print(f"{x:.2f}")
```

输出：

```text
3.14
```

输出格式也是正确性的一部分。算法算对了，但多了提示文字、少了空格或精度不对，同样可能 Wrong Answer。

---

## 13. 推荐的 `solve()` 结构

```python
def solve():
    n = int(input())
    nums = list(map(int, input().split()))

    answer = sum(nums)

    print(answer)


if __name__ == "__main__":
    solve()
```

当前只需理解：

```text
solve()
→ 把这道题的完整流程集中起来

if __name__ == "__main__":
→ 这个文件被直接运行时调用 solve()
```

更完整的模块语义回 [Python Foundation 09](../../../curriculum/01-python/docs/09-异常-文件-模块与导入.md) 学。

---

## 14. 大量输入：先知道还有“快读”

当数据很多时会看到：

```python
import sys

data = list(map(int, sys.stdin.buffer.read().split()))
```

它会一次读取剩余输入并拆成 token。

初学阶段不要所有题都强行写这种形式。**先把输入结构读懂，再谈 I/O 性能。**

---

## 15. Hot100 ACM 改写：两数之和

假设我们为练习规定：

```text
第一行：n target
第二行：n 个整数
```

输入：

```text
4 9
2 7 11 15
```

完整程序：

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

    i, j = two_sum(nums, target)
    print(i, j)


if __name__ == "__main__":
    solve()
```

算法并没有变，只是在外面补了：

```text
stdin → parse → algorithm → stdout
```

---

## 16. 哪些 Hot100 适合 ACM 改写

特别适合：

- 数组；
- 字符串；
- 矩阵；
- 图 / 网格；
- 数值 DP。

例如：

```text
1 两数之和
3 无重复字符的最长子串
53 最大子数组和
54 螺旋矩阵
200 岛屿数量
70 爬楼梯
```

不要求所有链表 / 二叉树题都改成 ACM。为了输入构造花大量时间，可能反而抢走当前算法目标。

---

## 17. 常见 ACM 错误

- 多打印“答案是”之类提示文字；
- 把第一行的 `T` 当作真正待计算数据；
- 明明是 EOF，却只调用一次 `input()`；
- 字符串包含空格却先 `.split()`；
- 把矩阵的行数 `n`、列数 `m` 搞反；
- 输出格式与题目不一致；
- 输入解析和算法逻辑混成一团，Debug 时找不到错误在哪一层。

能分离时尽量维持：

```text
parse
→ solve
→ print
```

---

## 18. 外部练习顺序

先完成专门的输入输出训练：

1. 牛客输入输出练习：<https://www.nowcoder.com/exam/oj?page=1&tab=%E7%AE%97%E6%B3%95%E7%AC%94%E9%9D%A2%E8%AF%95%E7%AF%87&topicId=372>
2. CodeFun ACM：<https://codefun2000.com/acm>

目标不是刷算法，而是见到下面这些词不再陌生：

```text
单组
T 组
EOF
哨兵结束
数组
矩阵
字符串
多行
格式化输出
```

然后从已经做过的 Hot100 里挑数组 / 字符串 / 矩阵题做 ACM 改写。

---

## 19. Exit Gate

你应该能不用查模板解释并写出：

- `input()` 为什么返回字符串；
- `split()` 之后是什么；
- `map(int, ...)` 在做什么；
- `list(map(int, input().split()))` 每一步发生什么；
- 单组输入；
- T 组输入；
- EOF；
- 哨兵结束；
- 一维数组；
- n×m 矩阵；
- 带空格字符串；
- 多条边；
- `print(*nums)`；
- 一个清晰的 `solve()`；
- 把已经会的“两数之和”变成完整 stdin → stdout 程序。

做到这里，“ACM 模式”应该只剩一句话：

> **算法之外，输入输出也由我负责。**

---

下一章：[05. Data Structures](05-data-structures.md)
