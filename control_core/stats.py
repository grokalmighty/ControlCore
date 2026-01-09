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

def compute_stats(last_n: int=200) -> Dict[str, dict]:
    """
    Compute per-script stats over the last_n events (global), not last_n per script.
    """

    recent = deque(maxlen=last_n)
    for e in _iter_events():
        recent.append(e)
    
    per = defaultdict(lambda: {
        "runs": 0,
        "fails": 0,
        "avg_ms": 0.0,
        "last_ok": None,
        "last_run_id": None,
        "last_time": None,
    })

    # Simple running example
    for e in recent:
        sid = e.get("script_id")
        if not sid:
            continue

        d = per[sid]
        d["runs"] += 1
        ok = bool(e.get("ok"))
        if not ok:
            d["fails"] += 1

        started = e.get("started_at")
        ended = e.get("ended_at")
        if isinstance(started, (int, float)) and isinstance(ended, (int, float)) and ended >= started:
            ms = (ended - started) * 1000.0
            n = d["runs"]
            d["avg_ms"] = d["avg_ms"] + (ms - d["avg_ms"]) / n
        
        d["last_ok"] = ok
        d["last_run_id"] = e.get("run_id")
        d["last_time"] = ended if ended is not None else e.get("started_at")
    
    return dict(per)