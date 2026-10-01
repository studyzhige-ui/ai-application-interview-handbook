"""Read marked, visible numeric tables without executing Markdown content."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

MODULE = Path(__file__).resolve().parents[1]


def numeric_table(name: str, module: Path = MODULE) -> list[list[str]]:
    """Return the one table immediately following a named marker.

    Scope: the simple pipe tables in this course, without embedded pipe symbols.
    A duplicate or missing marker is an error, not a silently skipped example.
    """
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError(f"invalid numeric example name: {name!r}")
    marker = f"<!-- numeric-example: {name} -->"
    matches: list[list[list[str]]] = []
    for path in sorted((module / "docs").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for found in re.finditer(re.escape(marker), text):
            rest = text[found.end():]
            rest = re.sub(r"^\s*(?:<!--.*?-->\s*)*", "", rest, flags=re.S)
            lines = []
            for line in rest.splitlines():
                if not line.strip().startswith("|"):
                    break
                lines.append(line.strip())
            if len(lines) < 3:
                raise ValueError(f"{path}: {name} must precede a nonempty table")
            cells = [[c.strip().replace('`', '') for c in line.strip('|').split('|')]
                     for line in lines]
            if any(len(row) != len(cells[0]) for row in cells):
                raise ValueError(f"{path}: inconsistent table width for {name}")
            if not all(re.fullmatch(r":?-+:?", c) for c in cells[1]):
                raise ValueError(f"{path}: invalid table separator for {name}")
            matches.append([cells[0], *cells[2:]])
    if len(matches) != 1:
        raise ValueError(f"expected one {name!r} table, found {len(matches)}")
    return matches[0]


def table_fingerprint(table: list[list[str]]) -> str:
    canonical = json.dumps(table, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
