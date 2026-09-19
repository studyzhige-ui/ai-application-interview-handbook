#!/usr/bin/env node
/**
 * Consume first-party Feishu-family ATS jobs captured from official career
 * pages by Playwright. Feishu search requests require runtime signatures, so
 * replaying unsigned URLs is intentionally avoided.
 */
import fs from "node:fs";

const cfg=JSON.parse(fs.readFileSync("market/jobs/official-2027-campus-sources.json","utf8"));
const browserPath="market/jobs/official-2027-browser-discovery.generated.json";
const browser=fs.existsSync(browserPath)?JSON.parse(fs.readFileSync(browserPath,"utf8")):{results:[]};
const out=process.argv[2]||"market/jobs/official-2027-feishu-discovery.generated.json";

function isFeishuLike(src,result){
  const urls=[src.portal,src.official_root,...(src.extra_portals||[]),
    ...(result?.pages||[]).map(p=>p.final_url||p.page_url),
    ...(result?.endpoints||[]).map(e=>e.url)
  ].filter(Boolean);
  return urls.some(u=>/\.jobs\.feishu\.cn|\/api\/v1\/search\/job\/posts/i.test(u));
}
function mergeJobs(jobs){
  const m=new Map();
  for(const j of jobs||[]){
    const key=j.job_id||j.official_url||((j.title||"")+"|"+(j.location||""));
    if(!key)continue;
    const old=m.get(key);
    if(!old||(String(j.description||"").length+String(j.requirements||"").length)>
      (String(old.description||"").length+String(old.requirements||"").length))m.set(key,j);
  }
  return [...m.values()];
}
const byCompany=new Map((browser.results||[]).map(x=>[x.company,x]));
const results=[];
for(const src of cfg.sources||[]){
  const b=byCompany.get(src.company);
  if(!b||!isFeishuLike(src,b))continue;
  const jobs=mergeJobs(b.jobs||[]);
  const full=Boolean(b.full_keyword_search);
  const complete=full&&["BROWSER_ENUMERATED","BROWSER_ENUMERATED_ZERO"].includes(b.status);
  results.push({
    company:src.company,portal:src.portal,
    status:complete?"OK":"BLOCKED",
    complete,full_keyword_search:full,
    jobs:complete?jobs:[],
    discovered_jobs:jobs.length,
    error:complete?"":"official Feishu page discovered, but exhaustive current-campus keyword enumeration is not yet proven"
  });
}
for(const r of results)console.log("feishu "+r.company+": status="+r.status+" jobs="+r.jobs.length+" discovered="+r.discovered_jobs);
fs.writeFileSync(out,JSON.stringify({generated_at:new Date().toISOString(),results},null,2)+"\n","utf8");
