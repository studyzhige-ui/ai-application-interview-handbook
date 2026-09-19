#!/usr/bin/env node
/**
 * Replay first-party Moka/outer ATS request contracts captured from official
 * company career pages. Contracts come only from official browser discovery.
 */
import fs from "node:fs";

const CFG=JSON.parse(fs.readFileSync("market/jobs/official-2027-campus-sources.json","utf8"));
const BROWSER=JSON.parse(fs.readFileSync("market/jobs/official-2027-browser-discovery.generated.json","utf8"));
const OUT=process.argv[2]||"market/jobs/official-2027-moka-discovery.generated.json";
const TERMS=CFG.strong_agent_keywords||CFG.agent_keywords||[];

function text(v){
  if(v==null)return "";
  if(typeof v==="string"||typeof v==="number")return String(v).trim();
  if(Array.isArray(v))return v.map(text).filter(Boolean).join(" / ");
  if(typeof v==="object")return Object.values(v).map(text).filter(Boolean).join(" / ");
  return "";
}
function findArray(node,depth=0){
  if(depth>8||node==null)return [];
  if(Array.isArray(node)){
    if(node.some(x=>x&&typeof x==="object"&&(x.id||x.jobId||x.name||x.title)))return node;
    for(const x of node){const a=findArray(x,depth+1);if(a.length)return a;}
    return [];
  }
  if(typeof node==="object"){
    for(const k of ["jobs","jobList","list","items","data","rows","records","result"]){
      if(k in node){const a=findArray(node[k],depth+1);if(a.length)return a;}
    }
    for(const v of Object.values(node)){const a=findArray(v,depth+1);if(a.length)return a;}
  }
  return [];
}
function getTitle(j){return text(j.name||j.title||j.jobName||j.positionName||j.jobTitle);}
function getId(j){return text(j.id||j.jobId||j.positionId||j.uuid);}
function normalize(company,base,j,keyword,cycle){
  const id=getId(j);
  const url=text(j.jobUrl||j.detailUrl||j.url||j.shareUrl) || (id ? base+"#/job/"+id : base);
  return {
    company,title:getTitle(j),job_id:id,
    location:text(j.location||j.locations||j.city||j.cityName||j.workLocation),
    category:text(j.recruitType||j.jobType||j.type)||"官方校招",
    department:text(j.department||j.departmentName||j.category||j.jobCategory),
    description:text(j.description||j.jobDescription||j.desc||j.responsibility||j.jobDuty),
    requirements:text(j.requirement||j.requirements||j.qualification||j.jobRequirement),
    official_url:url,official_api:"",cycle_evidence:cycle||"",matched_keywords:[keyword]
  };
}
function mergeJobs(jobs){
  const m=new Map();
  for(const j of jobs){
    const key=j.job_id || (j.title+"|"+j.location);
    if(!key)continue;
    if(!m.has(key))m.set(key,j);
    else{
      const o=m.get(key);
      for(const k of j.matched_keywords||[])if(!o.matched_keywords.includes(k))o.matched_keywords.push(k);
      if((j.description.length+j.requirements.length)>(o.description.length+o.requirements.length)){
        j.matched_keywords=o.matched_keywords;m.set(key,j);
      }
    }
  }
  return [...m.values()];
}
async function replay(company,result){
  const eps=(result.endpoints||[]).filter(e=>e.status===200 && /\/api\/outer\/ats-apply\/website\/jobs\/v2/.test(e.url) && e.method==="POST");
  if(!eps.length)return null;
  let template;
  try{template=JSON.parse(eps[0].post_data||"{}");}catch{return null;}
  const api=new URL(eps[0].url); api.search="";
  const base=(result.pages||[]).map(p=>p.final_url||p.page_url).find(u=>u&&/jobs|campus|apply|recruit/i.test(u)) || result.seed_portal || result.root_portal;
  const cycle=[...new Set((result.pages||[]).flatMap(p=>p.cycle_evidence||[]))].join(" / ");
  const jobs=[];
  let requests=0;
  for(const keyword of TERMS){
    let offset=0;
    for(let page=0;page<50;page++){
      const body={...template,keyword,offset,limit:100,needStat:true};
      const res=await fetch(api,{method:"POST",headers:{
        "User-Agent":"Mozilla/5.0 Chrome/126 Safari/537.36",
        "Accept":"application/json, text/plain, */*","Content-Type":"application/json;charset=UTF-8",
        "Origin":api.origin,"Referer":base
      },body:JSON.stringify(body)});
      requests++;
      if(!res.ok)throw new Error(company+" Moka HTTP "+res.status);
      const payload=await res.json();
      const rows=findArray(payload);
      for(const j of rows){
        const n=normalize(company,base,j,keyword,cycle);n.official_api=api.href;jobs.push(n);
      }
      let total=0;
      const candidates=[payload?.data?.total,payload?.data?.count,payload?.total,payload?.count,payload?.data?.pagination?.total];
      for(const v of candidates){const n=Number(v||0);if(n>total)total=n;}
      offset+=rows.length;
      if(!rows.length||rows.length<100||(total&&offset>=total))break;
    }
  }
  return {company,status:"OK",api:api.href,base,requests,jobs:mergeJobs(jobs),cycle_evidence:cycle};
}
const results=[];
for(const r of BROWSER.results||[]){
  try{
    const x=await replay(r.company,r);
    if(x){results.push(x);console.log("moka "+x.company+": jobs="+x.jobs.length+" requests="+x.requests);}
  }catch(e){
    results.push({company:r.company,status:"BLOCKED",jobs:[],error:String(e).slice(0,400)});
    console.log("moka "+r.company+": ERROR "+e);
  }
}
fs.writeFileSync(OUT,JSON.stringify({generated_at:new Date().toISOString(),keywords:TERMS,results},null,2)+"\n","utf8");
