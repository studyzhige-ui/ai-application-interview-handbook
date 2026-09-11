from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise SystemExit(f"{path}: missing anchor: {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def add_after(path: str, anchor: str, addition: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if addition in text:
        return
    if anchor not in text:
        raise SystemExit(f"{path}: missing anchor for addition: {anchor[:120]!r}")
    p.write_text(text.replace(anchor, anchor + "\n" + addition, 1), encoding="utf-8")


# ---------------------------------------------------------------------------
# Module-level truth
# ---------------------------------------------------------------------------
add_after(
    "fastapi/README.md",
    "# FastAPI｜AI 应用服务层",
    "\n> **Status：⏳ 课程骨架已完成，正式教材尚未撰写。** 当前仓库只有本 README/课程蓝图，尚无 `docs/`、`review/`、`interview/`。System Design 完成后回到 Foundation，FastAPI 是第一项正式补齐工作。详见 [`../roadmap/foundation-status-audit.md`](../roadmap/foundation-status-audit.md)。",
)
add_after(
    "backend-engineering/README.md",
    "# AI Backend Engineering｜AI 应用后端工程基础",
    "\n> **Status：⏳ 课程骨架已完成，正式教材尚未撰写。** 当前仓库只有本 README/课程蓝图，尚无 `docs/`、`review/`、`interview/`。System Design 已完成，后续在 FastAPI 正文之后正式建设这一横向 Production 主线。详见 [`../roadmap/foundation-status-audit.md`](../roadmap/foundation-status-audit.md)。",
)
add_after(
    "python/README.md",
    "# Python Foundation｜秋招面试知识手册",
    "\n> **Status：🟠 v1 完整可用，但当前统一标准的二次整改尚未完成。** 现有 `12` 章正文 + Review + Interview 可以正常学习；后续不推倒重写，而是在 FastAPI / AI Backend Engineering 补齐后，对照最新 `15` 道 Python Canonical 做 Coverage / Depth Remediation。详见 [`../roadmap/foundation-status-audit.md`](../roadmap/foundation-status-audit.md)。",
)
add_after(
    "system-design/README.md",
    "# System Design｜AI Application / Agent Production 终局模块",
    "\n> **Status：✅ 第一版完整系统教材已完成。** 当前为 `19` 个连续知识小板块 + Review + Interview 三件套；24 道 System Design Canonical 已按场景/能力映射进入教材，而不是一题一章。",
)

# ---------------------------------------------------------------------------
# Root README
# ---------------------------------------------------------------------------
add_after(
    "README.md",
    "Redis / Vector DB / LLM Foundation / RAG 的正文深度也已完成全量 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。",
    "Foundation 的真实完成度与 Python v1 质量核实见 [`roadmap/foundation-status-audit.md`](roadmap/foundation-status-audit.md)。System Design 完成后的仓库补齐顺序是：**FastAPI → AI Backend Engineering → Python v1 定向整改**。",
)
replace_once(
    "README.md",
    "- [Python Foundation](python/README.md) ✅ 完整系统教材\n- [FastAPI](fastapi/README.md) 🟡 完整课程骨架，正文后续补齐\n- [AI Backend Engineering](backend-engineering/README.md) 🟡 完整课程骨架，按 Production 主线持续补齐",
    "- [Python Foundation](python/README.md) 🟠 **v1 完整可用**；最新 15 Canonical / 当前统一深度标准的定向整改待完成\n- [FastAPI](fastapi/README.md) ⏳ **只有 README 课程骨架**；正式 `docs / review / interview` 尚未撰写\n- [AI Backend Engineering](backend-engineering/README.md) ⏳ **只有 README 课程骨架**；正式 `docs / review / interview` 尚未撰写",
)
replace_once(
    "README.md",
    "## Integration\n\n- System Design ⏳ **下一正式模块**；开始前先按知识子系统确定教材粒度，再映射 24 道 System Design Canonical。",
    "## Integration\n\n- [System Design](system-design/README.md) ✅ **19 个知识小板块**；24 道 L4 Canonical 已映射到通用设计方法 + 7 类综合真人场景，Review / Interview 已完成。",
)
replace_once(
    "README.md",
    "MySQL 23\nRedis 24\nVector DB 16\nLLM Foundation 14\nRAG 14\nAgent Harness 23",
    "MySQL 23\nRedis 24\nVector DB 16\nLLM Foundation 14\nRAG 14\nAgent Harness 23\nSystem Design 19",
)
replace_once(
    "README.md",
    "| Python | ✅ 完整系统教材 |\n| FastAPI | 🟡 完整课程骨架 |\n| AI Backend Engineering | 🟡 完整课程骨架 |\n| MySQL | ✅ 23-block；Granularity PASS |\n| Redis | ✅ 24-block；整改完成 |\n| Vector DB | ✅ 16-block；整改完成 |\n| LLM Foundation | ✅ 14-block；整改完成 |\n| RAG | ✅ 14-block；整改完成 |\n| Agent Harness / Runtime | ✅ 23-block；结构整改 + 深度验收完成 |\n| System Design | ⏳ 下一正式模块 |",
    "| Python | 🟠 v1 完整可用；最新 Canonical / 当前深度标准定向整改待完成 |\n| FastAPI | ⏳ README 课程骨架；正式正文未写 |\n| AI Backend Engineering | ⏳ README 课程骨架；正式正文未写 |\n| MySQL | ✅ 23-block；Granularity PASS |\n| Redis | ✅ 24-block；整改完成 |\n| Vector DB | ✅ 16-block；整改完成 |\n| LLM Foundation | ✅ 14-block；整改完成 |\n| RAG | ✅ 14-block；整改完成 |\n| Agent Harness / Runtime | ✅ 23-block；结构整改 + 深度验收完成 |\n| System Design | ✅ 19-block；正文 + Review + Interview 完成 |",
)

# ---------------------------------------------------------------------------
# Knowledge map
# ---------------------------------------------------------------------------
replace_once(
    "roadmap/knowledge-map.md",
    "内容深度验收：[`content-depth-audit.md`](content-depth-audit.md)；Redis / Vector DB / LLM Foundation / RAG 均已通过。",
    "内容深度验收：[`content-depth-audit.md`](content-depth-audit.md)；Redis / Vector DB / LLM Foundation / RAG / System Design 均已通过。\nFoundation 实际完成度：[`foundation-status-audit.md`](foundation-status-audit.md)。",
)
replace_once(
    "roadmap/knowledge-map.md",
    "## Python ✅\n入口：[`../python/README.md`](../python/README.md) — 完整系统教材 + Review + Interview。\n\n## FastAPI 🟡\n入口：[`../fastapi/README.md`](../fastapi/README.md) — 完整课程骨架，正文后续补齐。\n\n## AI Backend Engineering 🟡\n入口：[`../backend-engineering/README.md`](../backend-engineering/README.md) — 完整课程骨架，是贯穿后续模块的横向 Production 主线。",
    "## Python 🟠\n入口：[`../python/README.md`](../python/README.md) — v1 已有 12 章正文 + Review + Interview，可学习；最新 15 Canonical / 当前统一深度标准的定向整改待完成。\n\n## FastAPI ⏳\n入口：[`../fastapi/README.md`](../fastapi/README.md) — 当前只有 README 课程骨架，正式 `docs / review / interview` 尚未撰写。\n\n## AI Backend Engineering ⏳\n入口：[`../backend-engineering/README.md`](../backend-engineering/README.md) — 当前只有 README 课程骨架，正式 `docs / review / interview` 尚未撰写。",
)
replace_once(
    "roadmap/knowledge-map.md",
    "# 8. System Design ⏳\n\nSystem Design 是第 10 个正式一级模块，也是当前下一阶段。\n\n开始前直接应用已验证的教材粒度规则：\n\n```text\n先画知识依赖与系统子域\n→ 确定知识小板块\n→ 决定 Markdown 文件\n→ 最后映射 24 道 System Design Canonical 与真实追问\n```\n\n禁止再从“一题一章”开始。\n\n未来重点：企业知识库 RAG、大规模文档 RAG、多租户 AI Chat / Agent Platform、Coding Agent Backend、Long-running Agent Platform、Multi-Agent Workflow、AI Customer Service、Data / Analytical Agent。",
    "# 8. System Design ✅ — 19 blocks\n\n入口：[`../system-design/README.md`](../system-design/README.md)。\n\n24 道 System Design Canonical 全部为 L4，但教材没有一题一章，而是组织为：\n\n```text\nPart A：12 个通用设计能力\nRequirement / SLO / Capacity / State / Flow\n→ Cache / Partition / Consistency / Queue\n→ Reliability / Multi-tenancy / Observability / Evaluation\n\nPart B：7 类综合真人场景\nHigh-concurrency Transactional\n→ Realtime Read-heavy\n→ Large-scale Data Processing\n→ LLM Gateway / Multi-tenant AI Platform\n→ Enterprise RAG\n→ Production / Long-running Agent Backend\n→ Vertical AI Agent Patterns\n```\n\n真人面经决定 Case、Failure、Scale 与 Verification 深度；通用知识依赖决定前 12 章主干。",
)
replace_once(
    "roadmap/knowledge-map.md",
    "| Python | ✅ 完整教材 |\n| FastAPI | 🟡 完整课程骨架 |\n| AI Backend Engineering | 🟡 完整课程骨架 |\n| MySQL | ✅ 23 blocks |\n| Redis | ✅ 24 blocks |\n| Vector DB | ✅ 16 blocks |\n| LLM Foundation | ✅ 14 blocks |\n| RAG | ✅ 14 blocks |\n| Agent Harness / Runtime | ✅ 23 blocks；深度验收完成 |\n| System Design | ⏳ 下一正式模块 |",
    "| Python | 🟠 v1 完整可用；定向整改待完成 |\n| FastAPI | ⏳ 只有课程骨架；正式正文未写 |\n| AI Backend Engineering | ⏳ 只有课程骨架；正式正文未写 |\n| MySQL | ✅ 23 blocks |\n| Redis | ✅ 24 blocks |\n| Vector DB | ✅ 16 blocks |\n| LLM Foundation | ✅ 14 blocks |\n| RAG | ✅ 14 blocks |\n| Agent Harness / Runtime | ✅ 23 blocks；深度验收完成 |\n| System Design | ✅ 19 blocks；Review / Interview 完成 |",
)

# ---------------------------------------------------------------------------
# Granularity audit
# ---------------------------------------------------------------------------
insert_sd = """
## System Design — COMPLETE：24 Canonical → 19 curriculum blocks

System Design 的 24 道 Canonical 全部是 L4 Scenario，但没有采用 `24 题 = 24 文件`。最终结构是：

```text
12 个通用设计知识块
+ 7 个综合 Scenario Pattern
= 19 个教材文件
```

前 12 章按 `Requirement → SLO → Capacity → State → Flow → Scale → Correctness → Reliability → Security → Verification` 的知识依赖建立；后 7 章再把 Flash Sale、Feed、Migration、LLM Gateway、Enterprise RAG、Production Agent 等真人场景映射进去。

这验证了本审计的核心规则：**Scenario 可以很多，但教材应先教可迁移的方法，再用 Scenario 验证迁移能力。**
""".strip()
add_after(
    "roadmap/curriculum-granularity-audit.md",
    "Agent / Workflow / Harness\n→ Loop / Event / State\n→ Tool Runtime\n→ Planning / Stop / Budget\n→ Context Assembly / Compaction\n→ Memory / State / Long-running Reliability\n→ Permission / Sandbox / Injection / Containment\n→ MCP / Skills / Hooks / Routing\n→ Multi-Agent / A2A / Workspace\n→ Trace / Eval / Coding Agent\n→ Production Runtime\n→ Framework Mapping\n```",
    "\n" + insert_sd,
)
replace_once(
    "roadmap/curriculum-granularity-audit.md",
    "| Agent Harness | 47 | 23 | ✅ COMPLETE（结构 + 深度） |",
    "| Agent Harness | 47 | 23 | ✅ COMPLETE（结构 + 深度） |\n| System Design | 24 Canonical | 19 | ✅ COMPLETE |",
)
replace_once(
    "roadmap/curriculum-granularity-audit.md",
    "# 6. System Design 的固定规则\n\nSystem Design 是下一模块，并直接使用本轮已经验证的粒度方法：\n\n```text\n先画知识依赖与子系统边界\n→ 确定知识小板块\n→ 再决定 Markdown 文件\n→ 最后映射 24 道 System Design Canonical 和真实追问\n```\n\n禁止再先按问题清单生成几十个 Markdown，再事后合并。",
    "# 6. System Design 验证结果\n\nSystem Design 已按本轮规则完成，并验证这套方法可以直接用于 Scenario-heavy 模块：\n\n```text\n先画知识依赖与子系统边界\n→ 12 个通用设计知识块\n→ 7 个综合场景知识块\n→ 最后映射 24 道 System Design Canonical 和真实追问\n```\n\n最终为 **19 blocks**，没有出现“一题一章”后再返工合并的问题。未来新增模块继续沿用同一方法。",
)

# ---------------------------------------------------------------------------
# Content depth audit
# ---------------------------------------------------------------------------
replace_once(
    "roadmap/content-depth-audit.md",
    "> 本文件记录 Redis / Vector DB / LLM Foundation / RAG 在颗粒度整改后的**内容深度验收**。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。",
    "> 本文件记录 Redis / Vector DB / LLM Foundation / RAG 的颗粒度整改后深度验收，以及 System Design 首版完成后的深度验收。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。",
)
sd_depth = """
# 7. System Design — ✅ PASS

当前：**19 个连续知识小板块，`docs/01 → 19`，并包含 Review + Interview 三件套。**

System Design 从一开始就按当前粒度规则建设，没有经历“24 道 Canonical → 24 个文件”的机械映射。正文分成：

```text
01–12  通用设计方法
13–19  综合 Scenario Pattern
```

完成后重点核验了：

- `01-SystemDesign职责与答题框架.md`：是否先教 Clarify / SLO / Capacity / State / Failure / Verify；
- `13-HighConcurrencyTransactionalSystems.md`：是否从业务 invariant 进入库存 / Rate Limit / Token Refresh，而不是背组件；
- `17-EnterpriseRAGSystemDesign.md`：是否覆盖 Ingestion / Permission / Generation / Evaluation / Freshness / Cost；
- `18-ProductionAgentBackend.md`：是否覆盖 Durable Run、Checkpoint、Tool Side Effect、Lease、Cancellation、Trace / Eval；
- `19-VerticalAIAgentPatterns.md`：是否能把同一套方法迁移到 Analysis / Customer Service / Multimodal / Game / Content，而不是五套模板。

19 章统一具备：

```text
Why / Requirement
→ Mental Model / Data Flow
→ Trade-off / Failure
→ Scale / Security / Reliability（按主题）
→ Verification / Observability
→ 面试回答
→ 折叠自测
```

并额外提供 6 张 Review 总图、36 道 Interview Drill、60 个易错点和面试前速查表。

**最终结论：System Design Content Depth PASS。**
""".strip()
add_after(
    "roadmap/content-depth-audit.md",
    "**最终结论：RAG Content Depth PASS。**",
    "\n---\n\n" + sd_depth,
)
replace_once(
    "roadmap/content-depth-audit.md",
    "| RAG | 14 | ✅ `01–14` 连续 | ✅ PASS |",
    "| RAG | 14 | ✅ `01–14` 连续 | ✅ PASS |\n| System Design | 19 | ✅ `01–19` 连续 | ✅ PASS |",
)

# ---------------------------------------------------------------------------
# Research progress / module index / README
# ---------------------------------------------------------------------------
add_after(
    "research/questions/progress.md",
    "内容深度验收：`../../roadmap/content-depth-audit.md`。Redis / Vector DB / LLM Foundation / RAG 已完成全量 QA 与人工复核并通过。",
    "Foundation 完成度核实：`../../roadmap/foundation-status-audit.md`。FastAPI / AI Backend Engineering 当前只有课程骨架；Python 是可用 v1，但需最新 Canonical / 当前统一深度标准的定向整改。",
)
replace_once(
    "research/questions/progress.md",
    "| Python | ✅ 既有完整系统教材 |\n| FastAPI | 🟡 完整课程骨架，正文后续补齐 |\n| AI Backend Engineering | 🟡 完整课程骨架，按 Production 主线持续补齐 |\n| MySQL | ✅ **23 blocks**；Granularity PASS |\n| Redis | ✅ **24 blocks**；27→24 整改完成 |\n| Vector DB | ✅ **16 blocks**；23→16 整改完成 |\n| LLM Foundation | ✅ **14 blocks**；29→14 整改完成 |\n| RAG | ✅ **14 blocks**；34→14 整改完成 |\n| Agent Harness / Runtime | ✅ **23 blocks**；47→23 结构整改 + 正文深度验收完成 |\n| System Design | ⏳ **下一正式模块** |",
    "| Python | 🟠 v1 完整可用；最新 15 Canonical / 当前标准定向整改待完成 |\n| FastAPI | ⏳ 只有 README 课程骨架；正式正文未写 |\n| AI Backend Engineering | ⏳ 只有 README 课程骨架；正式正文未写 |\n| MySQL | ✅ **23 blocks**；Granularity PASS |\n| Redis | ✅ **24 blocks**；27→24 整改完成 |\n| Vector DB | ✅ **16 blocks**；23→16 整改完成 |\n| LLM Foundation | ✅ **14 blocks**；29→14 整改完成 |\n| RAG | ✅ **14 blocks**；34→14 整改完成 |\n| Agent Harness / Runtime | ✅ **23 blocks**；47→23 结构整改 + 正文深度验收完成 |\n| System Design | ✅ **19 blocks**；正文 + Review + Interview 完成 |",
)
replace_once(
    "research/questions/progress.md",
    "Agent Harness  47 → 23  COMPLETE（结构 + 深度）",
    "Agent Harness  47 → 23  COMPLETE（结构 + 深度）\nSystem Design  24 Canonical → 19 curriculum blocks  COMPLETE",
)
replace_once(
    "research/questions/progress.md",
    "## 下一阶段\n\n```text\nSystem Design\n```\n\n开始时先画知识依赖与子系统边界，再确定教材文件粒度，最后映射 24 道 System Design Canonical 与真人追问；禁止一题一章。",
    "## 下一阶段：Foundation Completion\n\nSystem Design 已完成。接下来补齐此前 Foundation 的真实缺口，仓库建设顺序为：\n\n```text\nFastAPI 正式教材\n→ AI Backend Engineering 正式教材\n→ Python v1 Canonical Coverage / Depth Remediation\n```\n\n这只是建设顺序；学习者的正式学习顺序仍为 `Python → FastAPI → AI Backend Engineering`。",
)

replace_once(
    "research/questions/module-index.md",
    "> **教材深度已独立验收。** Redis / Vector DB / LLM Foundation / RAG 的结果见 `../../roadmap/content-depth-audit.md`，不会以文件数量或字数替代人工质量判断。",
    "> **教材深度已独立验收。** Redis / Vector DB / LLM Foundation / RAG / System Design 的结果见 `../../roadmap/content-depth-audit.md`，不会以文件数量或字数替代人工质量判断。\n> **Foundation 实际完成度已单独核实。** 见 `../../roadmap/foundation-status-audit.md`。",
)
replace_once(
    "research/questions/module-index.md",
    "Agent Harness / Runtime ✅ 23 blocks；47→23 COMPLETE + depth validated\nSystem Design ⏳ NEXT",
    "Agent Harness / Runtime ✅ 23 blocks；47→23 COMPLETE + depth validated\nSystem Design ✅ 19 blocks；24 Canonical → 19 curriculum blocks COMPLETE",
)
replace_once(
    "research/questions/module-index.md",
    "Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架。",
    "Python 已有可用 v1 教材但需当前标准定向整改；FastAPI / AI Backend Engineering 当前只有 README 课程骨架，正式正文尚未撰写。",
)
replace_once(
    "research/questions/module-index.md",
    "下一正式教材模块：**System Design**。",
    "下一仓库建设阶段：**Foundation Completion — FastAPI → AI Backend Engineering → Python v1 Remediation**。学习顺序仍保持 `Python → FastAPI → AI Backend Engineering`。",
)

replace_once(
    "research/questions/README.md",
    "当前 Redis / Vector DB / LLM Foundation / RAG 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。",
    "当前 Redis / Vector DB / LLM Foundation / RAG / System Design 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。\nFoundation 当前真实完成度详见 `../../roadmap/foundation-status-audit.md`。",
)
replace_once(
    "research/questions/README.md",
    "Agent Harness / Runtime ✅ 23 blocks（47→23，结构 + 深度验收完成）\nSystem Design ⏳ 下一正式模块",
    "Agent Harness / Runtime ✅ 23 blocks（47→23，结构 + 深度验收完成）\nSystem Design ✅ 19 blocks（24 Canonical → 19 curriculum blocks）",
)
replace_once(
    "research/questions/README.md",
    "Python 已有完整教材；FastAPI / AI Backend Engineering 已有完整课程骨架。",
    "Python 已有完整可用 v1，但需最新 Canonical / 当前深度标准定向整改；FastAPI / AI Backend Engineering 目前只有 README 课程骨架，正式正文未写。",
)

# Validate stale state phrases are gone from the key entry points.
checks = {
    "README.md": ["System Design ⏳", "FastAPI | 🟡", "AI Backend Engineering | 🟡"],
    "roadmap/knowledge-map.md": ["# 8. System Design ⏳", "FastAPI 🟡", "AI Backend Engineering 🟡"],
    "research/questions/progress.md": ["System Design | ⏳ **下一正式模块**"],
    "research/questions/module-index.md": ["System Design ⏳ NEXT", "下一正式教材模块：**System Design**"],
    "research/questions/README.md": ["System Design ⏳ 下一正式模块"],
}
for path, stale_items in checks.items():
    text = (ROOT / path).read_text(encoding="utf-8")
    for stale in stale_items:
        if stale in text:
            raise SystemExit(f"{path}: stale status remains: {stale}")

print("System Design completion and Foundation status synchronized successfully.")
