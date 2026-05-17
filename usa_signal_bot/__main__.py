"""Main entry point for the usa_signal_bot package."""
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="USA Signal Bot CLI")
    parser.add_argument('command', help='Command to execute')
    parser.add_argument('--dimension', default='symbol', help='Dimension for attribution')
    parser.add_argument('--starting-equity', type=float, default=100000.0, help='Starting equity')
    parser.add_argument('--window', default='monthly', help='Time window')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--latest-review', action='store_true')

    args = parser.parse_args()

    class DummyConfig:
        class DummyAttribution:
            enabled = True
        attribution = DummyAttribution()

    class DummyContext:
        config = DummyConfig()

    context = DummyContext()

    from usa_signal_bot.app import cli

    cmd_map = {
        'attribution-info': lambda: cli.handle_attribution_info(context),
        'normalize-trades': lambda: cli.handle_normalize_trades(context),
        'pnl-attribution': lambda: cli.handle_pnl_attribution(context, args.dimension),
        'cost-attribution': lambda: cli.handle_cost_attribution(context, args.dimension),
        'symbol-attribution': lambda: cli.handle_symbol_attribution(context),
        'strategy-attribution': lambda: cli.handle_strategy_attribution(context),
        'sector-cluster-attribution': lambda: cli.handle_sector_cluster_attribution(context),
        'regime-attribution': lambda: cli.handle_regime_attribution(context),
        'signal-contribution': lambda: cli.handle_signal_contribution(context),
        'sizing-attribution': lambda: cli.handle_sizing_attribution(context),
        'rebalance-attribution': lambda: cli.handle_rebalance_attribution(context),
        'drawdown-attribution': lambda: cli.handle_drawdown_attribution(context, args.starting_equity),
        'risk-attribution': lambda: cli.handle_risk_attribution(context, args.dimension),
        'time-window-attribution': lambda: cli.handle_time_window_attribution(context, args.window),
        'attribution-scorecard': lambda: cli.handle_attribution_scorecard(context),
        'attribution-review': lambda: cli.handle_attribution_review(context),
        'attribution-summary': lambda: cli.handle_attribution_summary(context),
        'attribution-latest-review': lambda: cli.handle_attribution_latest_review(context),
        'attribution-validate': lambda: cli.handle_attribution_validate(context),
        'attribution-notification-preview': lambda: cli.handle_attribution_notification_preview(context),
        'attribution-notification-dispatch-dry-run': lambda: cli.handle_attribution_notification_dispatch_dry_run(context),
        'smoke': lambda: 0,
        'diagnostics-info': lambda: cli.handle_diagnostics_info(),
        'diagnostics-normalize-events': lambda: cli.handle_diagnostics_normalize_events(),
        'loss-analysis': lambda: cli.handle_loss_analysis(),
        'false-signal-analysis': lambda: cli.handle_false_signal_analysis(),
        'cost-degradation-analysis': lambda: cli.handle_cost_degradation_analysis(),
        'regime-failure-analysis': lambda: cli.handle_regime_failure_analysis(),
        'liquidity-execution-failure': lambda: cli.handle_liquidity_execution_failure(),
        'sizing-failure-analysis': lambda: cli.handle_sizing_failure_analysis(),
        'rebalance-failure-analysis': lambda: cli.handle_rebalance_failure_analysis(),
        'drawdown-diagnostics': lambda: cli.handle_drawdown_diagnostics(),
        'strategy-diagnostics': lambda: cli.handle_strategy_diagnostics(),
        'signal-family-diagnostics': lambda: cli.handle_signal_family_diagnostics(),
        'symbol-cluster-diagnostics': lambda: cli.handle_symbol_cluster_diagnostics(),
        'failure-signature-mining': lambda: cli.handle_failure_signature_mining(),
        'failure-cluster-ranking': lambda: cli.handle_failure_cluster_ranking(),
        'remediation-hints': lambda: cli.handle_remediation_hints(),
        'diagnostic-scorecard': lambda: cli.handle_diagnostic_scorecard(),
        'diagnostics-review': lambda: cli.handle_diagnostics_review(),
        'diagnostics-summary': lambda: cli.handle_diagnostics_summary(),
        'diagnostics-latest-review': lambda: cli.handle_diagnostics_latest_review(),
        'diagnostics-validate': lambda: cli.handle_diagnostics_validate(),
        'diagnostics-notification-preview': lambda: cli.handle_diagnostics_notification_preview(),
        'diagnostics-notification-dispatch-dry-run': lambda: cli.handle_diagnostics_notification_dispatch_dry_run(),

    }

    if args.command in cmd_map:
        return cmd_map[args.command]()

    print(f"Executing command: {args.command}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
