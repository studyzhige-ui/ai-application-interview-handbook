# Canonical Question 数据规范

更新日期：2026-09-10

本目录把 `research/interviews/batch-01.md` ～ `batch-26.md` 中冻结的 `S001–S279` HUMAN-A 来源，归一化为可统计、可回溯、可反哺课程设计的 Canonical Question 数据集。

> 完整知识体系决定“应该学什么”；Canonical Question 只负责记录真实市场“怎么问、问多深、在哪些场景追问”。

---

## 1. 为什么按模块做“全库纵向扫描”

采集阶段已经结束，因此不再按 Batch 增量生成 `canonical-batch-xx.md`。现在改为：

```text
S001–S279 全历史
      ↓
按一个知识模块纵向扫描全部来源
      ↓
原子化真实问题
      ↓
语义聚类 / Merge-Split 审计
      ↓
模块 Canonical Questions
      ↓
跨模块二次审计
      ↓
频率 / 深度 / 课程覆盖分析
```

这样可以避免早期 Batch 与后期 Batch 使用不同归一化标准，也避免同一知识点被分散在多个增量文件里。

---

## 2. Canonical Question 的字段

每道正式问题至少维护：

| 字段 | 含义 |
|---|---|
| `QID` | 模块内稳定编号，如 `MYSQL-003` |
| `Canonical Question` | 归一化后的核心问题 |
| `Topic` | 二级知识点 |
| `Question Type` | Concept / Why / Comparison / Project / Troubleshoot / System Design / Coding / Debug / Trade-off / AI Coding |
| `Evidence Sources` | 支撑该问题的独立 HUMAN-A `Sxxx` |
| `Source Count` | `Evidence Sources` 去重后的数量 |
| `Real Wording Variants` | 来自真实面试的典型问法变体，保留语境但不机械复制 |
| `Depth` | L1 概念、L2 原理、L3 工程场景、L4 Production / Failure / System Design |
| `Curriculum Link` | 后续教材对应章节；课程未建立时可暂缺 |

最终分析阶段还会从 Source Metadata 派生：

- 独立公司数；
- 岗位 / 轮次分布；
- 时间分布；
- 高频追问链；
- 模块交叉关系。

---

## 3. Merge / Split 规则

### 3.1 可以 Merge

只有当两个真实问法在面试回答时共享同一个核心知识模型，且主要差异只是措辞 / 场景包装时才合并。

例如：

- “Redis 为什么快？”
- “Redis 单线程为什么还能这么快？”

如果后者主要追线程模型，则**不能全部并入**前者；可以让“为什么快”作为上位问题，并把线程模型保留为独立 Canonical Question。

### 3.2 必须 Split

以下情况即使关键词相同，也必须拆分：

- 一个问“是什么”，另一个问“失败时怎么办”；
- 一个问算法原理，另一个问参数 / Trade-off；
- 一个问单机，另一个问分布式；
- 一个问实现，另一个问 Evaluation；
- 一个问正常路径，另一个问 Crash / Retry / Idempotency；
- 一个问题本身就包含面试官连续追到的独立能力点。

例如：

```text
MySQL MVCC 是什么？
≠
RR 下幻读如何治理？
≠
两个并发事务逐条 SELECT / UPDATE 时会发生什么？
```

---

## 4. 频率规则

`Source Count` 只按**独立 HUMAN-A 来源**计数。

同一 `Sxxx` 中：

- 同一主题连续追问 5 次，仍只为该 Canonical Question 贡献 `1` 个来源；
- 同一候选人同一公司同一招聘流程多轮已在采集层合并，不再重复加权；
- 不同候选人的独立流程即使问法相同，分别计数。

因此：

```text
频率 = 独立真实面试流程中出现过该核心能力的次数
```

而不是字符串出现次数。

---

## 5. Depth 定义

| Level | 含义 | 例子 |
|---|---|---|
| L1 | 定义 / 基础概念 | “MVCC 是什么？” |
| L2 | 原理 / 为什么 | “ReadView 如何判断可见性？” |
| L3 | 工程场景 / Troubleshooting | “Slow SQL 怎样定位？” |
| L4 | Production / Failure / System Design | “Cache 双写过程中节点宕机如何恢复？” |

一个 Canonical Question 可以覆盖多个 Level，最终以真实来源中出现过的**最高稳定深度**标记。

---

## 6. 面试热度与课程重要度严格分离

面试频率不能决定课程边界。

后续教材同时维护两套信号：

```text
Knowledge Importance
Core / Important / Advanced

Interview Heat
🔥🔥🔥 / 🔥🔥 / 🔥 / 单点信号
```

建议热度只作为复习优先级参考：

- `>= 10` 个独立 HUMAN-A：🔥🔥🔥
- `4–9`：🔥🔥
- `2–3`：🔥
- `1`：单点真实信号，不因为频率低而自动删除

基础知识即使面经频率较低，只要它是完整知识体系的必要前置，仍进入教材。

---

## 7. 证据边界

Canonical Question 只能由正式 `S001–S279` HUMAN-A 产生证据。

以下内容不能贡献：

- 搜索摘要；
- 转载 / 二次整理；
- 标准答案 / 题库；
- 付费内容账号包装；
- 自动 AI 面试；
- Role Scope 外普通 Backend / 算法场次；
- 已从正式库删除的同场重复来源。

Canonical Question 可以被教材进一步扩展，但扩展内容必须明确属于“知识体系补全”，不能伪装成“2026 真实面试高频”。

---

## 8. 当前工作流

模块归一化顺序：

```text
MySQL
→ Redis
→ Vector DB
→ RAG
→ Agent Harness / Runtime
→ FastAPI
→ Backend Engineering
→ LLM Foundation
→ System Design
→ Coding / Debug / AI Coding
```

前五块完成后先做一次跨模块审计；所有模块完成后再生成最终市场画像与课程覆盖矩阵。
