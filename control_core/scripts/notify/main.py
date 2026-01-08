import subprocess

def main(payload=None):
    payload = payload or {}
    failed = payload.get("failed_event", {})
    sid = failed.get("script_id", "unknown")
    run_id = failed.get("run_id", "unknown")

    title = "Control Core: Script failed"
    message = f"{sid} (run_id={run_id})"

    # Notification center
    script = f'display notification "{message} with title "{title}"'
    subprocess.run(["osascript", "-e", script], check=False)
    print(f"Notified: {message}")