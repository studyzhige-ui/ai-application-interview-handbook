#!/usr/bin/env node
/**
 * Generic first-party browser discovery for current official campus recruitment portals.
 *
 * It starts from the official company recruitment/career URL in the registry,
 * follows official campus/student/job links, observes JSON/XHR issued by the
 * official site itself, and extracts job-like objects. No aggregator/search
 * result content is imported.
 */
import fs from "node:fs";
import { chromium } from "playwright";

const ROOT = process.cwd();
const CONFIG = JSON.parse(fs.readFileSync("market/jobs/official-2027-campus-sources.json","utf8"));
const OUT = process.argv[2] || "market/jobs/official-2027-browser-discovery.generated.json";

const SEARCH_TERMS = CONFIG.search_keywords || CONFIG.strong_agent_keywords || CONFIG.agent_keywords || [];
const STRONG = [...new Set([...SEARCH_TERMS,"fde"])].map(x=>x.toLowerCase());
const COMPANY_BUDGET_MS=Math.max(15000,Number(process.env.COMPANY_BUDGET_MS||"45000"));
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
    const suffixes=["mokahr.com","mioffice.cn","feishu.cn","myworkdayjobs.com","workdayjobs.com","zhiye.com","ashbyhq.com"];
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

function jobishObject(o){
  if(!o||typeof o!=="object"||Array.isArray(o)) return false;
  const title=pick(o,TITLE_KEYS);
  const id=pick(o,ID_KEYS);
  return Boolean(title && (id || pick(o,DESC_KEYS) || pick(o,REQ_KEYS)));
}
function responseListStats(root){
  let best=null;
  const totalKeys=["total","totalCount","count","recordsTotal","totalNum","totalSize","totalElements"];
  function nearbyTotal(parent){
    if(!parent||typeof parent!=="object"||Array.isArray(parent)) return null;
    for(const k of totalKeys){
      const n=Number(parent[k]);
      if(Number.isFinite(n)&&n>=0) return n;
    }
    for(const k of ["page","pageInfo","pageForm","pagination","info"]){
      const x=parent[k];
      if(x&&typeof x==="object"&&!Array.isArray(x)){
        for(const tk of totalKeys){
          const n=Number(x[tk]);
          if(Number.isFinite(n)&&n>=0) return n;
        }
      }
    }
    return null;
  }
  function walk(node,path,parent,depth){
    if(depth>10||node==null)return;
    if(Array.isArray(node)){
      const objs=node.filter(x=>x&&typeof x==="object"&&!Array.isArray(x));
      if(objs.length && objs.some(jobishObject)){
        const cand={rows:objs.length,total:nearbyTotal(parent),path};
        if(!best || cand.rows>best.rows || (cand.total!=null && best.total==null)) best=cand;
      }
      for(let i=0;i<node.length;i++)walk(node[i],path+"["+i+"]",node,depth+1);
      return;
    }
    if(typeof node!=="object")return;
    for(const [k,v] of Object.entries(node))walk(v,path+"."+k,node,depth+1);
  }
  walk(root,"$",null,0);
  return best||{rows:0,total:null,path:""};
}
function parseRequestContract(entry){
  const raw=entry?.post_data||"";
  let bodyType="none",body=null;
  if(raw){
    try{body=JSON.parse(raw);bodyType="json";}catch{
      body=Object.fromEntries(new URLSearchParams(raw));bodyType="form";
    }
  }
  return {bodyType,body};
}
const PAGE_KEYS=["current","currentPage","pageNum","pageIndex","pageNo","page"];
const OFFSET_KEYS=["offset"];
const SIZE_KEYS=["size","pageSize","limit"];
const KEYWORD_KEYS=["keyword","keyWord","key","postName","jobTitle","positionName","kw","keywords"];
function deepGetContainer(obj,keys,depth=0){
  if(!obj||typeof obj!=="object"||Array.isArray(obj)||depth>5)return null;
  for(const k of keys)if(Object.prototype.hasOwnProperty.call(obj,k))return {obj,key:k};
  for(const v of Object.values(obj)){
    const got=deepGetContainer(v,keys,depth+1);
    if(got)return got;
  }
  return null;
}
function blankListRequest(entry){
  if(!entry||entry.status!==200||entry.response_list_path===undefined)return false;
  if(/(?:^|\/)(?:detail|info|filter|condition|category|config|count)(?:\/|$)/i.test(new URL(entry.url||"https://invalid/").pathname))return false;
  if(!/(?:job|position|post|apply_list)/i.test(entry.url||""))return false;
  const {body}=parseRequestContract(entry);
  if(body&&typeof body==="object"){
    const kw=deepGetContainer(body,KEYWORD_KEYS);
    if(kw && String(kw.obj[kw.key]??"").trim()!=="")return false;
  }
  try{
    const u=new URL(entry.url);
    for(const k of KEYWORD_KEYS){
      if(u.searchParams.has(k)&&String(u.searchParams.get(k)||"").trim()!=="")return false;
    }
  }catch{}
  return true;
}
function cloneObject(v){return v==null?v:JSON.parse(JSON.stringify(v));}
function setKeywordBlank(obj){
  if(!obj||typeof obj!=="object")return;
  for(const k of KEYWORD_KEYS){
    const hit=deepGetContainer(obj,[k]);
    if(hit)hit.obj[hit.key]="";
  }
}
function pagingContract(entry){
  const parsed=parseRequestContract(entry);
  const body=cloneObject(parsed.body);
  const pageHit=body?deepGetContainer(body,PAGE_KEYS):null;
  const offsetHit=body?deepGetContainer(body,OFFSET_KEYS):null;
  const sizeHit=body?deepGetContainer(body,SIZE_KEYS):null;
  let urlPage=null,urlOffset=null,urlSize=null;
  let parsedUrl=null;
  try{
    parsedUrl=new URL(entry.url);
    urlPage=PAGE_KEYS.find(k=>parsedUrl.searchParams.has(k))||null;
    urlOffset=OFFSET_KEYS.find(k=>parsedUrl.searchParams.has(k))||null;
    urlSize=SIZE_KEYS.find(k=>parsedUrl.searchParams.has(k))||null;
  }catch{}
  const size=Math.max(1,Number(
    sizeHit?sizeHit.obj[sizeHit.key]:(urlSize&&parsedUrl?parsedUrl.searchParams.get(urlSize):entry.response_rows||50)
  )||50);
  return {parsed,body,pageHit,offsetHit,sizeHit,urlPage,urlOffset,urlSize,size};
}
async function replayCapturedFullPool(page,company,endpointLog,collector,cycle,category){
  const candidates=(endpointLog||[]).filter(entry=>{
    if(blankListRequest(entry))return true;
    if(!entry||entry.status!==200||entry.response_list_path===undefined)return false;
    let pathname="";
    try{pathname=new URL(entry.url||"https://invalid/").pathname;}catch{}
    if(/(?:^|\/)(?:detail|info|filter|condition|category|config|count)(?:\/|$)/i.test(pathname))return false;
    return /(?:job|position|post|apply_list)/i.test(entry.url||"");
  });
  if(!candidates.length)return {complete:false};
  candidates.sort((a,b)=>{
    const ab=blankListRequest(a),bb=blankListRequest(b);
    if(ab!==bb)return ab?-1:1;
    const at=a.response_count==null?-1:Number(a.response_count);
    const bt=b.response_count==null?-1:Number(b.response_count);
    if((bt>=0)!==(at>=0))return bt>=0?-1:1;
    return Number(b.response_rows||0)-Number(a.response_rows||0);
  });
  for(const seed of candidates){
    if(/\/api\/v1\/search\/job\/posts/i.test(seed.url))continue;
    if(/\/api\/outer\/ats-apply\/website\/jobs\/v2/i.test(seed.url))continue;
    if(/\/api\/api\/Jobs/i.test(seed.url))continue;
    const pc=pagingContract(seed);
    const hasPaging=Boolean(pc.pageHit||pc.offsetHit||pc.urlPage||pc.urlOffset);
    const observedRows=Math.max(0,Number(seed.response_rows||0));
    const observedTotal=seed.response_count==null?null:Math.max(0,Number(seed.response_count||0));
    if(!hasPaging){
      if(seed.response_list_path!==undefined){
        return {complete:true,total:observedTotal??observedRows,covered:observedRows,endpoint:seed.url,one_shot:true};
      }
      continue;
    }
    let covered=0,total=observedTotal,terminal=false,lastSignature="";
    for(let step=0;step<200;step++){
      const body=cloneObject(pc.body);
      if(body)setKeywordBlank(body);
      const u=new URL(seed.url);
      for(const k of KEYWORD_KEYS)if(u.searchParams.has(k))u.searchParams.set(k,"");
      const pageSize=Math.max(1,pc.size||50);
      if(pc.urlSize)u.searchParams.set(pc.urlSize,String(pageSize));
      if(pc.urlOffset)u.searchParams.set(pc.urlOffset,String(step*pageSize));
      if(pc.urlPage)u.searchParams.set(pc.urlPage,String(step+1));
      if(body){
        const ph=deepGetContainer(body,PAGE_KEYS);
        const oh=deepGetContainer(body,OFFSET_KEYS);
        const sh=deepGetContainer(body,SIZE_KEYS);
        if(sh)sh.obj[sh.key]=pageSize;
        if(oh)oh.obj[oh.key]=step*pageSize;
        if(ph)ph.obj[ph.key]=step+1;
      }
      let result=null;
      try{
        result=await page.evaluate(async ({url,method,bodyType,body})=>{
          const opts={method};
          if(method!=="GET"&&method!=="HEAD"){
            if(bodyType==="json"){
              opts.headers={"Content-Type":"application/json"};
              opts.body=JSON.stringify(body||{});
            }else if(bodyType==="form"){
              opts.headers={"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"};
              opts.body=new URLSearchParams(body||{}).toString();
            }
          }
          const r=await fetch(url,opts);
          let data={};try{data=await r.json();}catch{}
          return {status:r.status,data};
        },{url:u.href,method:seed.method||"POST",bodyType:pc.parsed.bodyType,body});
      }catch{break;}
      if(!result||result.status!==200)break;
      const stats=responseListStats(result.data);
      if(step===0&&stats.total!=null)total=stats.total;
      recursiveJobs(result.data,{
        company,page_url:page.url(),response_url:seed.url,
        cycle_evidence:(cycle||[]).join(" / "),category
      },collector);
      const sig=JSON.stringify(result.data).slice(0,12000);
      if(step>0&&sig===lastSignature)break;
      lastSignature=sig;
      const rows=Math.max(0,Number(stats.rows||0));
      covered+=rows;
      if(total===0&&rows===0){terminal=true;break;}
      if(total!=null&&total>0&&covered>=total){terminal=true;break;}
      if(rows===0||rows<pageSize){terminal=true;break;}
    }
    if(terminal)return {complete:true,total:total??covered,covered,endpoint:seed.url};
  }
  return {complete:false};
}
async function scroll(page){
  for(let i=0;i<2;i++){
    try{await page.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));}catch{}
    await page.waitForTimeout(500);
  }
  try{await page.evaluate(()=>window.scrollTo(0,0));}catch{}
}
function jobLinkLike(href){
  const u=href||"";
  if(/(?:\/position\/list(?:[?#]|$)|\/jobs?\/?(?:[?#]|$)|\/positions?\/?(?:[?#]|$))/i.test(u)) return false;
  return /(?:\/job\/[^/?#]+|\/jobs\/[^/?#]+|\/position\/[^/?#]+|job-info|job[_-]?detail|postdetail|positionid=|jobid=|#\/job\/[^/?#]+|#\/position\/[^/?#]+|jobs\.ashbyhq\.com\/[^/]+\/[0-9a-f-]{20,})/i.test(u);
}
function cycleSnippets(body){
  // Current-campus evidence: year labels are metadata only. A live first-party
  // campus/new-grad board is valid even when it does not print a graduation year.
  const lines=(body||"").split(/\n+/).map(x=>x.trim()).filter(Boolean);
  return lines.filter(x=>/(校园招聘|校招|应届|毕业生|campus|graduate|new\s*grad|student|university)/i.test(x)).slice(0,8);
}
async function jobLinksOnPage(page,keyword,requiredText=""){
  const links=await page.locator("a[href]").evaluateAll(as=>as.map(a=>{
    const card=a.closest('li,[class*="job-card"],[class*="job-list"],[class*="job-item"],[class*="search-job"]') || a.parentElement;
    return {
      href:a.href,
      text:(a.innerText||a.textContent||"").trim(),
      context:((card?.innerText||card?.textContent||"").trim()).slice(0,2400)
    };
  }));
  const needle=(requiredText||"").trim().toLowerCase();
  return links
    .filter(a=>a.href && jobLinkLike(a.href) && (!needle || (a.context||"").toLowerCase().includes(needle)))
    .map(a=>({href:a.href,title:(a.text||"").slice(0,240),context:a.context||"",keyword}));
}
async function openJobSearchSurface(page){
  const patterns=[
    /职位|岗位|招聘职位|职位列表|岗位投递|应届生招聘|校园招聘|校招岗位/i,
    /jobs?|positions?|openings?|campus recruitment|graduates?/i
  ];
  const selectors=["a","button","[role=button]","li","[class*=nav]","[class*=menu]","[class*=tab]"];
  for(const sel of selectors){
    const loc=page.locator(sel);
    const n=Math.min(await loc.count().catch(()=>0),80);
    for(let i=0;i<n;i++){
      const el=loc.nth(i);
      let txt="";
      try{txt=((await el.innerText())||"").trim();}catch{}
      if(!txt||txt.length>40||!patterns.some(p=>p.test(txt)))continue;
      try{
        await el.click({timeout:1200});
        await page.waitForTimeout(800);
        const url=page.url();
        const body=(await page.locator("body").innerText().catch(()=>"")).slice(0,12000);
        if(/职位|岗位|job|position|投递/i.test(body+" "+url)) return {clicked:true,text:txt,url};
      }catch{}
    }
  }
  return {clicked:false};
}

async function collectSearchPages(page,keyword,requiredText=""){
  const hits=[];
  const seenSignatures=new Set();
  const maxSteps=keyword==="__FULL_LIST__"?200:10;
  for(let step=0;step<maxSteps;step++){
    await page.waitForTimeout(step===0?650:350);
    await scroll(page);
    assertNoSecurityChallenge(page.url(),await page.locator("body").innerText().catch(()=>""));
    const pageHits=await jobLinksOnPage(page,keyword,requiredText);
    const signature=pageHits.map(x=>x.href).sort().join("|");
    if(signature && seenSignatures.has(signature)) break;
    if(signature) seenSignatures.add(signature);
    hits.push(...pageHits);

    const candidates=[
      page.getByRole("button",{name:/下一页|下页|Next/i}).last(),
      page.getByRole("link",{name:/下一页|下页|Next/i}).last(),
      page.locator("button").filter({hasText:/下一页|下页|Next/i}).last(),
      page.locator("[class*=next]").last(),
      page.locator('[aria-label*="next" i]').last()
    ];
    let moved=false;
    for(const next of candidates){
      try{
        if(await next.count()===0) continue;
        if(!(await next.isVisible())) continue;
        const disabled=(await next.isDisabled().catch(()=>false)) ||
          (await next.getAttribute("aria-disabled"))==="true" ||
          /disabled/i.test((await next.getAttribute("class"))||"");
        if(disabled) continue;
        const before=page.url()+"|"+signature;
        await next.click({timeout:1200});
        await page.waitForTimeout(500);
        assertNoSecurityChallenge(page.url(),await page.locator("body").innerText().catch(()=>""));
        const afterHits=await jobLinksOnPage(page,keyword,requiredText);
        const after=page.url()+"|"+afterHits.map(x=>x.href).sort().join("|");
        if(after!==before){ moved=true; break; }
      }catch(e){
        if(e?.code==="OFFICIAL_SECURITY_CHALLENGE") throw e;
      }
    }
    if(!moved) break;
  }
  return hits;
}
function assertNoSecurityChallenge(url,body){
  const guard=String(body||"").slice(0,5000);
  if(/\/web\/passport\/zp\/(?:security|verify)(?:[/?#.]|$)/i.test(url||"") ||
     /(?:^|\n)\s*(?:安全验证|访问异常)(?:\s|$)/i.test(guard)){
    const error=new Error("first-party security challenge; enumeration is incomplete");
    error.code="OFFICIAL_SECURITY_CHALLENGE";
    throw error;
  }
}
async function searchInputs(page,options={}){
  assertNoSecurityChallenge(page.url(),await page.locator("body").innerText().catch(()=>""));
  const prefix=(options.prefix||"").trim();
  const requiredText=(options.requiredText||"").trim();
  const inputs=page.locator("input");
  const n=Math.min(await inputs.count(),40);
  let target=null;
  for(let i=0;i<n;i++){
    const el=inputs.nth(i);
    const ph=((await el.getAttribute("placeholder"))||"").toLowerCase();
    const aria=((await el.getAttribute("aria-label"))||"").toLowerCase();
    const type=((await el.getAttribute("type"))||"").toLowerCase();
    if(/(搜索|职位|岗位|keyword|search)/i.test(ph+" "+aria) || type==="search"){
      target=el; break;
    }
  }
  if(!target) return {found:false,terms:[],hits:[]};
  const hits=[];
  const terms=[];
  for(const q of SEARCH_TERMS){
    try{
      await target.fill((prefix ? prefix+" " : "")+q);
      await target.press("Enter").catch(()=>{});
      await page.waitForTimeout(500);
      assertNoSecurityChallenge(page.url(),await page.locator("body").innerText().catch(()=>""));
      hits.push(...await collectSearchPages(page,q,requiredText));
      terms.push(q);
      // Some SPAs replace the search input after navigation/pagination.
      const refreshed=page.locator("input");
      const count=Math.min(await refreshed.count(),40);
      for(let i=0;i<count;i++){
        const el=refreshed.nth(i);
        const ph=((await el.getAttribute("placeholder"))||"").toLowerCase();
        const aria=((await el.getAttribute("aria-label"))||"").toLowerCase();
        const type=((await el.getAttribute("type"))||"").toLowerCase();
        if(/(搜索|职位|岗位|keyword|search)/i.test(ph+" "+aria) || type==="search"){ target=el; break; }
      }
    }catch(e){
      if(e?.code==="OFFICIAL_SECURITY_CHALLENGE") throw e;
    }
  }
  try{ await target.fill(""); await target.press("Enter").catch(()=>{}); }catch{}
  return {found:true,terms,hits};
}
function splitJobText(body,title){
  const text=(body||"").replace(/\r/g,"").replace(/\n{3,}/g,"\n\n").trim();
  const descRe=/(职位描述|岗位职责|工作职责|工作内容|岗位描述|Responsibilities|Job Description)/i;
  const reqRe=/(职位要求|岗位要求|任职要求|任职资格|Qualifications|Requirements)/i;
  const di=text.search(descRe);
  const ri=text.search(reqRe);
  let description="",requirements="";
  if(di>=0 && ri>di){
    description=text.slice(di,ri).trim();
    requirements=text.slice(ri).trim();
  }else if(ri>=0){
    description=text.slice(0,ri).trim();
    requirements=text.slice(ri).trim();
  }else{
    description=text;
  }
  if(title && description.startsWith(title)) description=description.slice(title.length).trim();
  return {description:description.slice(0,12000),requirements:requirements.slice(0,8000)};
}
async function scrapeSearchHit(context,company,hit,parentCycle,boardScope){
  const p=await context.newPage();
  try{
    await p.goto(hit.href,{waitUntil:"domcontentloaded",timeout:12000});
    await p.waitForTimeout(700);
    const body=(await p.locator("body").innerText().catch(()=>"")).slice(0,40000);
    if(/\/web\/passport\/zp\/security/i.test(p.url()) || /安全验证|访问异常|验证码/i.test(body.slice(0,3000))){
      return {
        company,title:(hit.title||"").slice(0,240),job_id:"",location:"",
        category:boardScope==="campus"?"官方校园招聘搜索结果":"官方招聘搜索结果",
        department:"",description:"",requirements:"",official_url:hit.href,
        official_api:"DOM-LIST:"+hit.href,cycle_evidence:(parentCycle||[]).join(" / "),
        extraction_path:"official list title (detail security challenge)",matched_keyword:hit.keyword
      };
    }
    let title=(await p.locator("h1").first().innerText().catch(()=>"")).trim();
    if(!title) title=(await p.locator("h2").first().innerText().catch(()=>"")).trim();
    if(!title) title=hit.title||"";
    const {description,requirements}=splitJobText(body,title);
    const cycle=[...new Set([...(parentCycle||[]),...cycleSnippets(body)])].slice(0,8).join(" / ");
    return {
      company,title:title.slice(0,240),job_id:"",location:"",category:boardScope==="campus"?"官方校园招聘搜索结果":"官方招聘搜索结果",
      department:"",description,requirements,official_url:p.url(),
      official_api:"DOM-DETAIL:"+hit.href,cycle_evidence:cycle,
      extraction_path:"official UI keyword search:"+hit.keyword,
      matched_keyword:hit.keyword
    };
  }catch{return null;}finally{await p.close().catch(()=>{});}
}
async function runPage(context,company,url,rootHost,collector,visited,endpointLog,boardScope,navigationTimeoutMs=12000,options={}){
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
        const req=resp.request();
        const entry={
          url:ru,method:req.method(),post_data:(req.postData()||"").slice(0,4000),
          status:resp.status(),content_type:ct,resource_type:req.resourceType()
        };
        const genericStats=responseListStats(data);
        if(genericStats.path){
          entry.response_count=genericStats.total;
          entry.response_rows=genericStats.rows;
          entry.response_list_path=genericStats.path;
        }
        if(/\/api\/v1\/search\/job\/posts/i.test(ru)){
          const d=data?.data||{};
          entry.response_count=Number(d?.count||0);
          entry.response_rows=Array.isArray(d?.job_post_list)?d.job_post_list.length:0;
          entry.response_list_path="$.data.job_post_list";
        }
        if(/\/api\/api\/Jobs(?:\\?|$)/i.test(ru)){
          const d=data?.data||{};
          entry.response_count=Number(d?.count||0);
          entry.response_rows=Array.isArray(d?.listData)?d.listData.length:0;
          entry.response_list_path="$.data.listData";
        }
        if(!endpointLog.some(x=>x.url===entry.url && x.method===entry.method && x.post_data===entry.post_data)) endpointLog.push(entry);
        const pageText=(await page.locator("body").innerText().catch(()=>"")).slice(0,50000);
        const cycle=cycleSnippets(pageText).join(" / ");
        if(!options.disableNetworkJobExtraction){
          recursiveJobs(data,{company,page_url:page.url(),response_url:ru,cycle_evidence:cycle,category:boardScope==="campus"?"官方校园招聘":"官方招聘"},collector);
        }
      }catch{}
    })();
    responseTasks.push(task);
  });
  try{
    await page.goto(url,{waitUntil:"domcontentloaded",timeout:navigationTimeoutMs});
    await page.waitForTimeout(900);
    await scroll(page);
    let beforeBody=(await page.locator("body").innerText().catch(()=>"")).slice(0,80000);
    assertNoSecurityChallenge(page.url(),beforeBody);
    let beforeCycle=cycleSnippets(beforeBody);
    await Promise.allSettled(responseTasks);
    const explicitRenderedZero=/(?:找到|共|合计)\s*[（(]?\s*0\s*[)）]?\s*(?:个)?\s*(?:职位|岗位)|(?:暂无|没有|无)\s*(?:在招)?\s*(?:职位|岗位)/i.test(beforeBody);
    if(boardScope==="campus" && explicitRenderedZero){
      const finalUrl=page.url();
      await page.close();
      return {
        page_url:url,final_url:finalUrl,hasCampusEvidence:beforeCycle.length>0,cycle_evidence:beforeCycle,
        next:[],search_control_found:false,navigation_action:{clicked:false},
        search_terms_attempted:[],search_hit_links:0,list_scan_complete:true,list_links_seen:0,
        dom_explicit_zero:true,source_total:0
      };
    }
    // Moka exposes a stable jobs/v2 contract during the first official page load.
    // Once captured, stop spending browser time on keyword UI replay: the Moka
    // adapter will paginate the entire first-party pool deterministically.
    const mokaContractSeen=endpointLog.some(e=>/\/api\/outer\/ats-apply\/website\/jobs\/v2(?:\\?|$)/.test(e.url));
    if(mokaContractSeen){
      const finalUrl=page.url();
      await page.close();
      return {
        page_url:url,final_url:finalUrl,hasCampusEvidence:beforeCycle.length>0,cycle_evidence:beforeCycle,
        next:[],search_control_found:false,navigation_action:{clicked:false},
        search_terms_attempted:[],search_hit_links:0,list_scan_complete:false,list_links_seen:0,
        moka_contract_discovered:true
      };
    }

    // Feishu-family ATS pages expose signed first-party list calls. Exhaust the
    // blank-query list first: this enumerates the *entire* official pool rather
    // than proving only a set of target keywords.
    let signedFeishuSeen=endpointLog.some(e=>/\/api\/v1\/search\/job\/posts/i.test(e.url));
    if(!signedFeishuSeen){
      try{
        const host=new URL(page.url()).hostname;
        if(/\.jobs\.feishu\.cn$/i.test(host)){
          await page.goto(canonicalFeishuListUrl(page.url(),1,10),{waitUntil:"domcontentloaded",timeout:navigationTimeoutMs});
          await page.waitForTimeout(700);
          await Promise.allSettled(responseTasks);
          signedFeishuSeen=endpointLog.some(e=>/\/api\/v1\/search\/job\/posts/i.test(e.url));
        }
      }catch{}
    }
    if(signedFeishuSeen){
      const fullPoolProof=await exhaustFeishuSignedPool(page,endpointLog,responseTasks,navigationTimeoutMs);
      if(fullPoolProof.full_pool_complete){
        const bodyNow=(await page.locator("body").innerText().catch(()=>"")).slice(0,80000);
        const cycleNow=[...new Set([...beforeCycle,...cycleSnippets(bodyNow)])].slice(0,10);
        const finalUrl=page.url();
        await page.close();
        return {
          page_url:url,final_url:finalUrl,hasCampusEvidence:cycleNow.length>0,cycle_evidence:cycleNow,
          next:[],search_control_found:true,navigation_action:{clicked:false},
          search_terms_attempted:[],search_hit_links:0,
          list_scan_complete:true,list_links_seen:fullPoolProof.full_pool_covered,
          signed_feishu_full_pool:true,source_total:fullPoolProof.full_pool_total
        };
      }
    }
    // Sangfor's public campus API is session-bound: direct requests return
    // 401, while the official page's same-origin session can page /api/api/Jobs.
    // Exhaust it inside the browser context and use source count as the terminal proof.
    const sangforSeed=endpointLog.find(e=>e.status===200 && /\/api\/api\/Jobs(?:\\?|$)/i.test(e.url));
    if(sangforSeed){
      let seedBody={};
      try{seedBody=JSON.parse(sangforSeed.post_data||"{}");}catch{}
      const total=Math.max(0,Number(sangforSeed.response_count||0));
      const pageSize=Math.max(1,Number(seedBody.pageSize||sangforSeed.response_rows||10));
      let fetched=Math.max(0,Number(sangforSeed.response_rows||0));
      let pageNo=Math.max(1,Number(seedBody.page||1))+1;
      let terminal=(total===0 && fetched===0);
      while(!terminal && pageNo<=100 && fetched<total){
        const payload={
          channelId:Number(seedBody.channelId||101),page:pageNo,pageSize,
          departmentId:0,functionId:0,kw:"",locationId:0,workPlaceId:0
        };
        let result=null;
        try{
          result=await page.evaluate(async ({url,payload})=>{
            const r=await fetch(url,{
              method:"POST",headers:{"Content-Type":"application/json"},
              body:JSON.stringify(payload)
            });
            let body={}; try{body=await r.json();}catch{}
            return {status:r.status,body};
          },{url:sangforSeed.url.split("?")[0],payload});
        }catch{break;}
        if(!result||result.status!==200) break;
        const d=result.body?.data||{};
        const rows=Array.isArray(d.listData)?d.listData:[];
        recursiveJobs(
          result.body,
          {company,page_url:page.url(),response_url:sangforSeed.url.split("?")[0],
           cycle_evidence:beforeCycle.join(" / "),category:"官方校园招聘"},
          collector
        );
        fetched+=rows.length;
        if(!rows.length || rows.length<pageSize || (total>0 && fetched>=total)){terminal=true;break;}
        pageNo++;
      }
      if(terminal || (total>0 && fetched>=total)){
        const finalUrl=page.url();
        await page.close();
        return {
          page_url:url,final_url:finalUrl,hasCampusEvidence:beforeCycle.length>0,
          cycle_evidence:beforeCycle,next:[],search_control_found:false,
          navigation_action:{clicked:false},search_terms_attempted:[],
          search_hit_links:0,list_scan_complete:true,list_links_seen:fetched,
          sangfor_full_pool:true,source_total:total
        };
      }
    }

    const genericPool=options.disableNetworkJobExtraction ? {complete:false} : await replayCapturedFullPool(
      page,company,endpointLog,collector,beforeCycle,
      boardScope==="campus"?"官方校园招聘":"官方招聘"
    );
    if(genericPool.complete){
      const finalUrl=page.url();
      await page.close();
      return {
        page_url:url,final_url:finalUrl,hasCampusEvidence:beforeCycle.length>0,
        cycle_evidence:beforeCycle,next:[],search_control_found:false,
        navigation_action:{clicked:false},search_terms_attempted:[],
        search_hit_links:0,list_scan_complete:true,list_links_seen:genericPool.covered||0,
        generic_full_pool:true,source_total:genericPool.total,source_endpoint:genericPool.endpoint
      };
    }

    const initialHits=options.includeInitialList
      ? await collectSearchPages(page,"__INITIAL__",options.requiredCompanyText||"")
      : [];
    let search=await searchInputs(page,{prefix:options.searchPrefix||"",requiredText:options.requiredCompanyText||""});
    if(initialHits.length) search.hits.unshift(...initialHits);
    let navAction={clicked:false};
    let listScanComplete=false;
    let listHits=[];
    if(!search.found){
      navAction=await openJobSearchSurface(page);
      if(navAction.clicked){
        await page.waitForTimeout(900);
        beforeBody=(await page.locator("body").innerText().catch(()=>"")).slice(0,80000);
        assertNoSecurityChallenge(page.url(),beforeBody);
        beforeCycle=[...new Set([...beforeCycle,...cycleSnippets(beforeBody)])];
        await Promise.allSettled(responseTasks);
        let postNavFeishu=endpointLog.some(e=>/\/api\/v1\/search\/job\/posts/i.test(e.url));
        if(!postNavFeishu && /\.jobs\.feishu\.cn$/i.test(new URL(page.url()).hostname)){
          try{
            const href=canonicalFeishuListUrl(page.url(),1,10);
            await page.goto(href,{waitUntil:"domcontentloaded",timeout:navigationTimeoutMs});
            await page.waitForTimeout(900);
          }catch{}
          await Promise.allSettled(responseTasks);
          postNavFeishu=endpointLog.some(e=>/\/api\/v1\/search\/job\/posts/i.test(e.url));
        }
        if(postNavFeishu){
          const proof=await exhaustFeishuSignedPool(page,endpointLog,responseTasks,navigationTimeoutMs);
          if(proof.full_pool_complete){
            const finalUrl=page.url();
            await page.close();
            return {
              page_url:url,final_url:finalUrl,hasCampusEvidence:beforeCycle.length>0,
              cycle_evidence:beforeCycle,next:[],search_control_found:true,
              navigation_action:navAction,search_terms_attempted:[],
              search_hit_links:0,list_scan_complete:true,
              list_links_seen:proof.full_pool_covered,signed_feishu_full_pool:true,
              source_total:proof.full_pool_total
            };
          }
        }
        const postNavGeneric=options.disableNetworkJobExtraction ? {complete:false} : await replayCapturedFullPool(
          page,company,endpointLog,collector,beforeCycle,
          boardScope==="campus"?"官方校园招聘":"官方招聘"
        );
        if(postNavGeneric.complete){
          const finalUrl=page.url();
          await page.close();
          return {
            page_url:url,final_url:finalUrl,hasCampusEvidence:beforeCycle.length>0,
            cycle_evidence:beforeCycle,next:[],search_control_found:false,
            navigation_action:navAction,search_terms_attempted:[],
            search_hit_links:0,list_scan_complete:true,list_links_seen:postNavGeneric.covered||0,
            generic_full_pool:true,source_total:postNavGeneric.total,source_endpoint:postNavGeneric.endpoint
          };
        }
        search=await searchInputs(page,{prefix:options.searchPrefix||"",requiredText:options.requiredCompanyText||""});
      }
    }
    // A fixed official job-list page is enough. If the site has no search input,
    // exhaustively paginate the visible official list and let captured XHR/JSON
    // provide full JD fields; title-matching links are opened as an additional fallback.
    if(!search.found){
      listHits=await collectSearchPages(page,"__FULL_LIST__",options.requiredCompanyText||"");
      // An empty page without a search control is not proof that the official
      // job pool has zero jobs. Require actual job-list evidence before
      // certifying a full-list scan.
      listScanComplete=false;
      for(const h of listHits){
        const low=(h.title||"").toLowerCase();
        if(STRONG.some(k=>low.includes(k))) search.hits.push(h);
      }
    }
    await Promise.allSettled(responseTasks);

    const postSearchFeishu=endpointLog.some(e=>e.status===200 && /\/api\/v1\/search\/job\/posts/i.test(e.url));
    if(postSearchFeishu){
      try{
        const blankUrl=canonicalFeishuListUrl(page.url(),1,10);
        if(page.url()!==blankUrl){
          await page.goto(blankUrl,{waitUntil:"domcontentloaded",timeout:navigationTimeoutMs});
          await page.waitForTimeout(500);
        }
      }catch{}
      await collectSearchPages(page,"__FULL_LIST__");
      await Promise.allSettled(responseTasks);
      const proof=feishuKeywordCoverage(endpointLog);
      if(proof.full_pool_complete){
        const finalUrl=page.url();
        await page.close();
        return {
          page_url:url,final_url:finalUrl,hasCampusEvidence:beforeCycle.length>0,
          cycle_evidence:beforeCycle,next:[],search_control_found:true,
          navigation_action:navAction,search_terms_attempted:search.terms,
          search_hit_links:search.hits.length,list_scan_complete:true,
          list_links_seen:proof.full_pool_covered,signed_feishu_full_pool:true,
          source_total:proof.full_pool_total
        };
      }
    }

    const postSearchGeneric=options.disableNetworkJobExtraction ? {complete:false} : await replayCapturedFullPool(
      page,company,endpointLog,collector,beforeCycle,
      boardScope==="campus"?"官方校园招聘":"官方招聘"
    );
    if(postSearchGeneric.complete){
      const finalUrl=page.url();
      await page.close();
      return {
        page_url:url,final_url:finalUrl,hasCampusEvidence:beforeCycle.length>0,
        cycle_evidence:beforeCycle,next:[],search_control_found:search.found,
        navigation_action:navAction,search_terms_attempted:search.terms,
        search_hit_links:search.hits.length,list_scan_complete:true,
        list_links_seen:postSearchGeneric.covered||0,generic_full_pool:true,
        source_total:postSearchGeneric.total,source_endpoint:postSearchGeneric.endpoint
      };
    }

    const body=(await page.locator("body").innerText().catch(()=>"")).slice(0,80000);
    const cycleMatches=[...new Set([...beforeCycle,...cycleSnippets(body)])].slice(0,10);
    // Exact first-party detail URLs may not expose a searchable list or JSON
    // endpoint. Capture the rendered JD itself when the page title is a target
    // AI/Agent engineering role.
    if(/(?:\/position\/|\/job\/|jobdetail|positiondetail|#\/campus\/position\/)/i.test(url)){
      let detailTitle=(await page.locator("h1").first().innerText().catch(()=>"")).trim();
      if(!detailTitle) detailTitle=(await page.locator("h2").first().innerText().catch(()=>"")).trim();
      const detailBlob=(detailTitle+" "+body).toLowerCase();
      if(detailTitle && STRONG.some(k=>detailBlob.includes(k))){
        const jd=splitJobText(body,detailTitle);
        collector.push({
          company,title:detailTitle.slice(0,240),job_id:"",location:"",
          category:boardScope==="campus"?"官方校园招聘详情":"官方招聘详情",
          department:"",description:jd.description,requirements:jd.requirements,
          official_url:page.url(),official_api:"DOM-DETAIL:"+url,
          cycle_evidence:cycleMatches.join(" / "),
          extraction_path:"official DOM detail page"
        });
      }
    }
    const hasCampusEvidence=cycleMatches.length>0;
    const links=await page.locator("a[href]").evaluateAll(as=>as.map(a=>({href:a.href,text:(a.innerText||a.textContent||"").trim()})));
    const next=[];
    for(const a of links){
      if(!a.href||!sameOfficialFamily(a.href,url)) continue;
      if(/校园|校招|应届|招聘|人才|加入我们|加入|campus|graduate|student|position|职位|岗位|join us|career|jobs?/i.test(a.text+" "+a.href)) next.push(a.href);
    }

    const uniqueHits=[];
    const seenHits=new Set();
    for(const hit of search.hits){
      if(!hit.href||!sameOfficialFamily(hit.href,page.url())) continue;
      const key=hit.href+"|"+hit.keyword;
      if(seenHits.has(key)) continue;
      seenHits.add(key); uniqueHits.push(hit);
    }
    const feishuJsonCaptured=endpointLog.some(e=>/\/api\/v1\/search\/job\/posts/i.test(e.url));
    const detailHits=feishuJsonCaptured?[]:uniqueHits.slice(0,30);
    for(let i=0;i<detailHits.length;i+=4){
      const batch=await Promise.all(detailHits.slice(i,i+4).map(h=>scrapeSearchHit(context,company,h,cycleMatches,boardScope)));
      for(const j of batch) if(j) collector.push(j);
    }

    const finalUrl=page.url();
    await page.close();
    return {
      page_url:url,final_url:finalUrl,hasCampusEvidence,cycle_evidence:cycleMatches,
      next:[...new Set(next)].slice(0,10),
      search_control_found:search.found,
      navigation_action:navAction,
      search_terms_attempted:search.terms,
      search_hit_links:uniqueHits.length,
      list_scan_complete:listScanComplete,
      list_links_seen:listHits.length
    };
  }catch(e){
    await page.close().catch(()=>{});
    return {page_url:url,error:String(e).slice(0,400),hasCampusEvidence:false,next:[],search_control_found:false,search_terms_attempted:[]};
  }
}
function feishuKeywordCoverage(endpointLog){
  const eps=(endpointLog||[]).filter(e=>e.status===200 && /\/api\/v1\/search\/job\/posts/i.test(e.url));
  if(!eps.length) return {complete:false,terms:[]};
  const byKeyword=new Map();
  for(const e of eps){
    let body={};
    try{body=JSON.parse(e.post_data||"{}");}catch{}
    const keyword=String(body.keyword??"").toLowerCase();
    const limit=Math.max(1,Number(body.limit||10));
    const offset=Math.max(0,Number(body.offset||0));
    if(!byKeyword.has(keyword)) byKeyword.set(keyword,[]);
    byKeyword.get(keyword).push({
      offset,limit,total:Math.max(0,Number(e.response_count||0)),
      rows:Math.max(0,Number(e.response_rows||0))
    });
  }
  const required=["",...SEARCH_TERMS.map(x=>x.toLowerCase())];
  const completeTerm=q=>{
    const xs=(byKeyword.get(q)||[]).sort((a,b)=>a.offset-b.offset);
    if(!xs.length) return false;
    const total=Math.max(...xs.map(x=>x.total));
    let covered=0;
    for(const x of xs){
      if(x.offset>covered) return false;
      covered=Math.max(covered,x.offset+x.rows);
      if(total===0 && x.offset===0 && x.rows===0) return true;
      if(total>0 && covered>=total) return true;
      if(x.rows<x.limit) return true;
    }
    return total>0 && covered>=total;
  };
  const done=required.filter(completeTerm);
  const fullPoolComplete=completeTerm("");
  const blanks=(byKeyword.get("")||[]).sort((a,b)=>a.offset-b.offset);
  const fullTotal=blanks.length?Math.max(...blanks.map(x=>x.total)):0;
  const fullCovered=blanks.reduce((m,x)=>Math.max(m,x.offset+x.rows),0);
  return {
    complete:fullPoolComplete || done.length===required.length,
    full_pool_complete:fullPoolComplete,
    full_pool_total:fullTotal,
    full_pool_covered:fullCovered,
    terms:done
  };
}

function canonicalFeishuListUrl(raw,current=1,limit=10){
  const u=new URL(raw);
  let path=u.pathname.replace(/\/+$/,"");
  if(!/\/position\/list$/i.test(path)) path=path+"/position/list";
  u.pathname=path;
  u.searchParams.set("keywords","");
  u.searchParams.set("current",String(current));
  u.searchParams.set("limit",String(limit));
  for(const k of ["category","location","type","job_hot_flag","functionCategory","tag"]){
    if(!u.searchParams.has(k))u.searchParams.set(k,"");
  }
  return u.href;
}

async function clickFeishuNext(page,minOffset){
  const candidates=[
    page.getByRole("button",{name:/下一页|下页|Next/i}).last(),
    page.getByRole("link",{name:/下一页|下页|Next/i}).last(),
    page.locator("button").filter({hasText:/下一页|下页|Next/i}).last(),
    page.locator("[class*=pagination] [class*=next]").last(),
    page.locator("[class*=next]").last(),
    page.locator('[aria-label*="next" i]').last()
  ];
  for(const next of candidates){
    try{
      if(await next.count()===0||!(await next.isVisible()))continue;
      const disabled=(await next.isDisabled().catch(()=>false)) ||
        (await next.getAttribute("aria-disabled"))==="true" ||
        /disabled/i.test((await next.getAttribute("class"))||"");
      if(disabled)continue;
      const responsePromise=page.waitForResponse(resp=>{
        if(resp.status()!==200||!/\/api\/v1\/search\/job\/posts/i.test(resp.url()))return false;
        try{
          const b=JSON.parse(resp.request().postData()||"{}");
          return String(b.keyword??"")==="" && Number(b.offset||0)>=minOffset;
        }catch{return false;}
      },{timeout:6000}).catch(()=>null);
      await next.click({timeout:2500});
      const resp=await responsePromise;
      await page.waitForTimeout(120);
      if(resp)return true;
    }catch{}
  }
  return false;
}

async function exhaustFeishuSignedPool(page,endpointLog,responseTasks,navigationTimeoutMs){
  await Promise.allSettled(responseTasks);
  let proof=feishuKeywordCoverage(endpointLog);
  if(proof.full_pool_complete)return proof;

  // Always begin from the first official list page. Subsequent pages are reached
  // through the site's own paginator so its runtime signature/session stays valid.
  try{
    const first=canonicalFeishuListUrl(page.url(),1,10);
    if(page.url()!==first){
      await page.goto(first,{waitUntil:"domcontentloaded",timeout:navigationTimeoutMs});
      await page.waitForTimeout(650);
      await Promise.allSettled(responseTasks);
      proof=feishuKeywordCoverage(endpointLog);
      if(proof.full_pool_complete)return proof;
    }
  }catch{}

  let stalls=0;
  for(let step=0;step<220;step++){
    proof=feishuKeywordCoverage(endpointLog);
    if(proof.full_pool_complete)return proof;
    const total=Math.max(0,Number(proof.full_pool_total||0));
    const covered=Math.max(0,Number(proof.full_pool_covered||0));
    if(total===0&&covered===0)return proof;

    const moved=await clickFeishuNext(page,covered);
    await Promise.allSettled(responseTasks);
    const after=feishuKeywordCoverage(endpointLog);
    if(after.full_pool_complete)return after;
    if(!moved || Number(after.full_pool_covered||0)<=covered)stalls++; else stalls=0;
    if(stalls>=3)break;
  }
  return feishuKeywordCoverage(endpointLog);
}

async function processSource(browser,src){
  const context=await browser.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"});
  const collector=[];
  const endpointLog=[];
  const visited=new Set();
  const root=src.official_root || src.portal;
  const jobList=src.search_url || src.job_list_url || src.portal;
  const boardScope=src.board_scope || (src.current_campus_board?"campus":"official_recruiting");
  const queue=[jobList, ...(src.extra_job_list_urls||src.extra_portals||[])];
  const pageResults=[];
  const navigationTimeoutMs=Math.max(8000,Number(src.browser_navigation_timeout_ms||12000));
  const isFeishuFamily=/\/api\/v1\/search\/job\/posts/i.test((endpointLog||[]).map(e=>e.url).join(" "));
  const defaultBudget=src.mode==="feishu_direct"?360000:(src.mode==="portal_only"?180000:COMPANY_BUDGET_MS);
  const companyBudgetMs=Math.max(15000,Number(src.browser_company_budget_ms||defaultBudget));
  const started=Date.now();
  let timer=null;
  const work=(async()=>{
    while(queue.length && visited.size<6){
      if(Date.now()-started>companyBudgetMs) throw new Error("company enumeration budget exceeded");
      const u=queue.shift();
      const pr=await runPage(
        context,src.company,u,new URL(root).hostname,collector,visited,endpointLog,boardScope,navigationTimeoutMs,{
          searchPrefix:src.search_prefix||"",
          requiredCompanyText:src.required_company_text||"",
          disableNetworkJobExtraction:Boolean(src.disable_network_job_extraction),
          includeInitialList:Boolean(src.include_initial_list)
        }
      );
      if(pr){
        pageResults.push(pr);
        // Do not crawl arbitrary site navigation during recurring collection.
        // The fixed job_list_url is the contract; pagination/search stays inside runPage().
        // Additional official lists must be declared explicitly in extra_job_list_urls.
      }
    }
    const allJobs=uniqueJobs(collector);
    // Captured first-party XHR may prove the list even when the DOM exposes no links.
    if(!pageResults.some(x=>x.search_control_found) && allJobs.length>0){
      for(const pr of pageResults){
        if(!pr.search_control_found) pr.list_scan_complete=true;
      }
    }
    // The live first-party campus/new-grad board itself is the time gate.
    // Graduation year / project label is metadata only and must never decide
    // whether an otherwise live official job pool is enumerable.
    const jobs=allJobs;
    const searched=new Set(pageResults.flatMap(x=>x.search_terms_attempted||[]));
    const networkProof=feishuKeywordCoverage(endpointLog);
    const fullKeywordSearch=SEARCH_TERMS.every(k=>searched.has(k));
    const keywordSearchComplete=Boolean(src.keyword_search_is_terminal) && fullKeywordSearch;
    const listScanComplete=pageResults.some(x=>x.list_scan_complete===true) || networkProof.full_pool_complete || keywordSearchComplete;
    const pageErrors=pageResults.filter(x=>x.error).length;
    let status;
    if(listScanComplete && jobs.length) status="BROWSER_ENUMERATED";
    else if(listScanComplete && !jobs.length && pageErrors===0) status="BROWSER_ENUMERATED_ZERO";
    else if(pageErrors===0) status="BROWSER_CAMPUS_NEEDS_ADAPTER";
    else status="BROWSER_ERROR";
    console.log(`${src.company}: pages=${pageResults.length}, jobs=${jobs.length}, searched=${searched.size}/${SEARCH_TERMS.length}, status=${status}`);
    return {
      company:src.company,board_scope:boardScope,root_portal:root,seed_portal:src.portal,job_list_url:jobList,pages:pageResults,
      endpoints:endpointLog.slice(0,120),jobs,status,
      search_terms_attempted:[...searched],search_terms_expected:SEARCH_TERMS,
      full_keyword_search:fullKeywordSearch,list_scan_complete:listScanComplete
    };
  })();
  const timeout=new Promise((_,reject)=>{
    timer=setTimeout(()=>reject(new Error(`company enumeration timed out after ${companyBudgetMs}ms`)),companyBudgetMs);
  });
  try{
    return await Promise.race([work,timeout]);
  }catch(e){
    const proof=feishuKeywordCoverage(endpointLog);
    const jobs=uniqueJobs(collector);
    if(proof.full_pool_complete){
      const status=jobs.length?"BROWSER_ENUMERATED":"BROWSER_ENUMERATED_ZERO";
      console.log(`${src.company}: browser terminal via signed Feishu network proof, jobs=${jobs.length}, status=${status}`);
      return {
        company:src.company,board_scope:boardScope,root_portal:root,seed_portal:src.portal,job_list_url:jobList,
        pages:pageResults,endpoints:endpointLog.slice(0,120),jobs,status,
        error:"browser UI ended after exhaustive signed Feishu pagination: "+String(e).slice(0,300),
        search_terms_attempted:SEARCH_TERMS,search_terms_expected:SEARCH_TERMS,
        full_keyword_search:false,list_scan_complete:true,network_pagination_proof:true
      };
    }
    console.log(`${src.company}: browser ERROR ${String(e).slice(0,300)}`);
    return {company:src.company,board_scope:boardScope,root_portal:root,seed_portal:src.portal,job_list_url:jobList,pages:pageResults,endpoints:endpointLog.slice(0,120),jobs,status:"BROWSER_ERROR",error:String(e).slice(0,500),search_terms_attempted:[],search_terms_expected:SEARCH_TERMS,full_keyword_search:false};
  }finally{
    if(timer) clearTimeout(timer);
    work.catch(()=>{});
    await context.close().catch(()=>{});
  }
}

async function main(){
  // Dedicated API / direct ATS adapters are enumerated later by the sync layer.
  // Playwright is reserved for sources that genuinely need browser/XHR discovery.
  const allSources=CONFIG.sources.filter(s=>(s.mode==="portal_only" || s.mode==="feishu_direct") && !s.moka_org_id);
  const shardCount=Math.max(1,Number(process.env.SHARD_COUNT||"1"));
  const shardIndex=Math.max(0,Number(process.env.SHARD_INDEX||"0"));
  const sources=allSources.filter((_,i)=>i % shardCount === shardIndex);
  const browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  const results=[];
  const concurrency=Math.max(1,Number(process.env.BROWSER_COMPANY_CONCURRENCY||"8"));
  for(let i=0;i<sources.length;i+=concurrency){
    const chunk=sources.slice(i,i+concurrency);
    results.push(...await Promise.all(chunk.map(src=>processSource(browser,src))));
  }
  await browser.close();
  results.sort((a,b)=>a.company.localeCompare(b.company,"zh-CN"));
  fs.writeFileSync(OUT,JSON.stringify({generated_at:new Date().toISOString(),shard_index:shardIndex,shard_count:shardCount,source_count:sources.length,concurrency,results},null,2)+"\n","utf8");
}
await main();
