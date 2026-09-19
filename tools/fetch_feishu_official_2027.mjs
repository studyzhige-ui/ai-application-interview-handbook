#!/usr/bin/env node
/**
 * Enumerate first-party official Feishu recruitment tenants that were proven by
 * a company-owned careers page. This script never discovers tenants from third-party pages.
 */
import fs from "node:fs";

const cfg=JSON.parse(fs.readFileSync("market/jobs/official-2027-campus-sources.json","utf8"));
const out=process.argv[2] || "/tmp/feishu-official-2027.json";
const keywords=[
  "Agent","AI Agent","智能体","AI应用","AI 应用","大模型应用","LLM应用",
  "AI Native","Coding Agent","Code Agent","RAG","Harness","Runtime",
  "Agent Infra","MCP","Skill"
];

function tenantHost(url){
  try{
    const u=new URL(url);
    if(!u.hostname.endsWith(".jobs.feishu.cn")) return null;
    const first=u.pathname.replace(/^\//,"").split("/").filter(Boolean)[0]||"campus";
    const projects=(u.searchParams.get("project")||"").split(",").filter(Boolean);
    return {host:u.origin,pathname:u.pathname,search:u.search,websitePath:first,projects};
  }catch{return null;}
}
function normalizeJob(company,host,websitePath,j,keyword,sourceCycle){
  const subjects=[];
  const rawSubjects=j.job_subject_list || (j.job_subject ? [j.job_subject] : []);
  for(const s of rawSubjects){
    const name=typeof s?.name==="string" ? s.name : (s?.name?.zh_cn || s?.name?.i18n || "");
    if(name) subjects.push(name);
  }
  return {
    company,
    title:j.title||"",
    job_id:String(j.id||""),
    location:(j.city_list||[]).map(x=>x.name).filter(Boolean).join(" / ") || (j.city_info?.name||""),
    category:j.recruit_type?.name||"",
    department:j.job_category?.name || j.job_function?.name || "",
    description:j.description||"",
    requirements:j.requirement||"",
    official_url:host+"/"+websitePath+"/position/"+j.id+"/detail",
    official_api:host+"/api/v1/search/job/posts",
    cycle_evidence:[sourceCycle,...subjects,j.recruit_type?.name].filter(Boolean).join(" / "),
    matched_keywords:[keyword]
  };
}
async function oneKeyword(company,portal,keyword,channel,sourceCycle){
  const t=tenantHost(portal);
  if(!t) throw new Error("not a feishu jobs tenant");
  const api=`${t.host}/api/v1/search/job/posts`;
  const headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept":"application/json, text/plain, */*",
    "Content-Type":"application/json",
    "portal-platform":"pc",
    "portal-channel":channel,
    "website-path":t.pathname.replace(/^\//,"").split("/")[0] || "campus",
    "Origin":t.host,
    "Referer":portal
  };
  const jobs=[];
  let offset=0, requests=0;
  for(let page=0;page<30;page++){
    const body={
      keyword,limit:100,offset,portal_type:3,portal_entrance:1,language:"zh",
      job_category_id_list:[],location_code_list:[],subject_id_list:t.projects,recruitment_id_list:[]
    };
    const res=await fetch(api,{method:"POST",headers,body:JSON.stringify(body)});
    requests++;
    if(!res.ok) throw new Error(`${company} ${channel} HTTP ${res.status}`);
    const payload=await res.json();
    if(payload.code!==0) throw new Error(`${company} ${channel} code=${payload.code}`);
    const d=payload.data||{};
    const rows=d.job_post_list||[];
    for(const j of rows) jobs.push(normalizeJob(company,t.host,t.websitePath,j,keyword,sourceCycle));
    const total=Number(d.count||0);
    offset+=rows.length;
    if(!rows.length || offset>=total || rows.length<100) break;
  }
  return {jobs,requests};
}
async function enumerateSource(src){
  const t=tenantHost(src.portal);
  if(!t) return null;
  const channels=["campus","social"];
  let best=null, errors=[];
  const sourceCycle=(src.verified_2027_project || /2027/.test(src.note||"")) ? "官方2027项目" : "";
  for(const channel of channels){
    try{
      const batches=[];
      for(let i=0;i<keywords.length;i+=4){
        batches.push(...await Promise.all(keywords.slice(i,i+4).map(k=>oneKeyword(src.company,src.portal,k,channel,sourceCycle))));
      }
      const seen=new Map(); let requests=0;
      for(const b of batches){
        requests+=b.requests;
        for(const j of b.jobs){
          const key=j.job_id||j.official_url;
          if(seen.has(key)){
            const old=seen.get(key);
            for(const k of j.matched_keywords) if(!old.matched_keywords.includes(k)) old.matched_keywords.push(k);
          }else seen.set(key,j);
        }
      }
      const jobs=[...seen.values()];
      if(!best || jobs.length>best.jobs.length) best={company:src.company,portal:src.portal,channel,status:"OK",requests,jobs};
    }catch(e){ errors.push(`${channel}: ${String(e).slice(0,220)}`); }
  }
  if(best) return best;
  return {company:src.company,portal:src.portal,status:"BLOCKED",requests:0,jobs:[],error:errors.join(" | ")};
}

const sources=cfg.sources.filter(s=>tenantHost(s.portal));
const results=[];
for(let i=0;i<sources.length;i+=4){
  results.push(...(await Promise.all(sources.slice(i,i+4).map(enumerateSource))).filter(Boolean));
}
for(const r of results) console.log(`feishu ${r.company}: status=${r.status}, jobs=${r.jobs.length}, channel=${r.channel||""}`);
fs.writeFileSync(out,JSON.stringify({generated_at:new Date().toISOString(),keywords,results},null,2)+"\n","utf8");
