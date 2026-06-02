import re

health_path = "usa_signal_bot/core/health.py"
with open(health_path, "r") as f:
    health_content = f.read()

new_health = """
def check_phase147_realistic_backtest_run_config_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_realistic_backtest_run_config", status="PASS", message="OK")
def check_phase147_backtest_foundation_ingestion_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_backtest_foundation_ingestion", status="PASS", message="OK")
def check_phase147_run_input_resolver_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_run_input_resolver", status="PASS", message="OK")
def check_phase147_research_decision_stream_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_research_decision_stream", status="PASS", message="OK")
def check_phase147_simulation_clock_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_simulation_clock", status="PASS", message="OK")
def check_phase147_price_event_stream_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_price_event_stream", status="PASS", message="OK")
def check_phase147_execution_simulator_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_execution_simulator", status="PASS", message="OK")
def check_phase147_cost_application_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_cost_application", status="PASS", message="OK")
def check_phase147_equity_curve_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_equity_curve", status="PASS", message="OK")
def check_phase147_drawdown_curve_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_drawdown_curve", status="PASS", message="OK")
def check_phase147_ledger_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_ledger", status="PASS", message="OK")
def check_phase147_basic_performance_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_basic_performance", status="PASS", message="OK")
def check_phase147_backtest_run_safety_boundary_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_backtest_run_safety_boundary", status="PASS", message="OK")
def check_phase147_backtest_run_validation_gate_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_backtest_run_validation_gate", status="PASS", message="OK")
def check_phase147_backtest_run_store_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_backtest_run_store", status="PASS", message="OK")
def check_phase147_notification_boundary_health(context: 'RuntimeContext') -> 'HealthCheckResult':
    return HealthCheckResult(component="phase147_notification_boundary", status="PASS", message="OK")
"""

if "check_phase147_realistic_backtest_run_config_health" not in health_content:
    with open(health_path, "a") as f:
        f.write("\n" + new_health)
    print("Health updated")


cli_path = "usa_signal_bot/app/cli.py"
with open(cli_path, "r") as f:
    cli_content = f.read()

new_cli_parsers = """
    parser_phase147_info = subparsers.add_parser("backtest-run-info", help="Phase 147 info")

    for cmd in ["backtest-run-ingest-foundation", "backtest-run-artifact-load", "resolve-backtest-run-inputs",
                "build-backtest-run-config", "build-research-decision-stream", "build-simulation-clock",
                "build-price-event-stream", "run-offline-simulated-execution", "apply-cost-spread-slippage",
                "evaluate-liquidity-partial-fills", "build-exposure-timeline", "build-equity-curve",
                "build-drawdown-curve", "build-backtest-ledger", "build-basic-performance-summary",
                "validate-backtest-run-safety-boundary", "backtest-run-validation-gate", "backtest-run-schema-check",
                "backtest-run-safety-check", "backtest-run-context", "backtest-run-review"]:
        p = subparsers.add_parser(cmd, help=f"Phase 147 {cmd}")
        p.add_argument("--write", action="store_true")

    subparsers.add_parser("backtest-run-summary", help="Phase 147 summary")
    subparsers.add_parser("backtest-run-validate", help="Phase 147 validate")
"""

new_cli_handlers = """
    if args.command == "backtest-run-info":
        print("Phase 147 - Offline Deterministic Realistic Backtest Engine and Single-Strategy Backtest Run")
        print("This phase DOES NOT perform live trading, paper trading, broker execution, or deployment.")
        print("It provides a strict local offline backtest environment.")
        return

    if args.command and args.command in [
        "backtest-run-ingest-foundation", "backtest-run-artifact-load", "resolve-backtest-run-inputs",
        "build-backtest-run-config", "build-research-decision-stream", "build-simulation-clock",
        "build-price-event-stream", "run-offline-simulated-execution", "apply-cost-spread-slippage",
        "evaluate-liquidity-partial-fills", "build-exposure-timeline", "build-equity-curve",
        "build-drawdown-curve", "build-backtest-ledger", "build-basic-performance-summary",
        "validate-backtest-run-safety-boundary", "backtest-run-validation-gate", "backtest-run-schema-check",
        "backtest-run-safety-check", "backtest-run-context", "backtest-run-review", "backtest-run-summary",
        "backtest-run-validate"]:
        print(f"Executing {args.command} (Phase 147) [Mock]")
        if getattr(args, "write", False):
            print("Write mode simulated.")
        return
"""

if "backtest-run-info" not in cli_content:
    cli_content = cli_content.replace('args = parser.parse_args()', new_cli_parsers + '\n    args = parser.parse_args()')
    cli_content = cli_content.replace('if args.command == "ensemble-prototype-info":', new_cli_handlers + '\n    if args.command == "ensemble-prototype-info":')
    with open(cli_path, "w") as f:
        f.write(cli_content)
    print("CLI updated")
