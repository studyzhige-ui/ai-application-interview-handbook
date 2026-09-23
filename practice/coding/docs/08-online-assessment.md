# 08｜在线笔试：把算法放进完整交付约束

[← 上一章：Hot100 综合训练](07-hot100.md) · [Coding 首页](../README.md) · [下一章：AI Coding →](09-ai-coding.md)

> 在线笔试 OA（Online Assessment）把题意、输入输出、算法、数据范围、边界与时间预算放到一起。第 04 章已教输入协议，第 05–07 章已教结构和算法；这里通过完整任务组合它们，而不是再次引入一排陌生 API。

## 1. 先分清错误可能发生在哪一层

函数模式由平台准备参数，完整程序模式则要自己解析文字。失败可能来自输入解析、Python 操作、数据结构、算法、边界、复杂度或输出格式。看到 WA（Wrong Answer，答案错误）不要立刻随机换算法；看到 TLE（Time Limit Exceeded，超过时限）也不要先归咎于语言。

读题时圈出 n/m 和值域、是否多组、是否允许负数与空数据、是否保证有解、允许修改输入吗、时间和空间限制。n≤20 与 n≤200000 提供的可行范围不同，但仍要结合问题结构，不用 n 猜模板。

## 2. 完整任务：区间长度固定的最大和

**本章自定义练习，不是复制某家公司的题面。** 第一行 n k，第二行恰好 n 个整数。保证 1≤k≤n，元素允许为负数。输出长度恰好为 k 的连续子数组最大和。样例输入如下，输出 9，对应 [4,5]。

```text
5 2
1 -2 3 4 5
```

先手算每段：-1、1、7、9。朴素解每次重新累加 k 项，O(nk)；相邻窗口只差一个移出项与一个移入项，所以可复用当前和。这一步是从任务推导状态，不是只看到“连续”就套窗口。

```python
def max_window_sum(nums, k):
    current = 0
    for i in range(k):
        current += nums[i]
    best = current
    for right in range(k, len(nums)):
        current += nums[right] - nums[right - k]
        best = max(best, current)
    return best

assert max_window_sum([1,-2,3,4,5], 2) == 9
assert max_window_sum([-5,-2,-8], 2) == -7
assert max_window_sum([7], 1) == 7
assert max_window_sum([1,2,3], 3) == 6
```

best 不能初始化为 0，因为全负数时答案也可能为负。固定长度窗口不依赖正数假设；与“和太大就缩小”的变长窗口不同。函数 O(n) 时间、O(1) 额外空间；代码没有偷偷用 nums[:k] 创建切片。

## 3. 算法通过以后，再加输入和输出

算法函数不读取键盘、不打印，也不依赖上一次测试留下的变量。solve 负责协议。下面代码是完整程序，仍与上一节同一任务。

<!-- run: {"stdin":"5 2\n1 -2 3 4 5\n","stdout":"9\n"} -->
```python
def max_window_sum(nums, k):
    current = 0
    for i in range(k):
        current += nums[i]
    best = current
    for right in range(k, len(nums)):
        current += nums[right] - nums[right - k]
        best = max(best, current)
    return best

def solve():
    n, k = map(int, input().split())
    nums = list(map(int, input().split()))
    assert len(nums) == n and 1 <= k <= n
    answer = max_window_sum(nums, k)
    print(answer)

if __name__ == "__main__":
    solve()
```

assert 在这里用于本地验证对协议的理解，不是生产参数校验。若题目保证输入合法，提交前按平台要求处理。不要多输出提示文字，也不要把结果列表的 Python 表示当作空格分隔输出。

若题面改成第一行 T，每组先 n k 再一行数字，就把每组的读取和算法调用放到 T 循环内；若改成 EOF，则必须明确每组占几行，不能简单地对每一行独立求解。输入协议改变不意味着算法改变。

## 4. 样例之外怎样制造测试

先沿任务约束制造最小合法输入、k=1、k=n、全负数、全相同、重复值、答案在最左或最右。不要为题目保证不出现的输入擅自创造输出协议；但必须确认保证确实存在。

小规模时，用简单正确的暴力解与优化版逐个比对，称为对拍。它发现实现错误，不是代替复杂度分析或正确性证明。

```python
def brute(nums, k):
    best = sum(nums[:k])
    for left in range(1, len(nums) - k + 1):
        best = max(best, sum(nums[left:left + k]))
    return best

def fast(nums, k):
    current = sum(nums[:k])
    best = current
    for right in range(k, len(nums)):
        current += nums[right] - nums[right - k]
        best = max(best, current)
    return best

cases = [[1,-2,3], [-5,-2,-8], [0,0,0], [7], [4,1,4,1]]
for nums in cases:
    for k in range(1, len(nums) + 1):
        assert fast(nums, k) == brute(nums, k)
```

这里 fast 为了简写初始化用了切片，因此额外空间是 O(k)，不是上一节无切片版本的 O(1)。核算复杂度时必须检查实际代码，不能套用算法名字的标准结论。

## 5. WA 与 TLE 的调查顺序

WA 时先确认输入消费的行数和字段含义，再检查实际输出格式，然后手算失败样例，对照每轮状态，最后调查边界和算法依据。浮点题注意精度；Python 普通整数不受固定 32 位上限限制，但大整数、内存与递归深度仍有限制。

TLE 时先数工作量：是否反复线性查找、list 前端删除、循环里排序、复制越来越长的字符串、重复访问搜索状态、递归重复求同一个子问题。仅把 input 换成快读，不能从根本上修复不符合规模要求的平方算法。

错误日志只记录任务、实际失败、错误层、当时哪个假设不成立、下次应检查的信号。例如“best=0 默认答案非负”，比复制整段正确代码更容易迁移。

## 6. 工具回查必须指向已教过的内容

| 需求 | 工具与教学归属 |
|---|---|
| 计数与缺失项默认值 | 第 05 章 Counter、defaultdict；普通 dict 操作在第 02 章 |
| 队列、优先级 | 第 05 章 deque、heapq |
| 有序序列边界 | 第 06 章 bisect；先理解二分含义 |
| 数学函数 | 第 07 章 math 示例与任务驱动查询 |
| 单组、多组、EOF、大量输入 | 第 04 章 input、sys.stdin |

这张表只做回查，不承担首次教学。新任务出现尚未学过的基础工具时，应先补到负责该知识的章节，再把它用在组合练习中，而不是在这里写一句“自行补课”。

## 7. 从单题正确到整场时间管理

先不限时正确完成，消除 API 与输入输出障碍；再对单题练读题、朴素解、优化、实现、测试的完整流程；最后做多题整场模拟，统一时间预算、减少外部提示、提交后复盘。

整场先浏览题意与限制，识别能立即写、需要思考但有方向、完全陌生的任务。先完成把握较大的题，同时为每题留下边界与输出检查时间；不要为了“抢时间”省略协议理解。

Hot100 可先选熟悉题改完整程序，如 3、53、56、54、200、207、215、70、322，随后进入真实陌生题。避免在输入尚不熟时，把算法难度与环境难度同时拉满。

## 8. 实践验收

**练习：** 把第 2 节任务改成 T 组协议。输入 `2 / 5 2 / 1 -2 3 4 5 / 3 2 / -5 -2 -8`，输出 9、-7，各一行；斜杠仅表示换行。

<details><summary>查看完整参考答案</summary>

<!-- run: {"stdin":"2\n5 2\n1 -2 3 4 5\n3 2\n-5 -2 -8\n","stdout":"9\n-7\n"} -->
```python
def max_window_sum(nums, k):
    current = 0
    for i in range(k):
        current += nums[i]
    best = current
    for right in range(k, len(nums)):
        current += nums[right] - nums[right - k]
        best = max(best, current)
    return best

T = int(input())
for _ in range(T):
    n, k = map(int, input().split())
    nums = list(map(int, input().split()))
    assert len(nums) == n
    print(max_window_sum(nums, k))
```

</details>

能独立完成多组程序、从失败输出定位所属层、解释最大规模下的时间与空间、为边界写测试，并留下真实失败记录，才进入工程型 AI Coding。外部练习入口保留[牛客算法笔面试](https://www.nowcoder.com/exam/oj?page=1&tab=%E7%AE%97%E6%B3%95%E7%AC%94%E9%9D%A2%E8%AF%95%E7%AF%87&topicId=372)与 [CodeFun ACM](https://codefun2000.com/acm)；平台题量和界面不作为课程保证。
