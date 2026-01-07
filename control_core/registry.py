import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"

@dataclass(frozen=True)
class Script:
    id: str
    name: str
    enabled: bool
    entrypoint: str
    schedule: dict
    path: Path