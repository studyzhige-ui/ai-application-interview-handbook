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

# Phase 3：Curriculum Build / Granularity Remediation 🚧

## 固定课程原则

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度，不能反过来打乱模块本身的演进顺序。**

新增第二条正式原则：

> **研究粒度、Capability 粒度和教材文件粒度必须分开。Canonical Question 可以很细，但一个 Markdown 文件应代表一个完整知识小板块，而不是默认一题一章。**

详细规则：`../../roadmap/curriculum-granularity-audit.md`

统一建设形态仍是：

```text
模块 README
+ 系统正文 docs/
+ 每章折叠自测
+ review/ 图解与综合自测
+ interview/ 高频题
+ interview/ 易错点
+ interview/ 面试前速查
```

但 `docs/` 文件数现在由知识闭环决定，不再由 Canonical / Capability 数量隐式决定。

## 当前正式建设状态

| 模块 | Phase 3 状态 |
|---|---|
| Python | ✅ 既有完整系统教材 |
| FastAPI | 🟡 完整课程骨架，正文后续补齐 |
| AI Backend Engineering | 🟡 完整课程骨架，按 Bridge / Production 主线持续补齐 |
| MySQL | ✅ 23 章 + Review + Interview；Granularity Audit PASS |
| Redis | 🟠 27 章内容完成；Minor Granularity Remediation，目标约 23 |
| Vector DB | 🟠 23 章内容完成；Moderate Remediation，目标 16–18 |
| LLM Foundation | 🟠 29 章内容完成；Moderate Remediation，目标 14–17 |
| RAG | 🟠 34 章内容完成；Major Remediation，目标 14–16 |
| Agent Harness / Runtime | 🚧 旧 47 已物理迁移为 23 个知识小板块；深度验收中 |
| System Design | ⏸️ 当前粒度整改完成后启动 |

当前正式顺序：

```text
Agent 23-block 深度验收
→ RAG 粒度整改
→ LLM Foundation 粒度整改
→ Vector DB 粒度整改
→ Redis 轻度整改
→ System Design
```

MySQL 已通过审计，不为统一数字机械改章。

---

## Agent Harness / Runtime 当前状态 🚧

Agent 教材继续使用四层证据：

```text
Tier A  44 道 HUMAN-A Agent Canonical + Verified Follow-up Chains
Tier B  Claude Code + OpenAI Codex 固定源码快照
Tier C  Anthropic / OpenAI 官方工程资料 + MCP/A2A 规范 + 原始论文
Tier D  Runtime Capability Map + beginner-first curriculum
```

研究层已经完成：

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

旧 47 章的问题不是知识点错误，而是教材文件几乎沿 Capability Primitive 拆分。当前已完成：

```text
47 章旧目录
→ 23 个知识小板块
→ docs/ 01–23 连续
→ 旧碎片文件删除
→ Review 切换到 23-block 口径
```

当前 23-block 主线：

```text
Agent / Workflow / Harness
→ Loop / Run / Turn / Step / Event
→ Tool Runtime
→ Planning / Goal / Stop / Budget
→ Context Assembly / Compaction
→ Memory / State / Long-running Reliability
→ Permission / Sandbox / Injection / Containment
→ MCP / Skills / Hooks / Routing
→ Multi-Agent / A2A / Workspace
→ Trace / Eval / Coding Agent
→ Production Runtime
→ Framework Mapping
```

源码与 Tier C 权威资料**不得**改变 HUMAN-A Source Count。

---

## 已完成模块 Granularity Audit

| 模块 | 结论 | 说明 |
|---|---|---|
| MySQL | PASS | 章节普遍形成独立索引 / 事务 / 扩展闭环 |
| Redis | Minor | 少量 Runtime / Atomic / Lock 相邻章可合并 |
| Vector DB | Moderate | Vector Space、ANN、HNSW、Lifecycle 等拆得偏细 |
| LLM Foundation | Moderate | Transformer / Generation / Serving mechanism 粒度偏细 |
| RAG | Major | Chunk / Query / Retrieval / Eval 明显接近 Canonical 粒度 |
| Agent Harness | Major | 已完成 47→23 结构迁移 |

完整判断：`../../roadmap/curriculum-granularity-audit.md`。

---

## 模块完成后的强制同步清单

每完成或重组一个一级模块，必须同时检查并同步：

1. 模块自身 `README.md`；
2. 根 `README.md`；
3. `roadmap/knowledge-map.md`；
4. 本文件 `research/questions/progress.md`；
5. `research/questions/module-index.md`；
6. 自动生成的 `research/analysis/README.md` 与其生成 Workflow / Script 是否使用最新口径；
7. 任何仍写着“下一块 / 待建设 / 旧章节数”的关联入口；
8. 最后重新核验 `docs / review / interview` 文件数量、连续编号与链接。

---

## 下一阶段

当前不直接进入 System Design。

先完成：

```text
Agent 23-block 深度验收
        ↓
RAG / LLM / Vector / Redis Granularity Remediation
        ↓
System Design
```

System Design 开始时也必须先按知识子系统划分文件，再映射 24 道 System Design Canonical，不能反向一题一章。
