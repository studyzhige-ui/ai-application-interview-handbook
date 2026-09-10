# Canonical Questions

这里不做“网上见过什么题就全部收进来”的题库。

## Repository-first 规则

> **后续继续研究时，必须先读取仓库当前最新的 `README.md`、`schema.md`、`progress.md`、`module-index.md` 和相关模块文件。仓库最新描述高于聊天中的历史总结、旧分类和旧计数。**

这条规则用于避免在长对话或切换对话后重新沿用已经废弃的研究口径。

## 唯一证据原则

Canonical Question 只允许由 **HUMAN-A 真人高质量第一人称面经**产生市场证据：

```text
真人面试官
+
候选人本人第一人称
+
高信息密度
+
AI Application / Agent 目标岗位
+
可稳定核验
+
非转载重复
```

任何不满足上述标准的来源都不能创建新的 Canonical Question、提高某题的面试频率或伪装成课程学习优先级。

## 正式一级板块

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering
  ↓
MySQL
  ↓
Redis
  ↓
Vector DB
  ↓
LLM Foundation（应用工程深度）
  ↓
RAG
  ↓
Agent Harness / Runtime
  ↓
System Design
```

对应文件：

- `python.md`
- `fastapi.md`
- `ai-backend-engineering.md`
- `mysql.md`
- `redis.md`
- `vector-db.md`
- `llm-foundation.md`
- `rag.md`
- `agent-harness.md`
- `system-design.md`

`Coding / Debug / AI Coding` 只作为 `Question Type`，不作为一级板块。

## 当前冻结基线与研究状态

- HUMAN-A：`S001–S279`
- Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- Phase 1 十板块全库纵向 Canonicalization：✅ 完成
- Phase 2A Global Merge / Split Audit：✅ 完成
- 当前 Primary-owned ACTIVE Canonical：**229**
- Legacy MOVED 映射：**24**
- 下一阶段：Phase 2B Global Index + Market Analysis

当前十板块数量：

| 一级板块 | ACTIVE |
|---|---:|
| Python | 15 |
| FastAPI | 4 |
| AI Backend Engineering | 39 |
| MySQL | 26 |
| Redis | 19 |
| Vector DB | 12 |
| LLM Foundation（应用工程深度） | 22 |
| RAG | 29 |
| Agent Harness / Runtime | 39 |
| System Design | 24 |
| **合计** | **229** |

详细状态：

- `schema.md`：数据规范与板块边界；
- `module-index.md`：十板块 Ownership、迁移映射和 ACTIVE 数量；
- `global-audit.md`：Global Merge / Split / Evidence Audit 决策记录；
- `progress.md`：当前阶段与下一步。

## 与完整知识体系的关系

完整课程体系负责决定“应该学什么”；真人高质量面经只负责提供：

- 真实问法；
- 真实追问深度；
- 公司 / 岗位 / 轮次信号；
- 学习优先级校准。

因此不会为了扩充问题库，把二次创作、题库、标准答案、合集或无法核验的内容转化成额外学习任务。

Agent Harness 正式课程还会以：

- `studyzhige-ui/claude-code-source-private`
- `openai/codex`

作为成熟 Harness / Runtime 实现的最高参考，用于补齐课程知识边界与实现细节；源码证据**不能**反向改变 HUMAN-A 面试频率。