# Canonical Question 重建与课程建设进度

更新日期：2026-09-11

## Repository-first 规则

> **后续所有工作都以仓库当前最新描述为准。** 每次继续研究或建设教材前，先读取本目录的 `README.md`、`schema.md`、`progress.md`、`module-index.md`、根 `README.md`、`roadmap/knowledge-map.md` 与相关模块文件；聊天中的历史总结、旧分类、旧计数只能作为背景，不能覆盖仓库最新状态。

## Frozen Baseline

- HUMAN-A：`S001–S279`
- 正式 Batch：26
- 主动采集：已冻结
- ACTIVE Canonical：**235**
- Mapped Sources：**278**
- VALID-UNMAPPED：**1（S271）**

## 正式十板块

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

---

## Phase 1：十板块纵向 Canonicalization ✅

完成 `S001–S279` 全库回读、十板块纵向扫描、唯一 Primary Module 与第一轮跨模块归属审计。

Phase 1 结束：**230 ACTIVE / 22 MOVED**。

## Phase 2A：Global Merge / Split Audit ✅

完成全局 Merge / Split / Narrow / Evidence Reassignment。

Phase 2A 结束：**229 ACTIVE / 24 MOVED**。

## Phase 2B：Global Index + Market Analysis ✅

最终硬校验：

| Check | Result |
|---|---|
| Frozen HUMAN-A | ✅ 279 / 279 |
| ACTIVE Canonical | ✅ 235 / 235 |
| Mapped to >=1 Canonical | ✅ 278 |
| Documented VALID-UNMAPPED | ✅ 1 (`S271`) |
| Unexpected uncovered | ✅ 0 |
| Evidence outside S001–S279 | ✅ 0 |
| Source Count mismatch | ✅ 0 |

最终 Ownership：Python 15 / FastAPI 4 / AI Backend 39 / MySQL 26 / Redis 19 / Vector DB 12 / LLM Foundation 23 / RAG 29 / Agent Harness 44 / System Design 24 = **235**。

---

## Phase 3：Curriculum Build / Remediation 🚧

### 固定课程原则

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度，不能反过来打乱模块本身的演进顺序。**

统一建设形态：

```text
模块 README
+ 系统正文 docs/
+ 每章折叠自测
+ review/ 图解与综合自测
+ interview/ 高频题
+ interview/ 易错点
+ interview/ 面试前速查
```

### 当前正式建设状态

| 模块 | Phase 3 状态 |
|---|---|
| Python | ✅ 既有完整系统教材 |
| FastAPI | 🟡 完整课程骨架，正文后续补齐 |
| AI Backend Engineering | 🟡 完整课程骨架，按 Bridge / Production 主线持续补齐 |
| MySQL | ✅ 第一版完成：23 章 + Review + Interview |
| Redis | ✅ 第一版完成：27 章 + Review + Interview |
| Vector DB | ✅ 第一版完成：23 章 + Review + Interview |
| LLM Foundation | ✅ 第一版完成：29 章 + Review + Interview |
| RAG | ✅ 第一版完成：34 章 + Review + Interview |
| Agent Harness / Runtime | ✅ 第一版完成：47 章 + Review + Interview |
| System Design | 🚧 **下一块正式系统教材** |

正式顺序：

```text
MySQL ✅
→ Redis ✅
→ Vector DB ✅
→ LLM Foundation ✅
→ RAG ✅
→ Agent Harness / Runtime ✅
→ System Design 🚧
```

---

## Agent Harness / Runtime Phase 3 v1 ✅

Agent 教材没有直接从 Framework API 起步，而先完成四层证据融合：

```text
Tier A  44 道 HUMAN-A Agent Canonical + Verified Follow-up Chains
Tier B  Claude Code + OpenAI Codex 固定源码快照
Tier C  Anthropic / OpenAI 官方工程资料 + MCP/A2A 规范 + 原始论文
Tier D  Runtime Capability Map + beginner-first curriculum
```

已完成研究层：

- `research/agent-sources/README.md`
- `research/agent-sources/claude-code-source-index.md`
- `research/agent-sources/codex-source-index.md`
- `research/agent-sources/authoritative-web-sources.md`
- `research/agent-sources/runtime-capability-map.md`
- `roadmap/agent-authoritative-sources.md`

源码固定快照：

```text
Claude Code = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

教材已完成：

```text
agent-harness/README.md
+ docs/ 01–47
+ review/README.md
+ interview/高频面试题.md（56 道）
+ interview/面试易错点.md（86 个）
+ interview/面试前速查表.md
```

Agent 的核心顺序为：

```text
Agent / Workflow / Harness
→ Loop / Run / Turn / Step / Event
→ Tool Runtime
→ Planning / Stop / Budget
→ Context / Compaction
→ Memory / State / Checkpoint / Resume
→ Cancellation / Idempotency / Compensation
→ Permission / Sandbox / Injection / Containment
→ Discovery / MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Eval / Coding Verification
→ Production Runtime
→ Framework Mapping
```

源码与 Tier C 权威资料**不得**改变 HUMAN-A Source Count。

---

## 模块完成后的强制同步清单

每完成一个一级模块，必须同时检查并同步：

1. 模块自身 `README.md`；
2. 根 `README.md`；
3. `roadmap/knowledge-map.md`；
4. 本文件 `research/questions/progress.md`；
5. `research/questions/module-index.md`；
6. 自动生成的 `research/analysis/README.md` 与其生成 Workflow / Script 是否使用最新口径；
7. 任何仍写着“下一块 / 待建设”的关联入口；
8. 最后重新核验 `docs / review / interview` 文件数量、连续编号与链接。

---

## 下一步：System Design

System Design 不再新增一套孤立八股，而要把已经完成的前置模块汇合成真实 Production Architecture：

```text
Requirements / SLO
→ Capacity / Traffic
→ API / Streaming
→ Data / State / Retrieval
→ Agent Runtime
→ Async / Queue / Backpressure
→ Consistency / Reliability
→ Tenant / Security
→ Observability / Evaluation
→ Scaling / Cost / Degradation
```
