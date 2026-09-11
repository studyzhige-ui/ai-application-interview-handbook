from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if old not in text:
        raise SystemExit(f'missing anchor in {path}: {old[:120]!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

# Root README: Python is now also part of depth audit.
replace(
    'README.md',
    'Redis / Vector DB / LLM Foundation / RAG / System Design 的正文深度已完成 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。',
    'Python / Redis / Vector DB / LLM Foundation / RAG / System Design 的正文深度已完成 QA 与人工复核，记录见 [`roadmap/content-depth-audit.md`](roadmap/content-depth-audit.md)。',
)
replace(
    'README.md',
    'Foundation 的真实完成度与 Python v1 质量核实见 [`roadmap/foundation-status-audit.md`](roadmap/foundation-status-audit.md)。Python v1 定向整改已完成；Foundation 接下来的仓库补齐顺序是：**FastAPI → AI Backend Engineering**。',
    'Foundation 的真实完成度见 [`roadmap/foundation-status-audit.md`](roadmap/foundation-status-audit.md)。Python current-standard remediation 已完成；Foundation 剩余缺口只有：**FastAPI → AI Backend Engineering**。',
)

# Progress stale wording.
replace(
    'research/questions/progress.md',
    '内容深度验收：`../../roadmap/content-depth-audit.md`。Redis / Vector DB / LLM Foundation / RAG / System Design 已完成 QA 与人工复核并通过。\nFoundation 完成度核实：`../../roadmap/foundation-status-audit.md`。FastAPI / AI Backend Engineering 当前只有课程骨架；Python 是可用 v1，但需最新 Canonical / 当前统一深度标准的定向整改。',
    '内容深度验收：`../../roadmap/content-depth-audit.md`。Python / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成 QA 与人工复核并通过。\nFoundation 完成度核实：`../../roadmap/foundation-status-audit.md`。Python current-standard remediation 已完成；FastAPI / AI Backend Engineering 当前仍只有课程骨架。',
)
replace(
    'research/questions/progress.md',
    '```text\nMySQL          23 → 23  PASS',
    '```text\nPython         12 → 13  COMPLETE\nMySQL          23 → 23  PASS',
)

# Module index stale sentence.
replace(
    'research/questions/module-index.md',
    'Python 已有可用 v1 教材但需当前标准定向整改；FastAPI / AI Backend Engineering 当前只有 README 课程骨架，正式正文尚未撰写。',
    'Python 已完成 13-block current-standard Canonical Coverage / Depth Remediation；FastAPI / AI Backend Engineering 当前仍只有 README 课程骨架，正式正文尚未撰写。',
)

# Canonical README stale sentence and depth list.
replace(
    'research/questions/README.md',
    '当前 Redis / Vector DB / LLM Foundation / RAG / System Design 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。',
    '当前 Python / Redis / Vector DB / LLM Foundation / RAG / System Design 已完成独立内容深度验收；详见 `../../roadmap/content-depth-audit.md`。',
)
replace(
    'research/questions/README.md',
    '当前教材结构：\n\n```text\nMySQL ✅ 23 blocks',
    '当前教材结构：\n\n```text\nPython ✅ 13 blocks（12→13；15 Canonical Coverage / Depth PASS）\nMySQL ✅ 23 blocks',
)
replace(
    'research/questions/README.md',
    'Python 已有完整可用 v1，但需最新 Canonical / 当前深度标准定向整改；FastAPI / AI Backend Engineering 目前只有 README 课程骨架，正式正文未写。',
    'Python current-standard remediation 已完成；FastAPI / AI Backend Engineering 目前只有 README 课程骨架，正式正文未写。',
)

# Foundation audit: rewrite Python section from historical pending language to current truth.
p = ROOT / 'roadmap/foundation-status-audit.md'
text = p.read_text(encoding='utf-8')
start = text.index('## 3. Python Foundation')
end = text.index('---\n\n## 4. System Design 完成后的 Foundation 建设顺序', start)
new_section = '''## 3. Python Foundation — ✅ current-standard Remediation 已完成

当前仓库实际结构：

```text
python/
├── README.md
├── docs/       13 个连续知识小板块
├── review/     13 个逐章图解与自测
└── interview/  高频题 / Coding / 易错点 / 速查表
```

Python 原 v1 的 12-block 主干本身合理，因此本轮没有推倒重写，也没有把 15 道 Canonical 机械变成 15 个文件。

### 3.1 保留的 beginner-first 主干

```text
Object Model / Language Choice
→ Containers / Hash / Slicing
→ Mutability / Copy
→ Function / Scope / Closure
→ Pythonic Tools
→ Iterator / Generator
→ Decorator / Context Manager
→ OOP / Protocol
→ Error / File / Import
→ Structured Data / Validation
→ Memory / GC / GIL
→ Thread / Process / Coroutine / asyncio
→ Data Structure / Complexity
```

### 3.2 15 道 Canonical 的实际映射

```text
PY-001  Language Choice                  → 01
PY-002  list / tuple                     → 02
PY-003  dict Hash / collision / delete   → 02
PY-004  Function Parameters              → 04
PY-005  Duck Typing / Protocol           → 08
PY-006  Iterator / Generator             → 06
PY-007  Decorator                        → 07
PY-008  Context Manager                  → 07
PY-009  Slicing Cost                     → 02
PY-010  GIL                              → 11
PY-011  Thread / Process                 → 12
PY-012  asyncio / as_completed / timeout → 12
PY-013  Lock / RLock / Semaphore         → 12
PY-014  Structured Output Validation     → 10（唯一新增独立知识块）
PY-015  Closure                          → 04
```

这体现当前固定原则：**知识体系决定章节；真人面经决定补哪些真实工程深度。**

### 3.3 本轮实质补强

- `01`：新增 Python vs Java / Go 的工程选型与 trade-off；
- `02`：新增 dict Hash / Collision / Equality / Delete Probe Chain / Resize，并补内建序列 Slicing 的 O(k) 时间/空间语义；
- `08`：把 Duck Typing 从一句定义扩展为 Protocol Thinking、`typing.Protocol` vs ABC、可替换性和失败边界；
- `10`：新增 Structured Data / JSON / Schema / Business Validation 完整 trust-boundary 章节；
- `11`：重新整理 CPython 引用计数 / 循环 GC / 逻辑内存泄漏 / GIL / free-threaded 边界；
- `12`：补 `gather` vs `as_completed`、Timeout / Fallback / Cancellation、Lock / RLock / Semaphore、Thread/Process Pool 与 AI I/O 聚合；
- `03–07`：补正文内 GitHub `<details>` 折叠自测；
- Review / Interview / 速查表同步最新 AI Application 追问。

### 3.4 当前验收结论

已经机械验证：

```text
docs   = 01–13 连续
review = 01–13 连续
13/13 正文均有折叠自测
README 正文链接存在
旧 10/11/12 历史路径已删除
临时 remediation checkpoint 已删除
```

并已在 `content-depth-audit.md` 记录人工质量结论。

**结论：Python Foundation = 13 blocks；Canonical Coverage / Depth Remediation = PASS。**

'''
p.write_text(text[:start] + new_section + text[end:], encoding='utf-8')

# Content depth audit: include Python in scope and fix numbering after inserted section.
p = ROOT / 'roadmap/content-depth-audit.md'
text = p.read_text(encoding='utf-8')
text = text.replace(
    '> 本文件记录 Redis / Vector DB / LLM Foundation / RAG 的颗粒度整改后深度验收，以及 System Design 首版完成后的深度验收。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。',
    '> 本文件记录 Python / Redis / Vector DB / LLM Foundation / RAG 的整改后深度验收，以及 System Design 首版完成后的深度验收。目标不是让所有文件达到相同字数，而是确认每个知识小板块都能独立完成学习闭环。',
)
text = text.replace('# Python — ✅ PASS after current-standard remediation', '# 3. Python — ✅ PASS after current-standard remediation', 1)
text = text.replace('# 3. Redis — ✅ PASS', '# 4. Redis — ✅ PASS', 1)
text = text.replace('# 4. Vector DB — ✅ PASS', '# 5. Vector DB — ✅ PASS', 1)
text = text.replace('# 5. LLM Foundation — ✅ PASS after targeted remediation', '# 6. LLM Foundation — ✅ PASS after targeted remediation', 1)
text = text.replace('# 6. RAG — ✅ PASS after targeted remediation', '# 7. RAG — ✅ PASS after targeted remediation', 1)
text = text.replace('# 7. System Design — ✅ PASS', '# 8. System Design — ✅ PASS', 1)
text = text.replace('# 8. 最终验收状态', '# 9. 最终验收状态', 1)
text = text.replace('# 9. 后续规则', '# 10. 后续规则', 1)
p.write_text(text, encoding='utf-8')

print('Python final status cleanup complete.')
