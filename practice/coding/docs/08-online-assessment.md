# 08｜在线笔试：把算法放进完整交付约束

[← 上一章：Hot100 综合训练](07-hot100.md) · [Coding 首页](../README.md) · [下一章：AI Coding →](09-ai-coding.md)


函数已经在本地算对，提交后却收到 Wrong Answer。原因可能很小：把组数当成数组长度，漏读了一行，或者多打印了“答案是”三个字。

在线笔试 OA（Online Assessment）把这些责任放到了一起：不仅要想出算法，还要在给定时间内正确读题、读输入、处理边界并输出。**会解题与能交出完整程序，中间还有一段需要专门练习的连接。**

下面就用一道固定长度区间求和题走完整条过程。你已经学过它需要的容器、循环和输入操作，注意力可以放在这些部分怎样配合。

## 1. 先分清错误可能发生在哪一层

错误先分层，调查才有方向。输入没读对，应检查读了几行、每个字段代表什么；结果正确但格式不对，应检查输出；小数据正确而大数据超时，则需要数实际工作量。

WA（Wrong Answer）表示答案未通过，不能单凭这个结果认定是算法思路错了。TLE（Time Limit Exceeded）表示超过时限，也不能直接归咎于 Python。先拿到具体证据，再决定改哪一层。

读题时圈出 n/m 和值域、是否多组、是否允许负数与空数据、是否保证有解、允许修改输入吗、时间和空间限制。n≤20 与 n≤200000 提供的可行范围不同，但仍要结合问题结构，不用 n 猜模板。

## 2. 完整任务：区间长度固定的最大和

**本章自定义练习，不是复制某家公司的题面。** 第一行 n k，第二行恰好 n 个整数。保证 1≤k≤n，元素允许为负数。输出长度恰好为 k 的连续子数组最大和。样例输入如下，输出 9，对应 [4,5]。

```text
5 2
1 -2 3 4 5
```

先手算四个窗口的和：-1、1、7、9。每次重新加 k 个数当然正确，但相邻窗口大部分元素相同。

例如从 `[1,-2]` 移到 `[-2,3]`，旧和为 -1，只需减去离开的 1，再加上新来的 3，就得到 1。中间的 -2 不必重算。**固定长度让“移出谁、移入谁”非常明确**，所以可以只维护当前和。朴素解 O(nk)，复用以后只需线性扫描。

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

right 是新进入窗口的位置，right-k 就是这次离开的位置。先把第一个完整窗口算出来，随后每一步都用“新来的减去离开的”更新 current。

best 从第一个真实窗口的和开始，而不是从 0 开始。全负数也有合法答案，例如 `[-5,-2,-8]`、k=2 的最大和是 -7。这里不需要“元素为正”的假设，因为窗口长度固定；时间 O(n)，额外空间 O(1)。

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

## 6. 卡住时，分清是工具不熟还是思路不清

如果已经知道“每次取最早加入的一项”，却想不起函数名，缺的是队列操作；如果连应按什么顺序处理都不确定，继续查 API 也不会直接得到答案。把这两个问题分开，求助才有效。

| 已经明确的需求 | 回查时要确认什么 |
|---|---|
| 字符或数字的频次 | dict 的值代表次数；Counter 可以代做计数 |
| 按到达顺序处理 | deque 的 append 入队、popleft 出队 |
| 持续取最小优先项 | heapq 的堆顶与 push/pop，而不是全量排序 |
| 在有序数据中找边界 | bisect 返回插入点，不保证目标存在 |
| 输入到何时结束 | 是已知组数、EOF，还是题目规定的哨兵 |

第一次遇到某个不熟悉的方法，可以就地确认它接收什么、返回什么、会不会改变原对象。无需停下当前任务去学完整个库，但也不能把一个不清楚含义的调用塞进程序里碰运气。

## 7. 从单题正确到整场时间管理

先不限时正确完成，消除 API 与输入输出障碍；再对单题练读题、朴素解、优化、实现、测试的完整流程；最后做多题整场模拟，统一时间预算、减少外部提示、提交后复盘。

整场先浏览题意与限制，识别能立即写、需要思考但有方向、完全陌生的任务。先完成把握较大的题，同时为每题留下边界与输出检查时间；不要为了“抢时间”省略协议理解。

Hot100 可先选熟悉题改完整程序，如 3、53、56、54、200、207、215、70、322，随后进入真实陌生题。避免在输入尚不熟时，把算法难度与环境难度同时拉满。

## 8. 本章小结与面试怎么答

完整程序的正确性由多部分共同组成：题意理解、输入解析、算法、边界、输出格式和规模下的成本。把算法函数保持为“接收数据并返回结果”，再单独接入输入输出，会更容易定位哪一层出了问题。

**问：样例通过，但提交失败，你会怎样排查？**

> 🎯 先核对读取的行数和字段含义，再检查输出格式，然后手算最小失败样例并追踪状态。若小数据正确、大数据超时，就分析重复查找、复制和嵌套工作的总量，而不是先换语言或快读。

## 9. ⚠️ 容易混淆的地方

- 最大值初始化为 0 隐含了答案非负，可能被全负数击中。
- 多组题每组需要重新建立的状态，应在组循环内初始化。
- 对拍能发现实现不一致，不能代替正确性理由；两个实现也可能共享同一个错误假设。
- 用切片初始化和不用切片初始化，额外空间可能不同，必须按实际代码分析。

## 10. 章节自测与实践验收

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

## 11. 知识课程回看

输入与格式问题回看 [Python：文件、异常与模块](../../../curriculum/01-python/docs/09-异常-文件-模块与导入.md)；超时问题回看 [Python：数据结构与复杂度](../../../curriculum/01-python/docs/13-常见数据结构与复杂度.md)。复盘的目的，是把这次失败转成下一次可以提前检查的信号。
