"""Evidence preservation, conservative classification and frequency regression suite."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from collections import Counter

import build_interview_analysis as b

class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs,cls.summary=b.build()
        cls.contract=json.loads((b.BUSINESS/'03-strategy/corpus-contract.json').read_text())
        cls.sources=json.loads(cls.outputs['01-data/sources.json'])['sources']
        cls.records=json.loads(cls.outputs['01-data/question-occurrences.json'])['occurrences']
        cls.families=json.loads(cls.outputs['02-analysis/family-frequency.json'])['families']
        cls.byid={x['occurrence_id']:x for x in cls.records}
    def test_complete_source_contract(self):
        self.assertEqual([s['source_id'] for s in self.sources],self.contract['source_ids'])
        self.assertEqual(self.summary['batch_count'],len(self.contract['raw_sha256']))
    def test_all_bytes_match_input_contract(self):
        contract=json.loads((b.BUSINESS/'03-strategy/corpus-contract.json').read_text())
        for path,digest in contract['raw_sha256'].items():
            self.assertEqual(hashlib.sha256((b.BUSINESS/path).read_bytes()).hexdigest(),digest)
    def test_preserved_source_section_hashes(self):
        proof=json.loads((b.BUSINESS/'01-data/source-provenance.json').read_text())['sections']
        self.assertEqual(len(proof),len(self.contract['source_section_sha256']))
        contract=json.loads((b.BUSINESS/'03-strategy/corpus-contract.json').read_text())['source_section_sha256']
        actual={f"{s['source_id']}:{Path(p['raw_path']).stem}:{p['original_line_start']}":p['source_section_sha256'] for s in self.sources for p in s['raw_sections']}
        self.assertEqual(actual,contract)
    def test_module_frequency_excludes_broad_retrieval_hints(self):
        modules=json.loads(self.outputs['02-analysis/module-frequency.json'])['modules']
        for module in modules:
            fs=[f for f in self.families if f['module']==module['module'] and f['granularity']=='question_family']
            self.assertEqual(module['source_ids'],sorted({sid for f in fs for sid in f['source_ids']}))
    def test_all_source_section_text_is_exact(self):
        for source in self.sources:
            self.assertTrue(source['urls'],source['source_id'])
            for section in source['raw_sections']:
                lines=(b.BUSINESS/section['raw_path']).read_text().splitlines(keepends=True)
                self.assertEqual(section['text'],''.join(lines[section['line_start']-1:section['line_end']]))
    def test_every_record_retains_exact_lines(self):
        for r in self.records:
            lines=(b.BUSINESS/r['raw_path']).read_text().splitlines(keepends=True)
            self.assertEqual(r['raw_text'],''.join(lines[r['line_start']-1:r['line_end']]).rstrip('\r\n'))
    def test_every_numbered_list_item_accounted_for(self):
        total=sum(bool(b.NUMBERED.match(l)) for p in (b.BUSINESS/'01-data/raw').glob('*.md') for l in p.read_text().splitlines())
        self.assertEqual(total,self.summary['lexical_numbered_records_inside_source_sections']+self.summary['batch_editorial_numbered_items_excluded'])
    def test_source_order_and_unique_record_ids(self):
        self.assertEqual(len(self.byid),len(self.records))
        for source in self.sources:
            records=[self.byid[x] for x in source['occurrence_ids']]
            self.assertEqual([r['source_sequence'] for r in records],list(range(1,len(records)+1)))
    def test_s288_extension_count(self):
        records=[r for r in self.records if r['is_extension']]
        self.assertEqual(len(records),10)
        self.assertEqual({r['source_id'] for r in records},{'S288'})
        self.assertTrue(all(r['frequency_eligible'] for r in records))
    def test_s387_ranges_and_inferences_do_not_expand(self):
        records=[r for r in self.records if r['source_id']=='S387']
        self.assertEqual(len(records),106)
        self.assertEqual(sum(r['disposition']=='undisclosed' for r in records),4)
        inferred=[r for r in records if r['disposition']=='author_inference']
        self.assertEqual(len(inferred),2)
        self.assertTrue(all(not r['frequency_eligible'] for r in inferred))
    def test_s388_ambiguous_react_is_not_semantically_invented(self):
        r=self.byid['S388:batch-38:L00298']
        self.assertTrue(r['frequency_eligible'])
        self.assertFalse(set(r['family_ids']) & {'AGENT-LOOP','Q-AGENT-LOOP','FRONTEND-WEB','Q-FRONTEND-REACT'})
    def test_s389_candidate_review_is_not_interviewer_question(self):
        r=self.byid['S389:batch-38:L00401']
        self.assertEqual(r['disposition'],'candidate_question')
        self.assertFalse(r['family_ids'])
    def test_explicit_continuation_questions_contribute_without_splitting(self):
        r=self.byid['S359:batch-37:L03173']
        self.assertEqual(len(r['follow_up_texts']),2)
        self.assertIn('PY-ASYNC',r['family_ids'])
        rag=self.byid['S359:batch-37:L03177']
        self.assertIn('Q-RAG-UPDATE',rag['family_ids'])
        tool=self.byid['S359:batch-37:L03188']
        self.assertIn('AGENT-RECOVERY',tool['family_ids'])
        self.assertTrue(all('原文边界' not in f['text'] for f in tool['follow_up_texts']))
    def test_s391_original_bullets_are_indexed(self):
        records=[r for r in self.records if r['source_id']=='S391']
        self.assertEqual(len(records),21)
        self.assertTrue(all(r['original_list_marker'] is None for r in records))
        self.assertTrue(any('RRF算法' in r['original_text'] and r['frequency_eligible'] for r in records))
    def test_unknown_dates_not_filled_from_publication(self):
        s=next(x for x in self.sources if x['source_id']=='S399')
        self.assertTrue(any('年份未明示' in x['text'] for x in s['metadata_lines']))
        self.assertIsNone(s['heading_date_raw'])
    def test_family_frequency_recomputed_from_occurrences(self):
        for f in self.families:
            rs=[self.byid[x] for x in f['occurrence_ids']]
            self.assertTrue(all(r['frequency_eligible'] for r in rs))
            ids=sorted({r['source_id'] for r in rs})
            self.assertEqual(f['source_ids'],ids)
            self.assertEqual(f['source_count'],len(ids))
            self.assertEqual(f['source_denominator'],len(self.contract['source_ids']))
            self.assertEqual(f['occurrence_count'],len(rs))
            self.assertEqual(f['source_count_with_explicit_question']+f['source_count_with_topic_only_evidence'],len(ids))
    def test_all_memberships_follow_current_positive_and_negative_rules(self):
        for r in self.records:
            expected=b.match_record_families(r) if r['frequency_eligible'] else []
            self.assertEqual(r['family_matches'],expected)
    def test_statistics_use_only_current_first_source_records(self):
        self.assertTrue(all(r['source_id'] in {s['source_id'] for s in self.sources} for r in self.records))
    def test_normalized_groups_preserve_all_eligible_occurrences(self):
        qs=json.loads(self.outputs['01-data/normalized-questions.json'])['questions']
        assigned=[oid for q in qs for oid in q['occurrence_ids']]
        eligible=[r['occurrence_id'] for r in self.records if r['frequency_eligible']]
        self.assertEqual(sorted(assigned),sorted(eligible))
        self.assertEqual(len({q['question_id'] for q in qs}),len(qs))
    def test_root_prep_updates_only_explicit_markers(self):
        import re
        for rel,generated in self.outputs.items():
            if not rel.startswith('../../interview/'):continue
            old=(b.BUSINESS/rel).read_text()
            strip=lambda s:re.sub(r'<!-- evidence:start -->.*?<!-- evidence:end -->','<evidence>',s,flags=re.S)
            self.assertEqual(strip(old),strip(generated))
    def test_generated_artifacts_current(self):
        for path,text in self.outputs.items():self.assertEqual((b.BUSINESS/path).read_text(),text,path)
    def test_rebuild_deterministic(self):
        again,_=b.build()
        self.assertEqual(self.outputs,again)

class RuleTests(unittest.TestCase):
    def families(self,text,section=''):return {x['family_id'] for x in b.match_families(text,section)}
    def test_math_and_code_not_merged(self):
        for a,c in [('a*b','ab'),('x_y','xy'),('A','a'),('`x *= 2`','`x = 2`')]:self.assertNotEqual(b.normalize(a),b.normalize(c))
    def test_prefix_is_not_a_new_question(self):
        self.assertEqual(b.normalize('（原题2(1)）MySQL 索引是什么？'),b.normalize('MySQL 索引是什么？'))
    def test_candidate_label_survives_prefix_stripping(self):
        self.assertEqual(b.classify('（原题反问2）复杂链超时如何降级','',''),'candidate_question')
    def test_inference_and_placeholder_excluded(self):
        self.assertEqual(b.classify('【作者推断】订单索引如何设计','',''),'author_inference')
        self.assertEqual(b.classify('（原题1-24）【占位，未披露题面】项目深挖','',''),'undisclosed')
    def test_english_keywords_match_next_to_chinese(self):
        self.assertIn('Q-BE-TCP',self.families('TCP与UDP对比'))
        self.assertIn('Q-RAG-RRF',self.families('RRF计算过程'))
    def test_section_cannot_create_positive_hits(self):
        fs=self.families('MySQL索引失效','Agent框架与记忆')
        self.assertFalse(any(x.startswith('AGENT') or x.startswith('Q-AGENT') for x in fs))
    def test_linked_list_reorder_not_rerank(self):
        self.assertFalse(self.families('Coding：按头尾交替规则重排单链表')&{'RAG-RERANK','Q-RAG-RERANK'})
        self.assertIn('Q-RAG-RERANK',self.families('RAG检索结果如何重排'))
    def test_retrieval_not_eval(self):
        self.assertNotIn('Q-AGENT-EVAL',self.families('主流Agent Architecture、RAG Dense/Sparse Retrieval如何组合'))
    def test_return_text_not_palindrome(self):
        fs=self.families('文档中图片如何解析，避免只返回文字而丢失视觉信息')
        self.assertNotIn('Q-CODING-SUBSTRING',fs)
        self.assertIn('Q-CODING-SUBSTRING',self.families('最长回文子串'))
    def test_penetration_not_io(self):
        self.assertNotIn('Q-REDIS-THREAD',self.families('Redis Cache Penetration/Breakdown/Avalanche如何治理'))
        self.assertIn('Q-REDIS-THREAD',self.families('Redis I/O多线程与单线程命令执行'))
    def test_db_index_invalidation_not_rag_update(self):
        self.assertFalse(self.families('MySQL Index为什么快、什么时候失效')&{'RAG-UPDATE','Q-RAG-UPDATE'})
    def test_double_write_not_redis_without_cache(self):
        self.assertNotIn('Q-REDIS-CONSISTENCY',self.families('买家卖家双写表如何处理分布式事务和一致性'))
    def test_mq_transaction_not_mysql(self):
        self.assertNotIn('MYSQL-TX-BASICS',self.families('RocketMQ Transactional Message如何工作'))
    def test_database_logs_not_observability(self):
        self.assertNotIn('BE-OBSERVABILITY',self.families('redo log与binlog的两阶段提交为何需要'))
    def test_fiber_runtime_not_react(self):
        self.assertNotIn('Q-FRONTEND-REACT',self.families('Fiber为什么快，低/零内存分配机制是什么'))
    def test_embedding_not_quantization(self):
        self.assertNotIn('LLM-INFERENCE',self.families('RAG Chunk Embedding Retrieval Generation链路'))
        self.assertIn('LLM-INFERENCE',self.families('模型量化及KV Cache加速推理'))
    def test_agent_isolation_not_database_isolation(self):
        self.assertNotIn('Q-MYSQL-ISOLATION',self.families('AST Static Analysis与Sub-Agent Isolation如何配合'))
    def test_os_memory_and_context_not_agent(self):
        self.assertFalse(self.families('Java Memory Model与内存屏障')&{'AGENT-MEMORY','Q-AGENT-MEMORY'})
        self.assertNotIn('AGENT-CONTEXT',self.families('进程线程与context switch上下文切换'))
    def test_bounded_queue_capacity_not_service_scale(self):
        self.assertNotIn('Q-SD-SCALE',self.families('Coding：实现有最大容量的Blocking Queue'))
    def test_framework_mention_is_not_selection(self):
        self.assertNotIn('Q-AGENT-FRAMEWORK',self.families('自己修改的LangGraph Project中Memory System怎样设计'))
        self.assertIn('Q-AGENT-FRAMEWORK',self.families('为何选择LangGraph而不是自研Agent Runtime'))
    def test_memory_heap_is_not_topk_heap(self):
        self.assertNotIn('Q-CODING-TOPK',self.families('OS中Stack与Heap的差异是什么？'))
    def test_dataset_sampling_is_not_decoding_sampling(self):
        self.assertNotIn('Q-LLM-SAMPLING',self.families('Agent自进化所需数据怎样采样/收集？'))
    def test_redis_checkpoint_is_not_rdb_aof(self):
        self.assertNotIn('Q-REDIS-PERSIST',self.families('Redis预扣成功但DB写入失败时，一致性怎样恢复？'))
    def test_injection_requires_security_context(self):
        for text in ['FastAPI Middleware vs Dependency Injection','Spring Annotation依赖注入','MyBatis SQL Injection','Knowledge Card注入System Prompt','Memory注入机制']:
            self.assertFalse(self.families(text)&{'Q-AGENT-SANDBOX','AGENT-SECURITY'},text)
        self.assertIn('Q-AGENT-SANDBOX',self.families('Prompt Injection攻击如何防护'))
    def test_candidate_question_suffix(self):
        self.assertEqual(b.classify('团队Agent/Sandbox/安全/云监控占比反问','',''),'candidate_question')
    def test_unrelated_frameworks_are_not_agent_frameworks(self):
        for text in ['Gin与Kratos等Web/Microservice Framework怎样选型','项目为什么选择Spring或Socket，协议Framework取舍是什么','常见Frontend Framework与工程选型怎样理解']:
            self.assertNotIn('Q-AGENT-FRAMEWORK',self.families(text))
    def test_memory_fragmentation_not_agent_memory(self):
        self.assertNotIn('Q-AGENT-MEMORY',self.families('Memory Fragmentation怎样产生和治理'))
    def test_generic_threading_is_not_python(self):
        self.assertNotIn('PY-ASYNC',self.families('什么场景值得使用Multi-threading'))
    def test_nonredis_caches_not_redis(self):
        for text in ['KV Cache如何加速推理','Spring循环依赖三级缓存','短期记忆如何淘汰；LRU是否打乱对话顺序']:
            self.assertFalse(self.families(text)&{'REDIS-CACHE','REDIS-EVICTION'})
    def test_sql_select_is_not_os_select(self):
        for text in ['事务中的SELECT/UPDATE/INSERT','SELECT *与SELECT A,B,C','WHERE/SELECT索引']:
            self.assertNotIn('BE-OS',self.families(text))
    def test_memory_sliding_window_is_not_network(self):
        self.assertNotIn('BE-NETWORK',self.families('Memory滑动窗口摘要与压缩'))
    def test_event_loop_is_not_agent_loop(self):
        for text in ['FastAPI await与Event Loop','async/await event loop','Coding数组死循环']:
            self.assertFalse(self.families(text)&{'AGENT-LOOP','Q-AGENT-LOOP'})
    def test_generic_gc_does_not_imply_java(self):
        for text in ['Python与C++内存管理垃圾回收','V8 GC与MySQL和IVF']:
            self.assertFalse(self.families(text)&{'BE-JAVA','Q-BE-JVM'})
    def test_retrieval_ranking_does_not_imply_coding(self):
        for text in ['Retrieval/Ranking选型','RAG Chunk/Ranking/Eval','RRF融合排序','多路召回后排序重排','OS中Heap与Stack区别']:
            self.assertNotIn('CODING-ALGORITHM',self.families(text))
    def test_apt_decorator_is_not_python(self):
        self.assertFalse(self.families('APT Plugin/Decorator统一Logging和Error Collection')&{'PY-ITERATION','Q-PY-DECORATOR'})
    def test_computer_memory_needs_positive_agent_memory_evidence(self):
        for text in ['OS Memory Reclaim','JVM Memory Area','Go Memory Escape Leak PPROF','CPU到Memory访问链路','Redis Memory淘汰','StackOverflow/OutOfMemory','PagedAttention推理Memory Management','Physical与Virtual Memory文件处理']:
            self.assertFalse(self.families(text)&{'AGENT-MEMORY','Q-AGENT-MEMORY'},text)
        self.assertIn('Q-AGENT-MEMORY',self.families('Agent长期Memory如何召回'))
    def test_explicit_interview_feedback_not_question(self):
        self.assertEqual(b.classify('面试反馈：项目认可但工程化表达不清，应怎样证明做过','',''),'author_answer')
    def test_oom_does_not_match_bloom_or_room(self):
        for text in ['Bloom Filter原理','bookRoom与allocateRoom','Room状态']:
            self.assertNotIn('BE-DEPLOY',self.families(text))
        self.assertIn('BE-DEPLOY',self.families('OOM如何排查'))
    def test_ast_does_not_match_fast_or_elasticsearch(self):
        for text in ['FastAPI接口','FastMCP协议','Fail-fast策略','Elasticsearch检索','Fastjson漏洞']:
            self.assertNotIn('OTHER-TECHNICAL',self.families(text))
        self.assertIn('OTHER-TECHNICAL',self.families('AST与LSP代码解析'))
    def test_reactor_is_not_react(self):
        self.assertNotIn('Q-AGENT-LOOP',self.families('IO Multiplexing NIO与Reactor的关系'))
    def test_sla_is_not_substring_of_translation_or_island(self):
        for text in ['MCP Protocol Translation','Coding Maximum Area of Island']:
            self.assertNotIn('SD-TRADEOFF',self.families(text))
    def test_user_profile_is_not_profiler(self):
        self.assertNotIn('BE-OBSERVABILITY',self.families('Long-term Memory提炼Structured User Profile并存入Vector DB'))
    def test_latin_boundary_guard_is_central_and_chinese_safe(self):
        cases=[('AST','FastAPI','AST语法树'),('OOM','Bloom Filter','发生OOM异常'),('sla','Island','SLA约束'),('react','Reactor','ReAct原理'),('eval','Retrieval','Eval评测'),('io','Penetration','IO多路复用'),('tool','toolkit','Tool调用'),('profile','profiler','User Profile')]
        for term,negative,positive in cases:
            self.assertIsNone(b.rule_match(term,negative),(term,negative))
            self.assertIsNotNone(b.rule_match(term,positive),(term,positive))
    def test_process_notes_are_not_operating_system_processes(self):
        self.assertNotIn('BE-CONCURRENCY',self.families('Task Summary/File Summary/Process Notes'))
    def test_apt_tool_is_not_agent_tool_protocol(self):
        self.assertNotIn('AGENT-TOOLS',self.families('APT/Annotation Processing Tool Framework'))
    def test_latin_morphology_preserves_true_positive_terms(self):
        cases=[('tool.?call','Tool Calling'),('tool.?call','ToolCalling'),('function.?call','Function Calling'),('rerank','Reranker'),('rerank','Reranking'),('tool','Tools'),('skill','Skills'),('embedding','Embeddings'),('framework','Frameworks'),('thread','Threads'),('process','Processes')]
        for pattern,text in cases:self.assertIsNotNone(b.rule_match(pattern,text),(pattern,text))
        self.assertIn('Q-AGENT-TOOLCALL',self.families('Agent Tool Calling有哪些实现方式'))
        self.assertIn('Q-AGENT-TOOLCALL',self.families('Function Calling的完整机制是什么'))
        self.assertIn('Q-RAG-RERANK',self.families('BGE Reranker精排模型如何选择'))
    def test_common_positive_inflections_and_named_compounds(self):
        cases=[('RAG Text/Semantic Chunking','RAG-CHUNK'),('Consistent Hashing','BE-ARCHITECTURE'),('Rate Limiting算法','Q-BE-RATELIMIT'),('RabbitMQ可靠投递','Q-BE-MQ'),('MySQL Slow Query怎样优化','Q-MYSQL-EXPLAIN'),('MySQL索引优化和慢查询','Q-MYSQL-EXPLAIN'),('metrics/logs/traces','BE-OBSERVABILITY')]
        for text,family in cases:self.assertIn(family,self.families(text),(text,family))
    def test_bad_early_substring_cannot_hide_later_valid_alternative(self):
        self.assertEqual(b.rule_match('sql.*优化|slow query','MySQL Slow Query怎样优化')[0],'Slow Query')
    def test_every_declared_rule_has_a_working_positive_fixture(self):
        fixtures=json.loads((b.BUSINESS/'03-strategy/matching-fixtures.json').read_text())['positive_fixtures']
        self.assertEqual({f['family_id'] for f in fixtures},{r['family_id'] for r in b.FAMILY_RULES})
        for fixture in fixtures:
            self.assertIn(fixture['family_id'],self.families(fixture['text'],fixture['context']),fixture['family_id'])
    def test_every_declared_alias_preserves_chinese_adjacent_positive(self):
        for alias,(regex,concept) in zip(b.MATCHING_CONFIG['matching_aliases'],b.ALIASES):
            self.assertIsNotNone(regex.search(alias['term']+'如何实现'),alias)
            self.assertIsNone(regex.search('x'+alias['term']+'x'),alias)
            self.assertIn(concept,b.matching_text(alias['term']+'如何实现'))
    def test_parser_separates_source_extension_and_batch_observations(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw=Path(tmp)/'01-data/raw';raw.mkdir(parents=True)
            (raw/'batch-01.md').write_text('# Batch\n## S001 公司｜岗位｜一面｜HUMAN-A\n来源：https://example.com\n1. MySQL索引是什么？\n# 批次观察\n1. Agent很热门\n## Existing-process extension — S001 不新增ID\n1. Redis如何设计？\n# Final\n1. 原则总结\n')
            sources,records,_,editorial=b.parse_corpus(raw)
            self.assertEqual(len(sources),1);self.assertEqual(len(records),2)
            self.assertEqual(sum(x['numbered_item_count'] for x in editorial),2)
            self.assertTrue(records[-1]['is_extension'])

if __name__=='__main__':unittest.main()
