import os
from pathlib import Path


SERVER_ROOT = Path(
    os.environ["SERVER_ROOT"]
).resolve()

APPS_DIR = SERVER_ROOT / "apps"
DATA_DIR = SERVER_ROOT / "data"
CONFIG_DIR = SERVER_ROOT / "config"
LOG_DIR = SERVER_ROOT / "logs"


def app_paths(name: str) -> dict[str, Path]:
    return {
        "code": APPS_DIR / name,
        "data": DATA_DIR / name,
        "config": CONFIG_DIR / name,
    }