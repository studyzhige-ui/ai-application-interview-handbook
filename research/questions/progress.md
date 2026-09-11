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

```text
Frozen HUMAN-A              279 / 279
ACTIVE Canonical            235 / 235
Mapped to >=1 Canonical     278
VALID-UNMAPPED                1
Unexpected uncovered          0
Evidence outside baseline     0
Source Count mismatch         0
```

最终 Ownership：Python 15 / FastAPI 4 / AI Backend 39 / MySQL 26 / Redis 19 / Vector DB 12 / LLM Foundation 23 / RAG 29 / Agent Harness 44 / System Design 24 = **235**。

---

# Phase 3：Curriculum Build 🚧

## 固定课程原则

> **完整知识体系与初学者 0→1 的认知依赖决定教材主干；真人面经只校准复习权重、真实问法、追问深度与 Failure / Scale / Evaluation 强度。**

> **研究粒度、Capability 粒度和教材文件粒度必须分开。Canonical 可以很细，但一个 Markdown 文件应代表一个完整知识小板块。**

详细规则：`../../roadmap/curriculum-granularity-audit.md`。
内容深度验收：`../../roadmap/content-depth-audit.md`。Redis / Vector DB / LLM Foundation / RAG / System Design 已完成 QA 与人工复核并通过。
Foundation 完成度核实：`../../roadmap/foundation-status-audit.md`。FastAPI / AI Backend Engineering 当前只有课程骨架；Python 是可用 v1，但需最新 Canonical / 当前统一深度标准的定向整改。

## 当前正式建设状态

| 模块 | Phase 3 状态 |
|---|---|
| Python | 🟠 v1 完整可用；最新 15 Canonical / 当前标准定向整改待完成 |
| FastAPI | ⏳ 只有 README 课程骨架；正式正文未写 |
| AI Backend Engineering | ⏳ 只有 README 课程骨架；正式正文未写 |
| MySQL | ✅ **23 blocks**；Granularity PASS |
| Redis | ✅ **24 blocks**；27→24 整改完成 |
| Vector DB | ✅ **16 blocks**；23→16 整改完成 |
| LLM Foundation | ✅ **14 blocks**；29→14 整改完成 |
| RAG | ✅ **14 blocks**；34→14 整改完成 |
| Agent Harness / Runtime | ✅ **23 blocks**；47→23 结构整改 + 正文深度验收完成 |
| System Design | ✅ **19 blocks**；正文 + Review + Interview 完成 |

### Granularity Remediation 最终结果

```text
MySQL          23 → 23  PASS
Redis          27 → 24  COMPLETE
Vector DB      23 → 16  COMPLETE
LLM Foundation 29 → 14  COMPLETE
RAG            34 → 14  COMPLETE
Agent Harness  47 → 23  COMPLETE（结构 + 深度）
System Design  24 Canonical → 19 curriculum blocks  COMPLETE
```

不同数字是正常结果，不追求统一章数。

---

## Agent Harness / Runtime 完成状态 ✅

证据层保持：

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

完成内容：

```text
47 章旧目录
→ 23 个知识小板块
→ docs/ 01–23 连续
→ 旧碎片文件删除
→ Review 切换到 23-block 口径
→ 08–23 旧短稿全部深写
→ 01–07 抽查通过
→ rewrite / depth-validation checkpoint 清理
```

当前 23-block 正文已经按：Why → Runtime Model → Execution → Failure → Recovery/Security/Observability → Evidence → Interview → Self-test 验收。

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

## 下一阶段：Foundation Completion

System Design 已完成。接下来补齐此前 Foundation 的真实缺口，仓库建设顺序为：

```text
FastAPI 正式教材
→ AI Backend Engineering 正式教材
→ Python v1 Canonical Coverage / Depth Remediation
```

这只是建设顺序；学习者的正式学习顺序仍为 `Python → FastAPI → AI Backend Engineering`。
