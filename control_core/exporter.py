import csv
import json
from pathlib import Path
from typing import Iterable, Optional

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

def export_csv(output_path: str, max_rows: Optional[int] = None) -> Path:
    out = Path(output_path).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    rows_written = 0

    fieldnames = [
        "run_id",
        "script_id",
        "script_name",
        "ok",
        "exit_code",
        "started_at",
        "ended_at",
        "duration_ms",
        "timeout",
        "timeout_seconds",
        "stdout",
        "stderr",
        "error",
        "extra_json"
    ]

    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()

        for e in _iter_events():
            started = e.get("started_at")
            ended = e.get("ended_at")
            duration_ms = ""
            if isinstance(started, (int, float)) and isinstance(ended, (int, float)) and ended >= started:
                duration_ms = (ended - started) * 1000.0

            base = {
                "run_id": e.get("run_id", ""),
                "script_id": e.get("script_id", ""),
                "script_name": e.get("script_name", ""),
                "ok": e.get("ok", ""),
                "exit_code": e.get("exit_code", ""),
                "started_at": started if started is not None else "",
                "ended_at": ended if ended is not None else "",
                "duration_ms": duration_ms,
                "timeout": e.get("timeout", ""),
                "timeout_seconds": e.get("timeout_seconds", ""),
                "stdout": e.get("stdout", ""),
                "stderr": e.get("stderr", ""),
                "error": e.get("error", ""),
            }

            extras = {k: v for k, v in e.items() if k not in base and k not in ("duration_ms",)}
            base["extra_json"] = json.dumps(extras, ensure_ascii=False)

            w.writerow(base)
            rows_written += 1
            if max_rows is not None and rows_written >= max_rows:
                break
        
    return out
