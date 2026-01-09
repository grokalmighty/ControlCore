import time
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "logs.jsonl"

def rotate_logs() -> Path:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_PATH.exists() or LOG_PATH.stat().st_size == 0:
        LOG_PATH.touch(exist_ok=True)
        return LOG_PATH
    
    ts = time.strftime("%Y%m%d-%H%m%S")
    archived = LOG_PATH.parent / f"logs-{ts}.jsonl"
    LOG_PATH.rename(archived)
    LOG_PATH.touch(exist_ok=True)
    return archived