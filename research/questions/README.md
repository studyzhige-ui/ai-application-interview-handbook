# Canonical Questions

这里不做“网上见过什么题就全部收进来”的题库。

## Repository-first 规则

> **后续继续研究或建设教材时，必须先读取仓库当前最新的 `README.md`、`schema.md`、`progress.md`、`module-index.md`、根 README、知识地图和相关模块文件。仓库最新描述高于聊天中的历史总结、旧分类和旧计数。**

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

---

## 当前冻结基线与研究状态

- HUMAN-A：`S001–S279`
- Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- Phase 1 十板块纵向 Canonicalization：✅
- Phase 2A Global Merge / Split Audit：✅
- Phase 2B Global Index + Market Analysis：✅
- Primary-owned ACTIVE Canonical：**235**
- Legacy MOVED 映射：**24**
- Mapped HUMAN-A：**278**
- VALID-UNMAPPED：**1（S271）**

当前十板块数量：

| 一级板块 | ACTIVE |
|---|---:|
| Python | 15 |
| FastAPI | 4 |
| AI Backend Engineering | 39 |
| MySQL | 26 |
| Redis | 19 |
| Vector DB | 12 |
| LLM Foundation（应用工程深度） | 23 |
| RAG | 29 |
| Agent Harness / Runtime | 44 |
| System Design | 24 |
| **合计** | **235** |

最终一致性：

```text
Frozen HUMAN-A              279 / 279
ACTIVE Canonical            235 / 235
Mapped to >=1 Canonical     278
VALID-UNMAPPED                1
Unexpected uncovered          0
Evidence outside baseline     0
Source Count mismatch         0
```

详细状态：

- `schema.md`：数据规范与板块边界；
- `module-index.md`：Ownership、迁移映射和 Phase 3 状态；
- `global-audit.md`：Global Merge / Split / Evidence Audit；
- `progress.md`：研究与教材建设的当前阶段；
- `../analysis/`：Frequency / Coverage / Follow-up Chain / Knowledge Gap。

---

## Phase 3 Curriculum Build

固定原则：

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度。**

当前状态：

```text
MySQL ✅ 23 章 + Review + Interview
→ Redis ✅ 27 章 + Review + Interview
→ Vector DB ✅ 23 章 + Review + Interview
→ LLM Foundation ✅ 29 章 + Review + Interview
→ RAG ✅ 34 章 + Review + Interview
→ Agent Harness / Runtime 🚧 下一块
→ System Design
```

Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架。

---

## 与完整知识体系的关系

完整课程体系负责决定“应该学什么”；真人高质量面经只负责提供：

- 真实问法；
- 真实追问深度；
- 公司 / 岗位 / 轮次信号；
- 学习优先级校准。

因此不会为了扩充问题库，把二次创作、题库、标准答案、合集或无法核验的内容转化成额外学习任务。

---

## Agent Harness 特殊规则

Agent Harness 正式课程必须同时使用：

- Frozen HUMAN-A 44 道 Agent Canonical；
- `research/analysis/follow-up-chains.md`；
- `studyzhige-ui/claude-code-source-private`；
- `openai/codex`。

源码用于补齐成熟 Harness / Runtime 的实现事实和知识边界；源码证据**不能**反向改变 HUMAN-A 面试频率。
