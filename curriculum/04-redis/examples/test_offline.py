"""Offline document, RESP parser, and teaching-model checks. NOT Redis execution."""
import ast
import binascii
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from reader import DOCS,MODULE,RedisReplyError,assert_reply,export,labs,scripts
from protocol import encode,read_reply

class SourceChecks(unittest.TestCase):
    def test_all_chapters_and_learning_sections(self):
        files=sorted(DOCS.glob('*.md'));self.assertEqual(len(files),18)
        for i,p in enumerate(files,1):
            text=p.read_text(encoding='utf-8');self.assertTrue(text.startswith(f'# {i:02d}｜'),p.name)
            self.assertEqual(len(re.findall(r'^# ',text,re.M)),1,p.name)
            for section in ['## 本章小结','## 🎯 面试怎么回答','## 易错点','## 本章自测','## 知识回看与权威资料']:self.assertIn(section,text,p.name)
            self.assertEqual(text.count('<details>'),text.count('</details>'),p.name)
            quiz=text.split('## 本章自测')[1].split('## 知识回看')[0];self.assertEqual(quiz.count('<details>'),3,p.name)
            self.assertNotIn('<details open',text)
    def test_fixture_shape_and_unique_names(self):
        cases=labs();self.assertGreaterEqual(len(cases),20)
        for item in cases:self.assertEqual(len(item.commands),len(item.expected));self.assertTrue(all(cmd for cmd in item.commands))
    def test_automated_commands_do_not_change_instance_configuration(self):
        forbidden={'FLUSHALL','FLUSHDB','CONFIG','MODULE','SHUTDOWN','REPLICAOF','SLAVEOF','ACL','MIGRATE'}
        for item in labs():
            for command in item.commands:
                self.assertNotIn(command[0].upper(),forbidden)
                if command[0].upper() not in {'PING','MULTI','EXEC','DISCARD','UNWATCH'}:self.assertTrue(any(arg.startswith('lab:') for arg in command),command)
    def test_expected_reply_schema(self):
        def visit(value):
            if isinstance(value,dict):
                self.assertEqual(len(value),1);name=next(iter(value));self.assertIn(name,{'error','between','set','pairs'})
                if name=='between':self.assertLessEqual(*value[name])
            elif isinstance(value,list):
                for v in value:visit(v)
            else:self.assertTrue(value is None or type(value) in (str,int))
        for item in labs():
            for x in item.expected:visit(x)
    def test_main_reading_is_application_language_neutral(self):
        for p in DOCS.glob('*.md'):
            text=p.read_text(encoding='utf-8')
            self.assertNotIn('```python',text,p.name);self.assertNotIn('```java',text,p.name);self.assertNotIn('docker run',text,p.name)
    def test_explanatory_lua_has_explicit_bounded_contract(self):
        # Text-level guard only: this does not parse Lua or execute Redis.
        snippets = []
        for page in DOCS.glob('*.md'):
            text = page.read_text(encoding='utf-8')
            blocks = list(re.finditer(r'```lua\n(.*?)\n```', text, re.S))
            for block in blocks:
                self.assertTrue(text[:block.start()].rstrip().endswith('<!-- teaching-lua: bounded -->'))
                code = block[1]
                self.assertNotRegex(code, r'\b(?:for|while|repeat)\b')
                self.assertIn('#KEYS ~= 1', code)
                self.assertIn('#ARGV ~= 1', code)
                self.assertIn('1000000', code)
                calls = re.findall(r"redis\.call\('([^']+)'", code)
                self.assertEqual(calls, ['GET', 'DECRBY'])
                self.assertLess(code.index("redis.error_reply('invalid stock')"), code.index("redis.call('DECRBY'"))
                snippets.append(code)
        self.assertEqual(len(snippets), 1)

    def test_chapter_registry_matches_navigation(self):
        registry=json.loads((MODULE/'chapters.json').read_text(encoding='utf-8'));self.assertEqual([x['number'] for x in registry],list(range(1,19)))
        for item in registry:
            p=MODULE/item['path'];self.assertTrue(p.exists());self.assertIn(item['title'],p.read_text(encoding='utf-8').splitlines()[0])
    def test_basic_examples_and_detailed_labs_both_remain_checked(self):
        cases=labs();self.assertTrue(any(x.name.startswith('core_') for x in cases))
        detailed=[x for x in cases if x.source.name=='labs.md'];self.assertEqual(len(detailed),21);self.assertEqual(sum(len(x.commands) for x in detailed),119)
    def test_lua_identifiers_and_bounded_inputs_present(self):
        values=scripts();self.assertEqual(set(values),{'decrease','release_owner','fixed_window','sliding_window'})
        for name in ['decrease','fixed_window','sliding_window']:self.assertIn('tonumber',values[name]);self.assertIn('math.floor',values[name])
    def test_export_uses_exact_utf8_bytes_on_every_platform(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            export(destination)
            for name, code in scripts().items():
                self.assertEqual((destination/(name+'.lua')).read_bytes(), code.encode('utf-8'))
            self.assertTrue(all(b'\r\n' not in page.read_bytes() for page in destination.iterdir()))
            export(destination)  # The no-overwrite byte guard must accept its own output.

    def test_export_does_not_overwrite_changed_file(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d);out=export(path);self.assertGreater(out['files'],20);export(path)
            (path/'decrease.lua').write_text('unrelated user work')
            with self.assertRaises(ValueError):export(path)
            self.assertEqual((path/'decrease.lua').read_text(),'unrelated user work')
    def test_error_example_retains_partial_success_assertions(self):
        case=next(x for x in labs() if x.name=='transaction_error')
        self.assertTrue(any(isinstance(x,list) and any(isinstance(v,dict) and 'error' in v for v in x) for x in case.expected))
    def test_hash_views_use_order_independent_expectations(self):
        case=next(x for x in labs() if x.name=='hash_views');self.assertIn('pairs',case.expected[1]);self.assertIn('set',case.expected[2])
    def test_local_document_links(self):
        from urllib.parse import unquote,urlsplit
        missing=[]
        for p in MODULE.rglob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
                parsed=urlsplit(link)
                if parsed.scheme or not parsed.path:continue
                target=(p.parent/unquote(parsed.path)).resolve()
                if target.is_relative_to(MODULE.resolve()) and not target.exists():missing.append((p.name,link))
        self.assertFalse(missing,missing)

class ProtocolUnitChecks(unittest.TestCase):
    def test_encode_preserves_empty_and_unicode(self):
        self.assertEqual(encode(['SET','k','']),b'*3\r\n$3\r\nSET\r\n$1\r\nk\r\n$0\r\n\r\n')
        self.assertIn(b'$6\r\n'+ '你好'.encode()+b'\r\n',encode(['SET','k','你好']))
    def test_string_vs_integer(self):
        self.assertEqual(read_reply(io.BytesIO(b'$2\r\n12\r\n')),'12');self.assertEqual(read_reply(io.BytesIO(b':12\r\n')),12)
    def test_empty_vs_null(self):
        self.assertEqual(read_reply(io.BytesIO(b'$0\r\n\r\n')),'');self.assertIsNone(read_reply(io.BytesIO(b'$-1\r\n')))
    def test_null_array(self):self.assertIsNone(read_reply(io.BytesIO(b'*-1\r\n')))
    def test_nested_transaction_error_value(self):
        r=read_reply(io.BytesIO(b'*3\r\n+OK\r\n-WRONGTYPE bad type\r\n:1\r\n'));assert_reply(r,['OK',{'error':'WRONGTYPE'},1])
    def test_truncated_bulk_rejected(self):
        with self.assertRaises(ConnectionError):read_reply(io.BytesIO(b'$4\r\nab\r\n'))
    def test_invalid_type_rejected(self):
        with self.assertRaises(ValueError):read_reply(io.BytesIO(b'?bad\r\n'))
    def test_reply_matcher(self):
        assert_reply(['b','a'],{'set':['a','b']});assert_reply(['v','2','k','1'],{'pairs':{'k':'1','v':'2'}});assert_reply(599,{'between':[590,600]})
        with self.assertRaises(AssertionError):assert_reply('1',1)
        with self.assertRaises(AssertionError):assert_reply(0,{'between':[1,2]})
    def test_oversized_header_rejected(self):
        with self.assertRaises(ValueError):read_reply(io.BytesIO(b'$20000000\r\n'))

class ExplicitTeachingModels(unittest.TestCase):
    """Only arithmetic/state assumptions from the prose; not an implementation of Redis."""
    def test_rtt_estimate(self):self.assertAlmostEqual(100*(2+0.05),205)
    def test_two_cache_levels_denominators(self):
        total,l1,l2=1000,700,240;self.assertEqual(total-l1-l2,60);self.assertEqual((l1+l2)/total,.94);self.assertEqual(l2/(total-l1),.8)
    def test_session_absolute_limit(self):self.assertEqual(min(30,160-150),10)
    def test_retry_total(self):self.assertEqual(1000*(1+3),4000)
    def test_recent_payload_capacity(self):self.assertEqual(5000*30*400,60000000)
    def test_token_refill(self):self.assertEqual(min(5,1+2*1.5)-3,1)
    def test_window_left_boundary(self):
        scores=[1000,1500];self.assertEqual([x for x in scores if 1999-1000<x<=1999],[1000,1500]);self.assertEqual([x for x in scores if 2000-1000<x<=2000],[1500])
    def test_old_owner_counterexample(self):
        holder='A';holder='B';old_task_running=True;self.assertNotEqual(holder,'A');self.assertTrue(old_task_running)
    def test_fencing_only_after_new_epoch_observed(self):
        latest=42;self.assertFalse(41>=latest);latest=40;self.assertTrue(41>=latest)
    def test_stale_refill_counterexample(self):
        db='old';read_result=db;db='new';cache=None;cache=read_result;self.assertEqual(db,'new');self.assertEqual(cache,'old')
    def test_sentinel_detection_not_election_majority(self):
        sentinels,isolated,quorum=5,2,2;self.assertTrue(isolated>=quorum);self.assertFalse(isolated>=sentinels//2+1)
    def test_cluster_tag_model(self):
        def slot(key):
            begin=key.find(b'{');end=key.find(b'}',begin+1) if begin>=0 else -1
            part=key[begin+1:end] if end>begin+1 else key
            return binascii.crc_hqx(part,0)%16384
        self.assertEqual(slot(b'order:{u1}:a'),slot(b'quota:{u1}:b'));self.assertEqual(slot(b'foo'),12182)
        self.assertEqual(slot(b'x{}y{z}'),binascii.crc_hqx(b'x{}y{z}',0)%16384)

if __name__=='__main__':unittest.main(verbosity=2)
