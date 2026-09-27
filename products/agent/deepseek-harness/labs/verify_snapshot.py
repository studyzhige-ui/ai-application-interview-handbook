#!/usr/bin/env python3
"""Read-only source/environment gate. It does NOT run DeepSeek Harness tests."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

TARGET_SHA = '477b4f420553e8a52c2fbccc464d7561b239c443'
TARGET_VERSION = '0.1.7-rc.2'
CRITICAL_BLOBS = {
    'packages/core/agent-loop/src/agent.ts': 'bcd7ad17a82699c395c3a14855cdee6ed4a2b905',
    'packages/core/agent-loop/src/inbox.ts': 'ef00887a544c2dededb484ff7b9ce0efe83dea21',
    'packages/core/agent-loop/src/tool-calls.ts': 'f1f6256cb1e776e3b300f5cfaac8c6c344c5b03d',
    'packages/core/session/src/repair.ts': 'b87a69c35122cb5aedea5545259604cdbce7971e',
    'packages/core/tools/src/schema.ts': '5aea4f4f7fecb2b3408608e3abd5f97436d7e437',
    'packages/session/session-format-catalog/src/generated.ts': 'eab9d914564be9be6ccd331562bd9d4be97a6bd9',
    'packages/session/session-checkpoint-policy/src/index.ts': '0fc456eb08853b9fe54d0bf9ca3a26c05b4413cf',
    'packages/subagent/subagent/src/child-agent.ts': '0004567a30f5f9e50a91518c071ed87ce72ae671',
}
TEST_ROOTS = (
    'packages/core/agent-loop/', 'packages/core/session/', 'packages/core/tools/',
    'packages/context/session-reference/', 'packages/compaction/compaction-basic/',
    'packages/session/session-persistence-jsonl/', 'packages/subagent/subagent/',
)

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()

def supported_node(text: str) -> bool:
    match = re.fullmatch(r'v?(\d+)\.(\d+)\.(\d+)', text.strip())
    if not match:
        return False
    major, minor, patch = map(int, match.groups())
    return (major == 22 and (minor, patch) >= (19, 0)) or major >= 24

def run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"), capture_output=True, text=True, timeout=25)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f'{args[0]} exited {result.returncode}')
    return result.stdout.strip()

def version(name: str) -> str | None:
    executable = shutil.which(name)
    if not executable:
        return None
    try:
        return run([executable, '--version'])
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        return f'ERROR: {exc}'

def inspect(root: Path) -> dict:
    root = root.resolve(strict=True)
    head = run(['git', 'rev-parse', 'HEAD'], root)
    status = run(['git', 'status', '--porcelain=v1', '--untracked-files=no'], root)
    package = json.loads((root / 'package.json').read_text(encoding='utf-8'))
    node, pnpm = version('node'), version('pnpm')
    blockers: list[str] = []
    if head != TARGET_SHA:
        blockers.append('HEAD differs from the teaching snapshot')
    if status:
        blockers.append('Tracked source has local changes; inspect before interpreting results')
    if package.get('version') != TARGET_VERSION:
        blockers.append('package.json version differs from the teaching snapshot')
    if not node or not supported_node(node):
        blockers.append('Node does not satisfy ^22.19.0 || >=24.0.0')
    manager = package.get('packageManager', '')
    required_pnpm = manager.split('@', 1)[1].split('+', 1)[0] if manager.startswith('pnpm@') else None
    if not required_pnpm or pnpm != required_pnpm:
        blockers.append(f'pnpm must match packageManager ({manager})')
    blobs: dict[str, dict] = {}
    for relative, expected in CRITICAL_BLOBS.items():
        path = root / relative
        actual = git_blob(path.read_bytes()) if path.is_file() else None
        blobs[relative] = {'expected': expected, 'actual': actual, 'match': actual == expected}
        if actual != expected:
            blockers.append(f'Source bytes differ or are missing: {relative}')
    tracked = run(['git', 'ls-files', '-z'], root).split('\0')
    tests = sorted(p for p in tracked if p.startswith(TEST_ROOTS) and p.endswith(('.test.ts', '.spec.ts')))
    return {
        'kind': 'source-and-environment-gate-only', 'checkout': str(root),
        'head': head, 'target_sha': TARGET_SHA, 'version': package.get('version'),
        'node': node, 'pnpm': pnpm, 'package_manager': manager,
        'critical_source_blobs': blobs, 'discovered_test_files': tests,
        'blockers': blockers, 'ready_for_test_setup': not blockers,
        'product_tests_executed': False, 'real_service_executed': False,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path, help='Existing upstream checkout; never fetched or changed')
    args = parser.parse_args()
    try:
        report = inspect(args.checkout)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'error': str(exc), 'product_tests_executed': False}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['ready_for_test_setup'] else 2

if __name__ == '__main__':
    sys.exit(main())
