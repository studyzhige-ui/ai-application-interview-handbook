"""Filesystem paths only. Importing this module performs no collection or writes."""
from pathlib import Path
BUSINESS = Path(__file__).resolve().parents[2]
SCRIPTS = BUSINESS / "04-scripts"
CONFIG = BUSINESS / "03-strategy/official-2027-campus-sources.json"
