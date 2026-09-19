# Market｜AI Application / Agent 招聘市场证据层

[↑ Handbook 总目录](../README.md) · [Canonical Questions](../interview/canonical/README.md) · [Knowledge Map](../guide/knowledge-map.md)

> Market 回答两个问题：**公司正在招什么？真实面试正在问什么？**

## 1. 两种核心原始证据

### Jobs / JD

[AI Application & Agent 非算法岗位市场库](jobs/ai-agent-jd-market.md)

用于观察：

- 岗位名称与 Role Scope；
- 技术栈与工程职责；
- Agent / RAG / Backend / Full-stack 的边界；
- 市场需求随时间的变化。

维护规则：持续发现候选岗位、全库去重、来源升级、过期复核与删除。

### HUMAN-A Interviews

[真人面经目录](interviews/)

正式 HUMAN-A 必须满足：

```text
候选人本人第一人称
+ 真人面试官 / 真实招聘流程
+ 高信息密度
+ 目标 AI Application / Agent Role Scope
+ 正文稳定可核验
+ 非转载 / 非答案帖 / 非重复
```

**HUMAN-A 正式库：S001–S288 / 29 Batch。** 候选来源先进入 Market 证据层并完成质量与去重检查；单日热点不直接改变 Curriculum。

## 2. Market 内部结构

```text
market/
├── jobs/         # 原始岗位 JD 与持续维护
├── interviews/   # HUMAN-A 独立招聘流程
├── analysis/     # 频率、覆盖、追问链、Gap 等分析
├── monitoring/   # Inbox / Daily Log
└── policies/     # Source Quality / Role Scope 规则
```

## 3. 去重与质量原则

- JD：同公司 + 同岗位主体 + 高度相同职责只保留一条，优先官方来源。
- 面经：同候选人 + 同公司 + 同招聘流程的多轮合并为一个 Source。
- 搜索“0 命中”不能证明未收录；正式入库前必须回读历史做去重。
- 不为数量降低 Gate。

详细规则：

- [Source Quality Policy](policies/source-quality-policy.md)
- [Role Scope Policy](policies/role-scope-policy.md)
- [Market Analysis](analysis/README.md)

## 4. 与其他层的关系

```text
Market JD      → 公司声称需要什么
Market HUMAN-A → 面试实际验证什么
      ↓
Interview Canonical → 归一化成稳定能力
      ↓
Curriculum → 调整复习深度，不破坏知识依赖

References → 校准技术事实，但不创造市场频率
```
