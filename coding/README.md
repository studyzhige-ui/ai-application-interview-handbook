# Coding & Problem Solving｜从会看代码到能独立完成笔试与 AI Coding

[← Handbook 总目录](../README.md) · [Learning Path](../roadmap/learning-path.md) · [Hot100 映射表](hot100-map.md) · [Python Foundation](../python/README.md)

> **状态：V1 ✅**
>
> 这是一条横向实践能力轨道，不把自己伪装成第 11 个知识模块。十个正式模块回答“需要懂什么”；Coding 轨道回答“能不能从空白文件开始，把问题真正写成可运行、可验证的代码”。

---

## 1. 为什么需要单独的 Coding 轨道

只学习 Python、FastAPI、RAG、Agent 等知识，并不会自动获得稳定的编程基本功。

一个人可能已经能解释：

- Python 对象模型；
- dict / GIL / asyncio；
- RAG Pipeline；
- Agent Memory / Context / Tool Runtime；

但仍然会在下面这些地方卡住：

```text
input() 为什么读到的是字符串？
split() 到底把什么拆开？
T 组输入是什么意思？
EOF 是什么？
怎么从题目描述变成循环和变量？
为什么需要 dict，而不是“因为题解这么写”？
怎么自己定位 IndexError / KeyError？
LeetCode 会写函数，为什么笔试不会写完整程序？
AI 生成了一堆代码，我怎么判断它真的对？
```

这些问题属于 **Coding Skill / Problem Solving Skill**，不能靠继续背面经补齐。

所以本仓库现在明确区分两条线：

```text
Knowledge Track
Python / FastAPI / Backend / Data / LLM / RAG / Agent / System Design
→ 建立技术知识体系

Coding Track
Programming → Python Coding → ACM → DSA → Problem Solving → Hot100 → OA → AI Coding
→ 建立把知识变成代码的能力
```

两条线需要并行，而不是先把所有知识看完以后再开始写代码。

---

## 2. 本轨道的最终主线

```text
01 Programming Fundamentals
程序怎样执行，变量、判断、循环、函数、错误到底是什么
        ↓
02 Python Coding Basics
真正熟练使用 list / dict / set / str / for / 函数等写代码
        ↓
03 Basic Coding Exercises
从“看懂示例”过渡到“能从空白文件独立写出来”
        ↓
04 ACM Input / Output
stdin / stdout / input / split / T 组 / EOF / 数组 / 矩阵 / 多组数据
        ↓
05 Data Structures
数组、哈希、栈、队列、链表、树、堆、图到底解决什么操作需求
        ↓
06 Problem Solving & Algorithms
从读题、暴力解，到双指针、滑窗、DFS/BFS、回溯、二分、DP
        ↓
07 Hot100
完成剩余题目，并把前面分散学过的题重新组织成稳定算法体系
        ↓
08 Online Assessment
ACM + 算法 + 数据范围 + 边界条件 + 限时笔试 / 机试
        ↓
09 AI Coding
读陌生仓库 → 理解需求 → 让 AI 协作 → 修改 → 测试 → Debug → Review → 交付
```

这不是要求读完 01–06 才能碰 Hot100。Hot100 从早期就会开始出现。

---

## 3. Hot100 的固定使用原则

本轨道把 [LeetCode 热题 100](https://leetcode.cn/studyplan/top-100-liked/) 当作**贯穿式真实练习库**，而不是最后突然出现的 100 道作业。

固定规则：

```text
Hot100 适合作为当前知识点的自然例子
→ 优先使用 Hot100

Hot100 的前置知识明显超出当前阶段
→ 使用更小、更纯粹的入门例子

基础学会以后
→ 再连接回对应 Hot100
```

因此同一道题可能出现不止一次。

例如 `283. 移动零`：

```text
第一次：02 Python Coding Basics
目标：for / if / list / 原地修改的基本感觉

第二次：06 Problem Solving & Algorithms
目标：从额外数组推导双指针与 O(1) 额外空间

第三次：04 ACM / 08 OA
目标：自己读数组、输出结果、处理完整程序
```

这不是重复刷题，而是在不同认知层级重新理解同一个问题。

完整映射见：[Hot100 Curriculum Map](hot100-map.md)。

---

## 4. 9 章正式课程

| # | 章节 | 本章真正要解决的问题 |
|---:|---|---|
| 01 | [Programming Fundamentals](docs/01-programming-fundamentals.md) | 程序如何执行？变量、表达式、判断、循环、函数、输入输出和报错分别是什么？ |
| 02 | [Python Coding Basics](docs/02-python-coding-basics.md) | 怎样真正使用 Python 容器、循环、索引和函数写出小程序，而不是只认识语法？ |
| 03 | [Basic Coding Exercises](docs/03-basic-exercises.md) | 怎样从“看得懂”迈到“不给模板也能写出来”？ |
| 04 | [ACM Input / Output](docs/04-acm-input-output.md) | LeetCode 函数模式和笔试完整程序模式差在哪里？T、EOF、矩阵输入到底是什么？ |
| 05 | [Data Structures](docs/05-data-structures.md) | 为什么会有数组、哈希、栈、队列、链表、树、堆和图？各自在解决什么操作成本？ |
| 06 | [Problem Solving & Algorithms](docs/06-problem-solving-and-algorithms.md) | 拿到陌生题，怎样从暴力解一步步推导到可接受的算法，而不是猜模板？ |
| 07 | [Hot100](docs/07-hot100.md) | 怎样把已经穿插完成的 Hot100 收口成稳定、可复现、能解释的算法体系？ |
| 08 | [Online Assessment](docs/08-online-assessment.md) | 怎样把算法能力迁移到牛客等真实 ACM 笔试 / 机试环境？ |
| 09 | [AI Coding](docs/09-ai-coding.md) | 怎样在陌生代码库里借助 AI 完成需求分析、实现、测试、Debug 和 Review？ |

额外只有一张导航表：[hot100-map.md](hot100-map.md)。本轨道**不会**为 100 道题再制造 100 个 Markdown。

---

## 5. Coding 与 Python Foundation 的边界

两个目录会互相引用，但职责不同。

### [python/](../python/README.md) 负责“语言是什么”

例如：

- 对象、引用和身份；
- 可变 / 不可变；
- list / dict 的机制与成本；
- 函数、作用域、闭包；
- 迭代器、生成器；
- 异常、模块；
- GC / GIL；
- async / await。

### coding/ 负责“怎么真正用它解决问题”

例如：

- 从空白 `.py` 文件开始写程序；
- 读输入、打印输出；
- 循环遍历一个数组；
- 用 dict 做查找和计数；
- 从暴力解推导优化；
- Debug；
- 完成 Hot100；
- 完成 ACM 笔试；
- 阅读陌生仓库并和 AI Coding Agent 协作。

遇到语言机制问题，回 Python；遇到“我知道概念但写不出来”，回 Coding。

---

## 6. 初学者的固定学习动作

每一个 Coding 知识点至少经过下面六步：

```text
1. Read       看懂一个最小例子
2. Trace      手工追踪每一步变量怎么变化
3. Run        自己运行，确认真实输出
4. Modify     改输入 / 改条件，观察行为
5. Rebuild    关掉答案，从空白文件重新写
6. Explain    用自己的话解释为什么这样写
```

算法题再加三步：

```text
7. Brute Force   先得到一个正确但可能慢的办法
8. Optimize      找瓶颈，再选择数据结构 / 算法
9. Test          正常样例 + 边界 + 极端数据
```

**“看懂题解”不等于“会做”。**

---

## 7. 推荐学习方式：知识线与 Coding 线并行

不要使用下面这种顺序：

```text
先把 Python 13 章全部看完
→ 几周后再第一次认真写代码
```

更推荐：

```text
Python 正文学习一点
        ↕
Coding 01–03 立即把最基本语法写起来
        ↓
Coding 04 学会完整输入输出
        ↓
Coding 05–06 和 Python 数据结构知识互相连接
        ↓
Hot100 按知识依赖持续解锁
```

第一次学习时，不要求同时追求：

- 最短代码；
- 最优解；
- 一遍 AC；
- 记住所有模板。

先建立“我知道每一行为什么存在”的能力。

---

## 8. Hot100 不是一道一道孤立推进

本轨道不采用“官方列表从第一题机械刷到第 100 题”作为唯一顺序。

官方题单本身按哈希、双指针、滑动窗口、数组、矩阵、链表、二叉树、图、回溯、二分、栈、堆、贪心、动态规划等专题组织。这里进一步按**前置知识**重排第一次接触的位置。

一题建议保留四种状态：

```text
L = Learned
已经理解题意、数据结构和参考解法

S = Solved
关掉答案能独立写出并通过

A = ACM
适合的题已经改写成完整 stdin → solve → stdout

R = Recall
隔一段时间随机抽到仍能说出思路并重写关键代码
```

不是每一道题都必须做 ACM 改写。链表、树等题如果输入构造本身会抢走当前学习目标，就保留 LeetCode 形式。

---

## 9. 外部练习入口

### Hot100

- LeetCode 热题 100：<https://leetcode.cn/studyplan/top-100-liked/>

本仓库只维护学习顺序、知识映射与方法，不复制官方题面。

### ACM 输入输出

- 牛客算法笔面试篇 / 输入输出练习：<https://www.nowcoder.com/exam/oj?page=1&tab=%E7%AE%97%E6%B3%95%E7%AC%94%E9%9D%A2%E8%AF%95%E7%AF%87&topicId=372>
- CodeFun ACM 模式：<https://codefun2000.com/acm>

### AI Coding

- 牛客 AI 新题型篇：<https://www.nowcoder.com/exam/oj?page=1&tab=AI%E6%96%B0%E9%A2%98%E5%9E%8B%E7%AF%87&topicId=-9001>
- 牛客 AI Coding 题库：<https://www.nowcoder.com/problem/aicoding/?channelPut=www_oj_aicoding>

这些平台内容会变化。本 V1 在 **2026-09-18** 核对了入口与 Hot100 当前题单；仓库不把外部题库的动态题量写成永久事实。

---

## 10. Coding Exit Gate

完成 V1 主线后，目标不是“刷过很多题”，而是至少具备下面的可调用能力：

- 能从空白 `.py` 文件开始写一个小程序；
- 能解释 `input()` / `split()` / `map()` / `list()` 的数据变化；
- 能区分单组、T 组、EOF；
- 能读数组、矩阵、普通字符串和边列表；
- 能熟练使用 list / dict / set / deque / heapq 的基本操作；
- 能说出常见数据结构为什么存在，而不是只背名字；
- 面对陌生算法题先写出朴素解并分析瓶颈；
- 能解释时间复杂度和空间复杂度；
- 能完成 Hot100 的系统训练，而不是只记答案；
- 能把适合的 LeetCode 题改成 ACM 完整程序；
- 能读 traceback 并定位常见错误；
- 能阅读陌生 Python 项目中的入口、模块、测试与数据流；
- 能让 AI 协助调查 / 修改，但会检查 diff、运行测试并验证最终行为。

---

## 11. V1 的范围与后续原则

V1 已固定：

```text
9 章主线
+ 1 张 Hot100 全量映射表
+ 与根 README / Knowledge Map / Learning Path 的导航接入
```

暂时不做：

- 100 道 Hot100 的重复题解仓库；
- 按公司复制大量版权题面；
- 为每个小练习单独创建文件；
- 用“AI 能写”替代基础 Coding。

后续迭代应该由真实学习反馈驱动：哪一章仍有知识跳跃、哪一道练习太陡、哪些 Hot100 首次出现得过早，再调整顺序；不因为“看起来内容更多”就继续增加文档。

---

下一章：[01. Programming Fundamentals](docs/01-programming-fundamentals.md)
