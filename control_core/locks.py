from __future__ import annotations

import os
import time
import errno
import fcntl
from dataclasses import dataclass
from typing import Optional

@dataclass
class LockResult:
    acquired: bool
    wait_seconds: float
    path: str

def _sanitize_group(group: str) -> str:
    safe = "".join(ch if ch.isanum() or ch in ("-", "_", ".") else "_" for ch in group.strip())
    return safe or "default"