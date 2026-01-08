from pathlib import Path

def main():
    log = Path("data/logs.jsonl")
    if not log.exists():
        print("ALERT: no logs yet")
        return
    last = log.read_text(encoding="utf-8").strip().splitlines()[-1]
    print(f"ALERT: last event -> {last}")