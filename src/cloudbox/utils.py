import os
from pathlib import Path

def app_paths(name: str) -> dict[str, Path]:
        
    SERVER_ROOT = Path(
        os.environ["SERVER_ROOT"]
    ).resolve()

    APPS_DIR = SERVER_ROOT / "apps"
    DATA_DIR = SERVER_ROOT / "data"
    LOG_DIR = SERVER_ROOT / "logs"

    return {
        "code": APPS_DIR / name,
        "data": DATA_DIR / name,
        "log": LOG_DIR / name,
    }