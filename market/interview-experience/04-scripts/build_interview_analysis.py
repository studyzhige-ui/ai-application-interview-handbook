#!/usr/bin/env python3
"""Rebuild interview evidence from complete preserved first-source sections, without network access.

--check compares every generated artifact without changing files. Topic rules are
multi-label retrieval categories, NOT a claim that all wording is semantically equal.
Only literal normalization deduplicates question wording; source frequency is sets.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import unicodedata

BUSINESS = Path(__file__).resolve().parents[1]
SOURCE = re.compile(r'^## (S\d{3}) (.+)$')
EXTENSION = re.compile(r'^## Existing-process extension.*?\b(S\d{3})\b(.*)$')
BOUNDARY = re.compile(r'^#{1,2} ')
NUMBERED = re.compile(r'^(\d+)\.\s+(.+)$')
URL = re.compile(r'https?://[^\s<>`]+')
EXPLICIT = re.compile(r'[?？]|如何|怎样|为什么|为何|什么|是否|区别|原理|怎么|怎么办|哪些|解释|手写|手撕|设计|实现|对比|比较|说说|介绍')
BACKGROUND = re.compile(r'自我介绍|^自介[。？]?$|个人职责|本人职责|本人角色|毕业时间|毕业院校|实习时长|实习时间|到岗|薪资|待遇|工作时间|求职意向|求职方向|转正|离职|职业规划|职业发展|异地|个人优势|个人优缺点|兴趣爱好|学习途径|学习方法|学习渠道|学习来源|成就感|幸福感|本科.*成绩|为何选择.*专业|考研|转计算机|沟通能力|实习地点|跨城住宿|目前.*实习|实习感受|更喜欢.*实习|课程与实习|形容自己|投递动机|对.*公司.*了解|团队协作|团队主线|业务主线|期望薪|在校生提升|学习.*平台|项目来源|项目耗时|项目工期|项目做了多久|面试感受|选择.*公司|学校项目或个人兴趣')
UNDISCLOSED = re.compile(r'未披露|未展开|未给出|题面缺失|占位|未公开|未记录具体|未记具体|未详述')
TECHNICAL = re.compile(r'两数之和|爬楼梯|接雨水|评测|评估|测试|回归|分块|语义|面向对象|对象|继承|封装|多态|枚举|全排列|岛屿|栈|计算|物理核|逻辑核|指针|哈希|正则|贪心|动态规划|递归|Q/K/V|K/V|开发|上线|指标|原型|验收|性能|优化|耗时|生成|规模|并行|通信|解析|语料|运维|推理|智能体|知识|权限|流水|队列|代码|磁盘|事务|存储|故障|生产|回滚|发布|部署|技术|工程|业务流|项目|意图|补丁|令牌|模型|算法|索引|数据|系统|架构|接口|链路|并发|性能|数据库|查询|实现|设计|调度|锁|线程|进程|内存|协议|服务|框架|工具|编码|日志|路由|项目.*(?:难点|挑战)|技术方案|字段|状态|检索|向量|搜索|缓存|消息|网络|安全|agent|rag|llm|python|java|mysql|redis|api|sql|http|workflow|skill|coding|react|transformer|checkpoint|workflow',re.I)
MATCHING_CONFIG = json.loads((BUSINESS/'03-strategy/question-families.json').read_text())
FAMILY_RULES = MATCHING_CONFIG['families']
ALIASES = [(re.compile(r'(?<![a-z])'+re.escape(a['term'])+r'(?![a-z])', re.I),a['concept']) for a in MATCHING_CONFIG['matching_aliases']]
def matching_text(text):
    hits=[concept for regex,concept in ALIASES if regex.search(text)]
    return text+' '+' '.join(hits)
EXCLUSION_LABELS = {
 'background':'背景、求职安排或经历概述', 'candidate_question':'候选人反问',
 'author_answer':'作者回答、状态或面后反馈', 'author_inference':'作者推断或不确定题面',
 'undisclosed':'未披露题面或编号范围占位', 'explicitly_excluded':'原材料明确不计技术频率',
 'review_required':'技术内容或提问角色不足以确定', 'editorial':'采集元数据、校验说明或批次观察',
 'technical_question':'有具体问法的技术记录', 'technical_topic':'只披露技术主题/短记，未扩写问句',
}

def sha(data): return hashlib.sha256(data).hexdigest()
def dumps(x): return json.dumps(x,ensure_ascii=False,indent=2)+'\n'
def strip_prefix(text):
    return re.sub(r'^(?:（[^）]*(?:原题|原文|原段|原编号)[^）]*）|\([^)]*原题[^)]*\))\s*','',text).strip()
def normalize(text):
    # Preserve operators and mathematical punctuation; only typography/case/space.
    s=unicodedata.normalize('NFKC',strip_prefix(text))
    # Do not remove *, _, backticks, or other code/math operators.
    return re.sub(r'\s+',' ',s).strip(' 。.？?！!；;')
def classify(text,context,continuation):
    s=strip_prefix(text); full=s+'\n'+continuation
    if '作者推断' in full or '非确定题面' in full: return 'author_inference'
    if ('反问' in s and '面试官反问' not in s) or '原题反问' in text or re.search(r'反问',context): return 'candidate_question'
    if UNDISCLOSED.search(s): return 'undisclosed'
    if re.search(r'【(?:反馈|复盘|作者回答)|^面试反馈|^面后反馈|^作者(?:回答|表示|感想)|^我(?:答|回答)|^答[:：]',s): return 'author_answer'
    if '不计确定技术题频' in continuation or '不计技术题频' in continuation or '不进入题频' in continuation: return 'explicitly_excluded'
    if (BACKGROUND.search(s) and not re.search(r'架构|技术链路|完整链路|核心设计|工作原理|关键取舍|技术点|技术价值|关键难点|模型调优',s)) or re.search(r'HR(?:初聊|终面|面)?(?:｜.*)?$|行为面试|背景与意向|求职/实习安排',context): return 'background'
    if re.fullmatch(r'实习项目[。？]?',s): return 'background'
    if re.match(r'^(?:介绍)?(?:第[一二三]个)?项目(?:介绍|背景|流程)?[。？]?$|^(?:项目|实习)(?:深挖|拷打)[。？]?$',s): return 'background'
    scope=matching_text(s+' '+context)
    matched_family=any(rule_match(f['pattern'],scope) and (not f.get('requires') or rule_match(f['requires'],scope)) for f in FAMILY_RULES)
    if not TECHNICAL.search(scope) and not matched_family and not re.search(r'[A-Za-z]{2,}',s): return 'review_required'
    if EXPLICIT.search(s) and not s.startswith('主题：'): return 'technical_question'
    return 'technical_topic'

ENGLISH_STEMS=('hallucinat','tokeniz','idempoten','idempot','consisten','decompos','rewrit','retriev','reliab','quantiz','scalab','balanc','invalid','pars','tun','break')
LATIN_MORPHOLOGY={'chunk':r'chunk(?:s|ing)?','hash':r'hash(?:ing|es)?','limit':r'limit(?:ing|s)?','trace':r'trace(?:s)?','log':r'logs?','call':r'call(?:ing|s)?','rerank':r'rerank(?:er|ers|ing|s)?','tool':r'tools?','skill':r'skills?','thread':r'thread(?:s|ing)?','process':r'process(?:es)?','lock':r'lock(?:s|ing)?','model':r'models?','token':r'tokens?','context':r'contexts?','loop':r'loop(?:s|ing)?','framework':r'frameworks?','embedding':r'embeddings?','permission':r'permissions?','window':r'windows?','database':r'databases?','container':r'containers?','generator':r'generators?','iterator':r'iterators?','decorator':r'decorators?'}
@lru_cache(maxsize=None)
def compiled_rule(pattern):
    for term,morphology in LATIN_MORPHOLOGY.items():
        pattern=re.sub(r'(?<![A-Za-z])'+term+r'(?![A-Za-z])',lambda _:morphology,pattern)
    for stem in ENGLISH_STEMS:
        pattern=re.sub(r'(?<![A-Za-z])'+stem+r'(?![A-Za-z])',stem+r'[a-z]*',pattern)
    return re.compile(pattern,re.I|re.A)

def rule_match(pattern,text):
    """A Latin keyword may touch Chinese or punctuation, never an unrelated Latin token.

    Explicitly documented morphology and stems cover whole word families; everything else must
    end at a Latin-token boundary. This prevents AST/FastAPI, OOM/Bloom, etc.
    """
    position=0
    regex=compiled_rule(pattern)
    while position<len(text):
        match=regex.search(text,position)
        if match is None: return None
        start,end=match.span();position=start+1
        if start==end: continue
        if start and text[start-1].isascii() and text[start-1].isalpha() and text[start].isascii() and text[start].isalpha(): continue
        if end<len(text) and text[end-1].isascii() and text[end-1].isalpha() and text[end].isascii() and text[end].isalpha(): continue
        return match
    return None

def match_families(text, section='', suppressed=(), rules=None):
    """Positive matches come from the record, never solely from a section title."""
    context=matching_text(strip_prefix(text))
    disambiguation=context+' '+section
    matched=[]
    for family in rules if rules is not None else FAMILY_RULES:
        if family['family_id'] in suppressed: continue
        match=rule_match(family['pattern'],context)
        if (match and
            (not family.get('requires') or rule_match(family['requires'],disambiguation)) and
            (not family.get('domain_requires') or rule_match(family['domain_requires'],text+' '+section)) and
            (not family.get('excludes') or not rule_match(family['excludes'],context))):
            matched.append({'family_id':family['family_id'],'matched_term_or_alias':match[0]})
    return matched


def explicit_followups(continuation, first_line):
    rows=[]
    for offset,line in enumerate(continuation.splitlines()):
        match=re.match(r'^\s+- (.+)$',line)
        if not match: continue
        text=match[1]
        if re.match(r'原文边界|记录边界|不计|作者(?:回答|感想)|现场状态|答[:：]|原文(?:表述|未|没有)|边界',text): continue
        rows.append({'text':text,'line':first_line+offset})
    return rows

def match_record_families(rec, rules=None):
    result=[];seen=set()
    evidence=[{'text':rec['original_text'],'line':rec['line_start'],'kind':'primary'}]+[
        dict(x,kind='explicit_follow_up') for x in rec.get('follow_up_texts',[])]
    for entry in evidence:
        context=rec['section']+(' '+rec['original_text'] if entry['kind']=='explicit_follow_up' else '')
        for match in match_families(entry['text'],context,rec.get('suppressed_family_ids',()),rules):
            if match['family_id'] in seen:continue
            result.append(dict(match,evidence_text=entry['text'],evidence_line=entry['line'],evidence_kind=entry['kind']))
            seen.add(match['family_id'])
    return result

def load_blocks(raw_dir):
    blocks=[]; manifests=[]; batch_editorial=[]
    provenance_path=raw_dir.parents[1]/'01-data/source-provenance.json'
    provenance=json.loads(provenance_path.read_text())['sections'] if provenance_path.exists() else []
    origin_lookup={(x['source_id'],x['raw_path'],x['sha256']):x for x in provenance}
    for path in sorted(raw_dir.glob('batch-*.md')):
        data=path.read_bytes(); lines=data.decode('utf-8').splitlines(keepends=True)
        manifests.append({'path':path.relative_to(raw_dir.parents[1]).as_posix(),'sha256':sha(data),'bytes':len(data)})
        starts=[i for i,l in enumerate(lines) if BOUNDARY.match(l)]
        for pos,start in enumerate(starts):
            end=starts[pos+1] if pos+1<len(starts) else len(lines)
            heading=lines[start].rstrip('\r\n'); m=SOURCE.match(heading); ext=EXTENSION.match(heading)
            block={'raw_path':path.relative_to(raw_dir.parents[1]).as_posix(),'line_start':start+1,'line_end':end,
                   'heading':heading,'text':''.join(lines[start:end]),'lines':lines[start:end]}
            if m or ext:
                match=m or ext
                block.update(source_id=match[1],is_extension=bool(ext),heading_detail=match[2])
                origin=origin_lookup.get((match[1],block['raw_path'],sha(block['text'].encode())))
                if provenance and not origin: raise ValueError(f'Unpreserved first-source section: {match[1]} {path.name}')
                block['original_line_start']=origin['original_line_start'] if origin else block['line_start']
                block['original_line_end']=origin['original_line_end'] if origin else block['line_end']
                block['source_section_sha256']=sha(block['text'].encode())
                blocks.append(block)
            else:
                batch_editorial.append({'raw_path':block['raw_path'],'line_start':start+1,'line_end':end,
                    'heading':heading,'numbered_item_count':sum(bool(NUMBERED.match(l)) for l in lines[start:end]),
                    'reason':'batch_editorial_not_interviewer_evidence'})
    return blocks,manifests,batch_editorial

def parse_corpus(raw_dir):
    blocks,manifests,editorial=load_blocks(raw_dir); sources={}; occurrences=[]
    for block in blocks:
        sid=block['source_id']
        if not block['is_extension']:
            if sid in sources: raise ValueError(f'duplicate formal source: {sid}')
            parts=block['heading_detail'].split('｜')
            sources[sid]={'source_id':sid,'company_raw':parts[0].strip(),'role_raw':parts[1].strip() if len(parts)>1 else None,
              'round_raw':parts[2].strip() if len(parts)>2 else None,'heading_raw':block['heading_detail'],
              'heading_date_raw':'｜'.join(parts[3:-1]) or None,'raw_sections':[], 'urls':[], 'metadata_lines':[], 'occurrence_ids':[]}
    for block in blocks:
        sid=block['source_id']
        if sid not in sources: raise ValueError(f'orphan extension: {sid}')
        source=sources[sid]; text=block['text'];lines=block['lines']
        source['raw_sections'].append({k:block[k] for k in ('raw_path','line_start','line_end','original_line_start','original_line_end','source_section_sha256','is_extension','text')})
        source['urls']=list(dict.fromkeys(source['urls']+[u.rstrip('。；，,.') for u in URL.findall(text)]))
        source['metadata_lines'] += [{'raw_path':block['raw_path'],'line':block['line_start']+i,'text':l.rstrip('\r\n')}
          for i,l in enumerate(lines) if re.match(r'^(?:作者|补充作者|来源|.*来源[：:]|.*日期|.*时间线|时间线|日期说明|发布|原帖核验|真人|Role Scope|流程边界|本人及流程|记录范围)',l)]
        context=''; indexes=[]; note_zone=False
        for i,line in enumerate(lines):
            if line.startswith('### '): context=line[4:].strip(); note_zone=False
            if indexes and re.match(r'^(?:完整性|边界|校验|补充说明|去重|最终去重|原文保留|候选人状态)[：:]|^\*\*(?:完整性|边界|校验)',line): note_zone=True
            m=NUMBERED.match(line)
            # S391 preserves source bullets instead of artificially manufacturing numbers.
            bullet=re.match(r'^- (.+)$',line) if sid=='S391' and not note_zone else None
            if m or bullet: indexes.append((i,m[1] if m else None,m[2] if m else bullet[1],context,note_zone))
        for n,(idx,label,question,section,is_note) in enumerate(indexes):
            stop=idx+1
            while stop<len(lines) and (not lines[stop].strip() or lines[stop].startswith((' ','\t'))): stop+=1
            continuation=''.join(lines[idx+1:stop]).rstrip()
            oid=f"{sid}:{Path(block['raw_path']).stem}:L{block['original_line_start']+idx:05d}"
            disposition='editorial' if is_note else classify(question,section,continuation)
            rec={'occurrence_id':oid,'source_id':sid,'source_sequence':len(source['occurrence_ids'])+1,
                'raw_path':block['raw_path'],'line_start':block['line_start']+idx,'line_end':block['line_start']+stop-1,
                'original_line_start':block['original_line_start']+idx,'original_line_end':block['original_line_start']+stop-1,
                'section':section,'original_list_marker':label,'original_text':question,
                'continuation_text':continuation,'raw_text':''.join(lines[idx:stop]).rstrip('\r\n'),
                'is_extension':block['is_extension'],'disposition':disposition,
                'frequency_eligible':disposition in ('technical_question','technical_topic'),
                'normalized_text':normalize(question),'family_ids':[],'family_matches':[]}
            # No inferred follow-up edge: retain adjacency only. Explicit labels remain exact.
            rec['follow_up_texts']=explicit_followups(continuation,block['line_start']+idx+1)
            rec['explicit_follow_up']=bool(rec['follow_up_texts'] or re.search(r'原题[^）]*追问|^追问',question))
            if rec['follow_up_texts']:
                rec['normalized_text']+='\n'+'\n'.join(normalize(x['text']) for x in rec['follow_up_texts'])
            occurrences.append(rec);source['occurrence_ids'].append(oid)
    return sorted(sources.values(),key=lambda x:x['source_id']),occurrences,manifests,editorial

def build(base=BUSINESS):
    rules=json.loads((base/'03-strategy/question-families.json').read_text())['families']
    sources,occurrences,manifest,editorial=parse_corpus(base/'01-data/raw')
    decisions_path=base/'03-strategy/record-decisions.json'
    decisions=json.loads(decisions_path.read_text())['decisions'] if decisions_path.exists() else {}
    unknown=set(decisions)-{r['occurrence_id'] for r in occurrences}
    if unknown: raise ValueError(f'Orphan record decisions: {sorted(unknown)}')
    for r in occurrences:
        if r['occurrence_id'] in decisions:
            d=decisions[r['occurrence_id']]
            if d['disposition'] not in EXCLUSION_LABELS or not d['reason']: raise ValueError('Invalid record decision')
            r['automatic_disposition']=r['disposition'];r['disposition']=d['disposition'];r['review_reason']=d['reason'];r['suppressed_family_ids']=d.get('suppressed_family_ids',[])
            r['frequency_eligible']=r['disposition'] in ('technical_question','technical_topic')
    expected=json.loads((base/'03-strategy/corpus-contract.json').read_text())
    present=[x['source_id'] for x in sources]
    if present!=expected['source_ids']: raise ValueError('Source IDs differ from approved corpus contract; update contract explicitly for later admissions.')
    actual_manifest={x['path']:x['sha256'] for x in manifest}
    if actual_manifest!=expected['raw_sha256']: raise ValueError('First-source data files differ from corpus contract.')
    actual_sections={f"{src['source_id']}:{Path(sec['raw_path']).stem}:{sec['original_line_start']}":sec['source_section_sha256'] for src in sources for sec in src['raw_sections']}
    if actual_sections!=expected.get('source_section_sha256',actual_sections): raise ValueError('Formal first-source sections differ from preservation proof.')
    by_family=defaultdict(list);by_normal=defaultdict(list)
    for rec in occurrences:
        if not rec['frequency_eligible']: continue
        for match in match_record_families(rec,rules):
            rec['family_ids'].append(match['family_id']);rec['family_matches'].append(match)
            by_family[match['family_id']].append(rec)
        by_normal[rec['normalized_text']].append(rec)
    normalized=[]
    for text,records in sorted(by_normal.items()):
        qid='NQ-'+sha(text.encode())[:16]
        for rec in records: rec['normalized_question_id']=qid
        normalized.append({'question_id':qid,'normalized_text':text,'representative_question':strip_prefix(records[0]['original_text']),
            'source_count':len(set(r['source_id'] for r in records)),'source_ids':sorted(set(r['source_id'] for r in records)),
            'occurrence_ids':[r['occurrence_id'] for r in records],'family_ids':sorted(set(f for r in records for f in r['family_ids'])),
            'normalization_method':'unicode_nfkc_whitespace_only','semantic_equivalence_reviewed':False})
    frequencies=[]
    for family in rules:
        records=by_family[family['family_id']]
        ids=sorted(set(r['source_id'] for r in records))
        if not records: continue
        examples=[]; used=set()
        for r in records:
            if r['normalized_text'] in used:continue
            support=next(m for m in r['family_matches'] if m['family_id']==family['family_id'])
            examples.append({'text':strip_prefix(support['evidence_text']),'source_id':r['source_id'],'occurrence_id':r['occurrence_id'],
                             'raw_path':r['raw_path'],'line':support['evidence_line'],'evidence_kind':support['evidence_kind']});used.add(r['normalized_text'])
            if len(examples)==5:break
        frequencies.append({k:family[k] for k in ('family_id','module','label','granularity')}|{'source_count':len(ids),'source_denominator':len(sources),
            'source_ratio':round(len(ids)/len(sources),6),'grouping_scope':'question_intent_or_competency' if family['granularity']=='question_family' else 'retrieval_hint','semantic_equivalence_claimed':False,'statistical_evidence':family['granularity']=='question_family','source_ids':ids,'occurrence_count':len(records),
            'explicit_question_occurrence_count':sum(r['disposition']=='technical_question' for r in records),
            'topic_only_occurrence_count':sum(r['disposition']=='technical_topic' for r in records),
            'normalized_wording_count':len(set(r['normalized_text'] for r in records)),
            'source_count_with_explicit_question':len({r['source_id'] for r in records if r['disposition']=='technical_question'}),'source_count_with_topic_only_evidence':len(set(ids)-{r['source_id'] for r in records if r['disposition']=='technical_question'}),
            'occurrence_ids':[r['occurrence_id'] for r in records],'representative_questions':examples})
    frequencies.sort(key=lambda x:(-x['source_count'],x['family_id']))
    module_map=defaultdict(list)
    for f in frequencies:
        if f['granularity']=='question_family': module_map[f['module']].append(f)
    modules=[]
    for module,fs in module_map.items():
        sids=sorted(set(s for f in fs for s in f['source_ids']));oids=sorted(set(o for f in fs for o in f['occurrence_ids']))
        modules.append({'module':module,'source_count':len(sids),'source_denominator':len(sources),'source_ids':sids,
                        'occurrence_count':len(oids),'family_count':len(fs),'family_ids':[f['family_id'] for f in fs]})
    modules.sort(key=lambda x:(-x['source_count'],x['module']))
    dispositions=Counter(r['disposition'] for r in occurrences)
    eligible=[r for r in occurrences if r['frequency_eligible']]
    matched_sources={r['source_id'] for r in eligible if r['family_ids']}
    coverage={'schema_version':1,'source_count':len(sources),'batch_count':len(manifest),
      'source_ids':present,'lexical_numbered_records_inside_source_sections':sum(r['original_list_marker'] is not None for r in occurrences),
      'unnumbered_bullet_records':sum(r['original_list_marker'] is None for r in occurrences),
      'batch_editorial_numbered_items_excluded':sum(x['numbered_item_count'] for x in editorial),
      'record_count':len(occurrences),'disposition_counts':dict(sorted(dispositions.items())),
      'eligible_technical_record_count':len(eligible),'normalized_wording_count':len(normalized),'populated_topic_family_count':sum(f['granularity']=='topic' for f in frequencies),'populated_question_family_count':sum(f['granularity']=='question_family' for f in frequencies),
      'sources_with_eligible_technical_records':len(set(r['source_id'] for r in eligible)),
      'sources_with_topic_family_match':len(matched_sources),'sources_with_question_intent_family_match':len(set(s for f in frequencies if f['granularity']=='question_family' for s in f['source_ids'])),
      'sources_without_technical_records':sorted(set(present)-set(r['source_id'] for r in eligible)),
      'sources_without_topic_family_match':sorted(set(present)-matched_sources),
      'eligible_records_without_family':sum(not r['family_ids'] for r in eligible),'eligible_records_without_question_intent_family':sum(not any(f['family_id'] in r['family_ids'] for f in rules if f['granularity']=='question_family') for r in eligible),'sources_without_question_intent_family_match':sorted(set(present)-set(s for f in frequencies if f['granularity']=='question_family' for s in f['source_ids'])),
      'extension_records':sum(r['is_extension'] for r in occurrences),
      'excluded_or_review_record_count':sum(not r['frequency_eligible'] for r in occurrences),
      'limits':['All source text and continuations preserved; list entries are not individual atomic questions.',
        'Topic families are transparent deterministic multi-label classifications, not full human semantic deduplication.',
        'Only literal normalized wording is deduplicated. Frequency counts each independent flow once per family.',
        'Unknown years/dates remain raw; publication dates are not promoted to interview dates.',
        'Old derived paraphrases and analytical assertions are not first-source evidence and do not enter rebuilt data.',
        'A compound question may hit multiple families; family counts must not be added as a total question count.']}
    by_id={r['occurrence_id']:r for r in occurrences}
    for source in sources:
        rs=[by_id[x] for x in source['occurrence_ids']]
        source['eligible_technical_record_count']=sum(r['frequency_eligible'] for r in rs)
        source['disposition_counts']=dict(sorted(Counter(r['disposition'] for r in rs).items()))
    flows=[{'source_id':s['source_id'],'ordered_occurrence_ids':s['occurrence_ids'],
            'order_semantics':'recorded archive order; section labels retain original rounds; not inferred causality'} for s in sources]
    out={
      '01-data/sources.json':dumps({'schema_version':1,'sources':sources}),
      '01-data/question-occurrences.json':dumps({'schema_version':1,'occurrences':occurrences}),
      '01-data/normalized-questions.json':dumps({'schema_version':1,'normalization':'literal normalization only; topic grouping is separate','questions':normalized}),
      '01-data/question-families.json':dumps({'schema_version':1,'deduplication_unit':'independent source flow per explicitly defined question family','families':[f for f in frequencies if f['granularity']=='question_family']}),
      '01-data/raw-manifest.json':dumps({'schema_version':1,'files':manifest}),
      '02-analysis/family-frequency.json':dumps({'schema_version':1,'source_denominator':len(sources),'frequency_unit':'unique_source_flow','families':frequencies}),
      '02-analysis/question-family-frequency.json':dumps({'schema_version':1,'source_denominator':len(sources),'frequency_unit':'unique_source_flow','families':[f for f in frequencies if f['granularity']=='question_family']}),
      '02-analysis/topic-frequency.json':dumps({'schema_version':1,'source_denominator':len(sources),'frequency_unit':'unique_source_flow','families':[f for f in frequencies if f['granularity']=='topic']}),
      '02-analysis/module-frequency.json':dumps({'schema_version':1,'scope':'unique flows in conservative question-intent families only; broad retrieval hints excluded','modules':modules}),
      '02-analysis/coverage.json':dumps(coverage),
      '02-analysis/flow-traceability.json':dumps({'schema_version':1,'flows':flows}),
      '02-analysis/exclusion-register.json':dumps({'schema_version':1,'taxonomy':EXCLUSION_LABELS,
        'excluded_records':[{k:r[k] for k in ('occurrence_id','source_id','raw_path','line_start','disposition','original_text','continuation_text')} for r in occurrences if not r['frequency_eligible']],
        'batch_editorial_sections':editorial}),
    }
    csvio=io.StringIO();w=csv.writer(csvio,lineterminator='\n');w.writerow(['family_id','module','label','granularity','source_count','source_denominator','occurrence_count','normalized_wording_count','source_ids'])
    for f in frequencies:w.writerow([f[k] for k in ['family_id','module','label','granularity','source_count','source_denominator','occurrence_count','normalized_wording_count']]+[';'.join(f['source_ids'])])
    out['02-analysis/family-frequency.csv']=csvio.getvalue()
    lines=['# 全量面经分析','', '[← 面经业务](../README.md) · [统计规则](../03-strategy/normalization-policy.md) · [完整数据说明](../01-data/README.md)','',
      f"输入为 **{len(sources)} 个独立招聘流程、{len(manifest)} 个批次**。多轮与补充不另加来源。没有沿用旧冻结题数。",'',
      '## 数据覆盖与计数边界','',
      f"- 源内记录 {len(occurrences)} 条，其中编号记录 {coverage['lexical_numbered_records_inside_source_sections']}，原始无编号列表记录 {coverage['unnumbered_bullet_records']}",
      f"- 确定技术问法记录 {dispositions['technical_question']}；技术主题短记 {dispositions['technical_topic']}。两者均保留复合问题，不拆造子题",
      f"- 背景、反问、推断、占位或待复核记录 {coverage['excluded_or_review_record_count']} 条，不贡献技术题族频率",
      f"- 保守字面规范化得到 {len(normalized)} 组问法；另有 {coverage['populated_question_family_count']} 个细粒度问题族、{coverage['populated_topic_family_count']} 个较宽主题。三者分开计数",
      f"- {coverage['sources_with_question_intent_family_match']} / {len(sources)} 个流程至少命中细粒度问题意图族；{coverage['eligible_records_without_question_intent_family']} 条技术记录暂未匹配该层规则，原文照常保留",
      '', '细粒度题族仍是问题意图或能力范围的归组，不是已核验的同义原子问题。例如 Memory 实现、更新和召回不能因同属一组而声称是同一道题。字面规范化、题族归组与尚未完成的逐题语义同义审核严格分开。宽主题只是检索线索，不进入知识域频率。当前统计不外推为招聘市场概率。',
      '', '## 细粒度问题族频率','', '| 题族 | 知识域 | 独立流程 | 原始技术记录 |', '|---|---|---:|---:|']
    for f in frequencies:
        if f['granularity']=='question_family':lines.append(f"| {f['label']} (`{f['family_id']}`) | {f['module']} | {f['source_count']}/{len(sources)} | {f['occurrence_count']} |")
    lines+=['','## 主题检索层','', '较宽主题仅用于资料检索，不属于已确认的独立问题频率，也不进入知识域频率；可能与细粒度问题族重叠。见[主题检索覆盖](topic-frequency.json)。']
    lines+=['','## 可追溯接口','', '- [细粒度问题族频率](question-family-frequency.json)：来源集合、命中记录与代表问法',
      '- [包含 granularity 的全量分组 JSON](family-frequency.json) / [CSV](family-frequency.csv)：区分 question_family 与 topic',
      '- [知识域频率](module-frequency.json)：对域内来源取并集，不相加题族频数',
      f'- [覆盖报告](coverage.json)：包含所有 {len(sources)} 个流程及未映射项',
      '- [逐流程顺序](flow-traceability.json)：保留原小节、序号与追问标记；相邻不等于因果',
      '- [排除登记](exclusion-register.json)：逐项保留理由和原文定位',
      '- [完整问法记录](../01-data/question-occurrences.json) / [规范化问法](../01-data/normalized-questions.json)',
      '', '## 重建','', '在仓库根目录执行：','', '```sh',
      'python market/interview-experience/04-scripts/build_interview_analysis.py',
      'python market/interview-experience/04-scripts/build_interview_analysis.py --check',
      'python -m unittest discover -s market/interview-experience/04-scripts -p "test_*.py"','```','']
    out['02-analysis/README.md']='\n'.join(lines)
    # The integrator owns prep prose; update ONLY its explicit evidence markers.
    repo=base.parents[1]
    for module in ('python','fastapi','mysql','redis','backend-engineering','llm-foundation','vector-db','rag','agent','system-design'):
        prep=repo/'interview'/module/'01-高频面试题.md'
        if not prep.exists(): continue
        original=prep.read_text()
        marker=re.compile(r'(<!-- evidence:start -->).*?(<!-- evidence:end -->)',re.S)
        if not marker.search(original): raise ValueError(f'Missing evidence marker: {prep}')
        fs=[f for f in frequencies if f['module']==module and f['granularity']=='question_family'][:5]
        lines=['', '## 全量一手流程中的重点题族', '',
            f'从全部 {len(sources)} 个独立招聘流程重新归组。下列数字为问题意图/能力题族级流程支持数，同一流程出现多轮或多个问法只计一次；它不是单一同义原题的出现次数。复合问题不拆造子题；正文回答是备考教学整理。', '',
            '| 题族 | 独立流程支持 | 原始问法示例 |', '|---|---:|---|']
        for f in fs:
            sample=f['representative_questions'][0]
            raw='../../market/interview-experience/'+sample['raw_path']+'?plain=1#L'+str(sample['line'])
            wording=sample['text'].replace('|',r'\|').replace('\n',' ')
            lines.append(f"| {f['label']} | {f['source_count']}/{len(sources)} | [{sample['source_id']}：{wording}]({raw}) |")
        lines.extend(['', '[完整题族规则与频率](../../market/interview-experience/02-analysis/README.md) · [逐题追溯数据](../../market/interview-experience/01-data/question-occurrences.json)', ''])
        rendered=marker.sub(lambda m:m[1]+'\n'.join(lines)+m[2],original)
        out['../../'+prep.relative_to(repo).as_posix()]=rendered
    return out,coverage

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs,summary=build();stale=[]
    for rel,text in outputs.items():
        path=BUSINESS/rel
        if args.check:
            if not path.exists() or path.read_text()!=text:stale.append(rel)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    if stale:print('Stale generated artifacts:\n'+'\n'.join(stale),file=sys.stderr);return 1
    print(f"{'Checked' if args.check else 'Built'} {len(outputs)} artifacts; {summary['source_count']} source flows; {summary['eligible_technical_record_count']} eligible technical records; {summary['normalized_wording_count']} literal wording groups.")
    return 0
if __name__=='__main__':raise SystemExit(main())
