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

const SEARCH_TERMS = CONFIG.strong_agent_keywords || CONFIG.agent_keywords || [];
const STRONG = SEARCH_TERMS.map(x=>x.toLowerCase());
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
async function scroll(page){
  for(let i=0;i<2;i++){
    await page.evaluate(()=>window.scrollTo(0,document.body.scrollHeight));
    await page.waitForTimeout(500);
  }
  await page.evaluate(()=>window.scrollTo(0,0));
}
function jobLinkLike(href){
  return /(?:\/job\/|\/jobs\/|\/position\/|job-info|postdetail|positionid=|jobid=|#\/job\/|#\/position\/|jobs\.ashbyhq\.com\/[^/]+\/[0-9a-f-]{20,})/i.test(href||"");
}
function cycleSnippets(body){
  // Current-campus evidence: year labels are metadata only. A live first-party
  // campus/new-grad board is valid even when it does not print a graduation year.
  const lines=(body||"").split(/\n+/).map(x=>x.trim()).filter(Boolean);
  return lines.filter(x=>/(校园招聘|校招|应届|毕业生|campus|graduate|new\s*grad|student|university)/i.test(x)).slice(0,8);
}
async function jobLinksOnPage(page,keyword){
  const links=await page.locator("a[href]").evaluateAll(as=>as.map(a=>({
    href:a.href,
    text:(a.innerText||a.textContent||"").trim()
  })));
  return links
    .filter(a=>a.href && jobLinkLike(a.href))
    .map(a=>({href:a.href,title:(a.text||"").slice(0,240),keyword}));
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

async function collectSearchPages(page,keyword){
  const hits=[];
  const seenSignatures=new Set();
  for(let step=0;step<30;step++){
    await page.waitForTimeout(step===0?650:350);
    await scroll(page);
    const pageHits=await jobLinksOnPage(page,keyword);
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
        const afterHits=await jobLinksOnPage(page,keyword);
        const after=page.url()+"|"+afterHits.map(x=>x.href).sort().join("|");
        if(after!==before){ moved=true; break; }
      }catch{}
    }
    if(!moved) break;
  }
  return hits;
}
async function searchInputs(page){
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
      await target.fill(q);
      await target.press("Enter").catch(()=>{});
      await page.waitForTimeout(500);
      terms.push(q);
      hits.push(...await collectSearchPages(page,q));
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
    }catch{}
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
async function runPage(context,company,url,rootHost,collector,visited,endpointLog,boardScope){
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
        if(!endpointLog.some(x=>x.url===entry.url && x.method===entry.method && x.post_data===entry.post_data)) endpointLog.push(entry);
        const pageText=(await page.locator("body").innerText().catch(()=>"")).slice(0,50000);
        const cycle=cycleSnippets(pageText).join(" / ");
        recursiveJobs(data,{company,page_url:page.url(),response_url:ru,cycle_evidence:cycle,category:boardScope==="campus"?"官方校园招聘":"官方招聘"},collector);
      }catch{}
    })();
    responseTasks.push(task);
  });
  try{
    await page.goto(url,{waitUntil:"domcontentloaded",timeout:12000});
    await page.waitForTimeout(900);
    await scroll(page);
    let beforeBody=(await page.locator("body").innerText().catch(()=>"")).slice(0,80000);
    let beforeCycle=cycleSnippets(beforeBody);
    let search=await searchInputs(page);
    let navAction={clicked:false};
    let listScanComplete=false;
    let listHits=[];
    if(!search.found){
      navAction=await openJobSearchSurface(page);
      if(navAction.clicked){
        beforeBody=(await page.locator("body").innerText().catch(()=>"")).slice(0,80000);
        beforeCycle=[...new Set([...beforeCycle,...cycleSnippets(beforeBody)])];
        search=await searchInputs(page);
      }
    }
    // A fixed official job-list page is enough. If the site has no search input,
    // exhaustively paginate the visible official list and let captured XHR/JSON
    // provide full JD fields; title-matching links are opened as an additional fallback.
    if(!search.found){
      listHits=await collectSearchPages(page,"__FULL_LIST__");
      listScanComplete=true;
      for(const h of listHits){
        const low=(h.title||"").toLowerCase();
        if(STRONG.some(k=>low.includes(k))) search.hits.push(h);
      }
    }
    await Promise.allSettled(responseTasks);

    const body=(await page.locator("body").innerText().catch(()=>"")).slice(0,80000);
    const cycleMatches=[...new Set([...beforeCycle,...cycleSnippets(body)])].slice(0,10);
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
    const detailHits=uniqueHits.slice(0,30);
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
  const started=Date.now();
  let timer=null;
  const work=(async()=>{
    while(queue.length && visited.size<6){
      if(Date.now()-started>COMPANY_BUDGET_MS) throw new Error("company enumeration budget exceeded");
      const u=queue.shift();
      const pr=await runPage(context,src.company,u,new URL(root).hostname,collector,visited,endpointLog,boardScope);
      if(pr){
        pageResults.push(pr);
        // Do not crawl arbitrary site navigation during recurring collection.
        // The fixed job_list_url is the contract; pagination/search stays inside runPage().
        // Additional official lists must be declared explicitly in extra_job_list_urls.
      }
    }
    const allJobs=uniqueJobs(collector);
    // The live first-party campus/new-grad board itself is the time gate.
    // Graduation year / project label is metadata only and must never decide
    // whether an otherwise live official job pool is enumerable.
    const jobs=allJobs;
    const searched=new Set(pageResults.flatMap(x=>x.search_terms_attempted||[]));
    const listScanComplete=pageResults.some(x=>x.list_scan_complete===true);
    const fullKeywordSearch=SEARCH_TERMS.every(k=>searched.has(k)) || listScanComplete;
    const pageErrors=pageResults.filter(x=>x.error).length;
    let status;
    if(fullKeywordSearch && jobs.length) status="BROWSER_ENUMERATED";
    else if(fullKeywordSearch && !jobs.length && pageErrors===0) status="BROWSER_ENUMERATED_ZERO";
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
    timer=setTimeout(()=>reject(new Error(`company enumeration timed out after ${COMPANY_BUDGET_MS}ms`)),COMPANY_BUDGET_MS);
  });
  try{
    return await Promise.race([work,timeout]);
  }catch(e){
    console.log(`${src.company}: browser ERROR ${String(e).slice(0,300)}`);
    return {company:src.company,board_scope:boardScope,root_portal:root,seed_portal:src.portal,job_list_url:jobList,pages:pageResults,endpoints:endpointLog.slice(0,120),jobs:uniqueJobs(collector),status:"BROWSER_ERROR",error:String(e).slice(0,500),search_terms_attempted:[],search_terms_expected:SEARCH_TERMS,full_keyword_search:false};
  }finally{
    if(timer) clearTimeout(timer);
    work.catch(()=>{});
    await context.close().catch(()=>{});
  }
}

async function main(){
  // Dedicated API / direct ATS adapters are enumerated later by the sync layer.
  // Playwright is reserved for sources that genuinely need browser/XHR discovery.
  const allSources=CONFIG.sources.filter(s=>s.mode==="portal_only");
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
