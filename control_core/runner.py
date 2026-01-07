import importlib
import json
import time
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Tuple
from uuid import uuid4

from .registry import Script

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "logs.jsonl"

def _load_uncallable(entrypoint: str):
    module_path, func_name = entrypoint.split(":")
    module = importlib.import_module(module_path)
    fn = getattr(module, func_name)
    return fn

def log_event(event: Dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def run_script(script: Script) -> Tuple[bool, str]:
    run_id = str(uuid4())
    started = time.time()

    event_base = {
        "run_id": run_id,
        "script_id": script.id,
        "script_name": script.name,
        "started_at": started,
    }

    try:
        fn = _load_uncallable(script.entrypoint)
        result = fn()
        ended = time.time()

        log_event(
            {
                **event_base,
                "ended_at": ended,
                "ok": True,
                "result": repr(result),
            }
        )
        return True, run_id
    
    except Exception:
        ended = time.time()
        tb =traceback.format_exc()

        log_event(
            {
                **event_base,
                "ended_at": ended,
                "ok": False,
                "error": tb,
            }
        )
        return False, run_id