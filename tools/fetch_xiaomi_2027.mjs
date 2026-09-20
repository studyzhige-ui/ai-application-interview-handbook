#!/usr/bin/env node
/**
 * Enumerate Xiaomi official 2027 campus formal pool via first-party ATSX,
 * with parallel pagination after the first count request.
 */
import { writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const API="https://xiaomi.jobs.f.mioffice.cn/api/v1/search/job/posts";
const DETAIL_ROOT="https://xiaomi.jobs.f.mioffice.cn/campus/position";
const out=process.argv[2]||join(tmpdir(),"xiaomi-2027-campus.json");
const headers={
  "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36",
  "Accept":"application/json, text/plain, */*","Content-Type":"application/json",
  "portal-platform":"pc","portal-channel":"campus","website-path":"campus",
  "Referer":"https://xiaomi.jobs.f.mioffice.cn/campus/"
};
const limit=100;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const REQUEST_TIMEOUT_MS=15000;
async function fetchWithRetry(url,options,label){
  let last;
  for(let attempt=1;attempt<=4;attempt++){
    try{
      const res=await fetch(url,{...options,signal:AbortSignal.timeout(REQUEST_TIMEOUT_MS)});
      if(res.ok || res.status<500) return res;
      last=new Error(`${label} HTTP ${res.status} ${res.statusText}`);
    }catch(e){ last=e; }
    if(attempt<4) await sleep(800*attempt);
  }
  throw last;
}
async function fetchPage(offset){
  const body={keyword:"",limit,offset,portal_type:3,portal_entrance:1,language:"zh",recruitment_id_list:["201"]};
  const res=await fetchWithRetry(API,{method:"POST",headers,body:JSON.stringify(body)},"Xiaomi"+" offset="+offset);
  if(!res.ok) throw new Error(`Xiaomi HTTP ${res.status} ${res.statusText} offset=${offset}`);
  const payload=await res.json();
  if(payload.code!==0) throw new Error(`Xiaomi code=${payload.code}: ${payload.message||""}`);
  return payload.data||{};
}
function norm(j){
  return {
    company:"小米",title:j.title||"",job_id:String(j.id||""),
    location:(j.city_list||[]).map(x=>x.name).filter(Boolean).join(" / ") || (j.city_info?.name||""),
    category:j.recruit_type?.name||"校招正式",
    department:j.job_function?.name || j.job_category?.name || "",
    description:j.description||"",requirements:j.requirement||"",
    official_url:`${DETAIL_ROOT}/${j.id}/detail`,official_api:API,
    cycle_evidence:[j.job_subject?.name?.zh_cn,j.job_subject?.name,j.recruit_type?.name].filter(x=>typeof x==="string"&&x).join(" / ") || "小米官方 campus 正式岗池"
  };
}
const first=await fetchPage(0);
const total=Number(first.count||0);
const rows=[...(first.job_post_list||[])];
const offsets=[];
for(let o=limit;o<total;o+=limit) offsets.push(o);
const concurrency=8;
let requests=1;
for(let i=0;i<offsets.length;i+=concurrency){
  const ds=await Promise.all(offsets.slice(i,i+concurrency).map(fetchPage));
  requests+=ds.length;
  for(const d of ds) rows.push(...(d.job_post_list||[]));
}
const seen=new Map();
for(const j of rows){const n=norm(j);if(n.job_id)seen.set(n.job_id,n);}
const jobs=[...seen.values()];
writeFileSync(out,JSON.stringify({strategy:"official-campus-pool-parallel",concurrency,requests,total,jobs},null,2)+"\n","utf8");
console.log(`xiaomi official campus fetched=${jobs.length}, total=${total}, requests=${requests}`);
