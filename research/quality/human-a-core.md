# HUMAN-A Core Dataset

更新日期：2026-09-09

从 Batch 11 起，本项目用于“真人面试频率 / 公司 / 轮次 / 课程优先级”分析的正式核心数据集只接受：

> **Human Interviewer + A-grade First-person + Role Scope Gate**

完整准入规则见 [`source-quality-policy.md`](./source-quality-policy.md)。

## 明确排除

- `S119`：去哪儿旅行 AI 全栈方向，候选人记录真实，但面试官为自动化 AI 系统。问题可以作为历史研究信号保留，但 **不属于 HUMAN-A Core，不参与真人面试频率统计，也不能单独推动课程优先级**。

## 历史批次处理

Batch 01–10 在研究早期曾主动保留 B/C/D/E、整理帖和跨平台信号，以扩大问题召回。为了保持已有 `Sxxx` 稳定引用，不强行重编号或删除历史研究文件。

后续统计时采用两层视图：

```text
Historical Research Records
    └── 早期 A/B/C/D/E / leads / automated 等

HUMAN-A Core
    └── 真人 + 第一人称 A 级 + 目标 AI 岗
```

当后续开始正式做全量频率矩阵时，会逐条回审 Batch 01–10，只把满足当前 HUMAN-A 标准的历史来源纳入 Core。

## Batch 11 起的承诺

新的正式 Batch 不再写入：

- 自动化 AI 面试；
- B 级低信息密度分享；
- 合集 / 整理 / 搬运；
- `含完整答案` / 标准答案 / 模拟题；
- 无法稳定核验的跨平台帖子。

因此，Batch 11 及之后的新增正式 `Sxxx` 默认就是 HUMAN-A，除非未来审计发现来源证据有问题并显式降级。
