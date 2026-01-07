import json
import subprocess
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from uuid import uuid4

from .registry import Script

LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "logs.jsonl"

def log_event(event: Dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def run_script(script: Script, timeout_seconds: Optional[float] = 30.0) -> Tuple[bool, str]:
    """
    Run script.entrypoint in a separate Python process.
    Captures stdout/stderr and logs structured results.
    """

    run_id = str(uuid4())
    started = time.time()

    event_base = {
        "run_id": run_id,
        "script_id": script.id,
        "script_name": script.name,
        "started_at": started,
    }

    # Launch: python -c "import module; module.func()"
    module_path, func_name = script.entrypoint.split(":")
    code = f"import {module_path} as m; getattr(m, '{func_name}')()"

    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        ended = time.time()

        ok = proc.returncode == 0
        log_event(
            {
                **event_base,
                "ended_at": ended,
                "ok": ok,
                "exit_Code": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "timeout_seconds": timeout_seconds,
            }
        )
        return ok, run_id
    
    except subprocess.TimeoutExpired as e:
        ended = time.time()
        log_event(
            {
                **event_base,
                "ended_at": ended,
                "ok": False,
                "exit_code": None,
                "stdout": e.stdout if isinstance(e.stdout, str) else "",
                "stderr": e.stderr if isinstance(e.stderr, str) else "",
                "timeout": True,
                "timeout_seconds": timeout_seconds,
            }
        )
        return False, run_id
    
    except Exception:
        ended = time.time()
        tb = traceback.format_exc()
        log_event({**event_base, "ended_at": ended, "ok": False, "error": tb})
        return False, run_id