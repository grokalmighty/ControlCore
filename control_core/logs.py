import json 
import time
from pathlib import Path
from typing import Dict, Iterator, Optional

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "logs.jsonl"

def _iter_log_lines() -> Iterator[dict]:
    if not LOG_PATH.exists():
        return
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue