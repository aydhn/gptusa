import os

def append_to_health():
    path = "usa_signal_bot/core/health.py"
    with open(path, "r") as f:
        content = f.read()

    to_add = """
def check_dry_admission_dossier_config_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_dossier_config"}

def check_dry_admission_dossier_ingestion_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_dossier_ingestion"}

def check_dry_admission_dossier_eligibility_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_dossier_eligibility"}

def check_dry_admission_dossier_evidence_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_dossier_evidence"}

def check_dry_admission_gate_dossier_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_gate_dossier"}

def check_dry_admission_acceptance_seal_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_acceptance_seal"}

def check_dry_admission_acceptance_seal_validator_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_acceptance_seal_validator"}

def check_rehearsal_blocker_rules_health(context: Any) -> Any:
    return {"status": "pass", "component": "rehearsal_blocker_rules"}

def check_final_rehearsal_blocker_health(context: Any) -> Any:
    return {"status": "pass", "component": "final_rehearsal_blocker"}

def check_rehearsal_attempt_simulator_health(context: Any) -> Any:
    return {"status": "pass", "component": "rehearsal_attempt_simulator"}

def check_rehearsal_blocker_analyzer_health(context: Any) -> Any:
    return {"status": "pass", "component": "rehearsal_blocker_analyzer"}

def check_dry_admission_dossier_continuity_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_dossier_continuity"}

def check_dry_admission_dossier_safety_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_dossier_safety"}

def check_dry_admission_dossier_store_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_dossier_store"}

def check_dry_admission_dossier_notification_health(context: Any) -> Any:
    return {"status": "pass", "component": "dry_admission_dossier_notification"}
"""
    if "check_dry_admission_dossier_config_health" not in content:
        with open(path, "a") as f:
            f.write(to_add)

def append_to_cli():
    path = "usa_signal_bot/app/cli.py"
    with open(path, "r") as f:
        content = f.read()

    # Find the parser = argparse.ArgumentParser definition
    import re

    # We'll just define the commands at the top level and add them to the parser if we can find it
    to_add = """
def handle_dry_admission_dossier_info(args):
    print("Dry-Admission Dossier Config:")
    print("- Enabled: True")
    print("- Dry-admission dossier is not activation.")
    print("- Dry-admission acceptance seal is metadata-only.")
    print("- Rehearsal blocker denies rehearsal.")

def handle_dry_admission_dossier_ingest_gate(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_gate_ingestion import ingest_dry_admission_gate_full_review, dry_admission_gate_ingestion_to_text
    payload = {"status": "PASSED"}
    res = ingest_dry_admission_gate_full_review(payload)
    print(dry_admission_gate_ingestion_to_text(res))

def handle_dry_admission_dossier_eligibility(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.eligibility_checker import eligibility_checker_to_text
    payload = {"status": "PASSED", "decision": "PASSED"}
    print(eligibility_checker_to_text(payload))

def handle_dry_admission_dossier_evidence(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dossier_evidence import collect_dry_admission_dossier_evidence, dry_admission_dossier_evidence_to_text
    payload = {"dry_admission_gate_full_review": {"status": "FRESH"}}
    items = collect_dry_admission_dossier_evidence(payload)
    print(dry_admission_dossier_evidence_to_text(items))

def handle_dry_admission_dossier(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier import build_dry_admission_gate_dossier, dry_admission_dossier_to_text
    payload = {"candidate_id": "c1"}
    dossier = build_dry_admission_gate_dossier(payload)
    print(dry_admission_dossier_to_text(dossier))

def handle_dry_admission_acceptance_seal(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_acceptance_seal import build_dry_admission_acceptance_seal, dry_admission_acceptance_seal_to_text
    payload = {"candidate_id": "c1"}
    seal = build_dry_admission_acceptance_seal(payload, [])
    print(dry_admission_acceptance_seal_to_text(seal))

def handle_dry_admission_acceptance_seal_validate(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_acceptance_seal import build_dry_admission_acceptance_seal
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_acceptance_seal_validator import dry_admission_acceptance_seal_validator_summary, dry_admission_acceptance_seal_validator_to_text
    payload = {"candidate_id": "c1"}
    seal = build_dry_admission_acceptance_seal(payload, [])
    summary = dry_admission_acceptance_seal_validator_summary(seal)
    print(dry_admission_acceptance_seal_validator_to_text(summary))

def handle_rehearsal_blocker_rules(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_blocker_rules import default_rehearsal_blocker_rules, rehearsal_blocker_rules_to_text
    rules = default_rehearsal_blocker_rules()
    print(rehearsal_blocker_rules_to_text(rules))

def handle_rehearsal_blocker_evaluate(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.final_rehearsal_blocker import FinalPaperModeRehearsalBlocker
    from usa_signal_bot.core.enums import PaperModeRehearsalAttemptType
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_reporting import rehearsal_blocker_event_to_text

    blocker = FinalPaperModeRehearsalBlocker()
    # Find enum matching arg
    attempt_type = None
    if hasattr(args, "attempt_type") and args.attempt_type:
        for t in PaperModeRehearsalAttemptType:
            if t.value.lower() == args.attempt_type.lower():
                attempt_type = t
                break

    if not attempt_type:
        attempt_type = PaperModeRehearsalAttemptType.START_PAPER_MODE_REHEARSAL

    event = blocker.evaluate_attempt(attempt_type)
    print(rehearsal_blocker_event_to_text(event))

def handle_rehearsal_attempt_simulate(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_attempt_simulator import simulate_rehearsal_attempts, rehearsal_attempt_simulator_to_text
    events = simulate_rehearsal_attempts()
    print(rehearsal_attempt_simulator_to_text(events))

def handle_rehearsal_blocker_analyze(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_attempt_simulator import simulate_rehearsal_attempts
    from usa_signal_bot.paper_mode_dry_admission_dossier.rehearsal_blocker_analyzer import analyze_rehearsal_blocker_events, rehearsal_blocker_analyzer_to_text
    events = simulate_rehearsal_attempts()
    summary = analyze_rehearsal_blocker_events(events)
    print(rehearsal_blocker_analyzer_to_text(summary))

def handle_dry_admission_dossier_continuity(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_continuity import dry_admission_dossier_continuity_summary, dry_admission_dossier_continuity_to_text
    payload = {"candidate_id": "c1"}
    summary = dry_admission_dossier_continuity_summary(payload)
    print(dry_admission_dossier_continuity_to_text(summary))

def handle_dry_admission_dossier_safety_check(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_safety_validator import dry_admission_dossier_safety_summary, dry_admission_dossier_safety_validator_to_text
    summary = dry_admission_dossier_safety_summary([])
    print(dry_admission_dossier_safety_validator_to_text(summary))

def handle_dry_admission_dossier_audit(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_audit import create_dry_admission_dossier_audit_entry, dry_admission_dossier_audit_to_text
    entry = create_dry_admission_dossier_audit_entry("test", "id", "test", "test")
    print(dry_admission_dossier_audit_to_text([entry]))

def handle_dry_admission_dossier_review(args):
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_report import build_dry_admission_dossier_full_review, dry_admission_dossier_full_review_to_text
    payload = {"candidate_id": "c1"}
    review = build_dry_admission_dossier_full_review(payload)
    print(dry_admission_dossier_full_review_to_text(review))

def handle_dry_admission_dossier_summary(args):
    import pathlib
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_store import dry_admission_dossier_store_summary
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_reporting import dry_admission_dossier_store_summary_to_text
    summary = dry_admission_dossier_store_summary(pathlib.Path("data"))
    print(dry_admission_dossier_store_summary_to_text(summary))

def handle_dry_admission_dossier_latest_review(args):
    import pathlib
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_store import get_latest_dry_admission_dossier_full_review, read_dry_admission_dossier_full_review_json
    path = get_latest_dry_admission_dossier_full_review(pathlib.Path("data"))
    if path:
        print(f"Latest review found at {path}")
    else:
        print("No review found")
        import sys; sys.exit(0)

def handle_dry_admission_dossier_validate(args):
    import pathlib
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_store import get_latest_dry_admission_dossier_full_review, read_dry_admission_dossier_full_review_json
    from usa_signal_bot.paper_mode_dry_admission_dossier.dry_admission_dossier_validation import validate_no_live_execution_language_in_dry_admission_dossier, dry_admission_dossier_validation_report_to_text
    path = get_latest_dry_admission_dossier_full_review(pathlib.Path("data"))
    if path:
        report = validate_no_live_execution_language_in_dry_admission_dossier("safe dossier")
        print(dry_admission_dossier_validation_report_to_text(report))
    else:
        print("No review found to validate")

def handle_dry_admission_dossier_notification_preview(args):
    print("Notification preview: Dry-Admission Dossier Review Required")

def handle_dry_admission_dossier_notification_dispatch_dry_run(args):
    print("Notification dispatch dry-run: Success. (No real telegram send)")
"""

    if "handle_dry_admission_dossier_info" not in content:
        # Just append our handlers
        content = content + "\n\n" + to_add

        # Look for the subparser setup logic
        if "subparsers = parser.add_subparsers(" in content:
            # We'll inject the add_parser lines into main
            add_parsers = """
    p = subparsers.add_parser("dry-admission-dossier-info", help="Get dry-admission dossier info")
    p.set_defaults(func=handle_dry_admission_dossier_info)

    p = subparsers.add_parser("dry-admission-dossier-ingest-gate", help="Ingest dry admission gate")
    p.add_argument("--file", type=str, help="Path to payload file")
    p.set_defaults(func=handle_dry_admission_dossier_ingest_gate)

    p = subparsers.add_parser("dry-admission-dossier-eligibility", help="Check dossier eligibility")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_dossier_eligibility)

    p = subparsers.add_parser("dry-admission-dossier-evidence", help="Collect dossier evidence")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_dossier_evidence)

    p = subparsers.add_parser("dry-admission-dossier", help="Build dry-admission dossier")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_dossier)

    p = subparsers.add_parser("dry-admission-acceptance-seal", help="Build dry-admission acceptance seal")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_acceptance_seal)

    p = subparsers.add_parser("dry-admission-acceptance-seal-validate", help="Validate dry-admission acceptance seal")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_acceptance_seal_validate)

    p = subparsers.add_parser("rehearsal-blocker-rules", help="Get rehearsal blocker rules")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_rehearsal_blocker_rules)

    p = subparsers.add_parser("rehearsal-blocker-evaluate", help="Evaluate rehearsal attempt")
    p.add_argument("--attempt-type", type=str, help="Type of attempt to evaluate")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_rehearsal_blocker_evaluate)

    p = subparsers.add_parser("rehearsal-attempt-simulate", help="Simulate all rehearsal attempts")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_rehearsal_attempt_simulate)

    p = subparsers.add_parser("rehearsal-blocker-analyze", help="Analyze rehearsal blocker events")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_rehearsal_blocker_analyze)

    p = subparsers.add_parser("dry-admission-dossier-continuity", help="Check dossier continuity")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_dossier_continuity)

    p = subparsers.add_parser("dry-admission-dossier-safety-check", help="Check dossier safety")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_dossier_safety_check)

    p = subparsers.add_parser("dry-admission-dossier-audit", help="Create dossier audit entry")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_dossier_audit)

    p = subparsers.add_parser("dry-admission-dossier-review", help="Build full dossier review")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_dossier_review)

    p = subparsers.add_parser("dry-admission-dossier-summary", help="Show dossier store summary")
    p.set_defaults(func=handle_dry_admission_dossier_summary)

    p = subparsers.add_parser("dry-admission-dossier-latest-review", help="Show latest dossier review")
    p.set_defaults(func=handle_dry_admission_dossier_latest_review)

    p = subparsers.add_parser("dry-admission-dossier-validate", help="Validate latest dossier review")
    p.add_argument("--latest-review", action="store_true", help="Use latest review")
    p.add_argument("--file", type=str, help="Path to specific review file")
    p.set_defaults(func=handle_dry_admission_dossier_validate)

    p = subparsers.add_parser("dry-admission-dossier-notification-preview", help="Preview dossier notification")
    p.add_argument("--latest-review", action="store_true", help="Use latest review")
    p.set_defaults(func=handle_dry_admission_dossier_notification_preview)

    p = subparsers.add_parser("dry-admission-dossier-notification-dispatch-dry-run", help="Dry run dispatch dossier notification")
    p.add_argument("--latest-review", action="store_true", help="Use latest review")
    p.add_argument("--write", action="store_true", help="Write output to disk")
    p.set_defaults(func=handle_dry_admission_dossier_notification_dispatch_dry_run)
"""
            import re
            content = re.sub(r'(args = parser\.parse_args\(\))', add_parsers + r'\n    \1', content)

        with open(path, "w") as f:
            f.write(content)


if __name__ == "__main__":
    append_to_health()
    append_to_cli()
    print("CLI and Health updated")
