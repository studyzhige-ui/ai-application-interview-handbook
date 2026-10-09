"""Optional byte-exact preservation into a new content-addressed observation."""
import hashlib
from pathlib import Path


def preserve_observation(path: Path, destination: Path) -> Path:
    data = path.read_bytes()
    target = destination / path.stem / (hashlib.sha256(data).hexdigest() + path.suffix)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.read_bytes() != data:
            raise RuntimeError(f"Observation hash mismatch: {target}")
    else:
        with target.open("xb") as stream:
            stream.write(data)
    return target
