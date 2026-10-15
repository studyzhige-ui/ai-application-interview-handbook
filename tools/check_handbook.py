#!/usr/bin/env python3
"""Read-only architecture, Markdown navigation and merge-marker checks."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse
import re
import unicodedata

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

def conflict_text(text: str) -> str:
    """Only explicit, balanced teaching examples are exempt. Code fences are not."""
    start='<!-- conflict-example:start -->'; end='<!-- conflict-example:end -->'
    pattern=re.escape(start)+r'.*?'+re.escape(end)
    cleaned=re.sub(pattern,'',text,flags=re.S)
    if start in cleaned or end in cleaned:
        raise ValueError('Unbalanced conflict-example markers')
    return cleaned

def check(root: Path) -> list[str]:
    errors=[]
    required={'curriculum','products','practice','market','interview','tools','.github'}
    actual={p.name for p in root.iterdir() if p.is_dir() and p.name not in {'.git','__pycache__'}}
    if actual != required: errors.append(f'root directories: expected {sorted(required)}, got {sorted(actual)}')
    for name in ('README.md','WRITING.md'):
        if not (root/name).is_file(): errors.append(f'missing {name}')
    for area in ('curriculum','products','practice','market','interview','tools'):
        if not (root/area/'README.md').is_file(): errors.append(f'{area}: missing README.md')
    module_names=['01-python','02-fastapi','03-mysql','04-redis','05-backend-engineering','06-llm-foundation','07-vector-db','08-rag','09-agent','10-system-design']
    if {p.name for p in (root/'curriculum').iterdir()} != {'README.md', *module_names}:
        errors.append('curriculum: modules do not match the agreed learning order')
    for relative,expected in {
        'products': {'README.md','codex','claude-code','deepseek-harness','deer-flow'},
        'practice': {'README.md','coding','software'},
        'practice/coding': {'README.md','docs','exercises'},
        'market': {'README.md','job-description','interview-experience'},
    }.items():
        directory=root/relative
        if not directory.is_dir() or {p.name for p in directory.iterdir()} != expected:
            errors.append(f'{relative}: unexpected architecture entries')
    software=root/'practice/software'
    if software.is_dir():
        for p in software.iterdir():
            if not p.is_file() or (p.name!='README.md' and not re.match(r'^\d{2}-.+\.md$',p.name)):
                errors.append(f'practice/software: tutorials must be numbered direct Markdown: {p.name}')
    for module in (root/'curriculum').glob('*'):
        if not module.is_dir(): continue
        # Reader-approved curriculum modules contain README.md and docs; review/ is not required.
        expected={'README.md','docs'}
        found={p.name for p in module.iterdir()}
        if found != expected: errors.append(f'{module.relative_to(root)}: expected README.md/docs/review, got {sorted(found)}')
    for product in (root/'products').glob('*'):
        if not product.is_dir(): continue
        if not (product/'README.md').is_file(): errors.append(f'{product.relative_to(root)} missing README')
        if any(p.is_dir() or p.suffix!='.md' for p in product.iterdir()): errors.append(f'{product.relative_to(root)}: product content must be direct Markdown')
    if {p.name for p in (root/'interview').iterdir()} != {'README.md', *module_names}:
        errors.append('interview: modules do not match the agreed learning order')
    for domain in (root/'interview').glob('*'):
        if not domain.is_dir(): continue
        expected={'README.md','01-高频面试题.md','02-易混易错点.md','03-面试速查.md'}
        if {p.name for p in domain.iterdir()}!=expected: errors.append(f'{domain.relative_to(root)}: invalid preparation files')
    for business in ('job-description','interview-experience'):
        expected={'README.md','01-data','02-analysis','03-strategy','04-scripts','05-logs'}
        p=root/'market'/business
        if not p.is_dir() or {x.name for x in p.iterdir() if x.name!='__pycache__'}!=expected: errors.append(f'market/{business}: invalid business layers')
    cache={}
    for page in sorted(root.rglob('*.md')):
        if '.git' in page.parts: continue
        text=page.read_text(encoding='utf-8')
        try: clean=conflict_text(text)
        except ValueError as e: errors.append(f'{page.relative_to(root)}: {e}'); clean=text
        if re.search(r'^(?:<{7}|={7}|>{7})(?: |$)',clean,re.M): errors.append(f'{page.relative_to(root)}: unresolved conflict marker')
        # Immutable source snapshots preserve their original references, which may be historical.
        if '/01-data/raw/' in page.as_posix(): continue
        targets=set()
        for label,href in markdown_links(text):
            try: item=resolve(root,page,href)
            except ValueError: errors.append(f'{page.relative_to(root)}: invalid URL {href}'); continue
            if item is None: continue
            target,anchor=item; targets.add(target)
            if not target.is_relative_to(root.resolve()): errors.append(f'{page.relative_to(root)}: path escapes repository: {href}');continue
            if not target.exists(): errors.append(f'{page.relative_to(root)}: broken path {href}');continue
            if anchor and target.is_file() and target.suffix=='.md':
                # GitHub's plain source view uses line anchors rather than heading slugs.
                line_anchor=re.fullmatch(r'L(\d+)(?:-L(\d+))?',anchor)
                if line_anchor and urlsplit(href).query=='plain=1':
                    first=int(line_anchor[1]); last=int(line_anchor[2] or first)
                    if not 1 <= first <= last <= len(target.read_text(encoding='utf-8').splitlines()):
                        errors.append(f'{page.relative_to(root)}: invalid source line range {href}')
                    continue
                if target not in cache: cache[target]=anchors(target.read_text(encoding='utf-8'))
                if anchor not in cache[target]: errors.append(f'{page.relative_to(root)}: missing anchor {href}')
        if page.name=='README.md':
            # Each reader-facing README lists direct Markdown and child entry pages.
            # Machine/raw data and implementation folders have their own business contracts.
            rel=page.relative_to(root).as_posix()
            if rel.startswith(('curriculum/','products/','practice/','interview/')):
                children=[p for p in page.parent.glob('*.md') if p!=page]
                children += [p for p in page.parent.glob('*/README.md')]
                if page.parent.parent.name in {'curriculum','coding'} or rel=='practice/coding/README.md': children += list((page.parent/'docs').glob('*.md'))
                for child in children:
                    if child.resolve() not in targets: errors.append(f'{rel}: README does not link {child.relative_to(page.parent)}')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args(); errors=check(args.root.resolve())
    for error in errors: print(error)
    print(f'{len(errors)} handbook validation error(s)')
    return bool(errors)

if __name__=='__main__': raise SystemExit(main())
