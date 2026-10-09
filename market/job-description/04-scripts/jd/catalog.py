"""Mechanical validation and readable rendering of model-reviewed JD records."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse


def load_catalog(path):
    """Load the current library and its hash-pinned non-current observations."""
    path = Path(path)
    current = json.loads(path.read_text(encoding='utf-8'))
    reference = current.pop('supporting_observations', None)
    if reference is None:
        return current
    if reference['path'] != 'source-observations.json':
        raise ValueError('Unsupported observations file')
    raw = path.with_name(reference['path']).read_bytes()
    if len(raw) != reference['bytes'] or hashlib.sha256(raw).hexdigest() != reference['sha256']:
        raise ValueError('Supporting observations hash or size mismatch')
    support = json.loads(raw)
    if support['snapshot'] != current['snapshot']:
        raise ValueError('Supporting observations belong to another snapshot')
    sources = support['companies']
    mapping = {c['source_id']: c['other_observations'] for c in sources}
    if len(mapping) != len(sources) or set(mapping) != {c['source_id'] for c in current['companies']}:
        raise ValueError('Supporting observation source IDs are missing or duplicated')
    for company in current['companies']:
        company['other_observations'] = mapping[company['source_id']]
    current['historical_observations'] = support['historical_observations']
    return current


def counts(catalog):
    companies = catalog['companies']
    return {
        'registered_sources': len(companies),
        'current_jobs': sum(len(c['jobs']) for c in companies),
        'companies_with_current_jobs': sum(bool(c['jobs']) for c in companies),
        'historical_observations': len(catalog.get('historical_observations', [])),
        'coverage': {level: sum(c['coverage']['coverage_level'] == level for c in companies)
                     for level in ('complete', 'limited', 'restricted', 'not_started')},
    }


def validate_catalog(catalog, registered_ids):
    errors = []
    if "sourcetoken=" in json.dumps(catalog,ensure_ascii=False).lower():
        errors.append("Public catalog URLs contain a source access parameter")
    companies = catalog.get('companies', [])
    ids = [c.get('source_id') for c in companies]
    if len(ids) != len(set(ids)) or set(ids) != set(registered_ids):
        errors.append('Catalog source IDs differ from the registry or are duplicated')
    for company in companies:
        source = company['source_id']
        if company.get('coverage', {}).get('coverage_level') not in {'complete', 'limited', 'restricted', 'not_started'}:
            errors.append(f'{source}: missing explicit coverage level')
        seen = set()
        for job in company.get('jobs', []):
            identity = job.get('req_id')
            if not isinstance(identity, str) or not identity or identity in seen:
                errors.append(f'{source}: missing/duplicate requisition ID {identity}')
            seen.add(identity)
            label = f'{source}/{identity}'
            for key in ('title', 'official_url', 'full_text', 'decision_reason',
                        'official_type_evidence', 'checked_at_utc'):
                if not job.get(key):
                    errors.append(f'{label}: missing {key}')
            parsed = urlparse(job.get('official_url', ''))
            if parsed.scheme != 'https' or not parsed.hostname:
                errors.append(f'{label}: invalid public source URL')
            if job.get('decision') != 'include' or job.get('review_depth') != 'full_jd':
                errors.append(f'{label}: current job lacks completed full-JD model review')
            if job.get('recruitment_type') not in {'campus', 'internship'}:
                errors.append(f'{label}: unsupported current recruitment type')
            if not isinstance(job.get('locations'), list):
                errors.append(f'{label}: locations must preserve a list')
            text = job.get('full_text', '')
            if hashlib.sha256(text.encode('utf-8')).hexdigest() != job.get('body_sha256'):
                errors.append(f'{label}: source body hash mismatch')
            evidence = job.get('engineering_evidence')
            if not isinstance(evidence, list) or not evidence or any(not q or q not in text for q in evidence):
                errors.append(f'{label}: development evidence is missing or not verbatim')
        for observation in company.get('other_observations', []):
            if observation.get('decision') == 'include':
                errors.append(f'{source}: included job stored among excluded/pending observations')
    for record in catalog.get('historical_observations', []):
        if record.get('status') != 'historical' or record.get('current_pool_eligible') is not False:
            errors.append('Historical observation is not explicitly excluded from current counts')
    if catalog.get('counts') != counts(catalog):
        errors.append('Recorded counts differ from explicit stored records')
    return errors


def render_catalog(catalog):
    summary = counts(catalog)
    lines = ['# 校招与实习岗位索引', '',
             f"本次核验：{catalog['snapshot']['checked_at_utc']}。收录 **{summary['current_jobs']} 个去重岗位或官方岗位意向**，来自 **{summary['companies_with_current_jobs']} 个公司或品牌入口**。", '',
             '完整职责、任职要求、工程依据和所有官方字段保存在[唯一岗位库](official-jds.json)。本页是同源生成的轻量索引，点击岗位名打开官方详情；[综合分析与覆盖范围](../02-analysis/README.md)说明未查全和受限入口。', '',
             '标为“研究交叉”或“多方向”的岗位，只纳入其明确的应用工程职责，不表示整份JD都是纯AI应用研发。届次和资格以官方完整原文为准，历史观察不计本页岗位数。', '']
    labels={'应用与Agent核心研发':'应用研发','评测与测试工具研发':'评测研发','算法或研究与应用工程混合':'研究交叉','多方向或跨职能工程':'多方向'}
    def cell(value):
        return str(value or '未单列').replace('|', '／').replace('\n', ' ')
    for company in catalog['companies']:
        if not company['jobs']: continue
        lines += [f"## {company['company']}（{len(company['jobs'])}）", '', '| 岗位与官方链接 | 招聘类型 | 毕业/学历范围 | 地点 | 职责范围 |', '| --- | --- | --- | --- | --- |']
        for job in company['jobs']:
            kind={'campus':'校招','internship':'实习'}[job['recruitment_type']]
            locations='、'.join(str(x) for x in job['locations']) or '未披露'
            title=cell(job['title']).replace('[','（').replace(']','）')
            lines.append(f"| [{title}]({job['official_url']}) | {kind} | {cell(job.get('cohort') or '未披露')} | {cell(locations)} | {labels[job['role_track']]} |")
        lines.append('')
    return '\n'.join(lines).rstrip()+'\n'
