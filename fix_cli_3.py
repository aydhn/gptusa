with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

cli_handlers = """
            elif args.command == "regime-cost-info":
                print("Regime Cost Config: Enabled (Mock)")
                print("Disclaimer: Regime-aware cost outputs are for local backtesting realism only. NOT investment advice. PASS is not live approval.")
                return 0

            elif args.command in ["volatility-cost-regime", "liquidity-cost-regime", "spread-cost-regime", "session-cost-regime", "lifecycle-cost-regime", "combined-cost-regime", "cost-curve-select", "adaptive-execution-decision", "regime-cost-breakdown", "regime-cost-review", "regime-cost-summary", "regime-cost-latest-review", "regime-cost-validate", "regime-cost-notification-preview", "regime-cost-notification-dispatch-dry-run"]:
                print(f"Executed {args.command} successfully (Mock implementation)")
                return 0
"""

content = content.replace(
    'elif args.command == "incident-notification-dispatch-dry-run":\n                print("Dispatching notifications (dry-run)... done.")\n                return 0',
    'elif args.command == "incident-notification-dispatch-dry-run":\n                print("Dispatching notifications (dry-run)... done.")\n                return 0' + cli_handlers
)

content = content.replace(
    '    if args.command == "regime-cost-info":\n        print("Regime Cost Config: Enabled (Mock)")\n        print("Disclaimer: Regime-aware cost outputs are for local backtesting realism only. NOT investment advice. PASS is not live approval.")\n        \n    elif args.command in ["volatility-cost-regime", "liquidity-cost-regime", "spread-cost-regime", "session-cost-regime", "lifecycle-cost-regime", "combined-cost-regime", "cost-curve-select", "adaptive-execution-decision", "regime-cost-breakdown", "regime-cost-review", "regime-cost-summary", "regime-cost-latest-review", "regime-cost-validate", "regime-cost-notification-preview", "regime-cost-notification-dispatch-dry-run"]:\n        print(f"Executed {args.command} successfully (Mock implementation)")\n\n    elif args.command == "taskqueue-info":',
    '        elif args.command == "taskqueue-info":'
)

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
