import sys

from .registry import discover_scripts, list_scripts
from .runner import run_script

def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m control_core.cli [list|run <id>]")
        return 2
    
    cmd = argv[0]

    if cmd == "list":
        for s in list_scripts():
            status = "ENABLED" if s.enabled else "disabled"
            print(f"{s.id:10} {status:8} {s.name}")
        return 0
    
    if cmd == "run":
        if len(argv) < 2:
            print("Usage: python -m controle_core.cli run <id>")
            return 2
        script_id = argv[1]
        scripts = discover_scripts()
        if script_id not in scripts:
            print(f"Unknown script id: {script_id}")
            return 1
        
        ok, run_id = run_script(scripts[script_id])
        print(f"run_id={run_id} ok={ok}")
        return 0 if ok else 1
    
    print(f"Unknown command: {cmd}")
    return 2