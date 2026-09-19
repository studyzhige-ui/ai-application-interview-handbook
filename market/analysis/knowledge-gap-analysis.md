# Knowledge Gap Analysis｜Current Market Evidence × Curriculum

[← Market Analysis](README.md) · [↑ Market](../README.md) · [Curriculum](../../curriculum/README.md) · [历史 Phase 2B Gap](history/phase-2b-knowledge-gap-analysis-2026-09-11.md)

快照日期：2026-09-19

> 本文件只回答“当前还缺什么”。2026-09-11 的 Phase 2B 建课阶段 Gap 已归档；已经解决的旧缺口（LLM 一级模块、Vector/RAG 边界、MySQL 等未建教材）不再作为当前任务重复出现。

## 1. 当前基线

```text
Curriculum           10 modules / 185 blocks / V1
Frozen Canonical     S001–S279 / 235 ACTIVE
Market HUMAN-A       S001–S288 / 29 Batch
Pending Evidence     S280–S288（9 flows，等待 periodic Canonical review）
JD Market            47 detailed non-algorithm JDs（2026-09-19 初始基线）
```

完整知识体系仍决定第一次学习顺序；Market / Canonical 负责校准真实岗位需求、问法与深度。

## 2. P0｜没有新的 Curriculum 结构缺口

当前十个正式模块均存在完整正文、Review 与 Interview 使用层：

```text
Python → FastAPI → AI Backend
→ MySQL → Redis → Vector DB
→ LLM Foundation → RAG → Agent → System Design
```

因此当前不需要新增第 11 个知识模块，也不应因为短期热点重新拆散现有主线。

## 3. P1｜S280–S288 尚未进入 Canonical 周期审查

Market 已继续增长，但 Frozen Canonical 仍停在 S279。这是**有意的节奏差**，不是数据错误。

下一次 periodic review 需要：

1. 对 S280–S288 回读并映射现有 Canonical；
2. 识别真正无法映射的新能力；
3. 检查是否达到新增 / Merge / Split Canonical 的证据门槛；
4. 重新生成 Frequency / Depth / Coverage；
5. 只有完成上述步骤后才改变 Frozen Baseline。

近期 Market Observation 包括 Side-effect / Write Safety、Long-task Harness、Framework Extension Boundary、Eval Gate / Review Agent、AI-assisted Engineering Verification；这些在 review 前只作为市场观察，不直接改教材。

## 4. P1｜Bridge Labs 尚未形成正式实践层

当前 Curriculum 分模块学习已经完整，但真实岗位会把能力组合起来。

建议正式建设至少四类 Bridge Lab：

```text
A. FastAPI + Async LLM Service
B. MySQL + Redis + MQ Reliable Backend
C. Vector DB + RAG Evaluation Pipeline
D. RAG + Agent Harness + Long-running Runtime
```

Bridge Lab 应进入 Practice / 使用层，而不是再增加 Curriculum 模块。

## 5. P1｜Cross-module Mock Interview 尚未产品化

真实面试常从项目入口跨模块追问：

```text
RAG quality
→ Vector retrieval
→ Backend timeout
→ Redis state
→ Agent recovery
→ System Design scale
```

当前已有 Verified Follow-up Chain 证据，但还缺一套可重复训练的跨模块 Mock 流程、评分标准与复盘模板。

## 6. P1｜JD Market 需要持续提升 Recall 与 Freshness

岗位库已经建立，但公开招聘互联网天然动态：

- 官方岗位持续上下线；
- 同一岗位存在城市 / 批次 / 镜像重复；
- 部分招聘平台只暴露摘要；
- “Agent 工程”与“Agent 算法”职位标题可能接近。

因此岗位层的目标不是声明绝对 100% 全量，而是持续：

```text
发现 → 官方来源优先 → 全库去重
→ 过期复核 → 删除失效 → 来源升级
```

每周二、周五的岗位维护任务负责这一层。

## 7. P2｜References 可按需求扩展

当前集中 Reference Index 已覆盖 Agent、FastAPI、AI Backend Engineering。MySQL / Redis / Vector DB / LLM / RAG 等模块的权威来源仍主要分散在正文。

这不影响 Curriculum 正确性，但后续若需要更强的版本追踪与事实审计，可以逐模块建立独立 Reference Index；不以“目录对称”作为必须扩展的理由。

## 8. 当前优先级

```text
1. 持续 Market HUMAN-A / JD 监测
2. 周期性处理 S280+ Canonical mapping
3. 建 Bridge Labs
4. 建 Cross-module Mock Interview
5. 按需要扩展 References
```

> **当前主要 Gap 已从“缺教材”转向“持续市场证据如何周期性进入面试模型，以及怎样把完整知识转化为跨模块实践能力”。**
