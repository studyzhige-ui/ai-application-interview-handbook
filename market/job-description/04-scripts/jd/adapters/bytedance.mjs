#!/usr/bin/env node
/** Dormant by default. Every selected list row gets detail, regardless of title. */
import { collectPaged, runCLI, validateOptions } from "./bounded.mjs";
import { feishuSpecification } from "./feishu.mjs";

export async function collectByteDance(source, options, dependencies = {}) {
  validateOptions(options);
  if (source.mode !== "bytedance_api") throw new Error("ByteDance adapter requires a registered bytedance_api source");
  return collectPaged(source, options, feishuSpecification(source, {
    api: "https://jobs.bytedance.com/api/v1/search/job/posts",
    detailRoot: "https://jobs.bytedance.com/campus/position", channel: "campus",
  }), dependencies);
}

await runCLI(import.meta.url, collectByteDance);
