"""Opt-in, real local Qdrant REST functional experiment. No SDK / mock fallback.

Creates a uniquely named collection, mutates ONLY that collection, then deletes it.
No network is used without --run. Only a loopback server is accepted.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
TARGET='1.19.1'

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true',help='Explicitly allow mutation of a new disposable collection')
    parser.add_argument('--url',default='http://127.0.0.1:6333')
    args=parser.parse_args()
    if not args.run:
        print(json.dumps({'status':'SKIP','reason':'--run not supplied','target':TARGET}))
        return 77
    u=urllib.parse.urlparse(args.url)
    if u.scheme not in ('http','https') or u.hostname not in ('127.0.0.1','localhost','::1') or u.username or u.password or u.query or u.fragment or u.path not in ('','/'):
        raise ValueError('Only a credential-free loopback HTTP(S) root URL is allowed')
    base=args.url.rstrip('/')
    # Ignore proxy environment variables, including for loopback.
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def call(method,path,body=None):
        data=None if body is None else json.dumps(body).encode('utf-8')
        req=urllib.request.Request(base+path,data=data,method=method,headers={'Content-Type':'application/json'})
        with opener.open(req,timeout=15) as response:
            result=json.load(response)
        if result.get('status') not in (None,'ok'):
            raise RuntimeError(f'Qdrant returned an error: {result}')
        return result
    try:
        version=call('GET','/').get('version')
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'Server responded with HTTP {exc.code}; this is not a missing-service SKIP') from exc
    except (urllib.error.URLError,TimeoutError,OSError) as exc:
        print(json.dumps({'status':'SKIP','reason':str(exc),'target':TARGET}))
        return 77
    if version != TARGET:
        raise RuntimeError(f'Expected server {TARGET}, found {version}; no silent version substitution')
    name='vector_course_'+uuid.uuid4().hex
    root='/collections/'+name
    created=False
    def completed(response):
        if response.get('result',{}).get('status') != 'completed':
            raise AssertionError(f'write was not completed: {response}')
    outcome=None
    try:
        try:
            call('PUT',root,{'vectors':{'size':2,'distance':'Cosine'}})
        except Exception as exc:
            raise RuntimeError(f'Creation of {name} failed; its outcome may be unknown. Inspect only this disposable name before cleanup.') from exc
        created=True
        fixture=json.loads(Path(__file__).with_name('data.json').read_text(encoding='utf-8'))
        points=[{'id':i+1,'vector':r['vector'],'payload':{k:v for k,v in r.items() if k!='vector'}} for i,r in enumerate(fixture['records'])]
        completed(call('PUT',root+'/points?wait=true',{'points':points}))
        completed(call('PUT',root+'/points?wait=true',{'points':points})) # replay stable IDs
        count=call('POST',root+'/points/count',{'exact':True})['result']['count']
        if count != 6: raise AssertionError(f'replay changed count: {count}')
        result=call('POST',root+'/points/query',{
            'query':fixture['query'],'filter':{'must':[{'key':'tenant_id','match':{'value':'alpha'}}]},
            'limit':3,'params':{'exact':True},'with_payload':True})['result']['points']
        result_ids=[p['payload']['id'] for p in result]
        if result_ids != ['A','C','D']: raise AssertionError(result_ids)
        retrieved=call('POST',root+'/points',{'ids':[1],'with_payload':True,'with_vector':True})['result']
        if len(retrieved)!=1 or retrieved[0]['payload']['source_version']!=1: raise AssertionError(retrieved)
        completed(call('POST',root+'/points/payload?wait=true',{'payload':{'source_version':2},'points':[1]}))
        updated=call('POST',root+'/points',{'ids':[1],'with_payload':True})['result']
        if updated[0]['payload']['source_version']!=2: raise AssertionError(updated)
        completed(call('POST',root+'/points/delete?wait=true',{'points':[1]}))
        if call('POST',root+'/points',{'ids':[1],'with_payload':True})['result']: raise AssertionError('deleted record remains visible')
        outcome={'status':'PASS','server':version,'kind':'real_single_local_server_functional_test',
                 'collection':name,'filtered_exact_ids':result_ids,
                 'limits':'No HNSW path proof, durability/restart, multi-client, replica, failure, or production verification'}
    finally:
        if created:
            # Cleanup failure must be visible; never silently report success with leftover data.
            call('DELETE',root)
    print(json.dumps(outcome,indent=2));return 0
if __name__=='__main__': sys.exit(main())
