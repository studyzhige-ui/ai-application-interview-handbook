#!/usr/bin/env node
/** Explicit bounded Moka jobs/v2 enumeration and detail, with lossless raw capture. */
import { createDecipheriv } from "node:crypto";
import { collectPaged, runCLI, validateOptions } from "./bounded.mjs";
import { collectBrowser } from "./browser.mjs";

export function decryptEnvelope(envelope) {
  if (!envelope?.data || !envelope?.necromancer) return envelope;
  const decipher = createDecipheriv("aes-128-cbc", Buffer.from(envelope.necromancer, "utf8"), Buffer.from("de7c21ed8d6f50fe", "utf8"));
  return JSON.parse(Buffer.concat([decipher.update(Buffer.from(envelope.data, "base64")), decipher.final()]).toString("utf8"));
}

const WPS_SOURCE_ID = "official-018";
export const WPS_RUNTIME_PARAMETER_ENV = "JD_MOKA_SOURCE_PARAMETER_OFFICIAL_018";

function runtimeParameter(source, environment) {
  if (source.source_id !== WPS_SOURCE_ID && !source.moka_requires_runtime_source_parameter) return "";
  // A runtime value may only reach this exact registered first-party tenant.
  if (source.source_id !== WPS_SOURCE_ID || source.moka_endpoint !== "https://join.wps.cn/api/outer/ats-apply/website/jobs/v2"
      || source.moka_org_id !== "wps" || String(source.moka_site_id) !== "41436") {
    throw new Error("Runtime source parameter is restricted to the registered WPS source");
  }
  const parameter = environment?.[WPS_RUNTIME_PARAMETER_ENV];
  if (typeof parameter !== "string" || !parameter.trim()) {
    throw new Error(`WPS source blocked before collection: operator must configure ${WPS_RUNTIME_PARAMETER_ENV} for this manual run`);
  }
  return parameter;
}

/** Runtime input is never attached to source/options/result objects or written to disk. */
function privateCapturePolicy(parameter) {
  const variants = [...new Set([parameter, encodeURIComponent(parameter), JSON.stringify(parameter).slice(1, -1), Buffer.from(parameter).toString("base64")])].filter(Boolean).sort((a, b) => b.length - a.length);
  function redactText(text) {
    for (const value of variants) text = text.split(value).join("[REDACTED_RUNTIME_PARAMETER]");
    return text;
  }
  function sanitize(value) {
    if (typeof value === "string") return redactText(value);
    if (Array.isArray(value)) return value.map(sanitize);
    if (value && typeof value === "object") return Object.fromEntries(Object.entries(value).map(([key, item]) => [
      redactText(key), /^(?:error|detail_error|body_error)$/.test(key) && item ? "[PRIVATE_DIAGNOSTIC_REDACTED]" : sanitize(item),
    ]));
    return value;
  }
  function sanitizeCapture(body, metadata) {
    // An interrupted body may contain a partial credential; do not persist it.
    if (metadata?.body_complete === false) return { bytes: Buffer.from("[INCOMPLETE_PRIVATE_RESPONSE_OMITTED]"), redacted: true };
    const bytes = Buffer.from(body);
    const text = bytes.toString("utf8");
    try {
      const payload = JSON.parse(text);
      // Encrypted envelopes are decodable with their embedded key. Inspect the
      // decoded response too, rather than saving a recoverable credential echo.
      if (payload?.data && payload?.necromancer) {
        const decoded = decryptEnvelope(payload);
        const original = JSON.stringify(decoded);
        const cleaned = JSON.stringify(sanitize(decoded));
        if (original !== cleaned) return { bytes: Buffer.from(cleaned), redacted: true };
      }
      const original = JSON.stringify(payload);
      const cleaned = JSON.stringify(sanitize(payload));
      if (original !== cleaned) return { bytes: Buffer.from(cleaned), redacted: true };
    } catch {
      // A private response that cannot be inspected safely is not raw-archived.
      return { bytes: Buffer.from("[UNINSPECTABLE_PRIVATE_RESPONSE_OMITTED]"), redacted: true };
    }
    const cleaned = redactText(text);
    return { bytes: Buffer.from(cleaned), redacted: cleaned !== text };
  }
  return { sanitize, sanitizeCapture };
}

export function mokaSpecification(source, sourceParameter = "") {
  if (sourceParameter && source.source_id !== WPS_SOURCE_ID) throw new Error("Runtime source parameter is restricted to the registered WPS source");
  if (source.source_id === WPS_SOURCE_ID || source.moka_requires_runtime_source_parameter || sourceParameter) {
    // Reuse the exact destination guard even when a caller builds a specification directly.
    runtimeParameter(source, { [WPS_RUNTIME_PARAMETER_ENV]: sourceParameter });
  }
  if (!source.moka_endpoint || !source.moka_org_id || !source.moka_site_id) throw new Error("Registered Moka endpoint, organization, and site are required");
  const api = new URL(source.moka_endpoint);
  if (api.protocol !== "https:" || !/\/api\/outer\/ats-apply\/website\/jobs\/v2$/.test(api.pathname)) throw new Error("Unrecognized registered Moka jobs/v2 endpoint");
  const detailApi = `${api.origin}/api/outer/ats-apply/website/job`;
  const locale = source.moka_locale || "zh-CN";
  const base = { orgId: String(source.moka_org_id), siteId: String(source.moka_site_id), locale };
  const headers = { "Accept": "application/json,*/*", "Content-Type": "application/json" };
  const post = (url, body) => ({ url, init: { method: "POST", headers, body: JSON.stringify(body) } });
  return {
    // Moka's public jobs/v2 endpoint rejects limit values above 50 with code 102.
    pageSize: 50,
    decode(payload) {
      const decoded = decryptEnvelope(payload);
      if (decoded?.code != null && decoded.code !== 0) throw new Error(`Moka upstream code=${decoded.code}: ${decoded.msg || ""}`);
      return decoded;
    },
    listRequest(offset, limit) {
      const body = { ...base, limit, offset, needStat: true, jobIdTopList: [], keyword: "", customFields: {}, site: source.moka_site || "campus" };
      if (sourceParameter) body.sourceToken = sourceParameter;
      if (source.moka_commitments?.length) body.commitments = source.moka_commitments;
      return post(api.href, body);
    },
    listData(payload) {
      const data = payload?.data || payload || {};
      const total = data.jobStats?.total ?? data.total ?? data.count;
      return { rows: data.jobs || data.list || data.items, total: total == null ? null : Number(total) };
    },
    detailRequest(row) {
      const jobId = row.id ?? row.jobId;
      return jobId == null || jobId === "" ? null : post(detailApi, { ...base, jobId: String(jobId) });
    },
    detailData(payload) { return payload?.data?.job || payload?.data || payload?.job; },
    normalize(row) {
      const id = row.id ?? row.jobId;
      const portal = source.job_list_url || source.search_url || source.portal;
      let detailUrl = row.detailUrl || row.jobUrl || "";
      if (!detailUrl && id != null && id !== "") detailUrl = `${portal.split("#")[0]}#/job/${encodeURIComponent(id)}`;
      return {
        company: source.company, title: row.title || row.name || "", job_id: id == null ? "" : String(id),
        location: (row.locations || []).map(value => value.cityName || value.country || value.address || "").filter(Boolean).join(" / "),
        category: row.commitment || "", department: row.department?.name || row.zhineng?.name || "",
        // Preserve HTML and whitespace exactly. The model, rather than a splitter, interprets it.
        description: row.jobDescription || row.description || "", requirements: row.requirement || row.requirements || "",
        official_url: detailUrl, official_api: api.href,
      };
    },
  };
}

export async function collectMoka(source, options, dependencies = {}) {
  validateOptions(options);
  const parameter = runtimeParameter(source, dependencies.env || process.env);
  const privacy = parameter ? privateCapturePolicy(parameter) : {};
  const direct = await collectPaged(source, options, mokaSpecification(source, parameter), { ...dependencies, ...privacy });
  const transportFailure = !parameter && direct.jobs.length === 0
    && (direct.failures || []).some(failure => /fetch failed|HTTP (?:403|405|429|5\d\d)/i.test(String(failure.error || "")));
  if (!transportFailure) return direct;
  const browser = await collectBrowser(source, options, dependencies);
  return {
    ...browser,
    transport_fallback: "browser_after_moka_transport_failure",
    direct_attempt: {
      status: direct.status,
      error: direct.error,
      stop_reason: direct.stop_reason,
      counts: direct.counts,
      failures: direct.failures,
    },
  };
}

await runCLI(import.meta.url, collectMoka);
