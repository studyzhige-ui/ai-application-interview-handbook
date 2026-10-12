#!/usr/bin/env node
/**
 * Dormant first-party browser collector. Only an explicitly selected registry
 * source is opened. Pagination and detail selection use structural IDs/URLs;
 * text is retained verbatim for later model review, never used for role ranking.
 */
import { CollectionStop, createRuntime, collectionResult, runCLI, validateOptions } from "./bounded.mjs";

const TITLE_KEYS = ["positionName", "jobName", "jobTitle", "positionTitle", "recruitPostName", "postName", "title", "name"];
const ID_KEYS = ["positionId", "jobId", "postId", "publishId", "reqId", "id", "code"];
const DESCRIPTION_KEYS = ["description", "jobDescription", "jobDesc", "positionDesc", "responsibility", "responsibilities", "jobDuty", "duty", "workContent", "desc", "postDuty"];
const REQUIREMENT_KEYS = ["requirement", "requirements", "jobRequirement", "positionRequire", "positionDemand", "qualification", "qualifications", "serveRequirement", "request"];
const URL_KEYS = ["shareUrl", "detailUrl", "jobUrl", "positionUrl", "url", "href", "link"];
const LIST_KEYS = new Set(["jobs", "job_post_list", "positions", "positionList", "jobList", "listData", "posts", "postList"]);
const TOTAL_KEYS = ["total", "totalCount", "count", "recordsTotal", "totalNum", "totalSize", "totalElements"];
const PAGE_KEYS = ["current", "currentPage", "pageNum", "pageIndex", "pageNo", "page"];
const KEYWORD_KEYS = ["keyword", "keyWord", "postName", "jobTitle", "positionName", "kw", "keywords"];
function pick(object, keys) {
  for (const key of keys) if (object?.[key] != null && typeof object[key] !== "object") return String(object[key]);
  return "";
}

export function assertNoSecurityChallenge(url, body) {
  if (/\/web\/passport\/zp\/(?:security|verify)(?:[/?#.]|$)/i.test(url || "") || /(?:^|\n)\s*(?:安全验证|访问异常)(?:\s|$)/i.test(body || "")) {
    throw new CollectionStop("OFFICIAL_SECURITY_CHALLENGE", "First-party security challenge; collection is incomplete");
  }
}

export function jobLinkLike(href) {
  if (/(?:\/position\/list(?:[?#]|$)|\/jobs?\/?(?:[?#]|$)|\/positions?\/?(?:[?#]|$))/i.test(href || "")) return false;
  return /(?:\/jobs?\/[^/?#]+|\/positions?\/[^/?#]+|job-info|job[_-]?detail|postdetail|positionid=|jobid=|postid=|#\/jobs?\/[^/?#]+|#\/positions?\/[^/?#]+|jobs\.ashbyhq\.com\/[^/]+\/[0-9a-f-]{20,})/i.test(href || "");
}

/** Recognize list structure, never the meaning of any title or description. */
export function extractList(payload) {
  const candidates = [];
  function totalOf(parent) {
    for (const container of [parent, parent?.page, parent?.pageInfo, parent?.pageForm, parent?.pagination]) {
      for (const key of TOTAL_KEYS) {
        const value = container?.[key];
        if (value != null && value !== "" && Number.isSafeInteger(Number(value)) && Number(value) >= 0) return Number(value);
      }
    }
    return null;
  }
  function visit(node, parent, key, depth = 0) {
    if (depth > 12 || node == null || typeof node !== "object") return;
    if (Array.isArray(node)) {
      const known = LIST_KEYS.has(key);
      const structural = node.length > 0 && node.every(row => row && typeof row === "object" && !Array.isArray(row) && pick(row, ID_KEYS) && pick(row, TITLE_KEYS));
      if (known || structural) candidates.push({ rows: node, total: totalOf(parent), path: key });
      else for (const child of node) visit(child, node, "", depth + 1);
    } else for (const [childKey, child] of Object.entries(node)) visit(child, node, childKey, depth + 1);
  }
  visit(payload, null, "");
  return candidates.find(candidate => LIST_KEYS.has(candidate.path)) || candidates[0] || null;
}

export function normalizeBrowserRow(row, source, responseUrl, pageUrl) {
  const id = pick(row, ID_KEYS);
  const feishuSearch = /\/api\/v1\/search\/job\/posts/.test(responseUrl);
  let url = pick(row, URL_KEYS);
  if (!url && id && feishuSearch) {
    const origin = new URL(responseUrl).origin;
    const channel = source.feishu_channel || new URL(pageUrl).pathname.split("/").filter(Boolean)[0] || "campus";
    url = `${origin}/${channel}/position/${encodeURIComponent(id)}/detail`;
  }
  try { if (url) url = new URL(url, pageUrl).href; } catch { url = ""; }
  const location = feishuSearch
    ? (row.city_list || []).map(city => pick(city, ["name", "i18n_name", "en_name"])).filter(Boolean).join(" / ") || pick(row.city_info, ["name", "i18n_name", "en_name"])
    : pick(row, ["location", "city", "workCity", "workPlace", "workLocation", "cityName", "workCityName"]);
  const category = feishuSearch ? pick(row.recruit_type, ["name", "i18n_name", "en_name"]) : "";
  const department = feishuSearch
    ? pick(row.job_category, ["name", "i18n_name", "en_name"]) || pick(row.job_function, ["name", "i18n_name", "en_name"])
    : pick(row, ["department", "departmentName", "deptName", "categoryName", "jobCategory"]);
  return {
    company: source.company, job_id: id, title: pick(row, TITLE_KEYS),
    description: pick(row, DESCRIPTION_KEYS), requirements: pick(row, REQUIREMENT_KEYS),
    location, category, department,
    official_url: url, official_api: responseUrl, raw_list: row,
    list_detail_complete: feishuSearch && Object.hasOwn(row, "description") && Object.hasOwn(row, "requirement"),
  };
}

function findField(object, keys, depth = 0) {
  if (!object || typeof object !== "object" || Array.isArray(object) || depth > 8) return null;
  for (const key of keys) if (Object.hasOwn(object, key)) return { object, key };
  for (const value of Object.values(object)) { const hit = findField(value, keys, depth + 1); if (hit) return hit; }
  return null;
}

/** Replay only an observed blank-query unsigned pagination contract. */
export function nextRequest(observed) {
  if (!observed?.list?.rows.length || observed.list.total == null) return null;
  const url = new URL(observed.url);
  // Signed ATS calls must use the site's own UI so signatures remain site-issued.
  if (/\/api\/v1\/search\/job\/posts/.test(url.pathname) || [...url.searchParams.keys()].some(key => /sign|token|nonce/i.test(key))) return null;
  let body = null, bodyType = "none";
  if (observed.postData) {
    try { body = JSON.parse(observed.postData); bodyType = "json"; }
    catch { body = Object.fromEntries(new URLSearchParams(observed.postData)); bodyType = "form"; }
  }
  for (const key of KEYWORD_KEYS) {
    const hit = findField(body, [key]);
    if (hit && String(hit.object[key] ?? "") !== "") return null;
    if (url.searchParams.has(key) && url.searchParams.get(key) !== "") return null;
  }
  let advanced = false;
  const offset = findField(body, ["offset"]);
  const page = findField(body, PAGE_KEYS);
  if (offset) { offset.object[offset.key] = Number(offset.object[offset.key]) + observed.list.rows.length; advanced = true; }
  else if (page) { page.object[page.key] = Number(page.object[page.key]) + 1; advanced = true; }
  if (url.searchParams.has("offset")) { url.searchParams.set("offset", String(Number(url.searchParams.get("offset")) + observed.list.rows.length)); advanced = true; }
  else {
    const pageKey = PAGE_KEYS.find(key => url.searchParams.has(key));
    if (pageKey) { url.searchParams.set(pageKey, String(Number(url.searchParams.get(pageKey)) + 1)); advanced = true; }
  }
  if (!advanced) return null;
  return { url: url.href, method: observed.method || "POST", bodyType, body };
}

function registeredOrigins(source) {
  const urls = [source.portal, source.job_list_url, source.search_url, source.official_root, source.api, source.detail_api, ...(source.extra_portals || []), ...(source.extra_job_list_urls || [])].filter(Boolean);
  return new Set(urls.map(url => new URL(url).origin));
}

export async function createPlaywrightDriver(source, runtime, dependencies = {}) {
  // Lazy dependency: imports, help, and invalid/disabled commands never load Playwright.
  const chromium = dependencies.chromium || (await import("playwright")).chromium;
  const browser = await runtime.run(() => chromium.launch({ headless: true, timeout: runtime.remainingMs() }));
  let context;
  const abortClose = () => { void browser.close().catch(() => {}); };
  runtime.signal.addEventListener("abort", abortClose, { once: true });
  try {
    context = await runtime.run(() => browser.newContext());
    const origins = registeredOrigins(source);
    await runtime.run(() => context.route("**/*", route => {
      const request = route.request();
      if (runtime.signal.aborted || ["image", "media", "font"].includes(request.resourceType())) return route.abort();
      // Never follow a navigation/redirect out of the selected registry source.
      if (request.isNavigationRequest() && !origins.has(new URL(request.url()).origin)) return route.abort();
      return route.continue();
    }));
    const listPage = await runtime.run(() => context.newPage());
    let pending = [], observations = [], lastObserved = null, lastDomRowCount = 0;
    function attach(page, kind) {
      page.on("response", response => {
        let origin;
        try { origin = new URL(response.url()).origin; } catch { return; }
        const contentType = response.headers()["content-type"] || "";
        if (!origins.has(origin) || !/json|html/i.test(contentType)) return;
        const task = (async () => {
          const bytes = await runtime.run(() => response.body());
          runtime.check();
          const request = response.request();
          const capture = runtime.capture(bytes, { url: response.url(), method: request.method(), request_body: request.postData(), status: response.status(), content_type: contentType, kind });
          if (kind !== "list" || !/json/i.test(contentType) || response.status() !== 200) return;
          let payload; try { payload = JSON.parse(bytes.toString("utf8")); } catch { return; }
          const list = extractList(payload);
          if (list) observations.push({ url: response.url(), method: request.method(), postData: request.postData(), list, capture_id: capture.capture_id });
        })().catch(error => { if (!runtime.signal.aborted) runtime.failures.push({ kind, url: response.url(), error: String(error) }); });
        pending.push(task);
      });
    }
    attach(listPage, "list");
    async function settle(page) {
      await runtime.run(() => page.waitForLoadState("networkidle", { timeout: Math.min(1000, runtime.remainingMs()) })).catch(error => { runtime.check(); });
      if (page === listPage && source.browser_settle_ms) {
        const delay = Math.min(Number(source.browser_settle_ms), runtime.remainingMs());
        if (Number.isFinite(delay) && delay > 0) await runtime.run(() => page.waitForTimeout(delay));
      }
      const tasks = pending; pending = [];
      await runtime.run(() => Promise.all(tasks));
    }
    async function navigation(page, url) {
      if (!origins.has(new URL(url).origin)) throw new Error(`Detail URL is outside the selected registered source: ${url}`);
      for (let attempt = 1; attempt <= 3; attempt++) {
        runtime.check();
        try {
          runtime.counts.requests++;
          const response = await runtime.run(() => page.goto(url, { waitUntil: "domcontentloaded", timeout: runtime.remainingMs() }));
          await settle(page);
          if (response && response.status() >= 400) {
            const error = new Error(`Official page HTTP ${response.status()}: ${url}`);
            error.retryable = response.status() >= 500 || response.status() === 429;
            throw error;
          }
          return;
        } catch (error) {
          runtime.check();
          runtime.failures.push({ kind: page === listPage ? "list" : "detail", url, attempt, error: String(error) });
          if (attempt === 3 || error.retryable === false || error instanceof CollectionStop) throw error;
          if (page === listPage) runtime.listAttempt();
        }
      }
    }
    return {
      async open(url) { await navigation(listPage, url); },
      async snapshot() {
        await settle(listPage);
        const body = await runtime.run(() => listPage.locator("body").innerText());
        assertNoSecurityChallenge(listPage.url(), body);
        const html = await runtime.run(() => listPage.content());
        const domCapture = runtime.capture(Buffer.from(html, "utf8"), { url: listPage.url(), kind: "rendered_list_dom", content_type: "text/html; charset=utf-8" });
        const links = await runtime.run(() => listPage.locator(source.job_link_selector || "a[href]").evaluateAll(anchors => anchors.map(anchor => ({ href: anchor.href, title: anchor.innerText || anchor.textContent || "" }))));
        const observed = observations; observations = [];
        const rows = [];
        let total = null;
        if (source.dom_total_pattern) {
          const match = body.match(new RegExp(source.dom_total_pattern, "i"));
          if (match?.[1]) {
            const parsed = Number(String(match[1]).replace(/,/g, ""));
            if (Number.isSafeInteger(parsed) && parsed >= 0) total = parsed;
          }
        }
        // A page can emit job recommendations, dictionaries and the real result list.
        // Mixing every structurally list-like response inflates counts and can make a
        // valid page appear larger than its advertised total. Prefer the strongest
        // single list contract for this page: known Feishu search first, then the
        // largest advertised pool, then the largest visible row set.
        const ranked = observed.slice().sort((a, b) => {
          const aFeishu = /\/api\/v1\/search\/job\/posts/.test(new URL(a.url).pathname) ? 1 : 0;
          const bFeishu = /\/api\/v1\/search\/job\/posts/.test(new URL(b.url).pathname) ? 1 : 0;
          if (aFeishu !== bFeishu) return bFeishu - aFeishu;
          const aTotal = a.list.total == null ? -1 : a.list.total;
          const bTotal = b.list.total == null ? -1 : b.list.total;
          if (aTotal !== bTotal) return bTotal - aTotal;
          return (b.list.rows?.length || 0) - (a.list.rows?.length || 0);
        });
        const primary = ranked[0] || null;
        if (primary) {
          lastObserved = primary;
          if (primary.list.total != null) total = primary.list.total;
          for (const raw of primary.list.rows) rows.push({ ...normalizeBrowserRow(raw, source, primary.url, listPage.url()), list_capture_id: primary.capture_id });
        }
        if (source.dom_job_selector) {
          const domRows = await runtime.run(() => listPage.locator(source.dom_job_selector).evaluateAll((nodes, config) => {
            const read = (node, selector) => {
              if (!selector) return "";
              const element = node.querySelector(selector);
              return (element?.innerText || element?.textContent || "").trim();
            };
            return nodes.map((node, index) => {
              const link = config.urlSelector ? node.querySelector(config.urlSelector) : node.querySelector("a[href]");
              return {
                title: read(node, config.titleSelector),
                location: read(node, config.locationSelector),
                category: read(node, config.categorySelector),
                department: read(node, config.departmentSelector),
                official_url: link?.href || "",
                raw_text: (node.innerText || node.textContent || "").trim(),
                dom_index: index,
              };
            });
          }, {
            titleSelector: source.dom_title_selector,
            locationSelector: source.dom_location_selector,
            categorySelector: source.dom_category_selector,
            departmentSelector: source.dom_department_selector,
            urlSelector: source.dom_url_selector,
          }));
          lastDomRowCount = domRows.length;
          for (const row of domRows) {
            rows.push({
              company: source.company, job_id: "", title: row.title,
              location: row.location, category: row.category, department: row.department,
              description: "", requirements: "", official_url: row.official_url,
              raw_list: { dom_index: row.dom_index, text: row.raw_text },
              list_capture_id: domCapture.capture_id,
            });
          }
        } else lastDomRowCount = 0;
        for (const link of links) {
          if (!link.href || !origins.has(new URL(link.href).origin) || !(source.job_link_selector || jobLinkLike(link.href))) continue;
          // Link matching is structural; all link labels, including empty labels, are retained.
          rows.push({ company: source.company, job_id: "", title: link.title, official_url: link.href, raw_list: link, list_capture_id: domCapture.capture_id });
        }
        return { rows, total, page_url: listPage.url(), raw_html_capture_id: domCapture.capture_id };
      },
      async nextAction() {
        const feishuNext = listPage.locator("li.atsx-pagination-next:not(.atsx-pagination-disabled)").last();
        if (await runtime.run(() => feishuNext.count()) && await runtime.run(() => feishuNext.isVisible())) {
          return async () => {
            await runtime.run(async () => {
              const response = listPage.waitForResponse(
                item => /\/api\/v1\/search\/job\/posts/.test(new URL(item.url()).pathname) && item.status() === 200,
                { timeout: Math.min(5000, runtime.remainingMs()) },
              ).catch(() => null);
              await feishuNext.click({ timeout: runtime.remainingMs() });
              await response;
            });
            await settle(listPage);
          };
        }
        const candidates = [
          listPage.getByRole("button", { name: /^(?:下一页|下页|next)(?:\s|$)/i }).last(),
          listPage.getByRole("link", { name: /^(?:下一页|下页|next)(?:\s|$)/i }).last(),
          listPage.locator('[rel="next"], [class*="pagination"] [class*="next"], [aria-label*="next" i]').last(),
        ];
        for (const next of candidates) {
          const exists = await runtime.run(() => next.count());
          if (!exists || !(await runtime.run(() => next.isVisible()))) continue;
          const disabled = await runtime.run(() => next.isDisabled());
          const ariaDisabled = await runtime.run(() => next.getAttribute("aria-disabled"));
          const classes = await runtime.run(() => next.getAttribute("class"));
          if (disabled || ariaDisabled === "true" || /disabled/i.test(classes || "")) continue;
          return async () => { await runtime.run(() => next.click({ timeout: runtime.remainingMs() })); await settle(listPage); };
        }
        if (source.dom_infinite_scroll && lastDomRowCount) {
          return async () => {
            await runtime.run(() => listPage.evaluate(() => window.scrollTo(0, document.body.scrollHeight)));
            const delay = Math.min(Number(source.browser_scroll_settle_ms || 1200), runtime.remainingMs());
            if (Number.isFinite(delay) && delay > 0) await runtime.run(() => listPage.waitForTimeout(delay));
            await settle(listPage);
          };
        }
        const replay = nextRequest(lastObserved);
        if (!replay) return null;
        return async () => {
          runtime.counts.requests++;
          await runtime.run(() => listPage.evaluate(async request => {
            const init = { method: request.method, redirect: "error" };
            if (request.method !== "GET" && request.method !== "HEAD") {
              init.headers = { "Content-Type": request.bodyType === "form" ? "application/x-www-form-urlencoded;charset=UTF-8" : "application/json" };
              init.body = request.bodyType === "form" ? new URLSearchParams(request.body).toString() : JSON.stringify(request.body);
            }
            const response = await fetch(request.url, init);
            await response.arrayBuffer();
            if (!response.ok) throw new Error(`Observed pagination HTTP ${response.status}`);
          }, replay));
          await settle(listPage);
        };
      },
      async detail(job) {
        const page = await runtime.run(() => context.newPage());
        attach(page, "detail");
        try {
          await navigation(page, job.official_url);
          const body = await runtime.run(() => page.locator("body").innerText());
          assertNoSecurityChallenge(page.url(), body);
          const html = await runtime.run(() => page.content());
          const capture = runtime.capture(Buffer.from(html, "utf8"), { url: page.url(), kind: "rendered_detail_dom", content_type: "text/html; charset=utf-8" });
          return { raw_detail_text: body, raw_detail_html: html, detail_capture_id: capture.capture_id, final_url: page.url() };
        } finally { await page.close().catch(() => {}); }
      },
      async close() { runtime.signal.removeEventListener("abort", abortClose); await browser.close(); },
    };
  } catch (error) { runtime.signal.removeEventListener("abort", abortClose); await browser.close().catch(() => {}); throw error; }
}

export async function collectBrowser(source, options, dependencies = {}) {
  validateOptions(options);
  const runtime = createRuntime(source, options, dependencies);
  const state = { total: null, listComplete: false };
  let driver;
  try {
    driver = await runtime.run(() => (dependencies.driverFactory || createPlaywrightDriver)(source, runtime, dependencies));
    const seeds = [...new Set([source.job_list_url || source.search_url || source.portal, ...(source.extra_portals || []), ...(source.extra_job_list_urls || [])].filter(Boolean))];
    if (!seeds.length) throw new Error("Registered source has no list portal");
    let allListsComplete = true;
    for (const seed of seeds) {
      runtime.listAttempt();
      await runtime.run(() => driver.open(seed));
      const seedStart = runtime.jobs.length;
      let seedTotal = null;
      while (true) {
        const snapshot = await runtime.run(() => driver.snapshot());
        if (snapshot.total != null) {
          if (seedTotal != null && seedTotal !== snapshot.total) throw new Error("Advertised browser list total changed");
          seedTotal = snapshot.total;
          state.total = seeds.length === 1 ? seedTotal : null;
        }
        let added = 0;
        for (const row of snapshot.rows || []) {
          const job = { ...row, detail_status: "PENDING" };
          if (!runtime.addJob(job)) continue;
          added++;
          if (job.list_detail_complete) {
            delete job.list_detail_complete;
            job.detail_status = "OK";
            continue;
          }
          delete job.list_detail_complete;
          if (!job.official_url) { job.detail_status = "NEEDS_ADAPTER"; continue; }
          runtime.counts.detail_jobs_attempted++;
          try { Object.assign(job, await runtime.run(() => driver.detail(job)), { detail_status: "OK" }); }
          catch (error) {
            job.detail_status = error.code === "TIMEOUT" ? "TIMEOUT" : "ERROR";
            job.detail_error = String(error);
            if (error instanceof CollectionStop) throw error;
          }
        }
        const count = runtime.jobs.length - seedStart;
        if (seedTotal != null && count === seedTotal) break;
        if (seedTotal != null && count > seedTotal) throw new Error("Collected unique jobs exceed advertised browser total");
        if (runtime.jobs.length >= options.maxJobs) throw new CollectionStop("MAX_JOBS");
        const next = await runtime.run(() => driver.nextAction());
        if (!next) { allListsComplete = false; break; }
        if (!added && count > 0) throw new Error("Pagination made no ID/URL progress; collection is incomplete");
        runtime.listAttempt();
        await runtime.run(next);
      }
    }
    state.listComplete = allListsComplete;
    if (!allListsComplete) state.error = new CollectionStop("LIST_TOTAL_UNPROVEN", "Visible records retained; full-list total is not proven");
  } catch (error) { state.error = error; }
  finally {
    if (driver) {
      let cleanupTimer;
      try { await Promise.race([driver.close().catch(() => {}), new Promise(resolve => { cleanupTimer = setTimeout(resolve, 750); })]); }
      finally { clearTimeout(cleanupTimer); }
    }
    runtime.close();
  }
  return collectionResult(runtime, state);
}

await runCLI(import.meta.url, collectBrowser);
