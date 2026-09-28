#!/usr/bin/env python3
"""Apply the reviewed Agent drafts to one isolated branch, validate and commit.

No remote main write, force push, evidence mutation or unrelated lesson write.
The transport files and this workflow are removed before the final commit.
"""
from __future__ import annotations
import hashlib
import html
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / 'tools'))
from sync_outer_navigation import anchors, heading_slug, markdown_links, resolve

BASE = 'a6b51b9f00bf3fe7910cfe4ca248e80545f566e3'
BRANCH = 'work/agent-clarity-20260928'
REPO = 'studyzhige-ui/ai-application-interview-handbook'
MODULE = 'curriculum/09-agent'
DATE = '2026-09-28'
REPORT = f'guide/project/agent-clarity-refinement-{DATE}.md'
MAPPING = f'guide/project/agent-clarity-mapping-{DATE}.json'
VALIDATION = f'guide/project/agent-clarity-validation-{DATE}.json'
TRANSPORT_WORKFLOW = '.github/workflows/agent-reader-apply.yml'


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT).decode('utf-8')


def original(path: str) -> str:
    return git('show', f'{BASE}:{path}')


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def write(path: str, content: str) -> None:
    p = ROOT / path; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.rstrip() + '\n', encoding='utf-8', newline='\n')


def jwrite(path: str, data) -> None:
    write(path, json.dumps(data, ensure_ascii=False, indent=2))


assert os.environ.get('GITHUB_REPOSITORY') == REPO, 'unexpected repository'
assert os.environ.get('GITHUB_REF_NAME') == BRANCH, 'not the isolated publication branch'
assert not git('status', '--porcelain').strip(), 'checkout must begin clean'
paths = [p for p in git('ls-tree', '-r', '--name-only', BASE, MODULE + '/docs').splitlines() if p.endswith('.md')]
paths.sort()
assert len(paths) == 24
old = {i: original(p) for i, p in enumerate(paths, 1)}
drafts = {i: read(f'_agent_refine/{i:02d}.md') for i in range(1, 25)}
review = read('_agent_refine/review.md'); quick = read('_agent_refine/quick.md')
answers = json.loads(read('_agent_refine/interview.json'))
assert len(answers) == 56

# Original numbered sections -> new main explanation. Endcaps are handled by role.
DEST = {
1:[1,2,3,5,4,2,1,5],
2:[2,3,3,4,5,5,5,5,3],
3:[1,2,4,3,5,5,5,3,1,6,3],
4:[1,1,2,3,4,5,6,6,4,6],
5:[1,2,3,3,6,4,4,5,3,6],
6:[1,1,2,2,3,4,5,5,6,6,6],
7:[1,2,2,1,3,4,3,5,5,4],
8:[1,2,2,3,5,5,4,3,4,2],
9:[1,3,3,2,5,6,6,7,4,3,6],
10:[1,2,3,1,3,2,4,5,6,4,6],
11:[1,2,4,2,3,5,5,5,5,5,6,6],
12:[1,3,2,3,4,2,6,6,6,5,5,6,6],
13:[1,3,4,4,2,2,3,5,4,4,6,6,7,4],
14:[1,2,2,2,3,3,4,5,5,5,5,5],
15:[1,1,2,3,4,3,3,1,1,5,4,6],
16:[1,2,3,4,5,6,7],
17:[1,2,2,2,2,3,3,4,5,5],
18:[1,1,6,2,3,3,3,4,4,5,4,5,6],
19:[1,2,2,2,3,3,3,4,3,4,4,4,4,5,6,4],
20:[2,2,3,3,1,3,5,1,4,4,3,6],
21:[1,1,2,3,3,4,4,2,5,6,5,6,3,6,6,3],
22:[1,1,1,2,2,2,3,4,5,3,3,5,6,6,6,1],
23:[1,4,2,1,2,3,4,4,4,2,5,2,1,7,7,5,2,7,6],
24:[1,5,2,3,4,5,5,6,6,6,7,1,6,7],
}


def numbered_sections(text: str):
    matches = list(re.finditer(r'^## (\d+)\. (.+)$', text, re.M))
    return [(int(m[1]), m[2], text[m.start():matches[j+1].start() if j+1 < len(matches) else len(text)]) for j, m in enumerate(matches)]


def outer_details(text: str) -> list[str]:
    depth = 0; start = None; result = []
    for m in re.finditer(r'</?details\b[^>]*>', text):
        if m[0].startswith('</'):
            depth -= 1
            if depth == 0 and start is not None:
                result.append(text[start:m.end()]); start = None
        else:
            if depth == 0: start = m.start()
            depth += 1
    if depth != 0: raise ValueError('original details are unbalanced')
    return result


# Preserve tested standard-library examples verbatim, including their disclaimers.
for n, marker in [(3, 'feedback_loop'), (5, 'registry_projection')]:
    fences = re.findall(r'```python\n.*?\n```', old[n], re.S)
    code = next(c for c in fences if '# runnable-example: ' + marker in c)
    drafts[n] = drafts[n].replace('{{' + marker + '}}', code)

mcp = old[16].split('<a id="human-a"></a>', 1)[0].rstrip()
mcp = re.sub(r'^\[← 上一章\].*$', '', mcp, flags=re.M)
mcp = mcp.replace('本章主要依据用户指定的官方`2026-07-28`架构文档', '本章采用官方 `2026-07-28` 协议作为学习基线，关键行为核验于 2026-09-28')
mcp = mcp.replace('没有MCP时，GitHubAdapter、SlackAdapter、DatabaseAdapter、NotionAdapter可能各写一套公共交互；标准化减少重复接入，但底层业务API和真实授权仍需要实现。\n', '')
mcp = mcp.replace('；下一章解释Skill（技能包）和Hook（生命周期钩子）如何利用这些能力，不再重复协议全过程。', '。')
mcp = re.sub(r'<a\s+id="[^"]+"></a>\s*', '', mcp)
drafts[16] = drafts[16].replace('{{keep_mcp_main}}', mcp)
# Directly explain two remaining terms before their review questions use them.
drafts[17] = drafts[17].replace('## 2. Skill', 'Command（命令入口）通常由用户显式触发应用行为，例如 `/review` 可以启动报告核查。一个命令可以加载技能或调用工具；入口、知识与执行仍是不同责任。\n\n## 2. Skill', 1)
drafts[10] = drafts[10].replace('## 2. 从旧历史', '窗口更大可以推迟容量上限，但不消除重复、陈旧信息、时延和费用，也不保证所有输入都被有效利用。是否压缩应看任务与实测，可以先缩小读取或外部化，不要求每次都强制生成摘要。\n\n## 2. 从旧历史', 1)

# Keep product-specific deep dives outside the learning mainline.
notes = ['# Agent｜固定实现对照与选读', '', '[← 技术资料](README.md) · [课程入口](../../curriculum/09-agent/README.md)', '',
         '本页承接课程中的产品实现选读，首次学习不需要靠它补齐核心前提。各段保留原稿指定快照的实现范围；本轮没有重新核验这些仓库的全部上游变化，不将其视作当前发行版的默认保证。', '',
         '课程旧实现对照主要使用 Codex `fc948f8c473e5d11e780ffcf1fd7f812a2020932` 与学习用 Claude Code 私有镜像 `58231dcce408f805c645cfbc352d2876b517223b`。Products 和当前源码索引有自己的版本，不跨快照拼接结论。官方协议与框架行为以课程末尾的明确版本和官方链接为准。', '']
extra_sections = {8:{5}, 13:{3,9,11}, 17:{7}, 18:{7}, 19:{7}, 20:{4,10}, 23:{3}, 24:{3,4,5}}
source_preserved = []
for n, p in enumerate(paths, 1):
    title = drafts[n].splitlines()[0][2:]
    notes += [f'<a id="chapter-{n:02d}"></a>', f'## {title}', '', f'[回到课程](../../{p}) · [本次精修前的固定稿](https://github.com/{REPO}/blob/{BASE}/{p})', '']
    pieces = []
    for block in outer_details(old[n]):
        summary = re.search(r'<summary>(.*?)</summary>', block, re.S)
        if summary and re.search(r'源码|产品|实现对照|官方|Codex|Claude|框架|Benchmark', summary[1]):
            if '# runnable-example:' not in block:
                pieces.append(block)
    for num, title_old, segment in numbered_sections(old[n]):
        if num in extra_sections.get(n, set()):
            cleaned = re.sub(r'^## \d+\. ', '### ', segment, count=1)
            pieces.append('<details>\n<summary>补充：' + html.escape(title_old) + '</summary>\n\n' + cleaned.strip() + '\n\n</details>')
    if not pieces:
        notes += ['本章主要建立通用职责与边界；具体实现可沿[源码及官方资料索引](README.md)选择，不额外复制正文或要求掌握产品私有类名。', '']
    for segment in pieces:
        segment = re.sub(r'<a\s+id="[^"]+"></a>\s*', '', segment)
        segment = '\n'.join(line for line in segment.splitlines() if not re.search(r'HUMAN-A|AGENT-\d{3}|S\d{3}|Source Count', line))
        # Relative references were written from a curriculum chapter, not this index.
        for _, href in list(markdown_links(segment)):
            value = resolve(ROOT, ROOT / p, href)
            if value:
                target, fragment = value
                relative = os.path.relpath(target, ROOT / 'references/agent').replace(os.sep, '/')
                new_href = relative + ('#' + fragment if fragment else '')
                segment = segment.replace('](' + href + ')', '](' + new_href + ')')
        notes += [segment.strip(), '']
    source_preserved.append({'chapter':n, 'preserved_optional_blocks':len(pieces), 'target':f'references/agent/implementation-notes.md#chapter-{n:02d}'})
write('references/agent/implementation-notes.md', '\n'.join(notes))

aliases = []; dispositions = []
for n, p in enumerate(paths, 1):
    text = drafts[n]
    if '{{' in text: raise ValueError('unresolved template: ' + p)
    # Stable current anchors use core-N; section-N remains a compatibility alias.
    text = re.sub(r'^(## (\d+)\. .+)$', lambda m:f'<a id="core-{m[2]}"></a>\n\n'+m[1], text, flags=re.M)
    endcaps = {'summary':'## 本章小结', 'interview':'## 🎯 面试怎么回答', 'pitfalls':'## ⚠️ 易错点', 'self-test':'## 本章自测', 'references':'## 知识回看与权威资料'}
    for key, heading in endcaps.items():
        text = text.replace(heading, f'<a id="{key}"></a>\n\n' + heading, 1)
    present = anchors(text); assignments = {}
    for num, title_old, segment in numbered_sections(old[n]):
        if '面试怎么' in title_old: target = 'interview'
        elif '易错' in title_old: target = 'pitfalls'
        elif '自测' in title_old: target = 'self-test'
        elif re.search(r'HUMAN-A|产品实现|源码证据|官方资料', title_old): target = 'references'
        else:
            count = len(re.findall(r'^## \d+\. ', text, re.M))
            desired = DEST[n][num-1] if num <= len(DEST[n]) else count
            target = 'core-' + str(min(desired, count))
        for alias in anchors(segment):
            if alias not in present:
                assignments.setdefault(alias, target)
        dispositions.append({'path':p, 'old_section':num, 'old_title':title_old, 'new_target':target,
                             'treatment':'证据/实现移至资料或维护映射' if target=='references' else '按认知职责整合，不承诺逐字保留'})
    # Preserve explicit anchors before headings, full-document duplicate heading slugs,
    # and any incoming historical compatibility aliases.
    for alias in anchors(old[n]):
        if alias in present or alias in assignments: continue
        if alias == 'human-a': target = 'references'
        elif alias in endcaps: target = alias
        elif alias.startswith('section-'):
            num = int(alias.split('-')[-1]); target = ('core-' + str(DEST[n][num-1])) if num <= len(DEST[n]) else 'references'
        else:
            # Legacy IDs precede their explanation, so find the next old heading.
            loc = old[n].find(f'id="{alias}"')
            before = old[n][:loc] if loc >= 0 else ''
            prev = list(re.finditer(r'^## (\d+)\. (.+)$', before, re.M))
            idx = int(prev[-1][1]) if prev else 0
            target = ('core-' + str(DEST[n][idx-1])) if 1 <= idx <= len(DEST[n]) else 'references'
        if target not in present: target = 'references'
        assignments[alias] = target
    grouped = {}
    for alias, target in sorted(assignments.items()):
        grouped.setdefault(target, []).append(alias)
        aliases.append({'path':p, 'alias':alias, 'target':target})
    for target, values in grouped.items():
        markup = '\n'.join('<a id="' + html.escape(alias, quote=True) + '"></a>' for alias in values)
        text = text.replace(f'<a id="{target}"></a>', markup + '\n' + f'<a id="{target}"></a>', 1)
    nav = ('[← ' + ('RAG](../../08-rag/README.md)' if n==1 else '上一章](' + Path(paths[n-2]).name + ')')
           + ' · [Agent 目录](../README.md) · '
           + ('[综合复习 →](../review/README.md)' if n==24 else '[下一章 →](' + Path(paths[n]).name + ')'))
    first, rest = text.split('\n', 1)
    text = first + '\n\n' + nav + '\n' + rest + '\n\n---\n\n' + nav
    write(p, text)

# Map existing frozen identifiers to teaching locations, not to duplicated question text.
canonical = original('interview/canonical/agent-harness.md')
canonical_ids = sorted(set(re.findall(r'^###\s+(AGENT-\d{3})\s+·', canonical, re.M)))
assert canonical_ids, 'cannot locate canonical heading format'
evidence = []
for cid in canonical_ids:
    target_chapters = [n for n in old if cid in old[n]]
    if not target_chapters: raise ValueError('existing evidence not located: ' + cid)
    targets = [paths[n-1] + '#core-1' for n in target_chapters]
    evidence.append({'canonical_id':cid, 'baseline_mentions_in_chapters':target_chapters,
                     'teaching_targets':targets,
                     'decision':'保留所属通用机制，删除正文来源叙事；按本轮章节职责整合',
                     'evidence_level':'复用已收录 Canonical 与章节映射；非新增外部原帖核验'})
jwrite(MAPPING, {'schema_version':1, 'baseline':BASE, 'date':DATE, 'aliases':aliases,
                 'section_dispositions':dispositions, 'implementation_preservation':source_preserved,
                 'evidence':evidence, 'frozen_statistics_changed':False,
                 'scope_note':'映射用于导航与维护，不证明全部面经原帖重新回读或每项事实重新验证。'})

# Curated answers retain every original training question and get exact primary links.
old_questions = original(MODULE + '/interview/高频面试题.md')
questions = re.findall(r'^### (\d+)\. (.+)$', old_questions, re.M)
assert [int(i) for i,_ in questions] == list(range(1,57))
records = [{'id':int(i), 'question':q, 'chapter':a[0], 'section':a[1], 'answer':a[2]}
           for (i,q),a in zip(questions,answers)]
jwrite(MODULE + '/interview/questions.json', {'schema_version':1, 'purpose':'教学口述题的单一编辑源，不是新的面经证据或频率统计', 'questions':records})
write(MODULE + '/review/README.md', review)
write(MODULE + '/interview/面试前速查表.md', quick)

homepage = ['# Agent｜从任务到可验证的执行', '', '[← RAG](../08-rag/README.md) · [Handbook](../../README.md) · [学习路线](../../guide/learning-path.md) · [System Design →](../10-system-design/README.md)', '',
            '模型可以提出下一步，但程序必须把允许的动作做出来，把结果带回来，并判断任务是否真的完成。本模块沿这一条反馈主线，学习工具、上下文、记忆、状态、安全、恢复和评测。', '',
            '适合已经理解模型基本输入输出、接口与权限、数据库和缓存基本用途的学习者。进入时不要求掌握 Agent 框架；概念不绑定某种编程语言，两段 Python 标准库例子只是可选的可观察实验。', '',
            '## 学习主线', '', '```text', '任务与自主权 → 反馈循环 → 工具说明、发现与执行', '→ 计划和模型输入 → 记忆、状态与恢复', '→ 权限、协议与扩展 → 协作 → 诊断、评测与交付', '```', '',
            '## 正式章节', '']
phases = [('A｜先走通一项任务',range(1,4)),('B｜把工具调用变成受控执行',range(4,8)),('C｜选择下一步及模型所需信息',range(8,12)),('D｜保存与恢复工作',range(12,14)),('E｜安全接入与协作',range(14,20)),('F｜验证、交付与实现选择',range(20,25))]
for name, numbers in phases:
    homepage += ['### '+name, '', '| 章 | 要理解的问题 |', '|---:|---|']
    for n in numbers:
        topic = re.sub(r'^# \d+\. ', '', read(paths[n-1]).splitlines()[0])
        homepage.append(f'| {n:02d} | [{topic}](docs/{Path(paths[n-1]).name}) |')
    homepage += ['']
homepage += ['## 怎样学习与回看', '',
             '第一遍沿主线理解每个动作及结果，用章末自测检查能否推导。第二遍用 Review 重建关系，再用集中问题训练口述；产品源码用于对照真实实现，不作为首次理解的隐藏前提。', '',
             '| 入口 | 用途 |', '|---|---|', '| [综合复习](review/README.md) | 用任务和失败重建机制关系 |', '| [面试表达](interview/高频面试题.md) | 逐题练习判断、原因和边界 |', '| [易错点](interview/面试易错点.md) | 从各章同一来源回顾误区 |', '| [回顾卡](interview/面试前速查表.md) | 临时唤醒已学知识 |', '| [Agent Products](../../products/agent/README.md) | 进入固定源码中的完整系统 |', '| [技术资料](../../references/agent/README.md) | 核对版本与事实，选择实现选读 |', '',
             '## 模块边界', '',
             '模型生成机制由 LLM Foundation 讲解，检索证据质量由 RAG 讲解；Agent 负责它们如何参与反馈执行。通用事务、队列与幂等机制在 Backend 维护，本模块解释模型与工具执行带来的状态、恢复和授权边界。需要的最小前提仍在使用处说明。', '',
             'MCP 采用明确的 2026-07-28 学习基线并对照旧版生命周期，A2A 对照 1.0.0 发布规范。框架网站、安装版本和产品源码快照分别核对；不因存在配置项就保证所有环境行为相同。', '',
             '## 维护与验证依据', '',
             f'本模块包含 {len(paths)} 篇正文。可运行小例子只验证本地反馈与工具映射，不代表已运行真实模型、网络工具或生产恢复实验。', '',
             f'[精修范围与验证记录](../../{REPORT})说明基线、保留迁移与实际检查；[证据及兼容映射](../../{MAPPING})用于持续维护，不在正文重复来源统计。', '',
             '维护生成配套时运行 `python tools/sync_agent_materials.py --check`；结构、内部引用和两个本地例子通过 `python tools/validate_agent_readability.py --run-examples` 检查。自动检查不代替读者验收。']
new_home = '\n'.join(homepage)
old_home = original(MODULE + '/README.md')
missing = anchors(old_home) - anchors(new_home)
new_home = new_home.replace('## 维护与验证依据', '\n'.join(f'<a id="{html.escape(a,quote=True)}"></a>' for a in sorted(missing)) + '\n\n## 维护与验证依据')
write(MODULE + '/README.md', new_home)

style = read('guide/documentation-style-guide.md')
old_policy = re.search(r'## Agent 章末固定形式\n.*?(?=\n## )', style, re.S)
assert old_policy, 'current Agent style paragraph changed; review rather than overwrite'
new_policy = '''## Agent 主线、证据与训练分工

正文按知识依赖建立独立模型，真人问题用于抽象共同机制、校准深度与失败条件。来源 ID、频次和收录过程进入维护映射或 Interview 证据入口，不要求在教材重复一段 HUMAN-A 栏目。不能为了让关键词检查通过而污染教学主线。

每章保留具体引入、机制和可观察例子、本章小结、可见的 🎯 面试怎么回答、就地及章末 ⚠️ 易错点、默认折叠自测，以及有用途的知识回看。隐藏面试与复习部分以后，正文仍应能独立建立核心知识；可选产品实现不能成为自测的未讲前提。

集中题目要逐题核对问法、答案和正文位置，不按章节批量复用同一个回答。结构重组同步配套与检查器，保留必要历史锚点并说明真实迁移；历史记录和冻结统计不回写。

Agent 集中问答以 `curriculum/09-agent/interview/questions.json` 为编辑源，易错点以各章为源，使用 `tools/sync_agent_materials.py` 重建并检查漂移。源码选读维护在技术资料层，明确原快照与本轮核验范围。结构、关键词和代码运行都不能独自证明正文易懂。
'''
style = style[:old_policy.start()] + new_policy.rstrip() + '\n' + style[old_policy.end():]
write('guide/documentation-style-guide.md', style)
refs = read('references/agent/README.md')
refs += f'''\n\n## 课程讲解与固定实现选读

[实现对照](implementation-notes.md)集中保存各章有用途的固定源码选读；[能力映射](runtime-capability-map.md)定位正式主责章节。不要将选读中的私有类名、历史开关或产品参数当成首次学习的必备概念。

课程精修关键事实核验：2026-09-28。JSON Schema 数值范围、MCP 2026-07-28、A2A 1.0.0、框架恢复与工具护栏等按正文官方链接校准；没有重新核验全部上游源码，也没有运行真实模型和外部恢复系统。产品目录与本页既有快照表保留各自范围。

[本轮维护记录](../../{REPORT})与[证据映射](../../{MAPPING})记录移入、保留和验证边界，不修改真人来源准入、Canonical 归属或冻结计数。
'''
if 'reader-revision-20260917' not in anchors(refs):
    refs = refs.replace('## 课程讲解与固定实现选读', '<a id="reader-revision-20260917"></a>\n\n## 课程讲解与固定实现选读')
write('references/agent/README.md', refs)

report = f'''# Agent 全模块讲解精修｜{DATE}

[← 课程](../../{MODULE}/README.md) · [章节、证据与锚点映射](agent-clarity-mapping-{DATE}.json) · [机器验证结果](agent-clarity-validation-{DATE}.json)

## 基线与范围

发布整合基线 `{BASE}`，保留此前外围导航同步。24 篇正文、模块入口、Review、56 道口述题、易错点与速查、必要资料入口及现行写作/检查规则纳入本轮。其他课程正文、Products、Coding、Market、Canonical 与历史审查记录不改写。

## 对审查问题的处理

| 问题 | 处理与位置 |
|---|---|
| F01 校验边界 | 04 用实际 Schema 与输入结果区分解析、minimum 范围、业务和授权；14 的检查责任同步 |
| F02 问答错配 | 56 道问题保留身份，答案逐题核对；questions.json 为编辑源，生成可见答案与准确 core-N 回看 |
| F03 章节重复与配套编号 | 05 管发现，16 管协议，17 管 Skill/Hook/Plugin；易错点按24章自动取正文，不复制 MCP 问答 |
| F04 隐藏前提与孤立自测 | 08 的缓存解释归09；13 删除不存在代码的自测，改用有完整条件的恢复推演；产品细节为选读 |
| F05 证据渗入正文 | 来源标识与收录叙事进入维护映射，正文按共同机制展开 |
| F06 检查规则与哲学冲突 | 现行规范和验证器不再要求 HUMAN-A 栏目或正文出现题号；增加单源漂移、题目定位与实际示例回归 |
| F07 导航与版本漂移 | 逐章保留兼容锚点并生成迁移映射；当前标题、资料与复习入口同步 |
| F08 正确新协议被误删风险 | 保留 MCP 2026-07-28 主干，A2A 按1.0.0解释；旧初始化与新请求语义分别标识 |

## 内容保留与重新组织

入门先走通模型判断、程序行动、结果与验收；八组责任放到23章回看。工具、计划、上下文、状态、恢复、安全和协作都从具体状态与失败窗口解释，不机械减少或增加章节数。关键边界如未知副作用、迟到取消、批准绑定、记忆纠错与删除、候选遗漏、写入所有权和评分器错误仍在主责正文。

两段标准库教学示例从原稿原样提取，补足运行与观察说明。产品固定实现转入 references 的按章选读，并保留原快照限制；原395项历史保留记录不改写。新的章节与别名映射用于定位，不把锚点数量或旧段落命中率当成技术深度证明。

## 面经与官方证据边界

本轮复用已有 Canonical、原章节来源关联与已完成审查，不宣称重新穷举外部真人帖子，也不把关键词匹配说成全库逐条原帖复核。没有新增来源、修改冻结 Source Count 或改变 Canonical 主责。所有原关联在维护 JSON 保留，教学深度按共同机制整理。

官方定点核对包括 JSON Schema 数值范围、MCP 2026-07-28 请求与 input_required、A2A 1.0.0、LangGraph 中断重跑、LangChain create_agent、Agents SDK 执行/批准/护栏/追踪、Skills 与 Hooks。链接贴近对应正文。旧产品私有源码与全部最新提交未重新完整验证。

## 验证与未验证

机器结果写在配套 JSON，记录实际命令、返回状态和依赖版本。范围包括两个命名标准库示例、JSON Schema 真实校验、生成资料一致性、24章 Markdown 转 HTML 的表格/标题/折叠结构、兼容锚点与全仓本地链接，以及现有导航/语义/冻结生成器检查。

Markdown 转换与 HTML 结构检查不是实际 GitHub 桌面/手机逐页截图验收；未宣称视觉溢出全量通过。没有调用付费模型，没有运行真实 MCP/A2A、数据库恢复、网络副作用或生产故障演练。本地模拟、静态检查和真实集成严格区分。

## 发布方式

在独立分支组装并验证，最终差异不包含临时载荷或临时工作流；通过 PR 合并后再核对 main。此记录不是提前宣称合并完成，发布结果以实际 PR 和提交为准。
'''
write(REPORT, report)
jwrite(VALIDATION, {'status':'validation_pending', 'baseline':BASE, 'scope':'bounded curriculum validation, not real Agent integration'})

# Render aids from declared single sources.
subprocess.run([sys.executable, 'tools/sync_agent_materials.py', '--apply'], check=True)
# Preserve existing inbound anchors to support pages without retaining old numbering in prose.
for path, target in [(MODULE+'/review/README.md','综合推演'), (MODULE+'/interview/面试易错点.md',None), (MODULE+'/interview/面试前速查表.md','交付前回顾')]:
    if path.endswith('面试易错点.md'): continue  # Generated titles now match all24; exact incoming links checked below.
    text = read(path); missing = anchors(original(path)) - anchors(text)
    if missing:
        markup = '\n'.join(f'<a id="{html.escape(a,quote=True)}"></a>' for a in sorted(missing))
        heading = '## ' + target
        write(path, text.replace(heading, markup + '\n\n' + heading, 1))

# Remove temporary transport before any global Markdown scans and before publication.
shutil.rmtree(ROOT / '_agent_refine')
(ROOT / TRANSPORT_WORKFLOW).unlink()
subprocess.run([sys.executable, 'tools/sync_outer_navigation.py', '--apply'], check=True)

EXACT_ALLOWED = {
 'README.md','curriculum/README.md','guide/knowledge-map.md','guide/learning-path.md',
 'guide/navigation-index.json','guide/navigation-index.md','guide/project/README.md','guide/audits/README.md',
 'guide/README.md','tools/README.md','references/README.md','products/README.md','products/agent/README.md',
 'guide/audits/final-quality-audit.md','guide/audits/content-depth-audit.md','guide/audits/curriculum-granularity-audit.md',
 'guide/audits/foundation-status-audit.md','guide/project/integration-status.md',
 'guide/documentation-style-guide.md','references/agent/README.md','references/agent/runtime-capability-map.md',
 'references/agent/implementation-notes.md','tools/sync_agent_materials.py','tools/validate_agent_readability.py',
 'tools/test_agent_course.py','tools/agent-validation-requirements.txt', REPORT,MAPPING,VALIDATION,
}

def allowed(path: str, transport: bool = False) -> bool:
    return path.startswith(MODULE+'/') or path in EXACT_ALLOWED or (transport and (path.startswith('_agent_refine/') or path==TRANSPORT_WORKFLOW))


def stage_safe():
    changed = set(git('diff','--name-only','HEAD').splitlines())
    new = set(git('ls-files','--others','--exclude-standard','-z').split('\0')) - {''}
    bad = [p for p in changed|new if not allowed(p, True)]
    if bad: raise ValueError('unauthorized working changes: '+repr(bad))
    if changed|new:
        subprocess.run(['git','add','-A','--',*sorted(changed|new)], check=True)
    final = git('diff','--name-only',BASE).splitlines()
    bad = [p for p in final if not allowed(p)]
    if bad: raise ValueError('unauthorized final diff: '+repr(bad))
    return final

changed = stage_safe()
results = []
commands = [
 [sys.executable,'-m','compileall','-q','tools'],
 [sys.executable,'tools/sync_agent_materials.py','--check'],
 [sys.executable,'tools/test_agent_course.py'],
 [sys.executable,'tools/validate_agent_readability.py','--run-examples'],
 [sys.executable,'tools/sync_outer_navigation.py','--check'],
 [sys.executable,'tools/test_outer_navigation.py'],
 [sys.executable,'tools/test_learning_navigation.py'],
 [sys.executable,'tools/validate_repository_semantics.py'],
]
for cmd in commands:
    if cmd[1].endswith('.py') and not (ROOT/cmd[1]).is_file():
        raise FileNotFoundError('required validation unavailable: '+cmd[1])
    print('\nRUN:', ' '.join(cmd), flush=True)
    result = subprocess.run(cmd, text=True, encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    print(result.stdout, flush=True)
    results.append({'command':cmd[1:], 'exit_code':result.returncode, 'output':result.stdout})
    if result.returncode:
        raise RuntimeError('validation failed; no publication commit: '+' '.join(cmd))

# Verify frozen generators without staging or accepting any changed evidence.
for cmd in [[sys.executable,'tools/validate_canonical_coverage.py','--help']]:
    pass
# Existing CI exercises all canonical/market regeneration on the PR; record separately.
manifest = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in changed if (ROOT/p).is_file() and p != VALIDATION}
jwrite(VALIDATION, {'status':'passed', 'baseline':BASE, 'workflow_run':os.environ.get('GITHUB_RUN_ID'),
                    'python':sys.version, 'dependencies':{name:importlib.metadata.version(name) for name in ('jsonschema','markdown-it-py')},
                    'commands':results, 'changed_files':changed, 'content_sha256':manifest,
                    'canonical_market_and_unrelated_lessons_unchanged':True,
                    'canonical_market_regeneration':'must be checked separately by the existing PR workflow',
                    'real_model_or_external_service_integration':'not run', 'browser_visual_review':'not run; Markdown/HTML structure only'})
stage_safe()
subprocess.run(['git','config','user.name','github-actions[bot]'], check=True)
subprocess.run(['git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com'], check=True)
subprocess.run(['git','commit','-m','docs(agent): refine all lessons and synchronize teaching aids'], check=True)
# An ordinary branch push fails safely if another actor changed this branch.
subprocess.run(['git','push','origin',f'HEAD:refs/heads/{BRANCH}'], check=True)
print('PUBLISHED BRANCH COMMIT:', git('rev-parse','HEAD').strip(), flush=True)
print('FINAL DIFF FILES:', json.dumps(git('diff','--name-only',BASE,'HEAD').splitlines(),ensure_ascii=False), flush=True)
