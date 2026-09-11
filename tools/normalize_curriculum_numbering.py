from pathlib import Path
from urllib.parse import unquote
import re

ROOT = Path(__file__).resolve().parents[1]

MODULE_COUNTS = {
    "redis": 24,
    "vector-db": 16,
    "llm-foundation": 14,
    "rag": 14,
}

RENAMES = {
    # Vector DB
    "05-ExactSearch与ANN.md": "03-ExactSearch与ANN.md",
    "07-ANN索引谱系.md": "04-ANN索引谱系.md",
    "08-HNSW机制与调优.md": "05-HNSW机制与调优.md",
    "10-IVF原理.md": "06-IVF原理.md",
    "11-Quantization与PQ.md": "07-Quantization与PQ.md",
    "12-IndexSelection.md": "08-IndexSelection.md",
    "13-Vector数据建模.md": "09-Vector数据建模.md",
    "14-MetadataFilter.md": "10-MetadataFilter.md",
    "15-Partition与TenantIsolation.md": "11-Partition与TenantIsolation.md",
    "16-VectorIndex生命周期.md": "12-VectorIndex生命周期.md",
    "19-分布式VectorDB.md": "13-分布式VectorDB.md",
    "20-性能容量与Production诊断.md": "14-性能容量与Production诊断.md",
    "22-产品与架构选型.md": "15-产品与架构选型.md",
    "23-GraphDB边界与系统设计.md": "16-GraphDB边界与系统设计.md",
    # LLM Foundation
    "05-TransformerBlock.md": "03-TransformerBlock.md",
    "06-Attention与Position.md": "04-Attention与Position.md",
    "10-Generation与Decoding.md": "05-Generation与Decoding.md",
    "13-KVCache与PrefillDecode.md": "06-KVCache与PrefillDecode.md",
    "15-ServingEngine与性能.md": "07-ServingEngine与性能.md",
    "19-ModelAPI与Selection.md": "08-ModelAPI与Selection.md",
    "21-Embedding与Reranker.md": "09-Embedding与Reranker.md",
    "23-MultimodalFoundation.md": "10-MultimodalFoundation.md",
    "24-PromptEngineering.md": "11-PromptEngineering.md",
    "25-Hallucination与干预边界.md": "12-Hallucination与干预边界.md",
    "27-FineTuning与LoRA.md": "13-FineTuning与LoRA.md",
    "29-PostTraining与Distillation.md": "14-PostTraining与Distillation.md",
    # RAG
    "03-CorpusGovernance.md": "02-CorpusGovernance.md",
    "05-DocumentProcessing.md": "03-DocumentProcessing.md",
    "08-ChunkingDesign.md": "04-ChunkingDesign.md",
    "11-AdvancedChunkStructure.md": "05-AdvancedChunkStructure.md",
    "14-QueryPlanning.md": "06-QueryPlanning.md",
    "18-RetrievalStack.md": "07-RetrievalStack.md",
    "22-Rerank与CandidateBudget.md": "08-Rerank与CandidateBudget.md",
    "24-EvidenceDelivery.md": "09-EvidenceDelivery.md",
    "26-RetrievalEvaluation.md": "10-RetrievalEvaluation.md",
    "28-EndToEndQualityEngineering.md": "11-EndToEndQualityEngineering.md",
    "31-ProductionGovernance.md": "12-ProductionGovernance.md",
    "33-ScaleCostObservability.md": "13-ScaleCostObservability.md",
    "34-GraphRAG与AgenticRAG.md": "14-GraphRAG与AgenticRAG.md",
}


def add_after(path: Path, anchor: str, line: str) -> None:
    text = path.read_text(encoding="utf-8")
    if line in text:
        return
    if anchor not in text:
        raise SystemExit(f"{path}: sync anchor not found: {anchor!r}")
    text = text.replace(anchor, anchor + "\n" + line, 1)
    path.write_text(text, encoding="utf-8")


# Replace stale references throughout Markdown files.
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    new_text = text
    for old, new in RENAMES.items():
        new_text = new_text.replace(old, new)

    new_text = re.sub(
        r"^>?\s*为避免[^\n]*历史文件编号[^\n]*\n?",
        "",
        new_text,
        flags=re.MULTILINE,
    )
    new_text = re.sub(
        r"^>?\s*文件保留合并后最早历史编号[^\n]*\n?",
        "",
        new_text,
        flags=re.MULTILINE,
    )
    new_text = new_text.replace(
        "正式学习顺序以本 README 为准；文件数量已经物理收敛为 16。",
        "当前 `docs/` 已连续编号为 `01–16`；正式学习顺序与文件编号一致。",
    )
    new_text = new_text.replace(
        "正式顺序以下面的 14-block 为准。",
        "当前 `docs/` 已连续编号为 `01–14`；正式学习顺序与文件编号一致。",
    )
    new_text = new_text.replace(
        "文件名保留了部分历史编号，正式学习顺序以 `../README.md` 为准。",
        "当前正文已连续编号，正式学习顺序与 `../README.md` 一致。",
    )

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")

# Normalize H1 numbering and require continuous filenames.
for module, count in MODULE_COUNTS.items():
    docs = ROOT / module / "docs"
    files = sorted(p for p in docs.glob("*.md") if re.match(r"^\d{2}-", p.name))
    prefixes = [int(p.name[:2]) for p in files]
    expected = list(range(1, count + 1))
    if prefixes != expected:
        raise SystemExit(f"{module}: numbering mismatch: {prefixes} != {expected}")

    for p in files:
        num = p.name[:2]
        text = p.read_text(encoding="utf-8")
        lines = text.splitlines()
        if not lines:
            raise SystemExit(f"{p}: empty file")
        title = re.sub(r"^#\s*\d{1,2}\s*(?:[.｜|:-]\s*)?", "", lines[0]).strip()
        if not title:
            raise SystemExit(f"{p}: cannot derive title from {lines[0]!r}")
        lines[0] = f"# {num}｜{title}"
        normalized = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
        if normalized != text:
            p.write_text(normalized, encoding="utf-8")

# Synchronize current depth-audit status into module/project entry points.
add_after(
    ROOT / "redis" / "README.md",
    "> **Granularity Audit：✅ 已完成。** 原 27 章经过教材粒度审计后收敛为 **24 个知识小板块**。合并依据不是章节数量，而是“一个文件是否形成完整认知闭环”。研究层的 19 道 Redis Canonical、Source Count 和真人面经频率没有变化。",
    "> **Content Depth Audit：✅ 通过。** `docs/01–24` 已完成全量结构扫描与人工复核；较短章节属于边界较窄的完整主题，不存在占位稿。详细记录见 [`../roadmap/content-depth-audit.md`](../roadmap/content-depth-audit.md)。",
)
add_after(
    ROOT / "llm-foundation" / "README.md",
    "> **Granularity Audit：✅ 已完成。** 原 29 章在不删知识点的前提下收敛为 **14 个正式知识小板块**。研究层 23 道 LLM Canonical、HUMAN-A Source Count 与模块边界完全不变。",
    "> **Content Depth Audit：✅ 通过。** `docs/01–14` 已连续编号并完成全量 QA；Multimodal Foundation 已补强到 Production 级输入预算、Failure Attribution、Evaluation 与治理深度。详细记录见 [`../roadmap/content-depth-audit.md`](../roadmap/content-depth-audit.md)。",
)
add_after(
    ROOT / "rag" / "README.md",
    "> **Granularity Audit：✅ 已完成。** 原 34 章内容已按 Production RAG 子系统收敛为 **14 个正式知识小板块**；29 道 RAG Canonical、88 个 HUMAN-A 覆盖来源和所有 Source Count 保持不变。",
    "> **Content Depth Audit：✅ 通过。** `docs/01–14` 已连续编号并完成全量 QA；Scale/Cost/Observability 与 GraphRAG/Agentic RAG 两个原先偏薄的大主题已完成 Production 深度补强。详细记录见 [`../roadmap/content-depth-audit.md`](../roadmap/content-depth-audit.md)。",
)

add_after(
    ROOT / "README.md",
    "因此不再默认 `1 Canonical ≈ 1 Markdown`。完整审计见 [`roadmap/curriculum-granularity-audit.md`](roadmap/curriculum-granularity-audit.md)。",
    "Redis / Vector DB / LLM Foundation / RAG 的正文深度也已完成全量 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。",
)
add_after(
    ROOT / "roadmap" / "knowledge-map.md",
    "章节数不追求统一。审计记录：[`curriculum-granularity-audit.md`](curriculum-granularity-audit.md)。",
    "内容深度验收：[`content-depth-audit.md`](content-depth-audit.md)；Redis / Vector DB / LLM Foundation / RAG 均已通过。",
)
add_after(
    ROOT / "research" / "questions" / "progress.md",
    "详细规则：`../../roadmap/curriculum-granularity-audit.md`。",
    "内容深度验收：`../../roadmap/content-depth-audit.md`。Redis / Vector DB / LLM Foundation / RAG 已完成全量 QA 与人工复核并通过。",
)
add_after(
    ROOT / "research" / "questions" / "module-index.md",
    "> **Canonical 数量不等于教材章节数。** Canonical 是可独立追问能力；教材文件按完整知识小板块组织。",
    "> **教材深度已独立验收。** Redis / Vector DB / LLM Foundation / RAG 的结果见 `../../roadmap/content-depth-audit.md`，不会以文件数量或字数替代人工质量判断。",
)
add_after(
    ROOT / "research" / "questions" / "README.md",
    "因此 **44 道 Agent Canonical 不等于 44 章，29 道 RAG Canonical 也不等于 29 章。**",
    "当前 Redis / Vector DB / LLM Foundation / RAG 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。",
)

# Validate local Markdown links inside the four audited modules.
link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+\.md(?:#[^)]+)?)\)")
violations = []
for module in MODULE_COUNTS:
    base = ROOT / module
    for path in base.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(text):
            target = unquote(raw_target.split("#", 1)[0]).strip()
            if not target or target.startswith(("http://", "https://")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                violations.append(f"{path}: link escapes repo: {raw_target}")
                continue
            if not resolved.exists():
                violations.append(f"{path}: broken local link: {raw_target}")

# Final stale-reference and stale-wording checks.
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for old in RENAMES:
        if old in text:
            violations.append(f"{path}: stale reference {old}")

for module in MODULE_COUNTS:
    for path in (ROOT / module).rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "文件名保留了部分历史编号" in text or "文件保留合并后最早历史编号" in text:
            violations.append(f"{path}: stale historical-number wording")

if violations:
    raise SystemExit("\n".join(violations))

print("Curriculum numbering, links, status wording and depth-audit references validated successfully.")
