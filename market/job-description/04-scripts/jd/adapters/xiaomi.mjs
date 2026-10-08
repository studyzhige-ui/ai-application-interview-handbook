#!/usr/bin/env node
/** Dormant, bounded Xiaomi ATS collector, retaining the registered campus scope. */
import { collectPaged, runCLI, validateOptions } from "./bounded.mjs";
import { feishuSpecification } from "./feishu.mjs";

export async function collectXiaomi(source, options, dependencies = {}) {
  validateOptions(options);
  if (source.mode !== "xiaomi_api") throw new Error("Xiaomi adapter requires a registered xiaomi_api source");
  return collectPaged(source, options, feishuSpecification(source, {
    api: "https://xiaomi.jobs.f.mioffice.cn/api/v1/search/job/posts",
    detailRoot: "https://xiaomi.jobs.f.mioffice.cn/campus/position", channel: "campus",
    recruitmentIds: source.feishu_recruitment_ids || ["201"],
  }), dependencies);
}

await runCLI(import.meta.url, collectXiaomi);
