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

# Replace stale references throughout Markdown files.
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    new_text = text
    for old, new in RENAMES.items():
        new_text = new_text.replace(old, new)

    # These statements became false after continuous renumbering.
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

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")

# Normalize H1 numbering to the actual filename number and require continuous filenames.
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

# Final stale-reference checks.
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for old in RENAMES:
        if old in text:
            violations.append(f"{path}: stale reference {old}")
    if path.name == "README.md" and path.parent.name in MODULE_COUNTS:
        if "保留合并后最早" in text or "历史文件编号" in text:
            violations.append(f"{path}: stale historical-number wording")

if violations:
    raise SystemExit("\n".join(violations))

print("Curriculum numbering and local Markdown links validated successfully.")
