#!/usr/bin/env node
/**
 * Generic first-party browser discovery for dynamic campus recruitment portals.
 *
 * It starts from the official company recruitment/career URL in the registry,
 * follows official campus/2027/student links, observes JSON/XHR issued by the
 * official site itself, and extracts job-like objects. No aggregator/search
 * result content is imported.
 */
import fs from "node:fs";
import { chromium } from "playwright";

const ROOT = process.cwd();
const CONFIG = JSON.parse(fs.readFileSync("market/jobs/official-2027-campus-sources.json","utf8"));
const OUT = process.argv[2] || "market/jobs/official-2027-browser-discovery.generated.json";

const STRONG = (CONFIG.strong_agent_keywords || CONFIG.agent_keywords || []).map(x=>x.toLowerCase());
const TITLE_KEYS = ["positionName","jobName","jobTitle","positionTitle","recruitPostName","postName","title","name"];
const ID_KEYS = ["positionId","jobId","postId","publishId","reqId","id","code"];
const DESC_KEYS = ["description","jobDescription","jobDesc","positionDesc","responsibility","responsibilities","jobDuty","duty","workContent","desc","postDuty"];
const REQ_KEYS = ["requirement","requirements","jobRequirement","positionRequire","positionDemand","qualification","qualifications","serveRequirement","request"];
const LOC_KEYS = ["location","city","workCity","workPlace","workLocation","workLocations","cityName","workCityName"];
const DEPT_KEYS = ["department","departmentName","deptName","categoryName","jobCategory","positionCategoryName"];
const URL_KEYS = ["shareUrl","detailUrl","jobUrl","positionUrl","url","href","link"];

function text(v){
  if(v==null) return "";
  if(typeof v==="string"||typeof v==="number"||typeof v==="boolean") return String(v).trim();
  if(Array.isArray(v)) return v.map(text).filter(Boolean).join(" / ");
  if(typeof v==="object") return Object.values(v).map(text).filter(Boolean).join(" / ");
  return "";
}
function pick(o,keys){ for(const k of keys){ if(Object.prototype.hasOwnProperty.call(o,k)){const v=text(o[k]); if(v)return v;} } return ""; }
function sameOfficialFamily(a,b){
  try{
    const ha=new URL(a).hostname.replace(/^www\./,"");
    const hb=new URL(b).hostname.replace(/^www\./,"");
    const suffixes=["mokahr.com","mioffice.cn","feishu.cn","myworkdayjobs.com","workdayjobs.com"];
    if(ha===hb||ha.endsWith("."+hb)||hb.endsWith("."+ha)) return true;
    // ATS hosts are accepted only because navigation originated from the official page.
    return suffixes.some(s=>ha.endsWith(s));
  }catch{return false;}
}
function recursiveJobs(node,meta,out,path="$",depth=0){
  if(depth>12||node==null) return;
  if(Array.isArray(node)){
    for(let i=0;i<node.length;i++) recursiveJobs(node[i],meta,out,`${path}[${i}]`,depth+1);
    return;
  }
  if(typeof node!=="object") return;
  const title=pick(node,TITLE_KEYS);
  const id=pick(node,ID_KEYS);
  const desc=pick(node,DESC_KEYS);
  const req=pick(node,REQ_KEYS);
  const loc=pick(node,LOC_KEYS);
  const dept=pick(node,DEPT_KEYS);
  const objText=(title+" "+desc+" "+req+" "+dept).toLowerCase();
  const agentHit=STRONG.some(k=>objText.includes(k));
  const jobShape=!!title && (!!desc || !!req || (!!id && /(job|position|post|recruit|career)/i.test(meta.response_url+" "+path)));
  if(jobShape && agentHit){
    let u=pick(node,URL_KEYS);
    try{ if(u) u=new URL(u,meta.page_url).href; }catch{}
    out.push({
      company:meta.company,title,job_id:id,location:loc,category:meta.category||"官方校招待复核",
      department:dept,description:desc,requirements:req,
      official_url:u||meta.page_url,official_api:meta.response_url,
      cycle_evidence:meta.cycle_evidence||"", extraction_path:path
    });
  }
  for(const [k,v] of Object.entries(node)) recursiveJobs(v,meta,out,`${path}.${k}`,depth+1);
}
function uniqueJobs(jobs){
  const m=new Map();
  for(const j of jobs){
    const key=[j.company,j.job_id||"",j.title,j.location].join("|");
    const old=m.get(key);
    if(!old || (j.description.length+j.requirements.length)>(old.description.length+old.requirements.length)) m.set(key,j);
  }
  return [...m.values()];
}
async function scroll(page){
  for(let i=0;i<8;i++){
    await page.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));
    await page.waitForTimeout(700);
  }
  await page.evaluate(()=>window.scrollTo(0,0));
}
async function searchInputs(page){
  const inputs=page.locator('input');
  const n=Math.min(await inputs.count(),20);
  for(let i=0;i<n;i++){
    const el=inputs.nth(i);
    const ph=((await el.getAttribute("placeholder"))||"").toLowerCase();
    if(!/(搜索|职位|岗位|keyword|search)/i.test(ph)) continue;
    for(const q of ["Agent","智能体","AI应用","大模型应用"]){
      try{
        await el.fill(q);
        await el.press("Enter");
        await page.waitForTimeout(1200);
        await scroll(page);
      }catch{}
    }
    break;
  }
}
async function runPage(context,company,url,rootHost,collector,visited){
  if(visited.has(url)||visited.size>10) return;
  visited.add(url);
  const page=await context.newPage();
  const responseTasks=[];
  page.on("response",resp=>{
    const task=(async()=>{
      const ct=(resp.headers()["content-type"]||"").toLowerCase();
      if(!ct.includes("json")) return;
      const ru=resp.url();
      if(!sameOfficialFamily(ru,url)) return;
      try{
        const data=await resp.json();
        const bodyText=JSON.stringify(data).slice(0,200000).toLowerCase();
        if(!/(job|position|recruit|career|岗位|职位)/i.test(ru+" "+bodyText)) return;
        const pageText=(await page.locator("body").innerText().catch(()=>'' )).slice(0,50000);
        const cycle=(pageText.match(/2027[^\n]{0,50}|[^\n]{0,50}2027/g)||[]).slice(0,3).join(" / ");
        recursiveJobs(data,{company,page_url:page.url(),response_url:ru,cycle_evidence:cycle},collector);
      }catch{}
    })();
    responseTasks.push(task);
  });
  try{
    await page.goto(url,{waitUntil:"domcontentloaded",timeout:30000});
    await page.waitForTimeout(2500);
    await scroll(page);
    await searchInputs(page);
    await Promise.allSettled(responseTasks);
    const body=(await page.locator("body").innerText().catch(()=>'' )).slice(0,80000);
    const cycleMatches=(body.match(/2027[^\n]{0,80}|[^\n]{0,80}2027/g)||[]);
    const has2027=cycleMatches.length>0;
    const links=await page.locator("a").evaluateAll(as=>as.map(a=>({href:a.href,text:(a.innerText||a.textContent||"").trim()})));
    const next=[];
    for(const a of links){
      if(!a.href||!sameOfficialFamily(a.href,url)) continue;
      if(/2027|校园|校招|应届|campus|graduate|student|position|职位|岗位|join us|career/i.test(a.text+" "+a.href)) next.push(a.href);
    }
    // DOM fallback: official links/cards whose visible text itself matches target keywords.
    for(const a of links){
      const low=(a.text||"").toLowerCase();
      if(!STRONG.some(k=>low.includes(k))) continue;
      collector.push({
        company,title:a.text.trim().slice(0,200),job_id:"",location:"",category:"官方页面候选",
        department:"",description:"",requirements:"",official_url:a.href||page.url(),
        official_api:"DOM:"+page.url(),cycle_evidence:has2027?cycleMatches.slice(0,2).join(" / "):"",
        extraction_path:"DOM anchor"
      });
    }
    await page.close();
    return {page_url:url,final_url:page.url(),has2027,cycle_evidence:cycleMatches.slice(0,5),next:[...new Set(next)].slice(0,6)};
  }catch(e){
    await page.close().catch(()=>{});
    return {page_url:url,error:String(e).slice(0,400),has2027:false,next:[]};
  }
}
async function main(){
  const sources=CONFIG.sources.filter(s=>s.mode==="portal_only" || s.browser_probe===true);
  const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  const results=[];
  for(const src of sources){
    const context=await browser.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"});
    const collector=[];
    const visited=new Set();
    const root=src.official_root || src.portal;
    const queue=[root];
    const pageResults=[];
    while(queue.length && visited.size<8){
      const u=queue.shift();
      const pr=await runPage(context,src.company,u,new URL(root).hostname,collector,visited);
      if(pr){
        pageResults.push(pr);
        for(const n of pr.next||[]) if(!visited.has(n)) queue.push(n);
      }
    }
    const jobs=uniqueJobs(collector);
    const has2027=pageResults.some(x=>x.has2027) || jobs.some(j=>/2027/.test(j.cycle_evidence));
    results.push({company:src.company,root_portal:root,seed_portal:src.portal,pages:pageResults,jobs,has2027,status:jobs.length?"BROWSER_OK":(has2027?"BROWSER_OK_0_MATCH":"BROWSER_NO_2027_EVIDENCE")});
    console.log(`${src.company}: pages=${pageResults.length}, jobs=${jobs.length}, 2027=${has2027}`);
    await context.close();
  }
  await browser.close();
  fs.writeFileSync(OUT,JSON.stringify({generated_at:new Date().toISOString(),results},null,2)+"\n","utf8");
}
await main();
