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
