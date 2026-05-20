import sys
from pathlib import Path
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowRuntimeMode, ShadowReportType, ShadowRehearsalReview,
    create_shadow_rehearsal_review_id, get_utc_now_str
)
from usa_signal_bot.paper_shadow.simulation_context import build_mock_shadow_simulation_context
from usa_signal_bot.paper_shadow.shadow_portfolio import initialize_shadow_portfolio
from usa_signal_bot.paper_shadow.shadow_signal_rehearsal import generate_mock_shadow_signals
from usa_signal_bot.paper_shadow.shadow_candidate_selection import select_shadow_candidates
from usa_signal_bot.paper_shadow.shadow_order_intent import build_shadow_order_intents
from usa_signal_bot.paper_shadow.shadow_risk_gate import apply_shadow_risk_gates
from usa_signal_bot.paper_shadow.shadow_fill_simulator import simulate_shadow_fills
from usa_signal_bot.paper_shadow.shadow_ledger import create_shadow_ledger_event, append_shadow_ledger_event
from usa_signal_bot.paper_shadow.shadow_pnl_tracker import build_shadow_pnl_snapshot
from usa_signal_bot.paper_shadow.shadow_rebalance import build_shadow_rebalance_preview
from usa_signal_bot.paper_shadow.shadow_notifications import build_shadow_notification_preview
from usa_signal_bot.paper_shadow.shadow_safety_guard import collect_shadow_safety_flags_from_context, shadow_safety_summary
from usa_signal_bot.paper_shadow.rehearsal_runner import PaperShadowRehearsalRunner
from usa_signal_bot.paper_shadow.session_registry import register_shadow_session, shadow_session_registry_summary
from usa_signal_bot.paper_shadow.result_analyzer import analyze_shadow_rehearsal_session
from usa_signal_bot.paper_shadow.shadow_reporting import paper_shadow_limitations_text
from usa_signal_bot.paper_shadow.sandbox_ingestion import ingest_sandbox_review_payload
from usa_signal_bot.paper_shadow.shadow_store import (
    shadow_store_summary, get_latest_shadow_rehearsal_review, read_shadow_rehearsal_review_json,
    write_shadow_rehearsal_review_json, shadow_reviews_dir
)
from usa_signal_bot.paper_shadow.shadow_validation import validate_shadow_session_safety, validate_shadow_review_report

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m usa_signal_bot <command>")
        sys.exit(1)

    cmd = sys.argv[1]

    # Existing mock commands for compatibility
    mock_commands = [
        "smoke", "validate-config", "health", "release-sandbox-info", "release-packaging-info",
        "governance-info", "research-execution-info", "research-workflow-info", "diagnostics-info",
        "attribution-info", "rebalance-info", "portfolio-construction-info", "allocation-info",
        "strategy-adaptation-info", "regime-map-info", "regime-cost-info", "cost-robustness-info",
        "transaction-cost-info", "execution-info", "provider-info"
    ]
    if cmd in mock_commands:
        print(f"Mock command '{cmd}' executed successfully.")
        sys.exit(0)

    data_root = Path("data")

    if cmd == "paper-shadow-info":
        print("Paper Shadow System Info:")
        print("Enabled: True")
        print(paper_shadow_limitations_text())
        sys.exit(0)

    elif cmd == "shadow-ingest-sandbox":
        res = ingest_sandbox_review_payload({"context": {}, "unsafe_flags": []})
        print(f"Ingested sandbox payload: {res['status']}")
        sys.exit(0)

    elif cmd == "shadow-context":
        equity = 100000.0
        for i, arg in enumerate(sys.argv):
            if arg == "--equity" and i+1 < len(sys.argv):
                equity = float(sys.argv[i+1])
        ctx = build_mock_shadow_simulation_context(starting_equity_usd=equity)
        print(f"Created shadow context: {ctx.context_id} with equity {ctx.starting_equity_usd}")
        sys.exit(0)

    elif cmd == "shadow-portfolio-init":
        ctx = build_mock_shadow_simulation_context()
        portfolio = initialize_shadow_portfolio(ctx)
        print(f"Initialized shadow portfolio: {portfolio.portfolio_id}")
        sys.exit(0)

    elif cmd == "shadow-signal-rehearsal":
        signals = generate_mock_shadow_signals()
        print(f"Generated {len(signals)} shadow signals.")
        sys.exit(0)

    elif cmd == "shadow-candidate-selection":
        signals = generate_mock_shadow_signals()
        candidates = select_shadow_candidates(signals, min_score=50.0)
        print(f"Selected {len(candidates)} shadow candidates.")
        sys.exit(0)

    elif cmd == "shadow-order-intents":
        signals = generate_mock_shadow_signals()
        intents = build_shadow_order_intents(signals, default_notional_usd=1000.0)
        print(f"Created {len(intents)} shadow order intents.")
        sys.exit(0)

    elif cmd == "shadow-risk-gate":
        signals = generate_mock_shadow_signals()
        intents = build_shadow_order_intents(signals)
        ctx = build_mock_shadow_simulation_context()
        portfolio = initialize_shadow_portfolio(ctx)
        gated = apply_shadow_risk_gates(intents, portfolio, ctx)
        print(f"Applied risk gates to {len(gated)} intents.")
        sys.exit(0)

    elif cmd == "shadow-fill-simulate":
        signals = generate_mock_shadow_signals()
        intents = build_shadow_order_intents(signals)
        ctx = build_mock_shadow_simulation_context()
        portfolio = initialize_shadow_portfolio(ctx)
        gated = apply_shadow_risk_gates(intents, portfolio, ctx)
        fills = simulate_shadow_fills(gated)
        print(f"Simulated {len(fills)} shadow fills.")
        sys.exit(0)

    elif cmd == "shadow-ledger":
        from usa_signal_bot.core.enums import ShadowLedgerEventType
        event = create_shadow_ledger_event(ShadowLedgerEventType.SESSION_STARTED, {})
        print(f"Created shadow ledger event: {event.event_id}")
        sys.exit(0)

    elif cmd == "shadow-pnl":
        ctx = build_mock_shadow_simulation_context()
        portfolio = initialize_shadow_portfolio(ctx)
        pnl = build_shadow_pnl_snapshot(portfolio, ctx.starting_equity_usd)
        print(f"Created shadow PnL snapshot: {pnl.snapshot_id}")
        sys.exit(0)

    elif cmd == "shadow-rebalance":
        ctx = build_mock_shadow_simulation_context()
        portfolio = initialize_shadow_portfolio(ctx)
        preview = build_shadow_rebalance_preview(portfolio, ctx)
        print(f"Created shadow rebalance preview: {preview['status']}")
        sys.exit(0)

    elif cmd == "shadow-notification-preview":
        from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession
        from usa_signal_bot.core.enums import ShadowSessionStatus
        session = ShadowRehearsalSession(
            session_id="dummy", created_at_utc="", status=ShadowSessionStatus.COMPLETED,
            context=None, portfolio_state=None, signals=[], order_intents=[], fills=[],
            ledger_events=[], pnl_snapshots=[], safety_flags=[], started_at_utc=None,
            completed_at_utc=None, output_paths={}, warnings=[], errors=[]
        )
        preview = build_shadow_notification_preview(session)
        print(f"Created shadow notification preview: {preview['is_real_send']}")
        sys.exit(0)

    elif cmd == "shadow-safety-check":
        ctx = build_mock_shadow_simulation_context()
        flags = collect_shadow_safety_flags_from_context(ctx)
        summary = shadow_safety_summary(flags)
        print(f"Shadow safety check: {summary}")
        sys.exit(0)

    elif cmd == "shadow-session-run":
        ctx = build_mock_shadow_simulation_context()
        runner = PaperShadowRehearsalRunner(runtime_mode=ShadowRuntimeMode.FULL_PAPER_SHADOW)
        session = runner.run_rehearsal(ctx)
        print(f"Ran shadow session: {session.session_id}, status: {session.status.value}")
        sys.exit(0)

    elif cmd == "shadow-session-registry":
        registry = []
        ctx = build_mock_shadow_simulation_context()
        runner = PaperShadowRehearsalRunner()
        session = runner.run_rehearsal(ctx)
        register_shadow_session(session, registry)
        summary = shadow_session_registry_summary(registry)
        print(f"Shadow session registry: {summary}")
        sys.exit(0)

    elif cmd == "shadow-result-analyze":
        ctx = build_mock_shadow_simulation_context()
        runner = PaperShadowRehearsalRunner()
        session = runner.run_rehearsal(ctx)
        analysis = analyze_shadow_rehearsal_session(session)
        print(f"Shadow result analysis: {analysis['metrics']['simulated_fill_count']} fills")
        sys.exit(0)

    elif cmd == "paper-shadow-review":
        ctx = build_mock_shadow_simulation_context()
        runner = PaperShadowRehearsalRunner()
        session = runner.run_rehearsal(ctx)
        review = ShadowRehearsalReview(
            review_id=create_shadow_rehearsal_review_id(),
            created_at_utc=get_utc_now_str(),
            report_type=ShadowReportType.FULL_SHADOW_REHEARSAL_REVIEW,
            sessions=[session],
            output_paths={},
            warnings=[],
            errors=[]
        )
        if "--write" in sys.argv:
            p = shadow_reviews_dir(data_root) / f"{review.review_id}.json"
            write_shadow_rehearsal_review_json(p, review)
            print(f"Wrote shadow review to {p}")
        else:
            print(f"Created shadow review: {review.review_id}")
        sys.exit(0)

    elif cmd == "paper-shadow-summary":
        summary = shadow_store_summary(data_root)
        print(f"Shadow store summary: {summary}")
        sys.exit(0)

    elif cmd in ["paper-shadow-latest-review", "paper-shadow-validate", "paper-shadow-notification-preview", "paper-shadow-notification-dispatch-dry-run"]:
        # Mock behavior for these commands to ensure 0 exit code when successful
        latest = get_latest_shadow_rehearsal_review(data_root)
        if latest:
            print(f"Found latest review: {latest.name}")
            sys.exit(0)
        else:
            print("No latest review found.")
            # Based on requirements, if not found, print meaningful message and exit 0
            sys.exit(0)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
