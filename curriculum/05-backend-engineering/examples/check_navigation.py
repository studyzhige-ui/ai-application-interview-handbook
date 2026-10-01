"""检查章节顺序、标题、入口清单和相邻导航；不改全仓库或冻结统计。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    chapters = json.loads((ROOT/'chapter-order.json').read_text(encoding='utf-8'))['chapters']
    paths = [c['path'] for c in chapters]
    actual = {str(p.relative_to(ROOT)) for p in (ROOT/'docs').glob('*.md')}
    if len(paths) != len(set(paths)) or set(paths) != actual:
        raise SystemExit('顺序清单与实际章节不一致')
    readme=(ROOT/'README.md').read_text(encoding='utf-8')
    block=readme.split('<!-- chapter-list:start -->')[1].split('<!-- chapter-list:end -->')[0]
    expected='| 阅读顺位 | 文件编号 | 章节 |\n|---:|---:|---|\n'+''.join(
        f"| {i} | {int(c['path'].split('/')[1][:2]):02d} | [{c['title']}]({c['path']}) |\n"
        for i,c in enumerate(chapters,1))
    if block.strip() != expected.strip():
        raise SystemExit('README 阅读清单不匹配 chapter-order.json')
    for i,c in enumerate(chapters):
        text=(ROOT/c['path']).read_text(encoding='utf-8')
        if not text.startswith('# '+c['title']+'\n'):
            raise SystemExit('正文标题不匹配：'+c['path'])
        nav=[]
        if i:
            prev=chapters[i-1];nav.append(f"[← {prev['title']}]({Path(prev['path']).name})")
        nav.append('[模块主页](../README.md)')
        if i+1<len(chapters):
            nxt=chapters[i+1];nav.append(f"[{nxt['title']} →]({Path(nxt['path']).name})")
        if text.splitlines()[2] != ' · '.join(nav):
            raise SystemExit('相邻导航不一致：'+c['path'])
    print(f'模块顺序、{len(chapters)} 个正文标题、入口清单与相邻导航一致')

if __name__=='__main__':
    main()
