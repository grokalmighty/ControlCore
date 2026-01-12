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

def list_process_names() -> Set[str]:
    try:
        out = subprocess.check_output(["ps", "-axo", "comm="], text=True)
        names: Set[str] = set()
        for line in out.splitlines():
            name = line.strip()
            if not name:
                continue
            
            name = name.split("/")[-1]
            names.add(name)
        return names
    except Exception:
        return set()