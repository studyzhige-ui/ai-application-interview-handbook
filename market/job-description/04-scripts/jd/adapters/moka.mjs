#!/usr/bin/env node
/**
 * Enumerate first-party Moka-family ATS tenants discovered from official company career pages.
 *
 * The public jobs/v2 and website/job endpoints return an AES-CBC envelope.
 * We bootstrap aesIv + cookies from the official portal HTML, decrypt the
 * complete job pool, then fetch full detail for each job. No third-party job
 * data is ever imported.
 */
import fs from "node:fs";
import { cacheIsFresh, assertCompletePool } from "./cache.mjs";
import { fileURLToPath } from "node:url";
import path from "node:path";
const BUSINESS = fileURLToPath(new URL("../../../", import.meta.url));
const businessPath = p => path.join(BUSINESS, p);
import { createDecipheriv } from "node:crypto";

const CFG=JSON.parse(fs.readFileSync(businessPath("03-strategy/official-2027-campus-sources.json"),"utf8"));
const BROWSER=JSON.parse(fs.readFileSync(businessPath("01-data/official-2027-browser-discovery.generated.json"),"utf8"));
const OUT=process.argv[2]||businessPath("01-data/official-2027-moka-discovery.generated.json");
const REQUEST_TIMEOUT_MS=15000;
const TENANT_TIMEOUT_MS=90000;
const TENANT_CONCURRENCY=4;
const AES_IV="de7c21ed8d6f50fe";
const MOKA_LIST_API="https://app.mokahr.com/api/outer/ats-apply/website/jobs/v2";
const TARGET_TITLE_RE=/(?:agent|智能体|rag|harness|runtime|coding|ai\s*(?:应用|全栈|开发|研发|工程|平台|infra|devops|软件|系统|后端|前端)|大模型(?:应用|开发|研发|工程|平台)|fde)/i;
async function fetchTimed(url,options={}){
  return fetch(url,{...options,signal:AbortSignal.timeout(REQUEST_TIMEOUT_MS)});
}

function htmlDecode(s){
  return (s||"")
    .replace(/&quot;/g,'"').replace(/&lt;/g,"<").replace(/&gt;/g,">")
    .replace(/&#x27;/g,"'").replace(/&#39;/g,"'").replace(/&amp;/g,"&");
}
function htmlToText(s){
  return htmlDecode(s||"")
    .replace(/<br\s*\/?>/gi,"\n")
    .replace(/<\/(p|div|li|h[1-6]|tr|td|th|ul|ol|section)>/gi,"\n")
    .replace(/<[^>]+>/g,"").replace(/&nbsp;/gi," ")
    .replace(/\u00a0/g," ").replace(/[ \t]+\n/g,"\n")
    .replace(/\n{3,}/g,"\n\n").trim();
}
function parseInit(html){
  const m=html.match(/<input[^>]*id=["']init-data["'][^>]*value=["']([^"']+)["']/i)
       || html.match(/<input[^>]*value=["']([^"']+)["'][^>]*id=["']init-data["']/i);
  if(!m)return null;
  try{return JSON.parse(htmlDecode(m[1]));}catch{return null;}
}
function splitJD(text){
  const t=htmlToText(text);
  const m=t.match(/\n\s*(?:任职要求|岗位要求|职位要求|Requirements?\s*[:：]?)/i);
  if(!m)return {description:t,requirements:""};
  const i=m.index||0;
  return {description:t.slice(0,i).trim(),requirements:t.slice(i).trim()};
}
function decryptEnvelope(env){
  if(!env||typeof env!=="object")return env;
  if(!env.data||!env.necromancer)return env;
  try{
    const key=Buffer.from(env.necromancer,"utf8");
    const iv=Buffer.from(AES_IV,"utf8");
    const d=createDecipheriv("aes-128-cbc",key,iv);
    const plain=Buffer.concat([d.update(Buffer.from(env.data,"base64")),d.final()]).toString("utf8");
    return JSON.parse(plain);
  }catch{return null;}
}
function configuredContract(src){
  if(!src?.moka_endpoint||!src?.moka_org_id||!src?.moka_site_id)return null;
  const body={
    orgId:String(src.moka_org_id),siteId:String(src.moka_site_id),
    limit:30,offset:0,needStat:true,jobIdTopList:[],
    customFields:{},site:src.moka_site||"campus",locale:src.moka_locale||"zh-CN"
  };
  if(src.moka_source_token)body.sourceToken=src.moka_source_token;
  if(Array.isArray(src.moka_commitments)&&src.moka_commitments.length)body.commitments=src.moka_commitments;
  return {endpoint:MOKA_LIST_API,body};
}
function resultFromConfiguredSource(src){
  const contract=configuredContract(src);
  if(!contract)return null;
  return {
    company:src.company,seed_portal:src.search_url||src.job_list_url||src.portal,
    root_portal:src.official_root,pages:[{
      page_url:src.search_url||src.job_list_url||src.portal,
      final_url:src.search_url||src.job_list_url||src.portal,
      cycle_evidence:[src.current_campus_board?"当前官方校园招聘":"当前官方招聘"]
    }],
    endpoints:[{
      status:200,method:"POST",url:contract.endpoint,
      post_data:JSON.stringify(contract.body)
    }],
    configured_contract:true
  };
}

function endpointContract(result){
  const eps=(result.endpoints||[]).filter(e=>
    e.status===200 && e.method==="POST" && /\/api\/outer\/ats-apply\/website\/jobs\/v2(?:\\?|$)/.test(e.url)
  );
  if(!eps.length)return null;
  for(const e of eps){
    try{
      const body=JSON.parse(e.post_data||"{}");
      if(body.orgId&&body.siteId)return {endpoint:e.url,body};
    }catch{}
  }
  return null;
}
function officialPage(result,endpoint){
  const origin=new URL(endpoint).origin;
  const pages=(result.pages||[]).map(p=>p.final_url||p.page_url).filter(Boolean);
  return pages.find(u=>{try{return new URL(u).origin===origin && /job|campus|apply|recruit/i.test(u);}catch{return false;}})
      || pages.find(u=>{try{return new URL(u).origin===origin;}catch{return false;}})
      || result.seed_portal || result.root_portal;
}
async function bootstrap(url){
  const headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
  };
  let r=await fetchTimed(url,{headers,redirect:"manual"});
  const cookies=[];
  const raw=r.headers.get("set-cookie");
  if(raw)cookies.push(...raw.split(/,(?=[^;,]+=)/).map(x=>x.split(";")[0].trim()).filter(Boolean));
  const cookie=cookies.join("; ");
  r=await fetchTimed(url,{headers:{...headers,Cookie:cookie},redirect:"follow"});
  if(!r.ok)throw new Error("portal HTTP "+r.status);
  const html=await r.text();
  const init=parseInit(html);
  if(!init?.aesIv)throw new Error("Moka init-data/aesIv missing");
  return {init,cookie,finalUrl:r.url};
}
async function apiCall(url,body){
  const r=await fetchTimed(url,{method:"POST",headers:{
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept":"application/json,*/*","Content-Type":"application/json"
  },body:JSON.stringify(body)});
  if(!r.ok)throw new Error("HTTP "+r.status+" "+url);
  const env=await r.json();
  const decoded=decryptEnvelope(env);
  if(!decoded)throw new Error("cannot decrypt "+url+" with fixed Moka IV");
  if(decoded.code!==undefined && decoded.code!==0)throw new Error("upstream code="+decoded.code+" "+(decoded.msg||""));
  return decoded;
}
function jobsFromDecoded(x){
  const d=x?.data||x||{};
  if(Array.isArray(d.jobs))return d.jobs;
  if(Array.isArray(d.list))return d.list;
  if(Array.isArray(d.items))return d.items;
  return [];
}
function totalFromDecoded(x){
  const d=x?.data||x||{};
  const raw=d?.jobStats?.total ?? d?.total ?? d?.count;
  if(raw==null) throw new Error("Moka list response missing advertised total");
  return Number(raw);
}
function cityText(j){
  const xs=j?.locations||[];
  const out=[];
  for(const x of xs){
    const v=x?.cityName||x?.country||x?.address||"";
    if(v&&!out.includes(v))out.push(v);
  }
  return out.join(" / ");
}
function normalize(company,j,api,portal,cycle){
  const id=String(j?.id||j?.jobId||"");
  const jd=splitJD(j?.jobDescription||j?.description||"");
  return {
    company,title:j?.title||j?.name||"",job_id:id,location:cityText(j),
    category:j?.commitment||(j?.hireMode===1?"全职":j?.hireMode===2?"实习":""),
    department:j?.department?.name||j?.zhineng?.name||"",
    description:jd.description,requirements:jd.requirements,
    official_url:portal,official_api:api,cycle_evidence:cycle||"",
    matched_keywords:[]
  };
}
function merge(existing,incoming){
  const m=new Map();
  for(const j of [...existing,...incoming]){
    const k=j.job_id||j.title+"|"+j.location;
    if(!k)continue;
    const old=m.get(k);
    if(!old||(j.description.length+j.requirements.length)>(old.description.length+old.requirements.length))m.set(k,j);
  }
  return [...m.values()];
}
async function enumerateOne(result){
  const contract=endpointContract(result);
  if(!contract)return null;
  const listUrl=new URL(contract.endpoint); listUrl.search="";
  const portal=officialPage(result,listUrl.href);
  const template={...contract.body};
  const orgId=template.orgId;
  const siteId=String(template.siteId);
  const locale=template.locale||"zh-CN";
  const site=template.site||(/campus/i.test(portal)?"campus":"social");
  const cycle=[...new Set((result.pages||[]).flatMap(p=>p.cycle_evidence||[]))].join(" / ");
  let offset=0,total=0,jobs=[];
  for(let page=0;page<100;page++){
    const body={...template,orgId,siteId,limit:50,offset,needStat:true,jobIdTopList:[],keyword:"",customFields:template.customFields||{},site,locale};
    const decoded=await apiCall(listUrl.href,body);
    const rows=jobsFromDecoded(decoded);
    if(page===0)total=totalFromDecoded(decoded);
    jobs=merge(jobs,rows.map(j=>normalize(result.company,j,listUrl.href,portal,cycle)));
    offset+=rows.length;
    if(!rows.length||rows.length<50||(total&&offset>=total))break;
  }
  assertCompletePool(total,jobs);
  const detailUrl=listUrl.origin+"/api/outer/ats-apply/website/job";
  // Full-pool proof comes from jobs/v2 pagination. Fetch expensive detail pages
  // only for titles that can enter the formal AI/Agent library; preserve every
  // list row so enumeration completeness is never coupled to detail latency.
  const targetJobs=jobs.filter(j=>TARGET_TITLE_RE.test(j.title||""));
  const enriched=[];
  for(let i=0;i<targetJobs.length;i+=8){
    const chunk=targetJobs.slice(i,i+8);
    const vals=await Promise.all(chunk.map(async j=>{
      if(!j.job_id)return j;
      try{
        const dec=await apiCall(detailUrl,{orgId,siteId,jobId:j.job_id,locale});
        const raw=dec?.data?.job||dec?.data||dec?.job||null;
        if(!raw||typeof raw!=="object")return j;
        return normalize(result.company,raw,detailUrl,portal,cycle);
      }catch{return j;}
    }));
    enriched.push(...vals);
  }
  return {
    company:result.company,status:"OK",complete:true,portal,api:listUrl.href,detail_api:detailUrl,
    fetched:jobs.length,total:total||jobs.length,cycle_evidence:cycle,jobs:merge(jobs,enriched)
  };
}

async function enumerateOneBounded(result){
  if(!endpointContract(result))return null;
  let timer;
  const timeout=new Promise((_,reject)=>{
    timer=setTimeout(()=>reject(new Error("Moka tenant timeout after "+TENANT_TIMEOUT_MS+"ms")),TENANT_TIMEOUT_MS);
  });
  try{return await Promise.race([enumerateOne(result),timeout]);}
  finally{if(timer)clearTimeout(timer);}
}

const results=[];
const configured=(CFG.sources||[]).map(resultFromConfiguredSource).filter(Boolean);
const configuredCompanies=new Set(configured.map(x=>x.company));
const discovered=(cacheIsFresh(BROWSER)?BROWSER.results||[]:[]).filter(r=>endpointContract(r)&&!configuredCompanies.has(r.company));
const candidates=[...configured,...discovered];
for(let i=0;i<candidates.length;i+=TENANT_CONCURRENCY){
  const chunk=candidates.slice(i,i+TENANT_CONCURRENCY);
  const settled=await Promise.all(chunk.map(async r=>{
    try{
      const x=await enumerateOneBounded(r);
      if(x)console.log("moka "+x.company+": jobs="+x.jobs.length+" total="+x.total);
      return x;
    }catch(e){
      console.log("moka "+r.company+": ERROR "+e);
      return {company:r.company,status:"BLOCKED",jobs:[],error:String(e).slice(0,500)};
    }
  }));
  results.push(...settled.filter(Boolean));
}
fs.writeFileSync(OUT,JSON.stringify({generated_at:new Date().toISOString(),source_commit:process.env.SYNC_SOURCE_SHA||"",run_id:process.env.GITHUB_RUN_ID||"",run_attempt:process.env.GITHUB_RUN_ATTEMPT||"",results},null,2)+"\n","utf8");
