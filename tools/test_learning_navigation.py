"""Regression checks for the navigation codemod, without touching real repository data."""
from pathlib import Path
import importlib.util
import json

spec=importlib.util.spec_from_file_location('nav',Path(__file__).with_name('sync_learning_navigation.py'))
nav=importlib.util.module_from_spec(spec);spec.loader.exec_module(nav)
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'guide/learning-order.json').read_text(encoding="utf-8"))
ORDER=[x['directory'] for x in data['modules']]
LABELS={x['directory']:x['label'] for x in data['modules']}
OLD=['01-python','02-fastapi','03-backend-engineering','04-mysql','05-redis','06-vector-db','07-llm-foundation','08-rag','09-agent','10-system-design']
NAMES={'01-python':'Python Foundation','02-fastapi':'FastAPI','03-backend-engineering':'AI Backend Engineering','04-mysql':'MySQL','05-redis':'Redis','06-vector-db':'Vector Database','07-llm-foundation':'LLM Foundation（应用工程深度）','08-rag':'RAG','09-agent':'Agent','10-system-design':'System Design'}


def test_full_chain_and_frozen_prose():
    chain=' → '.join(f'[{NAMES[x]}](../{x}/README.md)' for x in OLD)
    before=chain+'\n统计基线S001–S279：39 Canonical / 125来源。\n'
    after=nav.transform('curriculum/03-backend-engineering/README.md',before,ORDER,LABELS)
    assert [nav.identify(x) for x in after.splitlines()[0].split(' → ')]==ORDER
    assert after.splitlines()[1]==before.splitlines()[1]
    assert nav.transform('curriculum/03-backend-engineering/README.md',after,ORDER,LABELS)==after


def test_bold_current_module():
    chain=' → '.join('**Python Foundation**' if x=='01-python' else f'[{NAMES[x]}](../{x}/README.md)' for x in OLD)+'\n'
    result=nav.transform('curriculum/01-python/README.md',chain,ORDER,LABELS)
    assert result.startswith('**Python Foundation**')
    assert result.index('04-mysql')<result.index('03-backend-engineering')


def test_entry_table_keeps_counts_and_paths():
    head='| # | 模块 | Blocks | Canonical |\n|---|---|---|---|\n'
    before=head+''.join(f'| {i:02d} | [{NAMES[x]}](curriculum/{x}/README.md) | {100+i} | {200+i} |\n' for i,x in enumerate(OLD,1))
    result=nav.transform('README.md',before,ORDER,LABELS)
    rows=[x for x in result.splitlines() if nav.identify(x)]
    assert [nav.identify(x) for x in rows]==ORDER
    assert '| 05 | [AI Backend Engineering](curriculum/03-backend-engineering/README.md) | 103 | 203 |' in result


def test_adjacent_headers_and_tail():
    before='# Backend\n\n[← FastAPI](../02-fastapi/README.md) · [MySQL →](../04-mysql/README.md)\n\n正文：数据库机制见[MySQL](../04-mysql/README.md)。\n\n下一环：[MySQL](../04-mysql/README.md)。\n'
    after=nav.transform('curriculum/03-backend-engineering/README.md',before,ORDER,LABELS)
    assert '[← Redis](../05-redis/README.md)' in after
    assert '[Vector DB →](../06-vector-db/README.md)' in after
    assert '正文：数据库机制见[MySQL](../04-mysql/README.md)。' in after
    assert '下一环：[Vector DB](../06-vector-db/README.md)。' in after


def test_knowledge_map_moves_whole_sections():
    before='# Map\n\n'+''.join(f'## {i:02d}. [{NAMES[x]}](../curriculum/{x}/README.md) ✅ — {i} blocks\n\nPAYLOAD:{x}\n\n' for i,x in enumerate(OLD,1))+'## 使用规则\n\nDo not modify frozen history.\n'
    result=nav.transform('guide/knowledge-map.md',before,ORDER,LABELS)
    assert [line.split('PAYLOAD:')[1] for line in result.splitlines() if 'PAYLOAD:' in line]==ORDER
    assert result.endswith('## 使用规则\n\nDo not modify frozen history.\n')
    assert nav.transform('guide/knowledge-map.md',result,ORDER,LABELS)==result


def test_domain_flow_is_untouched():
    text='读取 → 校验 → 写入 → 失败 → 恢复\n'
    assert nav.transform('README.md',text,ORDER,LABELS)==text
