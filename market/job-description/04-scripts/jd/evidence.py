"""Append-only first-party observations, separate from the latest derived state."""
import hashlib
from pathlib import Path
from .paths import DATA, VERIFIED_INDEX, VERIFIED_INDEX_MD, OUT_JSON, OUT_MD, BROWSER_CACHE, FEISHU_CACHE, MOKA_CACHE

OBSERVATIONS = DATA / "observations"


def preserve_observation(path: Path, destination: Path = OBSERVATIONS) -> Path | None:
    """Keep exact source bytes before a current snapshot can be replaced."""
    if not path.exists():
        return None
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    target = destination / path.stem / (digest + path.suffix)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.read_bytes() != data:
            raise RuntimeError(f"Observation digest collision or corruption: {target}")
    else:
        # Exclusive creation prevents overwriting an immutable observation.
        with target.open("xb") as output:
            output.write(data)
    return target


def preserve_current():
    return [preserve_observation(path) for path in
            (VERIFIED_INDEX, VERIFIED_INDEX_MD, OUT_JSON, OUT_MD, BROWSER_CACHE, FEISHU_CACHE, MOKA_CACHE)]
