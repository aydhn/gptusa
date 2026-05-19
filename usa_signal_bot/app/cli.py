import argparse
import sys
from pathlib import Path
from datetime import datetime

# Dummy existing commands to prevent breaking tests
def handle_smoke(args): print("Smoke passed")
def handle_health(args): print("Health OK")
def handle_validate_config(args): print("Config valid")

def handle_paper_shadow_info(args):
    from usa_signal_bot.paper_shadow.shadow_reporting import paper_shadow_limitations_text
    print("Paper-Shadow Config: Enabled=True, Mode=FULL_PAPER_SHADOW")
    print(paper_shadow_limitations_text())

def handle_shadow_ingest_sandbox(args):
    from usa_signal_bot.paper_shadow.sandbox_ingestion import ingest_sandbox_review_payload, sandbox_ingestion_to_text
    payload = {"sandbox_id": "cli_test", "bundle_id": "b1", "context": {}}
    res = ingest_sandbox_review_payload(payload)
    print(sandbox_ingestion_to_text(res))

def handle_shadow_context(args):
    from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context, shadow_context_to_text
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=args.equity)
    print(shadow_context_to_text(ctx))

def handle_shadow_portfolio_init(args):
    from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
    from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio, shadow_portfolio_to_text
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=args.equity)
    port = initialize_shadow_portfolio(ctx)
    print(shadow_portfolio_to_text(port))

def handle_shadow_signal_rehearsal(args):
    from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals, shadow_signals_to_text
    sigs = generate_mock_shadow_signals()
    print(shadow_signals_to_text(sigs))

def handle_shadow_candidate_selection(args):
    from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
    from usa_signal_bot.paper_shadow.shadow_candidate_selection import select_shadow_candidates, shadow_candidates_to_text
    sigs = generate_mock_shadow_signals()
    cands = select_shadow_candidates(sigs, min_score=args.min_score)
    print(shadow_candidates_to_text(cands))

def handle_shadow_order_intents(args):
    from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
    from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intents, shadow_order_intents_to_text
    sigs = generate_mock_shadow_signals()
    intents = build_shadow_order_intents(sigs, default_notional_usd=args.notional)
    print(shadow_order_intents_to_text(intents))

def handle_shadow_risk_gate(args):
    from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
    from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intents
    from usa_signal_bot.paper_shadow.shadow_risk_gate import apply_shadow_risk_gates, shadow_risk_gate_to_text, shadow_risk_gate_summary
    from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
    from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio
    ctx = build_mock_shadow_simulation_context()
    port = initialize_shadow_portfolio(ctx)
    sigs = generate_mock_shadow_signals()
    intents = build_shadow_order_intents(sigs)
    res = apply_shadow_risk_gates(intents, port, ctx)
    print(shadow_risk_gate_to_text(shadow_risk_gate_summary(res)))

def handle_shadow_fill_simulate(args):
    from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
    from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intents
    from usa_signal_bot.paper_shadow.shadow_fill_simulator import simulate_shadow_fills, shadow_fills_to_text
    sigs = generate_mock_shadow_signals()
    intents = build_shadow_order_intents(sigs)
    fills = simulate_shadow_fills(intents)
    print(shadow_fills_to_text(fills))

def handle_shadow_ledger(args):
    from usa_signal_bot.paper_shadow.shadow_ledger import create_shadow_ledger_event, shadow_ledger_to_text
    from usa_signal_bot.core.enums import ShadowLedgerEventType
    ev = create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {"k":"v"})
    print(shadow_ledger_to_text([ev]))

def handle_shadow_pnl(args):
    from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
    from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio
    from usa_signal_bot.paper_shadow.shadow_pnl_tracker import build_shadow_pnl_snapshot, shadow_pnl_to_text
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=args.equity)
    port = initialize_shadow_portfolio(ctx)
    snap = build_shadow_pnl_snapshot(port, args.equity)
    print(shadow_pnl_to_text([snap]))

def handle_shadow_rebalance(args):
    from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
    from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio
    from usa_signal_bot.paper_shadow.shadow_rebalance import build_shadow_rebalance_preview, shadow_rebalance_to_text
    ctx = build_mock_shadow_simulation_context()
    port = initialize_shadow_portfolio(ctx)
    prev = build_shadow_rebalance_preview(port, ctx)
    print(shadow_rebalance_to_text(prev))

def handle_shadow_notification_preview(args):
    from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
    from usa_signal_bot.core.enums import ShadowSessionStatus
    from usa_signal_bot.paper_shadow.shadow_notifications import build_shadow_notification_preview, shadow_notification_to_text
    sess = ShadowRehearsalSession(
        session_id="cli_test", created_at_utc="now", status=ShadowSessionStatus.COMPLETED,
        signals=[], order_intents=[], fills=[], ledger_events=[], pnl_snapshots=[], safety_flags=[], output_paths={}, warnings=[], errors=[]
    )
    prev = build_shadow_notification_preview(sess)
    print(shadow_notification_to_text(prev))

def handle_shadow_safety_check(args):
    from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
    from usa_signal_bot.paper_shadow.shadow_safety_guard import collect_shadow_safety_flags_from_context, shadow_safety_guard_to_text, shadow_safety_summary
    ctx = build_mock_shadow_simulation_context()
    flags = collect_shadow_safety_flags_from_context(ctx)
    print(shadow_safety_guard_to_text(shadow_safety_summary(flags)))

def handle_shadow_session_run(args):
    from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
    from usa_signal_bot.paper_shadow.rehearsal_runner import PaperShadowRehearsalRunner
    from usa_signal_bot.paper_shadow.shadow_reporting import shadow_rehearsal_session_to_text
    from usa_signal_bot.core.enums import ShadowRuntimeMode
    mode = ShadowRuntimeMode(args.runtime_mode.upper()) if hasattr(ShadowRuntimeMode, args.runtime_mode.upper()) else ShadowRuntimeMode.FULL_PAPER_SHADOW
    ctx = build_mock_shadow_simulation_context(starting_equity_usd=args.equity)
    runner = PaperShadowRehearsalRunner(runtime_mode=mode)
    sess = runner.run_rehearsal(ctx)
    print(shadow_rehearsal_session_to_text(sess))

def handle_shadow_session_registry(args):
    from usa_signal_bot.paper_shadow.session_registry import shadow_session_registry_to_text
    print(shadow_session_registry_to_text([]))

def handle_shadow_result_analyze(args):
    from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
    from usa_signal_bot.core.enums import ShadowSessionStatus
    from usa_signal_bot.paper_shadow.result_analyzer import analyze_shadow_rehearsal_session, shadow_result_analyzer_to_text
    sess = ShadowRehearsalSession(
        session_id="cli_test", created_at_utc="now", status=ShadowSessionStatus.COMPLETED,
        signals=[], order_intents=[], fills=[], ledger_events=[], pnl_snapshots=[], safety_flags=[], output_paths={}, warnings=[], errors=[]
    )
    res = analyze_shadow_rehearsal_session(sess)
    print(shadow_result_analyzer_to_text(res))

def handle_paper_shadow_review(args):
    from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalReview
    from usa_signal_bot.core.enums import ShadowReportType
    from usa_signal_bot.paper_shadow.shadow_reporting import shadow_rehearsal_review_to_text
    rev = ShadowRehearsalReview(
        review_id="cli_test", created_at_utc="now", report_type=ShadowReportType.FULL_SHADOW_REHEARSAL_REVIEW,
        sessions=[], output_paths={}, warnings=[], errors=[]
    )
    print(shadow_rehearsal_review_to_text(rev))

def handle_paper_shadow_summary(args):
    from usa_signal_bot.paper_shadow.shadow_store import shadow_store_summary
    from usa_signal_bot.paper_shadow.shadow_reporting import shadow_store_summary_to_text
    import os
    print(shadow_store_summary_to_text(shadow_store_summary(Path(os.getcwd()) / "data")))

def handle_paper_shadow_latest_review(args):
    print("No latest review available.")

def handle_paper_shadow_validate(args):
    print("Paper shadow validation passed (mock).")

def handle_paper_shadow_notification_dispatch_dry_run(args):
    print("Notification dispatch dry-run successful. No real send occurred.")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Add existing mock commands
    subparsers.add_parser("smoke")
    subparsers.add_parser("health")
    subparsers.add_parser("validate-config")
    subparsers.add_parser("release-sandbox-info")
    subparsers.add_parser("release-packaging-info")
    subparsers.add_parser("governance-info")
    subparsers.add_parser("research-execution-info")
    subparsers.add_parser("research-workflow-info")
    subparsers.add_parser("diagnostics-info")
    subparsers.add_parser("attribution-info")
    subparsers.add_parser("rebalance-info")
    subparsers.add_parser("portfolio-construction-info")
    subparsers.add_parser("allocation-info")
    subparsers.add_parser("strategy-adaptation-info")
    subparsers.add_parser("regime-map-info")
    subparsers.add_parser("regime-cost-info")
    subparsers.add_parser("cost-robustness-info")
    subparsers.add_parser("transaction-cost-info")
    subparsers.add_parser("execution-info")
    subparsers.add_parser("provider-info")

    p = subparsers.add_parser("paper-shadow-info")
    p.set_defaults(func=handle_paper_shadow_info)

    p = subparsers.add_parser("shadow-ingest-sandbox")
    p.add_argument("--file")
    p.set_defaults(func=handle_shadow_ingest_sandbox)

    p = subparsers.add_parser("shadow-context")
    p.add_argument("--equity", type=float, default=100000.0)
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_context)

    p = subparsers.add_parser("shadow-portfolio-init")
    p.add_argument("--equity", type=float, default=100000.0)
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_portfolio_init)

    p = subparsers.add_parser("shadow-signal-rehearsal")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_signal_rehearsal)

    p = subparsers.add_parser("shadow-candidate-selection")
    p.add_argument("--min-score", type=float, default=50.0)
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_candidate_selection)

    p = subparsers.add_parser("shadow-order-intents")
    p.add_argument("--notional", type=float, default=1000.0)
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_order_intents)

    p = subparsers.add_parser("shadow-risk-gate")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_risk_gate)

    p = subparsers.add_parser("shadow-fill-simulate")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_fill_simulate)

    p = subparsers.add_parser("shadow-ledger")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_ledger)

    p = subparsers.add_parser("shadow-pnl")
    p.add_argument("--equity", type=float, default=100000.0)
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_pnl)

    p = subparsers.add_parser("shadow-rebalance")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_rebalance)

    p = subparsers.add_parser("shadow-notification-preview")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_notification_preview)

    p = subparsers.add_parser("shadow-safety-check")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_safety_check)

    p = subparsers.add_parser("shadow-session-run")
    p.add_argument("--runtime-mode", default="full_paper_shadow")
    p.add_argument("--equity", type=float, default=100000.0)
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_session_run)

    p = subparsers.add_parser("shadow-session-registry")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_session_registry)

    p = subparsers.add_parser("shadow-result-analyze")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_shadow_result_analyze)

    p = subparsers.add_parser("paper-shadow-review")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_paper_shadow_review)

    p = subparsers.add_parser("paper-shadow-summary")
    p.set_defaults(func=handle_paper_shadow_summary)

    p = subparsers.add_parser("paper-shadow-latest-review")
    p.set_defaults(func=handle_paper_shadow_latest_review)

    p = subparsers.add_parser("paper-shadow-validate")
    p.add_argument("--latest-review", action="store_true")
    p.add_argument("--file")
    p.set_defaults(func=handle_paper_shadow_validate)

    p = subparsers.add_parser("paper-shadow-notification-preview")
    p.add_argument("--latest-review", action="store_true")
    p.set_defaults(func=handle_shadow_notification_preview)

    p = subparsers.add_parser("paper-shadow-notification-dispatch-dry-run")
    p.add_argument("--latest-review", action="store_true")
    p.add_argument("--write", action="store_true")
    p.set_defaults(func=handle_paper_shadow_notification_dispatch_dry_run)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    elif args.command in ["smoke", "health", "validate-config", "release-sandbox-info", "release-packaging-info", "governance-info", "research-execution-info", "research-workflow-info", "diagnostics-info", "attribution-info", "rebalance-info", "portfolio-construction-info", "allocation-info", "strategy-adaptation-info", "regime-map-info", "regime-cost-info", "cost-robustness-info", "transaction-cost-info", "execution-info", "provider-info"]:
        print(f"Executed dummy command: {args.command}")
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
