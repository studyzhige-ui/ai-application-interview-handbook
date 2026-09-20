#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keep build_market_analysis.py expected canonical count aligned with reviewed audit."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "tools/phase2b_canonical_audit.json"
TARGET = ROOT / "tools/build_market_analysis.py"


def main() -> int:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    text = TARGET.read_text(encoding="utf-8")
    text, n = re.subn(
        r"^EXPECTED_QUESTIONS = \d+$",
        f"EXPECTED_QUESTIONS = {int(audit['expected_active_after'])}",
        text,
        count=1,
        flags=re.M,
    )
    if n != 1:
        raise SystemExit("could not sync EXPECTED_QUESTIONS")
    TARGET.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
