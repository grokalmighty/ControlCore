import json
import time
from collections import deque
from pathlib import Path
from typing import List, Optional

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "logs.jsonl"

def _safe_load(line: str) -> Optional[dict]:
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None
    