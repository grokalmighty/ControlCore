from pathlib import Path

def main(payload=None):
    payload = payload or {}
    failed = payload.get("failed_event", {})
    sid = failed.get("script_id", "?")
    run_id = failed.get("run_id", "?")
    stderr = failed.get("stderr", "")
    stdout = failed.get("stdout", "")
    error = failed.get("error", "")

    print("ALERT: Script failure")
    print(f"script_id: {sid}")
    print(f"run_id: {run_id}")

    if error:
        print("\nTraceback/error:")
        print(error.strip())

    if stderr:
        print("\nstderr:")
        print(stderr.strip())

    if stdout:
        print("\nstdout:")
        print(stdout.strip())    