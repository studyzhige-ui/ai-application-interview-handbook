"""Optional real Faiss experiment; strict version, no mock fallback, no persistence.

Missing dependency exits 77 (SKIP); wrong installed version exits with error.
Synthetic random workload is distinct from the six-point functional fixture.
"""
from __future__ import annotations
import importlib.util
import json
import platform
import time
import sys
TARGET='1.15.1'

def main() -> int:
    if importlib.util.find_spec('faiss') is None:
        print(json.dumps({'status':'SKIP','reason':'faiss is not installed','target':TARGET}))
        return 77
    import faiss
    import numpy as np
    if faiss.__version__ != TARGET:
        raise RuntimeError(f'expected faiss {TARGET}, found {faiss.__version__}; no silent version substitution')
    faiss.omp_set_num_threads(1)
    rng=np.random.default_rng(20260927)
    xb=rng.normal(size=(4096,32)).astype('float32')
    xq=rng.normal(size=(128,32)).astype('float32')
    k=10
    baseline=faiss.IndexFlatL2(32); baseline.add(xb)
    gold_d,gold=baseline.search(xq,k)
    rows=[]
    def evaluate(index,label,parameter):
        index.search(xq[:8],k)  # Small explicit warmup, no claim of full production warm state.
        start=time.perf_counter();dist,ids=index.search(xq,k);elapsed=time.perf_counter()-start
        recall=float(np.mean([len(set(a)&set(g))/k for a,g in zip(ids,gold)]))
        rows.append({'index':label,'parameter':parameter,'recall_at_10':recall,
                     'batch_queries':len(xq),'batch_seconds':elapsed,
                     'seconds_per_query_amortized':elapsed/len(xq)})
        return dist,ids
    evaluate(baseline,'Flat',{})
    start=time.perf_counter()
    graph=faiss.IndexHNSWFlat(32,16);graph.hnsw.efConstruction=100;graph.add(xb)
    graph_build=time.perf_counter()-start
    for ef in (16,64,128):
        graph.hnsw.efSearch=ef;evaluate(graph,'HNSW',{'M':16,'efConstruction':100,'efSearch':ef})
    start=time.perf_counter()
    ivf=faiss.IndexIVFFlat(faiss.IndexFlatL2(32),32,16,faiss.METRIC_L2)
    ivf.train(xb);ivf.add(xb);ivf_build=time.perf_counter()-start
    for nprobe in (1,4,16):
        ivf.nprobe=nprobe;d,ids=evaluate(ivf,'IVF_FLAT',{'nlist':16,'nprobe':nprobe})
    # Floating arithmetic may differ; compare sorted distance values, not strict bit identity.
    if not np.allclose(d,gold_d,rtol=1e-5,atol=1e-5):
        raise AssertionError('full-probe IVF_FLAT did not match Flat distance baseline')
    print(json.dumps({'status':'PASS','kind':'real_faiss_single_process_synthetic_workload',
                      'python':platform.python_version(),'faiss':faiss.__version__,'numpy':np.__version__,
                      'build_seconds':{'hnsw':graph_build,'ivf_including_training':ivf_build},
                      'results':rows,'limits':'No P95/P99, real text, service concurrency, persistence, or production claim'},indent=2))
    return 0
if __name__=='__main__': sys.exit(main())
