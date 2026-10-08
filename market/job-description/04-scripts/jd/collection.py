"""Manual, bounded collection of registered sources; no semantic decisions."""
from __future__ import annotations
from dataclasses import asdict
import json
from pathlib import Path
import subprocess
import sys
from .limits import Budget, CollectionStopped, collection_scope
from .paths import CONFIG, SCRIPTS
from .adapters.http import capture_scope
from .adapters.official import FETCHERS


def registry():
    payload = json.loads(CONFIG.read_text(encoding="utf-8"))
    sources = payload["sources"]
    ids = [source["source_id"] for source in sources]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate registered source ID")
    return {source["source_id"]: source for source in sources}


def selected_sources(ids):
    registered = registry()
    if not ids:
        raise ValueError("Select at least one registered --source-id")
    if len(ids) != len(set(ids)):
        raise ValueError("Repeat source IDs are not permitted")
    missing = set(ids) - registered.keys()
    if missing:
        raise ValueError("Unknown registered source ID: " + ", ".join(sorted(missing)))
    return [registered[source_id] for source_id in ids]


def node_adapter(source):
    if source.get("moka_org_id"):
        return "moka"
    return {"portal_only": "browser", "feishu_direct": "feishu", "xiaomi_api": "xiaomi", "bytedance_api": "bytedance"}.get(source["mode"])


def collect_python(source, budget, output, backend=None):
    """Testable worker. Production calls use a subprocess hard wall-time bound."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    budget.job_log = output / "jobs.jsonl"
    result = {"source_id": source["source_id"], "company": source["company"],
              "portal": source["portal"], "model_reviewed": False, "complete": False}
    with collection_scope(budget), capture_scope(output / "raw", backend) as requests:
        try:
            fetcher = FETCHERS.get(source["mode"])
            if fetcher is None:
                raise ValueError(f"No Python transport for {source['mode']}")
            fetcher(source)
            result["status"] = "COLLECTED_UNREVIEWED"
        except CollectionStopped as exc:
            result.update(status="PARTIAL", error=str(exc))
        except Exception as exc:
            result.update(status="PARTIAL" if budget.jobs else "BLOCKED", error=f"{type(exc).__name__}: {exc}")
        if budget.limits_hit or budget.failures:
            result["status"] = "PARTIAL"
        result.update(jobs=[asdict(job) for job in budget.jobs], requests=requests,
                      list_pages=budget.pages, limits_hit=sorted(budget.limits_hit), failures=budget.failures)
    with (output / "result.json").open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return result


def worker(source_id, max_pages, max_jobs, timeout_seconds, output):
    source = selected_sources([source_id])[0]
    return collect_python(source, Budget(max_pages, max_jobs, timeout_seconds), output)


def collect_manual(ids, *, enabled, max_pages, max_jobs, timeout_seconds, output):
    if not enabled:
        raise ValueError("Code collection is disabled; --enable-code-collection is required")
    Budget(max_pages, max_jobs, timeout_seconds)
    sources = selected_sources(ids)
    output = Path(output).resolve()
    # Exclusive run directory: never overwrite a snapshot, prior result or state.
    output.mkdir(parents=True, exist_ok=False)
    all_ok = True
    for source in sources:
        destination = output / source["source_id"]
        adapter = node_adapter(source)
        if adapter:
            destination.mkdir()
            command = ["node", str(SCRIPTS / "jd/adapters" / f"{adapter}.mjs"),
                       "--enable-code-collection", "--source-id", source["source_id"],
                       "--max-pages", str(max_pages), "--max-jobs", str(max_jobs),
                       "--timeout-seconds", str(timeout_seconds), "--output", str(destination / "result.json")]
        else:
            command = [sys.executable, "-B", "-c",
                       "from jd.collection import worker; import json,sys; worker(**json.loads(sys.argv[1]))",
                       json.dumps({"source_id": source["source_id"], "max_pages": max_pages, "max_jobs": max_jobs,
                                   "timeout_seconds": timeout_seconds, "output": str(destination)})]
        try:
            # Node aborts transport at its deadline; allow two seconds only to flush.
            # Python gets an exact subprocess deadline for slow response streams.
            process = subprocess.run(command, cwd=SCRIPTS, timeout=timeout_seconds + (2 if adapter else 0), check=False)
            if process.returncode:
                all_ok = False
            result_file = destination / "result.json"
            if result_file.exists():
                payload = json.loads(result_file.read_text(encoding="utf-8"))
                result = (payload.get("results") or [payload])[0]
                print(f"{source['source_id']}: {result.get('status', 'stored capture')}")
                if result.get("status") in ("PARTIAL", "BLOCKED", "TIMEOUT", "ERROR", "LIMITED", "INCOMPLETE"):
                    all_ok = False
            else:
                raise RuntimeError(f"Collector exited {process.returncode} without a result; see saved raw files")
        except (subprocess.TimeoutExpired, RuntimeError) as exc:
            all_ok = False
            destination.mkdir(parents=True, exist_ok=True)
            failure = {"source_id": source["source_id"], "company": source["company"], "status": "TIMEOUT" if isinstance(exc, subprocess.TimeoutExpired) else "BLOCKED",
                       "complete": False, "model_reviewed": False, "error": str(exc),
                       "preserved_partial_files": [str(path.relative_to(destination)) for path in destination.rglob("*") if path.is_file()]}
            with (destination / "interruption.json").open("x", encoding="utf-8") as stream:
                json.dump(failure, stream, ensure_ascii=False, indent=2)
            print(f"{source['source_id']}: {failure['status']}; partial files preserved")
    return 0 if all_ok else 1
