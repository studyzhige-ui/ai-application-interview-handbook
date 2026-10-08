"""Company collection orchestration; completed enumeration is separate from matches."""
from __future__ import annotations
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from .model import Job, SourceResult, txt
from .matching import RoleMatcher
from .freshness import cache_is_fresh
from .paths import BROWSER_CACHE, FEISHU_CACHE, MOKA_CACHE
from .adapters.official import FETCHERS
from .adapters.http import discover_api_candidates

def load_cache(path):
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if cache_is_fresh(payload):
            return {x["company"]: x for x in payload.get("results", []) if x.get("company")}
        print(f"Ignoring stale discovery cache: {path.name}", file=sys.stderr)
    except (ValueError, OSError) as exc:
        print(f"Ignoring unreadable discovery cache {path.name}: {exc}", file=sys.stderr)
    return {}

def to_jobs(company: str, raw_jobs: list[dict], fallback_url: str, fallback_api: str) -> list[Job]:
    return [
        Job(
            company,
            txt(j.get("title")),
            txt(j.get("job_id")),
            txt(j.get("location")),
            txt(j.get("category") or "官方动态招聘"),
            txt(j.get("department")),
            txt(j.get("description")),
            txt(j.get("requirements")),
            txt(j.get("official_url") or fallback_url),
            txt(j.get("official_api") or fallback_api),
            txt(j.get("cycle_evidence")),
        )
        for j in raw_jobs
    ]


class Collector:
    def __init__(self, cfg, *, browser=None, feishu=None, moka=None, fetchers=None):
        self.matcher = RoleMatcher(cfg)
        self.dynamic_by_company = load_cache(BROWSER_CACHE) if browser is None else browser
        self.feishu_by_company = load_cache(FEISHU_CACHE) if feishu is None else feishu
        self.moka_by_company = load_cache(MOKA_CACHE) if moka is None else moka
        self.fetchers = FETCHERS if fetchers is None else fetchers

    def collect(self, src: dict) -> tuple[SourceResult, list[Job]]:
        company = src["company"]
        mode = src["mode"]

        feishu = self.feishu_by_company.get(company) or {}
        if feishu.get("status") == "OK" and feishu.get("complete") is True:
            jobs = to_jobs(company, feishu.get("jobs") or [], src["portal"], "FEISHU:" + src["portal"])
            matches = self.matcher.target_matches(jobs, src)
            return SourceResult(
                company, "feishu_official", src["portal"],
                "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                len(jobs), len(matches)
            ), matches

        moka = self.moka_by_company.get(company) or {}
        if moka.get("status") == "OK" and moka.get("complete") is True:
            jobs = to_jobs(company, moka.get("jobs") or [], src["portal"], txt(moka.get("api")) or ("MOKA:" + src["portal"]))
            matches = self.matcher.target_matches(jobs, src)
            return SourceResult(
                company, "moka_official", src["portal"],
                "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                len(jobs), len(matches)
            ), matches

        if mode == "portal_only":
            dyn = self.dynamic_by_company.get(company) or {}
            raw_jobs = dyn.get("jobs") or []
            jobs = to_jobs(company, raw_jobs, src["portal"], "BROWSER:" + src["portal"])
            matches = self.matcher.target_matches(jobs, src)
            raw_status = txt(dyn.get("status"))
            full_search = bool(dyn.get("list_scan_complete"))
            if raw_status == "BROWSER_ENUMERATED" and full_search:
                status = "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES"
                error = ""
            elif raw_status in ("BROWSER_ENUMERATED_ZERO","BROWSER_OK_0_MATCH") and full_search:
                status = "ENUMERATED_ZERO_MATCHES"
                error = ""
            elif raw_status in ("BROWSER_NO_PUBLIC_CAMPUS","BROWSER_NO_PUBLIC_2027"):
                status = "NO_PUBLIC_CAMPUS_PROJECT"
                error = "官网当前未公开校园招聘职位池"
            elif raw_status in ("BROWSER_NO_CAMPUS_EVIDENCE","BROWSER_NO_2027_EVIDENCE","BROWSER_CAMPUS_NEEDS_ADAPTER","BROWSER_2027_NEEDS_ADAPTER"):
                status = "BLOCKED"
                error = "官方校招入口尚未完成可靠全量枚举；不能判定 0 岗位"
            elif raw_status == "BROWSER_ERROR":
                status = "BLOCKED"
                error = txt(dyn.get("error")) or "浏览器枚举失败"
            else:
                status = "BLOCKED"
                error = "官方根入口存在，但尚未完成可靠的当前校招岗位池枚举"
            return SourceResult(company, "browser_dynamic", src["portal"], status, len(raw_jobs), len(matches), error), matches
        fetcher = self.fetchers.get(mode)
        if not fetcher:
            return SourceResult(company, mode, src["portal"], "NO_FETCHER", 0, 0), []
        try:
            jobs = fetcher(src)
            uniq = self.matcher.target_matches(jobs, src)
            status = "ENUMERATED_WITH_MATCHES" if uniq else "ENUMERATED_ZERO_MATCHES"
            return SourceResult(company, mode, src["portal"], status, len(jobs), len(uniq)), uniq
        except Exception as e:
            # Dedicated adapter failure never means "0 jobs". If browser discovery
            # succeeded from the company's official root / ATS chain, use it as a
            # first-party fallback; otherwise keep the source explicitly BLOCKED.
            dyn = self.dynamic_by_company.get(company) or {}
            raw_jobs = dyn.get("jobs") or []
            browser_terminal = (
                bool(dyn.get("list_scan_complete"))
                and txt(dyn.get("status")) == "BROWSER_ENUMERATED"
            )
            if browser_terminal:
                browser_jobs = to_jobs(company, raw_jobs, src["portal"], "BROWSER:" + src["portal"])
                matches = self.matcher.target_matches(browser_jobs, src)
                return SourceResult(
                    company, "browser_fallback", src["portal"],
                    "ENUMERATED_WITH_MATCHES" if matches else "ENUMERATED_ZERO_MATCHES",
                    len(raw_jobs), len(matches),
                    f"dedicated adapter failed; exhaustive official current-campus browser fallback used: {type(e).__name__}: {e}"[:700],
                ), matches
            discovered = discover_api_candidates(src["portal"])
            diagnostic = f"{type(e).__name__}: {e}"
            if discovered:
                diagnostic += " | discovered: " + " ; ".join(discovered[:8])
            return SourceResult(
                company, mode, src["portal"], "BLOCKED", 0, 0,
                diagnostic[:1600],
            ), []


def collect_sources(cfg):
    collector = Collector(cfg)
    all_matches, results = [], []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(collector.collect, src) for src in cfg["sources"]]
        for future in as_completed(futures):
            result, matches = future.result()
            results.append(result)
            all_matches.extend(matches)
            print(f"collect {result.company}: {result.status}, fetched={result.fetched}, matched={result.matched}, error={result.error}", flush=True)
    results.sort(key=lambda r: r.company)
    all_matches.sort(key=lambda j: (j.company, j.title, j.location, j.job_id))
    return results, all_matches
