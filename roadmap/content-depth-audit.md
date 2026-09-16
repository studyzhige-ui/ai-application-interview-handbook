# Curriculum Content Depth Audit｜正文深度最终口径

> **2026-09-16更新：** Agent为16章分层增强版，全仓库177篇正文；本轮已完成机制迁移、通用推导示例、细粒度训练与结构验证，范围和限制见文末。旧全仓库终审仍是历史记录。


[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Granularity Audit](curriculum-granularity-audit.md)

> 当前十个一级模块共 **177 个正文知识块**。本文件统一记录完成状态；文件大小只用于发现异常，不作为质量结论。

## 验收标准

一个知识块应覆盖其主题所需要的大部分：

```text
为什么需要
→ 准确定义 / Mental Model
→ 机制 / 数据流 / 算法
→ Failure / Trade-off
→ Production / AI Application 场景
→ 模块边界
→ 面试表达 / 易错点 / 深挖
→ 折叠自测
```

窄主题可以较短；大型 Production 子系统如果只有概览则不能通过。

## 当前状态

| 模块 | Blocks | Numbering | Quality Status |
|---|---:|---|---|
| [Python Foundation](../python/README.md) | 13 | ✅ `01–13` | ✅ PASS |
| [FastAPI](../fastapi/README.md) | 16 | ✅ `01–16` | ✅ PASS |
| [AI Backend Engineering](../backend-engineering/README.md) | 22 | ✅ `01–22` | ✅ PASS |
| [MySQL](../mysql/README.md) | 23 | ✅ `01–23` | ✅ PASS |
| [Redis](../redis/README.md) | 24 | ✅ `01–24` | ✅ PASS |
| [Vector Database](../vector-db/README.md) | 16 | ✅ `01–16` | ✅ PASS |
| [LLM Foundation（应用工程深度）](../llm-foundation/README.md) | 14 | ✅ `01–14` | ✅ PASS |
| [RAG](../rag/README.md) | 14 | ✅ `01–14` | ✅ PASS |
| [Agent](../agent/README.md) | 16 | ✅ `01–16` | 分层增强与机制/训练迁移复核完成；范围见文末 |
| [System Design](../system-design/README.md) | 19 | ✅ `01–19` | ✅ PASS |

**当前正文总量：177 blocks。**

## 验收历史说明

- Python：保留 v1 主干后做 Canonical Coverage / Depth Remediation；
- FastAPI / AIBE / System Design：首版即按当前粒度和深度标准建设；
- Redis / Vector DB / LLM / RAG：完成旧结构颗粒度整改后重新做深度复核；
- MySQL：原 23-block 结构本身健康，机制与 correctness 边界审阅通过；
- Agent 历史版本：47→23 时完成旧短稿深写与证据验收；当前16章分层重构的检查范围见顶部更新说明。

## 后续规则

```text
先定认知闭环 → 写正文 → QA 找异常 → 人工复核 → 再标记完成
```

自动检查只负责发现异常，不能代替人工判断。


## 2026-09-16｜Agent 分层增强复核

保留16章任务驱动与四层主线，吸收main的23章机制细节和细粒度训练。前两章新增同一个通用文件报告的契约/控制权推导；16章均补阅读提示、情景自测与对应面试练习链接；长章分段阅读，不另建平行教材。

面试页保留main的56个练习能力范围，并增加8个系统推导题；86个易错辨析和速查同页组织。64道练习不等于真人Canonical；44道ACTIVE Canonical及研究证据保持不变。最小Loop教学例实际执行5种场景通过，但不替代真实模型/工具和生产可靠性测试。

逐章迁移表、具体差异处理、检查结果与限制只维护在[Agent增强质量记录](final-quality-audit.md#agent-enrichment-20260916)。结构检查不按字数冒充语义质量证明。
