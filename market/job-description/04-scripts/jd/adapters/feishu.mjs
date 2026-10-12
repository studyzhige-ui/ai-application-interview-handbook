#!/usr/bin/env node
/** Explicit, bounded first-party Feishu ATS list and detail collection. */
import { collectPaged, runCLI, validateOptions } from "./bounded.mjs";
import { collectBrowser } from "./browser.mjs";

function label(value) {
  if (typeof value === "string") return value;
  return value?.zh_cn || value?.i18n || value?.en_us || "";
}

export function feishuSpecification(source, overrides = {}) {
  const host = source.feishu_host || new URL(source.portal).hostname;
  const channel = overrides.channel || source.feishu_channel || new URL(source.portal).pathname.split("/").filter(Boolean)[0] || "campus";
  const api = overrides.api || source.api || `https://${host}/api/v1/search/job/posts`;
  const origin = new URL(api).origin;
  const detailRoot = overrides.detailRoot || source.feishu_apply_prefix || `${origin}/${channel}/position`;
  const headers = {
    "Accept": "application/json, text/plain, */*", "Content-Type": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "portal-platform": "pc", "portal-channel": channel, "website-path": channel,
    "Origin": origin, "Referer": source.portal,
  };
  return {
    browserListUrl: overrides.browserListUrl || null,
    listRequest(offset, limit) {
      const body = {
        keyword: "", limit, offset, portal_type: 3, portal_entrance: 1, language: "zh",
        job_category_id_list: [], location_code_list: [],
        subject_id_list: source.feishu_subject_ids || [],
        recruitment_id_list: overrides.recruitmentIds || source.feishu_recruitment_ids || [],
      };
      return { url: api, init: { method: "POST", headers, body: JSON.stringify(body) } };
    },
    listData(payload) {
      if (payload.code !== 0) throw new Error(`First-party ATS code=${payload.code}: ${payload.message || ""}`);
      const data = payload.data || {};
      return { rows: data.job_post_list, total: data.count == null ? null : Number(data.count) };
    },
    detailRequest(row) {
      if (row.id == null || row.id === "") return null;
      return { url: `${origin}/api/v1/job/posts/${encodeURIComponent(row.id)}`, init: { headers } };
    },
    detailData(payload) {
      if (payload.code !== 0) throw new Error(`First-party ATS detail code=${payload.code}: ${payload.message || ""}`);
      return payload.data?.job_post || payload.data;
    },
    normalize(row) {
      const id = row.id == null ? "" : String(row.id);
      return {
        company: source.company, title: row.title || "", job_id: id,
        location: (row.city_list || []).map(city => label(city?.name)).filter(Boolean).join(" / ") || label(row.city_info?.name),
        category: label(row.recruit_type?.name), department: label(row.job_category?.name) || label(row.job_function?.name),
        description: row.description || "", requirements: row.requirement || "",
        official_url: id ? `${detailRoot.replace(/\/$/, "")}/${encodeURIComponent(id)}/detail` : "", official_api: api,
      };
    },
  };
}

export async function collectFeishuWithBrowserFallback(source, options, specification, dependencies = {}) {
  const direct = await collectPaged(source, options, specification, dependencies);
  const direct405 = direct.jobs.length === 0
    && (direct.failures || []).some(failure => /HTTP 405/.test(String(failure.error || "")));
  if (!direct405) return direct;
  const portal = new URL(source.portal);
  const host = source.feishu_host || portal.hostname;
  const channel = source.feishu_channel || portal.pathname.split("/").filter(Boolean)[0] || "campus";
  let browserListUrl = specification.browserListUrl || source.job_list_url || source.portal;
  if (source.mode === "feishu_direct") {
    const derived = new URL(`https://${host}/${channel}/position/list`);
    // Project/subject filters are first-party portal state; preserve them when
    // moving from a marketing/home URL to its official position-list route.
    for (const [key, value] of portal.searchParams) derived.searchParams.append(key, value);
    browserListUrl = derived.href;
  }
  const listSource = { ...source, job_list_url: browserListUrl };
  const browser = await collectBrowser(listSource, options, dependencies);
  return {
    ...browser,
    transport_fallback: "browser_after_direct_405",
    direct_attempt: {
      status: direct.status,
      error: direct.error,
      stop_reason: direct.stop_reason,
      counts: direct.counts,
      failures: direct.failures,
    },
  };
}

export async function collectFeishu(source, options, dependencies = {}) {
  validateOptions(options);
  if (source.mode !== "feishu_direct") throw new Error("Feishu adapter requires a registered feishu_direct source");
  return collectFeishuWithBrowserFallback(source, options, feishuSpecification(source), dependencies);
}

await runCLI(import.meta.url, collectFeishu);
