"""Single source of truth for business-owned paths, independent of the caller's cwd."""
from pathlib import Path
import os
import tempfile
BUSINESS = Path(__file__).resolve().parents[2]
ROOT = BUSINESS.parents[1]
DATA = BUSINESS / "01-data"
ANALYSIS = BUSINESS / "02-analysis"
STRATEGY = BUSINESS / "03-strategy"
SCRIPTS = BUSINESS / "04-scripts"
LOGS = BUSINESS / "05-logs"
CONFIG = STRATEGY / "official-2027-campus-sources.json"
VERIFIED_INDEX = DATA / "official-company-role-index.json"
MANUAL_ROLE_SEEDS = DATA / "official-first-party-role-seeds.json"
VERIFIED_INDEX_MD = DATA / "official-company-role-index.md"
SCAN_POOL_MD = ANALYSIS / "company-scan-pool.md"
OUT_MD = DATA / "official-2027-agent-jobs.generated.md"
OUT_JSON = DATA / "official-2027-agent-jobs.generated.json"
BROWSER_CACHE = DATA / "official-2027-browser-discovery.generated.json"
FEISHU_CACHE = DATA / "official-2027-feishu-discovery.generated.json"
MOKA_CACHE = DATA / "official-2027-moka-discovery.generated.json"
TEMP_ROOT = Path(os.environ.get("RUNNER_TEMP") or tempfile.gettempdir())
XIAOMI_NODE_CACHE = Path(os.environ.get("XIAOMI_CACHE") or (TEMP_ROOT / "xiaomi-2027-campus.json"))
BYTEDANCE_NODE_CACHE = Path(os.environ.get("BYTEDANCE_CACHE") or (TEMP_ROOT / "bytedance-campus.json"))
