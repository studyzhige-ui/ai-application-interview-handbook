#!/usr/bin/env python3
"""Build reproducible Phase 2B market-analysis views from the frozen HUMAN-A corpus.

This script deliberately treats repository files as the source of truth:
- interview/canonical/*.md: canonical questions and evidence mapping
- market/interviews/batch-*.md: source metadata

It never adds external evidence and never changes Source Count based on web/search popularity.
"""

from __future__ import annotations

import csv
import itertools
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_DIR = ROOT / "interview" / "canonical"
INTERVIEWS_DIR = ROOT / "market" / "interviews"
ANALYSIS_DIR = ROOT / "market" / "analysis"

MODULE_FILES = [
    ("Python", "python.md"),
    ("FastAPI", "fastapi.md"),
    ("AI Backend Engineering", "ai-backend-engineering.md"),
    ("MySQL", "mysql.md"),
    ("Redis", "redis.md"),
    ("Vector DB", "vector-db.md"),
    ("LLM Foundation（应用工程深度）", "llm-foundation.md"),
    ("RAG", "rag.md"),
    ("Agent Harness / Runtime", "agent-harness.md"),
    ("System Design", "system-design.md"),
]
MODULE_ORDER = {name: i for i, (name, _) in enumerate(MODULE_FILES)}
EXPECTED_QUESTIONS = 235
EXPECTED_SOURCE_IDS = {f"S{i:03d}" for i in range(1, 280)}

QUESTION_RE = re.compile(
    r"^###\s+(?P<qid>(?:PY|FASTAPI|AIBE|MYSQL|REDIS|VDB|LLM|RAG|AGENT|SD)-\d{3})\s+·\s+(?P<question>.+?)\s*$",
    re.M,
)
SOURCE_HEADING_RE = re.compile(r"^##\s+(S\d{3})\s+(.+?)\s*$", re.M)


@dataclass(frozen=True)
class Question:
    qid: str
    module: str
    question: str
    topic: str
    question_type: str
    depth: str
    source_count: int
    evidence: tuple[str, ...]
    related_modules: str
    language: str


@dataclass(frozen=True)
class Source:
    source_id: str
    company_raw: str
    company_group: str
    role_raw: str
    role_primary: str
    role_tags: tuple[str, ...]
    round_raw: str
    round_tags: tuple[str, ...]
    heading: str
    batch_file: str


def field(block: str, name: str) -> str:
    m = re.search(rf"^- \*\*{re.escape(name)}\*\*：(.+?)\s*$", block, re.M)
    return m.group(1).strip() if m else ""


def parse_questions() -> list[Question]:
    questions: list[Question] = []
    seen_qids: set[str] = set()

    for module, filename in MODULE_FILES:
        text = (QUESTIONS_DIR / filename).read_text(encoding="utf-8")
        matches = list(QUESTION_RE.finditer(text))
        for i, m in enumerate(matches):
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = text[start:end]
            qid = m.group("qid")
            if qid in seen_qids:
                raise ValueError(f"duplicate QID: {qid}")
            seen_qids.add(qid)

            source_count_text = field(block, "Source Count")
            if not source_count_text:
                raise ValueError(f"missing Source Count: {qid}")
            source_count_match = re.search(r"\d+", source_count_text)
            if not source_count_match:
                raise ValueError(f"invalid Source Count: {qid}: {source_count_text}")
            source_count = int(source_count_match.group())

            evidence_line = field(block, "Evidence Sources")
            evidence = tuple(dict.fromkeys(re.findall(r"S\d{3}", evidence_line)))
            if source_count != len(evidence):
                raise ValueError(
                    f"Source Count mismatch {qid}: declared={source_count}, evidence={len(evidence)} {evidence}"
                )

            questions.append(
                Question(
                    qid=qid,
                    module=module,
                    question=m.group("question").strip(),
                    topic=field(block, "Topic"),
                    question_type=field(block, "Question Type"),
                    depth=field(block, "Depth"),
                    source_count=source_count,
                    evidence=evidence,
                    related_modules=field(block, "Related Modules"),
                    language=field(block, "Language / Ecosystem"),
                )
            )

    if len(questions) != EXPECTED_QUESTIONS:
        raise ValueError(f"expected {EXPECTED_QUESTIONS} active questions, parsed {len(questions)}")
    return questions


def normalize_company(raw: str) -> str:
    s = raw.strip()
    rules = [
        (("字节", "抖音"), "字节跳动"),
        (("蚂蚁",), "蚂蚁集团"),
        (("阿里", "淘天", "高德", "优酷", "千问"), "阿里巴巴"),
        (("腾讯",), "腾讯"),
        (("美团",), "美团"),
        (("快手",), "快手"),
        (("小红书",), "小红书"),
        (("百度",), "百度"),
        (("拼多多", "PDD"), "拼多多"),
        (("京东",), "京东"),
        (("滴滴",), "滴滴"),
        (("Bilibili", "哔哩", "bilibili"), "哔哩哔哩"),
        (("OPPO", "Oppo"), "OPPO"),
        (("vivo", "VIVO"), "vivo"),
        (("小米",), "小米"),
        (("Shopee", "虾皮"), "Shopee"),
        (("MiniMax",), "MiniMax"),
        (("大疆",), "大疆"),
        (("携程",), "携程"),
        (("网易",), "网易"),
        (("九号",), "九号公司"),
        (("米哈游",), "米哈游"),
        (("深信服",), "深信服"),
        (("平安",), "平安"),
        (("大麦",), "大麦"),
        (("去哪儿",), "去哪儿"),
        (("同程",), "同程"),
        (("得物",), "得物"),
        (("华为",), "华为"),
    ]
    for keys, group in rules:
        if any(k in s for k in keys):
            return group
    # Keep long-tail labels rather than collapsing them into an opaque "other" bucket.
    return s


def normalize_role(raw: str) -> tuple[str, tuple[str, ...]]:
    s = raw.strip()
    low = s.lower()
    tags: list[str] = []

    def add(tag: str, *keys: str) -> None:
        if any(k.lower() in low for k in keys):
            tags.append(tag)

    add("Coding Agent / Agent Infra", "coding agent", "agent infra", "harness", "runtime", "agent 平台", "智能体平台", "平台研发")
    add("AI Backend", "ai backend", "agent backend", "ai 后端", "后端 ai", "后端ai", "应用服务端", "服务端")
    add("AI Full-stack", "ai 全栈", "ai full-stack", "ai fullstack", "全栈")
    add("Agent Development", "agent", "智能体")
    add("RAG / Knowledge", "rag", "知识库", "knowledge")
    add("LLM Application", "大模型", "llm")
    add("AI Application", "ai 应用", "ai应用", "ai application", "应用开发", "应用研发")
    add("FDE / Applied AI", "fde", "applied ai")

    tags = list(dict.fromkeys(tags))
    priority = [
        "Coding Agent / Agent Infra",
        "AI Backend",
        "AI Full-stack",
        "Agent Development",
        "RAG / Knowledge",
        "LLM Application",
        "AI Application",
        "FDE / Applied AI",
    ]
    primary = next((p for p in priority if p in tags), "Other AI Engineering")
    return primary, tuple(tags or ["Other AI Engineering"])


def normalize_round_tags(text: str) -> tuple[str, ...]:
    tags: list[str] = []
    checks = [
        ("R1 / 一面", ("一面", "初面", "1面")),
        ("R2 / 二面", ("二面", "2面")),
        ("R3 / 三面", ("三面", "3面")),
        ("R4+ / 四面及以上", ("四面", "4面", "五面", "5面")),
        ("Leader / 主管 / 交叉", ("Leader", "leader", "主管", "交叉面", "业务交叉")),
        ("HR", ("HR", "hr")),
        ("AI Coding / Vibe Coding", ("AI Coding", "ai coding", "Vibe Coding", "vibe coding", "在线笔试")),
        ("Technical / 未编号技术面", ("技术面", "技术轮")),
    ]
    for tag, keys in checks:
        if any(k in text for k in keys):
            tags.append(tag)
    return tuple(tags or ["Unspecified"])


def parse_sources() -> dict[str, Source]:
    sources: dict[str, Source] = {}
    for batch in sorted(INTERVIEWS_DIR.glob("batch-*.md")):
        text = batch.read_text(encoding="utf-8")
        for m in SOURCE_HEADING_RE.finditer(text):
            source_id, payload = m.group(1), m.group(2).strip()
            # Phase 2B analysis is intentionally frozen to S001–S279.
            # Newer HUMAN-A sources may coexist in market/interviews while awaiting periodic Canonical mapping.
            if source_id not in EXPECTED_SOURCE_IDS:
                continue
            parts = [p.strip() for p in payload.split("｜")]
            company_raw = parts[0] if parts else ""
            role_raw = parts[1] if len(parts) >= 2 else ""
            round_raw = parts[2] if len(parts) >= 3 else ""
            role_primary, role_tags = normalize_role(role_raw)
            source = Source(
                source_id=source_id,
                company_raw=company_raw,
                company_group=normalize_company(company_raw),
                role_raw=role_raw,
                role_primary=role_primary,
                role_tags=role_tags,
                round_raw=round_raw,
                round_tags=normalize_round_tags(payload),
                heading=f"{source_id} {payload}",
                batch_file=batch.name,
            )
            if source_id in sources:
                raise ValueError(
                    f"duplicate source heading {source_id}: {sources[source_id].heading!r} vs {source.heading!r}"
                )
            sources[source_id] = source

    ids = set(sources)
    missing = sorted(EXPECTED_SOURCE_IDS - ids)
    if missing:
        raise ValueError(f"frozen source baseline mismatch: missing={missing}")
    return sources


def heat(count: int) -> str:
    if count >= 10:
        return "🔥🔥🔥"
    if count >= 4:
        return "🔥🔥"
    if count >= 2:
        return "🔥"
    return "单点真实信号"


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def build() -> None:
    questions = parse_questions()
    sources = parse_sources()
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

    # Validate all evidence IDs are in the frozen source baseline.
    unknown_evidence = sorted({sid for q in questions for sid in q.evidence if sid not in sources})
    if unknown_evidence:
        raise ValueError(f"unknown evidence source IDs: {unknown_evidence}")

    questions_sorted = sorted(
        questions,
        key=lambda q: (MODULE_ORDER[q.module], q.qid),
    )
    frequency_sorted = sorted(
        questions,
        key=lambda q: (-q.source_count, MODULE_ORDER[q.module], q.qid),
    )

    source_to_questions: dict[str, list[Question]] = defaultdict(list)
    for q in questions:
        for sid in q.evidence:
            source_to_questions[sid].append(q)

    canonical_covered_sources = {sid for sid, qs in source_to_questions.items() if qs}
    uncovered_sources = sorted(EXPECTED_SOURCE_IDS - canonical_covered_sources)

    # Machine-readable source metadata.
    source_rows = []
    for sid in sorted(sources):
        s = sources[sid]
        source_rows.append(
            {
                "source_id": sid,
                "company_raw": s.company_raw,
                "company_group": s.company_group,
                "role_raw": s.role_raw,
                "role_primary": s.role_primary,
                "role_tags": "; ".join(s.role_tags),
                "round_raw": s.round_raw,
                "round_tags": "; ".join(s.round_tags),
                "batch_file": s.batch_file,
                "canonical_question_count": len(source_to_questions.get(sid, [])),
            }
        )
    write_csv(
        ANALYSIS_DIR / "source-metadata.csv",
        source_rows,
        [
            "source_id",
            "company_raw",
            "company_group",
            "role_raw",
            "role_primary",
            "role_tags",
            "round_raw",
            "round_tags",
            "batch_file",
            "canonical_question_count",
        ],
    )

    # Global question index: CSV + Markdown.
    question_rows = []
    for q in questions_sorted:
        question_rows.append(
            {
                "qid": q.qid,
                "module": q.module,
                "topic": q.topic,
                "depth": q.depth,
                "source_count": q.source_count,
                "interview_heat": heat(q.source_count),
                "question_type": q.question_type,
                "related_modules": q.related_modules,
                "question": q.question,
                "evidence_sources": ";".join(q.evidence),
            }
        )
    write_csv(
        ANALYSIS_DIR / "global-question-index.csv",
        question_rows,
        [
            "qid",
            "module",
            "topic",
            "depth",
            "source_count",
            "interview_heat",
            "question_type",
            "related_modules",
            "question",
            "evidence_sources",
        ],
    )

    lines = [
        "# Global Canonical Question Index",
        "",
        "更新日期：2026-09-11",
        "",
        "> 自动从十个正式 Canonical 文件生成；统计范围为 Frozen Canonical Baseline `S001–S279 / 235 ACTIVE`。本文件不创建新证据，只提供全局可排序视图。",
        "",
        "| QID | Module | Topic | Depth | Sources | Heat | Canonical Question |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for q in questions_sorted:
        lines.append(
            f"| `{q.qid}` | {md_escape(q.module)} | {md_escape(q.topic)} | {q.depth} | {q.source_count} | {heat(q.source_count)} | {md_escape(q.question)} |"
        )
    (ANALYSIS_DIR / "global-question-index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Frequency ranking.
    tier_counter = Counter(heat(q.source_count) for q in questions)
    freq_lines = [
        "# Canonical Question Frequency Ranking",
        "",
        "更新日期：2026-09-11",
        "",
        "> `Source Count` = 独立 HUMAN-A 招聘流程数，不是关键词出现次数。频率只表示真实面试信号，不等于课程知识重要度。",
        "",
        "## Heat 分布",
        "",
        f"- 🔥🔥🔥（>=10）：**{tier_counter['🔥🔥🔥']}**",
        f"- 🔥🔥（4–9）：**{tier_counter['🔥🔥']}**",
        f"- 🔥（2–3）：**{tier_counter['🔥']}**",
        f"- 单点真实信号（1）：**{tier_counter['单点真实信号']}**",
        "",
        "## 全量排名",
        "",
        "| Rank | QID | Module | Sources | Depth | Heat | Question |",
        "|---:|---|---|---:|---:|---|---|",
    ]
    for rank, q in enumerate(frequency_sorted, 1):
        freq_lines.append(
            f"| {rank} | `{q.qid}` | {md_escape(q.module)} | {q.source_count} | {q.depth} | {heat(q.source_count)} | {md_escape(q.question)} |"
        )
    (ANALYSIS_DIR / "frequency-ranking.md").write_text("\n".join(freq_lines) + "\n", encoding="utf-8")

    # Module-level evidence metrics.
    module_rows = []
    for module, _ in MODULE_FILES:
        qs = [q for q in questions if q.module == module]
        union_sources = {sid for q in qs for sid in q.evidence}
        counts = [q.source_count for q in qs]
        module_rows.append(
            {
                "module": module,
                "canonical_questions": len(qs),
                "unique_sources": len(union_sources),
                "source_question_incidences": sum(counts),
                "mean_sources_per_question": round(statistics.mean(counts), 2) if counts else 0,
                "median_sources_per_question": statistics.median(counts) if counts else 0,
                "triple_heat_questions": sum(c >= 10 for c in counts),
                "l4_questions": sum(q.depth == "L4" for q in qs),
            }
        )
    write_csv(
        ANALYSIS_DIR / "module-metrics.csv",
        module_rows,
        list(module_rows[0].keys()),
    )

    # Coverage distributions from frozen source headings.
    company_counter = Counter(s.company_group for s in sources.values())
    company_raw_counter = Counter(s.company_raw for s in sources.values())
    role_primary_counter = Counter(s.role_primary for s in sources.values())
    role_tag_counter = Counter(tag for s in sources.values() for tag in s.role_tags)
    round_counter = Counter(tag for s in sources.values() for tag in s.round_tags)

    # Per-company/module source-flow matrix.
    company_module: dict[str, Counter[str]] = defaultdict(Counter)
    role_module: dict[str, Counter[str]] = defaultdict(Counter)
    round_module: dict[str, Counter[str]] = defaultdict(Counter)
    for sid, qs in source_to_questions.items():
        s = sources[sid]
        modules = {q.module for q in qs}
        for module in modules:
            company_module[s.company_group][module] += 1
            role_module[s.role_primary][module] += 1
            for rt in s.round_tags:
                round_module[rt][module] += 1

    coverage_lines = [
        "# Market Coverage — Company / Role / Round",
        "",
        "更新日期：2026-09-11",
        "",
        "> 本文件只统计冻结 `S001–S279` 的来源标题元数据。`Sxxx` 已在采集层把同一候选人同一公司同一招聘流程的多轮合并，因此公司 / 岗位的基本单位仍是独立招聘流程。Round tag 是一个流程是否包含该轮次，允许一条多轮流程同时命中多个 Round tag。",
        "",
        "## 总覆盖",
        "",
        f"- 正式 HUMAN-A 来源：**{len(sources)}**",
        f"- 至少映射到 1 道 Canonical 的来源：**{len(canonical_covered_sources)}**",
        f"- 未映射到 Canonical 的来源：**{len(uncovered_sources)}**",
        f"- 规范化公司 / 组织标签：**{len(company_counter)}**",
        f"- 原始公司标题标签：**{len(company_raw_counter)}**",
        "",
        "## Company Group 覆盖",
        "",
        "| Company Group | Source Flows |",
        "|---|---:|",
    ]
    for company, count in company_counter.most_common():
        coverage_lines.append(f"| {md_escape(company)} | {count} |")

    coverage_lines += [
        "",
        "## Primary Role 覆盖",
        "",
        "> Role Primary 是按来源标题做的确定性归一化；`role_raw` 永久保留在 `source-metadata.csv`，避免关键词归类覆盖原始岗位语义。",
        "",
        "| Primary Role | Source Flows |",
        "|---|---:|",
    ]
    for role, count in role_primary_counter.most_common():
        coverage_lines.append(f"| {md_escape(role)} | {count} |")

    coverage_lines += [
        "",
        "## Role Tag 覆盖（非互斥）",
        "",
        "| Role Tag | Source Flows |",
        "|---|---:|",
    ]
    for role, count in role_tag_counter.most_common():
        coverage_lines.append(f"| {md_escape(role)} | {count} |")

    coverage_lines += [
        "",
        "## Round / Stage 覆盖（非互斥）",
        "",
        "| Round Tag | Source Flows containing tag |",
        "|---|---:|",
    ]
    for rt, count in round_counter.most_common():
        coverage_lines.append(f"| {md_escape(rt)} | {count} |")

    top_companies = [c for c, _ in company_counter.most_common(15)]
    coverage_lines += [
        "",
        "## Top Company × Module：出现过该模块问题的独立流程数",
        "",
        "| Company | " + " | ".join(m for m, _ in MODULE_FILES) + " |",
        "|---|" + "---:|" * len(MODULE_FILES),
    ]
    for company in top_companies:
        coverage_lines.append(
            "| "
            + md_escape(company)
            + " | "
            + " | ".join(str(company_module[company][m]) for m, _ in MODULE_FILES)
            + " |"
        )

    coverage_lines += [
        "",
        "## Primary Role × Module：出现过该模块问题的独立流程数",
        "",
        "| Role | " + " | ".join(m for m, _ in MODULE_FILES) + " |",
        "|---|" + "---:|" * len(MODULE_FILES),
    ]
    for role, _ in role_primary_counter.most_common():
        coverage_lines.append(
            "| "
            + md_escape(role)
            + " | "
            + " | ".join(str(role_module[role][m]) for m, _ in MODULE_FILES)
            + " |"
        )

    if uncovered_sources:
        coverage_lines += ["", "## 未映射来源", "", ", ".join(f"`{s}`" for s in uncovered_sources)]

    (ANALYSIS_DIR / "market-coverage.md").write_text("\n".join(coverage_lines) + "\n", encoding="utf-8")

    # Depth and type distributions.
    depth_questions = Counter(q.depth for q in questions)
    depth_weighted = Counter()
    type_questions = Counter()
    type_weighted = Counter()
    for q in questions:
        depth_weighted[q.depth] += q.source_count
        tokens = [x.strip() for x in q.question_type.split("/") if x.strip()]
        for token in tokens:
            type_questions[token] += 1
            type_weighted[token] += q.source_count

    depth_lines = [
        "# Interview Depth & Question Type Analysis",
        "",
        "更新日期：2026-09-11",
        "",
        "> `Canonical Questions` 看问题模型数量；`Evidence Incidences` 把每道题按独立 HUMAN-A Source Count 加权。两种口径都不等同于课程知识重要度。",
        "",
        "## Depth",
        "",
        "| Depth | Canonical Questions | Evidence Incidences |",
        "|---|---:|---:|",
    ]
    for d in ("L1", "L2", "L3", "L4"):
        depth_lines.append(f"| {d} | {depth_questions[d]} | {depth_weighted[d]} |")

    depth_lines += [
        "",
        "## Question Type token",
        "",
        "| Type | Canonical Questions | Evidence Incidences |",
        "|---|---:|---:|",
    ]
    for t, n in type_questions.most_common():
        depth_lines.append(f"| {md_escape(t)} | {n} | {type_weighted[t]} |")

    depth_lines += [
        "",
        "## Module × Depth",
        "",
        "| Module | L1 | L2 | L3 | L4 |",
        "|---|---:|---:|---:|---:|",
    ]
    for module, _ in MODULE_FILES:
        c = Counter(q.depth for q in questions if q.module == module)
        depth_lines.append(f"| {md_escape(module)} | {c['L1']} | {c['L2']} | {c['L3']} | {c['L4']} |")
    (ANALYSIS_DIR / "depth-and-types.md").write_text("\n".join(depth_lines) + "\n", encoding="utf-8")

    # Topic-level market-evidence matrix for curriculum calibration.
    topic_stats: dict[tuple[str, str], dict[str, object]] = {}
    for q in questions:
        key = (q.module, q.topic)
        stat = topic_stats.setdefault(
            key,
            {"questions": [], "sources": set(), "max_count": 0, "incidences": 0, "max_depth": "L1"},
        )
        stat["questions"].append(q.qid)
        stat["sources"].update(q.evidence)
        stat["max_count"] = max(int(stat["max_count"]), q.source_count)
        stat["incidences"] = int(stat["incidences"]) + q.source_count
        if q.depth > str(stat["max_depth"]):
            stat["max_depth"] = q.depth

    matrix_lines = [
        "# Curriculum Evidence Matrix",
        "",
        "更新日期：2026-09-11",
        "",
        "> 这是**市场证据矩阵**，不是最终课程目录。它回答“真实面试在哪些 Topic 上反复出现、最高追到多深”；完整知识体系仍可加入没有高频面经证据但属于必要前置的章节。",
        "",
    ]
    for module, _ in MODULE_FILES:
        matrix_lines += [f"## {module}", "", "| Topic | Canonical | Unique Sources | Max Q Frequency | Max Depth | QIDs |", "|---|---:|---:|---:|---:|---|"]
        rows = []
        for (m, topic), stat in topic_stats.items():
            if m != module:
                continue
            rows.append((topic, stat))
        rows.sort(key=lambda x: (-len(x[1]["sources"]), -int(x[1]["max_count"]), x[0]))
        for topic, stat in rows:
            matrix_lines.append(
                f"| {md_escape(topic)} | {len(stat['questions'])} | {len(stat['sources'])} | {stat['max_count']} | {stat['max_depth']} | {', '.join(f'`{q}`' for q in stat['questions'])} |"
            )
        matrix_lines.append("")
    (ANALYSIS_DIR / "curriculum-evidence-matrix.md").write_text("\n".join(matrix_lines) + "\n", encoding="utf-8")

    # Co-occurrence across independent source flows. This is NOT an ordered follow-up chain.
    pair_counter: Counter[tuple[str, str]] = Counter()
    module_pair_counter: Counter[tuple[str, str]] = Counter()
    q_lookup = {q.qid: q for q in questions}
    for sid, qs in source_to_questions.items():
        qids = sorted({q.qid for q in qs})
        for a, b in itertools.combinations(qids, 2):
            pair_counter[(a, b)] += 1
        modules = sorted({q.module for q in qs}, key=lambda x: MODULE_ORDER[x])
        for a, b in itertools.combinations(modules, 2):
            module_pair_counter[(a, b)] += 1

    co_lines = [
        "# Canonical Co-occurrence Analysis",
        "",
        "更新日期：2026-09-11",
        "",
        "> 共现 = 两道 Canonical 出现在同一个独立 HUMAN-A 招聘流程中。它能帮助发现常见追问组合，但**没有顺序信息**，不能直接宣称为面试官的固定 Follow-up Chain。真正追问链需要回到原始 Batch 人工核验。",
        "",
        "## Module pair co-occurrence",
        "",
        "| Module A | Module B | Shared Source Flows |",
        "|---|---|---:|",
    ]
    for (a, b), n in module_pair_counter.most_common():
        co_lines.append(f"| {md_escape(a)} | {md_escape(b)} | {n} |")

    co_lines += [
        "",
        "## Top Canonical pairs",
        "",
        "| QID A | QID B | Shared Sources | Pair |",
        "|---|---|---:|---|",
    ]
    shown = 0
    for (a, b), n in pair_counter.most_common():
        if n < 3 or shown >= 120:
            break
        qa, qb = q_lookup[a], q_lookup[b]
        co_lines.append(
            f"| `{a}` | `{b}` | {n} | {md_escape(qa.topic)} ↔ {md_escape(qb.topic)} |"
        )
        shown += 1
    (ANALYSIS_DIR / "cooccurrence.md").write_text("\n".join(co_lines) + "\n", encoding="utf-8")

    # Validation report.
    validation_lines = [
        "# Phase 2B Data Validation",
        "",
        "更新日期：2026-09-11",
        "",
        "| Check | Result |",
        "|---|---|",
        f"| ACTIVE Canonical parsed | ✅ {len(questions)} / expected {EXPECTED_QUESTIONS} |",
        f"| Frozen HUMAN-A source IDs parsed | ✅ {len(sources)} / expected 279 |",
        "| Duplicate QID | ✅ none |",
        "| Duplicate Sxxx heading | ✅ none |",
        "| Source Count == unique Evidence Sources | ✅ all questions passed |",
        "| Evidence Source outside S001–S279 | ✅ none |",
        f"| Canonical-covered source flows | {len(canonical_covered_sources)} / 279 |",
        f"| Uncovered source flows | {len(uncovered_sources)} |",
        "",
        "The builder exits non-zero before writing final analysis if any hard consistency check fails.",
    ]
    if uncovered_sources:
        validation_lines += ["", "Uncovered: " + ", ".join(f"`{sid}`" for sid in uncovered_sources)]
    (ANALYSIS_DIR / "validation.md").write_text("\n".join(validation_lines) + "\n", encoding="utf-8")

    # Concise summary generated only from repository-derived statistics.
    top20 = frequency_sorted[:20]
    summary_lines = [
        "# Market Analysis｜Frozen Canonical Baseline",
        "",
        "[← Market 首页](../README.md) · [↑ Handbook 总目录](../../README.md) · [Canonical Questions →](../../interview/canonical/README.md)",
        "",
        "> **数据范围：Frozen Canonical Baseline。** 本页只统计 `S001–S279 / 235 ACTIVE Canonical`；Market 的持续监测总量与 `S280+` 状态以 `market/README.md` 为准。",
        "",
        "统计快照日期：2026-09-11",
        "",
        "## Frozen Baseline",
        "",
        f"- HUMAN-A：**{len(sources)}**",
        f"- ACTIVE Canonical：**{len(questions)}**",
        f"- 至少进入一个 Canonical 的来源：**{len(canonical_covered_sources)}**",
        f"- 三星高频题（>=10 sources）：**{tier_counter['🔥🔥🔥']}**",
        f"- L4 Production / Failure / System Design Canonical：**{sum(q.depth == 'L4' for q in questions)}**",
        "",
        "## Top 20 真人面试信号",
        "",
        "| Rank | QID | Module | Sources | Topic |",
        "|---:|---|---|---:|---|",
    ]
    for i, q in enumerate(top20, 1):
        summary_lines.append(f"| {i} | `{q.qid}` | {md_escape(q.module)} | {q.source_count} | {md_escape(q.topic)} |")

    summary_lines += [
        "",
        "## Module evidence footprint",
        "",
        "| Module | Canonical | Unique Sources | Source×Question Incidences | >=10 Qs | L4 Qs |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in module_rows:
        summary_lines.append(
            f"| {md_escape(str(row['module']))} | {row['canonical_questions']} | {row['unique_sources']} | {row['source_question_incidences']} | {row['triple_heat_questions']} | {row['l4_questions']} |"
        )
    summary_lines += [
        "",
        "当前 Curriculum 范围与阅读顺序以 `guide/navigation-index.md` 为准，验证边界见 `guide/audits/final-quality-audit.md`；`interview/canonical/progress.md` 只记录冻结审核覆盖；当前 Gap 见 `market/analysis/knowledge-gap-analysis.md`，Phase 2B 历史 Gap 见 `market/analysis/history/`。本自动生成 README 不重复维护易过期的 Market 总量或课程下一步。",
    ]
    (ANALYSIS_DIR / "README.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
