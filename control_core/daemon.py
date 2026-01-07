import yaml
import subprocess
import datetime
import json
from pathlib import Path

def load_policies():
    with open("policies.yaml", "r") as f:
        return yaml.safe_load(f)["policies"]
    
def time_matches(policy_time):
    now = datetime.datetime.now().strftime("%H:%M")
    return now == policy_time

def run_script(script_id):
    script_dir = Path("scripts") / script_id
    manifest_path = script_dir / "manifest.yaml"

    if not manifest_path.exists():
        raise Exception("Missing manifest")
    
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)
    
    entrypoint = script_dir / manifest["entrypoint"]

    result = subprocess.run(
        ["python3", entrypoint],
        capture_output=True,
        text=True,
        timeout=manifest.get("timeout_seconds", 10)
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }

def log_event(data):
    with open("logs.jsonl", "a") as f:
        f.write(json.dumps(data) + "\n")

def main():
    policies = load_policies()
    
    while True:
        for policy in policies:
            event = policy["event"]

            if event["type"] == "TIME_TRIGGER":
                if time_matches(event["time"]):
                    for action in policy["actions"]:
                        if "run_script" in action:
                            script_id = action["run_script"]

                            result = run_script(script_id)

                            log_event({
                                "timestamp": datetime.datetime.utcnow().isoformat(),
                                "policy": policy["policy_id"],
                                "action": "RUN_SCRIPT",
                                "script": script_id,
                                "result": result
                            })

        time.sleep(30)