# HUMAN-A Core Dataset

更新日期：2026-09-09

本项目用于真实面经、频率、公司、轮次和课程优先级分析的**唯一活跃数据集**只接受：

> **Human Interviewer + A-grade First-person + Role Scope Gate**

并且这一标准与平台无关。来源可以是牛客、小红书、知乎、脉脉、Bilibili、抖音、CSDN、个人博客或其他公开平台；只要无法通过完全相同的 HUMAN-A 标准，就不能进入 Core。

完整准入规则见 [`source-quality-policy.md`](./source-quality-policy.md)。

## HUMAN-A 必须同时满足

1. 真人面试官与候选人的真实技术面 / Leader 面；
2. 候选人本人第一人称高质量复盘；
3. 有足够现场痕迹与具体技术追问；
4. 岗位属于 AI Application / Agent / RAG / AI Backend / AI Full-stack / Agent Runtime 等目标方向；
5. 来源可稳定核验；
6. 不是转载、合集或同场跨平台重复。

## 历史批次修正

Batch 01–10 的采集标准是在研究过程中逐步收紧的，因此 `S001–S128` 必须逐条回审。

在回审完成前：

- 历史 `Sxxx` 不能直接计入 HUMAN-A Core；
- 不能用历史总来源数代表真人高质量面试样本数；
- 不能基于未回审来源计算真人频率、公司频率和课程优先级；
- 历史 canonical question 也必须重新审计其证据来源。

## 低质量来源不再保留为知识层

此前曾把低质量来源视为“知识发现信号”。这个策略从现在起取消。

原因是本项目已经明确采用：

> **完整知识体系负责覆盖领域本身，高质量真人面经负责提供血肉和真实问法。**

因此：

- 非 HUMAN-A 来源不贡献课程知识点；
- 非 HUMAN-A 来源不贡献 canonical question；
- 非 HUMAN-A 来源不参与 Gap Analysis；
- 一个历史 canonical question 如果回审后没有任何 HUMAN-A 证据，则从活跃 canonical question 库中删除；
- 即使这个问题本身“看起来很高级”，也不会因为低质量来源而保留；
- 如果它确实属于完整知识体系，应由对应模块正文自然覆盖，而不是挂着一个虚假的“真实面经问题”身份。

## 历史低质量记录如何处理

Git 历史已经天然保存研究演进过程，因此当前仓库不需要长期维护一个会干扰阅读的低质量“研究层”。

回审过程中，对明确不符合标准的历史来源：

1. 在审计表中记录排除原因；
2. 从后续 HUMAN-A 来源索引中移除；
3. 对其独占的 canonical question 执行删除；
4. 如历史 Batch 文件中混入大量低质量条目，审计完成后会重写为清洗后的版本，或明确移出活跃研究目录；
5. 不为了保持 `Sxxx` 连续而保留污染数据。ID 出现空洞可以接受，质量优先于编号美观。

## 已知明确排除案例

无需等待进一步审计即可确认不属于 HUMAN-A Core 的包括：

- `S119`：自动化 AI 面试；
- Batch 03 中明确标注为整理 / 合集的来源，例如 `S032`；
- Batch 04 中明确标注为整理 / 待核实的 `S043–S045`；
- Batch 05 中的二次创作、整理合集、低信息密度短视频、题目信号；
- 其他任何无法满足真人 + 第一人称 A 级 + 目标岗位 + 稳定核验的历史来源。

## 回审后的最终结构

```text
完整课程体系
├── Python
├── FastAPI
├── Backend Engineering
├── MySQL
├── Redis
├── Vector DB
├── RAG
└── Agent Harness

HUMAN-A Core
└── 只保存真人高质量第一人称面经
    └── 只从这些面经生成 canonical questions
```

不再保留一个“低质量面经也能贡献知识点”的中间层。

## Batch 11 起

Batch 11 及之后新增正式来源默认按 HUMAN-A 标准采集，但仍允许未来审计时降级或删除。

## 下一步

对 Batch 01–10 执行完整 Human-A Re-audit：

1. 重新打开原始页面；
2. 判断真人面试官；
3. 判断候选人本人第一人称；
4. 判断信息密度与现场痕迹；
5. 判断岗位范围；
6. 判断转载 / 合集 / 重复；
7. 输出 `KEEP_CORE / EXCLUDE_* / NEEDS_EVIDENCE`；
8. 删除无 HUMAN-A 支撑的历史 canonical questions；
9. 重建干净的 HUMAN-A 来源清单与问题证据矩阵；
10. 再继续进行频率、公司、轮次与学习优先级分析。
