#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    ("python", "Python Foundation", 13, "research/questions/python.md", "PY", 15),
    ("fastapi", "FastAPI", 16, "research/questions/fastapi.md", "FASTAPI", 4),
    ("backend-engineering", "AI Backend Engineering", 22, "research/questions/ai-backend-engineering.md", "AIBE", 39),
    ("mysql", "MySQL", 23, "research/questions/mysql.md", "MYSQL", 26),
    ("redis", "Redis", 24, "research/questions/redis.md", "REDIS", 19),
    ("vector-db", "Vector Database", 16, "research/questions/vector-db.md", "VDB", 12),
    ("llm-foundation", "LLM Foundation", 14, "research/questions/llm-foundation.md", "LLM", 23),
    ("rag", "RAG", 14, "research/questions/rag.md", "RAG", 29),
    ("agent-harness", "Agent Harness / Runtime", 23, "research/questions/agent-harness.md", "AGENT", 44),
    ("system-design", "System Design", 19, "research/questions/system-design.md", "SD", 24),
]

CURRENT_STATE_FILES = [
    ROOT / "README.md",
    ROOT / "roadmap/knowledge-map.md",
    ROOT / "roadmap/foundation-status-audit.md",
    ROOT / "roadmap/integration-status.md",
    ROOT / "research/questions/README.md",
    ROOT / "research/questions/progress.md",
    ROOT / "research/questions/module-index.md",
]

REQUIRED_INTERVIEW = ["高频面试题.md", "面试易错点.md", "面试前速查表.md"]

fails: list[str] = []
warnings: list[str] = []
summary: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def md_links(path: Path, text: str):
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = m.group(1).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        yield target


def check_markdown_links() -> None:
    checked = 0
    for path in ROOT.rglob("*.md"):
        # frozen raw interview batches may intentionally contain source URLs / copied markdown fragments;
        # relative repository navigation is what this audit validates.
        text = path.read_text(encoding="utf-8")
        for target in md_links(path, text):
            # Ignore angle-style placeholders and scheme-like pseudo links.
            if target.startswith("<") or "://" in target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"link escapes repository: {path.relative_to(ROOT)} -> {target}")
                continue
            if not resolved.exists():
                fail(f"broken local link: {path.relative_to(ROOT)} -> {target}")
            checked += 1
    summary.append(f"Markdown relative links checked: {checked}")


def check_modules() -> None:
    total_docs = 0
    total_q = 0
    for slug, name, expected_docs, qpath, prefix, expected_q in MODULES:
        module = ROOT / slug
        docs_dir = module / "docs"
        readme = module / "README.md"
        review = module / "review" / "README.md"
        interview = module / "interview"
        for p in (readme, review):
            if not p.exists():
                fail(f"missing required file: {p.relative_to(ROOT)}")
        for fname in REQUIRED_INTERVIEW:
            p = interview / fname
            if not p.exists():
                fail(f"missing interview file: {p.relative_to(ROOT)}")

        docs = sorted(docs_dir.glob("*.md")) if docs_dir.exists() else []
        numbered = []
        for p in docs:
            m = re.match(r"^(\d{2})-", p.name)
            if not m:
                fail(f"non-numbered doc in {slug}/docs: {p.name}")
                continue
            numbered.append((int(m.group(1)), p))
        nums = [n for n, _ in numbered]
        expected_nums = list(range(1, expected_docs + 1))
        if nums != expected_nums:
            fail(f"{slug}: docs numbering/count mismatch: got {nums}, expected {expected_nums}")
        if len(docs) != expected_docs:
            fail(f"{slug}: docs count={len(docs)}, expected={expected_docs}")

        for n, p in numbered:
            text = p.read_text(encoding="utf-8")
            first = next((line.strip() for line in text.splitlines() if line.strip()), "")
            if not re.match(rf"^#\s+0?{n}(?:\.|\s|｜|：)", first):
                fail(f"{p.relative_to(ROOT)}: H1 number does not match filename: {first}")
            if "<details>" not in text or "</details>" not in text:
                warn(f"{p.relative_to(ROOT)}: no collapsed self-test/details found")
            if "面试" not in text and "Interview" not in text:
                warn(f"{p.relative_to(ROOT)}: no explicit interview expression section found")
            if p.stat().st_size < 3500:
                warn(f"{p.relative_to(ROOT)}: short file signal ({p.stat().st_size} bytes), needs manual review")
            # Large subsystem files should normally expose failure/trade-off language; absence is a review signal only.
            if not re.search(r"Failure|Trade[- ]?off|失败|故障|易错|边界", text, re.I):
                warn(f"{p.relative_to(ROOT)}: no obvious Failure/Trade-off/boundary marker")

        qfile = ROOT / qpath
        if not qfile.exists():
            fail(f"missing canonical file: {qpath}")
            actual_q = 0
        else:
            qtext = qfile.read_text(encoding="utf-8")
            actual_q = len(re.findall(rf"^###\s+{re.escape(prefix)}-\d{{3}}\b", qtext, re.M))
            if actual_q != expected_q:
                fail(f"{name}: Canonical count={actual_q}, expected={expected_q}")
        total_docs += len(docs)
        total_q += actual_q
        summary.append(f"{name}: docs {len(docs)}/{expected_docs}, canonical {actual_q}/{expected_q}")

    if total_docs != 184:
        fail(f"total curriculum docs={total_docs}, expected=184")
    if total_q != 235:
        fail(f"total ACTIVE canonical={total_q}, expected=235")
    summary.append(f"TOTAL: curriculum docs={total_docs}, canonical={total_q}")


def check_readme_state() -> None:
    root = (ROOT / "README.md").read_text(encoding="utf-8")
    if "184 个正文知识块" not in root:
        fail("root README missing current 184-block total")
    for slug, name, blocks, _, _, canonical in MODULES:
        if f"]({slug}/README.md)" not in root:
            fail(f"root README missing clickable module link: {name}")
        # Knowledge map must expose module links too.
        km = (ROOT / "roadmap/knowledge-map.md").read_text(encoding="utf-8")
        if f"](../{slug}/README.md)" not in km:
            fail(f"knowledge-map missing clickable module link: {name}")

    stale_patterns = [
        r"正式正文未写",
        r"只有 README 课程骨架",
        r"NOT WRITTEN",
        r"下一模块[:：].*System Design",
        r"Foundation 当前唯一.*缺口",
    ]
    for p in CURRENT_STATE_FILES:
        text = p.read_text(encoding="utf-8")
        for pat in stale_patterns:
            if re.search(pat, text, re.I):
                fail(f"stale current-state wording in {p.relative_to(ROOT)}: /{pat}/")

    # Generated analysis README must be protected at its generator source.
    builder = (ROOT / "tools/build_market_analysis.py").read_text(encoding="utf-8")
    if "Research Analysis｜Phase 2B Market Analysis" not in builder:
        fail("market-analysis generator does not contain current README title")
    if "不重复维护课程状态" not in builder:
        fail("market-analysis generator lacks current stale-state guard wording")


def check_mermaid_signals() -> None:
    # Conservative GitHub Mermaid guardrails: flag historically problematic HTML breaks.
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "```mermaid" not in text:
            continue
        if "<br/>" in text or "<br>" in text:
            warn(f"{path.relative_to(ROOT)}: Mermaid contains <br>; verify GitHub rendering")


def main() -> int:
    check_modules()
    check_markdown_links()
    check_readme_state()
    check_mermaid_signals()

    print("=== FINAL V1 MECHANICAL AUDIT ===")
    for line in summary:
        print("OK  ", line)
    print(f"\nFAILURES: {len(fails)}")
    for x in fails:
        print("FAIL", x)
    print(f"\nWARNINGS: {len(warnings)}")
    for x in warnings:
        print("WARN", x)

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
