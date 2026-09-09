# Batch 01–10 HUMAN-A Re-audit

更新日期：2026-09-09

## 为什么需要重新审计

前 10 个 Batch 的采集标准是在研究过程中逐步演进的，并非一开始就采用当前的 HUMAN-A 硬门槛。

早期阶段为了扩大召回，曾主动保留：

- 整理 / 合集；
- 低信息密度第一人称；
- 面试题信号 / 二次创作；
- 短视频线索；
- 待核实来源；
- 自动化 AI 面试；
- 与目标岗位相邻但不完全一致的样本。

这些内容对“发现知识边界”有价值，但不能与真人、高质量、第一人称面经等权，更不能用于真实面试频率统计。

## 当前唯一 Core 标准

每个历史来源都必须同时通过：

- **H — Human Interviewer**：真人面试官，不是 AI 自动面试 / 模拟面试；
- **F — First-person**：候选人本人第一人称复盘；
- **A — A-grade Quality**：问题密度高，有自然现场痕迹、追问、回答状态或结果；
- **R — Role Scope**：AI Application / Agent / RAG / AI Backend / AI Full-stack / Agent Runtime 等目标方向；
- **D — Deduplicated**：不是同一场面试的转载 / 合集重复。

只有 `H + F + A + R + D` 全部通过，状态才是 `KEEP_CORE`。

## 审计输出状态

- `KEEP_CORE`：进入 HUMAN-A Core，参与真人频率 / 公司 / 轮次统计。
- `EXCLUDE_AUTOMATED`：AI 自动面试或非真人面试。
- `EXCLUDE_NOT_FIRST_PERSON`：整理、合集、搬运、题库。
- `EXCLUDE_LOW_DENSITY`：信息量不足，无法作为高质量核心证据。
- `EXCLUDE_ROLE_SCOPE`：不属于目标 AI Application / Agent 岗。
- `EXCLUDE_DUPLICATE`：同场转载 / 重复来源。
- `NEEDS_EVIDENCE`：目前证据不足，需要找到原帖或更多上下文。

## 已知不符合当前 Core 的历史来源

在完整回审开始前，已有以下明确案例：

- Batch 03：`S032` 明确为整理 / 合集。
- Batch 04：`S043–S045` 明确为整理 / 待核实。
- Batch 05：包含大量 `面试题信号 / 二次创作`、整理合集和低信息密度短视频；这些不进入 Core。
- Batch 09：包含明确 B 级来源，需要重新验证或排除。
- Batch 10：`S119` 为自动化 AI 面试，明确排除。

因此，历史 `S001–S128` 不能直接等价为“128 场真人高质量面经”。

## 对 canonical questions 的处理

不删除已有 canonical ID，以避免破坏知识体系和引用；但把“知识是否值得学习”和“真人面试频率证据”分开：

```text
Canonical Question
├── Knowledge Coverage
│   └── 这个知识点是否属于完整课程体系
└── Interview Evidence
    ├── HUMAN-A Core 命中数
    ├── 历史非 Core 信号数
    └── 当前证据状态
```

如果一道题目前只来自非 Core 来源：

- 可以因为知识体系本身需要而继续保留；
- 不能标记成“真人高频”；
- 后续搜索优先寻找独立 HUMAN-A 证据。

## 审计顺序

为了避免继续在污染数据上做统计，优先级如下：

1. Batch 01–05：污染风险最高，先审；
2. Batch 06–08：标准已明显收紧，但仍重新核验；
3. Batch 09–10：重点处理 B 级与自动化来源；
4. 重建 HUMAN-A Core 清单；
5. 重算 canonical question 的 HUMAN-A 命中；
6. 再继续做频率 / 公司 / 轮次 / 学习优先级分析。

## 原则

> **宁可核心样本数量变少，也不要让“看起来像真实面经”的内容污染我们的学习优先级。**

历史文件不会删除，因为它们仍有研究和追溯价值；但“历史研究层”和“HUMAN-A 核心证据层”从此彻底分开。
