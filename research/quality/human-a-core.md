# HUMAN-A Core Dataset

更新日期：2026-09-09

本项目用于“真人面试频率 / 公司 / 轮次 / 课程优先级”分析的核心数据集，只接受：

> **Human Interviewer + A-grade First-person + Role Scope Gate**

也就是说：

1. 必须是真人面试官与候选人的真实技术面 / Leader 面；
2. 必须是候选人本人第一人称复盘，且有足够现场痕迹和技术细节；
3. 必须属于 AI Application / Agent / RAG / AI Backend / AI Full-stack / Agent Runtime 等目标岗位；
4. 不能只是合集、二次整理、模拟题、标准答案、自动 AI 面试、低信息密度短视频或无法核验的转载。

完整准入规则见 [`source-quality-policy.md`](./source-quality-policy.md)。

## 历史批次的重要修正

Batch 01–10 的采集标准是在研究过程中逐步收紧的，因此这些批次中的 `Sxxx` **不能因为当时被写入正式 Batch、甚至被标记为 A，就自动视为 HUMAN-A Core**。

历史来源必须逐条重新打开原始页面并通过当前标准复核后，才能进入 HUMAN-A Core。

在回审完成前：

- `S001–S128` 统一视为 **Historical Research Records / 待回审**；
- 不使用“历史总来源数”直接代表真人高质量面试样本数；
- 不基于未回审来源计算真人面试频率、公司频率和课程优先级；
- 由这些来源建立的 canonical question 可以继续保留为知识分类，但若没有 HUMAN-A 证据支撑，则不能仅凭历史来源声称“真实真人面试高频”。

## 已知明确排除案例

以下历史记录无需等待进一步审计即可确认不属于 HUMAN-A Core：

- `S119`：去哪儿旅行 AI 全栈方向，候选人记录真实，但面试官为自动化 AI 系统。
- Batch 03 中明确标注为 `整理/合集` 的来源，例如 `S032`。
- Batch 04 中明确标注为 `整理/待核实` 的 `S043–S045`。
- Batch 05 中的 `面试题信号/二次创作`、整理合集和低信息密度短视频来源；这些只属于历史问题发现层，不属于 HUMAN-A Core。
- Batch 09 中明确标注为 B 级、公司/场次信息不足或低信息密度的来源，需要排除或重新核验，不能自动进入 Core。

这些 ID 为保持引用稳定不会删除或重编号，但后续核心统计会过滤掉。

## 两层数据视图

```text
Historical Research Records
    └── 早期 A/B/C/D/E / leads / automated / 待核实等

HUMAN-A Core
    └── 真人 + 第一人称 A 级 + 目标 AI 岗 + 已逐条复核
```

## Batch 11 起的准入承诺

从 Batch 11 起，新增正式来源按 HUMAN-A 标准采集，不再主动写入：

- 自动化 AI 面试；
- B 级低信息密度分享；
- 合集 / 整理 / 搬运；
- `含完整答案` / 标准答案 / 模拟题；
- 无法稳定核验的跨平台帖子。

但“Batch 11+ 默认符合”不等于永久免审：如果未来发现来源证据不足、并非真人或不是第一人称，应显式降级并从 Core 移出。

## 下一步

对 Batch 01–10 执行一次完整的 **Human-A Re-audit**：

1. 重新打开每个原始 URL；
2. 判断是否为真人面试；
3. 判断是否为候选人本人第一人称；
4. 判断信息密度和现场痕迹；
5. 判断岗位范围；
6. 判断是否转载 / 合集 / 同场跨平台重复；
7. 输出 `KEEP / EXCLUDE / NEEDS_EVIDENCE`；
8. 重新生成 HUMAN-A 核心来源数和 canonical question 证据矩阵。
