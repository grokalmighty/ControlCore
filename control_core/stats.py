import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "logs.jsonl"

def _iter_events() -> Iterable[dict]:
    if not LOG_PATH.exists():
        return []
    
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue