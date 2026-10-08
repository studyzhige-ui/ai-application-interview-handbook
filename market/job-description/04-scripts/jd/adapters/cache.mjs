/** Shared, offline-testable snapshot provenance gate. */
export function cacheIsFresh(payload, env=process.env, now=Date.now()){
  const stamp=Date.parse(payload?.generated_at||"");
  const age=now-stamp;
  if(!Number.isFinite(stamp)||age < -300000 || age > 6*60*60*1000)return false;
  for(const [name,field] of [["SYNC_SOURCE_SHA","source_commit"],["GITHUB_RUN_ID","run_id"],["GITHUB_RUN_ATTEMPT","run_attempt"]]){
    if(env[name] && String(payload?.[field]||"")!==String(env[name]))return false;
  }
  return true;
}

export function assertCompletePool(total, jobs){
  if(!Number.isInteger(total)||total<0||!Array.isArray(jobs)||jobs.length<total){
    throw new Error(`Incomplete official pool: unique=${jobs?.length}, advertised=${total}`);
  }
}
