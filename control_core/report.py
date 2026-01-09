import json
import time
from collections import defaultdict, deque
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

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

def _duration_ms(e: dict) -> float | None:
    s = e.get("started_at")
    en = e.get("ended_at")

    if isinstance(s, (int, float)) and isinstance(en, (int, float)) and en >= s:
        return (en - s) * 1000.0
    return None
