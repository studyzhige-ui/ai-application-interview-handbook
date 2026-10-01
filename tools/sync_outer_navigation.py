#!/usr/bin/env python3
"""Synchronize active peripheral navigation from repository files, not frozen evidence.

Default: dry run. --apply writes only the planned allowlist; --check detects drift.
No source admission, Canonical frequency, lesson, exercise or historical record is rewritten.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

REGISTRY = 'guide/navigation-index.json'
INDEX = 'guide/navigation-index.md'
STATUS_PAGES = {
    'guide/audits/final-quality-audit.md',
    'guide/audits/content-depth-audit.md',
    'guide/audits/curriculum-granularity-audit.md',
    'guide/audits/foundation-status-audit.md',
    'guide/project/integration-status.md',
}
DESCRIPTIONS = {
 '01-python':'名字与对象、数据容器、函数、资源和并发执行。',
 '02-fastapi':'请求与响应、数据校验、资源生命周期、流式交付与接口验证。',
 '03-mysql':'表与查询、索引、事务、并发、恢复与数据增长。',
 '04-redis':'数据操作、生命周期、缓存、原子修改、持久化与高可用。',
 '05-backend-engineering':'在接口、数据库和缓存之上组织可靠执行、幂等、任务恢复与跨系统协作。',
 '07-vector-db':'向量比较、精确与近似检索、索引、过滤、版本和维护。',
 '06-llm-foundation':'从 Token、模型计算与生成，理解推理成本、模型选择和训练干预。',
 '08-rag':'从语料和查询得到候选、证据、回答，再用评测与版本管理验证质量。',
 '09-agent':'沿模型判断、程序行动、结果回填与任务验收，建立工具、上下文、记忆、安全和恢复。',
 '10-system-design':'从用户动作与完成条件推导容量、状态责任和协作方案，在故障与条件变化中验证取舍。',
}
ROUTES = {
 '01-python':'数据与对象 → 函数与执行 → 对象协作与输入边界 → 运行机制、并发与成本',
 '02-fastapi':'请求与数据契约 → 依赖、资源与执行 → 流式交付与访问控制 → 外部工作、取消与退出 → 测试、部署与综合实践',
 '03-mysql':'表与 SQL → 关系、约束与统计 → 索引与执行计划 → 事务、MVCC、锁与恢复 → 分页、结构演进与批量写入 → 复制、CDC 与分片 → 应用数据建模与跨系统边界',
 '04-redis':'数据与生命周期 → 缓存读取、更新与失效 → 执行成本与多步修改 → 持久化、复制与分片 → 消息、状态与故障判断',
 '05-backend-engineering':'请求责任与持久状态 → 网络与流式交付 → 执行者、容量与等待预算 → 操作身份、幂等与重试 → 消息、可靠任务与一致性 → 安全、观测、部署与演进',
 '07-vector-db':'向量、距离与精确基线 → 图、倒排与压缩索引 → 索引选择 → 数据、过滤与版本 → 分布式执行、评测与维护',
 '06-llm-foundation':'Token 与上下文 → Transformer、注意力与位置 → 生成与解码 → KV 缓存与推理服务 → 模型接口、检索模型与多模态 → Prompt、事实性与训练干预',
 '08-rag':'任务与语料 → 解析、清洗与切分 → 查询与检索 → 融合、重排与证据组装 → 回答、引用与评测 → 权限、版本和生产治理',
 '09-agent':'任务与自主权 → 反馈循环 → 工具说明、发现与执行 → 计划和模型输入 → 记忆、状态与恢复 → 权限、协议与扩展 → 协作 → 诊断、评测与交付',
 '10-system-design':'用户动作与完成条件 → 工作量、资源和状态责任 → 正常数据流与协作边界 → 正确性、过载、权限与恢复 → 观察、评估与安全演进 → 不同业务条件下的组合与取舍',
}
REFERENCE_NAMES = {'agent':'Agent 与产品源码','fastapi':'FastAPI','backend-engineering':'Backend','mysql':'MySQL','redis':'Redis','vector-db':'Vector DB','llm-foundation':'LLM Foundation','rag':'RAG'}

def read(path: Path) -> str:
    return path.read_text(encoding='utf-8')

def tracked(root: Path) -> list[Path]:
    if (root/'.git').exists():
        raw=subprocess.check_output(['git','ls-files','-z'],cwd=root)
        return [root/os.fsdecode(p) for p in raw.split(b'\0') if p]
    return sorted(p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts)

def prose(text: str) -> str:
    out=[]; fence=None
    for line in text.splitlines(keepends=True):
        m=re.match(r'^\s{0,3}(`{3,}|~{3,})',line)
        if m:
            mark=m.group(1)
            if fence is None: fence=mark
            elif mark[0]==fence[0] and len(mark)>=len(fence): fence=None
            out.append('\n'); continue
        out.append('\n' if fence else re.sub(r'(`+).*?\1','',line))
    return ''.join(out)

def markdown_links(text: str):
    """Inline links with balanced URL parentheses, references, and HTML href/src."""
    text=prose(text)
    for m in re.finditer(r'!?\[([^\]\n]*)\]\(',text):
        start=m.end(); i=start; depth=1
        while i<len(text) and depth:
            if text[i]=='\\': i+=2; continue
            if text[i]=='(': depth+=1
            if text[i]==')': depth-=1
            i+=1
        if depth: continue
        raw=text[start:i-1].strip()
        if raw.startswith('<') and '>' in raw: href=raw[1:raw.index('>')]
        else: href=raw.split()[0] if raw else ''
        if href: yield m.group(1),href
    for m in re.finditer(r'^\s{0,3}\[([^\]]+)\]:\s*<?([^\s>]+)>?',text,re.M):
        yield m.group(1),m.group(2)
    for m in re.finditer(r'(?:href|src)=["\']([^"\']+)["\']',text):
        yield 'HTML',m.group(1)

def resolve(root: Path, page: Path, href: str):
    value=urlsplit(href)
    if value.scheme or value.netloc: return None
    if not value.path: return page.resolve(),unquote(value.fragment)
    base=root if value.path.startswith('/') else page.parent
    return (base/unquote(value.path).lstrip('/')).resolve(),unquote(value.fragment)

def heading_slug(title: str) -> str:
    title=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',title)
    title=re.sub(r'<[^>]+>','',title).replace('`','').replace('*','').lower()
    return ''.join(c for c in title if c in ' -_' or unicodedata.category(c)[0] in 'LNM').replace(' ','-')

def anchors(text: str) -> set[str]:
    result=set(re.findall(r'<[^>]+\b(?:id|name)=["\']([^"\']+)',text))
    used={}; fence=None
    for line in text.splitlines():
        m=re.match(r'^\s{0,3}(`{3,}|~{3,})',line)
        if m:
            mark=m.group(1)
            if fence is None: fence=mark
            elif mark[0]==fence[0] and len(mark)>=len(fence): fence=None
            continue
        if fence: continue
        m=re.match(r'^#{1,6}\s+(.+?)(?:\s+#+)?\s*$',line)
        if not m: continue
        slug=heading_slug(m.group(1)); n=used.get(slug,0); used[slug]=n+1
        result.add(slug if n==0 else f'{slug}-{n}')
    return result

def title(path: Path) -> str:
    return next((line[2:].strip() for line in read(path).splitlines() if line.startswith('# ')),path.stem)

def rel(page: str, target: str) -> str:
    return Path(os.path.relpath(target,Path(page).parent)).as_posix()

def block(text: str, tag: str, heading: str, content: str) -> str:
    start=f'<!-- {tag}:start -->'; end=f'<!-- {tag}:end -->'
    replacement=f'{start}\n{heading}\n\n{content.strip()}\n{end}'
    if start in text:
        if end not in text: raise ValueError(f'Unclosed generated block: {tag}')
        return re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:replacement,text,flags=re.S)
    return text.rstrip()+'\n\n'+replacement+'\n'

def chapter_order(root: Path, page: Path, docs: list[Path]) -> list[Path]:
    """Prefer complete chapter tables, not incidental earlier prerequisite links."""
    text=read(page)
    tables='\n'.join(line for line in text.splitlines() if line.lstrip().startswith('|'))
    for candidate in (tables, text):
        ordered=[]
        for _,href in markdown_links(candidate):
            target=resolve(root,page,href)
            if target and target[0] in docs and target[0] not in ordered:
                ordered.append(target[0])
        if set(ordered)==set(docs):return ordered
    raise ValueError(f'Module README does not list all chapters: {page}')

def metadata(root: Path, docs: list[Path]) -> list[dict]:
    # Text fingerprints must not depend on Git checkout LF/CRLF conversion.
    return [{'path':p.relative_to(root).as_posix(), 'title':title(p),
             'sha256':hashlib.sha256(read(p).encode('utf-8')).hexdigest()} for p in docs]

def support_entries(root: Path, base: Path) -> list[str]:
    result=[]
    for name in ('review','interview','labs','examples'):
        directory=base/name; page=directory/'README.md'
        if page.is_file():result.append(page.relative_to(root).as_posix())
        elif directory.is_dir():result.append(directory.relative_to(root).as_posix()+'/')
    return result

def validation_paths(root: Path) -> list[Path]:
    """Read-only scope: all tracked Markdown, not just generated entry pages."""
    return sorted(p for p in tracked(root) if p.suffix.lower()=='.md' and p.is_file())

def conflict_text(text: str) -> str:
    """Only explicit, balanced teaching examples are exempt. Code fences are not."""
    start='<!-- conflict-example:start -->'; end='<!-- conflict-example:end -->'
    pattern=re.escape(start)+r'.*?'+re.escape(end)
    cleaned=re.sub(pattern,'',text,flags=re.S)
    if start in cleaned or end in cleaned:
        raise ValueError('Unbalanced conflict-example markers')
    return cleaned


def inventory(root: Path) -> dict:
    modules=json.loads(read(root/'guide/learning-order.json'))['modules']
    if len(modules)!=10 or len({m['directory'] for m in modules})!=10:
        raise ValueError('Learning order must contain ten distinct module identifiers')
    result=[]
    for m in modules:
        base=root/'curriculum'/m['directory']; page=base/'README.md'
        docs=sorted(p for p in (base/'docs').glob('*.md') if re.match(r'^\d+[-_]',p.name))
        if not docs: raise ValueError(f'No chapters: {base}')
        order=chapter_order(root,page,docs)
        support=support_entries(root,base)
        records=m.get('review_records',[])
        for record in records:
            if not (root/record).is_file():raise ValueError(f'Missing review evidence: {record}')
        result.append({**m,'readme':page.relative_to(root).as_posix(),'chapter_count':len(docs),
                       'reading_order':[p.relative_to(root).as_posix() for p in order],
                       'chapter_metadata':metadata(root,order),'support':support})
    products=[]
    for page in sorted((root/'products/agent').glob('*/README.md')):
        docs=sorted([*page.parent.glob('[0-9][0-9]-*.md'),*(page.parent/'docs').glob('[0-9][0-9]-*.md')])
        text=read(page)
        fixed=re.search(r'https://github\.com/([^/\s]+/[^/\s]+)/(?:tree|blob|commit)/([0-9a-f]{40})',text)
        products.append({'name':title(page).split('｜')[0], 'readme':page.relative_to(root).as_posix(),'chapter_count':len(docs),'chapters':[p.relative_to(root).as_posix() for p in docs],'reading_order':[p.relative_to(root).as_posix() for p in chapter_order(root,page,docs)],'chapter_metadata':metadata(root,docs),'support':support_entries(root,page.parent),'source_repository':fixed.group(1) if fixed else None,'source_commit':fixed.group(2) if fixed else None,'private_mirror':bool((fixed and fixed.group(1).endswith('/claude-code-source-private')) or any(term in text for term in ('私有镜像', '私有源码', '私人学习快照', '私人快照')))})
    coding=sorted((root/'practice/coding/docs').glob('[0-9][0-9]-*.md'))
    refs=[p.relative_to(root).as_posix() for p in sorted((root/'references').glob('*/README.md'))]
    refs.extend(p.relative_to(root).as_posix() for p in sorted((root/'curriculum').glob('*/references.md')))
    return {'schema_version':2,'sources':['guide/learning-order.json','curriculum/*/README.md','curriculum/*/docs/*.md','products/agent/*/README.md','products/agent/*/[0-9][0-9]-*.md','practice/coding/docs/*.md','references/*/README.md','curriculum/*/references.md'],'curriculum_chapters':sum(m['chapter_count'] for m in result),'modules':result,'products':products,'coding_chapters':len(coding),'coding_metadata':metadata(root,coding),'references':refs,'statistics_boundary':'Counts describe tracked learning files, not frozen Canonical questions or independent interview sources.'}

def peripheral_paths(root: Path) -> list[Path]:
    return sorted(p for p in tracked(root) if p.suffix.lower()=='.md' and (p.name.lower()=='readme.md' or p.relative_to(root).as_posix() in {'guide/knowledge-map.md','guide/learning-path.md','guide/terminology-glossary.md',INDEX}|STATUS_PAGES))

def plan(root: Path, data: dict) -> dict[str,str]:
    spec=importlib.util.spec_from_file_location('existing_navigation',root/'tools/sync_learning_navigation.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    order=[m['directory'] for m in data['modules']]; labels={m['directory']:m['label'] for m in data['modules']}
    counts={m['directory']:m['chapter_count'] for m in data['modules']}; total=data['curriculum_chapters']
    desired={}
    def put(path,text):
        if not (root/path).exists() or read(root/path)!=text: desired[path]=text
    targets=['README.md','guide/knowledge-map.md','curriculum/README.md']+[m['readme'] for m in data['modules']]
    for path in targets:
        original=read(root/path)
        text=mod.transform(path,original,order,labels)
        if path=='README.md':
            text=re.sub(r'^> \*\*课程：.*$',f'> **课程：10 个模块 / {total} 篇正文** · **Products：{len(data["products"])} 套固定源码快照学习模块** · **市场：JD + HUMAN-A 证据** · **面试能力：235 ACTIVE Canonical（冻结统计基线见 Interview）**',text,flags=re.M)
            for identifier,description in DESCRIPTIONS.items():
                text=re.sub(r'^(\|[^\n]*\]\(curriculum/'+re.escape(identifier)+r'/README\.md\)\s*\|)[^\n]*$',lambda m:m.group(1)+' '+description+' |',text,flags=re.M)
            needle='- [AI Backend Engineering 权威资料](references/backend-engineering/README.md)'
            if needle in text and '(references/mysql/README.md)' not in text:
                text=text.replace(needle,needle+'\n- [MySQL 官方资料](references/mysql/README.md)与[Redis 官方资料](references/redis/README.md)')
            text=block(text,'learning-inventory','## 内容范围与验证边界',f'课程正文数量由实际文件计算；Products 和 Coding 不计入这 {total} 篇。完整入口与数量见[学习资源索引](guide/navigation-index.md)。\n\n课程完成状态、源码阅读、数值实验、真实服务验证与生产验证分别以对应模块的记录为准；冻结面经统计不因文档重排而重算。')
        elif path=='guide/knowledge-map.md':
            lines=text.splitlines(keepends=True)
            for i,line in enumerate(lines):
                identifier=mod.identify(line)
                if line.startswith('|') and identifier in counts:
                    cells=line.split('|')
                    if len(cells)>=7:
                        cells[3]=f' {counts[identifier]} '; cells[-2]=' '+DESCRIPTIONS[identifier]+' '
                        lines[i]='|'.join(cells)
            text=''.join(lines).replace('| Blocks |','| 正文章节 |')
            pattern=r'(^## \d{2}\. \[.*?\]\(\.\./curriculum/(\d{2}-[a-z-]+)/README\.md\))[^\n]*'
            text=re.sub(pattern,lambda m:m.group(1)+f" — {counts[m.group(2)]} 章",text,flags=re.M)
            matches=list(re.finditer(pattern,text,re.M))
            for m in reversed(matches):
                identifier=m.group(2); start=m.end(); next_heading=re.search(r'^## ',text[start:],re.M)
                end=start+next_heading.start() if next_heading else len(text)
                segment=text[start:end]
                segment=re.sub(r'\n\n[^\n]+\n\n```text\n.*?\n```', '\n\n'+DESCRIPTIONS[identifier]+'\n\n```text\n'+ROUTES[identifier]+'\n```',segment,count=1,flags=re.S)
                text=text[:start]+segment+text[end:]
            # Preserve incoming links to the old numbered/quantity-bearing headings.
            old_heads={m.group(2):(m.group(0),heading_slug(m.group(0).lstrip('# ').strip())) for m in re.finditer(pattern,original,re.M)}
            present=anchors(text)
            for match in reversed(list(re.finditer(pattern,text,re.M))):
                old=old_heads.get(match.group(2))
                if old and old[1] not in present:
                    text=text[:match.end()]+f'\n<a id="{old[1]}"></a>'+text[match.end():]
                    present.add(old[1])
            text=text.replace('> 十个一级模块已经全部完成第一版系统教材。这里强调','> 本页按当前正式文件描述十个模块，不以历史验收状态替代后续版本验证。这里强调')
            text=text.replace('### 成熟产品源码层','### 成熟产品源码层')
            text=text.replace('[当前质量审计](audits/final-quality-audit.md)','[审计记录索引](audits/README.md)')
            text=text.replace('当前粒度与深度状态见','历史粒度与深度审查见').replace('v1.0 全仓库最终结论见','v1.0 历史基线结论见')
            text=block(text,'learning-inventory','## 当前文件范围',f'10 个课程模块合计 **{total} 篇正文**。Products 为 **{len(data["products"])} 套 / {sum(p["chapter_count"] for p in data["products"])} 篇专题正文**，Coding 为 **{data["coding_chapters"]} 篇正文**，均作为独立轨道，不加入课程章节合计。\n\n完整入口见[学习资源索引](navigation-index.md)。Canonical 列和各模块来源覆盖保留冻结基线，不能相加推算独立面经总量。')
        elif path.startswith('curriculum/') and path.count('/')==2:
            identifier=path.split('/')[1]
            text=text.replace('> **课程版本：V1** · **教材状态：✅ 完整**','> **课程范围：'+str(counts[identifier])+' 篇正式正文**')
            text=text.replace('> **质量门：✅ Granularity / Coverage / Content Depth**','> **质量说明：** 历史审查与当前验证范围分别记录，不以目录完整代替阅读和运行验收。')
            if identifier=='09-agent':
                text=re.sub(r'(## 4\. 正式学习主线\s*\n\n```text\n).*?(\n```)',lambda m:m.group(1)+ROUTES[identifier]+m.group(2),text,count=1,flags=re.S)
        put(path,text)
    path='guide/learning-path.md'; text=read(root/path)
    text=re.sub(r'\d+个正文章节',f'{total}个正文章节',text)
    text=block(text,'learning-inventory','## 章节与配套入口',f'按[学习顺序配置](learning-order.json)和实际正文同步，当前合计 {total} 篇。目录编号、正文顺序与前后导航保持一致；冻结统计不随导航改变。\n\n[学习资源索引](navigation-index.md)列出每个模块的正文、回顾、面试和实验入口；分组与章节内顺序以各模块 README 为准。')
    put(path,text)
    path='references/README.md'; text=read(root/path)
    lines=['| 资料入口 | 用途 |','|---|---|']
    rank={m['directory'].split('-',1)[1]:i for i,m in enumerate(data['modules'])}
    def reference_key(path):
        name=Path(path).parent.name
        return name.split('-',1)[1] if path.startswith('curriculum/') else name
    refs=sorted(data['references'],key=lambda p:(rank.get(reference_key(p),99),p))
    for p in refs:
        folder=reference_key(p); label=REFERENCE_NAMES.get(folder,title(root/p).split('｜')[0])
        lines.append(f'| [{label}]({rel(path,p)}) | 核对该模块的官方资料、适用版本与实现边界。 |')
    text=re.sub(r'(## 索引\n).*?(\n证据来源包括：)',lambda m:m.group(1)+'\n'+'\n'.join(lines)+'\n'+m.group(2),text,count=1,flags=re.S)
    put(path,text)
    for path in ['products/README.md','products/agent/README.md']:
        text=read(root/path)
        if path=='products/agent/README.md':
            for p in data['products']:
                if p['source_repository'] and p['source_commit']:
                    text=re.sub(re.escape(p['source_repository'])+r'@[0-9a-f]{40}',p['source_repository']+'@'+p['source_commit'],text)
            text=text.replace('四个产品都实现了 Context、Tool、Persistence、Permission 和 Multi-Agent 等能力，但它们围绕不同的运行中心组织这些机制。','四个学习模块使用相同的观察问题进行对照；具体能力是否实现、默认开启或可用，须以各自固定快照和入口条件判断，不能从同名栏目推导能力等价。')
        detail='\n'.join(f'- [{p["name"]}]({rel(path,p["readme"])})：{p["chapter_count"]} 篇专题正文，快照 `{p["source_repository"]}@{p["source_commit"]}`。' for p in data['products'])
        note='Claude Code 使用获授权的私人学习快照，需相应访问权限；其重建/整理范围以模块说明为准，不等同于官方完整源码。其他产品也应区分源码快照、安装版本与实际运行验证。'
        text=block(text,'product-inventory','## 模块范围与访问边界',detail+'\n\n'+note)
        put(path,text)
    for path in ['guide/project/README.md','guide/audits/README.md']:
        text=read(root/path)
        base=text.split('<!-- records-index:start -->')[0]
        linked={resolve(root,root/path,h)[0] for _,h in markdown_links(base) if resolve(root,root/path,h)}
        records=[p for p in (root/path).parent.rglob('*.md') if p.name!='README.md' and p not in linked]
        records.sort(key=lambda p:((re.findall(r'20\d{2}-\d{2}-\d{2}',p.name) or ['0000'])[0],p.as_posix()),reverse=True)
        items=[f'- [{title(p)}]({rel(path,p.relative_to(root).as_posix())})' for p in records]
        intro='按记录自身的基线、日期与验证范围阅读。历史 PASS 不代表此后所有正文已经再次验收；这里只补齐索引，不改写原记录。'
        text=block(text,'records-index','## 专项记录补充索引',intro+'\n\n'+'\n'.join(items))
        put(path,text)
    for path in sorted(STATUS_PAGES):
        if not (root/path).is_file():continue
        text=read(root/path)
        if path.endswith('final-quality-audit.md'):
            content=(f'正式课程：**{len(data["modules"])} 个模块 / {total} 篇正文**。'
                     f'Products：**{len(data["products"])} 套 / {sum(p["chapter_count"] for p in data["products"])} 篇专题正文**。'
                     f'Coding：**{data["coding_chapters"]} 篇正文**。\n\n'
                     '此段由实际文件生成，只表示文档范围；检查结果与专项证据见上文。')
            heading='## 可重建的内容范围'
        elif path.endswith('integration-status.md'):
            chain=' → '.join(f'[{m["label"]}]({rel(path,m["readme"])})' for m in data['modules'])
            content=chain+f'\n\n课程合计 {total} 篇；Products 与 Coding 作为独立轨道。正文标题、阅读顺序、配套入口与内容指纹见[机器目录]({rel(path,REGISTRY)})。'
            heading='## 正式学习主线'
        elif path.endswith('curriculum-granularity-audit.md'):
            rows=['| 顺序 | 模块 | 正文 | 认知主线 |','|---:|---|---:|---|']
            for rank,m in enumerate(data['modules'],1):
                rows.append(f'| {rank:02d} | [{m["label"]}]({rel(path,m["readme"])}) | {m["chapter_count"]} | {ROUTES[m["directory"]]} |')
            content='\n'.join(rows)+f'\n\n合计 **{total} 篇**；章节标题和顺序可回到各模块入口逐项核对。'
            heading='## 现有模块与认知主线'
        else:
            modules=data['modules'][:5] if path.endswith('foundation-status-audit.md') else data['modules']
            rows=['| 顺序 | 模块 | 正文 | 专项记录入口（按记录自身范围） |','|---:|---|---:|---|']
            for rank,m in enumerate(modules,1):
                records=m.get('review_records',[])
                links=' · '.join(f'[{title(root/r)}]({rel(path,r)})' for r in records)
                rows.append(f'| {rank:02d} | [{m["label"]}]({rel(path,m["readme"])}) | {m["chapter_count"]} | {links or "无本轮独立专项复验记录；不继承旧版 PASS"} |')
            content='\n'.join(rows)+'\n\n记录入口不自动授予通过状态；需要查看其基线、修改范围、实际检查和未验证项目。'
            heading='## 课程范围与证据索引'
        put(path,block(text,'current-scope',heading,content))
    # All product snapshot tables are derived from the product entry pages.
    path='references/agent/README.md'
    if (root/path).is_file():
        text=read(root/path)
        for product in data['products']:
            slug=Path(product['readme']).parent.name
            pattern=r'^(\|[^\n]*?\|[^\n]*?\|)\s*`[0-9a-f]{40}`(\s*\|[^\n]*products/agent/'+re.escape(slug)+r'/README\.md[^\n]*$)'
            text=re.sub(pattern,lambda m:m.group(1)+' `'+product['source_commit']+'`'+m.group(2),text,flags=re.M)
        records={
            'claude-code':'guide/audits/claude-code-clarity-refinement-2026-09-27.md',
            'codex':'guide/audits/codex-clarity-refinement-2026-09-27.md',
            'deepseek-harness':'guide/audits/deepseek-harness-clarity-refinement-2026-09-27.md',
            'deer-flow':'guide/audits/deerflow-clarity-refinement-2026-09-27.md',
        }
        rows=['| 产品 | 实际阅读顺序 | 教学修订记录 |','|---|---|---|']
        for product in data['products']:
            slug=Path(product['readme']).parent.name
            labels={c['path']:c['title'] for c in product['chapter_metadata']}
            links=' → '.join(f'[{Path(c).name[:2]}]({rel(path,c)})' for c in product['reading_order'])
            record=records.get(slug)
            evidence=f'[修订范围与验证]({rel(path,record)})' if record and (root/record).is_file() else '见产品入口'
            rows.append(f'| [{product["name"]}]({rel(path,product["readme"])}) | {links} | {evidence} |')
        text=block(text,'product-evidence','## 产品阅读与修订证据', '\n'.join(rows)+'\n\n正文序号与各产品阅读主线保持一致。历史修订记录只说明其基线与实际验证，当前源码依据见产品入口。')
        put(path,text)
    path='guide/README.md';text=read(root/path)
    text=block(text,'learning-inventory','## 导航事实来源','[学习资源索引](navigation-index.md)汇总当前课程、产品、实践和资料入口；[学习顺序配置](learning-order.json)决定模块先后，[机器可读目录](navigation-index.json)由现有文件生成。\n\n维护时运行 `python tools/sync_outer_navigation.py --check` 检查生成漂移与全仓 Markdown 本地链接；先查看默认预览，再使用 `--apply` 更新。历史面经统计和正文不属于同步写入范围。')
    put(path,text)
    path='tools/README.md';text=read(root/path)
    text=block(text,'outer-sync','## 全仓外围导航同步','- [`sync_outer_navigation.py`](sync_outer_navigation.py)：只读扫描全仓 Markdown 的路径、锚点与冲突残留；只在明确允许的入口页、状态页和生成索引内同步数量、顺序、正文指纹与证据入口；默认只预览，`--check` 检查漂移，`--apply` 才写入。\n- [`sync_learning_navigation.py`](sync_learning_navigation.py)：复用已有的路线与前后导航转换，保留目录标识。\n- [`test_outer_navigation.py`](test_outer_navigation.py)：验证计数、保护边界、真实阅读顺序、链接解析、冲突示例和重复运行。\n\n正文、源码与实践资料可被读取和校验，但不会被同步器改写。同步不会重新生成 Market / Canonical，也不自动宣称阅读或实机验证通过。')
    put(path,text)
    path='practice/README.md';text=read(root/path)
    text=block(text,'learning-inventory','## 配套入口',f'[Coding](coding/README.md)包含 {data["coding_chapters"]} 篇正文；练习、Notebook 与渲染版本沿其模块入口使用，不重复计入 Curriculum。开发工作流见 [Tooling](tooling/README.md)。完整资源范围见[学习资源索引](../guide/navigation-index.md)。')
    put(path,text)
    lines=['# 学习资源索引｜按实际内容导航','', '[← Handbook](../README.md) · [学习路线](learning-path.md) · [知识地图](knowledge-map.md)','', '模块顺序来自 `learning-order.json`，章节数量来自正式正文文件；同一正文的 Notebook、实验和渲染版本不重复计数。','',f'## Curriculum：10 个模块，{total} 篇正文','', '| 学习顺序 | 模块 | 正文 | 回顾、面试与实践 |','|---:|---|---:|---|']
    for i,m in enumerate(data['modules'],1):
        support=' · '.join(f'[{Path(p.rstrip("/")).parent.name if p.endswith("README.md") else Path(p.rstrip("/")).name}]({rel(INDEX,p)})' for p in m['support'])
        lines.append(f'| {i:02d} | [{m["label"]}]({rel(INDEX,m["readme"])}) | {m["chapter_count"]} | {support} |')
    lines+=['','## Products：固定快照中的系统实践','', '| 模块 | 专题正文 | 来源边界 |','|---|---:|---|']
    for p in data['products']:
        lines.append(f'| [{p["name"]}]({rel(INDEX,p["readme"])}) | {p["chapter_count"]} | '+('学习用私有镜像，需访问权限；不等同于官方完整仓库。' if p['private_mirror'] else '固定源码快照；不代表全部环境已运行验证。')+' |')
    lines+=['','## 正文标题与实际阅读顺序','','顺序读取模块 README 的完整目录表，并检查与章节编号一致；先修链接不改变目录顺序。']
    for item in [*data['modules'],*data['products']]:
        label=item.get('label',item.get('name',''))
        by_path={c['path']:c for c in item['chapter_metadata']}
        lines+=['','<details>',f'<summary>{label} · {item["chapter_count"]} 篇</summary>','']
        for rank,chapter in enumerate(item['reading_order'],1):
            lines.append(f'{rank}. [{by_path[chapter]["title"]}]({rel(INDEX,chapter)})')
        for entry in item.get('support',[]):
            name=Path(entry.rstrip('/')).parent.name if entry.endswith('README.md') else Path(entry.rstrip('/')).name
            lines.append(f'\n配套：[{name}]({rel(INDEX,entry)})')
        lines+=['','</details>']
    lines+=['','<details>','<summary>Coding · 正文顺序</summary>','']
    for rank,chapter in enumerate(data['coding_metadata'],1):
        lines.append(f'{rank}. [{chapter["title"]}]({rel(INDEX,chapter["path"])})')
    lines+=['','</details>']
    lines+=['','## Practice 与技术依据','',f'- [Coding](../practice/coding/README.md)：{data["coding_chapters"]} 篇正文，题单和练习由模块入口承接。','- [Python 高频基础操作](../practice/python-basics/README.md)：语言与容器的常见写法。','- [数据库基础操作](../practice/database-basics/README.md)：SQL 与 Redis 命令的输入、结果和状态。','- [Git 与开发工作流](../practice/tooling/README.md)：可选参考，不计入课程章数。',f'- [References](../references/README.md)：{len(refs)} 个资料入口（含集中资料目录与模块内参考页），技术事实与真人面经证据分开。','- [项目记录](project/README.md)与[审计记录](audits/README.md)：按记录的适用基线读取。','','⚠️ 章节数量和入口可达仅证明文档范围与导航一致，不等于完成初学者阅读、真实服务或生产验证。','']
    put(INDEX,'\n'.join(lines));put(REGISTRY,json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return desired

def validate(root: Path, pages: list[Path]) -> dict:
    missing=[]; bad_anchors=[]; conflicts=[]; n=0; cache={}
    for p in pages:
        text=read(p)
        if re.search(r'^(?:<{7}|={7}|>{7})(?:\s|$)',conflict_text(text),re.M): conflicts.append(p.relative_to(root).as_posix())
        for label,href in markdown_links(text):
            dest=resolve(root,p,href)
            if not dest: continue
            target,fragment=dest; n+=1
            if not target.exists():missing.append({'page':p.relative_to(root).as_posix(),'href':href});continue
            if fragment and target.is_file() and target.suffix=='.md':
                if target not in cache:cache[target]=anchors(read(target))
                if fragment not in cache[target]:bad_anchors.append({'page':p.relative_to(root).as_posix(),'href':href})
    return {'markdown_pages_scanned':len(pages),'peripheral_pages_scanned':len(pages),'local_links_checked':n,'missing_paths':missing,'unresolved_anchors':bad_anchors,'conflict_markers':conflicts}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    mode=parser.add_mutually_exclusive_group();mode.add_argument('--apply',action='store_true');mode.add_argument('--check',action='store_true')
    parser.add_argument('--report',type=Path)
    args=parser.parse_args();root=args.root.resolve()
    before={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked(root) if p.is_file()}
    data=inventory(root);changes=plan(root,data)
    permitted={p.relative_to(root).as_posix() for p in peripheral_paths(root)}|{REGISTRY,INDEX}
    if not set(changes)<=permitted:raise RuntimeError('Write outside peripheral allowlist')
    if args.apply:
        for path,content in changes.items():
            p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8',newline='\n')
    protected=[p for p,h in before.items() if p not in changes and (not (root/p).is_file() or hashlib.sha256((root/p).read_bytes()).hexdigest()!=h)]
    if protected:raise RuntimeError('Protected content changed: '+repr(protected))
    pages=validation_paths(root)
    if (root/INDEX).exists() and root/INDEX not in pages:pages.append(root/INDEX)
    checks=validate(root,pages)
    result={'python_version':sys.version.split()[0],'mode':'apply' if args.apply else ('check' if args.check else 'preview'),'curriculum_chapters':data['curriculum_chapters'],'module_counts':{m['directory']:m['chapter_count'] for m in data['modules']},'product_chapters':sum(p['chapter_count'] for p in data['products']),'coding_chapters':data['coding_chapters'],'changed_files':list(changes),'unchanged_protected_files':len(before)-len(set(changes)&set(before)),'protected_content_changes':protected,'idempotent':not plan(root,inventory(root)) if args.apply else None,**checks}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if checks['missing_paths'] or checks['unresolved_anchors'] or checks['conflict_markers']:return 2
    if args.apply and not result['idempotent']:return 2
    return 1 if args.check and changes else 0

if __name__=='__main__':raise SystemExit(main())
