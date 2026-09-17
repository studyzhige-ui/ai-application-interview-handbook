# Curriculum Content Depth Audit｜正文深度最终口径

> **2026-09-17：** Agent24章已恢复展开式教学并核对旧版内容。185篇为当前结构计数；不以历史PASS或文件大小证明读者理解。详见[修订记录](agent-reader-revision.md)。

[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Granularity Audit](curriculum-granularity-audit.md)

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
| [Python Foundation](../python/README.md) | 13 | ✅ `01–13` | ✅ PASS |
| [FastAPI](../fastapi/README.md) | 16 | ✅ `01–16` | ✅ PASS |
| [AI Backend Engineering](../backend-engineering/README.md) | 22 | ✅ `01–22` | ✅ PASS |
| [MySQL](../mysql/README.md) | 23 | ✅ `01–23` | ✅ PASS |
| [Redis](../redis/README.md) | 24 | ✅ `01–24` | ✅ PASS |
| [Vector Database](../vector-db/README.md) | 16 | ✅ `01–16` | ✅ PASS |
| [LLM Foundation（应用工程深度）](../llm-foundation/README.md) | 14 | ✅ `01–14` | ✅ PASS |
| [RAG](../rag/README.md) | 14 | ✅ `01–14` | ✅ PASS |
| [Agent](../agent/README.md) | 24 | ✅ `01–24` | ✅ PASS |
| [System Design](../system-design/README.md) | 19 | ✅ `01–19` | ✅ PASS |

**当前正文总量：185 blocks。**

## 验收历史说明

- Python：保留 v1 主干后做 Canonical Coverage / Depth Remediation；
- FastAPI / AIBE / System Design：首版即按当前粒度和深度标准建设；
- Redis / Vector DB / LLM / RAG：完成旧结构颗粒度整改后重新做深度复核；
- MySQL：原 23-block 结构本身健康，机制与 correctness 边界审阅通过；
- Agent Harness：47→23 后对旧短稿区域做第二轮深写与源码 / 官方证据验收。

## 后续规则

```text
先定认知闭环 → 写正文 → QA 找异常 → 人工复核 → 再标记完成
```

自动检查只负责发现异常，不能代替人工判断。
