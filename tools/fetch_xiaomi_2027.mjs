#!/usr/bin/env node
/**
 * Enumerate Xiaomi official campus pool via Xiaomi's self-hosted ATSX endpoint.
 * First-party only: xiaomi.jobs.f.mioffice.cn.
 */
import { writeFileSync } from "node:fs";

const API = "https://xiaomi.jobs.f.mioffice.cn/api/v1/search/job/posts";
const DETAIL_ROOT = "https://xiaomi.jobs.f.mioffice.cn/campus/position";
const out = process.argv[2] || "/tmp/xiaomi-2027-campus.json";

const headers = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
  "Accept": "application/json, text/plain, */*",
  "Content-Type": "application/json",
  "portal-platform": "pc",
  "portal-channel": "campus",
  "website-path": "campus",
  "Referer": "https://xiaomi.jobs.f.mioffice.cn/campus/"
};

const jobs = [];
let offset = 0;
const limit = 100;
let total = null;

for (let page = 0; page < 100; page++) {
  const body = {
    keyword: "",
    limit,
    offset,
    portal_type: 3,
    portal_entrance: 1,
    language: "zh",
    recruitment_id_list: ["201"]
  };
  const res = await fetch(API, {method: "POST", headers, body: JSON.stringify(body)});
  if (!res.ok) throw new Error(`Xiaomi HTTP ${res.status} ${res.statusText}`);
  const payload = await res.json();
  if (payload.code !== 0) throw new Error(`Xiaomi code=${payload.code}: ${payload.message || ""}`);
  const d = payload.data || {};
  const rows = d.job_post_list || [];
  if (total === null) total = Number(d.count || 0);
  for (const j of rows) {
    jobs.push({
      company: "小米",
      title: j.title || "",
      job_id: String(j.id || ""),
      location: (j.city_list || []).map(x => x.name).filter(Boolean).join(" / ") || (j.city_info?.name || ""),
      category: j.recruit_type?.name || "校招正式",
      department: j.job_function?.name || j.job_category?.name || "",
      description: j.description || "",
      requirements: j.requirement || "",
      official_url: `${DETAIL_ROOT}/${j.id}/detail`,
      official_api: API,
      cycle_evidence: [j.job_subject?.name?.zh_cn, j.job_subject?.name, j.recruit_type?.name].filter(x => typeof x === "string" && x).join(" / ") || "小米官方 campus 正式岗池"
    });
  }
  offset += rows.length;
  if (!rows.length || (total && offset >= total)) break;
}

writeFileSync(out, JSON.stringify({total: total ?? jobs.length, jobs}, null, 2) + "\n", "utf8");
console.log(`xiaomi official campus fetched=${jobs.length}, total=${total}`);
