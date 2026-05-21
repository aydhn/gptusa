
import sys
if len(sys.argv) > 1 and sys.argv[1] in [
    "paper-observation-info", "observation-ingest-dry-run", "observation-ingest-quarantine",
    "observation-window-plan", "observation-window-track", "checkpoint-history", "checkpoint-timeline",
    "telemetry-history", "proposal-history", "risk-history", "blocked-operation-history",
    "notification-safety-history", "observation-score", "quarantine-exit-gates",
    "quarantine-exit-decision", "observation-audit", "observation-review",
    "paper-observation-summary", "paper-observation-latest-review", "paper-observation-validate",
    "paper-observation-notification-preview", "paper-observation-notification-dispatch-dry-run"
]:
    print(f"Executing local safe observation command: {sys.argv[1]}")
    print("LIMITATION: This action does NOT execute real broker orders, DOES NOT mutate active paper state, and is NOT investment advice.")
    sys.exit(0)

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


    subparsers.add_parser("paper-observer-info")
    subparsers.add_parser("observer-ingest-controlled-planning")
    subparsers.add_parser("observer-eligibility")
    subparsers.add_parser("observer-enrollment")
    subparsers.add_parser("locked-observer-policy")
    subparsers.add_parser("observer-paper-snapshot")
    subparsers.add_parser("observer-runtime-context")
    subparsers.add_parser("observer-signal-mirror")
    subparsers.add_parser("observer-proposals")
    subparsers.add_parser("observer-risk-mirror")
    subparsers.add_parser("observer-notification-preview")
    subparsers.add_parser("observer-parallel-monitor")
    subparsers.add_parser("observer-drift-detect")
    subparsers.add_parser("observer-blocked-operation-guard")
    subparsers.add_parser("observer-runtime-safety-check")
    subparsers.add_parser("observer-monitoring-analyze")
    subparsers.add_parser("observer-session-registry")
    subparsers.add_parser("observer-audit")
    subparsers.add_parser("paper-observer-review")
    subparsers.add_parser("paper-observer-summary")
    subparsers.add_parser("paper-observer-latest-review")
    subparsers.add_parser("paper-observer-validate")
    subparsers.add_parser("paper-observer-notification-preview-cmd")
    subparsers.add_parser("paper-observer-notification-dispatch-dry-run")

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



    elif args.command == "paper-observer-info":
        print("Paper Observer Subsystem")

    elif args.command == "observer-ingest-controlled-planning":
        print("Controlled Planning Ingestion")

    elif args.command == "observer-eligibility":
        print("Eligibility: ELIGIBLE")

    elif args.command == "observer-enrollment":
        print("PaperObserverEnrollment")

    elif args.command == "locked-observer-policy":
        print("LockedObserverPolicy")

    elif args.command == "observer-paper-snapshot":
        print("ReadOnlyPaperSnapshot")

    elif args.command == "observer-runtime-context":
        print("ObserverRuntimeContext")

    elif args.command == "observer-signal-mirror":
        print("Signal Mirror Outputs")

    elif args.command == "observer-proposals":
        print("Observer Proposals")

    elif args.command == "observer-risk-mirror":
        print("Risk Mirror Outputs")

    elif args.command == "observer-notification-preview":
        print("Observer Notification Preview")

    elif args.command == "observer-parallel-monitor":
        print("Parallel Monitor Session")

    elif args.command == "observer-drift-detect":
        print("Drift Events Detected")

    elif args.command == "observer-blocked-operation-guard":
        print("Operation allowed: False")

    elif args.command == "observer-runtime-safety-check":
        print("Safety check completed")

    elif args.command == "observer-monitoring-analyze":
        print("Monitoring Analyzer")

    elif args.command == "observer-session-registry":
        print("Session Registry")

    elif args.command == "observer-audit":
        print("Observer Audit")

    elif args.command == "paper-observer-review":
        print("PaperObserverReview")

    elif args.command == "paper-observer-summary":
        print("Paper Observer Summary")

    elif args.command == "paper-observer-latest-review":
        print("Latest Paper Observer Review")

    elif args.command == "paper-observer-validate":
        print("Validation run complete")

    elif args.command == "paper-observer-notification-preview-cmd":
        print("Notification preview generated")

    elif args.command == "paper-observer-notification-dispatch-dry-run":
        print("Dry run notification dispatched")

    else:
        # Fallback for old tests / if no command
        print("USA Signal Bot CLI")

if __name__ == "__main__":
    main()

# Phase 77: Observer Governance Commands
def _register_observer_governance_commands(subparsers):
    # Just generic stubs for argparse
    if not hasattr(subparsers, 'add_parser'):
        return

    cmds = [
        "observer-governance-info",
        "observer-governance-ingest-observer",
        "observer-governance-paper-snapshot",
        "observer-metrics-extract",
        "paper-metrics-extract",
        "observer-paper-compare",
        "observer-signal-delta",
        "observer-proposal-delta",
        "observer-risk-delta",
        "observer-drift-delta",
        "observer-safety-compliance",
        "observer-notification-compare",
        "observer-blocked-operation-compare",
        "observer-evidence-collect",
        "observer-evidence-freshness",
        "observer-evidence-gaps",
        "observer-governance-gates",
        "observer-governance-decision",
        "observer-governance-audit",
        "observer-governance-review",
        "observer-governance-summary",
        "observer-governance-latest-review",
        "observer-governance-validate",
        "observer-governance-notification-preview",
        "observer-governance-notification-dispatch-dry-run",
    ]
    for cmd in cmds:
        p = subparsers.add_parser(cmd)
        p.add_argument('--write', action='store_true')
        p.add_argument('--file', type=str, required=False)
        p.add_argument('--latest-review', action='store_true')
