"""从实验的统一实现导出正文片段。默认检查；--apply 才更新模块内 Markdown。"""
from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'examples/backend_lab.py'

def expected_documents() -> dict[Path, str]:
    source = SOURCE.read_text(encoding='utf-8')
    regions = dict(re.findall(r'^# region (\w+)\n(.*?)^# endregion \1\s*$', source, re.M | re.S))
    result = {}
    for path in (ROOT / 'docs').glob('*.md'):
        before = path.read_text(encoding='utf-8')
        def replace(match):
            name = match.group(1)
            if name not in regions:
                raise ValueError(f'{path}: 未定义片段 {name}')
            return f'<!-- snippet: {name} -->\n```python\n{regions[name].rstrip()}\n```\n<!-- /snippet -->'
        after = re.sub(r'<!-- snippet: (\w+) -->.*?<!-- /snippet -->', replace, before, flags=re.S)
        if before != after:
            result[path] = after
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    changes = expected_documents()
    if changes and not args.apply:
        raise SystemExit('片段不同步：' + ', '.join(str(p.relative_to(ROOT)) for p in changes))
    for path, text in changes.items():
        path.write_text(text, encoding='utf-8')
    print(f'正文片段：{len(changes)} 项更新' if args.apply else '正文片段与实验统一源一致')

if __name__ == '__main__':
    main()
