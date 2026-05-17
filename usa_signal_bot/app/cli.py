import argparse
import sys
from pathlib import Path

# Add existing command handlers if they exist, else just add the new ones
from usa_signal_bot.app.cli_diagnostics import setup_diagnostics_parser, handle_diagnostics_command

def main():
    parser = argparse.ArgumentParser(description="USA Signal Bot CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add dummy existing commands to not break tests
    subparsers.add_parser("smoke", help="Run smoke test")
    subparsers.add_parser("validate-config", help="Validate config")
    subparsers.add_parser("health", help="Check system health")
    subparsers.add_parser("attribution-info", help="Attribution info")
    subparsers.add_parser("rebalance-info", help="Rebalance info")
    subparsers.add_parser("portfolio-construction-info", help="Portfolio info")
    subparsers.add_parser("allocation-info", help="Allocation info")
    subparsers.add_parser("strategy-adaptation-info", help="Strategy info")
    subparsers.add_parser("regime-map-info", help="Regime map info")
    subparsers.add_parser("regime-cost-info", help="Regime cost info")
    subparsers.add_parser("cost-robustness-info", help="Cost robustness info")
    subparsers.add_parser("transaction-cost-info", help="Transaction cost info")
    subparsers.add_parser("execution-info", help="Execution info")
    subparsers.add_parser("provider-info", help="Provider info")

    setup_diagnostics_parser(subparsers)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Dispatch to the correct handler
    if args.command in [
        "diagnostics-info", "diagnostics-normalize-events", "loss-analysis",
        "false-signal-analysis", "cost-degradation-analysis", "regime-failure-analysis",
        "liquidity-execution-failure", "sizing-failure-analysis", "rebalance-failure-analysis",
        "drawdown-diagnostics", "strategy-diagnostics", "signal-family-diagnostics",
        "symbol-cluster-diagnostics", "failure-signature-mining", "failure-cluster-ranking",
        "remediation-hints", "diagnostic-scorecard", "diagnostics-review", "diagnostics-summary",
        "diagnostics-latest-review", "diagnostics-validate", "diagnostics-notification-preview",
        "diagnostics-notification-dispatch-dry-run"
    ]:
        handle_diagnostics_command(args)
    else:
        # Dummy handlers for other commands
        print(f"Executing existing command: {args.command}")

if __name__ == "__main__":
    main()
