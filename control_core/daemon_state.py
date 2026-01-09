import os 
from pathlib import Path
from typing import Optional

PID_PATH = Path(__file__).resolve().parent.parent / "data" / "daemon.pid"

def write_pid() -> None:
    PID_PATH.parent.mkdir(parents=True, exist_ok=True)
    PID_PATH.write_text(str(os.getpid()), encoding="utf-8")
