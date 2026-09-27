"""Run source-extracted cases against a fresh, owned Redis 8.10.2 process.

Requires a local redis-server executable. Never connects to an existing server.
Missing prerequisites are reported as NOT RUN and return a nonzero exit status.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import json
from pathlib import Path
import re
import shutil
import socket
import subprocess
import tempfile
import time
import traceback
from protocol import Client
from reader import VERSION,RedisReplyError,assert_reply,labs,scripts


@contextmanager
def own_server(executable, directory, extra=()):
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1',0));port=reservation.getsockname()[1]
    logfile=open(Path(directory)/'redis.log','ab')
    command=[executable,'--bind','127.0.0.1','--port',str(port),'--protected-mode','yes',
             '--save','','--appendonly','no','--dir',str(directory),'--dbfilename','reader.rdb',
             '--loglevel','warning',*extra]
    process=subprocess.Popen(command,cwd=directory,stdout=logfile,stderr=subprocess.STDOUT)
    try:
        ready=False
        for _ in range(100):
            if process.poll() is not None:break
            try:
                with Client(port,0.2) as c:
                    if c.execute('PING')=='PONG':ready=True;break
            except (OSError,ValueError):pass
            time.sleep(0.03)
        if not ready:raise RuntimeError('Owned teaching Redis failed to start; inspect its temporary log')
        with Client(port) as c:
            info=c.execute('INFO','server')
            found=re.search(r'^process_id:(\d+)\r?$',info,re.M)
            if not found or int(found[1])!=process.pid:raise RuntimeError('Refusing server not owned by this runner')
        yield port,process
    finally:
        if process.poll() is None:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
        logfile.close()


def advanced_cases(port,emit):
    code=scripts()
    with Client(port) as a,Client(port) as b:
        def check(name,fn):
            try:fn();emit(name,True,None)
            except Exception as exc:emit(name,False,repr(exc));raise
        def watch_conflict():
            assert_reply(a.execute('SET','lab:live:watch',10),'OK');assert_reply(a.execute('WATCH','lab:live:watch'),'OK')
            assert_reply(a.execute('GET','lab:live:watch'),'10');assert_reply(b.execute('SET','lab:live:watch',8),'OK')
            assert_reply(a.execute('MULTI'),'OK');assert_reply(a.execute('SET','lab:live:watch',9),'QUEUED')
            assert_reply(a.execute('EXEC'),None);assert_reply(a.execute('GET','lab:live:watch'),'8')
        check('two_clients_watch_conflict',watch_conflict)
        def queue_error():
            a.execute('MULTI');assert isinstance(a.execute('SET','lab:live:bad'),RedisReplyError)
            assert_reply(a.execute('SET','lab:live:not_applied',1),'QUEUED');assert_reply(a.execute('EXEC'),{'error':'EXECABORT'})
            assert_reply(a.execute('GET','lab:live:not_applied'),None)
        check('queue_error_aborts_transaction',queue_error)
        def lua_error():
            program="redis.call('SET',KEYS[1],'kept'); return redis.call('INCR',KEYS[1])"
            assert isinstance(a.execute('EVAL',program,1,'lab:live:lua_error'),RedisReplyError)
            assert_reply(a.execute('GET','lab:live:lua_error'),'kept')
        check('lua_error_does_not_rollback',lua_error)
        def decrease():
            a.execute('SET','lab:live:stock',5);assert_reply(a.execute('EVAL',code['decrease'],1,'lab:live:stock',3),2)
            assert_reply(a.execute('EVAL',code['decrease'],1,'lab:live:stock',3),-2)
            assert isinstance(a.execute('EVAL',code['decrease'],1,'lab:live:stock',-1),RedisReplyError)
            assert_reply(a.execute('GET','lab:live:stock'),'2')
        check('bounded_decrease_source_script',decrease)
        def release_owner():
            a.execute('SET','lab:live:lock','bob','PX',60000);assert_reply(a.execute('EVAL',code['release_owner'],1,'lab:live:lock','alice'),0)
            assert_reply(a.execute('GET','lab:live:lock'),'bob');assert_reply(a.execute('EVAL',code['release_owner'],1,'lab:live:lock','bob'),1)
        check('conditional_release_source_script',release_owner)
        def fixed():
            for allowed,count in [(1,1),(1,2),(0,2)]:
                r=a.execute('EVAL',code['fixed_window'],1,'lab:live:fixed',2,60000)
                assert_reply(r[:2],[allowed,count]);assert_reply(r[2],{'between':[55000,60000]})
        check('fixed_window_source_script',fixed)
        def sliding():
            for now,mid,want in [(1000,'a',[1,1]),(1500,'b',[1,2]),(1600,'b',[2,2]),(1999,'c',[0,2]),(2000,'c',[1,2])]:
                assert_reply(a.execute('EVAL',code['sliding_window'],1,'lab:live:sliding',now,1000,2,mid),want)
        check('sliding_window_boundaries_source_script',sliding)
        def pipeline():
            assert_reply(a.pipeline([('SET','lab:live:p1',1),('SET','lab:live:p2',2),('MGET','lab:live:p1','lab:live:p2')]),['OK','OK',['1','2']])
        check('resp_pipeline_order',pipeline)
        def expiration():
            a.execute('SET','lab:live:expires','x','PX',50)
            for _ in range(100):
                if a.execute('GET','lab:live:expires') is None:break
                time.sleep(0.01)
            assert_reply(a.execute('PTTL','lab:live:expires'),-2)
        check('expires_from_reads',expiration)
        def fields():
            a.execute('HSET','lab:live:hfield','a',1,'b',2);assert_reply(a.execute('HEXPIRE','lab:live:hfield',60,'FIELDS',1,'a'),[1])
            assert_reply(a.execute('TTL','lab:live:hfield'),-1);assert_reply(a.execute('HTTL','lab:live:hfield','FIELDS',2,'a','b'),[{'between':[50,60]},-1])
        check('field_expiry_is_not_key_expiry',fields)
        def pending_claim():
            assert_reply(a.execute('XADD','lab:live:stream','1000-0','job','j1'),'1000-0');a.execute('XGROUP','CREATE','lab:live:stream','g',0)
            a.execute('XREADGROUP','GROUP','g','alice','COUNT',1,'STREAMS','lab:live:stream','>')
            assert_reply(b.execute('XREADGROUP','GROUP','g','bob','COUNT',1,'STREAMS','lab:live:stream','>'),None)
            got=b.execute('XAUTOCLAIM','lab:live:stream','g','bob',0,'0-0','COUNT',1);assert_reply(got[1],[['1000-0',['job','j1']]])
            assert_reply(b.execute('XACK','lab:live:stream','g','1000-0'),1);assert_reply(b.execute('XLEN','lab:live:stream'),1)
        check('stream_pending_claim_not_delete',pending_claim)
    def pubsub():
        with Client(port) as pub,Client(port) as sub:
            assert_reply(sub.execute('SUBSCRIBE','lab:live:channel'),['subscribe','lab:live:channel',1])
            assert_reply(pub.execute('PUBLISH','lab:live:channel','one'),1);assert_reply(sub.receive(),['message','lab:live:channel','one'])
            assert_reply(sub.execute('UNSUBSCRIBE','lab:live:channel'),['unsubscribe','lab:live:channel',0])
            assert_reply(pub.execute('PUBLISH','lab:live:channel','missed'),0);sub.execute('SUBSCRIBE','lab:live:channel')
            pub.execute('PUBLISH','lab:live:channel','two');assert_reply(sub.receive(),['message','lab:live:channel','two'])
    check('pubsub_offline_event_not_replayed',pubsub)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--server',help='local redis-server executable; no host/url argument accepted')
    parser.add_argument('--report',type=Path,default=Path('redis-live-report.json'));args=parser.parse_args()
    report={'target_version':VERSION,'mode':'real-server','status':'not-run','checks':[],
            'limitations':['Standalone loopback Redis only; no Sentinel/Cluster failover, disk power-loss or cloud validation',
                           'No Java, Python or other application client-library integration is covered by this RESP2 runner']}
    def save():args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    executable=args.server or shutil.which('redis-server')
    if not executable:
        report['reason']='redis-server executable is unavailable; live tests did not run';save();print(report['reason']);return 2
    try:
        version=subprocess.run([executable,'--version'],text=True,capture_output=True,check=True,timeout=10).stdout
        match=re.search(r'\bv=(\d+\.\d+\.\d+)\b',version);report['actual_version']=match[1] if match else version.strip()
        if not match or match[1]!=VERSION:
            report['reason']='Exact target version required; no silent compatibility pass';save();print(report['reason']);return 2
        def emit(name,ok,error):report['checks'].append({'name':name,'passed':ok,'error':error})
        with tempfile.TemporaryDirectory(prefix='redis-reader-owned-') as directory:
            with own_server(executable,directory) as (port,process):
                with Client(port) as c:
                    for item in labs():
                        try:
                            for cmd,expected in zip(item.commands,item.expected):assert_reply(c.execute(*cmd),expected)
                            emit(item.name,True,None)
                        except Exception as exc:emit(item.name,False,repr(exc));raise
                advanced_cases(port,emit)
            with own_server(executable,directory) as (port,process):
                with Client(port) as c:
                    c.execute('SET','lab:persist','v1');assert_reply(c.execute('SAVE'),'OK');c.execute('SET','lab:persist','v2')
                    try:c.execute('SHUTDOWN','NOSAVE')
                    except (OSError,ConnectionError):pass
                process.wait(timeout=5)
            with own_server(executable,directory) as (port,process):
                with Client(port) as c:assert_reply(c.execute('GET','lab:persist'),'v1')
                emit('snapshot_restores_saved_value_not_later_write',True,None)
        report['status']='passed';report['checks_run']=len(report['checks']);save();print(f"{len(report['checks'])} real-server checks passed on {VERSION}");return 0
    except Exception as exc:
        report['status']='failed';report['error']=repr(exc);save();traceback.print_exc();return 1

if __name__=='__main__':raise SystemExit(main())
