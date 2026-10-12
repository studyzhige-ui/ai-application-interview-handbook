import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";
import { createCipheriv, createHash } from "node:crypto";
import { parseArgs, selectSource, collectPaged, createRuntime } from "../jd/adapters/bounded.mjs";
import { collectByteDance } from "../jd/adapters/bytedance.mjs";
import { collectFeishu } from "../jd/adapters/feishu.mjs";
import { collectMoka, WPS_RUNTIME_PARAMETER_ENV } from "../jd/adapters/moka.mjs";
import { collectBrowser, extractList, nextRequest, assertNoSecurityChallenge } from "../jd/adapters/browser.mjs";

const directory = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../jd/adapters");
const source = { source_id: "fixture-source", company: "Fixture", mode: "bytedance_api", portal: "https://jobs.bytedance.com/campus/" };
const options = (changes = {}) => ({ enableCodeCollection: true, sourceId: source.source_id, maxPages: 5, maxJobs: 10, timeoutSeconds: 2, ...changes });
const response = (payload, status = 200) => new Response(typeof payload === "string" ? payload : JSON.stringify(payload), { status, headers: { "content-type": "application/json" } });
const listPayload = (rows, count) => ({ code: 0, data: { count, job_post_list: rows } });
const detailPayload = row => ({ code: 0, data: { job_post: row } });
const adapters = ["browser", "bytedance", "xiaomi", "feishu", "moka"];

for (const adapter of adapters) {
  test(`${adapter}: import has no data reads, writes, network, or Playwright initialization`, () => {
    const file = new URL(`../jd/adapters/${adapter}.mjs`, import.meta.url).href;
    const script = `import fs from 'node:fs'; globalThis.fetch=()=>{throw Error('NETWORK');}; const read=fs.readFileSync; fs.readFileSync=(file,...args)=>{if(String(file).endsWith('.mjs'))return read(file,...args);throw Error('DATA READ '+file);}; fs.writeFileSync=()=>{throw Error('WRITE');}; await import(${JSON.stringify(file)});`;
    const run = spawnSync(process.execPath, ["--input-type=module", "-e", script], { encoding: "utf8" });
    assert.equal(run.status, 0, run.stderr);
    assert.equal(run.stdout, "");
  });
  test(`${adapter}: default command fails closed before registry/Playwright access`, () => {
    const run = spawnSync(process.execPath, [path.join(directory, `${adapter}.mjs`)], { encoding: "utf8" });
    assert.equal(run.status, 2);
    assert.match(run.stderr, /Code collection is disabled/);
    assert.equal(run.stdout, "");
  });
}

test("all independent enable, source, and numeric bounds are mandatory", () => {
  const args = ["--enable-code-collection", "--source-id", "fixture-source", "--max-pages", "2", "--max-jobs", "3", "--timeout-seconds", "0.5"];
  assert.equal(parseArgs(args).timeoutSeconds, 0.5);
  assert.throws(() => parseArgs([]), /disabled/);
  assert.throws(() => parseArgs(args.slice(0, -2)), /timeoutSeconds/);
  assert.throws(() => parseArgs([...args, "--max-pages", "3"]), /Repeated/);
  assert.throws(() => parseArgs(args.map(value => value === "2" ? "0" : value)), /positive integer/);
  assert.throws(() => parseArgs(args.map(value => value === "0.5" ? "NaN" : value)), /finite/);
  assert.throws(() => parseArgs([...args, "--unknown", "yes"]), /Unknown/);
  assert.throws(() => selectSource({ sources: [source] }, "unknown"), /registered source/);
  assert.throws(() => selectSource({ sources: [source, source] }, source.source_id), /found 2/);
});

test("explicit structural collection keys dedupe repeated DOM observations without inventing job IDs", () => {
  const runtime = createRuntime(source, options());
  try {
    assert.equal(runtime.addJob({ title: "same", collection_key: "page-1:0" }), true);
    assert.equal(runtime.addJob({ title: "same", collection_key: "page-1:0" }), false);
    assert.equal(runtime.addJob({ title: "same", collection_key: "page-1:1" }), true);
    assert.equal(runtime.jobs.length, 2);
    assert(runtime.jobs.every(job => !job.job_id && !job.official_url));
  } finally {
    runtime.close();
  }
});

test("direct collector calls without the explicit gate make zero requests", async () => {
  let requests = 0;
  await assert.rejects(collectByteDance(source, {}, { fetch() { requests++; } }), /disabled/);
  assert.equal(requests, 0);
});

test("every title gets detail; exact raw response bytes and complete long fields survive", async () => {
  const rows = [{ id: "a", title: "研究员" }, { id: "b", title: "销售" }, { id: "c", title: "Agent 工程师" }, { id: "d", title: "" }];
  const listBody = '  {"code":0,"data":{"count":4,"job_post_list":' + JSON.stringify(rows) + '}}\n';
  const details = [], longBody = "  <p>原始职责\r\n&amp;  </p>".repeat(10000);
  const result = await collectByteDance(source, options(), { async fetch(url, init) {
    assert.equal(init.signal.aborted, false);
    if (url.endsWith("/search/job/posts")) {
      assert.equal(JSON.parse(init.body).keyword, "");
      assert.match(init.headers["User-Agent"], /Chrome\/141/);
      assert.match(init.headers["Accept-Language"], /^zh-CN/);
      return response(listBody);
    }
    const id = url.split("/").at(-1); details.push(id);
    return response(detailPayload({ ...rows.find(row => row.id === id), description: longBody, requirement: "\t 原始要求 \n" }));
  } });
  assert.equal(result.complete, true);
  assert.deepEqual(details, ["a", "b", "c", "d"]);
  assert.deepEqual(result.jobs.map(job => job.title), rows.map(row => row.title));
  assert.equal(result.jobs[0].description, longBody);
  assert.equal(result.jobs[0].requirements, "\t 原始要求 \n");
  assert.equal(Buffer.from(result.captures[0].body_base64, "base64").toString(), listBody);
  assert.equal(result.captures[0].sha256, createHash("sha256").update(listBody).digest("hex"));
  assert.deepEqual(result.jobs[0].raw_list, rows[0]);
});

test("Feishu 405 falls back to the registered first-party browser flow", async () => {
  const fallbackRows = [{ title: "普通岗位", job_id: "browser-1", official_url: "https://jobs.bytedance.com/campus/position/browser-1/detail" }];
  const fixture = browserFixture([{ rows: fallbackRows, total: 1 }]);
  const result = await collectByteDance(source, options(), {
    ...fixture,
    async fetch() { return response("method changed", 405); },
  });
  assert.equal(result.complete, true);
  assert.equal(result.transport_fallback, "browser_after_direct_405");
  assert.equal(result.jobs.length, 1);
  assert.equal(result.jobs[0].job_id, "browser-1");
  assert.match(result.direct_attempt.failures[0].error, /HTTP 405/);
});

test("Feishu browser fallback opens the official channel position list", async () => {
  const feishuSource = {
    source_id: "fixture-feishu", company: "Fixture Feishu", mode: "feishu_direct",
    portal: "https://fixture.jobs.feishu.cn/123456/", job_list_url: "https://fixture.jobs.feishu.cn/123456/",
    feishu_host: "fixture.jobs.feishu.cn", feishu_channel: "123456",
  };
  const opened = [];
  const fixture = browserFixture([{ rows: [], total: 0 }], { async open(url) { opened.push(url); } });
  const result = await collectFeishu(feishuSource, options({ sourceId: feishuSource.source_id }), {
    ...fixture,
    async fetch() { return response("method changed", 405); },
  });
  assert.equal(result.complete, true);
  assert.equal(result.transport_fallback, "browser_after_direct_405");
  assert.deepEqual(opened, ["https://fixture.jobs.feishu.cn/123456/position/list"]);
});

test("Feishu browser fallback honors an explicitly registered browser list URL", async () => {
  const feishuSource = {
    source_id: "fixture-feishu-custom", company: "Fixture Feishu", mode: "feishu_direct",
    portal: "https://fixture.jobs.feishu.cn/", job_list_url: "https://fixture.jobs.feishu.cn/",
    feishu_host: "fixture.jobs.feishu.cn", feishu_channel: "index",
    feishu_browser_list_url: "https://fixture.jobs.feishu.cn/692892/position/list",
  };
  const opened = [];
  const fixture = browserFixture([{ rows: [], total: 0 }], { async open(url) { opened.push(url); } });
  const result = await collectFeishu(feishuSource, options({ sourceId: feishuSource.source_id }), {
    ...fixture,
    async fetch() { return response("method changed", 405); },
  });
  assert.equal(result.complete, true);
  assert.deepEqual(opened, [feishuSource.feishu_browser_list_url]);
});

test("max-jobs bounds retained jobs and detail fetches even if a server ignores limit", async () => {
  let calls = 0;
  const rows = Array.from({ length: 9 }, (_, index) => ({ id: String(index), title: "same title" }));
  const result = await collectByteDance(source, options({ maxJobs: 2 }), { async fetch(url) {
    calls++;
    return response(url.endsWith("/search/job/posts") ? listPayload(rows, 9) : detailPayload({ id: url.split("/").at(-1), title: "same title" }));
  } });
  assert.equal(result.status, "LIMITED");
  assert.equal(result.stop_reason, "MAX_JOBS");
  assert.equal(result.jobs.length, 2);
  assert.equal(result.counts.detail_jobs_attempted, 2);
  assert.equal(calls, 3);
  assert.equal(JSON.parse(Buffer.from(result.captures[0].body_base64, "base64")).data.job_post_list.length, 9);
});

test("pagination uses offsets and continues short pages when total says more", async () => {
  const offsets = [];
  const result = await collectByteDance(source, options(), { async fetch(url, init) {
    if (!url.endsWith("/search/job/posts")) return response(detailPayload({ id: url.split("/").at(-1), title: "ordinary" }));
    const offset = JSON.parse(init.body).offset; offsets.push(offset);
    return response(listPayload([{ id: String(offset), title: "ordinary" }], 3));
  } });
  assert.equal(result.complete, true);
  assert.deepEqual(offsets, [0, 1, 2]);
});

test("max-pages stops list requests and returns captured partial records", async () => {
  let lists = 0;
  const result = await collectByteDance(source, options({ maxPages: 2 }), { async fetch(url) {
    if (!url.endsWith("/search/job/posts")) return response(detailPayload({ id: url.split("/").at(-1) }));
    return response(listPayload([{ id: String(lists++), title: "职位" }], 8));
  } });
  assert.equal(result.status, "LIMITED");
  assert.equal(result.stop_reason, "MAX_PAGES");
  assert.equal(lists, 2);
  assert.equal(result.jobs.length, 2);
  assert.equal(result.captures.length, 4);
});

test("list retries consume page budget; raw failures remain available", async () => {
  let requests = 0;
  const result = await collectByteDance(source, options({ maxPages: 2 }), { async fetch() { requests++; return response('{"failure":"retry"}', 503); } });
  assert.equal(result.status, "LIMITED");
  assert.equal(requests, 2);
  assert.equal(result.failures.length, 2);
  assert.equal(result.captures.length, 2);
});

test("detail retries are bounded and report failure without deleting raw list records", async () => {
  let detailRequests = 0;
  const result = await collectByteDance(source, options(), { async fetch(url) {
    if (url.endsWith("/search/job/posts")) return response(listPayload([{ id: "a", title: "非目标标题" }], 1));
    detailRequests++; return response("unavailable", 503);
  } });
  assert.equal(detailRequests, 3);
  assert.equal(result.list_scan_complete, true);
  assert.equal(result.complete, false);
  assert.equal(result.jobs[0].detail_status, "ERROR");
  assert.deepEqual(result.jobs[0].raw_list, { id: "a", title: "非目标标题" });
});

test("timeout aborts active fetch and keeps partial capture, with no later requests", async () => {
  let requests = 0, signal;
  const result = await collectByteDance(source, options({ timeoutSeconds: 0.03 }), { async fetch(url, init) {
    requests++;
    if (url.endsWith("/search/job/posts")) return response(listPayload([{ id: "a", title: "Raw" }], 2));
    signal = init.signal;
    return new Promise((_, reject) => init.signal.addEventListener("abort", () => reject(new Error("aborted")), { once: true }));
  } });
  assert.equal(result.status, "TIMEOUT");
  assert.equal(signal.aborted, true);
  assert.equal(result.jobs.length, 1);
  assert.equal(result.captures.length, 1);
  assert.equal(result.jobs[0].detail_status, "TIMEOUT");
  await new Promise(resolve => setTimeout(resolve, 20));
  assert.equal(requests, 2);
});

test("exact IDs deduplicate; identical titles with different IDs remain separate", async () => {
  const rows = [{ id: "a", title: "same" }, { id: "a", title: "changed" }, { id: "b", title: "same" }];
  const details = [];
  const result = await collectByteDance(source, options(), { async fetch(url) {
    if (url.endsWith("/search/job/posts")) return response(listPayload(rows, 2));
    const id = url.split("/").at(-1); details.push(id); return response(detailPayload({ id, title: "same" }));
  } });
  assert.equal(result.complete, true);
  assert.deepEqual(details, ["a", "b"]);
});

test("repeated page below advertised total is incomplete, never fabricated complete", async () => {
  const result = await collectByteDance(source, options(), { async fetch(url) {
    return response(url.endsWith("/search/job/posts") ? listPayload([{ id: "a", title: "x" }], 2) : detailPayload({ id: "a" }));
  } });
  assert.equal(result.complete, false);
  assert.match(result.error, /Incomplete official pool/);
});

test("missing totals cannot certify zero or trigger details", async () => {
  const result = await collectByteDance(source, options(), { async fetch() { return response({ code: 0, data: { job_post_list: [] } }); } });
  assert.equal(result.complete, false);
  assert.equal(result.jobs.length, 0);
  assert.equal(result.captures.length, 1);
});

test("a proven empty pool is complete", async () => {
  const result = await collectByteDance(source, options(), { async fetch() { return response(listPayload([], 0)); } });
  assert.equal(result.complete, true);
  assert.equal(result.jobs.length, 0);
});

test("Moka retains encrypted bytes and fetches details for every title", async () => {
  const mokaSource = { ...source, mode: "portal_only", portal: "https://app.mokahr.com/campus/fixture/1", moka_endpoint: "https://app.mokahr.com/api/outer/ats-apply/website/jobs/v2", moka_org_id: "fixture", moka_site_id: "1" };
  const rows = [{ id: "1", title: "销售" }, { id: "2", title: "算法研究" }], detailIds = [];
  function encrypted(payload) {
    const key = "0123456789abcdef";
    const cipher = createCipheriv("aes-128-cbc", Buffer.from(key), Buffer.from("de7c21ed8d6f50fe"));
    return JSON.stringify({ necromancer: key, data: Buffer.concat([cipher.update(JSON.stringify(payload)), cipher.final()]).toString("base64") });
  }
  const listBody = encrypted({ code: 0, data: { jobs: rows, total: 2 } });
  const result = await collectMoka(mokaSource, options(), { async fetch(url, init) {
    if (url.endsWith("jobs/v2")) {
      assert(JSON.parse(init.body).limit <= 50);
      return response(listBody);
    }
    const id = JSON.parse(init.body).jobId; detailIds.push(id);
    return response(encrypted({ code: 0, data: { job: { id, title: rows.find(row => row.id === id).title, jobDescription: "  <p>Original &amp; body</p>\n" } } }));
  } });
  assert.equal(result.complete, true);
  assert.deepEqual(detailIds, ["1", "2"]);
  assert.equal(result.jobs[0].description, "  <p>Original &amp; body</p>\n");
  assert.equal(Buffer.from(result.captures[0].body_base64, "base64").toString(), listBody);
});

function browserFixture(pages, changes = {}) {
  const calls = { opens: 0, next: 0, details: [], closed: false };
  let index = 0;
  const driver = {
    async open() { calls.opens++; }, async snapshot() { return pages[index]; },
    async nextAction() { return index < pages.length - 1 ? async () => { calls.next++; index++; } : null; },
    async detail(job) { calls.details.push(job.official_url); return { raw_detail_html: "<main>  原始正文\r\n</main>", raw_detail_text: "  原始正文\r\n" }; },
    async close() { calls.closed = true; }, ...changes,
  };
  return { calls, driverFactory: () => driver };
}
const browserRows = ["销售", "研究员", "Agent", ""].map((title, index) => ({ title, job_id: String(index), official_url: `https://example.test/job/${index}` }));
const browserSource = { ...source, mode: "portal_only", portal: "https://example.test/jobs" };

test("browser visits every structurally identified detail regardless of title", async () => {
  const fixture = browserFixture([{ rows: browserRows, total: 4 }]);
  const result = await collectBrowser(browserSource, options(), fixture);
  assert.equal(result.complete, true);
  assert.equal(fixture.calls.details.length, 4);
  assert.equal(result.jobs[0].raw_detail_html, "<main>  原始正文\r\n</main>");
  assert.equal(fixture.calls.closed, true);
});

test("browser page cap prevents any further navigation, while preserving detail bodies", async () => {
  const fixture = browserFixture(browserRows.map(row => ({ rows: [row], total: 4 })));
  const result = await collectBrowser(browserSource, options({ maxPages: 2 }), fixture);
  assert.equal(result.status, "LIMITED");
  assert.equal(fixture.calls.opens + fixture.calls.next, 2);
  assert.equal(fixture.calls.details.length, 2);
  assert.equal(result.jobs.length, 2);
});

test("browser job cap prevents extra detail calls even on an overfull list", async () => {
  const fixture = browserFixture([{ rows: browserRows, total: 4 }]);
  const result = await collectBrowser(browserSource, options({ maxJobs: 1 }), fixture);
  assert.equal(result.status, "LIMITED");
  assert.equal(fixture.calls.details.length, 1);
});

test("browser timeout closes the driver and preserves partial rows", async () => {
  const fixture = browserFixture([{ rows: browserRows, total: 4 }], { async detail() { return new Promise(() => {}); } });
  const result = await collectBrowser(browserSource, options({ timeoutSeconds: 0.02 }), fixture);
  assert.equal(result.status, "TIMEOUT");
  assert.equal(result.jobs.length, 1);
  assert.equal(fixture.calls.closed, true);
});

test("browser can derive advertised total and structural rows from registered DOM selectors", async () => {
  const rows = [
    { title: "岗位A", location: "北京", category: "正式" },
    { title: "岗位B", location: "上海", category: "实习" },
  ];
  const fixture = browserFixture([{ rows: rows.map((row, i) => ({ ...row, job_id: String(i), official_url: `https://example.test/job/${i}` })), total: 2 }]);
  const selected = {
    ...browserSource,
    dom_total_pattern: "共\\s*([0-9,]+)\\s*个职位",
  };
  const result = await collectBrowser(selected, options(), fixture);
  assert.equal(result.complete, true);
  assert.equal(result.total, 2);
});

test("browser missing total preserves observations without claiming completeness", async () => {
  const fixture = browserFixture([{ rows: browserRows, total: null }]);
  const result = await collectBrowser(browserSource, options(), fixture);
  assert.equal(result.complete, false);
  assert.equal(result.jobs.length, 4);
  assert.equal(result.stop_reason, "LIST_TOTAL_UNPROVEN");
});

test("structural JSON extraction includes empty titles and empty lists with totals", () => {
  assert.equal(extractList({ data: { jobs: [{ id: "x", title: "" }], total: 1 } }).rows.length, 1);
  assert.deepEqual(extractList({ data: { jobs: [], total: 0 } }).rows, []);
});

test("observed unsigned pagination retains body filters but never adds role keywords", () => {
  const result = nextRequest({ url: "https://example.test/api/jobs", method: "POST", postData: '{"offset":0,"limit":2,"keyword":"","tenant":"one"}', list: { rows: [{}, {}], total: 5 } });
  assert.deepEqual(result.body, { offset: 2, limit: 2, keyword: "", tenant: "one" });
  assert.equal(nextRequest({ url: "https://example.test/api/v1/search/job/posts", postData: '{"offset":0}', list: { rows: [{}], total: 3 } }), null);
  assert.equal(nextRequest({ url: "https://example.test/api/jobs", postData: '{"offset":0,"keyword":"agent"}', list: { rows: [{}], total: 3 } }), null);
});

test("security challenges remain explicit failures; ordinary descriptions are not blocked", () => {
  assert.throws(() => assertNoSecurityChallenge("https://m.zhipin.com/web/passport/zp/verify.html", ""), /challenge/);
  assert.doesNotThrow(() => assertNoSecurityChallenge("https://example.test/job/1", "职责：开发验证码登录系统，支持安全验证。"));
});

test("an existing output file is never overwritten, even with an enabled command", () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "jd-bounded-test-"));
  try {
    const original = path.join(temporary, "original.json"); fs.writeFileSync(original, "original bytes\r\n");
    const run = spawnSync(process.execPath, [path.join(directory, "browser.mjs"), "--enable-code-collection", "--source-id", "fixture-source", "--max-pages", "1", "--max-jobs", "1", "--timeout-seconds", "1", "--registry", path.join(temporary, "absent.json"), "--output", original], { encoding: "utf8" });
    assert.equal(run.status, 2);
    assert.match(run.stderr, /will not be overwritten/);
    assert.equal(fs.readFileSync(original, "utf8"), "original bytes\r\n");
  } finally { fs.rmSync(temporary, { recursive: true, force: true }); }
});

test("missing IDs and URLs never cause same-title rows to be conflated", async () => {
  const specification = {
    listRequest: () => ({ url: "https://example.test/jobs", init: {} }),
    listData: payload => ({ rows: payload.rows, total: 3 }),
    normalize: row => ({ title: row.title, job_id: "", official_url: "", raw_marker: row.marker }),
    detailRequest: () => null,
  };
  const result = await collectPaged(source, options(), specification, { async fetch() { return response({ rows: [{ title: "same", marker: 1 }, { title: "same", marker: 2 }, { title: "same", marker: 3 }] }); } });
  assert.equal(result.list_scan_complete, true);
  assert.equal(result.jobs.length, 3);
  assert.deepEqual(result.jobs.map(job => job.raw_marker), [1, 2, 3]);
});

test("timeout during response streaming preserves received bytes as an incomplete capture", async () => {
  const prefix = Buffer.from(' {"unfinished":');
  const result = await collectByteDance(source, options({ timeoutSeconds: 0.02 }), { async fetch() {
    return new Response(new ReadableStream({ start(controller) { controller.enqueue(prefix); } }), { headers: { "content-type": "application/json" } });
  } });
  assert.equal(result.status, "TIMEOUT");
  assert.equal(result.captures.length, 1);
  assert.equal(result.captures[0].body_complete, false);
  assert.deepEqual(Buffer.from(result.captures[0].body_base64, "base64"), prefix);
});

test("distinct authoritative IDs survive a shared URL, while URL-only duplicates do not", async () => {
  const rows = [
    { job_id: "a", title: "same", official_url: "https://example.test/detail" },
    { job_id: "b", title: "same", official_url: "https://example.test/detail" },
    { job_id: "", title: "same", official_url: "https://example.test/detail" },
  ];
  const fixture = browserFixture([{ rows, total: 2 }]);
  const result = await collectBrowser(browserSource, options(), fixture);
  assert.equal(result.jobs.length, 2);
  assert.deepEqual(result.jobs.map(job => job.job_id), ["a", "b"]);
  assert.equal(fixture.calls.details.length, 2);
});

test("browser includes both explicit extra portal and extra job-list registry URLs", async () => {
  const opened = [];
  const fixture = browserFixture([{ rows: [], total: 0 }], { async open(url) { opened.push(url); } });
  const selected = { ...browserSource, extra_portals: ["https://example.test/campus"], extra_job_list_urls: ["https://example.test/graduate"] };
  const result = await collectBrowser(selected, options(), fixture);
  assert.equal(result.complete, true);
  assert.deepEqual(opened, [selected.portal, ...selected.extra_portals, ...selected.extra_job_list_urls]);
});

test("browser snapshot uses one primary job-list response instead of merging recommendations", async () => {
  const mainRows = [{ id: "1", title: "主列表岗位", detailUrl: "https://example.test/job/1" }];
  const recRows = [
    { id: "r1", title: "推荐1", detailUrl: "https://example.test/job/r1" },
    { id: "r2", title: "推荐2", detailUrl: "https://example.test/job/r2" },
  ];
  let responseHandler, pages = 0;
  function pageFixture(isList) {
    let url = "";
    return {
      on(event, callback) { if (event === "response") responseHandler = callback; },
      async goto(nextUrl) {
        url = nextUrl;
        if (isList) {
          const emit = async (responseUrl, payload) => responseHandler({
            url: () => responseUrl,
            headers: () => ({ "content-type": "application/json" }),
            status: () => 200,
            body: async () => Buffer.from(JSON.stringify(payload)),
            request: () => ({ method: () => "POST", postData: () => '{"offset":0}' }),
          });
          await emit("https://example.test/api/recommendations", { data: { jobs: recRows, total: 2 } });
          await emit("https://example.test/api/v1/search/job/posts", { code: 0, data: { job_post_list: mainRows, count: 1 } });
        }
        return { status: () => 200 };
      },
      url: () => url, async waitForLoadState() {}, async content() { return "<main></main>"; },
      locator(selector) {
        if (selector === "body") return { async innerText() { return ""; } };
        return { async evaluateAll() { return []; } };
      },
      async close() {},
    };
  }
  const context = { async route() {}, async newPage() { return pageFixture(pages++ === 0); } };
  const chromium = { async launch() { return { async newContext() { return context; }, async close() {} }; } };
  const result = await collectBrowser(browserSource, options(), { chromium });
  assert.equal(result.complete, true);
  assert.deepEqual(result.jobs.map(job => job.job_id), ["1"]);
});

test("Feishu pagination waits for the site-issued signed search response before snapshotting", async () => {
  const rows = [
    { id: "1", title: "第一页", description: "a", requirement: "ra", city_list: [{ name: "北京" }], recruit_type: { name: "校招" }, job_category: { name: "研发" } },
    { id: "2", title: "第二页", description: "b", requirement: "rb", city_list: [{ name: "上海" }], recruit_type: { name: "实习" }, job_category: { name: "工程" } },
  ];
  let listPage, pageIndex = 0, pagesCreated = 0;
  const signedUrl = index => `https://example.test/api/v1/search/job/posts?offset=${index}&_signature=site-issued-${index}`;

  function makePage(isList) {
    let url = "", responseHandler = null, responseWaiter = null;
    async function emitList(index) {
      const payload = { code: 0, data: { count: 2, job_post_list: [rows[index]] } };
      const response = {
        url: () => signedUrl(index), headers: () => ({ "content-type": "application/json" }), status: () => 200,
        body: async () => Buffer.from(JSON.stringify(payload)),
        request: () => ({ method: () => "POST", postData: () => JSON.stringify({ offset: index, limit: 1 }) }),
      };
      if (responseHandler) await responseHandler(response);
      if (responseWaiter && responseWaiter.predicate(response)) {
        const resolve = responseWaiter.resolve; responseWaiter = null; resolve(response);
      }
    }
    const page = {
      on(event, callback) { if (event === "response") responseHandler = callback; },
      async goto(nextUrl) { url = nextUrl; if (isList) await emitList(pageIndex); return { status: () => 200 }; },
      url: () => url,
      async waitForLoadState() {},
      async waitForResponse(predicate) { return new Promise(resolve => { responseWaiter = { predicate, resolve }; }); },
      async content() { return "<main></main>"; },
      locator(selector) {
        if (selector === "body") return { async innerText() { return ""; } };
        if (selector === "a[href]") return { async evaluateAll() { return []; } };
        if (selector === "li.atsx-pagination-next:not(.atsx-pagination-disabled)") return {
          last() { return this; },
          async count() { return isList && pageIndex === 0 ? 1 : 0; },
          async isVisible() { return isList && pageIndex === 0; },
          async click() { pageIndex = 1; await emitList(1); },
        };
        return {
          last() { return this; }, async count() { return 0; }, async isVisible() { return false; },
          async isDisabled() { return false; }, async getAttribute() { return null; },
        };
      },
      getByRole() { return { last() { return this; }, async count() { return 0; } }; },
      async close() {},
    };
    return page;
  }
  const context = { async route() {}, async newPage() { const page = makePage(pagesCreated++ === 0); if (!listPage) listPage = page; return page; } };
  const chromium = { async launch() { return { async newContext() { return context; }, async close() {} }; } };
  const result = await collectBrowser(browserSource, options(), { chromium });
  assert.equal(result.complete, true);
  assert.deepEqual(result.jobs.map(job => job.job_id), ["1", "2"]);
  assert.equal(result.total, 2);
  assert.equal(result.counts.detail_jobs_attempted, 0);
  assert.deepEqual(result.jobs.map(job => job.location), ["北京", "上海"]);
  assert.deepEqual(result.jobs.map(job => job.category), ["校招", "实习"]);
  assert.deepEqual(result.jobs.map(job => job.department), ["研发", "工程"]);
});

test("production browser driver can collect configured DOM job cards and body totals", async () => {
  const domSource = {
    ...browserSource,
    dom_total_pattern: "共\\s*([0-9,]+)\\s*个职位",
    dom_job_selector: "li.search-item",
    dom_title_selector: ".title",
    dom_location_selector: ".location",
    dom_category_selector: ".category",
  };
  let pages = 0;
  function pageFixture(isList) {
    let url = "";
    return {
      on() {},
      async goto(nextUrl) { url = nextUrl; return { status: () => 200 }; },
      url: () => url, async waitForLoadState() {}, async waitForTimeout() {},
      async content() { return "<main></main>"; },
      locator(selector) {
        if (selector === "body") return { async innerText() { return "职位列表 共2个职位"; } };
        if (selector === "a[href]") return { async evaluateAll() { return []; } };
        if (selector === "li.search-item") return { async evaluateAll(fn, config) {
          const make = values => ({
            innerText: values.text,
            textContent: values.text,
            querySelector(sel) {
              const map = {
                ".title": { innerText: values.title, textContent: values.title },
                ".location": { innerText: values.location, textContent: values.location },
                ".category": { innerText: values.category, textContent: values.category },
              };
              return map[sel] || null;
            },
          });
          return fn([
            make({ title: "岗位A", location: "北京", category: "正式", text: "岗位A 北京 正式" }),
            make({ title: "岗位B", location: "上海", category: "实习", text: "岗位B 上海 实习" }),
          ], config);
        } };
        return { last() { return this; }, async count() { return 0; }, async isVisible() { return false; }, async isDisabled() { return false; }, async getAttribute() { return null; } };
      },
      getByRole() { return { last() { return this; }, async count() { return 0; } }; },
      async close() {},
    };
  }
  const context = { async route() {}, async newPage() { return pageFixture(pages++ === 0); } };
  const chromium = { async launch() { return { async newContext() { return context; }, async close() {} }; } };
  const result = await collectBrowser(domSource, options(), { chromium });
  assert.equal(result.list_scan_complete, true);
  assert.equal(result.complete, false);
  assert.equal(result.total, 2);
  assert.deepEqual(result.jobs.map(job => [job.title, job.location]), [["岗位A", "北京"], ["岗位B", "上海"]]);
  assert(result.jobs.every(job => job.detail_status === "NEEDS_ADAPTER"));
});

test("production browser driver captures original HTML/JSON bytes and full rendered details offline", async () => {
  const transportHtml = Buffer.from("<!DOCTYPE html>\r\n<html><body> 原始页面 &amp; </body></html>\n");
  const rows = [{ id: "1", title: "销售", detailUrl: "https://example.test/job/1" }, { id: "2", title: "研究员", detailUrl: "https://example.test/job/2" }];
  const jsonBody = Buffer.from(' {"data":{"jobs":' + JSON.stringify(rows) + ',"total":2}}\n');
  const opened = [];
  let pages = 0, closed = false;
  function pageFixture(isList) {
    let url = "", listener;
    return {
      on(event, callback) { assert.equal(event, "response"); listener = callback; },
      async goto(nextUrl) {
        url = nextUrl; opened.push(url);
        const emit = (responseUrl, bytes, type) => listener({
          url: () => responseUrl, headers: () => ({ "content-type": type }), status: () => 200, body: async () => bytes,
          request: () => ({ method: () => "GET", postData: () => null }),
        });
        emit(url, transportHtml, "text/html");
        if (isList) emit("https://example.test/api/jobs", jsonBody, "application/json");
        return { status: () => 200 };
      },
      url: () => url, async waitForLoadState() {}, async content() { return "<main>  rendered\r\n完整正文 &amp; </main>"; },
      locator(selector) {
        if (selector === "body") return { async innerText() { return "  rendered\r\n完整正文 & "; } };
        return { async evaluateAll() { return rows.map(row => ({ href: row.detailUrl, title: row.title })); } };
      },
      async close() {},
    };
  }
  const context = { async route() {}, async newPage() { return pageFixture(pages++ === 0); } };
  const chromium = { async launch() { return { async newContext() { return context; }, async close() { closed = true; } }; } };
  const result = await collectBrowser(browserSource, options(), { chromium });
  assert.equal(result.complete, true);
  assert.deepEqual(opened, [browserSource.portal, ...rows.map(row => row.detailUrl)]);
  assert.equal(result.jobs.length, 2);
  const htmlCaptures = result.captures.filter(capture => capture.content_type === "text/html");
  assert.equal(htmlCaptures.length, 3);
  for (const capture of htmlCaptures) assert.deepEqual(Buffer.from(capture.body_base64, "base64"), transportHtml);
  const jsonCapture = result.captures.find(capture => capture.content_type === "application/json");
  assert.deepEqual(Buffer.from(jsonCapture.body_base64, "base64"), jsonBody);
  assert.equal(result.jobs[0].raw_detail_text, "  rendered\r\n完整正文 & ");
  assert.equal(closed, true);
});

test("unknown registry selection fails before collection and creates no output", () => {
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), "jd-bounded-registry-"));
  try {
    const registry = path.join(temporary, "registry.json"), output = path.join(temporary, "new.json");
    fs.writeFileSync(registry, JSON.stringify({ sources: [source] }));
    const run = spawnSync(process.execPath, [path.join(directory, "browser.mjs"), "--enable-code-collection", "--source-id", "unregistered", "--max-pages", "1", "--max-jobs", "1", "--timeout-seconds", "1", "--registry", registry, "--output", output], { encoding: "utf8" });
    assert.equal(run.status, 2);
    assert.match(run.stderr, /Expected one registered source/);
    assert.equal(fs.existsSync(output), false);
  } finally { fs.rmSync(temporary, { recursive: true, force: true }); }
});


const wpsSource = {
  source_id: "official-018", company: "金山办公/WPS", mode: "portal_only",
  portal: "https://join.wps.cn/", moka_endpoint: "https://join.wps.cn/api/outer/ats-apply/website/jobs/v2",
  moka_org_id: "wps", moka_site_id: "41436", moka_requires_runtime_source_parameter: true,
};
const privateOptions = () => options({ sourceId: wpsSource.source_id });
const dummyParameter = 'DUMMY_ONLY_RUNTIME_PARAMETER_"_测试';

test("WPS missing runtime parameter fails before network and ignores legacy source values", async () => {
  let calls = 0;
  await assert.rejects(collectMoka({ ...wpsSource, moka_source_token: "DUMMY_IGNORED_LEGACY_FIELD" }, privateOptions(), {
    env: {}, async fetch() { calls++; throw Error("Unexpected network"); },
  }), /operator must configure JD_MOKA_SOURCE_PARAMETER_OFFICIAL_018/);
  assert.equal(calls, 0);
});

test("WPS runtime input reaches only its pinned list request and is absent from saved captures and records", async () => {
  const destinations = [];
  const result = await collectMoka(wpsSource, privateOptions(), {
    env: { [WPS_RUNTIME_PARAMETER_ENV]: dummyParameter },
    async fetch(url, init) {
      destinations.push(url);
      const request = JSON.parse(init.body);
      if (url.endsWith("jobs/v2")) {
        assert.equal(request.sourceToken, dummyParameter);
        return response({ data: { jobs: [{ id: "1", title: "普通岗位", echo: dummyParameter }], total: 1 } });
      }
      assert.equal(request.sourceToken, undefined);
      const key = "0123456789abcdef";
      const cipher = createCipheriv("aes-128-cbc", Buffer.from(key), Buffer.from("de7c21ed8d6f50fe"));
      const data = { data: { job: { id: "1", title: "普通岗位", description: "职责 " + dummyParameter, echo: encodeURIComponent(dummyParameter) } } };
      return response({ necromancer: key, data: Buffer.concat([cipher.update(JSON.stringify(data)), cipher.final()]).toString("base64") });
    },
  });
  assert.equal(result.complete, true);
  assert(destinations.every(url => new URL(url).origin === "https://join.wps.cn"));
  const serialized = JSON.stringify(result);
  for (const variant of [dummyParameter, JSON.stringify(dummyParameter).slice(1, -1), encodeURIComponent(dummyParameter), Buffer.from(dummyParameter).toString("base64")]) assert(!serialized.includes(variant));
  assert.equal(JSON.parse(result.captures[0].request_body).sourceToken, "[REDACTED_RUNTIME_PARAMETER]");
  for (const capture of result.captures) {
    const body = Buffer.from(capture.body_base64, "base64").toString();
    assert(!body.includes(dummyParameter));
    assert(!body.includes(encodeURIComponent(dummyParameter)));
    assert.equal(capture.sensitive_values_redacted, true);
  }
  assert.equal(result.jobs[0].raw_list.echo, "[REDACTED_RUNTIME_PARAMETER]");
  assert.equal(result.jobs[0].description, "职责 [REDACTED_RUNTIME_PARAMETER]");
});

test("WPS runtime input is removed from transport error diagnostics", async () => {
  const result = await collectMoka(wpsSource, privateOptions(), {
    env: { [WPS_RUNTIME_PARAMETER_ENV]: dummyParameter },
    async fetch() { throw Error("Fixture echo " + dummyParameter); },
  });
  assert.equal(result.status, "INCOMPLETE");
  assert(result.failures.length > 0);
  assert(!JSON.stringify(result).includes(JSON.stringify(dummyParameter).slice(1, -1)));
  assert.equal(result.error, "[PRIVATE_DIAGNOSTIC_REDACTED]");
});

test("WPS runtime input cannot be sent to a different endpoint or tenant", async () => {
  let calls = 0;
  await assert.rejects(collectMoka({ ...wpsSource, moka_endpoint: "https://example.invalid/api/outer/ats-apply/website/jobs/v2" }, privateOptions(), {
    env: { [WPS_RUNTIME_PARAMETER_ENV]: dummyParameter }, async fetch() { calls++; },
  }), /restricted to the registered WPS source/);
  assert.equal(calls, 0);
});

test("other Moka sources ignore the WPS runtime environment and keep original raw bytes", async () => {
  const ordinary = { ...wpsSource, source_id: "fixture-other-moka", moka_requires_runtime_source_parameter: false, moka_org_id: "fixture" };
  const raw = ' {"data": {"jobs": [], "total": 0}} \n';
  const result = await collectMoka(ordinary, options({ sourceId: ordinary.source_id }), {
    env: { [WPS_RUNTIME_PARAMETER_ENV]: dummyParameter },
    async fetch(url, init) { assert.equal(JSON.parse(init.body).sourceToken, undefined); return response(raw); },
  });
  assert.equal(result.complete, true);
  assert.equal(Buffer.from(result.captures[0].body_base64, "base64").toString(), raw);
  assert.equal(result.captures[0].sensitive_values_redacted, undefined);
});

test("active source registry contains no stored Moka source parameter", () => {
  const registry = JSON.parse(fs.readFileSync(new URL("../../03-strategy/official-2027-campus-sources.json", import.meta.url), "utf8"));
  assert(registry.sources.every(entry => !Object.hasOwn(entry, "moka_source_token")));
  const wps = registry.sources.find(entry => entry.source_id === "official-018");
  assert.equal(wps.moka_requires_runtime_source_parameter, false);
  assert.equal(wps.moka_endpoint, wpsSource.moka_endpoint);
  assert.equal(wps.moka_org_id, "wps");
  assert.equal(wps.moka_site_id, "41436");
});


test("private incomplete and unparseable responses cannot persist partial runtime-input echoes", async () => {
  const secretPrefix = dummyParameter.slice(0, 10);
  const malformed = await collectMoka(wpsSource, privateOptions(), {
    env: { [WPS_RUNTIME_PARAMETER_ENV]: dummyParameter },
    async fetch() { return response(secretPrefix + " malformed response"); },
  });
  assert(!JSON.stringify(malformed).includes(secretPrefix));
  assert.equal(malformed.error, "[PRIVATE_DIAGNOSTIC_REDACTED]");
  assert.equal(Buffer.from(malformed.captures[0].body_base64, "base64").toString(), "[UNINSPECTABLE_PRIVATE_RESPONSE_OMITTED]");
  const partial = await collectMoka(wpsSource, { ...privateOptions(), timeoutSeconds: 0.02 }, {
    env: { [WPS_RUNTIME_PARAMETER_ENV]: dummyParameter },
    async fetch() {
      return new Response(new ReadableStream({ start(controller) { controller.enqueue(Buffer.from(secretPrefix)); } }), { headers: { "content-type": "application/json" } });
    },
  });
  assert.equal(partial.status, "TIMEOUT");
  assert(!JSON.stringify(partial).includes(secretPrefix));
  assert.equal(Buffer.from(partial.captures[0].body_base64, "base64").toString(), "[INCOMPLETE_PRIVATE_RESPONSE_OMITTED]");
});
