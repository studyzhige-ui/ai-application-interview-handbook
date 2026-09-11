from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    "redis": 24,
    "vector-db": 16,
    "llm-foundation": 14,
    "rag": 14,
}

warnings = []
rows = []

for module, expected_count in MODULES.items():
    docs = ROOT / module / "docs"
    files = sorted(docs.glob("[0-9][0-9]-*.md"))
    if len(files) != expected_count:
        warnings.append(f"{module}: expected {expected_count} docs, got {len(files)}")

    for p in files:
        text = p.read_text(encoding="utf-8")
        size = len(text.encode("utf-8"))
        sections = len(re.findall(r"^##+\s", text, flags=re.MULTILINE))
        details = text.count("<details")
        code_fences = text.count("```") // 2
        has_interview = any(k in text for k in ["面试怎么答", "面试怎么回答", "30 秒回答", "🎯"])
        has_failure = any(k in text for k in ["Failure", "失败", "故障", "风险", "Trade-off", "易错点", "错误"])
        has_self_test = details >= 1 or "自测" in text

        flags = []
        if size < 3500:
            flags.append("very-short")
        if sections < 6:
            flags.append("few-sections")
        if code_fences < 2:
            flags.append("few-diagrams/examples")
        if not has_interview:
            flags.append("no-interview-answer")
        if not has_failure:
            flags.append("no-failure-tradeoff")
        if not has_self_test:
            flags.append("no-self-test")

        rows.append((module, p.name, size, sections, details, code_fences, ",".join(flags) or "OK"))
        if flags:
            warnings.append(f"{module}/{p.name}: {', '.join(flags)}")

print("module\tfile\tbytes\tsections\tdetails\tcode_blocks\tflags")
for row in rows:
    print("\t".join(map(str, row)))

print("\n=== AUDIT WARNINGS ===")
if warnings:
    for w in warnings:
        print(w)
else:
    print("NONE")

print(f"\nTOTAL_DOCS={len(rows)} WARNINGS={len(warnings)}")
