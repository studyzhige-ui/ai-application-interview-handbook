import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

// Exercise the production search function without starting Playwright, importing
// dependencies, making network calls, or running the top-level collector.
const source = fs.readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)), "../jd/adapters/browser.mjs"), "utf8");
const helperStart = source.indexOf("function assertNoSecurityChallenge(");
const searchStart = source.indexOf("async function searchInputs(");
const searchEnd = source.indexOf("function splitJobText(", searchStart);
assert.ok(searchStart >= 0 && searchEnd > searchStart);
const sourceUnderTest = source.slice(helperStart < 0 ? searchStart : helperStart, searchEnd);

function fixture({ blockedInitially = false, blockAfterEnter = false, noInput = false, normalFillError = false } = {}) {
  const calls = { fills: [], presses: 0, collections: 0 };
  let blocked = blockedInitially;
  const input = {
    async getAttribute(name) { return ({ type: "search", placeholder: "搜索职位" })[name] || null; },
    async fill(value) {
      calls.fills.push(value);
      if (normalFillError && value.endsWith("agent")) throw new Error("input temporarily unavailable");
    },
    async press() { calls.presses++; if (blockAfterEnter) blocked = true; },
  };
  const page = {
    url() { return blocked ? "https://m.zhipin.com/web/passport/zp/verify.html" : "https://m.zhipin.com/zhaopin/example/"; },
    locator(selector) {
      if (selector === "input") return { async count() { return noInput ? 0 : 1; }, nth() { return input; } };
      if (selector === "body") return { async innerText() { return blocked ? "安全验证 当前 IP 地址可能存在异常访问行为，完成验证后即可正常使用。" : "官方校园招聘职位列表"; } };
      throw new Error(`Unexpected selector: ${selector}`);
    },
    async waitForTimeout() {},
  };
  const context = vm.createContext({
    SEARCH_TERMS: ["agent", "rag", "mcp"],
    async collectSearchPages(_page, term) { calls.collections++; return [{ href: "https://example.test/job/1", keyword: term }]; },
  });
  const searchInputs = vm.runInContext(sourceUnderTest + "\nsearchInputs;", context);
  return { calls, searchInputs, page };
}

test("an initial verification page is an explicit error, even without a search input", async () => {
  const f = fixture({ blockedInitially: true, noInput: true });
  await assert.rejects(f.searchInputs(f.page), /security challenge/);
  assert.equal(f.calls.fills.length, 0);
  assert.equal(f.calls.presses, 0);
});

test("verification after the first search stops immediately instead of trying later keywords", async () => {
  const f = fixture({ blockAfterEnter: true });
  await assert.rejects(f.searchInputs(f.page, { prefix: "BOSS直聘 校招" }), /security challenge/);
  assert.deepEqual(f.calls.fills, ["BOSS直聘 校招 agent"]);
  assert.equal(f.calls.presses, 1);
  assert.equal(f.calls.collections, 0);
});

test("normal search keeps all keyword results and the existing reset behavior", async () => {
  const f = fixture();
  const result = await f.searchInputs(f.page, { prefix: "BOSS直聘 校招" });
  assert.equal(result.found, true);
  assert.deepEqual(Array.from(result.terms), ["agent", "rag", "mcp"]);
  assert.equal(result.hits.length, 3);
  assert.equal(f.calls.collections, 3);
  assert.equal(f.calls.presses, 4);
  assert.equal(f.calls.fills.at(-1), "");
});

test("an ordinary empty page remains needs-adapter rather than becoming a fabricated security block", async () => {
  const f = fixture({ noInput: true });
  const result = await f.searchInputs(f.page);
  assert.equal(result.found, false);
  assert.equal(result.terms.length, 0);
});

test("ordinary transient input errors retain their existing best-effort behavior", async () => {
  const f = fixture({ normalFillError: true });
  const result = await f.searchInputs(f.page);
  assert.deepEqual(Array.from(result.terms), ["rag", "mcp"]);
  assert.equal(f.calls.collections, 2);
});

test("BOSS verify URLs are blocked even before challenge text finishes rendering", () => {
  const guard = vm.runInNewContext(sourceUnderTest + "\nassertNoSecurityChallenge;");
  assert.throws(() => guard("https://m.zhipin.com/web/passport/zp/verify.html", ""), /security challenge/);
  assert.throws(() => guard("https://m.zhipin.com/web/passport/zp/security-check", "安全验证"), /security challenge/);
  assert.doesNotThrow(() => guard("https://example.test/jobs", "暂无岗位"));
});

test("a job description mentioning verification codes is not a security page", () => {
  const guard = vm.runInNewContext(sourceUnderTest + "\nassertNoSecurityChallenge;");
  assert.doesNotThrow(() => guard("https://example.test/jobs", "岗位职责：设计验证码登录系统，处理安全验证和访问异常。"));
  assert.doesNotThrow(() => guard("https://example.test/login", "输入短信验证码"));
  assert.throws(() => guard("https://example.test/", "安全验证\n请完成以下验证"), /security challenge/);
});

test("a pagination challenge stops before another next-page attempt", async () => {
  const collectStart = source.indexOf("async function collectSearchPages(");
  const collectSource = source.slice(collectStart, searchStart);
  let blocked = false, clicks = 0, linkReads = 0;
  const next = {
    last() { return this; }, filter() { return this; }, async count() { return 1; },
    async isVisible() { return true; }, async isDisabled() { return false; },
    async getAttribute() { return null; }, async click() { clicks++; blocked = true; },
  };
  const page = {
    url() { return blocked ? "https://m.zhipin.com/web/passport/zp/verify.html" : "https://example.test/jobs"; },
    async waitForTimeout() {}, getByRole() { return next; },
    locator(selector) {
      if (selector === "body") return { async innerText() { return blocked ? "安全验证" : "职位列表"; } };
      return next;
    },
  };
  const collect = vm.runInNewContext(collectSource + "\ncollectSearchPages;", {
    async scroll() {},
    async jobLinksOnPage() { linkReads++; return [{ href: "https://example.test/job/1" }]; },
  });
  await assert.rejects(collect(page, "agent"), /security challenge/);
  assert.equal(clicks, 1);
  assert.equal(linkReads, 1);
});

test("the initial challenge is returned as an error rather than needs-adapter or zero jobs", async () => {
  const runStart = source.indexOf("async function runPage(");
  const runEnd = source.indexOf("function feishuKeywordCoverage(", runStart);
  const guardSource = source.slice(helperStart, searchStart);
  let closed = false;
  const page = {
    on() {}, async goto() {}, async waitForTimeout() {},
    url() { return "https://m.zhipin.com/web/passport/zp/verify.html"; },
    locator() { return { async innerText() { return "安全验证 当前 IP 地址可能存在异常访问行为"; } }; },
    async close() { closed = true; },
  };
  const runPage = vm.runInNewContext(guardSource + source.slice(runStart, runEnd) + "\nrunPage;", { async scroll() {} });
  const result = await runPage({ async newPage() { return page; } }, "BOSS直聘/看准科技", "https://m.zhipin.com/zhaopin/example/", "zhipin.com", [], new Set(), [], "campus");
  assert.match(result.error, /security challenge; enumeration is incomplete/);
  assert.equal(result.search_terms_attempted.length, 0);
  assert.notEqual(result.list_scan_complete, true);
  assert.equal(closed, true);
});

const {cacheIsFresh, assertCompletePool} = await import("../jd/adapters/cache.mjs");

test("cache freshness requires the expected commit and run", () => {
  const now=Date.now();
  const p={generated_at:new Date(now).toISOString(),source_commit:"sha",run_id:"run"};
  const env={SYNC_SOURCE_SHA:"sha",GITHUB_RUN_ID:"run"};
  assert.equal(cacheIsFresh(p,env,now),true);
  assert.equal(cacheIsFresh({...p,run_id:"old"},env,now),false);
  assert.equal(cacheIsFresh({...p,source_commit:"old"},env,now),false);
  assert.equal(cacheIsFresh({...p,generated_at:new Date(now-7*3600000).toISOString()},env,now),false);
  assert.equal(cacheIsFresh({},env,now),false);
});

test("accelerators reject missing, negative and partial totals", () => {
  assert.throws(()=>assertCompletePool(undefined,[]),/Incomplete/);
  assert.throws(()=>assertCompletePool(-1,[]),/Incomplete/);
  assert.throws(()=>assertCompletePool(3,[{},{}]),/Incomplete/);
  assert.doesNotThrow(()=>assertCompletePool(0,[]));
  assert.doesNotThrow(()=>assertCompletePool(2,[{},{}]));
});

function signedProof(entries){
  const start=source.indexOf("function feishuKeywordCoverage(");
  const end=source.indexOf("function canonicalFeishuListUrl(",start);
  const fn=vm.runInNewContext(source.slice(start,end)+"\nfeishuKeywordCoverage;",{SEARCH_TERMS:["agent"]});
  return fn(entries);
}
function entry(offset,rows,total){
  return {url:"https://example.test/api/v1/search/job/posts",status:200,
    post_data:JSON.stringify({keyword:"",offset,limit:10}),response_rows:rows,response_count:total};
}

test("a short Feishu page does not override a larger advertised total",()=>{
  assert.equal(signedProof([entry(0,2,20)]).full_pool_complete,false);
  assert.equal(signedProof([entry(0,10,20),entry(10,10,20)]).full_pool_complete,true);
  assert.equal(signedProof([entry(0,0,0)]).full_pool_complete,true);
});

test("missing totals or gaps cannot certify a signed pool",()=>{
  assert.equal(signedProof([entry(0,0,null)]).full_pool_complete,undefined);
  assert.equal(signedProof([entry(0,10,30),entry(20,10,30)]).full_pool_complete,false);
});

test("browser JD splitting keeps the full first-party body",()=>{
  const start=source.indexOf("function splitJobText(");
  const end=source.indexOf("async function scrapeSearchHit(",start);
  const fn=vm.runInNewContext(source.slice(start,end)+"\nsplitJobText;");
  const duties="完整职责".repeat(6000), requirements="完整要求".repeat(4000);
  const out=fn("职责\n"+duties+"\n任职要求\n"+requirements,"");
  assert.ok(out.description.includes(duties));
  assert.ok(out.requirements.includes(requirements));
});

test("observed jobs without a complete-list proof remain needs-adapter",async()=>{
  const start=source.indexOf("async function processSource(");
  const end=source.indexOf("async function main(",start);
  const fn=vm.runInNewContext(source.slice(start,end)+"\nprocessSource;",{
    URL, setTimeout, clearTimeout, COMPANY_BUDGET_MS:15000,SEARCH_TERMS:["agent"],console:{log(){}},
    uniqueJobs:x=>x,feishuKeywordCoverage:()=>({full_pool_complete:false}),
    async runPage(_ctx,_company,url,_host,jobs,visited){
      visited.add(url);jobs.push({company:"Company",title:"Agent工程师"});
      return {page_url:url,search_control_found:false,list_scan_complete:false,search_terms_attempted:[]};
    }
  });
  const out=await fn({async newContext(){return {async close(){}};}},
    {company:"Company",mode:"portal_only",portal:"https://example.test/jobs",official_root:"https://example.test",current_campus_board:true});
  assert.equal(out.status,"BROWSER_CAMPUS_NEEDS_ADAPTER");
  assert.equal(out.list_scan_complete,false);
  assert.equal(out.jobs.length,1);
});

test("generic replay cannot certify a short page below the advertised total",async()=>{
  const start=source.indexOf("async function replayCapturedFullPool(");
  const end=source.indexOf("async function scroll(",start);
  const fn=vm.runInNewContext(source.slice(start,end)+"\nreplayCapturedFullPool;",{
    URL, URLSearchParams, blankListRequest:()=>true,
    pagingContract:()=>({body:{offset:0,limit:10},offsetHit:{key:"offset"},size:10,parsed:{bodyType:"json"}}),
    cloneObject:x=>JSON.parse(JSON.stringify(x)),setKeywordBlank(){},KEYWORD_KEYS:[],PAGE_KEYS:[],OFFSET_KEYS:[],SIZE_KEYS:[],
    deepGetContainer:()=>null,responseListStats:()=>({path:"$.jobs",rows:2,total:20}),recursiveJobs(){}
  });
  const out=await fn({url:()=>"https://example.test/jobs",async evaluate(){return {status:200,data:{jobs:[{},{}],total:20}};}},
    "Company",[{url:"https://example.test/api/jobs",status:200,response_list_path:"$.jobs",response_rows:2,response_count:20}],[],[],"campus");
  assert.equal(out.complete,false);
});

test("Moka short-page results below advertised total are blocked",async()=>{
  const moka=fs.readFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)),"../jd/adapters/moka.mjs"),"utf8");
  const start=moka.indexOf("async function enumerateOne(");
  const end=moka.indexOf("async function enumerateOneBounded(",start);
  const fn=vm.runInNewContext(moka.slice(start,end)+"\nenumerateOne;",{
    URL,assertCompletePool,
    endpointContract:()=>({endpoint:"https://example.test/api/jobs",body:{orgId:"o",siteId:"s"}}),
    officialPage:()=>"https://example.test/campus",async apiCall(){return {};},
    jobsFromDecoded:()=>[{id:"a"},{id:"b"}],totalFromDecoded:()=>20,
    normalize:(_company,j)=>({job_id:j.id,title:"Agent工程师"}),merge:(_old,incoming)=>incoming
  });
  await assert.rejects(fn({company:"Company",pages:[]}),/Incomplete official pool/);
});
