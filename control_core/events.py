from __future__ import annotations
import subprocess
import time
import socket
from typing import Optional, Set, Dict, Any, List

def get_idle_seconds_macos() -> Optional[float]:
    """
    Returns idle seconds, or None if unsupported
    """
    try:
        out = subprocess.check_output(
            ["ioreg", "-c", "IOHIDSystem"],
            text=True,
            stderr=subprocess.DEVNULL,
        )

        for line in out.splitlines():
            if "HIDIdleTime" in line:
                parts = line.strip().split()
                for token in reversed(parts):
                    if token.isdigit():
                        ns = int(token)
                        return ns / 1e9
        return None
    except Exception:
        return None
