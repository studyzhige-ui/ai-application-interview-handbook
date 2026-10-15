/** Dormant, fail-closed collection primitives. Importing this module does no I/O. */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

export const DEFAULT_REGISTRY = fileURLToPath(new URL("../../../03-strategy/official-2027-campus-sources.json", import.meta.url));
export const USAGE = "--enable-code-collection --source-id ID --max-pages N --max-jobs N --timeout-seconds SECONDS [--registry PATH] [--output NEW_PATH]";

export function validateOptions(options = {}) {
  if (options.enableCodeCollection !== true) throw new Error("Code collection is disabled; explicit --enable-code-collection is required");
  if (typeof options.sourceId !== "string" || !options.sourceId.trim()) throw new Error("An explicit registered --source-id is required");
  for (const key of ["maxPages", "maxJobs"]) {
    if (!Number.isSafeInteger(options[key]) || options[key] < 1) throw new Error(`${key} must be an explicit positive integer`);
  }
  if (!Number.isFinite(options.timeoutSeconds) || options.timeoutSeconds <= 0 || options.timeoutSeconds * 1000 > 2147483647) {
    throw new Error("timeoutSeconds must be an explicit positive finite number below 2147483 seconds");
  }
  return options;
}

export function parseArgs(argv) {
  const fields = { "--source-id": "sourceId", "--max-pages": "maxPages", "--max-jobs": "maxJobs", "--timeout-seconds": "timeoutSeconds", "--registry": "registry", "--output": "output" };
  const options = {};
  const seen = new Set();
  for (let index = 0; index < argv.length; index++) {
    const flag = argv[index];
    if (seen.has(flag)) throw new Error(`Repeated option: ${flag}`);
    seen.add(flag);
    if (flag === "--enable-code-collection") { options.enableCodeCollection = true; continue; }
    if (!fields[flag]) throw new Error(`Unknown option: ${flag}`);
    const value = argv[++index];
    if (!value || value.startsWith("--")) throw new Error(`Missing value for ${flag}`);
    options[fields[flag]] = ["--max-pages", "--max-jobs", "--timeout-seconds"].includes(flag) ? Number(value) : value;
  }
  return validateOptions(options);
}

export function selectSource(registry, sourceId) {
  const matches = (registry.sources || []).filter(source => source.source_id === sourceId);
  if (matches.length !== 1 || !matches[0].company) throw new Error(`Expected one registered source for ${sourceId}; found ${matches.length}`);
  return matches[0];
}

export class CollectionStop extends Error {
  constructor(code, message = code) { super(message); this.code = code; }
}

export function createRuntime(source, options, dependencies = {}) {
  validateOptions(options);
  if (!source?.source_id || source.source_id !== options.sourceId) throw new Error("Selected source_id does not match collection options");
  const sanitize = dependencies.sanitize || (value => value);
  const sanitizeCapture = dependencies.sanitizeCapture || (body => ({ bytes: Buffer.from(body), redacted: false }));
  const controller = new AbortController();
  const deadline = Date.now() + options.timeoutSeconds * 1000;
  const captures = [], failures = [], jobs = [], exactIds = new Set(), exactUrls = new Set(), structuralKeys = new Set();
  const counts = { list_page_attempts: 0, detail_jobs_attempted: 0, requests: 0 };
  let closed = false;
  const timer = setTimeout(() => controller.abort(new CollectionStop("TIMEOUT", "Collection wall-clock timeout")), options.timeoutSeconds * 1000);
  function check() {
    if (closed) throw new CollectionStop("CLOSED");
    if (controller.signal.aborted || Date.now() >= deadline) {
      if (!controller.signal.aborted) controller.abort(new CollectionStop("TIMEOUT"));
      throw new CollectionStop("TIMEOUT", "Collection wall-clock timeout");
    }
  }
  async function run(operation) {
    check();
    let onAbort;
    const aborted = new Promise((_, reject) => {
      onAbort = () => reject(new CollectionStop("TIMEOUT", "Collection wall-clock timeout"));
      controller.signal.addEventListener("abort", onAbort, { once: true });
    });
    try { return await Promise.race([Promise.resolve().then(operation), aborted]); }
    finally { controller.signal.removeEventListener("abort", onAbort); }
  }
  function listAttempt() {
    check();
    if (counts.list_page_attempts >= options.maxPages) throw new CollectionStop("MAX_PAGES", "List-page attempt limit reached (retries included)");
    counts.list_page_attempts++;
  }
  function capture(body, metadata) {
    const safe = sanitizeCapture(body, metadata);
    const bytes = safe.bytes;
    const entry = { capture_id: captures.length, ...sanitize(metadata), ...(safe.redacted ? { sensitive_values_redacted: true } : {}), encoding: "base64", body_base64: bytes.toString("base64"), byte_length: bytes.length, sha256: createHash("sha256").update(bytes).digest("hex") };
    captures.push(entry);
    return entry;
  }
  function addJob(job) {
    check();
    const id = job.job_id == null ? "" : String(job.job_id);
    const url = job.official_url || "";
    const structuralKey = job.collection_key == null ? "" : String(job.collection_key);
    // A known ID is authoritative: two distinct IDs may legitimately share a URL.
    // URL-only DOM representations can still deduplicate an already-seen job URL.
    // collection_key is an explicitly source-scoped within-run transport key; it is
    // never promoted to an official job ID and is only used when the source cannot
    // expose stable IDs/URLs (for example cumulative infinite-scroll DOM cards).
    if (id ? exactIds.has(id) : (url ? exactUrls.has(url) : (structuralKey && structuralKeys.has(structuralKey)))) return false;
    if (jobs.length >= options.maxJobs) throw new CollectionStop("MAX_JOBS", "Unique-job limit reached");
    if (id) exactIds.add(id);
    if (url) exactUrls.add(url);
    if (!id && !url && structuralKey) structuralKeys.add(structuralKey);
    jobs.push(job); // Missing identifiers are preserved; never deduplicate by title/body.
    return true;
  }
  async function request(url, init = {}, kind = "detail") {
    let lastError;
    for (let attempt = 1; attempt <= 3; attempt++) {
      check();
      if (kind === "list") listAttempt();
      counts.requests++;
      try {
        const response = await run(() => (dependencies.fetch || globalThis.fetch)(url, { ...init, redirect: "error", signal: controller.signal }));
        const metadata = sanitize({ url: response.url || String(url), method: init.method || "GET", request_body: init.body ?? null, status: response.status, content_type: response.headers?.get?.("content-type") || "", kind, attempt });
        const chunks = [];
        const reader = response.body?.getReader?.();
        let bytes;
        try {
          if (reader) {
            while (true) {
              const chunk = await run(() => reader.read());
              if (chunk.done) break;
              chunks.push(Buffer.from(chunk.value));
            }
            bytes = Buffer.concat(chunks);
          } else bytes = Buffer.from(await run(() => response.arrayBuffer()));
        } catch (error) {
          const partial = capture(Buffer.concat(chunks), { ...metadata, body_complete: false, body_error: String(error) });
          error.capture_id = partial.capture_id;
          if (reader) void reader.cancel().catch(() => {});
          throw error;
        }
        const entry = capture(bytes, { ...metadata, body_complete: true });
        if (!response.ok) {
          const error = new Error(`HTTP ${response.status}: ${url}`);
          error.retryable = response.status >= 500 || response.status === 429;
          error.capture_id = entry.capture_id;
          throw error;
        }
        return { bytes, capture: entry, response };
      } catch (error) {
        if (error instanceof CollectionStop || controller.signal.aborted) { check(); throw error; }
        lastError = error;
        failures.push(sanitize({ kind, url: String(url), attempt, error: String(error), capture_id: error.capture_id ?? null }));
        if (error.retryable === false || attempt === 3) throw error;
        await run(() => new Promise(resolve => setTimeout(resolve, Math.min(50 * attempt, Math.max(1, deadline - Date.now())))));
      }
    }
    throw lastError;
  }
  return {
    source, options, captures, failures, jobs, counts, signal: controller.signal,
    check, run, listAttempt, capture, addJob, request, sanitize,
    remainingMs: () => Math.max(1, deadline - Date.now()),
    close() { if (!closed) { closed = true; clearTimeout(timer); controller.abort(new CollectionStop("CLOSED")); } },
  };
}

export function collectionResult(runtime, state = {}) {
  const listComplete = state.listComplete === true;
  const detailComplete = runtime.jobs.every(job => job.detail_status === "OK");
  const complete = listComplete && detailComplete && !state.error;
  return runtime.sanitize({
    source_id: runtime.source.source_id, company: runtime.source.company, review_state: "unreviewed",
    status: complete ? "OK" : state.error?.code === "TIMEOUT" ? "TIMEOUT" : ["MAX_PAGES", "MAX_JOBS"].includes(state.error?.code) ? "LIMITED" : "INCOMPLETE",
    complete, list_scan_complete: listComplete, details_complete: detailComplete,
    total: state.total ?? null, limits: { max_pages: runtime.options.maxPages, max_jobs: runtime.options.maxJobs, timeout_seconds: runtime.options.timeoutSeconds },
    counts: { ...runtime.counts, jobs: runtime.jobs.length },
    error: state.error ? String(state.error) : "", stop_reason: state.error?.code || "",
    jobs: runtime.jobs, captures: runtime.captures, failures: runtime.failures,
  });
}

/** A configured structural API collector: no keyword, title, role, or body matching. */
export async function collectPaged(source, options, specification, dependencies = {}) {
  const runtime = createRuntime(source, options, dependencies);
  const state = { total: null, listComplete: false };
  let offset = 0;
  try {
    while (true) {
      runtime.check();
      if (runtime.jobs.length >= options.maxJobs) throw new CollectionStop("MAX_JOBS");
      const configuredPageSize = specification.pageSize == null ? 100 : Number(specification.pageSize);
      if (!Number.isSafeInteger(configuredPageSize) || configuredPageSize < 1) throw new Error("Adapter pageSize must be a positive integer");
      const size = Math.min(configuredPageSize, options.maxJobs - runtime.jobs.length);
      const request = specification.listRequest(offset, size);
      const response = await runtime.request(request.url, request.init, "list");
      const payload = JSON.parse(response.bytes.toString("utf8"));
      const decoded = specification.decode ? specification.decode(payload) : payload;
      const { rows, total } = specification.listData(decoded);
      if (!Array.isArray(rows) || !Number.isSafeInteger(total) || total < 0) throw new Error("Official list response missing rows or a valid advertised total");
      if (state.total === null) state.total = total;
      else if (state.total !== total) throw new Error("Advertised total changed during pagination; completeness cannot be certified");
      let added = 0;
      for (const raw of rows) {
        runtime.check();
        const job = { ...specification.normalize(raw), raw_list: raw, list_capture_id: response.capture.capture_id, detail_status: "PENDING" };
        if (!runtime.addJob(job)) continue;
        added++;
        const detailRequest = specification.detailRequest(raw);
        if (!detailRequest) { job.detail_status = "NEEDS_ADAPTER"; continue; }
        runtime.counts.detail_jobs_attempted++;
        try {
          const detail = await runtime.request(detailRequest.url, detailRequest.init, "detail");
          job.detail_capture_id = detail.capture.capture_id;
          const detailPayload = JSON.parse(detail.bytes.toString("utf8"));
          const detailDecoded = specification.decode ? specification.decode(detailPayload) : detailPayload;
          const detailRaw = specification.detailData(detailDecoded);
          if (!detailRaw || typeof detailRaw !== "object" || Array.isArray(detailRaw) || !Object.keys(detailRaw).length) throw new Error("Official detail response missing job data");
          const normalized = specification.normalize(detailRaw);
          if (job.job_id && normalized.job_id && job.job_id !== normalized.job_id) throw new Error("Detail ID does not match requested job");
          job.detail_status = "OK";
          job.raw_detail = detailRaw;
          job.detail_capture_id = detail.capture.capture_id;
          for (const [key, value] of Object.entries(normalized)) if (value !== "" && value != null) job[key] = value;
        } catch (error) {
          job.detail_status = error.code === "TIMEOUT" ? "TIMEOUT" : "ERROR";
          job.detail_error = String(error);
          if (error instanceof CollectionStop) throw error;
        }
      }
      offset += rows.length;
      if (runtime.jobs.length === state.total) { state.listComplete = true; break; }
      if (runtime.jobs.length > state.total) throw new Error("Unique jobs exceed advertised total");
      if (!rows.length || !added || offset >= state.total) throw new Error("Incomplete official pool: empty/repeated page or duplicate IDs below advertised total");
      // A short page never certifies completeness when the source advertises more.
    }
  } catch (error) { state.error = error; }
  finally { runtime.close(); }
  return collectionResult(runtime, state);
}

export async function runCLI(moduleUrl, collector, argv = process.argv.slice(2)) {
  if (!process.argv[1] || path.resolve(process.argv[1]) !== fileURLToPath(moduleUrl)) return;
  if (argv.length === 1 && argv[0] === "--help") { process.stdout.write(`${USAGE}\n`); return; }
  try {
    const options = parseArgs(argv); // All gates precede even registry reads.
    if (options.output && fs.existsSync(options.output)) throw new Error("Output already exists; original files will not be overwritten");
    const registry = JSON.parse(fs.readFileSync(options.registry || DEFAULT_REGISTRY, "utf8"));
    const source = selectSource(registry, options.sourceId);
    const result = await collector(source, options);
    const payload = { generated_at: new Date().toISOString(), collection_mode: "manual-explicit-bounded", source_count: 1, results: [result] };
    const serialized = JSON.stringify(payload, null, 2) + "\n";
    if (options.output) fs.writeFileSync(options.output, serialized, { encoding: "utf8", flag: "wx" });
    else process.stdout.write(serialized);
    if (!result.complete) process.exitCode = 1;
  } catch (error) { process.stderr.write(`${error.message}\nUsage: ${USAGE}\n`); process.exitCode = 2; }
}
