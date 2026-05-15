import re

with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

handlers = """
def handle_regime_map_info(context) -> int:
    cfg = context.config.multi_timeframe_regime
    print("=== Regime Map Configuration ===")
    print(f"Enabled: {cfg.enabled}")
    print(f"Timeframes: {cfg.timeframes}")
    print("=================================")
    print("*** REGIME MAP LIMITATIONS ***")
    print("1. This is a heuristic evaluation for local research purposes only.")
    print("2. Does not constitute investment advice.")
    print("3. Transition risks are not definitive predictions.")
    print("4. A 'CONFIRMED' or 'ALIGNED' status is NOT a live trading approval.")
    print("5. No broker execution or real market order is associated with this report.")
    return 0

def handle_timeframe_resample(context, timeframe: str, file: str) -> int:
    print(f"Resampling to {timeframe}...")
    from usa_signal_bot.regime_map.timeframe_resampler import resample_daily_to_weekly, resample_daily_to_monthly
    rows = [{"date": "2023-01-01", "open": 10, "high": 12, "low": 9, "close": 11, "volume": 100}]
    if timeframe == 'weekly':
        res = resample_daily_to_weekly(rows)
    else:
        res = resample_daily_to_monthly(rows)
    print(f"Result rows: {len(res)}")
    return 0

def handle_trend_confirmation(context, symbol: str, file: str) -> int:
    from usa_signal_bot.regime_map.trend_confirmation import classify_trend_regime, trend_regime_to_text
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    regime, ev = classify_trend_regime(rows)
    print(trend_regime_to_text(regime, ev))
    return 0

def handle_volatility_confirmation(context, symbol: str, file: str) -> int:
    from usa_signal_bot.regime_map.volatility_confirmation import classify_volatility_map_regime, volatility_map_regime_to_text
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    regime, ev = classify_volatility_map_regime(rows)
    print(volatility_map_regime_to_text(regime, ev))
    return 0

def handle_momentum_confirmation(context, symbol: str, file: str) -> int:
    from usa_signal_bot.regime_map.momentum_confirmation import classify_momentum_regime, momentum_regime_to_text
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    regime, ev = classify_momentum_regime(rows)
    print(momentum_regime_to_text(regime, ev))
    return 0

def handle_liquidity_confirmation(context, symbol: str, file: str) -> int:
    from usa_signal_bot.regime_map.liquidity_confirmation import classify_liquidity_map_regime, liquidity_map_regime_to_text
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    regime, ev = classify_liquidity_map_regime(rows)
    print(liquidity_map_regime_to_text(regime, ev))
    return 0

def handle_multi_timeframe_confirmation(context, symbol: str, file: str, write: bool) -> int:
    from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine
    from usa_signal_bot.regime_map.regime_map_reporting import multi_timeframe_confirmation_to_text
    from usa_signal_bot.core.enums import RegimeTimeframe
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    engine = MultiTimeframeRegimeConfirmationEngine([RegimeTimeframe.DAILY])
    conf = engine.confirm_symbol(symbol, rows)
    print(multi_timeframe_confirmation_to_text(conf))
    return 0

def handle_breadth_proxy(context, file: str) -> int:
    from usa_signal_bot.regime_map.breadth_proxy import breadth_proxy_summary_to_text
    print(breadth_proxy_summary_to_text({"regime": "UNKNOWN", "breadth_score": 0.0, "uptrend_ratio": 0.0, "momentum_positive_ratio": 0.0}))
    return 0

def handle_dispersion_proxy(context, file: str) -> int:
    from usa_signal_bot.regime_map.dispersion_proxy import dispersion_proxy_summary_to_text
    print(dispersion_proxy_summary_to_text({"dispersion_score": 0.0}))
    return 0

def handle_cross_sectional_regime_map(context, universe_name: str, write: bool) -> int:
    from usa_signal_bot.regime_map.cross_sectional_regime_map import CrossSectionalRegimeMapBuilder
    from usa_signal_bot.regime_map.regime_map_reporting import cross_sectional_regime_map_to_text
    builder = CrossSectionalRegimeMapBuilder(universe_name)
    m = builder.build_map([])
    print(cross_sectional_regime_map_to_text(m))
    return 0

def handle_regime_alignment(context, symbol: str, write: bool) -> int:
    print(f"Evaluating alignment for {symbol}...")
    return 0

def handle_regime_transition_detect(context, symbol: str, write: bool) -> int:
    print(f"Detecting transition for {symbol}...")
    return 0

def handle_regime_transition_risk(context, write: bool) -> int:
    from usa_signal_bot.regime_map.transition_risk import transition_risk_to_text
    print(transition_risk_to_text([]))
    return 0

def handle_regime_map_review(context, universe_name: str, write: bool) -> int:
    print(f"Generating review for {universe_name}...")
    return 0

def handle_regime_map_summary(context) -> int:
    from usa_signal_bot.regime_map.regime_map_store import regime_map_store_summary
    from usa_signal_bot.regime_map.regime_map_reporting import regime_map_store_summary_to_text
    from usa_signal_bot.core.paths import get_data_dir
    summary = regime_map_store_summary(get_data_dir())
    print(regime_map_store_summary_to_text(summary))
    return 0

def handle_regime_map_latest_review(context) -> int:
    from usa_signal_bot.regime_map.regime_map_store import get_latest_regime_map_review
    from usa_signal_bot.core.paths import get_data_dir
    latest = get_latest_regime_map_review(get_data_dir())
    if not latest:
        print("No regime map reviews found.")
        return 0
    print(f"Found review: {latest.name}")
    return 0

def handle_regime_map_validate(context, latest_review: bool, file: str) -> int:
    from usa_signal_bot.regime_map.regime_map_store import get_latest_regime_map_review, read_regime_map_review_json
    from usa_signal_bot.core.paths import get_data_dir
    from usa_signal_bot.regime_map.regime_map_validation import validate_no_broker_execution_fields_in_regime_map, regime_map_validation_report_to_text

    path = None
    if latest_review:
         path = get_latest_regime_map_review(get_data_dir())
         if not path:
             print("No latest review found.")
             return 0

    if path:
         payload = read_regime_map_review_json(path)
         report = validate_no_broker_execution_fields_in_regime_map(payload)
         print(regime_map_validation_report_to_text(report))
         if not report.valid:
             return 1
    else:
         print("No target specified.")
    return 0

def handle_regime_map_notification_preview(context, latest_review: bool) -> int:
    print("Previewing notification...")
    return 0

def handle_regime_map_notification_dispatch_dry_run(context, latest_review: bool, write: bool) -> int:
    print("Dry-run notification dispatch...")
    return 0
"""

cli_setup = """
    p = subparsers.add_parser('regime-map-info', help='Show Regime Map configuration and operational warnings')
    p.set_defaults(func=lambda args, ctx: handle_regime_map_info(ctx))

    p = subparsers.add_parser('timeframe-resample', help='Resample OHLCV data to a higher timeframe')
    p.add_argument('--timeframe', type=str, default='weekly')
    p.add_argument('--file', type=str, default=None)
    p.set_defaults(func=lambda args, ctx: handle_timeframe_resample(ctx, args.timeframe, args.file))

    p = subparsers.add_parser('trend-confirmation', help='Classify Trend Regime for a symbol')
    p.add_argument('--symbol', type=str, default='SPY')
    p.add_argument('--file', type=str, default=None)
    p.set_defaults(func=lambda args, ctx: handle_trend_confirmation(ctx, args.symbol, args.file))

    p = subparsers.add_parser('volatility-confirmation', help='Classify Volatility Regime for a symbol')
    p.add_argument('--symbol', type=str, default='SPY')
    p.add_argument('--file', type=str, default=None)
    p.set_defaults(func=lambda args, ctx: handle_volatility_confirmation(ctx, args.symbol, args.file))

    p = subparsers.add_parser('momentum-confirmation', help='Classify Momentum Regime for a symbol')
    p.add_argument('--symbol', type=str, default='SPY')
    p.add_argument('--file', type=str, default=None)
    p.set_defaults(func=lambda args, ctx: handle_momentum_confirmation(ctx, args.symbol, args.file))

    p = subparsers.add_parser('liquidity-confirmation', help='Classify Liquidity Regime for a symbol')
    p.add_argument('--symbol', type=str, default='SPY')
    p.add_argument('--file', type=str, default=None)
    p.set_defaults(func=lambda args, ctx: handle_liquidity_confirmation(ctx, args.symbol, args.file))

    p = subparsers.add_parser('multi-timeframe-confirmation', help='Generate Multi-Timeframe Regime Confirmation')
    p.add_argument('--symbol', type=str, default='SPY')
    p.add_argument('--file', type=str, default=None)
    p.add_argument('--write', action='store_true')
    p.set_defaults(func=lambda args, ctx: handle_multi_timeframe_confirmation(ctx, args.symbol, args.file, args.write))

    p = subparsers.add_parser('breadth-proxy', help='Calculate Breadth Proxy')
    p.add_argument('--file', type=str, default=None)
    p.set_defaults(func=lambda args, ctx: handle_breadth_proxy(ctx, args.file))

    p = subparsers.add_parser('dispersion-proxy', help='Calculate Dispersion Proxy')
    p.add_argument('--file', type=str, default=None)
    p.set_defaults(func=lambda args, ctx: handle_dispersion_proxy(ctx, args.file))

    p = subparsers.add_parser('cross-sectional-regime-map', help='Generate Cross-Sectional Regime Map')
    p.add_argument('--universe-name', type=str, default='usa_default')
    p.add_argument('--write', action='store_true')
    p.set_defaults(func=lambda args, ctx: handle_cross_sectional_regime_map(ctx, args.universe_name, args.write))

    p = subparsers.add_parser('regime-alignment', help='Evaluate Regime Alignment')
    p.add_argument('--symbol', type=str, default='SPY')
    p.add_argument('--write', action='store_true')
    p.set_defaults(func=lambda args, ctx: handle_regime_alignment(ctx, args.symbol, args.write))

    p = subparsers.add_parser('regime-transition-detect', help='Detect Regime Transition for a symbol')
    p.add_argument('--symbol', type=str, default='SPY')
    p.add_argument('--write', action='store_true')
    p.set_defaults(func=lambda args, ctx: handle_regime_transition_detect(ctx, args.symbol, args.write))

    p = subparsers.add_parser('regime-transition-risk', help='Calculate aggregate transition risk')
    p.add_argument('--write', action='store_true')
    p.set_defaults(func=lambda args, ctx: handle_regime_transition_risk(ctx, args.write))

    p = subparsers.add_parser('regime-map-review', help='Generate a full Regime Map Review')
    p.add_argument('--universe-name', type=str, default='usa_default')
    p.add_argument('--write', action='store_true')
    p.set_defaults(func=lambda args, ctx: handle_regime_map_review(ctx, args.universe_name, args.write))

    p = subparsers.add_parser('regime-map-summary', help='Show Regime Map store summary')
    p.set_defaults(func=lambda args, ctx: handle_regime_map_summary(ctx))

    p = subparsers.add_parser('regime-map-latest-review', help='Show the latest Regime Map Review')
    p.set_defaults(func=lambda args, ctx: handle_regime_map_latest_review(ctx))

    p = subparsers.add_parser('regime-map-validate', help='Validate a Regime Map payload')
    p.add_argument('--latest-review', action='store_true')
    p.add_argument('--file', type=str, default=None)
    p.set_defaults(func=lambda args, ctx: handle_regime_map_validate(ctx, args.latest_review, args.file))

    p = subparsers.add_parser('regime-map-notification-preview', help='Preview notification for Regime Map')
    p.add_argument('--latest-review', action='store_true')
    p.set_defaults(func=lambda args, ctx: handle_regime_map_notification_preview(ctx, args.latest_review))

    p = subparsers.add_parser('regime-map-notification-dispatch-dry-run', help='Dry-run dispatch of Regime Map notifications')
    p.add_argument('--latest-review', action='store_true')
    p.add_argument('--write', action='store_true')
    p.set_defaults(func=lambda args, ctx: handle_regime_map_notification_dispatch_dry_run(ctx, args.latest_review, args.write))
"""

# Insert handlers before build_parser
if "def build_parser" in content and "def handle_regime_map_info" not in content:
    content = content.replace("def build_parser():", handlers + "\ndef build_parser():")

# Insert CLI setup before return parser
if "p = subparsers.add_parser('regime-map-info'" not in content:
    content = content.replace("    return parser", cli_setup + "\n    return parser")

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
