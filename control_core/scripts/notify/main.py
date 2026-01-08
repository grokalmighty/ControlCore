import subprocess

def _extract_error_line(failed: dict) -> str:
    text = (failed.get("error") or failed.get("stderr") or "").strip()
    if not text:
        return ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[-1] if lines else ""

def main(payload=None):
    payload = payload or {}
    failed = payload.get("failed_event", {})
    sid = failed.get("script_id", "unknown")
    run_id = failed.get("run_id", "unknown")
    err_line = _extract_error_line(failed)

    title = "Control Core: Script failed"
    message = f"{sid} (run_id={run_id})"
    if err_line:
        message = f"{message}\n{err_line}"

    # Notification center
    script = f'display notification "{message} with title "{title}"'
    subprocess.run(["osascript", "-e", script], check=False)
    print(f"Notified: {sid} {run_id} {err_line}")