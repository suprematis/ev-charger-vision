"""Environment and Path Resolver for Local Execution."""
import os
import sys
from pathlib import Path

def get_repo_root() -> Path:
    current = Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists() or (parent / "configs").exists() or (parent / "src").exists():
            return parent
    return current

REPO_ROOT = get_repo_root()

# Ensure src/ is importable
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Standard paths
CONFIGS_DIR = REPO_ROOT / "configs"
DATA_RAW_DIR = Path(os.getenv("EV_RAW_DATA_DIR", REPO_ROOT / "data" / "raw_screenshots"))
DATA_PROCESSED_DIR = Path(os.getenv("EV_PROCESSED_DIR", REPO_ROOT / "data" / "processed"))
DATA_MODELS_DIR = Path(os.getenv("EV_MODELS_DIR", REPO_ROOT / "data" / "models"))

# Hierarchy: local uncommitted override > default tracked config
LOCAL_CFG = CONFIGS_DIR / "spots_calibrated.local.json"
DEFAULT_CFG = CONFIGS_DIR / "spots_calibrated.json"
CONFIG_SPOTS_FILE = LOCAL_CFG if LOCAL_CFG.exists() else DEFAULT_CFG

for d in [DATA_PROCESSED_DIR, DATA_MODELS_DIR, CONFIGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)