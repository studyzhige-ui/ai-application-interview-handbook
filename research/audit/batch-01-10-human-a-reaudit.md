# Batch 01–10 HUMAN-A Re-audit

更新日期：2026-09-09

## 为什么需要重新审计

前 10 个 Batch 的采集标准是在研究过程中逐步演进的，并非一开始就采用当前的 HUMAN-A 硬门槛。

早期阶段为了扩大召回，曾主动保留整理 / 合集、低信息密度第一人称、二次创作、短视频线索、待核实来源、自动化 AI 面试以及岗位边界较宽的样本。

现在统一改为：

> **来源平台可以不同，但准入标准只有一套。只有真人面试官 + 候选人本人 A 级第一人称 + 目标 AI 岗位 + 可稳定核验 + 非重复，才能留下。**

## 当前唯一 Core 标准

每个历史来源都必须同时通过：

- **H — Human Interviewer**：真人面试官，不是 AI 自动面试 / 模拟面试；
- **F — First-person**：候选人本人第一人称复盘；
- **A — A-grade Quality**：问题密度高，有自然现场痕迹、追问、回答状态或结果；
- **R — Role Scope**：AI Application / Agent / RAG / AI Backend / AI Full-stack / Agent Runtime 等目标方向；
- **D — Deduplicated**：不是同一场面试的转载 / 合集重复；
- **V — Verifiable**：正文与元数据可以稳定核验。

只有 `H + F + A + R + D + V` 全部通过，状态才是 `KEEP_CORE`。

## 平台无差别

牛客、小红书、知乎、脉脉、Bilibili、抖音、CSDN、个人博客等全部执行同一标准。

- 平台不会提供质量加分；
- 非牛客来源只要能稳定核验，也可以成为 HUMAN-A；
- 牛客来源如果是合集、题库、低密度或自动面试，同样排除。

## 审计输出状态

- `KEEP_CORE`：进入 HUMAN-A Core；
- `EXCLUDE_AUTOMATED`：AI 自动面试或非真人面试；
- `EXCLUDE_NOT_FIRST_PERSON`：整理、合集、搬运、题库；
- `EXCLUDE_LOW_DENSITY`：信息量不足；
- `EXCLUDE_ROLE_SCOPE`：岗位不属于目标方向；
- `EXCLUDE_DUPLICATE`：同场转载 / 重复来源；
- `EXCLUDE_UNVERIFIABLE`：无法稳定核验正文、元数据或真人属性；
- `NEEDS_EVIDENCE`：暂时证据不足，等待原帖；在证据补齐前视同非 Core。

## 已知不符合当前 Core 的历史来源

在完整回审开始前，已有明确案例：

- Batch 03：`S032` 明确为整理 / 合集；
- Batch 04：`S043–S045` 明确为整理 / 待核实；
- Batch 05：包含大量二次创作、整理合集、低信息密度短视频和问题信号；
- Batch 09：包含明确 B 级来源，需要重新验证或排除；
- Batch 10：`S119` 为自动化 AI 面试，明确排除。

因此历史 `S001–S128` 不能直接等价为真人高质量面经。

## canonical questions：重新构建，不再保留低质量来源独占问题

此前的策略是：即使来源不进入 Core，canonical question 也可以作为“知识发现”继续保留。

这个策略取消。

新的规则是：

1. 每一道活跃 canonical question 至少要有一个 `KEEP_CORE` HUMAN-A 来源；
2. 如果一道历史 canonical question 的所有来源都被排除，该问题直接从活跃题库删除；
3. 如果它同时有 HUMAN-A 与低质量来源，只保留 HUMAN-A 证据，删除非 Core 命中；
4. 低质量来源提出的“独特高级问题”也不例外，不因为问题本身有趣而保留；
5. 领域知识是否应该学习，由完整课程体系决定，不由低质量面经兜底；
6. canonical question 的职责只剩一个：**记录真实高质量真人面试到底怎么问。**

因此最终关系是：

```text
知识体系
└── 从 0 建立完整覆盖

HUMAN-A 真人面经
└── 提供真实问法 / 频率 / 深挖方向

低质量来源
└── 不进入知识体系，不进入题库，不参与 Gap Analysis
```

## 历史 Batch 文件处理

Git 历史本身已经保存研究过程，所以当前仓库没有必要继续把已确认低质量条目留在活跃研究目录里。

回审完成后：

- 对 `KEEP_CORE` 来源保留原 `Sxxx`，允许 ID 不连续；
- 对明确 `EXCLUDE_*` 来源，从活跃 Batch 内容中删除或迁出；
- 不为了保持编号连续而保留污染数据；
- 重新生成一份 `research/interviews/human-a-index.md` 作为唯一正式来源索引；
- 重新生成 HUMAN-A-only canonical question 库。

## 审计顺序

1. Batch 01–05：污染风险最高；
2. Batch 06–08：标准已收紧但仍逐条核验；
3. Batch 09–10：清理 B 级、自动化与证据不足来源；
4. 重建 HUMAN-A Core 来源清单；
5. 清洗 canonical questions，只保留有 HUMAN-A 证据的问题；
6. 重算真人命中数 / 公司数 / 轮次分布；
7. 再继续后续 Batch 搜集和课程优先级分析。

## 最终原则

> **我们的知识体系负责“学什么”，HUMAN-A 面经负责“企业真人到底怎么问”。低质量来源两边都不需要。**

宁可删除大量历史题目和来源，也不要让数据膨胀反过来增加学习负担。
