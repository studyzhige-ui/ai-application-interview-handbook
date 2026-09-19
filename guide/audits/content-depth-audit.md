# Curriculum Content Depth Audit｜正文深度最终口径

> **2026-09-17：** Agent24章已恢复展开式教学并核对旧版内容。185篇为当前结构计数；不以历史PASS或文件大小证明读者理解。详见[修订记录](../project/agent-reader-revision.md)。

[← Handbook 总目录](../../README.md) · [Knowledge Map](../knowledge-map.md) · [Granularity Audit](curriculum-granularity-audit.md)

> 当前十个一级模块共 **185 个正文知识块**。本文件统一记录完成状态；文件大小只用于发现异常，不作为质量结论。

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
| [Python Foundation](../../curriculum/01-python/README.md) | 13 | ✅ `01–13` | ✅ PASS |
| [FastAPI](../../curriculum/02-fastapi/README.md) | 16 | ✅ `01–16` | ✅ PASS |
| [AI Backend Engineering](../../curriculum/03-backend-engineering/README.md) | 22 | ✅ `01–22` | ✅ PASS |
| [MySQL](../../curriculum/04-mysql/README.md) | 23 | ✅ `01–23` | ✅ PASS |
| [Redis](../../curriculum/05-redis/README.md) | 24 | ✅ `01–24` | ✅ PASS |
| [Vector Database](../../curriculum/06-vector-db/README.md) | 16 | ✅ `01–16` | ✅ PASS |
| [LLM Foundation（应用工程深度）](../../curriculum/07-llm-foundation/README.md) | 14 | ✅ `01–14` | ✅ PASS |
| [RAG](../../curriculum/08-rag/README.md) | 14 | ✅ `01–14` | ✅ PASS |
| [Agent](../../curriculum/09-agent/README.md) | 24 | ✅ `01–24` | ✅ PASS |
| [System Design](../../curriculum/10-system-design/README.md) | 19 | ✅ `01–19` | ✅ PASS |

**当前正文总量：185 blocks。**

## 验收历史说明

- Python：保留 v1 主干后做 Canonical Coverage / Depth Remediation；
- FastAPI / AIBE / System Design：首版即按当前粒度和深度标准建设；
- Redis / Vector DB / LLM / RAG：完成旧结构颗粒度整改后重新做深度复核；
- MySQL：原 23-block 结构本身健康，机制与 correctness 边界审阅通过；
- Agent Harness：47→23 完成粒度收敛与深写；随后为分离 MCP 协议生命周期与 Skills / Hooks / Extensions 扩展生命周期调整为 24 章，并重新核对内容去向与证据。

## 后续规则

```text
先定认知闭环 → 写正文 → QA 找异常 → 人工复核 → 再标记完成
```

自动检查只负责发现异常，不能代替人工判断。
