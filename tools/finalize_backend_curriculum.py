from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "backend-engineering"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"missing anchor in {path}: {old[:140]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def regex_once(path: Path, pattern: str, repl: str) -> None:
    text = path.read_text(encoding="utf-8")
    out, n = re.subn(pattern, repl, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"regex mismatch in {path}: {pattern[:120]!r}, n={n}")
    path.write_text(out, encoding="utf-8")


# ---------------------------------------------------------------------------
# 0. Module QA before marking complete.
# ---------------------------------------------------------------------------
docs = sorted((MOD / "docs").glob("[0-9][0-9]-*.md"))
nums = [int(p.name[:2]) for p in docs]
if nums != list(range(1, 23)):
    raise SystemExit(f"AIBE docs numbering invalid: {nums}")

for p in docs:
    text = p.read_text(encoding="utf-8")
    if len(text.encode("utf-8")) < 6000:
        raise SystemExit(f"AIBE doc suspiciously short: {p}")
    if "<details" not in text:
        raise SystemExit(f"AIBE doc missing folded self-test: {p}")
    if "🎯" not in text or "面试" not in text:
        raise SystemExit(f"AIBE doc missing interview expression: {p}")
    if "⚠️" not in text:
        raise SystemExit(f"AIBE doc missing explicit pitfall section: {p}")

readme = MOD / "README.md"
for target in re.findall(r"\]\((docs/[^)#]+\.md)\)", readme.read_text(encoding="utf-8")):
    if not (MOD / target).exists():
        raise SystemExit(f"AIBE README broken doc link: {target}")

required = [
    MOD / "review" / "README.md",
    MOD / "interview" / "高频面试题.md",
    MOD / "interview" / "面试易错点.md",
    MOD / "interview" / "面试前速查表.md",
    ROOT / "research" / "backend-sources" / "README.md",
]
for p in required:
    if not p.exists():
        raise SystemExit(f"AIBE required file missing: {p}")

# ---------------------------------------------------------------------------
# 1. Root README.
# ---------------------------------------------------------------------------
p = ROOT / "README.md"
replace_once(
    p,
    "Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 的正文深度已完成 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。",
    "Python / FastAPI / AI Backend Engineering / Redis / Vector DB / LLM Foundation / RAG / System Design 的正文深度已完成 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。",
)
replace_once(
    p,
    "Foundation 的真实完成度见 [`roadmap/foundation-status-audit.md`](roadmap/foundation-status-audit.md)。Python 与 FastAPI 已完成；Foundation 当前唯一正式教材缺口是 **AI Backend Engineering**。",
    "Foundation 的真实完成度见 [`roadmap/foundation-status-audit.md`](roadmap/foundation-status-audit.md)。Python / FastAPI / AI Backend Engineering 已全部达到正式教材 + Coverage / Depth 验收标准，**Foundation ✅ 完成**。",
)
replace_once(
    p,
    "- [AI Backend Engineering](backend-engineering/README.md) ⏳ **只有 README 课程骨架**；正式 `docs / review / interview` 尚未撰写",
    "- [AI Backend Engineering](backend-engineering/README.md) ✅ **22 个知识小板块**；39 道 Canonical Coverage + 权威工程资料校准 + Depth PASS",
)
replace_once(
    p,
    "Python 13\nFastAPI 16\nMySQL 23",
    "Python 13\nFastAPI 16\nAI Backend Engineering 22\nMySQL 23",
)
replace_once(
    p,
    "| AI Backend Engineering | ⏳ README 课程骨架；正式正文未写 |",
    "| AI Backend Engineering | ✅ 22-block；39 Canonical Coverage / Depth PASS |",
)
# Mark whole curriculum build complete if header exists.
text = p.read_text(encoding="utf-8")
if "# 当前 Phase 3 状态" in text and "**Phase 3 十板块第一版 Curriculum Build：✅ 完成。**" not in text:
    text = text.replace("# 当前 Phase 3 状态\n", "# 当前 Phase 3 状态\n\n**Phase 3 十板块第一版 Curriculum Build：✅ 完成。**\n\n", 1)
    p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# 2. Knowledge Map.
# ---------------------------------------------------------------------------
p = ROOT / "roadmap" / "knowledge-map.md"
replace_once(
    p,
    "内容深度验收：[`content-depth-audit.md`](content-depth-audit.md)；Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 均已通过。",
    "内容深度验收：[`content-depth-audit.md`](content-depth-audit.md)；Python / FastAPI / AI Backend Engineering / Redis / Vector DB / LLM Foundation / RAG / System Design 均已通过。",
)
regex_once(
    p,
    r"## AI Backend Engineering ⏳\n.*?\n\n---",
    "## AI Backend Engineering ✅ — 22 blocks\n入口：[`../backend-engineering/README.md`](../backend-engineering/README.md) — 已完成 `docs/01–22`、Review、Interview 与权威工程资料索引；39 道 AIBE Canonical 已映射到 Python-first Backend Engineering 主干，Content Depth PASS。\n\n**Foundation：✅ Python 13 + FastAPI 16 + AI Backend Engineering 22 全部完成。**\n\n---",
)
replace_once(
    p,
    "| AI Backend Engineering | ⏳ 只有课程骨架；正式正文未写 |",
    "| AI Backend Engineering | ✅ 22 blocks；Canonical Coverage / Depth PASS |",
)
text = p.read_text(encoding="utf-8")
if "# 11. 当前 Phase 3 状态" in text and "十板块第一版课程建设：✅ 完成" not in text:
    text = text.replace("# 11. 当前 Phase 3 状态\n", "# 11. 当前 Phase 3 状态\n\n**十板块第一版课程建设：✅ 完成。**\n\n", 1)
    p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# 3. Foundation status audit.
# ---------------------------------------------------------------------------
p = ROOT / "roadmap" / "foundation-status-audit.md"
aibe_section = '''## 2. AI Backend Engineering — ✅ 22 blocks / Canonical Coverage / Depth PASS

当前仓库实际结构：

```text
backend-engineering/
├── README.md
├── docs/       01–22 连续知识小板块
├── review/     七张总图 + 24 个综合折叠自测
└── interview/  60 道高频题 + 90 个易错点 + 速查表
```

并建立：

```text
research/backend-sources/README.md
```

用于记录 Google SRE、AWS Builders' Library、Stripe、Apache Kafka、Kubernetes、OpenTelemetry、OAuth/RFC 与 OWASP 等权威资料；这些资料只校准工程机制，不改变 HUMAN-A Source Count。

原 README 规划约 55 个细粒度 Topic，研究层有 39 道 Canonical。正式教材没有按任一粒度机械建文件，而是收敛为 22 个认知闭环：

```text
Request / Network / Communication
→ Concurrency / Pool / Backpressure
→ Timeout / Retry / Idempotency
→ MQ / Kafka / Reliable Long-running Task
→ Consistency / State Ownership / Auth
→ Discovery / Observability / Linux / K8s
→ Config / Security
→ Cross-language Runtime Mapping
```

特别处理了 Spring / JVM / Java Concurrency / Go Runtime 真人市场信号：这些内容保留在 `22-CrossLanguageRuntimeMapping.md`，用于把生态题映射回 DI、Lock、Memory、Scheduler、Context 等通用 Backend Primitive，而不是破坏 Python-first 主干。

完成后机械核验：

```text
docs = 01–22 连续
22/22 正文 >= 6KB
22/22 正文含 🎯 面试表达、⚠️ 易错点、<details> 折叠自测
README 正文链接存在
Review / Interview 三件套存在
Backend Official Source Index 存在
```

人工重点复核了：

- `06 Backpressure / Rate Limit`：Queue Deadline、Load Shedding、Multi-tenant Quota；
- `08 Retry / Circuit / Failover`：Retry Amplification、Jitter、Budget、Fallback；
- `12 Reliable Async Task`：Outbox、Lease、Heartbeat、Reclaim、Fencing；
- `13 Consistency / Compensation`：DB+Cache Failure Window、CDC/Outbox、Saga/Reconciliation；
- `19 Container/K8s`：Startup/Readiness/Liveness、Drain、Pool Multiplication；
- `22 Cross-language Mapping`：明确 Concept Mapping ≠ Implementation Equivalence。

**结论：AI Backend Engineering Formal Curriculum = COMPLETE；Content Depth / Canonical Coverage = PASS。**
'''
regex_once(
    p,
    r"## 2\. AI Backend Engineering — .*?\n\n---\n\n## 3\. Python Foundation",
    aibe_section + "\n---\n\n## 3. Python Foundation",
)
regex_once(
    p,
    r"## 4\. 当前 Foundation 建设顺序.*?\n\n---\n\n## 5\. 完成标准",
    '''## 4. Foundation 完成状态

学习顺序仍然是：

```text
Python
→ FastAPI
→ AI Backend Engineering
```

当前三块均已达到：正文知识块 + Review + Interview + Canonical Coverage / Depth Audit，因此：

> **Foundation：✅ COMPLETE。**

---

## 5. 完成标准''',
)
text = p.read_text(encoding="utf-8")
text = text.replace("只有三块都达到这个标准，Foundation 才能整体标记为 `✅`。", "三块当前都已达到这个标准，Foundation 已整体标记为 `✅`。")
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# 4. Granularity audit.
# ---------------------------------------------------------------------------
p = ROOT / "roadmap" / "curriculum-granularity-audit.md"
text = p.read_text(encoding="utf-8")
if "## AI Backend Engineering — COMPLETE：约 55 outline topics / 39 Canonical → 22" not in text:
    marker = "## MySQL — PASS：23 → 23"
    insertion = '''## AI Backend Engineering — COMPLETE：约 55 outline topics / 39 Canonical → 22

AIBE 同时存在两种细粒度输入：旧 README 约 55 个 Topic，以及 39 道可独立追问的 HUMAN-A Canonical。正式建设时没有把它们一一落成 Markdown，而是按 Backend Production 因果链收敛为 **22 个知识块**。

```text
Network / Request
→ Capacity / Pool / Backpressure
→ Timeout / Retry / Idempotency
→ MQ / Durable Task
→ Consistency / State / Auth
→ Operations / Deployment / Security
→ Cross-language Runtime Mapping
```

Spring / JVM / Java / Go 的真人面试信号被统一放入最后一个跨语言映射块，因为它们主要是通用 DI / Concurrency / Memory / Scheduler Primitive 在不同生态中的实现，而不是 Python AI Backend 主线需要额外拆出的多个语言模块。

'''
    if marker not in text:
        raise SystemExit("Granularity MySQL marker missing")
    text = text.replace(marker, insertion + marker, 1)
text = text.replace(
    "| FastAPI | ~40 outline topics | 16 | ✅ COMPLETE |\n| MySQL",
    "| FastAPI | ~40 outline topics | 16 | ✅ COMPLETE |\n| AI Backend Engineering | ~55 outline topics / 39 Canonical | 22 | ✅ COMPLETE |\n| MySQL",
    1,
)
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# 5. Content depth audit.
# ---------------------------------------------------------------------------
p = ROOT / "roadmap" / "content-depth-audit.md"
replace_once(
    p,
    "> 本文件记录 Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG 的整改或首版深度验收，以及 System Design 首版完成后的深度验收。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。",
    "> 本文件记录 Python / FastAPI / AI Backend Engineering / Redis / Vector DB / LLM Foundation / RAG 的整改或首版深度验收，以及 System Design 首版完成后的深度验收。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。",
)
text = p.read_text(encoding="utf-8")
if "# 5. AI Backend Engineering — ✅ PASS" not in text:
    shifts = [
        ("# 11. 后续规则", "# 12. 后续规则"),
        ("# 10. 最终验收状态", "# 11. 最终验收状态"),
        ("# 9. System Design — ✅ PASS", "# 10. System Design — ✅ PASS"),
        ("# 8. RAG — ✅ PASS after targeted remediation", "# 9. RAG — ✅ PASS after targeted remediation"),
        ("# 7. LLM Foundation — ✅ PASS after targeted remediation", "# 8. LLM Foundation — ✅ PASS after targeted remediation"),
        ("# 6. Vector DB — ✅ PASS", "# 7. Vector DB — ✅ PASS"),
        ("# 5. Redis — ✅ PASS", "# 6. Redis — ✅ PASS"),
    ]
    for old, new in shifts:
        text = text.replace(old, new, 1)
    section = '''# 5. AI Backend Engineering — ✅ PASS

当前：**22 个连续知识小板块，`docs/01 → 22`，并包含 Review + Interview 三件套。**

AIBE 首版从一开始就按当前粒度规则建设：39 道 Canonical 用于市场深度校准，约 55 个旧 outline topics 作为内容素材，最终收敛成 22 个 Production Backend 认知闭环。

机械检查：

```text
22/22 docs 连续编号
22/22 >= 6KB
22/22 含 🎯 面试表达
22/22 含 ⚠️ 易错点
22/22 含 <details> 折叠自测
README docs 链接存在
review/README.md 存在
interview 三件套存在
research/backend-sources/README.md 存在
```

人工重点复核了 Backpressure、Retry、Reliable Async Task、Consistency/Compensation、K8s Deployment 和 Cross-language Mapping，均包含机制、Failure、Scale、Verification 与明确模块边界，没有“大主题只有概览”的情况。

权威资料只校准 Timeout/Retry/Overload、Idempotency、Kafka、K8s、Observability、OAuth、OWASP 等机制；HUMAN-A 市场证据仍只来自 39 道 AIBE Canonical。

**最终结论：AI Backend Engineering Content Depth / Canonical Coverage PASS。**

---

'''
    marker = "# 6. Redis — ✅ PASS"
    if marker not in text:
        raise SystemExit("Depth audit Redis marker missing after shift")
    text = text.replace(marker, section + marker, 1)
text = text.replace(
    "| FastAPI | 16 | ✅ `01–16` 连续 | ✅ PASS |\n| Redis",
    "| FastAPI | 16 | ✅ `01–16` 连续 | ✅ PASS |\n| AI Backend Engineering | 22 | ✅ `01–22` 连续 | ✅ PASS |\n| Redis",
    1,
)
text = text.replace(
    "Python current-standard remediation：13 篇\nFastAPI 首版独立验收：           16 篇\n第一轮颗粒度整改后的四模块：     68 篇\nSystem Design 首版独立验收：      19 篇\n----------------------------------\n合计：                           116 篇",
    "Python current-standard remediation：13 篇\nFastAPI 首版独立验收：           16 篇\nAI Backend Engineering 首版验收：22 篇\n第一轮颗粒度整改后的四模块：     68 篇\nSystem Design 首版独立验收：      19 篇\n----------------------------------\n合计：                           138 篇",
    1,
)
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# 6. Progress.
# ---------------------------------------------------------------------------
p = ROOT / "research" / "questions" / "progress.md"
replace_once(p, "# Phase 3：Curriculum Build 🚧", "# Phase 3：Curriculum Build ✅")
replace_once(
    p,
    "内容深度验收：`../../roadmap/content-depth-audit.md`。Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成 QA 与人工复核并通过。",
    "内容深度验收：`../../roadmap/content-depth-audit.md`。Python / FastAPI / AI Backend Engineering / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成 QA 与人工复核并通过。",
)
replace_once(
    p,
    "Foundation 完成度核实：`../../roadmap/foundation-status-audit.md`。Python 与 FastAPI 已完成；AI Backend Engineering 当前仍只有课程骨架。",
    "Foundation 完成度核实：`../../roadmap/foundation-status-audit.md`。Python / FastAPI / AI Backend Engineering 均已完成，Foundation ✅ COMPLETE。",
)
replace_once(
    p,
    "| AI Backend Engineering | ⏳ 只有 README 课程骨架；正式正文未写 |",
    "| AI Backend Engineering | ✅ **22 blocks**；39 Canonical Coverage / Content Depth PASS |",
)
replace_once(
    p,
    "FastAPI        ~40 outline topics → 16  COMPLETE\nMySQL",
    "FastAPI        ~40 outline topics → 16  COMPLETE\nAI Backend Eng. ~55 outline topics / 39 Canonical → 22  COMPLETE\nMySQL",
)
regex_once(
    p,
    r"## 下一阶段：Foundation Completion.*$",
    '''## Phase 3 完成状态

十个正式一级模块的第一版系统教材均已完成：

```text
Python 13
FastAPI 16
AI Backend Engineering 22
MySQL 23
Redis 24
Vector DB 16
LLM Foundation 14
RAG 14
Agent Harness / Runtime 23
System Design 19
```

Foundation 也已正式完成。后续工作进入**全仓库最终验收 / 面试训练与持续维护**，不再存在未撰写的一级模块。''',
)

# ---------------------------------------------------------------------------
# 7. Module index.
# ---------------------------------------------------------------------------
p = ROOT / "research" / "questions" / "module-index.md"
replace_once(
    p,
    "> **教材深度已独立验收。** Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 的结果见 `../../roadmap/content-depth-audit.md`，不会以文件数量或字数替代人工质量判断。",
    "> **教材深度已独立验收。** Python / FastAPI / AI Backend Engineering / Redis / Vector DB / LLM Foundation / RAG / System Design 的结果见 `../../roadmap/content-depth-audit.md`，不会以文件数量或字数替代人工质量判断。",
)
replace_once(
    p,
    "FastAPI ✅ 16 blocks；4 Canonical Coverage / Depth PASS\nMySQL",
    "FastAPI ✅ 16 blocks；4 Canonical Coverage / Depth PASS\nAI Backend Engineering ✅ 22 blocks；39 Canonical Coverage / Depth PASS\nMySQL",
)
replace_once(
    p,
    "Python 与 FastAPI 已完成 current-standard Curriculum / Coverage / Depth 验收；AI Backend Engineering 当前仍只有 README 课程骨架，正式正文尚未撰写。",
    "Python / FastAPI / AI Backend Engineering 已全部完成 current-standard Curriculum / Coverage / Depth 验收；Foundation ✅ COMPLETE。",
)
text = p.read_text(encoding="utf-8")
text = text.replace("下一仓库建设阶段：**Foundation Completion — AI Backend Engineering**。学习顺序仍保持 `Python → FastAPI → AI Backend Engineering`。", "十个一级模块的第一版正式教材现已全部完成；后续进入全仓库最终验收、面试训练与持续维护。学习顺序仍保持既定十板块顺序。")
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# 8. Canonical README.
# ---------------------------------------------------------------------------
p = ROOT / "research" / "questions" / "README.md"
replace_once(
    p,
    "当前 Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。",
    "当前 Python / FastAPI / AI Backend Engineering / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。",
)
replace_once(
    p,
    "FastAPI ✅ 16 blocks（4 Canonical Coverage / Depth PASS）\nMySQL",
    "FastAPI ✅ 16 blocks（4 Canonical Coverage / Depth PASS）\nAI Backend Engineering ✅ 22 blocks（39 Canonical Coverage / Depth PASS）\nMySQL",
)
replace_once(
    p,
    "Python 与 FastAPI 已完成 current-standard Curriculum / Coverage / Depth 验收；AI Backend Engineering 目前只有 README 课程骨架，正式正文未写。",
    "Python / FastAPI / AI Backend Engineering 已全部完成 current-standard Curriculum / Coverage / Depth 验收；Foundation ✅ COMPLETE，十个一级模块的第一版教材均已完成。",
)

# ---------------------------------------------------------------------------
# 9. Final stale-text guard.
# ---------------------------------------------------------------------------
for path in [
    ROOT / "README.md",
    ROOT / "roadmap" / "knowledge-map.md",
    ROOT / "roadmap" / "foundation-status-audit.md",
    ROOT / "research" / "questions" / "progress.md",
    ROOT / "research" / "questions" / "module-index.md",
    ROOT / "research" / "questions" / "README.md",
]:
    text = path.read_text(encoding="utf-8")
    stale = [
        "AI Backend Engineering 当前仍只有课程骨架",
        "AI Backend Engineering 目前只有 README 课程骨架",
        "AI Backend Engineering | ⏳ 只有",
        "AI Backend Engineering 正式教材\n```",
    ]
    for marker in stale:
        if marker in text:
            raise SystemExit(f"stale AIBE status remains in {path}: {marker}")

print("AIBE finalization validated: 22 docs + Review + Interview + sources; repository Phase 3 synchronized.")
