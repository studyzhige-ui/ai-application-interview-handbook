from pathlib import Path
import re
import urllib.parse
from collections import defaultdict

ROOT = Path("research")
BDIR = ROOT / "interviews"
batch_files = sorted(BDIR.glob("batch-*.md"))
id_head = re.compile(r"^## S(\d{3})\s+(.+)$", re.M)
any_h2 = re.compile(r"^##\s+.+$", re.M)
urlpat = re.compile(r"https?://[^\s)]+")


def norm_url(u: str) -> str:
    u = u.rstrip(".,;，。；")
    p = urllib.parse.urlsplit(u)
    host = p.netloc.lower()
    if host in {"api-cdn.nowcoder.com", "www.nowcoder.com", "nowcoder.com"}:
        host = "www.nowcoder.com"
    return urllib.parse.urlunsplit((p.scheme.lower(), host, p.path.rstrip("/"), "", ""))


def source_urls(block: str):
    out = []
    for line in block.splitlines():
        if "来源" in line:
            out.extend(u.rstrip(".,;，。；") for u in urlpat.findall(line))
    return out


# Parse all 379 source entries. An entry ends at the next H2 heading of any kind,
# so batch-level observation sections are never accidentally copied into a source.
entries = {}
file_meta = {}
for f in batch_files:
    text = f.read_text(encoding="utf-8")
    date_m = re.search(r"^采集日期：(.+)$", text, re.M)
    file_meta[f] = {
        "date": date_m.group(1).strip() if date_m else "2026-09-10",
        "tails": [],
    }
    h2s = list(any_h2.finditer(text))
    for idx, h in enumerate(h2s):
        line = h.group(0)
        m = re.match(r"^## S(\d{3})\s+(.+)$", line)
        end = h2s[idx + 1].start() if idx + 1 < len(h2s) else len(text)
        block = text[h.start():end].strip()
        block = re.sub(r"\n\s*---\s*$", "", block).rstrip()
        if m:
            sid = int(m.group(1))
            title = m.group(2).strip()
            if sid in entries:
                raise RuntimeError(f"duplicate parsed id S{sid:03d}")
            urls = source_urls(block)
            nurls = [norm_url(u) for u in urls]
            qcount = sum(bool(re.match(r"^\d+\.\s+", ln.strip())) for ln in block.splitlines())
            entries[sid] = {
                "id": sid,
                "title": title,
                "block": block,
                "file": f,
                "urls": urls,
                "nurls": nurls,
                "qcount": qcount,
            }
        else:
            file_meta[f]["tails"].append(block)

ids = sorted(entries)
assert ids == list(range(1, 380)), (ids[:5], ids[-5:], len(ids))

# Build exact-source connected components after URL normalization.
parent = {i: i for i in ids}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra


url_to_ids = defaultdict(list)
for i, e in entries.items():
    for u in set(e["nurls"]):
        url_to_ids[u].append(i)
for group in url_to_ids.values():
    if len(group) > 1:
        g = sorted(group)
        for i in g[1:]:
            union(g[0], i)

comps = defaultdict(list)
for i in ids:
    comps[find(i)].append(i)
dup_comps = [sorted(v) for v in comps.values() if len(v) > 1]
dup_comps.sort(key=lambda v: v[0])
assert len(dup_comps) == 82, len(dup_comps)
assert sum(len(c) - 1 for c in dup_comps) == 99

# Keep the earliest old ID in every exact-source component. If a later duplicate
# is a richer merged-round version, use its fuller body at the earliest canonical ID.
alias = {i: i for i in ids}
replacement = {}
exact_deleted = set()
for c in dup_comps:
    canonical = min(c)
    union_urls = set()
    for i in c:
        union_urls.update(entries[i]["nurls"])
    ranked = sorted(
        c,
        key=lambda i: (
            len(set(entries[i]["nurls"])),
            entries[i]["qcount"],
            len(entries[i]["block"]),
        ),
        reverse=True,
    )
    richest = ranked[0]
    # Safety: in this dataset the richest body covers every URL in its component.
    if set(entries[richest]["nurls"]) != union_urls:
        raise RuntimeError(f"component S{canonical:03d} needs multi-body merge: {c}")
    replacement[canonical] = entries[richest]["block"]
    for i in c:
        alias[i] = canonical
        if i != canonical:
            exact_deleted.add(i)

# One non-URL duplicate confirmed by the semantic audit:
# PDD AI Agent 2026-08-17 first round, same consecutive question sequence.
assert 219 not in exact_deleted and 60 not in exact_deleted
semantic_deleted = {219}
alias[219] = 60

deleted = exact_deleted | semantic_deleted
assert len(deleted) == 100
retained = [i for i in ids if i not in deleted]
assert len(retained) == 279
new_id = {old: n for n, old in enumerate(retained, 1)}


def resolve_old(old):
    seen = set()
    while alias.get(old, old) != old:
        if old in seen:
            raise RuntimeError("alias cycle")
        seen.add(old)
        old = alias[old]
    return old


def current_id(old):
    return new_id.get(resolve_old(old))


def remap_text(text: str) -> str:
    def repl(m):
        old = int(m.group(1))
        cur = current_id(old)
        return f"S{cur:03d}" if cur is not None else m.group(0)

    return re.sub(r"S(\d{3})", repl, text)


# Canonical source blocks.
canonical_block = {}
for old in retained:
    block = replacement.get(old, entries[old]["block"])
    block = re.sub(
        r"^## S\d{3}\s+",
        f"## S{old:03d} ",
        block,
        count=1,
        flags=re.M,
    )
    canonical_block[old] = remap_text(block)

# Rebuild every batch. Canonicals remain in the earliest ID's original batch.
batch_new_ids = {}
for f in batch_files:
    olds = [i for i in retained if entries[i]["file"] == f]
    batch_new_ids[f] = [new_id[i] for i in olds]
    num = re.search(r"batch-(\d+)\.md$", f.name).group(1)
    date = file_meta[f]["date"]
    head = (
        f"# Batch {int(num):02d} — HUMAN-A 真人高质量第一人称面经\n\n"
        f"采集日期：{date}\n\n"
        "> **2026-09-10 全库同场去重 / 重编号版本。** 当前 `Sxxx` 为去重后的正式编号；同一实际面试只保留最早 canonical。若后期重复条目包含更完整复盘或额外轮次，完整内容已合并回最早 canonical 后再删除后期重复编号。\n"
        "> HUMAN-A / Role Scope Gate 不变；同一招聘流程中的不同实际轮次不会仅因属于同一流程而被删除。\n"
        f"> 本批去重后当前保留 **{len(olds)}** 个正式来源。"
    )
    parts = [head]
    parts.extend(canonical_block[old] for old in olds)
    tails = file_meta[f]["tails"]
    if tails:
        parts.append(
            "> 注：以下批次观察 / 排除说明为采集时的过程记录；其中历史数量描述按采集当时口径保留，出现的来源 ID 已映射到当前正式编号。"
        )
        parts.extend(remap_text(t) for t in tails)
    f.write_text(
        "\n\n---\n\n".join(p.strip() for p in parts if p.strip()) + "\n",
        encoding="utf-8",
    )

# Remap source-ID references in every other research Markdown file.
for p in ROOT.rglob("*.md"):
    if p in batch_files:
        continue
    text = p.read_text(encoding="utf-8")
    p.write_text(remap_text(text), encoding="utf-8")

N = len(retained)
NEXT = N + 1
b26 = batch_new_ids[BDIR / "batch-26.md"]
assert len(b26) == 5, b26
b26_range = f"S{min(b26):03d}–S{max(b26):03d}"

# Authoritative README totals and audit note.
rp = ROOT / "README.md"
text = rp.read_text(encoding="utf-8")
text = re.sub(r"正式 HUMAN-A 来源：\*\*\d+ 个\*\*", f"正式 HUMAN-A 来源：**{N} 个**", text)
text = re.sub(r"来源编号：`S001–S\d{3}`", f"来源编号：`S001–S{N:03d}`", text)
text = re.sub(r"当前最大编号：`S\d{3}`", f"当前最大编号：`S{N:03d}`", text)
text = re.sub(
    r"若未来人为重开采集，下一条保留编号：\*\*`S\d{3}`\*\*",
    f"若未来人为重开采集，下一条保留编号：**`S{NEXT:03d}`**",
    text,
)
text = re.sub(
    r"- 最新 / 最终主动搜索 Batch：\[`interviews/batch-26\.md`\]\(interviews/batch-26\.md\)，新增 \*\*\d+ 个 HUMAN-A（S\d{3}–S\d{3}）\*\*",
    f"- 最新 / 最终主动搜索 Batch：[`interviews/batch-26.md`](interviews/batch-26.md)，全库去重后本批保留 **{len(b26)} 个 HUMAN-A（{b26_range}）**",
    text,
)
text = text.replace(
    "最终只放行 6 个独立大厂流程：百度 AI 应用工程师、蚂蚁国际 AI 应用开发、阿里云后端 AI 开发，以及 3 个不同候选人的快手大模型应用 / AI 应用服务端流程。",
    "搜索阶段曾放行 6 个候选流程；全库去重后，阿里云 4/22 后端 AI 开发与更早已收来源为同一场，已并回最早 canonical，因此 Batch 26 最终保留 5 个来源：百度 AI 应用工程师、蚂蚁国际 AI 应用开发，以及 3 个不同候选人的快手大模型应用 / AI 应用服务端流程。",
)
text = re.sub(r"\n---\n\n## 10\. 全库去重审计.*\Z", "", text, flags=re.S)
text += f"""

---

## 10. 全库去重审计（2026-09-10）

本库已对去重前的 **379** 个正式来源完成一次全量同场审计，并统一重排编号。

- 去重前：`S001–S379`，379 个；
- 精确 / 归一化来源 URL 连通组件：**82 组**；
- 同 URL / 同来源组件中删除靠后重复成员：**99 个**；
- 不同 URL 但经公司、日期、轮次和连续题序确认属于同一实际面试：**1 个**（审计前 `S060` / `S219`，保留较早 `S060`）；
- 总删除重复来源：**100 个**；
- 去重后：`S001–S{N:03d}`，共 **{N} 个 HUMAN-A**；
- 若未来人为重开采集，下一编号：`S{NEXT:03d}`。

本次“同场去重”的口径是**同一实际面试**，不是“同一候选人同一公司同一招聘流程”。因此明确的一面、二面、三面只要是不同实际面试，仍保留；已经被历史条目合并为一个来源的多轮流程也继续作为一个来源。对于“早期只记录其中一轮、后期重复条目补全了同一候选人的其它轮次”的 URL 组件，保留最早来源编号，但将后期更完整正文合并回最早 canonical，避免去重造成信息损失。
"""
rp.write_text(text, encoding="utf-8")

# Authoritative Inbox totals and audit note.
ip = ROOT / "monitoring" / "inbox.md"
text = ip.read_text(encoding="utf-8")
text = re.sub(
    r"正式来源：`S001–S\d{3}`，共 \*\*\d+ 个 HUMAN-A\*\*",
    f"正式来源：`S001–S{N:03d}`，共 **{N} 个 HUMAN-A**",
    text,
)
text = re.sub(
    r"最终主动搜索批次：Batch 26（`S\d{3}–S\d{3}`，新增 \d+ 个）",
    f"最终主动搜索批次：Batch 26（全库去重后本批保留 `{b26_range}`，共 {len(b26)} 个）",
    text,
)
text = re.sub(r"当前最大来源编号：`S\d{3}`", f"当前最大来源编号：`S{N:03d}`", text)
text = re.sub(
    r"若未来人为重开采集，下一条保留编号：\*\*`S\d{3}`\*\*",
    f"若未来人为重开采集，下一条保留编号：**`S{NEXT:03d}`**",
    text,
)
text = text.replace(
    "Batch 26 只搜索 2026 年大公司，并显著扩大搜索量；最终新增百度、蚂蚁国际、阿里云以及三个不同候选人的快手独立流程。",
    "Batch 26 只搜索 2026 年大公司，并显著扩大搜索量；搜索阶段曾放行百度、蚂蚁国际、阿里云以及三个不同候选人的快手流程。全库去重后，阿里云 4/22 流程与更早来源同场并回最早 canonical，因此 Batch 26 当前净保留 5 个来源。",
)
if "## 全库去重结果" not in text:
    insert = f"""
## 全库去重结果

- 去重前：379 个来源；
- 删除同一实际面试的重复条目：100 个；
- 去重后：`S001–S{N:03d}`，共 **{N} 个 HUMAN-A**；
- 其中 99 个来自归一化 URL 重复组件，另 1 个为不同 URL 但同公司 / 同日期 / 同轮次 / 连续题序确认同场；
- 不同实际轮次不会因为属于同一招聘流程而被删除；后期更完整的同源复盘已合并回最早 canonical。

"""
    text = text.replace("\n## 收官后规则\n", insert + "## 收官后规则\n")
ip.write_text(text, encoding="utf-8")

# Final full-library validation.
new_entries = []
final_url_to_ids = defaultdict(set)
for f in batch_files:
    t = f.read_text(encoding="utf-8")
    for m in id_head.finditer(t):
        new_entries.append(int(m.group(1)))
    h2s = list(any_h2.finditer(t))
    for idx, h in enumerate(h2s):
        m = re.match(r"^## S(\d{3})\s+", h.group(0))
        if not m:
            continue
        end = h2s[idx + 1].start() if idx + 1 < len(h2s) else len(t)
        block = t[h.start():end]
        sid = int(m.group(1))
        for u in set(norm_url(x) for x in source_urls(block)):
            final_url_to_ids[u].add(sid)

assert sorted(new_entries) == list(range(1, N + 1)), (
    len(new_entries),
    new_entries[:5],
    new_entries[-5:],
)
collisions = {u: sorted(v) for u, v in final_url_to_ids.items() if len(v) > 1}
assert not collisions, list(collisions.items())[:5]

original_urls = set(url_to_ids)
semantic_removed_urls = set(entries[219]["nurls"])
final_urls = set(final_url_to_ids)
assert final_urls == (original_urls - semantic_removed_urls), (
    len(original_urls),
    len(final_urls),
    original_urls - final_urls,
    final_urls - original_urls,
)
all_batches = "\n".join(p.read_text(encoding="utf-8") for p in batch_files)
assert "328260668ec94ebda5c84de205d13a58" not in all_batches

readme = rp.read_text(encoding="utf-8")
inbox = ip.read_text(encoding="utf-8")
assert f"正式 HUMAN-A 来源：**{N} 个**" in readme
assert f"来源编号：`S001–S{N:03d}`" in readme
assert f"正式来源：`S001–S{N:03d}`，共 **{N} 个 HUMAN-A**" in inbox

# Remove all temporary audit machinery from the final main tree.
for p in Path(".github/workflows").glob("dedupe-*.yml"):
    p.unlink()
this_script = Path(".github/scripts/final_dedupe.py")
if this_script.exists():
    this_script.unlink()

print(
    f"VALIDATION_OK old=379 exact_removed={len(exact_deleted)} "
    f"semantic_removed={len(semantic_deleted)} final={N} next=S{NEXT:03d}"
)
print(
    f"BATCH26={b26_range} count={len(b26)}; "
    f"normalized_source_urls={len(final_urls)}; collisions=0"
)
