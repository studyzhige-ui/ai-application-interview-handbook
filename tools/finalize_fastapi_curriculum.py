from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FAST = ROOT / "fastapi"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"missing anchor in {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def regex_once(path: Path, pattern: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    new_text, n = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit(f"regex anchor mismatch in {path}: {pattern[:100]!r}, matches={n}")
    path.write_text(new_text, encoding="utf-8")


# ---------------------------------------------------------------------------
# 0. Validate FastAPI module before marking it complete.
# ---------------------------------------------------------------------------
docs = sorted((FAST / "docs").glob("[0-9][0-9]-*.md"))
nums = [int(p.name[:2]) for p in docs]
if nums != list(range(1, 17)):
    raise SystemExit(f"FastAPI docs numbering invalid: {nums}")

for p in docs:
    text = p.read_text(encoding="utf-8")
    if len(text.encode("utf-8")) < 4500:
        raise SystemExit(f"FastAPI doc suspiciously short: {p}")
    if "<details" not in text:
        raise SystemExit(f"FastAPI doc missing folded self-test: {p}")
    if "面试怎么回答" not in text:
        raise SystemExit(f"FastAPI doc missing interview answer: {p}")

readme = FAST / "README.md"
readme_text = readme.read_text(encoding="utf-8")
for target in re.findall(r"\]\((docs/[^)#]+\.md)\)", readme_text):
    if not (FAST / target).exists():
        raise SystemExit(f"FastAPI README broken doc link: {target}")

required = [
    FAST / "review" / "README.md",
    FAST / "interview" / "高频面试题.md",
    FAST / "interview" / "面试易错点.md",
    FAST / "interview" / "面试前速查表.md",
    ROOT / "research" / "fastapi-sources" / "README.md",
]
for p in required:
    if not p.exists():
        raise SystemExit(f"FastAPI required file missing: {p}")

# ---------------------------------------------------------------------------
# 1. Root README.
# ---------------------------------------------------------------------------
p = ROOT / "README.md"
replace_once(
    p,
    "Python / Redis / Vector DB / LLM Foundation / RAG / System Design 的正文深度已完成 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。",
    "Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 的正文深度已完成 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。",
)
replace_once(
    p,
    "Foundation 的真实完成度见 [`roadmap/foundation-status-audit.md`](roadmap/foundation-status-audit.md)。Python current-standard remediation 已完成；Foundation 剩余缺口只有：**FastAPI → AI Backend Engineering**。",
    "Foundation 的真实完成度见 [`roadmap/foundation-status-audit.md`](roadmap/foundation-status-audit.md)。Python 与 FastAPI 已完成；Foundation 当前唯一正式教材缺口是 **AI Backend Engineering**。",
)
replace_once(
    p,
    "- [FastAPI](fastapi/README.md) ⏳ **只有 README 课程骨架**；正式 `docs / review / interview` 尚未撰写",
    "- [FastAPI](fastapi/README.md) ✅ **16 个知识小板块**；4 道 Canonical Coverage + 当前官方机制校准 + Depth PASS",
)
replace_once(
    p,
    "MySQL 23\nRedis 24\nVector DB 16\nLLM Foundation 14\nRAG 14\nAgent Harness 23\nSystem Design 19",
    "Python 13\nFastAPI 16\nMySQL 23\nRedis 24\nVector DB 16\nLLM Foundation 14\nRAG 14\nAgent Harness 23\nSystem Design 19",
)
replace_once(
    p,
    "| FastAPI | ⏳ README 课程骨架；正式正文未写 |",
    "| FastAPI | ✅ 16-block；4 Canonical Coverage / Depth PASS |",
)

# ---------------------------------------------------------------------------
# 2. Knowledge map.
# ---------------------------------------------------------------------------
p = ROOT / "roadmap" / "knowledge-map.md"
replace_once(
    p,
    "内容深度验收：[`content-depth-audit.md`](content-depth-audit.md)；Redis / Vector DB / LLM Foundation / RAG / System Design 均已通过。",
    "内容深度验收：[`content-depth-audit.md`](content-depth-audit.md)；Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 均已通过。",
)
regex_once(
    p,
    r"## FastAPI ⏳\n.*?\n\n## AI Backend Engineering ⏳",
    "## FastAPI ✅ — 16 blocks\n入口：[`../fastapi/README.md`](../fastapi/README.md) — 已完成 `docs/01–16`、Review、Interview 与官方技术资料索引；4 道 FastAPI Canonical 已映射到 beginner-first Web/API 主干，Content Depth PASS。\n\n## AI Backend Engineering ⏳",
)
replace_once(
    p,
    "| FastAPI | ⏳ 只有课程骨架；正式正文未写 |",
    "| FastAPI | ✅ 16 blocks；Canonical Coverage / Depth PASS |",
)

# ---------------------------------------------------------------------------
# 3. Foundation status audit: rewrite FastAPI section and build order.
# ---------------------------------------------------------------------------
p = ROOT / "roadmap" / "foundation-status-audit.md"
fastapi_section = '''## 1. FastAPI — ✅ 16 blocks / Canonical Coverage / Depth PASS

当前仓库实际结构：

```text
fastapi/
├── README.md
├── docs/       01–16 连续知识小板块
├── review/     六张总图 + 24 个综合折叠自测
└── interview/  30 道高频题 + 60 个易错点 + 速查表
```

并建立：

```text
research/fastapi-sources/README.md
```

用于记录 FastAPI / Starlette / Uvicorn / Pydantic 当前官方机制；权威资料只校准技术事实，不改变 HUMAN-A Source Count。

原 README 有约 40 个细粒度内容标题，它们是 Section / Capability 粒度，不适合直接做 40 个 Markdown。正式教材收敛为 16 个认知闭环：

```text
ASGI Request Lifecycle
→ API Contract / Validation
→ DI / Middleware / Resource Lifecycle
→ Async / Blocking Boundary
→ Streaming / SSE / WebSocket
→ Security / Tenant Context
→ External Resource Integration
→ Background / Upload / Long-running Boundary
→ Timeout / Cancellation / Disconnect
→ Testing / Observability / Deployment
→ AI Service Patterns
```

4 道 FastAPI HUMAN-A Canonical 的作用是校准重点，而不是决定目录：

```text
FASTAPI-001  ASGI / Request Lifecycle        → 01 / 02 / 05
FASTAPI-002  Middleware vs Dependency        → 04 / 05 / 09
FASTAPI-004  SSE / Agent Streaming           → 07 / 08 / 12 / 16
FASTAPI-005  Agent Service Framework Boundary→ 05–16，重点 16
```

低频但必要的 Routing、Pydantic、Testing、Deployment 等仍保留在完整知识主干中。

完成后机械核验：

```text
docs = 01–16 连续
16/16 正文 >= 4.5KB
16/16 正文含面试回答与折叠自测
README 正文链接存在
Review / Interview 三件套存在
Official Source Index 存在
```

人工重点复核了 `05 Resource Lifecycle`、`07 Streaming/SSE`、`12 Timeout/Cancellation`、`15 Deployment`、`16 AI Service Patterns`，没有发现“大主题只有概览”的短稿。

**结论：FastAPI Formal Curriculum = COMPLETE；Content Depth / Canonical Coverage = PASS。**
'''
regex_once(
    p,
    r"## 1\. FastAPI — .*?\n\n---\n\n## 2\. AI Backend Engineering",
    fastapi_section + "\n---\n\n## 2. AI Backend Engineering",
)
replace_once(
    p,
    "1. FastAPI：从 README 骨架写成正式 docs / review / interview\n2. AI Backend Engineering：从 README 骨架写成正式 docs / review / interview\n\nPython 的 current-standard remediation 已提前完成，不再列为待办。",
    "1. AI Backend Engineering：从 README 骨架写成正式 docs / review / interview\n\nPython 与 FastAPI 已完成，不再列为待办。",
)

# ---------------------------------------------------------------------------
# 4. Granularity audit.
# ---------------------------------------------------------------------------
p = ROOT / "roadmap" / "curriculum-granularity-audit.md"
if "## FastAPI — COMPLETE：约 40 个 outline topics → 16" not in p.read_text(encoding="utf-8"):
    text = p.read_text(encoding="utf-8")
    marker = "## MySQL — PASS：23 → 23"
    insertion = '''## FastAPI — COMPLETE：约 40 个 outline topics → 16

旧 FastAPI README 规划了约 40 个细粒度标题，但其中 Router、Pydantic、Streaming、Auth、Client、Testing 等很多只是同一知识系统里的 Section。正式建设时没有把这些标题机械落成文件，而是按 Request Lifecycle、Resource Lifecycle、Async/Streaming、Production Boundary 等认知闭环收敛为 **16 blocks**。

同时也没有因为 FastAPI 只有 4 道 Primary Canonical 就只写 4 章：Canonical 决定真实问法和深度，完整 Web/API 前置仍由知识体系保证。

'''
    if marker not in text:
        raise SystemExit("granularity MySQL marker missing")
    p.write_text(text.replace(marker, insertion + marker, 1), encoding="utf-8")
replace_once(
    p,
    "| Python | 12 | 13 | ✅ COMPLETE |\n| MySQL | 23 | 23 | ✅ PASS |",
    "| Python | 12 | 13 | ✅ COMPLETE |\n| FastAPI | ~40 outline topics | 16 | ✅ COMPLETE |\n| MySQL | 23 | 23 | ✅ PASS |",
)

# ---------------------------------------------------------------------------
# 5. Content depth audit.
# ---------------------------------------------------------------------------
p = ROOT / "roadmap" / "content-depth-audit.md"
replace_once(
    p,
    "> 本文件记录 Python / Redis / Vector DB / LLM Foundation / RAG 的整改后深度验收，以及 System Design 首版完成后的深度验收。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。",
    "> 本文件记录 Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG 的整改或首版深度验收，以及 System Design 首版完成后的深度验收。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。",
)
if "# 4. FastAPI — ✅ PASS" not in p.read_text(encoding="utf-8"):
    text = p.read_text(encoding="utf-8")
    # shift existing numbered module/final headings after Python
    shifts = [
        ("# 10. 后续规则", "# 11. 后续规则"),
        ("# 9. 最终验收状态", "# 10. 最终验收状态"),
        ("# 8. System Design — ✅ PASS", "# 9. System Design — ✅ PASS"),
        ("# 7. RAG — ✅ PASS after targeted remediation", "# 8. RAG — ✅ PASS after targeted remediation"),
        ("# 6. LLM Foundation — ✅ PASS after targeted remediation", "# 7. LLM Foundation — ✅ PASS after targeted remediation"),
        ("# 5. Vector DB — ✅ PASS", "# 6. Vector DB — ✅ PASS"),
        ("# 4. Redis — ✅ PASS", "# 5. Redis — ✅ PASS"),
    ]
    for old, new in shifts:
        text = text.replace(old, new, 1)
    fast_depth = '''# 4. FastAPI — ✅ PASS

当前：**16 个连续知识小板块，`docs/01 → 16`，并包含 Review + Interview 三件套。**

FastAPI 从旧 README 的约 40 个 outline topics 直接按当前教材粒度规则重建为 16 个认知闭环，没有经历“一个小标题一个文件”的过度拆分。

完成后机械检查：

```text
16/16 docs 连续编号
16/16 >= 4.5KB
16/16 含 🎯 面试回答
16/16 含 <details> 折叠自测
README docs 链接存在
review/README.md 存在
interview 三件套存在
research/fastapi-sources/README.md 存在
```

人工重点复核：

- `05-ResourceLifecycle.md`：是否真正讲清 yield Dependency scope、Streaming cleanup 与 Lifespan；
- `07-Streaming与SSE.md`：是否包含 typed event、mid-stream error、disconnect，而不是只教 `yield token`；
- `12-TimeoutCancellation与Disconnect.md`：是否区分 Transport Disconnect、Timeout、Coroutine Cancel、Business Cancel 和 Durable Run；
- `15-Deployment与GracefulShutdown.md`：是否覆盖 Worker Process、Pool multiplication、Liveness/Readiness、Drain / Shutdown；
- `16-AIServicePatterns.md`：是否真正把 Chat / RAG / Ingestion / Agent Run API 与 Agent Harness 分层。

权威技术事实使用当前 FastAPI / Starlette / Uvicorn / Pydantic 官方资料校准；HUMAN-A 市场证据仍只来自 4 道 FastAPI Canonical。

**最终结论：FastAPI Content Depth / Canonical Coverage PASS。**

---

'''
    marker = "# 5. Redis — ✅ PASS"
    if marker not in text:
        raise SystemExit("content depth Redis shifted marker missing")
    text = text.replace(marker, fast_depth + marker, 1)
    p.write_text(text, encoding="utf-8")

# final audit table: add Python and FastAPI if absent
text = p.read_text(encoding="utf-8")
old_table = "| 模块 | Blocks | Numbering | Depth |\n|---|---:|---|---|\n| Redis | 24 | ✅ `01–24` 连续 | ✅ PASS |"
new_table = "| 模块 | Blocks | Numbering | Depth |\n|---|---:|---|---|\n| Python | 13 | ✅ `01–13` 连续 | ✅ PASS |\n| FastAPI | 16 | ✅ `01–16` 连续 | ✅ PASS |\n| Redis | 24 | ✅ `01–24` 连续 | ✅ PASS |"
if old_table in text:
    text = text.replace(old_table, new_table, 1)
text = text.replace(
    "Python current-standard remediation：13 篇\n第一轮颗粒度整改后的四模块： 68 篇\nSystem Design 首版独立验收：     19 篇\n---------------------------------\n合计：                          100 篇",
    "Python current-standard remediation：13 篇\nFastAPI 首版独立验收：           16 篇\n第一轮颗粒度整改后的四模块：     68 篇\nSystem Design 首版独立验收：      19 篇\n----------------------------------\n合计：                           116 篇",
)
p.write_text(text, encoding="utf-8")

# ---------------------------------------------------------------------------
# 6. Progress.
# ---------------------------------------------------------------------------
p = ROOT / "research" / "questions" / "progress.md"
replace_once(
    p,
    "内容深度验收：`../../roadmap/content-depth-audit.md`。Python / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成 QA 与人工复核并通过。",
    "内容深度验收：`../../roadmap/content-depth-audit.md`。Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成 QA 与人工复核并通过。",
)
replace_once(
    p,
    "Foundation 完成度核实：`../../roadmap/foundation-status-audit.md`。Python current-standard remediation 已完成；FastAPI / AI Backend Engineering 当前仍只有课程骨架。",
    "Foundation 完成度核实：`../../roadmap/foundation-status-audit.md`。Python 与 FastAPI 已完成；AI Backend Engineering 当前仍只有课程骨架。",
)
replace_once(
    p,
    "| FastAPI | ⏳ 只有 README 课程骨架；正式正文未写 |",
    "| FastAPI | ✅ **16 blocks**；4 Canonical Coverage / Content Depth PASS |",
)
replace_once(
    p,
    "Python         12 → 13  COMPLETE\nMySQL",
    "Python         12 → 13  COMPLETE\nFastAPI        ~40 outline topics → 16  COMPLETE\nMySQL",
)
regex_once(
    p,
    r"## 下一阶段：Foundation Completion\n\n.*?学习者的正式学习顺序仍为 `Python → FastAPI → AI Backend Engineering`。",
    "## 下一阶段：Foundation Completion\n\nPython 与 FastAPI 已完成，Foundation 当前唯一缺口是：\n\n```text\nAI Backend Engineering 正式教材\n```\n\n学习者的正式学习顺序仍为 `Python → FastAPI → AI Backend Engineering`。",
)

# ---------------------------------------------------------------------------
# 7. Module index.
# ---------------------------------------------------------------------------
p = ROOT / "research" / "questions" / "module-index.md"
replace_once(
    p,
    "> **教材深度已独立验收。** Redis / Vector DB / LLM Foundation / RAG / System Design 的结果见 `../../roadmap/content-depth-audit.md`，不会以文件数量或字数替代人工质量判断。",
    "> **教材深度已独立验收。** Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 的结果见 `../../roadmap/content-depth-audit.md`，不会以文件数量或字数替代人工质量判断。",
)
replace_once(
    p,
    "Python ✅ 13 blocks；15 Canonical Coverage / Depth PASS\nMySQL",
    "Python ✅ 13 blocks；15 Canonical Coverage / Depth PASS\nFastAPI ✅ 16 blocks；4 Canonical Coverage / Depth PASS\nMySQL",
)
replace_once(
    p,
    "Python 已完成 13-block current-standard Canonical Coverage / Depth Remediation；FastAPI / AI Backend Engineering 当前仍只有 README 课程骨架，正式正文尚未撰写。",
    "Python 与 FastAPI 已完成 current-standard Curriculum / Coverage / Depth 验收；AI Backend Engineering 当前仍只有 README 课程骨架，正式正文尚未撰写。",
)
replace_once(
    p,
    "下一仓库建设阶段：**Foundation Completion — FastAPI → AI Backend Engineering → Python v1 Remediation**。学习顺序仍保持 `Python → FastAPI → AI Backend Engineering`。",
    "下一仓库建设阶段：**Foundation Completion — AI Backend Engineering**。学习顺序仍保持 `Python → FastAPI → AI Backend Engineering`。",
)

# ---------------------------------------------------------------------------
# 8. Canonical README.
# ---------------------------------------------------------------------------
p = ROOT / "research" / "questions" / "README.md"
replace_once(
    p,
    "当前 Python / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。",
    "当前 Python / FastAPI / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。",
)
replace_once(
    p,
    "Python ✅ 13 blocks（12→13；15 Canonical Coverage / Depth PASS）\nMySQL",
    "Python ✅ 13 blocks（12→13；15 Canonical Coverage / Depth PASS）\nFastAPI ✅ 16 blocks（4 Canonical Coverage / Depth PASS）\nMySQL",
)
replace_once(
    p,
    "Python current-standard remediation 已完成；FastAPI / AI Backend Engineering 目前只有 README 课程骨架，正式正文未写。",
    "Python 与 FastAPI 已完成 current-standard Curriculum / Coverage / Depth 验收；AI Backend Engineering 目前只有 README 课程骨架，正式正文未写。",
)

# ---------------------------------------------------------------------------
# 9. Final stale-state assertions.
# ---------------------------------------------------------------------------
status_files = [
    ROOT / "README.md",
    ROOT / "roadmap" / "knowledge-map.md",
    ROOT / "roadmap" / "foundation-status-audit.md",
    ROOT / "research" / "questions" / "progress.md",
    ROOT / "research" / "questions" / "module-index.md",
    ROOT / "research" / "questions" / "README.md",
]
for p in status_files:
    text = p.read_text(encoding="utf-8")
    bad = [
        "FastAPI | ⏳",
        "FastAPI — ⏳",
        "FastAPI / AI Backend Engineering 当前仍只有课程骨架",
        "FastAPI / AI Backend Engineering 目前只有 README 课程骨架",
    ]
    for marker in bad:
        if marker in text:
            raise SystemExit(f"stale FastAPI status remains in {p}: {marker}")

print("FastAPI finalization validated: 16 docs + review/interview + sources + repository status synchronized.")
