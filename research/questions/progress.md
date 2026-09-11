# Canonical Question 重建与课程建设进度

更新日期：2026-09-11

## Repository-first 规则

> **后续所有工作都以仓库当前最新描述为准。** 每次继续研究或建设教材前，先读取本目录 `README.md`、`schema.md`、`progress.md`、`module-index.md`、根 `README.md`、`roadmap/knowledge-map.md` 与相关模块文件；聊天中的历史总结、旧分类、旧计数只能作为背景。

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
→ FastAPI
→ AI Backend Engineering
→ MySQL
→ Redis
→ Vector DB
→ LLM Foundation（应用工程深度）
→ RAG
→ Agent Harness / Runtime
→ System Design
```

---

## Phase 1：十板块纵向 Canonicalization ✅

完成 `S001–S279` 全库回读、十板块纵向扫描、唯一 Primary Module 与第一轮跨模块归属审计。

## Phase 2A：Global Merge / Split Audit ✅

完成全局 Merge / Split / Narrow / Evidence Reassignment。

## Phase 2B：Global Index + Market Analysis ✅

最终硬校验：

| Check | Result |
|---|---|
| Frozen HUMAN-A | ✅ 279 / 279 |
| ACTIVE Canonical | ✅ 235 / 235 |
| Mapped to >=1 Canonical | ✅ 278 |
| VALID-UNMAPPED | ✅ 1 (`S271`) |
| Unexpected uncovered | ✅ 0 |
| Evidence outside baseline | ✅ 0 |
| Source Count mismatch | ✅ 0 |

最终 Ownership：Python 15 / FastAPI 4 / AI Backend 39 / MySQL 26 / Redis 19 / Vector DB 12 / LLM Foundation 23 / RAG 29 / Agent Harness 44 / System Design 24 = **235**。

---

# Phase 3：Curriculum Build / Granularity Remediation 🚧

## 固定课程原则

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度。**

> **研究粒度、Capability 粒度和教材文件粒度必须分开。Canonical 可以很细，但一个 Markdown 文件应代表一个完整知识小板块。**

详细规则：`../../roadmap/curriculum-granularity-audit.md`。

## 当前正式建设状态

| 模块 | Phase 3 状态 |
|---|---|
| Python | ✅ 既有完整系统教材 |
| FastAPI | 🟡 完整课程骨架，正文后续补齐 |
| AI Backend Engineering | 🟡 完整课程骨架，按 Production 主线持续补齐 |
| MySQL | ✅ **23 blocks**；Granularity PASS |
| Redis | ✅ **24 blocks**；已完成 27→24 整改 |
| Vector DB | ✅ **16 blocks**；已完成 23→16 整改 |
| LLM Foundation | ✅ **14 blocks**；已完成 29→14 整改 |
| RAG | ✅ **14 blocks**；已完成 34→14 整改 |
| Agent Harness / Runtime | 🚧 **23 blocks**；47→23 结构迁移完成，正文深度验收中 |
| System Design | ⏸️ Agent 深度验收完成后启动 |

### Granularity Remediation 已完成的结构调整

```text
MySQL          23 → 23  PASS
Redis          27 → 24  COMPLETE
Vector DB      23 → 16  COMPLETE
LLM Foundation 29 → 14  COMPLETE
RAG            34 → 14  COMPLETE
Agent Harness  47 → 23  STRUCTURE COMPLETE
```

不同数字是正常结果，不追求统一章数。

---

## Agent Harness / Runtime 当前任务 🚧

Agent 课程继续使用四层证据：

```text
Tier A  44 HUMAN-A Agent Canonical + Verified Follow-up Chains
Tier B  Claude Code + OpenAI Codex 固定源码快照
Tier C  Anthropic / OpenAI 官方工程资料 + MCP/A2A 规范 + 原始论文
Tier D  Runtime Capability Map + beginner-first curriculum
```

固定源码快照：

```text
Claude Code = 58231dcce408f805c645cfbc352d2876b517223b
OpenAI Codex = fc948f8c473e5d11e780ffcf1fd7f812a2020932
```

已经完成：

```text
47 章旧目录
→ 23 个知识小板块
→ docs/ 01–23 连续
→ 旧碎片文件删除
→ Review 切换到 23-block 口径
```

当前不再继续缩章。下一任务是：

> **逐章检查 23-block 是否达到 MySQL / RAG 同级教学深度，重点补强由旧短稿合并来的 08–23。**

验收维度：

```text
为什么存在
→ Runtime Mental Model
→ 正常执行路径
→ State / Protocol / Data Structure
→ Failure Timeline
→ Cancellation / Recovery / Idempotency
→ Security / Permission Boundary
→ Observability / Evaluation
→ Claude Code / Codex 实现证据
→ 面试回答 / 自测
```

---

## 模块完成后的强制同步清单

每完成或重组一个一级模块，必须同步并重新核验：

1. 模块自身 `README.md`；
2. 根 `README.md`；
3. `roadmap/knowledge-map.md`；
4. 本文件；
5. `research/questions/module-index.md`；
6. `research/questions/README.md`；
7. 自动生成的 `research/analysis/README.md` 及生成脚本是否使用最新口径；
8. `docs / review / interview` 实际文件数、README 链接、旧文件名残留。

---

## 下一阶段

当前顺序：

```text
Agent Harness 23-block 深度验收
→ Agent Review / Interview 最终校准
→ 全仓库状态再验收
→ System Design
```

System Design 开始时必须先按知识子系统划分文件，再映射 24 道 Canonical，禁止一题一章。
