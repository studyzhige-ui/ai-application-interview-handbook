"""Cross-platform generated-output publication with input-change and push-race gates.

This command is intended only for the existing authorized Actions schedule. It
never force-pushes. A new relevant input or output invalidates the in-flight run.
"""
from __future__ import annotations
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from .paths import ROOT, BUSINESS

PREFIX = BUSINESS.relative_to(ROOT).as_posix()
INPUT_PATHS = [PREFIX, ".github/workflows/sync-official-2027-agent-jobs.yml"]
OUTPUT_PATHS = [
    f"{PREFIX}/01-data/official-2027-agent-jobs.generated.json",
    f"{PREFIX}/01-data/official-2027-agent-jobs.generated.md",
    f"{PREFIX}/01-data/official-2027-browser-discovery.generated.json",
    f"{PREFIX}/01-data/official-2027-feishu-discovery.generated.json",
    f"{PREFIX}/01-data/official-2027-moka-discovery.generated.json",
    f"{PREFIX}/01-data/official-company-role-index.json",
    f"{PREFIX}/01-data/official-company-role-index.md",
    f"{PREFIX}/01-data/observations",
    f"{PREFIX}/02-analysis/company-scan-pool.md",
    f"{PREFIX}/02-analysis/official-2027-coverage-audit.generated.md",
    f"{PREFIX}/02-analysis/ai-agent-jd-market.md",
]


def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, text=True, encoding="utf-8",
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def relevant_inputs_changed(base, head):
    return bool(git("diff", "--name-only", f"{base}..{head}", "--", *INPUT_PATHS).stdout.strip())


def main():
    if os.environ.get("GITHUB_ACTIONS") != "true" or os.environ.get("GITHUB_REF") != "refs/heads/main":
        raise RuntimeError("Publication is allowed only in the authorized main-branch GitHub Actions run")
    source_sha = os.environ.get("SYNC_SOURCE_SHA", "").strip()
    if not source_sha:
        raise RuntimeError("SYNC_SOURCE_SHA is required for stale-output protection")
    if git("rev-parse", "HEAD").stdout.strip() != source_sha:
        raise RuntimeError("Checkout does not match collection source SHA")
    with tempfile.TemporaryDirectory(prefix="job-sync-", dir=os.environ.get("RUNNER_TEMP")) as tmp:
        stash = Path(tmp)
        existing = [p for p in OUTPUT_PATHS if (ROOT / p).exists()]
        for relative in existing:
            src, target = ROOT / relative, stash / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, target)
            else:
                shutil.copy2(src, target)
        git("fetch", "origin", "main")
        remote_sha = git("rev-parse", "origin/main").stdout.strip()
        if remote_sha != source_sha and relevant_inputs_changed(source_sha, remote_sha):
            print("Collection inputs changed; discard stale discovery output.")
            return 0
        git("reset", "--hard", "origin/main")
        for relative in existing:
            src, target = stash / relative, ROOT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if src.is_dir():
                shutil.copytree(src, target, dirs_exist_ok=True)
            else:
                shutil.copy2(src, target)
        if not git("status", "--porcelain", "--", *existing).stdout.strip():
            print("No discovery changes.")
            return 0
        git("config", "user.name", "github-actions[bot]")
        git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
        git("add", "--", *existing)
        git("commit", "-m", "market: sync official current-campus Agent discovery [skip ci]")
        for attempt in range(1, 4):
            git("fetch", "origin", "main")
            latest = git("rev-parse", "origin/main").stdout.strip()
            parent = git("rev-parse", "HEAD^").stdout.strip()
            if latest != parent:
                if relevant_inputs_changed(source_sha, latest):
                    print("Collection inputs changed during publication; discard stale discovery commit.")
                    return 0
                git("rebase", "origin/main")
            if git("push", "origin", "HEAD:main", check=False).returncode == 0:
                return 0
            print(f"Push raced with another commit; retry publication ({attempt}/3).")
        return 1
