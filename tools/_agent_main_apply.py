"""One-time application of the locally reviewed, checksum-locked reader revision."""
from pathlib import Path
import base64
import bz2
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = '37cbfd2b152c6a0aa5bbd8ca0c19820debc632b8'
COMPRESSED_SHA = 'dfead8f9b9437c8434351a78531dfd5f3bd470ec0e4c252e2c2f75224d589469'
JSON_SHA = '251b49b49733a86989586e747df03e4586d636080f74cf343bff2764e1e2eed7'

def sha(data):
    return hashlib.sha256(data).hexdigest()

pieces = []
for i in range(15):
    text = (ROOT / 'tools/_agent_main_bundle' / f'{i:02}.b64').read_text(encoding='ascii').strip()
    if i == 6:
        # Two transfer typos identified by comparing the downloaded staged artifact
        # with the original local bytes. Final whole-payload checks guard repairs.
        for old, new in [
            ('VgIMGKyMrZE0MCbGGIU9bu9bVdq/Dl+Kt4uCqxdmlhhXj8ZhwwT',
             'VgIMGKyMrZE0MCbGGIU9bu9bV9q/Dl+Kt4uCqxdmlhhXj8ZhwwT'),
            ('v828NuMnU1REnY6VcTrqfxr9l9X2WhG2FSBvx4MMejR8GvHmCWT',
             'v828NuMnU1REnY6VcTrqfxr9lX2WhG2FSBvx4MMejR8GvHmCWT'),
        ]:
            assert text.count(old) == 1, 'unexpected transfer bytes'
            text = text.replace(old, new, 1)
    pieces.append(text)
encoded = ''.join(pieces)
assert len(encoded) == 142960, 'payload length mismatch'
compressed = base64.b64decode(encoded, validate=True)
assert sha(compressed) == COMPRESSED_SHA, 'compressed checksum mismatch'
raw = bz2.decompress(compressed)
assert sha(raw) == JSON_SHA, 'document checksum mismatch'
payload = json.loads(raw)
assert payload['baseline'] == BASE
files = payload['files']
assert len(files) == 40 and set(files) == set(payload['expected'])

# Check every original before writing any replacement. Unexpected concurrent edits
# cause failure instead of overwriting work or modifying only half the document set.
for name, expected in payload['expected'].items():
    path = Path(name)
    assert not path.is_absolute() and '..' not in path.parts
    assert name == 'README.md' or name.startswith(('agent-harness/', 'roadmap/', 'research/agent-sources/')) or name in ('research/questions/progress.md', 'tools/validate_agent_readability.py')
    target = ROOT / path
    actual = sha(target.read_bytes()) if target.exists() else None
    assert actual == expected, f'baseline mismatch: {name}'

protected = {}
for folder in ['research/interviews', 'research/questions', 'research/analysis', 'research/monitoring']:
    for path in (ROOT / folder).rglob('*'):
        if path.is_file() and str(path.relative_to(ROOT)) not in files:
            protected[path] = sha(path.read_bytes())

for name, text in files.items():
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

subprocess.run([sys.executable, '-B', str(ROOT / 'tools/validate_agent_readability.py'), '--run-examples'], cwd=ROOT, check=True)
assert all(sha(p.read_bytes()) == digest for p, digest in protected.items()), 'protected research changed'
subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
subprocess.run(['git', 'add', '--', *files.keys()], cwd=ROOT, check=True)
staged = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=ROOT).decode().strip('\0').split('\0')
assert set(staged) == set(files), 'unexpected staged paths'
print(f'Applied exactly {len(files)} reviewed files; protected research checked: {len(protected)}, changed: 0')
print('SHA-256 verified: locally reviewed document bytes equal staged document bytes')
