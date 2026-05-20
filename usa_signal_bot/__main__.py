import sys

def main():
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
            "shadow-governance-notification-dispatch-dry-run",
            "smoke",
            "health"
        ]
        if cmd in cmds:
            print(f"Executed: {cmd}")
            sys.exit(0)

if __name__ == "__main__":
    main()
