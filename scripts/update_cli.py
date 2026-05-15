def update_cli():
    with open('usa_signal_bot/app/cli.py', 'r') as f:
        content = f.read()

    cli_parsers = """
    # Regime Cost Commands
    parser_rc_info = subparsers.add_parser("regime-cost-info", help="Show regime cost config")

    parser_vol_regime = subparsers.add_parser("volatility-cost-regime", help="Classify volatility regime")
    parser_vol_regime.add_argument("--atr-pct", type=float, help="ATR percentage")
    parser_vol_regime.add_argument("--gap-pct", type=float, help="Gap percentage")

    parser_liq_regime = subparsers.add_parser("liquidity-cost-regime", help="Classify liquidity regime")
    parser_liq_regime.add_argument("--adv", type=float, help="Average dollar volume")
    parser_liq_regime.add_argument("--volume", type=float, help="Average daily volume")

    parser_spr_regime = subparsers.add_parser("spread-cost-regime", help="Classify spread regime")
    parser_spr_regime.add_argument("--spread-bps", type=float, help="Spread proxy in bps")

    parser_sess_regime = subparsers.add_parser("session-cost-regime", help="Classify session regime")
    parser_sess_regime.add_argument("--session", type=str, help="Session type (regular, premarket, etc.)")

    parser_life_regime = subparsers.add_parser("lifecycle-cost-regime", help="Classify lifecycle regime")
    parser_life_regime.add_argument("--corporate-action-status", type=str, help="Status")
    parser_life_regime.add_argument("--lifecycle-status", type=str, help="Status")

    parser_comb_regime = subparsers.add_parser("combined-cost-regime", help="Classify combined regime")
    parser_comb_regime.add_argument("--symbol", type=str, default="SPY", help="Symbol")
    parser_comb_regime.add_argument("--atr-pct", type=float, help="ATR percentage")
    parser_comb_regime.add_argument("--adv", type=float, help="Average dollar volume")
    parser_comb_regime.add_argument("--spread-bps", type=float, help="Spread proxy in bps")
    parser_comb_regime.add_argument("--session", type=str, help="Session type")

    parser_curve_sel = subparsers.add_parser("cost-curve-select", help="Select cost curve")
    parser_curve_sel.add_argument("--symbol", type=str, default="SPY", help="Symbol")
    parser_curve_sel.add_argument("--atr-pct", type=float, help="ATR pct")
    parser_curve_sel.add_argument("--adv", type=float, help="ADV")
    parser_curve_sel.add_argument("--spread-bps", type=float, help="Spread bps")
    parser_curve_sel.add_argument("--write", action="store_true", help="Write to store")

    parser_adapt_dec = subparsers.add_parser("adaptive-execution-decision", help="Make adaptive execution decision")
    parser_adapt_dec.add_argument("--symbol", type=str, default="SPY", help="Symbol")
    parser_adapt_dec.add_argument("--atr-pct", type=float, help="ATR pct")
    parser_adapt_dec.add_argument("--adv", type=float, help="ADV")
    parser_adapt_dec.add_argument("--spread-bps", type=float, help="Spread bps")
    parser_adapt_dec.add_argument("--write", action="store_true", help="Write to store")

    parser_rc_brk = subparsers.add_parser("regime-cost-breakdown", help="Calculate regime cost breakdown")
    parser_rc_brk.add_argument("--symbol", type=str, default="SPY", help="Symbol")
    parser_rc_brk.add_argument("--base-cost-bps", type=float, default=50.0, help="Base cost")
    parser_rc_brk.add_argument("--atr-pct", type=float, help="ATR pct")
    parser_rc_brk.add_argument("--adv", type=float, help="ADV")
    parser_rc_brk.add_argument("--spread-bps", type=float, help="Spread bps")
    parser_rc_brk.add_argument("--write", action="store_true", help="Write to store")

    parser_rc_rev = subparsers.add_parser("regime-cost-review", help="Generate full review")
    parser_rc_rev.add_argument("--symbol", type=str, default="SPY", help="Symbol")
    parser_rc_rev.add_argument("--write", action="store_true", help="Write to store")

    parser_rc_sum = subparsers.add_parser("regime-cost-summary", help="Show store summary")
    parser_rc_latest = subparsers.add_parser("regime-cost-latest-review", help="Show latest review")

    parser_rc_val = subparsers.add_parser("regime-cost-validate", help="Validate regime cost")
    parser_rc_val.add_argument("--latest-review", action="store_true", help="Use latest review")

    parser_rc_np = subparsers.add_parser("regime-cost-notification-preview", help="Preview notification")
    parser_rc_np.add_argument("--latest-review", action="store_true", help="Use latest review")

    parser_rc_nd = subparsers.add_parser("regime-cost-notification-dispatch-dry-run", help="Dry run notification dispatch")
    parser_rc_nd.add_argument("--latest-review", action="store_true", help="Use latest review")
"""
    cli_handlers = """
    elif args.command == "regime-cost-info":
        print("Regime Cost Config: Enabled (Mock)")
        print("Disclaimer: Regime-aware cost outputs are for local backtesting realism only. NOT investment advice. PASS is not live approval.")

    elif args.command in ["volatility-cost-regime", "liquidity-cost-regime", "spread-cost-regime", "session-cost-regime", "lifecycle-cost-regime", "combined-cost-regime", "cost-curve-select", "adaptive-execution-decision", "regime-cost-breakdown", "regime-cost-review", "regime-cost-summary", "regime-cost-latest-review", "regime-cost-validate", "regime-cost-notification-preview", "regime-cost-notification-dispatch-dry-run"]:
        print(f"Executed {args.command} successfully (Mock implementation)")
"""

    if "regime-cost-info" not in content:
        content = content.replace(
            "    # Task Queue Commands",
            cli_parsers + "\n    # Task Queue Commands"
        )
        content = content.replace(
            '    elif args.command == "taskqueue-info":',
            cli_handlers + '\n    elif args.command == "taskqueue-info":'
        )
        with open('usa_signal_bot/app/cli.py', 'w') as f:
            f.write(content)

update_cli()
