# 08｜Online Assessment：把算法能力迁移到真实笔试 / 机试

[← 上一章：Hot100](07-hot100.md) · [Coding 首页](../README.md) · [下一章：AI Coding →](09-ai-coding.md)

> 真实 OA（Online Assessment，在线笔试 / 机试）不是“换个平台继续 LeetCode”。它把 **输入输出、算法、数据范围、时间压力、边界处理和完整程序正确性**放在一起考。

---

## 1. OA 比 LeetCode 多了哪些责任

LeetCode 核心代码模式：

```text
平台解析输入
→ 平台构造参数
→ 你实现函数
→ 平台调用
```

ACM/OA：

```text
读题
→ 解析完整输入
→ 选择算法
→ 自己创建数据结构
→ 输出
→ 一次提交接受隐藏测试
```

所以 OA 的错误来源至少有四层：

```text
1. Parse 错
2. Algorithm 错
3. Boundary / Complexity 错
4. Output Format 错
```

不要算法一 WA 就默认“算法想错了”。

---

## 2. 做题前先读数据范围

假设：

```text
n <= 20
```

和：

```text
n <= 200000
```

允许的算法完全不同。

拿到题先圈：

```text
n / m 范围
元素值范围
是否多组
是否有负数
是否有重复
是否保证有解
时间限制
空间限制
```

这些不是题面装饰，而是解法约束。

---

## 3. 先把 Input Contract 写成变量

例如题面：

```text
第一行 n, k
第二行 n 个整数
```

先不要想算法，先确认：

```python
n, k = map(int, input().split())
nums = list(map(int, input().split()))
```

再问：

```text
len(nums) 是否应该等于 n？
多组还是单组？
k 是值、长度还是次数？
```

输入层理解清楚，算法层才有意义。

---

## 4. 推荐 OA 代码分层

简单题也尽量形成：

```python
def algorithm(nums, k):
    # 纯算法
    ...
    return answer


def solve():
    # parse
    n, k = map(int, input().split())
    nums = list(map(int, input().split()))

    # solve
    answer = algorithm(nums, k)

    # output
    print(answer)


if __name__ == "__main__":
    solve()
```

好处：

```text
输入错？
看 solve 的 parse

算法错？
单独测试 algorithm

输出错？
看最后 print
```

Debug 边界会清楚很多。

---

## 5. 本地样例不只是“复制题目样例”

题目给：

```text
5
1 2 3 4 5
```

你还应该自己想：

```text
最小 n
全相同
全负数
已经有序
逆序
重复很多
答案在最左 / 最右
无解（如果允许）
```

隐藏测试最喜欢击中：

> 你默认成立、但题目从未保证的条件。

---

## 6. Wrong Answer 时怎么排查

按层排，而不是随机改：

```text
A. 我读对输入了吗？
B. 我输出格式对吗？
C. 样例能手算一致吗？
D. 最小边界呢？
E. 重复 / 0 / 负数呢？
F. 算法 invariant 在每一步都成立吗？
G. 有溢出 / 精度问题吗？
H. 数据量大时会超时吗？
```

Python 没有普通整数的 32 位溢出问题，但仍要注意浮点精度、递归深度和内存。

---

## 7. Time Limit Exceeded 时怎么排查

先不要急着换语言。

问：

```text
复杂度是什么？

n 最大是多少？

有没有：
- 两层 O(n²)？
- list 前端反复 pop / insert？
- 在循环里反复排序？
- 在循环里构造巨大字符串？
- DFS 重复访问状态？
- 没有 memo 的重复递归？
```

如果算法复杂度本身不够，换“快读”通常救不了。

---

## 8. Python OA 常用工具箱

不是让你一次背完，只要逐步熟悉：

```python
from collections import Counter, defaultdict, deque
import heapq
import bisect
import math
import sys
```

常见用途：

| 工具 | 常见用途 |
|---|---|
| `Counter` | 频次 |
| `defaultdict` | 邻接表 / 分组 |
| `deque` | BFS / 双端队列 |
| `heapq` | Priority Queue / Top K |
| `bisect` | 有序序列二分位置 |
| `math` | 数学函数 |
| `sys.stdin` | EOF / 大量输入 |

原则：先理解普通写法，再用库让实现更稳定。

---

## 9. 把 Hot100 变成 OA 训练

不要重新找一批完全陌生题才叫“笔试训练”。

可以先把熟悉题改完整程序：

```text
3 无重复字符最长子串
53 最大子数组和
56 合并区间
54 螺旋矩阵
200 岛屿数量
207 课程表
215 第 K 大
70 爬楼梯
322 零钱兑换
```

目标是训练：

```text
题面 input contract
→ parse
→ 已知算法
→ output
```

把输入输出自动化以后，再进入公司真题 / 陌生 OA。

---

## 10. 限时训练不要一开始就追求“模拟正式考试”

建议三个阶段：

### Stage 1｜不限时正确完成

先消灭：

- ACM 输入不熟；
- Python API 不熟；
- 基础算法不会实现。

### Stage 2｜单题限时

例如给自己一个合理时间窗口，训练：

```text
读题
→ 朴素解
→ 优化
→ 实现
→ 测试
```

### Stage 3｜整场模拟

再做：

```text
多题
+ 统一时间预算
+ 不查答案
+ 提交后复盘
```

初学阶段一上来整场模拟，很可能只是连续体验不会做，并不能高效学习。

---

## 11. 整场 OA 的题目管理

开始后先快速浏览全部题目，识别：

```text
我能立即写的
需要思考但有方向的
完全陌生的
```

先拿确定性更高的分数是通用考试策略，但不要因此草率跳过题目约束。

每道题提交前做最短检查：

```text
是否多组？
输出有没有调试文字？
边界下标？
复杂度？
变量有没有读错含义？
```

---

## 12. OA 后的复盘比题量更重要

每场只记录：

```text
题目：
结果：AC / WA / TLE / 未完成

失败层：
Input / Python / Data Structure / Algorithm / Boundary / Complexity / Time Management

我第一次错误判断是什么？

下一次应该识别什么信号？
```

例如：

```text
失败：TLE

原因：
每个位置都向右重新扫描，O(n²)

下次信号：
“右侧第一个更大元素”
→ 检查是否能用单调栈保存未解决位置
```

这会把真题变成能力反馈，而不是题号收藏。

---

## 13. 外部练习入口

ACM 输入输出基础：

- 牛客算法笔面试篇：<https://www.nowcoder.com/exam/oj?page=1&tab=%E7%AE%97%E6%B3%95%E7%AC%94%E9%9D%A2%E8%AF%95%E7%AF%87&topicId=372>
- CodeFun ACM：<https://codefun2000.com/acm>

完成输入输出专项后，优先进入真实算法笔试题，而不是继续刷大量 A+B。

题库结构和具体题量会变化，本仓库不复制动态题面。

---

## 14. Exit Gate

进入 AI Coding 前，至少应该：

- 能独立读取单组 / T 组 / EOF；
- 能快速把题面 input contract 翻成 Python 变量；
- 算法函数和 I/O 能基本分离；
- 会根据 n 粗略排除明显过慢复杂度；
- WA 时能按 Input / Algorithm / Boundary / Output 分层排查；
- TLE 时先看算法复杂度而不是先怪 Python；
- 已做过一批 Hot100 ACM 改写；
- 已完成若干真实 OA / 真题并留下失败分类。

---

下一章：[09. AI Coding](09-ai-coding.md)
