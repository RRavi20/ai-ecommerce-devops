#!/usr/bin/env python3
import subprocess
from datetime import datetime
from pathlib import Path

REPORT_DIR = Path("reports/incidents")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def run_command(command):
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return result.stderr.strip() or "Command failed"
        return result.stdout.strip() or "No output"
    except Exception as exc:
        return f"Error: {exc}"



def get_loki_logs():
    """Retrieve recent application logs from Loki."""
    import json
    import urllib.parse
    import urllib.request

    query = '{job="docker",container="ai-ecommerce-jenkins"}'
    params = urllib.parse.urlencode({
        "query": query,
        "limit": "20",
        "direction": "backward",
    })
    url = "http://localhost:3100/loki/api/v1/query_range?" + params

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        lines = []
        for stream in data.get("data", {}).get("result", []):
            for entry in stream.get("values", []):
                lines.append(entry[1])

        return "\n".join(lines) if lines else "No matching application logs found."
    except Exception as exc:
        return f"Loki query failed: {exc}"

def main():
    print("1/4 Checking Kubernetes pods...")
    pods = run_command(["kubectl", "get", "pods", "-A"])

    print("2/4 Checking warning events...")
    events = run_command([
        "kubectl", "get", "events", "-A",
        "--field-selector=type=Warning",
        "--sort-by=.lastTimestamp"
    ])

    print("3/4 Checking Kubernetes node...")
    nodes = run_command(["kubectl", "get", "nodes", "-o", "wide"])

    print("4/5 Collecting application logs from Loki...")
    loki_logs = get_loki_logs()

    findings = []

    if "notready" in nodes.lower().replace(" ", ""):
        findings.append(
            "HIGH: A node may not be Ready. Check node conditions."
        )

    if any(word in events.lower() for word in (
        "readiness probe failed",
        "liveness probe failed",
        "startup probe failed",
    )):
        findings.append(
            "MEDIUM: Probe failures appear in warning events. "
            "Check current pod status and restart history."
        )

    if "back-off" in events.lower() or "crashloopbackoff" in pods.lower():
        findings.append(
            "HIGH: Restart back-off indicators found. "
            "Inspect affected container logs."
        )

    if not findings:
        findings.append(
            "No configured incident patterns detected. "
            "This does not guarantee the system is error-free."
        )

    print("5/5 Writing incident report...")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = REPORT_DIR / f"incident-{timestamp}.md"

    report = (
        "# Incident Analysis Report\n\n"
        f"Generated: {datetime.now().astimezone().isoformat()}\n\n"
        "## Preliminary Rule-Based Findings\n\n"
        + "\n".join("- " + item for item in findings)
        + "\n\n## Kubernetes Nodes\n\n"
        "```text\n" + nodes + "\n```\n"
        "\n## Kubernetes Pods\n\n"
        "```text\n" + pods + "\n```\n"
        "\n## Kubernetes Warning Events\n\n"
        "```text\n" + events + "\n```\n"
        "\n## Recent Application Logs (Loki)\n\n"
        "```text\n" + loki_logs + "\n```\n"
        "\n## Limitations\n\n"
        "This report uses rule-based checks, not AI-generated analysis. "
        "Warning events can be historical. Verify findings before taking "
        "action. The script does not modify Kubernetes resources.\n"
    )

    report_path.write_text(report, encoding="utf-8")
    print("\nIncident analysis completed.")
    print(f"Report saved: {report_path.resolve()}")
    for item in findings:
        print("- " + item)


if __name__ == "__main__":
    main()
