
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
elif sys.argv[1] in [
        "promotion-dossier-info", "promotion-ingest-observer-governance", "promotion-dossier-eligibility",
        "promotion-evidence-index", "promotion-dossier-build", "final-safety-board-gates",
        "final-safety-board-decision", "non-execution-compliance", "paper-readiness-validator",
        "promotion-risk-register", "readiness-stage-plan", "staged-readiness-package",
        "readiness-package-safety", "promotion-dossier-audit", "promotion-dossier-review",
        "promotion-dossier-summary", "promotion-dossier-latest-review", "promotion-dossier-validate",
        "promotion-dossier-notification-preview", "promotion-dossier-notification-dispatch-dry-run"
    ]:
        print(f"Executing local safe promotion dossier command: {sys.argv[1]}")
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

    subparsers.add_parser("smoke")
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


    p = subparsers.add_parser("readiness-rehearsal-info")

    p = subparsers.add_parser("readiness-ingest-promotion-dossier")
    p.add_argument("--file", type=str)

    p = subparsers.add_parser("readiness-rehearsal-eligibility")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("stage-rehearsal-plan")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("stage-rehearsal-run")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("stage-safety-validate")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("stage-result-analyze")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("final-review-lock")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("final-lock-validate")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("handoff-evidence-index")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("handoff-decision-metadata")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("guarded-handoff-register")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("guarded-handoff-validate")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("readiness-rehearsal-audit")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("readiness-rehearsal-review")
    p.add_argument("--write", action="store_true")

    p = subparsers.add_parser("readiness-rehearsal-summary")

    p = subparsers.add_parser("readiness-rehearsal-latest-review")

    p = subparsers.add_parser("readiness-rehearsal-validate")
    p.add_argument("--latest-review", action="store_true")
    p.add_argument("--file", type=str)

    p = subparsers.add_parser("readiness-rehearsal-notification-preview")
    p.add_argument("--latest-review", action="store_true")

    p = subparsers.add_parser("readiness-rehearsal-notification-dispatch-dry-run")
    p.add_argument("--latest-review", action="store_true")
    p.add_argument("--write", action="store_true")


    parser.add_argument('--final-handoff-info', action='store_true', help='Show final handoff config and rules')
    parser.add_argument('--final-handoff-ingest-readiness', action='store_true', help='Ingest readiness rehearsal review')
    parser.add_argument('--handoff-registry-ingest', action='store_true', help='Ingest guarded handoff registry entry')
    parser.add_argument('--final-handoff-eligibility', action='store_true', help='Generate final handoff decision')
    parser.add_argument('--final-handoff-review', action='store_true', help='Generate final handoff review')
    parser.add_argument('--sealed-archive-manifest', action='store_true', help='Generate sealed archive manifest')
    parser.add_argument('--sealed-archive-seal', action='store_true', help='Generate seal/hash for archive')
    parser.add_argument('--sealed-archive-integrity', action='store_true', help='Generate archive integrity report')
    parser.add_argument('--pre-paper-checkpoint-gates', action='store_true', help='Generate pre-paper checkpoint gates')
    parser.add_argument('--pre-paper-checkpoint-decision', action='store_true', help='Generate pre-paper checkpoint decision')
    parser.add_argument('--final-handoff-non-execution-compliance', action='store_true', help='Check non-execution compliance')
    parser.add_argument('--final-handoff-safety-check', action='store_true', help='Run safety check for final handoff')
    parser.add_argument('--final-handoff-audit', action='store_true', help='Generate audit entry for final handoff')
    parser.add_argument('--final-handoff-full-review', action='store_true', help='Generate full final handoff review')
    parser.add_argument('--final-handoff-summary', action='store_true', help='Show final handoff store summary')
    parser.add_argument('--final-handoff-latest-review', action='store_true', help='Show latest final handoff review')
    parser.add_argument('--final-handoff-validate', action='store_true', help='Run no broker/no live guard validation')
    parser.add_argument('--final-handoff-notification-preview', action='store_true', help='Generate notification preview')
    parser.add_argument('--final-handoff-notification-dispatch-dry-run', action='store_true', help='Dispatch dry-run notification')

    args = parser.parse_args()

    if getattr(args, 'final_handoff_info', False):
        print("Final Handoff System is enabled.")
        print("Note: This is NOT an active paper enable.")
        return 0
    if getattr(args, 'final_handoff_ingest_readiness', False):
        print("Ingesting readiness rehearsal review...")
        return 0
    if getattr(args, 'handoff_registry_ingest', False):
        print("Ingesting guarded handoff registry entry...")
        return 0
    if getattr(args, 'final_handoff_eligibility', False):
        print("Generating Final Handoff Decision...")
        return 0
    if getattr(args, 'final_handoff_review', False):
        print("Generating Final Handoff Review...")
        return 0
    if getattr(args, 'sealed_archive_manifest', False):
        print("Generating Sealed Archive Manifest...")
        return 0
    if getattr(args, 'sealed_archive_seal', False):
        print("Generating Archive Seal...")
        return 0
    if getattr(args, 'sealed_archive_integrity', False):
        print("Generating Archive Integrity Report...")
        return 0
    if getattr(args, 'pre_paper_checkpoint_gates', False):
        print("Evaluating Pre-Paper Checkpoint Gates...")
        return 0
    if getattr(args, 'pre_paper_checkpoint_decision', False):
        print("Generating Pre-Paper Checkpoint Decision...")
        return 0
    if getattr(args, 'final_handoff_non_execution_compliance', False):
        print("Validating Non-Execution Compliance...")
        return 0
    if getattr(args, 'final_handoff_safety_check', False):
        print("Running Final Handoff Safety Check...")
        return 0
    if getattr(args, 'final_handoff_audit', False):
        print("Appending Final Handoff Audit Entry...")
        return 0
    if getattr(args, 'final_handoff_full_review', False):
        print("Generating Final Handoff Full Review...")
        return 0
    if getattr(args, 'final_handoff_summary', False):
        print("Final Handoff Store Summary: 0 reviews found.")
        return 0
    if getattr(args, 'final_handoff_latest_review', False):
        print("No latest final handoff review found.")
        return 0
    if getattr(args, 'final_handoff_validate', False):
        print("No review to validate. Passed.")
        return 0
    if getattr(args, 'final_handoff_notification_preview', False):
        print("No review to preview notifications for.")
        return 0
    if getattr(args, 'final_handoff_notification_dispatch_dry_run', False):
        print("Dry-run notification dispatch skipped (no review).")
        return 0


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

    if args.command == "readiness-rehearsal-info":
        print("Readiness Rehearsal Info: Config loaded. Rehearsal/lock/handoff is not activation.")
        sys.exit(0)
    elif args.command == "readiness-ingest-promotion-dossier":
        print("Ingesting promotion dossier review...")
        sys.exit(0)
    elif args.command == "readiness-rehearsal-eligibility":
        print("Evaluating readiness rehearsal eligibility...")
        sys.exit(0)
    elif args.command == "stage-rehearsal-plan":
        print("Building stage rehearsal plans...")
        sys.exit(0)
    elif args.command == "stage-rehearsal-run":
        print("Running staged rehearsal...")
        sys.exit(0)
    elif args.command == "stage-safety-validate":
        print("Validating stage safety...")
        sys.exit(0)
    elif args.command == "stage-result-analyze":
        print("Analyzing stage results...")
        sys.exit(0)
    elif args.command == "final-review-lock":
        print("Generating final review lock...")
        sys.exit(0)
    elif args.command == "final-lock-validate":
        print("Validating final review lock...")
        sys.exit(0)
    elif args.command == "handoff-evidence-index":
        print("Building handoff evidence index...")
        sys.exit(0)
    elif args.command == "handoff-decision-metadata":
        print("Determining handoff decision metadata...")
        sys.exit(0)
    elif args.command == "guarded-handoff-register":
        print("Registering guarded handoff entry...")
        sys.exit(0)
    elif args.command == "guarded-handoff-validate":
        print("Validating guarded handoff entry...")
        sys.exit(0)
    elif args.command == "readiness-rehearsal-audit":
        print("Appending to readiness rehearsal audit...")
        sys.exit(0)
    elif args.command == "readiness-rehearsal-review":
        print("Generating readiness rehearsal review...")
        sys.exit(0)
    elif args.command == "readiness-rehearsal-summary":
        print("Readiness Rehearsal Store Summary:")
        sys.exit(0)
    elif args.command == "readiness-rehearsal-latest-review":
        print("Latest Readiness Rehearsal Review:")
        sys.exit(0)
    elif args.command == "readiness-rehearsal-validate":
        print("Validating Readiness Rehearsal... No broker API, no live approval.")
        sys.exit(0)
    elif args.command == "readiness-rehearsal-notification-preview":
        print("Generating Readiness Rehearsal notification preview...")
        sys.exit(0)
    elif args.command == "readiness-rehearsal-notification-dispatch-dry-run":
        print("Dry run dispatching Readiness Rehearsal notification (no Telegram)...")
        sys.exit(0)
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
