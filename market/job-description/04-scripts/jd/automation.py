"""GitHub-native JD scan orchestration.

Network collection and semantic role review are deliberately separate. This module
runs the registered transports, keeps an incremental identity/fingerprint baseline,
and writes a cumulative review queue. It never promotes a job into the reviewed
catalog and never interprets a failed scan as proof that a job disappeared.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .collection import collect_manual, registry

SCHEMA_VERSION = 2
TRACKING_QUERY_KEYS = {
    "from", "fromjob", "source", "sourcessr", "spread", "channelput",
    "employchannelcode", "anchorname",
}
AI_PATTERNS = (
    ("agent", r"agents?|智能体|agentic|multi[- ]?agent|tool[- ]?calling|function[- ]?call|mcp"),
    ("llm", r"\bllm\b|大模型|语言模型|生成式\s*ai|generative\s+ai|aigc|copilot"),
    ("rag", r"\brag\b|检索增强|向量检索|知识库|knowledge\s+base"),
    ("evaluation", r"评测|测评|benchmark|eval(?:uation)?|harness|回归测试|测试工具"),
    ("memory_context", r"上下文|context\s+engineering|记忆|memory|prompt\s+engineering"),
)
ENGINEERING_PATTERN = re.compile(
    r"开发|研发|工程|架构|后端|前端|全栈|平台|系统|服务|接口|api\b|sdk\b|"
    r"部署|运维|可观测|并发|数据库|python\b|java\b|go\b|golang\b|typescript\b|"
    r"javascript\b|编码|编程|代码|implementation|developer|engineer|backend|frontend|full[- ]?stack",
    re.I,
)
COMPILED_AI = tuple((name, re.compile(pattern, re.I)) for name, pattern in AI_PATTERNS)


def now_utc() -> str:
    fixed = os.environ.get("JD_AUTOMATION_NOW")
    if fixed:
        return fixed
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def dump_json(path: Path, payload) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path, default):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_url(value: str) -> str:
    value = str(value or "").strip()
    if not value:
        return ""
    try:
        parsed = urlsplit(value)
    except ValueError:
        return value
    query = []
    for key, val in parse_qsl(parsed.query, keep_blank_values=True):
        lowered = key.lower()
        if lowered.startswith("utm_") or lowered in TRACKING_QUERY_KEYS:
            continue
        query.append((key, val))
    query.sort()
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path, urlencode(query), parsed.fragment))


def job_identity(source_id: str, job: dict) -> str:
    job_id = str(job.get("job_id") or job.get("req_id") or "").strip()
    url = canonical_url(job.get("official_url") or "")
    if source_id == "official-002" and job_id:
        parsed = urlsplit(url)
        fragment_path = parsed.fragment.split("?", 1)[0].strip("/")
        if parsed.hostname == "campus.kuaishou.cn" and fragment_path == f"campus/job-info/{job_id}":
            return f"campus:{job_id}"
        if parsed.hostname == "zhaopin.kuaishou.cn" and fragment_path == f"official/trainee/job-info/{job_id}":
            return f"trainee:{job_id}"
        return f"kuaishou:{job_id}:{hashlib.sha256(url.encode()).hexdigest()[:12]}"
    if job_id:
        return f"id:{job_id}"
    if url:
        return "url:" + hashlib.sha256(url.encode()).hexdigest()[:24]
    raw = "\x1f".join(str(job.get(key) or "") for key in ("title", "location", "department", "description"))
    return "anon:" + hashlib.sha256(raw.encode()).hexdigest()[:24]


def _normalized_text(value) -> str:
    if isinstance(value, (list, tuple)):
        value = " | ".join(str(item) for item in value)
    elif isinstance(value, dict):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return re.sub(r"\s+", " ", str(value or "")).strip()


def job_fingerprint(job: dict) -> str:
    fields = {
        "title": _normalized_text(job.get("title")),
        "location": _normalized_text(job.get("location") or job.get("locations")),
        "category": _normalized_text(job.get("category")),
        "department": _normalized_text(job.get("department")),
        "description": _normalized_text(job.get("description")),
        "requirements": _normalized_text(job.get("requirements")),
        "official_url": canonical_url(job.get("official_url") or ""),
        "cycle_evidence": _normalized_text(job.get("cycle_evidence")),
    }
    raw = json.dumps(fields, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def compact_job(job: dict) -> dict:
    keys = (
        "job_id", "req_id", "title", "location", "locations", "category", "department",
        "description", "requirements", "official_url", "official_api", "cycle_evidence",
        "detail_status", "detail_error",
    )
    return {key: job.get(key) for key in keys if key in job and job.get(key) not in (None, "")}


def triage(job: dict) -> dict:
    text = "\n".join(_normalized_text(job.get(key)) for key in ("title", "description", "requirements", "category", "department"))
    signals = [name for name, pattern in COMPILED_AI if pattern.search(text)]
    engineering = bool(ENGINEERING_PATTERN.search(text))
    score = len(signals) * 2 + (2 if engineering else 0)
    if "agent" in signals:
        score += 2
    if "evaluation" in signals:
        score += 1
    priority = "high" if score >= 6 else "medium" if score >= 3 else "low"
    return {"priority": priority, "score": score, "signals": signals, "engineering_signal": engineering}


def shard_source_ids(shard_index: int, shard_count: int) -> list[str]:
    if shard_count <= 0 or shard_index < 0 or shard_index >= shard_count:
        raise ValueError("shard-index must be within [0, shard-count)")
    ids = sorted(registry())
    return [source_id for offset, source_id in enumerate(ids) if offset % shard_count == shard_index]


def scan_shard(*, shard_index: int, shard_count: int, max_pages: int, max_jobs: int,
               timeout_seconds: float, output: Path) -> int:
    """Collect one deterministic source shard. Source failures are data, not job failure."""
    output = Path(output).resolve()
    source_ids = shard_source_ids(shard_index, shard_count)
    if output.exists():
        raise ValueError(f"Output directory already exists: {output}")
    code = collect_manual(
        source_ids,
        enabled=True,
        max_pages=max_pages,
        max_jobs=max_jobs,
        timeout_seconds=timeout_seconds,
        output=output,
    )
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "checked_at_utc": now_utc(),
        "source_sha": os.environ.get("GITHUB_SHA", ""),
        "shard_index": shard_index,
        "shard_count": shard_count,
        "source_ids": source_ids,
        "collector_exit_code": code,
    }
    dump_json(output / "scan-manifest.json", manifest)
    # A partial/blocked source must not prevent the other shards from being reconciled.
    return 0


def _result_rank(result: dict) -> tuple[int, int]:
    complete = 1 if result.get("complete") is True else 0
    return complete, len(result.get("jobs") or [])


def load_scan_results(root: Path) -> dict[str, dict]:
    root = Path(root)
    results: dict[str, dict] = {}
    for path in sorted(root.rglob("result.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        candidates = payload.get("results") if isinstance(payload, dict) else None
        if not isinstance(candidates, list):
            candidates = [payload]
        for result in candidates:
            if not isinstance(result, dict) or not result.get("source_id"):
                continue
            result = dict(result)
            result["artifact_path"] = str(path.relative_to(root))
            previous = results.get(result["source_id"])
            if previous is None or _result_rank(result) > _result_rank(previous):
                results[result["source_id"]] = result
    for path in sorted(root.rglob("interruption.json")):
        try:
            result = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        source_id = result.get("source_id")
        if source_id and source_id not in results:
            result = dict(result)
            result["artifact_path"] = str(path.relative_to(root))
            results[source_id] = result
    return results


def _source_snapshot(source_id: str, result: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    jobs: dict[str, dict] = {}
    raw_by_identity: dict[str, dict] = {}
    for raw in result.get("jobs") or []:
        if not isinstance(raw, dict):
            continue
        identity = job_identity(source_id, raw)
        candidate = {
            "fingerprint": job_fingerprint(raw),
            "title": str(raw.get("title") or ""),
            "official_url": canonical_url(raw.get("official_url") or ""),
        }
        existing = jobs.get(identity)
        if existing and existing["fingerprint"] != candidate["fingerprint"]:
            # Preserve deterministic distinction instead of silently overwriting a collision.
            identity = identity + ":" + candidate["fingerprint"][:12]
        jobs[identity] = candidate
        raw_by_identity[identity] = raw
    return jobs, raw_by_identity


def _event_key(source_id: str, identity: str, change: str, fingerprint: str) -> str:
    raw = f"{source_id}\x1f{identity}\x1f{change}\x1f{fingerprint}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def _queue_event(queue: dict, *, checked_at: str, source_id: str, company: str,
                 identity: str, change: str, job: dict | None, previous: dict | None) -> bool:
    fingerprint = job_fingerprint(job) if job else str((previous or {}).get("fingerprint") or "removed")
    key = _event_key(source_id, identity, change, fingerprint)
    entries = queue.setdefault("entries", {})
    if key in entries:
        entries[key]["last_seen_at_utc"] = checked_at
        return False
    review = triage(job or previous or {}) if job else {"priority": "low", "score": 0, "signals": [], "engineering_signal": False}
    entries[key] = {
        "event_id": key,
        "source_id": source_id,
        "company": company,
        "identity": identity,
        "change": change,
        "first_seen_at_utc": checked_at,
        "last_seen_at_utc": checked_at,
        "review_state": "pending",
        "triage": review,
        "job": compact_job(job or {}) if job else None,
        "previous": previous,
    }
    return True


def reconcile(*, input_dir: Path, state_file: Path, queue_file: Path, report_file: Path) -> dict:
    checked_at = now_utc()
    registered = registry()
    results = load_scan_results(input_dir)
    state = load_json(state_file, {"schema_version": SCHEMA_VERSION, "sources": {}})
    queue = load_json(queue_file, {"schema_version": SCHEMA_VERSION, "entries": {}})
    if state.get("schema_version") != SCHEMA_VERSION or queue.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported JD automation state schema")

    run_counts = Counter()
    source_rows = []
    for source_id, source in registered.items():
        company = source["company"]
        result = results.get(source_id)
        previous_state = state["sources"].get(source_id, {})
        previous_jobs = dict(previous_state.get("jobs") or {})
        if result is None:
            run_counts["missing"] += 1
            source_rows.append((source_id, company, "MISSING_ARTIFACT", 0, len(previous_jobs), 0, "未取得该来源的扫描产物；旧基线保留"))
            continue

        current_jobs, raw_by_identity = _source_snapshot(source_id, result)
        status = str(result.get("status") or "UNKNOWN")
        complete = result.get("complete") is True
        has_observation = bool(current_jobs) or status in {"OK", "COLLECTED_UNREVIEWED", "PARTIAL", "LIMITED", "INCOMPLETE"}
        baseline_ready = bool(previous_state.get("baseline_ready"))
        new_events = 0

        if not baseline_ready:
            # Bootstrap observed identities without reporting the repository's pre-existing pool as new work.
            merged = dict(previous_jobs)
            merged.update(current_jobs)
            state["sources"][source_id] = {
                "company": company,
                "baseline_ready": has_observation,
                "baseline_kind": "complete" if complete else "observed",
                "jobs": current_jobs if complete else merged,
                "last_attempt_at_utc": checked_at,
                "last_status": status,
                "last_complete_at_utc": checked_at if complete else previous_state.get("last_complete_at_utc"),
            }
            if has_observation:
                run_counts["bootstrapped"] += 1
                note = "首次基线建立，不产生历史岗位新增事件"
            else:
                run_counts["waiting_baseline"] += 1
                note = "本次未取得可用岗位观察；等待后续成功扫描建立基线"
        else:
            for identity, current in current_jobs.items():
                old = previous_jobs.get(identity)
                raw = raw_by_identity.get(identity)
                if old is None:
                    if _queue_event(queue, checked_at=checked_at, source_id=source_id, company=company,
                                    identity=identity, change="added", job=raw, previous=None):
                        new_events += 1
                        run_counts["added"] += 1
                elif old.get("fingerprint") != current.get("fingerprint"):
                    if _queue_event(queue, checked_at=checked_at, source_id=source_id, company=company,
                                    identity=identity, change="changed", job=raw, previous=old):
                        new_events += 1
                        run_counts["changed"] += 1
            if complete:
                for identity in sorted(set(previous_jobs) - set(current_jobs)):
                    old = previous_jobs[identity]
                    if _queue_event(queue, checked_at=checked_at, source_id=source_id, company=company,
                                    identity=identity, change="possibly_removed", job=None, previous=old):
                        new_events += 1
                        run_counts["possibly_removed"] += 1
                next_jobs = current_jobs
            else:
                next_jobs = dict(previous_jobs)
                next_jobs.update(current_jobs)
            state["sources"][source_id] = {
                "company": company,
                "baseline_ready": True,
                "baseline_kind": "complete" if complete else previous_state.get("baseline_kind", "observed"),
                "jobs": next_jobs,
                "last_attempt_at_utc": checked_at,
                "last_status": status,
                "last_complete_at_utc": checked_at if complete else previous_state.get("last_complete_at_utc"),
            }
            note = "完整扫描，可判断消失" if complete else "非完整扫描；仅合并已观察新增/变化，不判断消失"

        if status in {"BLOCKED", "TIMEOUT", "ERROR"}:
            run_counts["blocked"] += 1
        elif complete:
            run_counts["complete"] += 1
        else:
            run_counts["partial"] += 1
        source_rows.append((source_id, company, status, len(current_jobs), len(state["sources"][source_id]["jobs"]), new_events, note))

    state["last_run"] = {
        "checked_at_utc": checked_at,
        "source_sha": os.environ.get("GITHUB_SHA", ""),
        "registered_sources": len(registered),
        "received_results": len(results),
    }
    queue["updated_at_utc"] = checked_at
    queue["policy"] = (
        "Every detected source change is preserved for review. triage only orders work; it never decides inclusion. "
        "The reviewed official catalog is not modified by automation."
    )
    dump_json(state_file, state)
    dump_json(queue_file, queue)

    pending = [entry for entry in queue["entries"].values() if entry.get("review_state") == "pending"]
    priorities = Counter((entry.get("triage") or {}).get("priority", "low") for entry in pending)
    report = [
        "# JD 自动采集状态", "",
        f"最近扫描：{checked_at}。登记入口 **{len(registered)}** 个，本次收到 **{len(results)}** 个来源结果。",
        "",
        "自动化只负责官方来源采集、身份/正文指纹比较和待审队列；不会凭关键词把岗位写入正式 JD 库，也不会因一次失败自动删除正式岗位。",
        "",
        f"本次新事件：新增 **{run_counts['added']}**、正文/字段变化 **{run_counts['changed']}**、完整扫描中可能消失 **{run_counts['possibly_removed']}**。",
        f"累计待审：**{len(pending)}**（高优先 {priorities['high']} / 中优先 {priorities['medium']} / 低优先 {priorities['low']}）。",
        "",
        "| 来源 | 公司 | 状态 | 本次观察 | 基线身份 | 新事件 | 处理 |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]
    for source_id, company, status, observed, baseline, events, note in source_rows:
        report.append(f"| {source_id} | {company.replace('|','／')} | {status} | {observed} | {baseline} | {events} | {note} |")
    report += [
        "",
        "待审原始内容见 ../01-data/automation/review-queue.json；扫描基线见 ../01-data/automation/scan-state.json。",
        "首次为某来源建立基线时不会把已有职位批量标记成新增。只有后续身份新增、指纹变化，或一次被确认完整的扫描中身份消失，才生成事件。",
    ]
    report_file = Path(report_file)
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text("\n".join(report).rstrip() + "\n", encoding="utf-8")
    return {"counts": dict(run_counts), "pending": len(pending), "results": len(results)}
