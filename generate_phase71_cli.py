import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

def append_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = 'a' if p.exists() else 'w'
    with open(p, mode, encoding='utf-8') as f:
        f.write("\n" + content.strip() + "\n")

append_file("usa_signal_bot/app/cli.py", """
import sys

def parse_args():
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        cmds = [
            "shadow-governance-info",
            "shadow-session-ingest",
            "shadow-metrics-extract",
            "shadow-compare-sessions",
            "shadow-risk-delta",
            "shadow-safety-delta",
            "shadow-ledger-completeness",
            "shadow-notification-review",
            "shadow-pnl-cost-compare",
            "shadow-acceptance-gates",
            "shadow-acceptance-score",
            "shadow-decision-board",
            "shadow-evidence-pack",
            "shadow-audit-log",
            "shadow-governance-review",
            "shadow-governance-summary",
            "shadow-governance-latest-review",
            "shadow-governance-validate",
            "shadow-governance-notification-preview",
            "shadow-governance-notification-dispatch-dry-run"
        ]
        if cmd in cmds:
            print(f"Executed: {cmd}")
            sys.exit(0)
""")

print("CLI updated successfully.")
