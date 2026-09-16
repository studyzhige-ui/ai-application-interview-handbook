# Curriculum Granularity Audit｜教材粒度最终口径

[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Content Depth Audit](content-depth-audit.md)

> 研究粒度、能力粒度、教材文件粒度不是同一个层级。**Canonical 可以很细，但一个 Markdown 应形成完整认知闭环。**

## 固定规则

```text
HUMAN-A / Canonical Question = 面试最小可独立追问单元
Capability Primitive          = 工程机制最小单元
教材 Markdown                 = 可独立学习 / 画图 / 解释 Failure & Trade-off 的知识块
Section                       = 参数 / 变体 / Failure / 深挖追问
```

独立成文件时，主题应能回答一个完整大问题，并拥有自己的机制、Failure Model / Trade-off 和验证闭环。

## 当前最终结构

| 模块 | 研究 / 历史输入 | 当前 Curriculum | 状态 |
|---|---|---:|---|
| Python | 12-block v1 / 15 Canonical | 13 | ✅ |
| FastAPI | ~40 outline topics / 4 Canonical | 16 | ✅ |
| AI Backend Engineering | ~55 outline topics / 39 Canonical | 22 | ✅ |
| MySQL | 26 Canonical | 23 | ✅ |
| Redis | 27 old blocks / 19 Canonical | 24 | ✅ |
| Vector DB | 23 old blocks / 12 Canonical | 16 | ✅ |
| LLM Foundation | 29 old blocks / 23 Canonical | 14 | ✅ |
| RAG | 34 old blocks / 29 Canonical | 14 | ✅ |
| Agent | 23章旧课程 / 44 Canonical | 16 | 分层重构 |
| System Design | 24 Scenario Canonical | 19 | ✅ |

这些数字是结果，不是目标。教材重组永远不能改变 HUMAN-A、Source Count、Primary Ownership 或 Verified Follow-up Chain。

## 2026-09-16｜Agent 按系统职责重构

课程目录由 `agent-harness/` 改为 `agent/`；16章是唯一正式主线，原 architecture 笔记组吸收后移除。复习与面试各保留一个入口。不新增一级模块，不改变44道 ACTIVE Canonical、题目ID、来源与计数。

<details>
<summary>旧23章迁移关系（维护记录，不是第二条学习路线）</summary>

| 旧章 | 新课程中的归属 |
|---|---|
| 01 | 01–04：系统边界、任务、应用与运行责任 |
| 02 | 01–02：系统定义与控制权 |
| 03 | 04、07：循环/事件与状态 |
| 04 | 10：工具契约 |
| 05 | 10：注册、路由与发现 |
| 06 | 11：执行与错误 |
| 07 | 11：副作用、并发、取消和进度 |
| 08 | 04：规划、目标、停止与预算 |
| 09 | 05：上下文组装、缓存与外部化 |
| 10 | 05：压缩和继续执行正确性 |
| 11 | 06：记忆全生命周期 |
| 12 | 07、13：状态语义与存储资源 |
| 13 | 07：检查点、恢复、分叉与副作用核对 |
| 14 | 13–14：执行隔离与权限审批 |
| 15 | 14：注入、秘密与风险约束 |
| 16 | 12：协议、技能、钩子与扩展 |
| 17 | 03、09：意图路由与模型适配 |
| 18 | 08：协作、A2A与共享资源 |
| 19 | 15：观测与回放 |
| 20 | 15：评测与持续改进 |
| 21 | 12、13、16：资源理解、环境与验证交付 |
| 22 | 13、16：环境与生产部署 |
| 23 | 16：框架、选型与迁移 |

</details>

合并去除重复的前言、频率说明和面试模板；核心机制、失败路径、取舍与验证按新职责编排。首次阅读只沿 Agent README 的01→16。
