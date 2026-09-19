#!/usr/bin/env node
/**
 * Enumerate Agent / AI-application related jobs from ByteDance's first-party campus ATSX.
 *
 * Instead of downloading the entire 7k+ campus pool every run, query the official ATS
 * with the complete target keyword set and union the results. This remains first-party
 * discovery and is materially faster.
 */
import { writeFileSync } from "node:fs";

const API = "https://jobs.bytedance.com/api/v1/search/job/posts";
const DETAIL_ROOT = "https://jobs.bytedance.com/campus/position";
const out = process.argv[2] || "/tmp/bytedance-campus.json";
const keywords = [
  "Agent","AI Agent","智能体","AI应用","AI 应用","大模型应用","LLM应用",
  "AI Native","Coding Agent","Code Agent","RAG","Harness","Runtime",
  "Agent Infra","MCP","Skill"
];
const headers = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
  "Accept": "application/json, text/plain, */*",
  "Content-Type": "application/json",
  "portal-platform": "pc",
  "portal-channel": "campus",
  "website-path": "campus",
  "Origin": "https://jobs.bytedance.com",
  "Referer": "https://jobs.bytedance.com/campus/position"
};

const seen = new Map();
let requestCount = 0;
let rawHits = 0;

for (const keyword of keywords) {
  let offset = 0;
  const limit = 100;
  for (let page = 0; page < 30; page++) {
    const body = {
      keyword, limit, offset,
      portal_type: 3,
      portal_entrance: 1,
      language: "zh",
      job_category_id_list: [],
      location_code_list: [],
      subject_id_list: [],
      recruitment_id_list: []
    };
    const res = await fetch(API, {method:"POST", headers, body:JSON.stringify(body)});
    requestCount++;
    if (!res.ok) throw new Error(`ByteDance HTTP ${res.status} ${res.statusText} keyword=${keyword}`);
    const payload = await res.json();
    if (payload.code !== 0) throw new Error(`ByteDance code=${payload.code}: ${payload.message||""}`);
    const d = payload.data || {};
    const rows = d.job_post_list || [];
    rawHits += rows.length;
    for (const j of rows) {
      const subjects = [];
      const rawSubjects = j.job_subject_list || (j.job_subject ? [j.job_subject] : []);
      for (const s of rawSubjects) {
        const name = typeof s?.name === "string" ? s.name : (s?.name?.zh_cn || s?.name?.i18n || "");
        if (name) subjects.push(name);
      }
      const job = {
        company: "字节跳动",
        title: j.title || "",
        job_id: String(j.id || ""),
        location: (j.city_list || []).map(x=>x.name).filter(Boolean).join(" / ") || (j.city_info?.name || ""),
        category: j.recruit_type?.name || "校园招聘",
        department: j.job_category?.name || j.job_function?.name || "",
        description: j.description || "",
        requirements: j.requirement || "",
        official_url: `${DETAIL_ROOT}/${j.id}/detail`,
        official_api: API,
        cycle_evidence: [...subjects, j.recruit_type?.name].filter(Boolean).join(" / ") || "字节官方 campus pool",
        matched_keywords: [keyword]
      };
      const key = job.job_id || job.official_url;
      if (seen.has(key)) {
        const old = seen.get(key);
        if (!old.matched_keywords.includes(keyword)) old.matched_keywords.push(keyword);
      } else {
        seen.set(key, job);
      }
    }
    const count = Number(d.count || 0);
    offset += rows.length;
    if (!rows.length || offset >= count || rows.length < limit) break;
  }
}

const jobs = [...seen.values()].sort((a,b)=>a.title.localeCompare(b.title,"zh-CN"));
writeFileSync(out, JSON.stringify({
  strategy: "official-keyword-union",
  keywords, requests: requestCount, raw_hits: rawHits,
  total: jobs.length, jobs
}, null, 2) + "\n", "utf8");
console.log(`bytedance official campus target discovery unique=${jobs.length}, raw_hits=${rawHits}, requests=${requestCount}`);
