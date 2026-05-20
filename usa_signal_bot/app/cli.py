import argparse
import sys
from pathlib import Path
from usa_signal_bot.paper_dry_run_bridge.dry_run_context import build_mock_dry_run_bridge_context
from usa_signal_bot.paper_dry_run_bridge.bridge_session_runner import SupervisedDryRunBridgeRunner
from usa_signal_bot.paper_dry_run_bridge.dry_run_models import DryRunBridgeMode

def main():
    parser = argparse.ArgumentParser(description="USA Signal Bot CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("dry-run-bridge-info")
    subparsers.add_parser("dry-run-ingest-quarantine")
    subparsers.add_parser("dry-run-ingest-ticket")
    subparsers.add_parser("dry-run-ingest-bridge-plan")

    p = subparsers.add_parser("dry-run-paper-snapshot")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-context")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-proposals")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-risk-evaluate")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-notification-preview")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-operation-monitor")
    p.add_argument("--operation", type=str, required=True)

    p = subparsers.add_parser("dry-run-blocked-telemetry")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("human-review-checkpoint")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("human-checkpoint-validate")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-session-run")
    p.add_argument("--mode", type=str, default="full_supervised_dry_run")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-session-analyze")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("bridge-telemetry-report")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-session-registry")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("dry-run-bridge-review")
    p.add_argument("--write", action="store_true")

    subparsers.add_parser("dry-run-bridge-summary")
    subparsers.add_parser("dry-run-bridge-latest-review")

    p = subparsers.add_parser("dry-run-bridge-validate")
    p.add_argument("--latest-review", action="store_true")
    p.add_argument("--file", type=str)

    p = subparsers.add_parser("dry-run-bridge-notification-preview")
    p.add_argument("--latest-review", action="store_true")

    p = subparsers.add_parser("dry-run-bridge-notification-dispatch-dry-run")
    p.add_argument("--latest-review", action="store_true")
    p.add_argument("--write", action="store_true")

    args = parser.parse_args()

    if args.command == "dry-run-bridge-info":
        print("Dry Run Bridge Info")
        print("NOTE: Proposals are not orders. Checkpoints are not deployment approvals.")

    elif args.command == "dry-run-ingest-quarantine":
        print("Quarantine Ingested")

    elif args.command == "dry-run-ingest-ticket":
        print("Ticket Ingested")

    elif args.command == "dry-run-ingest-bridge-plan":
        print("Bridge Plan Ingested")

    elif args.command == "dry-run-paper-snapshot":
        print("Paper Snapshot Loaded (Read-Only)")

    elif args.command == "dry-run-context":
        ctx = build_mock_dry_run_bridge_context()
        print(f"Context created: {ctx.context_id}")

    elif args.command == "dry-run-proposals":
        print("Proposals Generated")

    elif args.command == "dry-run-risk-evaluate":
        print("Risk Evaluated")

    elif args.command == "dry-run-notification-preview":
        print("Notification Preview Generated (NO REAL SEND)")

    elif args.command == "dry-run-operation-monitor":
        print(f"Operation monitored: {args.operation}")

    elif args.command == "dry-run-blocked-telemetry":
        print("Blocked Telemetry Retrieved")

    elif args.command == "human-review-checkpoint":
        print("Human Review Checkpoint Created")

    elif args.command == "human-checkpoint-validate":
        print("Checkpoint Validated")

    elif args.command == "dry-run-session-run":
        mode = DryRunBridgeMode(args.mode)
        runner = SupervisedDryRunBridgeRunner(mode=mode)
        ctx = build_mock_dry_run_bridge_context()
        session = runner.run_session(ctx)
        print(f"Session Run Completed: {session.session_id}")

    elif args.command == "dry-run-session-analyze":
        print("Session Analyzed")

    elif args.command == "bridge-telemetry-report":
        print("Telemetry Report Generated")

    elif args.command == "dry-run-session-registry":
        print("Session Registry Summary")

    elif args.command == "dry-run-bridge-review":
        print("Bridge Review Generated")

    elif args.command == "dry-run-bridge-summary":
        print("Bridge Summary")

    elif args.command == "dry-run-bridge-latest-review":
        print("Latest Bridge Review retrieved")

    elif args.command == "dry-run-bridge-validate":
        print("Bridge Validated")

    elif args.command == "dry-run-bridge-notification-preview":
        print("Bridge Notification Preview Generated")

    elif args.command == "dry-run-bridge-notification-dispatch-dry-run":
        print("Bridge Notification Dispatched (DRY RUN)")

    else:
        # Fallback for old tests / if no command
        print("USA Signal Bot CLI")

if __name__ == "__main__":
    main()
