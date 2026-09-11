# Canonical Questions

这里不做“网上见过什么题就全部收进来”的题库。

## Repository-first 规则

> **后续继续研究或建设教材时，必须先读取仓库当前最新的 `README.md`、`schema.md`、`progress.md`、`module-index.md`、根 README、知识地图和相关模块文件。仓库最新描述高于聊天中的历史总结、旧分类和旧计数。**

## 唯一证据原则

Canonical Question 只允许由 **HUMAN-A 真人高质量第一人称面经**产生市场证据。源码、官方文章、规范、论文可以补齐课程知识边界，但不能创建真人面试频率或提高 Source Count。

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

`Coding / Debug / AI Coding` 只作为 `Question Type`，不作为一级板块。

---

## 当前冻结基线与研究状态

- HUMAN-A：`S001–S279`
- Batch：26
- 主动采集：已冻结
- Phase 1 Canonicalization：✅
- Phase 2A Global Merge / Split Audit：✅
- Phase 2B Global Index + Market Analysis：✅
- Primary-owned ACTIVE Canonical：**235**
- Legacy MOVED：**24**
- Mapped HUMAN-A：**278**
- VALID-UNMAPPED：**1（S271）**

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

详细入口：

- `schema.md`：数据规范与板块边界；
- `module-index.md`：Ownership 与 Phase 3 状态；
- `global-audit.md`：Global Merge / Split 决策；
- `progress.md`：当前教材建设阶段；
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
→ Agent Harness / Runtime ✅ 47 章 + Review + Interview
→ System Design 🚧 下一块
```

Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架。

---

## Agent Harness 特殊证据规则

Agent Harness 的市场证据仍只来自 Frozen HUMAN-A 44 道 Agent Canonical。

正式教材另外使用：

- `research/analysis/follow-up-chains.md`；
- `studyzhige-ui/claude-code-source-private`；
- `openai/codex`；
- Anthropic / OpenAI 官方 Agent / Harness 工程资料；
- MCP / A2A 官方规范；
- ReAct / SWE-bench 等原始论文。

完整索引：[`../agent-sources/README.md`](../agent-sources/README.md)

固定源码快照：

```text
Claude Code commit = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex commit = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

课程使用原则：

```text
HUMAN-A → 市场真实度 / 频率 / 追问
源码     → 成熟实现事实
官方资料 → 跨产品稳定设计原则
课程体系 → beginner-first 0→1 演进
```

源码与网上权威资料**不能**反向改变 HUMAN-A 面试频率。
