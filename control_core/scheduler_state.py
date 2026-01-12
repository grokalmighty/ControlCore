import json
from pathlib import Path
from typing import Dict, Any

STATE_PATH = Path(__file__).resolve().parent.parent / "data" / "scheduler_state.json"

def load_state() -> Dict[str, Any]:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}