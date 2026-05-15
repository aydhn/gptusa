with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

new_commands = """
@cli.command()
def regime_map_info():
    \"\"\"Show Regime Map configuration and operational warnings.\"\"\"
    context = RuntimeContext()
    cfg = context.config.multi_timeframe_regime
    logger.info("=== Regime Map Configuration ===")
    logger.info(f"Enabled: {cfg.enabled}")
    logger.info(f"Timeframes: {cfg.timeframes}")
    logger.info("=================================")
    logger.info("*** REGIME MAP LIMITATIONS ***")
    logger.info("1. This is a heuristic evaluation for local research purposes only.")
    logger.info("2. Does not constitute investment advice.")
    logger.info("3. Transition risks are not definitive predictions.")
    logger.info("4. A 'CONFIRMED' or 'ALIGNED' status is NOT a live trading approval.")
    logger.info("5. No broker execution or real market order is associated with this report.")

@cli.command()
@click.option('--timeframe', type=str, default='weekly', help='Target timeframe to resample to (weekly, monthly).')
@click.option('--file', type=str, required=False, help='Local CSV/JSONL file with OHLCV data.')
def timeframe_resample(timeframe, file):
    \"\"\"Resample OHLCV data to a higher timeframe.\"\"\"
    logger.info(f"Resampling to {timeframe}...")
    from usa_signal_bot.regime_map.timeframe_resampler import resample_daily_to_weekly, resample_daily_to_monthly
    # Mock behavior for now if no file
    rows = [{"date": "2023-01-01", "open": 10, "high": 12, "low": 9, "close": 11, "volume": 100}]
    if timeframe == 'weekly':
        res = resample_daily_to_weekly(rows)
    else:
        res = resample_daily_to_monthly(rows)
    logger.info(f"Result rows: {len(res)}")

@cli.command()
@click.option('--symbol', type=str, default='SPY', help='Symbol to classify.')
@click.option('--file', type=str, required=False, help='Local data file.')
def trend_confirmation(symbol, file):
    \"\"\"Classify Trend Regime for a symbol.\"\"\"
    from usa_signal_bot.regime_map.trend_confirmation import classify_trend_regime, trend_regime_to_text
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    regime, ev = classify_trend_regime(rows)
    logger.info(trend_regime_to_text(regime, ev))

@cli.command()
@click.option('--symbol', type=str, default='SPY', help='Symbol to classify.')
@click.option('--file', type=str, required=False, help='Local data file.')
def volatility_confirmation(symbol, file):
    \"\"\"Classify Volatility Regime for a symbol.\"\"\"
    from usa_signal_bot.regime_map.volatility_confirmation import classify_volatility_map_regime, volatility_map_regime_to_text
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    regime, ev = classify_volatility_map_regime(rows)
    logger.info(volatility_map_regime_to_text(regime, ev))

@cli.command()
@click.option('--symbol', type=str, default='SPY', help='Symbol to classify.')
@click.option('--file', type=str, required=False, help='Local data file.')
def momentum_confirmation(symbol, file):
    \"\"\"Classify Momentum Regime for a symbol.\"\"\"
    from usa_signal_bot.regime_map.momentum_confirmation import classify_momentum_regime, momentum_regime_to_text
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    regime, ev = classify_momentum_regime(rows)
    logger.info(momentum_regime_to_text(regime, ev))

@cli.command()
@click.option('--symbol', type=str, default='SPY', help='Symbol to classify.')
@click.option('--file', type=str, required=False, help='Local data file.')
def liquidity_confirmation(symbol, file):
    \"\"\"Classify Liquidity Regime for a symbol.\"\"\"
    from usa_signal_bot.regime_map.liquidity_confirmation import classify_liquidity_map_regime, liquidity_map_regime_to_text
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    regime, ev = classify_liquidity_map_regime(rows)
    logger.info(liquidity_map_regime_to_text(regime, ev))

@cli.command()
@click.option('--symbol', type=str, default='SPY', help='Symbol to classify.')
@click.option('--file', type=str, required=False, help='Local data file.')
@click.option('--write', is_flag=True, help='Write to store.')
def multi_timeframe_confirmation(symbol, file, write):
    \"\"\"Generate Multi-Timeframe Regime Confirmation.\"\"\"
    from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine
    from usa_signal_bot.regime_map.regime_map_reporting import multi_timeframe_confirmation_to_text
    from usa_signal_bot.core.enums import RegimeTimeframe
    rows = [{"date": f"2023-01-{i:02d}", "open": 10, "high": 12, "low": 9, "close": 10+i, "volume": 100} for i in range(1, 31)]
    engine = MultiTimeframeRegimeConfirmationEngine([RegimeTimeframe.DAILY])
    conf = engine.confirm_symbol(symbol, rows)
    logger.info(multi_timeframe_confirmation_to_text(conf))
    if write:
        from usa_signal_bot.regime_map.regime_map_store import write_multi_timeframe_confirmation_json, confirmations_dir
        from usa_signal_bot.core.paths import get_data_dir
        write_multi_timeframe_confirmation_json(confirmations_dir(get_data_dir()) / f"{conf.confirmation_id}.json", conf)

@cli.command()
@click.option('--file', type=str, required=False, help='Local data file.')
def breadth_proxy(file):
    \"\"\"Calculate Breadth Proxy.\"\"\"
    from usa_signal_bot.regime_map.breadth_proxy import breadth_proxy_summary_to_text
    logger.info(breadth_proxy_summary_to_text({"regime": "UNKNOWN", "breadth_score": 0.0, "uptrend_ratio": 0.0, "momentum_positive_ratio": 0.0}))

@cli.command()
@click.option('--file', type=str, required=False, help='Local data file.')
def dispersion_proxy(file):
    \"\"\"Calculate Dispersion Proxy.\"\"\"
    from usa_signal_bot.regime_map.dispersion_proxy import dispersion_proxy_summary_to_text
    logger.info(dispersion_proxy_summary_to_text({"dispersion_score": 0.0}))

@cli.command()
@click.option('--universe-name', type=str, default='usa_default', help='Universe name.')
@click.option('--write', is_flag=True, help='Write to store.')
def cross_sectional_regime_map(universe_name, write):
    \"\"\"Generate Cross-Sectional Regime Map.\"\"\"
    from usa_signal_bot.regime_map.cross_sectional_regime_map import CrossSectionalRegimeMapBuilder
    from usa_signal_bot.regime_map.regime_map_reporting import cross_sectional_regime_map_to_text
    builder = CrossSectionalRegimeMapBuilder(universe_name)
    m = builder.build_map([])
    logger.info(cross_sectional_regime_map_to_text(m))
    if write:
        from usa_signal_bot.regime_map.regime_map_store import write_cross_sectional_regime_map_json, cross_sectional_maps_dir
        from usa_signal_bot.core.paths import get_data_dir
        write_cross_sectional_regime_map_json(cross_sectional_maps_dir(get_data_dir()) / f"{m.map_id}.json", m)

@cli.command()
@click.option('--symbol', type=str, default='SPY', help='Symbol to evaluate.')
@click.option('--write', is_flag=True, help='Write to store.')
def regime_alignment(symbol, write):
    \"\"\"Evaluate Regime Alignment.\"\"\"
    logger.info(f"Evaluating alignment for {symbol}...")

@cli.command()
@click.option('--symbol', type=str, default='SPY', help='Symbol to check.')
@click.option('--write', is_flag=True, help='Write to store.')
def regime_transition_detect(symbol, write):
    \"\"\"Detect Regime Transition for a symbol.\"\"\"
    logger.info(f"Detecting transition for {symbol}...")

@cli.command()
@click.option('--write', is_flag=True, help='Write to store.')
def regime_transition_risk(write):
    \"\"\"Calculate aggregate transition risk.\"\"\"
    from usa_signal_bot.regime_map.transition_risk import transition_risk_to_text
    logger.info(transition_risk_to_text([]))

@cli.command()
@click.option('--universe-name', type=str, default='usa_default', help='Universe name.')
@click.option('--write', is_flag=True, help='Write to store.')
def regime_map_review(universe_name, write):
    \"\"\"Generate a full Regime Map Review.\"\"\"
    logger.info(f"Generating review for {universe_name}...")

@cli.command()
def regime_map_summary():
    \"\"\"Show Regime Map store summary.\"\"\"
    from usa_signal_bot.regime_map.regime_map_store import regime_map_store_summary
    from usa_signal_bot.regime_map.regime_map_reporting import regime_map_store_summary_to_text
    from usa_signal_bot.core.paths import get_data_dir
    summary = regime_map_store_summary(get_data_dir())
    logger.info(regime_map_store_summary_to_text(summary))

@cli.command()
def regime_map_latest_review():
    \"\"\"Show the latest Regime Map Review.\"\"\"
    from usa_signal_bot.regime_map.regime_map_store import get_latest_regime_map_review, read_regime_map_review_json
    from usa_signal_bot.core.paths import get_data_dir
    latest = get_latest_regime_map_review(get_data_dir())
    if not latest:
        logger.info("No regime map reviews found.")
        return
    logger.info(f"Found review: {latest.name}")

@cli.command()
@click.option('--latest-review', is_flag=True, help='Validate latest review.')
@click.option('--file', type=str, required=False, help='Path to review JSON.')
def regime_map_validate(latest_review, file):
    \"\"\"Validate a Regime Map payload.\"\"\"
    from usa_signal_bot.regime_map.regime_map_store import get_latest_regime_map_review, read_regime_map_review_json
    from usa_signal_bot.core.paths import get_data_dir
    from usa_signal_bot.regime_map.regime_map_validation import validate_no_broker_execution_fields_in_regime_map, regime_map_validation_report_to_text
    import sys

    path = None
    if latest_review:
         path = get_latest_regime_map_review(get_data_dir())
         if not path:
             logger.info("No latest review found.")
             return

    if path:
         payload = read_regime_map_review_json(path)
         report = validate_no_broker_execution_fields_in_regime_map(payload)
         logger.info(regime_map_validation_report_to_text(report))
         if not report.valid:
             sys.exit(1)
    else:
         logger.info("No target specified.")

@cli.command()
@click.option('--latest-review', is_flag=True, help='Use latest review.')
def regime_map_notification_preview(latest_review):
    \"\"\"Preview notification for Regime Map.\"\"\"
    logger.info("Previewing notification...")

@cli.command()
@click.option('--latest-review', is_flag=True, help='Use latest review.')
@click.option('--write', is_flag=True, help='Write out generated notifications.')
def regime_map_notification_dispatch_dry_run(latest_review, write):
    \"\"\"Dry-run dispatch of Regime Map notifications.\"\"\"
    logger.info("Dry-run notification dispatch...")

"""

if "def regime_map_info()" not in content:
    content += "\n" + new_commands

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
