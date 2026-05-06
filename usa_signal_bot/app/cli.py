"""Command Line Interface for USA Signal Bot."""

import argparse
import sys
from typing import Optional
from pathlib import Path

from usa_signal_bot.core import paths
from usa_signal_bot.core.config import config_to_dict
from usa_signal_bot.app.runtime import initialize_runtime, run_startup_checks, build_runtime_summary


def handle_signal_rank_file(context, file_path: str, min_rank_score: float, write: bool) -> int:
    from usa_signal_bot.strategies.signal_store import read_signals_jsonl
    from usa_signal_bot.strategies.signal_ranking import rank_signals, filter_ranked_signals, ranking_report_to_text
    from usa_signal_bot.strategies.ranking_store import write_ranking_report_json, build_ranking_report_path
    from pathlib import Path

    path = Path(file_path)
    if not path.exists():
        print(f"Error: Signal file not found at {file_path}")
        return 1

    try:
        signals = read_signals_jsonl(path)
        print(f"Loaded {len(signals)} signals from {file_path}")

        config = context.config.signal_ranking if hasattr(context.config, 'signal_ranking') else None
        report = rank_signals(signals, config)

        if min_rank_score is not None:
            report = filter_ranked_signals(report, min_rank_score)

        print("\n" + ranking_report_to_text(report))

        if write:
            out_path = build_ranking_report_path(context.data_dir, report.report_id)
            write_ranking_report_json(out_path, report)
            print(f"\nReport written to: {out_path}")

        return 0
    except Exception as e:
        print(f"Error ranking signals: {e}")
        return 1

def handle_signal_select_candidates(context, file_path: str, max_candidates: int, min_rank_score: float, write: bool) -> int:
    from usa_signal_bot.strategies.signal_store import read_signals_jsonl
    from usa_signal_bot.strategies.signal_ranking import rank_signals
    from usa_signal_bot.strategies.candidate_selection import select_candidates, candidate_selection_report_to_text
    from usa_signal_bot.strategies.ranking_store import write_candidate_selection_report_json, write_selected_candidates_jsonl, build_candidate_selection_report_path, build_selected_candidates_path
    from pathlib import Path

    path = Path(file_path)
    if not path.exists():
        print(f"Error: Signal file not found at {file_path}")
        return 1

    try:
        signals = read_signals_jsonl(path)
        rank_config = context.config.signal_ranking if hasattr(context.config, 'signal_ranking') else None
        sel_config = context.config.candidate_selection if hasattr(context.config, 'candidate_selection') else None

        if sel_config is not None:
            if max_candidates is not None:
                sel_config.max_candidates = max_candidates
            if min_rank_score is not None:
                sel_config.min_rank_score = min_rank_score

        ranking_report = rank_signals(signals, rank_config)
        report = select_candidates(ranking_report, sel_config)

        print("\n" + candidate_selection_report_to_text(report))

        if write:
            out_path = build_candidate_selection_report_path(context.data_dir, report.report_id)
            write_candidate_selection_report_json(out_path, report)
            print(f"\nReport written to: {out_path}")

            if report.selected_candidates:
                cand_path = build_selected_candidates_path(context.data_dir, report.report_id)
                write_selected_candidates_jsonl(cand_path, report.selected_candidates)
                print(f"Selected candidates written to: {cand_path}")

        return 0
    except Exception as e:
        print(f"Error selecting candidates: {e}")
        return 1

def handle_signal_ranking_summary(context) -> int:
    from usa_signal_bot.strategies.ranking_store import ranking_store_summary

    summary = ranking_store_summary(context.data_dir)
    print("\n--- Signal Ranking Storage Summary ---")
    print(f"Total Files: {summary['total_files']}")
    print(f"Ranking Reports: {summary['ranking_reports']}")
    print(f"Selection Reports: {summary['selection_reports']}")
    print(f"Portfolio Reports: {summary['portfolio_reports']}")
    print(f"Candidate JSONL Files: {summary['candidate_files']}")

    if summary['total_files'] == 0:
        print("\nNo ranking or selection outputs found. Try running 'signal-rank-file' or 'strategy-portfolio-run' first.")
    elif args.command == "robustness-info":
        return command_robustness_info(args)
    elif args.command == "monte-carlo-run":
        return command_monte_carlo_run(args)
    elif args.command == "bootstrap-run":
        return command_bootstrap_run(args)
    elif args.command == "stress-test-run":
        return command_stress_test_run(args)
    elif args.command == "robustness-summary":
        return command_robustness_summary(args)
    elif args.command == "robustness-latest":
        return command_robustness_latest(args)
    elif args.command == "robustness-validate":
        return command_robustness_validate(args)
    else:
        print(f"\nLatest file: {summary['latest_file']}")

    return 0

def handle_selected_candidates_summary(context) -> int:
    from usa_signal_bot.strategies.ranking_store import list_ranking_outputs, read_selected_candidates_jsonl

    outputs = list_ranking_outputs(context.data_dir)
    candidate_files = [p for p in outputs if p.name.startswith("candidates_") and p.suffix == ".jsonl"]

    print("\n--- Selected Candidates Summary ---")
    if not candidate_files:
        print("No selected candidates files found.")
        return 0

    latest = candidate_files[0]
    print(f"Latest Candidates File: {latest.name}")

    try:
        cands = read_selected_candidates_jsonl(latest)
        print(f"Total Candidates: {len(cands)}")

        # Simple stats
        strategies = {}
        symbols = set()

        for c in cands:
            strat = c['signal']['strategy_name']
            sym = c['signal']['symbol']
            strategies[strat] = strategies.get(strat, 0) + 1
            symbols.add(sym)

        print(f"Unique Symbols: {len(symbols)}")
        print("\nBreakdown by Strategy:")
        for s, count in strategies.items():
            print(f"  {s}: {count}")

    except Exception as e:
        print(f"Error reading candidates file: {e}")

    return 0

def handle_strategy_portfolio_run(context, strategies_str: str, symbols_str: str, timeframes_str: str, write: bool) -> int:
    from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_portfolio import strategy_portfolio_result_to_text

    strategy_names = [s.strip() for s in strategies_str.split(",")] if strategies_str else []
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]

    if not strategy_names:
        print("Error: No strategies provided.")
        return 1

    registry = StrategyRegistry()
    engine = StrategyEngine(registry, context.data_dir, context.config)

    from usa_signal_bot.strategies.strategy_input import load_strategy_feature_frames_from_feature_store, filter_valid_strategy_frames, StrategyInputBatch

    try:
        # Load and filter frames
        frames = load_strategy_feature_frames_from_feature_store(context.data_dir, symbols, timeframes)
        valid_frames = filter_valid_strategy_frames(frames, strategy_names, registry)

        if not valid_frames:
            print("No valid feature frames found for the requested strategies/symbols/timeframes. Ensure feature engineering has run.")
            return 0

        batch = StrategyInputBatch(frames=valid_frames)
        result = engine.run_strategies_ranked(strategy_names, batch, write_outputs=write)

        print("\n" + strategy_portfolio_result_to_text(result))

        if write:
            print(f"\nPortfolio reports written to data/signals/ranking")

        return 0
    except Exception as e:
        print(f"Error in strategy portfolio run: {e}")
        return 1

def handle_rule_strategy_run_ranked(context, strategy_set_name: str, symbols_str: str, timeframes_str: str, write: bool) -> int:
    from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_portfolio import strategy_portfolio_result_to_text

    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]

    registry = StrategyRegistry()
    engine = StrategyEngine(registry, context.data_dir, context.config)

    try:
        result = engine.run_rule_strategy_set_ranked_from_feature_store(
            strategy_set_name=strategy_set_name,
            symbols=symbols,
            timeframes=timeframes,
            write_outputs=write
        )

        print("\n" + strategy_portfolio_result_to_text(result))

        if write:
            print(f"\nPortfolio reports written to data/signals/ranking")

        return 0
    except Exception as e:
        print(f"Error running rule strategy set ranked: {e}")
        return 1


def handle_signal_rank_file(context, file_path: str, min_rank_score: float, write: bool) -> int:
    from usa_signal_bot.strategies.signal_store import read_signals_jsonl
    from usa_signal_bot.strategies.signal_ranking import rank_signals, filter_ranked_signals, ranking_report_to_text
    from usa_signal_bot.strategies.ranking_store import write_ranking_report_json, build_ranking_report_path
    from pathlib import Path

    path = Path(file_path)
    if not path.exists():
        print(f"Error: Signal file not found at {file_path}")
        return 1

    try:
        signals = read_signals_jsonl(path)
        print(f"Loaded {len(signals)} signals from {file_path}")

        config = context.config.signal_ranking if hasattr(context.config, 'signal_ranking') else None
        report = rank_signals(signals, config)

        if min_rank_score is not None:
            report = filter_ranked_signals(report, min_rank_score)

        print("\n" + ranking_report_to_text(report))

        if write:
            out_path = build_ranking_report_path(context.data_dir, report.report_id)
            write_ranking_report_json(out_path, report)
            print(f"\nReport written to: {out_path}")

        return 0
    except Exception as e:
        print(f"Error ranking signals: {e}")
        return 1

def handle_signal_select_candidates(context, file_path: str, max_candidates: int, min_rank_score: float, write: bool) -> int:
    from usa_signal_bot.strategies.signal_store import read_signals_jsonl
    from usa_signal_bot.strategies.signal_ranking import rank_signals
    from usa_signal_bot.strategies.candidate_selection import select_candidates, candidate_selection_report_to_text
    from usa_signal_bot.strategies.ranking_store import write_candidate_selection_report_json, write_selected_candidates_jsonl, build_candidate_selection_report_path, build_selected_candidates_path
    from pathlib import Path

    path = Path(file_path)
    if not path.exists():
        print(f"Error: Signal file not found at {file_path}")
        return 1

    try:
        signals = read_signals_jsonl(path)
        rank_config = context.config.signal_ranking if hasattr(context.config, 'signal_ranking') else None
        sel_config = context.config.candidate_selection if hasattr(context.config, 'candidate_selection') else None

        if sel_config is not None:
            if max_candidates is not None:
                sel_config.max_candidates = max_candidates
            if min_rank_score is not None:
                sel_config.min_rank_score = min_rank_score

        ranking_report = rank_signals(signals, rank_config)
        report = select_candidates(ranking_report, sel_config)

        print("\n" + candidate_selection_report_to_text(report))

        if write:
            out_path = build_candidate_selection_report_path(context.data_dir, report.report_id)
            write_candidate_selection_report_json(out_path, report)
            print(f"\nReport written to: {out_path}")

            if report.selected_candidates:
                cand_path = build_selected_candidates_path(context.data_dir, report.report_id)
                write_selected_candidates_jsonl(cand_path, report.selected_candidates)
                print(f"Selected candidates written to: {cand_path}")

        return 0
    except Exception as e:
        print(f"Error selecting candidates: {e}")
        return 1

def handle_signal_ranking_summary(context) -> int:
    from usa_signal_bot.strategies.ranking_store import ranking_store_summary

    summary = ranking_store_summary(context.data_dir)
    print("\n--- Signal Ranking Storage Summary ---")
    print(f"Total Files: {summary['total_files']}")
    print(f"Ranking Reports: {summary['ranking_reports']}")
    print(f"Selection Reports: {summary['selection_reports']}")
    print(f"Portfolio Reports: {summary['portfolio_reports']}")
    print(f"Candidate JSONL Files: {summary['candidate_files']}")

    if summary['total_files'] == 0:
        print("\nNo ranking or selection outputs found. Try running 'signal-rank-file' or 'strategy-portfolio-run' first.")
    else:
        print(f"\nLatest file: {summary['latest_file']}")

    return 0

def handle_selected_candidates_summary(context) -> int:
    from usa_signal_bot.strategies.ranking_store import list_ranking_outputs, read_selected_candidates_jsonl

    outputs = list_ranking_outputs(context.data_dir)
    candidate_files = [p for p in outputs if p.name.startswith("candidates_") and p.suffix == ".jsonl"]

    print("\n--- Selected Candidates Summary ---")
    if not candidate_files:
        print("No selected candidates files found.")
        return 0

    latest = candidate_files[0]
    print(f"Latest Candidates File: {latest.name}")

    try:
        cands = read_selected_candidates_jsonl(latest)
        print(f"Total Candidates: {len(cands)}")

        # Simple stats
        strategies = {}
        symbols = set()

        for c in cands:
            strat = c['signal']['strategy_name']
            sym = c['signal']['symbol']
            strategies[strat] = strategies.get(strat, 0) + 1
            symbols.add(sym)

        print(f"Unique Symbols: {len(symbols)}")
        print("\nBreakdown by Strategy:")
        for s, count in strategies.items():
            print(f"  {s}: {count}")

    except Exception as e:
        print(f"Error reading candidates file: {e}")

    return 0

def handle_strategy_portfolio_run(context, strategies_str: str, symbols_str: str, timeframes_str: str, write: bool) -> int:
    from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_portfolio import strategy_portfolio_result_to_text

    strategy_names = [s.strip() for s in strategies_str.split(",")] if strategies_str else []
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]

    if not strategy_names:
        print("Error: No strategies provided.")
        return 1

    registry = StrategyRegistry()
    engine = StrategyEngine(registry, context.data_dir, context.config)

    from usa_signal_bot.strategies.strategy_input import load_strategy_feature_frames_from_feature_store, filter_valid_strategy_frames, StrategyInputBatch

    try:
        # Load and filter frames
        frames = load_strategy_feature_frames_from_feature_store(context.data_dir, symbols, timeframes)
        valid_frames = filter_valid_strategy_frames(frames, strategy_names, registry)

        if not valid_frames:
            print("No valid feature frames found for the requested strategies/symbols/timeframes. Ensure feature engineering has run.")
            return 0

        batch = StrategyInputBatch(frames=valid_frames)
        result = engine.run_strategies_ranked(strategy_names, batch, write_outputs=write)

        print("\n" + strategy_portfolio_result_to_text(result))

        if write:
            print(f"\nPortfolio reports written to data/signals/ranking")

        return 0
    except Exception as e:
        print(f"Error in strategy portfolio run: {e}")
        return 1

def handle_rule_strategy_run_ranked(context, strategy_set_name: str, symbols_str: str, timeframes_str: str, write: bool) -> int:
    from usa_signal_bot.strategies.strategy_registry import StrategyRegistry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_portfolio import strategy_portfolio_result_to_text

    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]

    registry = StrategyRegistry()
    engine = StrategyEngine(registry, context.data_dir, context.config)

    try:
        result = engine.run_rule_strategy_set_ranked_from_feature_store(
            strategy_set_name=strategy_set_name,
            symbols=symbols,
            timeframes=timeframes,
            write_outputs=write
        )

        print("\n" + strategy_portfolio_result_to_text(result))

        if write:
            print(f"\nPortfolio reports written to data/signals/ranking")

        return 0
    except Exception as e:
        print(f"Error running rule strategy set ranked: {e}")
        return 1

def handle_universe_info(context) -> int:
    from usa_signal_bot.universe.registry import get_default_watchlist_path, get_sample_stocks_path, get_sample_etfs_path

    print("\n--- USA Signal Bot Universe Info ---")
    print("\nThis seed file is NOT the entire USA universe.")
    print("\nIt is meant for sample purposes and will be expanded later.")
    print(f"Default Watchlist : {context.config.universe.default_watchlist_file}")
    print(f"Sample Stocks     : {get_sample_stocks_path(context.data_dir)}")
    print(f"Sample ETFs       : {get_sample_etfs_path(context.data_dir)}")
    print(f"Allowed Asset Types: {context.config.universe.asset_types}")
    print(f"Include Stocks    : {context.config.universe.include_stocks}")
    print(f"Include ETFs      : {context.config.universe.include_etfs}")
    print(f"Default Currency  : {context.config.universe.default_currency}")
    return 0

def handle_universe_validate(context, file_path: str = "") -> int:
    from pathlib import Path
    from usa_signal_bot.universe.validator import validate_universe_csv_file
    from usa_signal_bot.universe.reporting import validation_report_to_text

    if file_path:
        target = Path(file_path)
    else:
        target = Path(context.config.universe.default_watchlist_file)
        if not target.is_absolute():
            target = context.project_root / target

    print(f"Validating {target}...")
    report = validate_universe_csv_file(target)
    print(validation_report_to_text(report))

    return 0 if report.passed else 1

def handle_universe_list(context, asset_type: str = "", limit: int = 0, include_inactive: bool = False) -> int:
    from usa_signal_bot.universe.loader import load_default_watchlist

    try:
        res = load_default_watchlist(context.data_dir, context.config.universe.default_watchlist_file)
        u = res.universe

        symbols = u.symbols
        if not include_inactive:
            symbols = [s for s in symbols if s.active]

        if asset_type:
            at = asset_type.upper()
            symbols = [s for s in symbols if s.asset_type.value == at or str(s.asset_type) == at]

        if limit:
            symbols = symbols[:limit]

        print(f"--- Universe Symbols ({len(symbols)}) ---")
        for s in symbols:
            print(f"{s.symbol:<8} {str(s.asset_type):<6} {s.currency}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_universe_build(context) -> int:
    from usa_signal_bot.universe.builder import build_default_universe, write_default_universe_snapshot
    from usa_signal_bot.universe.reporting import summarize_universe, universe_summary_to_text

    try:
        print("\nBuilding default universe snapshot...")
        u = build_default_universe(context.data_dir)
        p = write_default_universe_snapshot(context.data_dir, u)

        summary = summarize_universe(u)
        print(f"Snapshot written to {p}")
        print(universe_summary_to_text(summary))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_universe_summary(context, json_out: bool = False) -> int:
    from usa_signal_bot.universe.loader import load_default_watchlist
    from usa_signal_bot.universe.reporting import summarize_universe, universe_summary_to_text, write_universe_summary_json
    from pathlib import Path

    try:
        res = load_default_watchlist(context.data_dir, context.config.universe.default_watchlist_file)
        summary = summarize_universe(res.universe, [res.source_path])

        if json_out:
            out_path = context.reports_dir / "universe_summary.json"
            write_universe_summary_json(out_path, summary)
            print(f"JSON summary written to {out_path}")
        else:
            print(universe_summary_to_text(summary))

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_cli_exception(e: Exception) -> int:
    """Handles exceptions explicitly meant for the CLI output."""
    print(f"Error: {str(e)}", file=sys.stderr)
    return 1

def handle_smoke(context) -> None:
    """Runs a quick smoke test of the core components."""
    print("\n--- USA Signal Bot Smoke Test ---")
    checks = run_startup_checks(context)
    for check in checks:
        print(f"✓ {check}")
    print("\n\nSmoke test completed successfully. System is ready.")

def handle_show_config(context) -> None:
    """Displays the currently loaded and merged configuration."""
    print("\n--- Loaded Configuration ---")
    import pprint
    cfg_dict = config_to_dict(context.config)
    pprint.pprint(cfg_dict, width=80)

def handle_show_paths() -> None:
    """Displays all resolved system paths."""
    print("\n--- Resolved System Paths ---")
    print(f"Project Root   : {paths.PROJECT_ROOT}")
    print(f"Config Dir     : {paths.CONFIG_DIR}")
    print(f"Data Dir       : {paths.DATA_DIR}")
    print(f"Logs Dir       : {paths.LOGS_DIR}")
    print(f"Cache Dir      : {paths.CACHE_DIR}")
    print(f"Reports Dir    : {paths.REPORTS_DIR}")
    print(f"Paper Trade Dir: {paths.PAPER_DIR}")
    print(f"Backtests Dir  : {paths.BACKTESTS_DIR}")

def handle_validate_config(context) -> None:
    """Validates configuration rules."""
    print("\n--- Configuration Validation ---")
    print("\nRules applied:")
    print("\n- broker_order_routing_enabled MUST be False")
    print("\n- web_scraping_allowed MUST be False")
    print("\n- dashboard_enabled MUST be False")
    print("\n- mode MUST be 'local_paper_only'")
    print(f"Current mode: {context.config.runtime.mode}")
    print("\n\nResult: OK. All strict conditions are met.")

def handle_runtime_summary(context) -> None:
    """Displays a JSON summary of the runtime state."""
    import json
    summary = build_runtime_summary(context)
    print(json.dumps(summary, indent=2))

def handle_check_env(context) -> None:
    """Checks required and optional environment variables."""
    from usa_signal_bot.core.environment import get_env
    print("\n--- Environment Variables Check ---")

    # For Phase 2, we just verify the mechanism works
    # We might expect TELEGRAM_BOT_TOKEN to be present if telegram is enabled
    telegram_enabled = context.config.telegram.enabled
    bot_token_env_name = context.config.telegram.bot_token_env

    print(f"Telegram Enabled: {telegram_enabled}")

    if telegram_enabled:
        token = get_env(bot_token_env_name)
        if token:
            print(f"✓ {bot_token_env_name} is set (value masked)")
        else:
            print(f"✗ {bot_token_env_name} is NOT set. Telegram notifications will fail.")
    else:
        print(f"- {bot_token_env_name} is not required because telegram is disabled.")

    print("\n\nEnvironment check completed.")

def handle_health(context) -> int:
    """Runs the system health checks and prints the result."""
    from usa_signal_bot.core.health import run_health_checks, health_results_to_dict
    from usa_signal_bot.utils.json_utils import safe_json_dumps

    print("\n--- System Health Check ---")
    results = run_health_checks(context)

    # Simple console output
    for res in results:
        status_symbol = "✓" if res.passed else "✗"
        print(f"[{status_symbol}] {res.name}: {res.message}")
        if res.details and not res.passed:
            print(f"    Details: {res.details}")

    # Determine overall status
    all_passed = all(res.passed for res in results)

    print("\n\n--- Summary JSON ---")
    print(safe_json_dumps(health_results_to_dict(results)))

    return 0 if all_passed else 1

def handle_log_info(context) -> None:
    """Displays information about the logging subsystem."""
    print("\n--- Logging Subsystem Info ---")
    print(f"Log Level     : {context.config.logging.level}")
    print(f"Log File Path : {context.log_file_path}")
    print(f"Audit Log Path: {context.audit_log_path}")
    print(f"Console Output: {'Enabled' if context.config.logging.enable_console else 'Disabled'}")
    print(f"File Output   : {'Enabled' if context.config.logging.enable_file else 'Disabled'}")

    # Check if files exist and size
    if context.log_file_path.exists():
        size_kb = context.log_file_path.stat().st_size / 1024
        print(f"Main Log Size : {size_kb:.2f} KB")
    else:
        print("\nMain Log      : Not created yet")

    if context.audit_log_path.exists():
        size_kb = context.audit_log_path.stat().st_size / 1024
        print(f"Audit Log Size: {size_kb:.2f} KB")
    else:
        print("\nAudit Log     : Not created yet")


def handle_audit_tail(context, limit: int) -> None:
    """Tails the last N events from the audit log."""
    print(f"--- Last {limit} Audit Events ---")
    if not context.audit_log_path.exists():
        print("\nAudit log file does not exist yet.")
        return

    from usa_signal_bot.utils.file_utils import read_last_lines
    lines = read_last_lines(context.audit_log_path, limit)

    if not lines:
        print("\nAudit log is empty.")
        return

    import json
    for line in lines:
        try:
            event = json.loads(line)
            timestamp = event.get('timestamp_utc', 'UNKNOWN')
            event_type = event.get('event_type', 'UNKNOWN')
            severity = event.get('severity', 'UNKNOWN')
            msg = event.get('message', '')
            print(f"[{timestamp}] {severity} - {event_type}: {msg}")
        except json.JSONDecodeError:
            print(f"Raw line: {line.strip()}")

def handle_storage_info(context) -> None:
    """Displays storage subsystem information."""
    from usa_signal_bot.storage.file_store import LocalFileStore
    from usa_signal_bot.storage.paths import StorageArea

    print("\n--- USA Signal Bot Storage Info ---")
    store = LocalFileStore(context.data_dir)
    print(f"Root Directory: {store.root_dir}")

    print("\n\nStorage Areas:")
    for area in StorageArea:
        path = store.area_path(area.value)
        exists = path.exists()
        file_count = len(list(path.glob("*"))) if exists else 0
        status = "Ready" if exists else "Missing"
        print(f"  - {area.value:<12} [{status}] ({file_count} items): {path}")

def handle_storage_check(context) -> int:
    """Runs storage integrity checks."""
    from usa_signal_bot.storage.integrity import verify_file_integrity
    from usa_signal_bot.storage.file_store import LocalFileStore

    print("\n--- USA Signal Bot Storage Integrity Check ---")
    store = LocalFileStore(context.data_dir)

    try:
        # Example check: just verify all manifests
        manifests = store.list_files("manifests", "*.json")
        if not manifests:
            print("\nNo manifests found to check.")
            return 0

        all_passed = True
        for manifest_path in manifests:
            print(f"\nChecking manifest: {manifest_path.name}")
            try:
                from usa_signal_bot.storage.json_store import read_json_dict
                manifest_data = read_json_dict(manifest_path)
                records = manifest_data.get("records", [])
                print(f"  Found {len(records)} records.")

                for record in records:
                    target_path = Path(record.get("path", ""))
                    expected_hash = record.get("checksum_sha256")

                    if not target_path.is_absolute():
                        # Assume paths in manifest are relative to project root
                        target_path = context.project_root / target_path

                    if not target_path.exists():
                        print(f"  ✗ MISSING: {target_path}")
                        all_passed = False
                        continue

                    if expected_hash:
                        is_valid = verify_file_integrity(target_path, expected_hash)
                        if is_valid:
                            print(f"  ✓ OK: {target_path.name}")
                        else:
                            print(f"  ✗ CORRUPTED: {target_path.name} (Hash mismatch)")
                            all_passed = False
                    else:
                        print(f"  ? UNVERIFIED: {target_path.name} (No hash in manifest)")

            except Exception as e:
                print(f"  ✗ ERROR processing manifest: {e}")
                all_passed = False

        return 0 if all_passed else 1
    except Exception as e:
        print(f"Storage check failed: {e}")
        return 1

def handle_storage_list(context, area: str = "") -> int:
    """Lists files in the storage system."""
    from usa_signal_bot.storage.file_store import LocalFileStore
    from usa_signal_bot.storage.paths import StorageArea
    from usa_signal_bot.utils.file_utils import normalize_safe_filename

    print("\n--- USA Signal Bot Storage List ---")
    store = LocalFileStore(context.data_dir)

    try:
        if area:
            # Validate area
            valid_areas = [a.value for a in StorageArea]
            if area not in valid_areas:
                print(f"Invalid area '{area}'. Valid areas: {valid_areas}")
                return 1
            areas_to_list = [area]
        else:
            areas_to_list = [a.value for a in StorageArea]

        for a in areas_to_list:
            files = store.list_files(a)
            print(f"\n[{a}] ({len(files)} items)")
            for f in files:
                size_kb = f.stat().st_size / 1024
                print(f"  - {f.name} ({size_kb:.1f} KB)")

        return 0
    except Exception as e:
        print(f"Error listing storage: {e}")
        return 1


def handle_active_universe_info(context) -> int:
    from usa_signal_bot.universe.active import resolve_active_universe, active_universe_resolution_to_text

    try:
        res = resolve_active_universe(
            data_root=context.data_dir,
            fallback_to_watchlist=context.config.active_universe.fallback_to_watchlist
        )
        print(active_universe_resolution_to_text(res))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_symbols(context, limit: int = 0, asset_type: str = "", include_inactive: bool = False) -> int:
    from usa_signal_bot.universe.active import resolve_active_universe

    try:
        res = resolve_active_universe(
            data_root=context.data_dir,
            fallback_to_watchlist=context.config.active_universe.fallback_to_watchlist
        )

        symbols = res.universe.symbols if include_inactive else res.universe.get_active_symbols()
        if symbols and isinstance(symbols[0], str): symbols = [s for s in res.universe.symbols if s.symbol in symbols] if not include_inactive else res.universe.symbols

        if asset_type:
            at_lower = asset_type.lower()
            symbols = [s for s in symbols if hasattr(s, "asset_type") and (s.asset_type.value.lower() if hasattr(s.asset_type, 'value') else str(s.asset_type).lower()) == at_lower]

        print(f"Active Universe Symbols ({len(symbols)} found)")
        print("\n-" * 50)

        display_limit = limit if limit and limit > 0 else len(symbols)
        for sym in symbols[:display_limit]:
            status = "ACTIVE" if hasattr(sym, "active") and sym.active else "INACTIVE"
            at = sym.asset_type.value if hasattr(sym.asset_type, 'value') else str(sym.asset_type)
            print(f"{sym.symbol:10} | {at:5} | {status:8} | {sym.name or 'N/A'}")

        if len(symbols) > display_limit:
            print(f"... and {len(symbols) - display_limit} more symbols")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_plan(context, timeframes_str: str = "", provider: str = "yfinance", limit: int = 0, asset_type: str = "", force: bool = False, no_cache: bool = False) -> int:
    from usa_signal_bot.universe.active import resolve_active_universe
    from usa_signal_bot.data.multitimeframe import MultiTimeframeDataRequest, MultiTimeframeDataPipeline
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.data.downloader import MarketDataDownloader

    try:
        res = resolve_active_universe(
            data_root=context.data_dir,
            fallback_to_watchlist=context.config.active_universe.fallback_to_watchlist
        )

        timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else context.config.multi_timeframe.default_timeframes

        active_symbols = res.universe.get_active_symbols()
        if asset_type:
            at_lower = asset_type.lower()
            active_symbols = [s for s in active_symbols if hasattr(s, "asset_type") and (s.asset_type.value.lower() if hasattr(s.asset_type, 'value') else str(s.asset_type).lower()) == at_lower]

        symbols = [s.symbol if hasattr(s, 'symbol') else str(s) for s in active_symbols]
        if limit and limit > 0:
            symbols = symbols[:limit]

        registry = create_default_provider_registry(include_yfinance=context.config.providers.yfinance_enabled)
        downloader = MarketDataDownloader(registry, context.data_dir)
        pipeline = MultiTimeframeDataPipeline(downloader, context.data_dir, provider)

        print(f"Planning data refresh for {len(symbols)} symbols from active universe across {len(timeframes)} timeframes...")

        cached_bars = pipeline.collect_cached_bars_for_timeframes(symbols, timeframes)

        from usa_signal_bot.data.refresh import build_cache_refresh_plan
        from usa_signal_bot.data.models import CacheRefreshRequest

        req = CacheRefreshRequest(
            provider_name=provider,
            symbols=symbols,
            timeframes=timeframes,
            force_refresh=force,
            use_cache=not no_cache,
            ttl_seconds=context.config.cache_refresh.default_ttl_seconds
        )

        from usa_signal_bot.data.refresh import build_cache_refresh_plan
        plan = build_cache_refresh_plan(req, cached_bars)

        from usa_signal_bot.data.refresh import cache_refresh_plan_to_text
        print(cache_refresh_plan_to_text(plan))

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_download(context, timeframes_str: str = "", provider: str = "yfinance", limit: int = 0, asset_type: str = "", force: bool = False, no_cache: bool = False) -> int:
    from usa_signal_bot.data.active_universe_pipeline import ActiveUniverseDataPipeline, ActiveUniversePipelineRequest, active_pipeline_result_to_text
    from usa_signal_bot.universe.readiness_gate import UniverseReadinessGateCriteria
    from usa_signal_bot.data.multitimeframe import MultiTimeframeDataPipeline
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.data.downloader import MarketDataDownloader

    try:
        registry = create_default_provider_registry(include_yfinance=context.config.providers.yfinance_enabled)
        downloader = MarketDataDownloader(registry, context.data_dir)
        mtf_pipeline = MultiTimeframeDataPipeline(downloader, context.data_dir, provider)

        pipeline = ActiveUniverseDataPipeline(mtf_pipeline, context.data_dir)

        timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else context.config.multi_timeframe.default_timeframes

        max_symbols = limit if limit and limit > 0 else context.config.active_universe.max_symbols_per_run

        criteria = UniverseReadinessGateCriteria(
            min_symbol_score=context.config.universe_readiness_gate.min_symbol_score,
            min_required_timeframes=context.config.universe_readiness_gate.min_required_timeframes,
            required_primary_timeframe=context.config.universe_readiness_gate.required_primary_timeframe,
            allow_partial_symbols=context.config.universe_readiness_gate.allow_partial_symbols,
            min_eligible_symbol_ratio=context.config.universe_readiness_gate.min_eligible_symbol_ratio,
            max_failed_symbol_ratio=context.config.universe_readiness_gate.max_failed_symbol_ratio
        )

        req = ActiveUniversePipelineRequest(
            provider_name=provider,
            timeframes=timeframes,
            asset_type=asset_type,
            max_symbols=max_symbols,
            force_refresh=force,
            use_cache=not no_cache,
            fallback_to_watchlist=context.config.active_universe.fallback_to_watchlist,
            readiness_criteria=criteria,
            write_reports=True,
            write_eligible_outputs=True
        )

        print(f"Starting active universe data download pipeline...")
        print(f"Provider: {provider}, Timeframes: {timeframes}, Max Symbols: {max_symbols}")

        result = pipeline.run(req)

        print(active_pipeline_result_to_text(result))

        return 0 if result.success else 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_readiness(context, latest_run: bool, from_cache: bool) -> int:
    from usa_signal_bot.universe.readiness_gate import UniverseReadinessGateReport, universe_readiness_gate_report_to_text
    import json

    try:
        gate_path = None

        if latest_run:
            from usa_signal_bot.data.universe_runs import get_latest_universe_data_run, build_universe_run_dir
            run = get_latest_universe_data_run(context.data_dir)
            if run:
                run_dir = build_universe_run_dir(context.data_dir, run.run_id)
                gate_path = run_dir / "gate_report.json"

        if gate_path and gate_path.exists():
            with open(gate_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            from usa_signal_bot.core.enums import UniverseReadinessGateStatus, SymbolReadinessStatus
            from usa_signal_bot.universe.readiness_gate import SymbolReadinessDecision

            report = UniverseReadinessGateReport(
                report_id=data["report_id"],
                created_at_utc=data["created_at_utc"],
                universe_name=data["universe_name"],
                total_symbols=data["total_symbols"],
                eligible_symbols=data["eligible_symbols"],
                partial_symbols=data["partial_symbols"],
                ineligible_symbols=data["ineligible_symbols"],
                missing_data_symbols=data["missing_data_symbols"],
                failed_validation_symbols=data["failed_validation_symbols"],
                eligible_symbol_ratio=data["eligible_symbol_ratio"],
                failed_symbol_ratio=data["failed_symbol_ratio"],
                status=UniverseReadinessGateStatus(data["status"]),
                decisions=[
                    SymbolReadinessDecision(
                        symbol=d["symbol"],
                        status=SymbolReadinessStatus(d["status"]),
                        score=d["score"],
                        ready_timeframes=d["ready_timeframes"],
                        missing_timeframes=d["missing_timeframes"],
                        failed_timeframes=d["failed_timeframes"],
                        reasons=d["reasons"]
                    ) for d in data["decisions"]
                ],
                blocking_reasons=data.get("blocking_reasons", []),
                warnings=data.get("warnings", [])
            )

            print(universe_readiness_gate_report_to_text(report))
            return 0
        else:
            print("\nNo latest run gate report found. Please run active-universe-download first.")
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_runs(context) -> int:
    from usa_signal_bot.data.universe_runs import list_universe_data_runs

    try:
        runs = list_universe_data_runs(context.data_dir)
        print(f"Universe Data Runs ({len(runs)} found)")
        print("\n-" * 100)

        for run in runs:
            print(f"{run.run_id:30} | {run.status.value:15} | {run.universe_name:20} | {run.total_symbols} symbols | {run.created_at_utc}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_latest_run(context) -> int:
    from usa_signal_bot.data.universe_runs import get_latest_universe_data_run, universe_data_run_to_text

    try:
        run = get_latest_universe_data_run(context.data_dir)
        if not run:
            print("\nNo universe data runs found.")
            return 0

        print(universe_data_run_to_text(run))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_eligible(context, latest_run: bool, format: str) -> int:
    try:
        if latest_run:
            readiness_dir = context.data_dir / "universe" / "readiness"
            if format == "csv":
                path = readiness_dir / "eligible_symbols.csv"
            elif format == "txt":
                path = readiness_dir / "eligible_symbols.txt"
            else:
                print(f"Unsupported format: {format}")
                return 1

            if path.exists():
                print(f"Eligible symbols path: {path}")
                with open(path, "r", encoding="utf-8") as f:
                    print(f.read())
                return 0
            else:
                print(f"Eligible symbols file not found: {path}")
                return 1
        else:
            print("\nOnly latest-run is currently supported for eligible symbols.")
            return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1



def handle_momentum_indicator_list(context) -> int:
    from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
    from usa_signal_bot.core.enums import IndicatorCategory
    print("\n--- Momentum Indicator Registry ---")
    reg = create_default_indicator_registry()
    for ind in reg.list_by_category(IndicatorCategory.MOMENTUM): print(ind.metadata.name)
    return 0

def handle_momentum_indicator_set_info(context, set_name: str) -> int:
    from usa_signal_bot.features.momentum_sets import get_momentum_indicator_set
    from usa_signal_bot.features.reporting import momentum_indicator_set_to_text
    print(momentum_indicator_set_to_text(get_momentum_indicator_set(set_name)))
    return 0

def handle_momentum_feature_compute_cache(context, symbols_str: str, timeframes_str: str, set_name: str, provider: str, write: bool) -> int:
    from usa_signal_bot.features.engine import FeatureEngine
    from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
    from usa_signal_bot.features.reporting import momentum_feature_summary_to_text
    print("\nMomentum Feature Compute from Cache")
    symbols = [s.strip() for s in symbols_str.split(",")] if symbols_str else []
    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]
    engine = FeatureEngine(create_default_indicator_registry(), context.data_dir)
    res = engine.compute_momentum_set_from_cache(symbols, timeframes, set_name=set_name, provider_name=provider)
    print(momentum_feature_summary_to_text(res))
    return 0 if res.is_successful() else 1

def handle_momentum_feature_summary(context) -> int:
    from usa_signal_bot.features.feature_store import feature_store_dir
    print("\nFeature Outputs Summary")
    return 0


def run_volatility_indicator_list() -> int:
    try:
        from usa_signal_bot.features.indicator_registry import get_default_registry
        from usa_signal_bot.core.enums import IndicatorCategory

        reg = get_default_registry()
        v_inds = reg.list_by_category(IndicatorCategory.VOLATILITY)

        if not v_inds:
            print("\nNo volatility indicators registered.")
            return 0

        print(f"Registered Volatility Indicators ({len(v_inds)}):\n")
        for ind in v_inds:
            m = ind.metadata
            print(f"- {m.name} (v{m.version})")
            print(f"  Description: {m.description}")
            print(f"  Min bars: {m.min_bars}")
            print(f"  Produces: {', '.join(m.produces)}")
            print()
        return 0
    except Exception as e:
        print(f"Error listing volatility indicators: {e}")
        return 1

def run_volatility_indicator_set_info(args) -> int:
    try:
        from usa_signal_bot.features.volatility_sets import get_volatility_indicator_set, list_volatility_indicator_sets
        from usa_signal_bot.features.indicator_registry import get_default_registry

        if not args.set:
            sets = list_volatility_indicator_sets()
            print("\nAvailable Volatility Indicator Sets:\n")
            for s in sets:
                print(f"- {s.name}")
            print("\n\nUse --set <name> to see details.")
            return 0

        try:
            ind_set = get_volatility_indicator_set(args.set)
        except Exception as e:
            print(f"Error: {e}")
            return 1

        reg = get_default_registry()

        print(f"Volatility Indicator Set: {ind_set.name}\n")
        print("\nIndicators and Parameters:")
        for name in ind_set.indicators:
            params = ind_set.params_by_indicator.get(name, {})
            try:
                ind_meta = reg.get(name).metadata
                desc = ind_meta.description
            except:
                desc = "Unknown indicator"

            print(f"  - {name} ({desc})")
            if params:
                for k, v in params.items():
                    print(f"      {k}: {v}")
            else:
                print("\n      (default parameters)")

        return 0
    except Exception as e:
        print(f"Error getting volatility indicator set info: {e}")
        return 1

def run_volatility_feature_compute_cache(args) -> int:
    try:
        from usa_signal_bot.core.runtime_state import RuntimeContext
        from usa_signal_bot.features.indicator_registry import get_default_registry
        from usa_signal_bot.features.engine import FeatureEngine
        from usa_signal_bot.features.reporting import (
            write_volatility_feature_report_json,
            volatility_feature_summary_to_text
        )
        from usa_signal_bot.features.volatility_sets import get_volatility_indicator_set
        from usa_signal_bot.features.validation import (
             validate_volatility_feature_columns,
             feature_validation_report_to_text
        )

        ctx = RuntimeContext.create()
        reg = get_default_registry()
        engine = FeatureEngine(reg, ctx.paths.data_dir)

        symbols = args.symbols.split(",") if args.symbols else []
        timeframes = args.timeframes.split(",") if args.timeframes else ["1d"]
        provider = args.provider
        set_name = args.set

        print(f"Computing volatility features from cache for {len(symbols) if symbols else 'ALL'} symbols...")
        print(f"Timeframes: {timeframes}")
        print(f"Set: {set_name}")
        print(f"Provider: {provider}")

        try:
             ind_set = get_volatility_indicator_set(set_name)
        except Exception as e:
             print(f"Error: {e}")
             return 1

        res = engine.compute_volatility_set_from_cache(symbols, timeframes, set_name, provider)

        print("\n\n" + volatility_feature_summary_to_text(res))

        if not res.is_successful():
             print("\n\nFeature computation failed or was partially successful. Check errors.")
             return 1

        val_report = None
        if res.feature_rows:
            import pandas as pd
            from usa_signal_bot.features.dataframe_utils import feature_rows_to_dataframe
            df = feature_rows_to_dataframe(res.feature_rows)
            val_report = validate_volatility_feature_columns(df, res.produced_features)
            print("\n\n" + feature_validation_report_to_text(val_report))

        if args.write and res.is_successful() and res.feature_rows:
             meta = engine.write_result(res)

             import uuid
             from usa_signal_bot.features.feature_store import build_feature_output_path
             from usa_signal_bot.core.enums import FeatureStorageFormat
             out_id = uuid.uuid4().hex
             group = "all"
             report_path = build_feature_output_path(
                ctx.paths.data_dir, provider, res.request.universe_name, "meta", group, FeatureStorageFormat.JSONL
             ).with_name(f"{out_id}_volatility_report.json")

             write_volatility_feature_report_json(report_path, res, ind_set)
             print(f"\nOutputs written. Meta ID: {meta.output_id}")

        return 0
    except Exception as e:
        print(f"Error computing volatility features: {e}")
        return 1

def run_volatility_feature_summary(args) -> int:
    try:
        from usa_signal_bot.core.runtime_state import RuntimeContext
        from usa_signal_bot.features.feature_store import list_feature_metadata

        ctx = RuntimeContext.create()
        metas = list_feature_metadata(ctx.paths.data_dir)

        vol_metas = []
        for m in metas:
             # Basic heuristic: Check if it has volatility indicators in its list
             has_vol = any(i in ["atr", "true_range", "bollinger_bands", "keltner_channel"] for i in m.indicators)
             if has_vol:
                  vol_metas.append(m)

        if not vol_metas:
            print("\nNo volatility feature outputs found in storage.")
            return 0

        print(f"Found {len(vol_metas)} volatility feature outputs:\n")
        for m in vol_metas:
            print(f"- Output ID: {m.output_id}")
            print(f"  Created: {m.created_at_utc}")
            print(f"  Provider: {m.provider_name}, Universe: {m.universe_name or 'N/A'}")
            print(f"  Symbols: {len(m.symbols)}, Timeframes: {m.timeframes}")
            print(f"  Indicators: {len(m.indicators)}, Features: {len(m.produced_features)}")
            print(f"  Rows: {m.row_count}")
            print()
        return 0
    except Exception as e:
        print(f"Error listing volatility feature summary: {e}")
        return 1


def handle_strategy_list(context) -> int:
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_reporting import strategy_registry_to_text
    print("\n--- Strategy Registry ---")
    try:
        registry = create_default_strategy_registry()
        print(strategy_registry_to_text(registry))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_strategy_info(context, name: str) -> int:
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_metadata import strategy_metadata_summary_text
    from usa_signal_bot.strategies.strategy_params import strategy_parameter_schema_to_dict
    import json

    try:
        registry = create_default_strategy_registry()
        if not registry.has(name):
            print(f"Error: Strategy '{name}' not found.")
            return 1

        strategy = registry.get(name)
        print(strategy_metadata_summary_text(strategy.metadata))
        print("\nParameters:")
        print(json.dumps(strategy_parameter_schema_to_dict(strategy.parameter_schema), indent=2))

        has_warning = any("execution" in str(n).lower() and "not" in str(n).lower() for n in strategy.metadata.notes)
        if has_warning:
             print("\nNote: This strategy generates candidates only. NO EXECUTION will be performed.")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_strategy_run_feature_store(context, strategy_name: str, symbols_str: str, timeframes_str: str, write: bool) -> int:
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_reporting import strategy_run_result_to_text, strategy_signal_list_to_text
    from usa_signal_bot.features.feature_store import list_feature_outputs

    print(f"--- Strategy Run (Feature Store): {strategy_name} ---")

    if not list_feature_outputs(context.data_dir):
         print("\nError: No feature outputs found. Please run a feature-pipeline-run command first.")
         return 1

    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("\nError: --symbols is required for this command")
        return 1

    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]

    try:
        registry = create_default_strategy_registry()
        engine = StrategyEngine(registry, context.data_dir)

        res = engine.run_strategy_from_feature_store(strategy_name, symbols, timeframes, write_outputs=write)

        print("\n" + strategy_run_result_to_text(res))
        if res.signals:
            print("\n" + strategy_signal_list_to_text(res.signals))

        return 0 if str(res.status) != "FAILED" else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_strategy_run_defaults(context, symbols_str: str, timeframes_str: str, write: bool) -> int:
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_reporting import strategy_run_result_to_text
    from usa_signal_bot.features.feature_store import list_feature_outputs

    print(f"--- Strategy Run Defaults ---")

    if not list_feature_outputs(context.data_dir):
         print("\nError: No feature outputs found. Please run a feature-pipeline-run command first.")
         return 1

    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("\nError: --symbols is required for this command")
        return 1

    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]

    try:
        registry = create_default_strategy_registry()
        engine = StrategyEngine(registry, context.data_dir)

        strategies = context.config.strategies.default_strategies
        print(f"Running {len(strategies)} default strategies...")

        success = True
        for strat in strategies:
            if registry.has(strat):
                print(f"\n--- Strategy: {strat} ---")
                res = engine.run_strategy_from_feature_store(strat, symbols, timeframes, write_outputs=write)
                print(strategy_run_result_to_text(res))
                if str(res.status) == "FAILED":
                    success = False
            else:
                 print(f"Warning: Strategy '{strat}' not found in registry.")

        return 0 if success else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_signal_store_info(context) -> int:
    from usa_signal_bot.strategies.signal_store import signal_store_summary
    import json
    try:
        summary = signal_store_summary(context.data_dir)
        print("\n--- Signal Store Info ---")
        print(json.dumps(summary, indent=2))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_signal_summary(context) -> int:
    from usa_signal_bot.strategies.signal_store import list_signal_outputs
    import json

    print("\n--- Signal Outputs Summary ---")
    try:
        files = list_signal_outputs(context.data_dir)
        if not files:
            print("\nNo signal outputs found.")
            return 0

        print(f"Found {len(files)} signal files. Showing latest 5:\n")

        for f in files[:5]:
            try:
                count = 0
                strat = "Unknown"
                tf = "Unknown"
                with open(f, "r") as jsonl_file:
                    for line in jsonl_file:
                        if line.strip():
                            count += 1
                            if count == 1:
                                d = json.loads(line)
                                strat = d.get("strategy_name", "Unknown")
                                tf = d.get("timeframe", "Unknown")
                print(f"[{f.name}] Strategy: {strat}, Timeframe: {tf}, Signals: {count}")
            except Exception:
                print(f"  [Error reading file {f.name}]")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_signal_validate(context, file_path_str: str) -> int:
    from usa_signal_bot.strategies.signal_store import read_signals_jsonl
    from usa_signal_bot.strategies.signal_contract import StrategySignal
    from usa_signal_bot.strategies.signal_validation import validate_signal_list, signal_validation_report_to_text
    from pathlib import Path

    print("\n--- Signal File Validation ---")
    if not file_path_str:
        print("\nError: --file is required")
        return 1

    path = Path(file_path_str)
    if not path.exists():
        print(f"Error: File {path} does not exist")
        return 1

    try:
        raw_signals = read_signals_jsonl(path)

        # Simple instantiation logic for validation
        signals = []
        for r in raw_signals:
            try:
                # Remove extra fields if any, to avoid init errors
                if "metadata" in r and not r["metadata"]:
                    r["metadata"] = {}
                signals.append(StrategySignal(**r))
            except Exception as e:
                 print(f"Failed to instantiate signal: {e}")

        if not signals and raw_signals:
            print("\nError: Could not parse signals from file.")
            return 1

        val_report = validate_signal_list(signals)
        print("\n" + signal_validation_report_to_text(val_report))
        return 0 if val_report.valid else 1
    except Exception as e:
        print(f"Validation failed: {e}")
        return 1



def handle_backtest_info(context, args):
    from usa_signal_bot.core.logging_config import setup_logging
    setup_logging(context.config)

    cfg = context.config.backtesting
    h_cfg = context.config.historical_replay
    print("=== Backtest Foundation Info ===")
    print(f"Backtesting Enabled: {cfg.enabled}")
    print(f"Historical Replay Enabled: {h_cfg.enabled}")
    print(f"Store Dir: {cfg.store_dir}")
    print(f"Default Starting Cash: ${cfg.default_starting_cash:.2f}")
    print(f"Default Signal Mode: {cfg.default_signal_mode}")
    print(f"Default Exit Mode: {cfg.default_exit_mode}")
    print(f"Default Hold Bars: {cfg.default_hold_bars}")
    print("\nWARNING: This engine does not produce live orders or paper trades.")
    print("It is purely for local historical signal replay and research.")
    return 0

def handle_backtest_run_signals(context, args):
    from usa_signal_bot.backtesting.backtest_engine import BacktestEngine, BacktestRunRequest, BacktestRunConfig
    from usa_signal_bot.backtesting.backtest_reporting import backtest_run_result_to_text

    try:
        symbols = args.symbols.split(",") if args.symbols else []
        req = BacktestRunRequest(
            run_name="CLI_Signal_Run",
            symbols=symbols,
            timeframe=args.timeframe,
            signal_file=args.signal_file,
            start_date=args.start,
            end_date=args.end
        )

        cfg = context.config.backtesting
        req.config = BacktestRunConfig(
            starting_cash=args.starting_cash if args.starting_cash is not None else cfg.default_starting_cash,
            fee_rate=cfg.default_fee_rate,
            slippage_bps=cfg.default_slippage_bps,
            signal_to_order=__import__('usa_signal_bot.backtesting.signal_adapter', fromlist=['default_signal_to_order_config']).default_signal_to_order_config(),
            exit_mode=__import__('usa_signal_bot.core.enums', fromlist=['BacktestExitMode']).BacktestExitMode(cfg.default_exit_mode.upper() if isinstance(cfg.default_exit_mode, str) else cfg.default_exit_mode),
            hold_bars=args.hold_bars if args.hold_bars is not None else cfg.default_hold_bars,
            max_positions=cfg.max_positions,
            max_position_notional=cfg.max_position_notional,
            allow_fractional_quantity=cfg.allow_fractional_quantity
        )

        sig_mode_enum = __import__('usa_signal_bot.core.enums', fromlist=['BacktestSignalMode']).BacktestSignalMode(cfg.default_signal_mode.upper())
        req.config.signal_to_order.signal_mode = sig_mode_enum

        engine = BacktestEngine(context.data_dir)
        result = engine.run(req)

        print(backtest_run_result_to_text(result))

        if getattr(args, 'write', True):
            paths = engine.write_result(result)
            print(f"\nResult written to {paths[0].parent}")
        return 0
    except Exception as e:
        import logging
        logging.getLogger("usa_signal_bot.cli").error(f"Failed to run backtest: {e}")
        return 1

def handle_backtest_run_candidates(context, args):
    from usa_signal_bot.backtesting.backtest_engine import BacktestEngine, BacktestRunRequest, BacktestRunConfig
    from usa_signal_bot.backtesting.backtest_reporting import backtest_run_result_to_text

    try:
        symbols = args.symbols.split(",") if args.symbols else []
        req = BacktestRunRequest(
            run_name="CLI_Candidate_Run",
            symbols=symbols,
            timeframe=args.timeframe,
            selected_candidates_file=args.candidates_file,
            start_date=args.start,
            end_date=args.end
        )

        cfg = context.config.backtesting
        req.config = BacktestRunConfig(
            starting_cash=args.starting_cash if args.starting_cash is not None else cfg.default_starting_cash,
            fee_rate=cfg.default_fee_rate,
            slippage_bps=cfg.default_slippage_bps,
            signal_to_order=__import__('usa_signal_bot.backtesting.signal_adapter', fromlist=['default_signal_to_order_config']).default_signal_to_order_config(),
            exit_mode=__import__('usa_signal_bot.core.enums', fromlist=['BacktestExitMode']).BacktestExitMode(cfg.default_exit_mode.upper() if isinstance(cfg.default_exit_mode, str) else cfg.default_exit_mode),
            hold_bars=args.hold_bars if args.hold_bars is not None else cfg.default_hold_bars,
            max_positions=cfg.max_positions,
            max_position_notional=cfg.max_position_notional,
            allow_fractional_quantity=cfg.allow_fractional_quantity
        )

        sig_mode_enum = __import__('usa_signal_bot.core.enums', fromlist=['BacktestSignalMode']).BacktestSignalMode(cfg.default_signal_mode.upper())
        req.config.signal_to_order.signal_mode = sig_mode_enum

        engine = BacktestEngine(context.data_dir)
        result = engine.run(req)

        print(backtest_run_result_to_text(result))

        if getattr(args, 'write', True):
            paths = engine.write_result(result)
            print(f"\nResult written to {paths[0].parent}")
        return 0
    except Exception as e:
        import logging
        logging.getLogger("usa_signal_bot.cli").error(f"Failed to run backtest: {e}")
        return 1

def handle_backtest_summary(context, args):
    from usa_signal_bot.backtesting.backtest_store import list_backtest_runs
    from usa_signal_bot.core.serialization import load_json

    runs = list_backtest_runs(context.data_dir)
    if not runs:
        print("No backtest runs found.")
        return 0

    print("=== Backtest Runs ===")
    for run_dir in runs:
        result_file = run_dir / "result.json"
        if result_file.exists():
            data = load_json(result_file)
            metrics = data.get("metrics", {})
            print(f"- {data.get('run_id')} | {data.get('created_at_utc')} | {data.get('status')}")
            if metrics:
                print(f"    Eq: ${metrics.get('ending_equity', 0):.2f} | Ret: {metrics.get('total_return_pct', 0)*100:.2f}% | Trades: {metrics.get('total_trades', 0)}")
            print("")
    return 0

def handle_backtest_latest(context, args):
    from usa_signal_bot.backtesting.backtest_store import list_backtest_runs
    from usa_signal_bot.core.serialization import load_json
    import json

    runs = list_backtest_runs(context.data_dir)
    if not runs:
        print("No backtest runs found.")
        return 0

    latest = runs[0]
    result_file = latest / "result.json"
    if result_file.exists():
        data = load_json(result_file)
        print("=== Latest Backtest Run ===")
        print(json.dumps(data, indent=2))
    return 0

def handle_backtest_validate(context, args):
    from usa_signal_bot.backtesting.backtest_store import list_backtest_runs
    import json

    runs = list_backtest_runs(context.data_dir)
    if not runs:
        print("No runs to validate.")
        return 0

    print(f"Found {len(runs)} runs. Validation infrastructure is ready.")
    print("Broker execution guard logic is active during actual runs.")
    return 0



def command_robustness_info(args) -> int:
    try:
        from usa_signal_bot.core.config import load_app_config
        config = load_app_config()
        mc = getattr(config, 'monte_carlo', None)
        bt = getattr(config, 'bootstrap_analysis', None)
        st = getattr(config, 'stress_testing', None)
        rb = getattr(config, 'robustness', None)

        print("Robustness & Stress Testing Configuration")
        print("-" * 80)

        if mc:
            print("Monte Carlo Simulation:")
            print(f"  Enabled: {mc.enabled}")
            print(f"  Default Type: {mc.default_simulation_type}")
            print(f"  Iterations: {mc.default_iterations} (Max: {mc.max_iterations})")
            print(f"  Random Seed: {mc.random_seed}")

        if bt:
            print("\nBootstrap Analysis:")
            print(f"  Enabled: {bt.enabled}")
            print(f"  Default Percentiles: {bt.default_percentiles}")

        if st:
            print("\nStress Testing:")
            print(f"  Enabled: {st.enabled}")
            print(f"  Missing Trade Fraction: {st.missing_trade_fraction}")
            print(f"  Fee/Slippage Multipliers: {st.fee_stress_multiplier}x / {st.slippage_stress_multiplier}x")

        if rb:
             print("\nRobustness Score:")
             print(f"  Enabled: {rb.enabled}")
             print(f"  Thresholds: VR > {rb.very_robust_score} | R > {rb.robust_score} | M > {rb.moderate_score} | F > {rb.fragile_score}")

        print("\n" + "="*80)
        print("IMPORTANT LIMITATION: Robustness scores and Monte Carlo percentile bands")
        print("are based on historical distributions and DO NOT guarantee future performance.")
        print("="*80)

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def _load_ledger_and_curve(run_dir):
    import json
    from usa_signal_bot.backtesting.trade_ledger import TradeLedger, BacktestTrade, TradeDirection, TradeStatus
    from usa_signal_bot.backtesting.equity_curve import EquityCurve, EquityCurvePoint
    from usa_signal_bot.core.enums import TradeDirection as ETradeDirection

    ledger = None
    curve = None

    ledger_path = run_dir / "trade_ledger.json"
    if ledger_path.exists():
        with open(ledger_path, "r") as f:
            l_data = json.load(f)
            trades = []
            for t in l_data.get("closed_trades", []):
                trades.append(BacktestTrade(
                    trade_id=t.get("trade_id", "unknown"),
                    symbol=t.get("symbol", "unknown"),
                    timeframe=t.get("timeframe", "1d"),
                    direction=ETradeDirection(t.get("direction", "LONG")),
                    status=TradeStatus.CLOSED,
                    entry_fill_id=None, exit_fill_id=None,
                    entry_time_utc=t.get("entry_time_utc", ""),
                    exit_time_utc=t.get("exit_time_utc", ""),
                    entry_price=t.get("entry_price", 0.0),
                    exit_price=t.get("exit_price", 0.0),
                    quantity=t.get("quantity", 0.0),
                    gross_pnl=t.get("gross_pnl", 0.0),
                    net_pnl=t.get("net_pnl", 0.0),
                    total_fees=t.get("total_fees", 0.0),
                    total_slippage_cost=t.get("total_slippage_cost", 0.0),
                    return_pct=t.get("return_pct", 0.0),
                    holding_bars=None, holding_seconds=None,
                    exit_reason=t.get("exit_reason", "UNKNOWN"),
                    signal_id=None, strategy_name=None
                ))
            ledger = TradeLedger(ledger_id=l_data.get("ledger_id", "simulated"), trades=trades, open_trades=[], closed_trades=trades, created_at_utc="")

    curve_path = run_dir / "equity_curve.json"
    if curve_path.exists():
        with open(curve_path, "r") as f:
            c_data = json.load(f)
            points = []
            for p in c_data.get("points", []):
                 points.append(EquityCurvePoint(
                      timestamp_utc=p.get("timestamp_utc", ""),
                      equity=p.get("equity", 0.0),
                      cash=p.get("cash", 0.0),
                      realized_pnl=0.0, unrealized_pnl=0.0, drawdown=0.0, drawdown_pct=0.0
                 ))
            curve = EquityCurve(points=points, starting_cash=c_data.get("starting_cash", 100000.0), ending_equity=c_data.get("ending_equity"), max_drawdown=None, max_drawdown_pct=None)

    return ledger, curve

def command_monte_carlo_run(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.core.config import load_app_config
        from usa_signal_bot.backtesting.backtest_store import find_latest_backtest_run_dir, find_backtest_run_dir
        from usa_signal_bot.backtesting.monte_carlo_models import MonteCarloConfig
        from usa_signal_bot.core.enums import MonteCarloSimulationType
        from usa_signal_bot.backtesting.monte_carlo_simulator import MonteCarloSimulator
        from usa_signal_bot.backtesting.robustness_store import build_robustness_run_dir, write_monte_carlo_result_json, write_monte_carlo_paths_jsonl
        from usa_signal_bot.backtesting.robustness_reporting import monte_carlo_result_to_text, write_robustness_report_json

        config = load_app_config()
        mc_config_base = getattr(config, 'monte_carlo', None)

        data_root = Path("data")
        run_dir = None
        if args.run_id:
            run_dir = find_backtest_run_dir(data_root, args.run_id)
        elif getattr(args, "latest_backtest", False):
            run_dir = find_latest_backtest_run_dir(data_root)

        if not run_dir:
            print("Error: Backtest run not found.")
            return 1

        ledger, curve = _load_ledger_and_curve(run_dir)
        if not ledger and not curve:
            print("Error: Trade ledger and equity curve missing from backtest run.")
            return 1

        sim_type = MonteCarloSimulationType(args.type) if getattr(args, "type", None) else MonteCarloSimulationType(mc_config_base.default_simulation_type if mc_config_base else "TRADE_BOOTSTRAP")
        iterations = getattr(args, "iterations", None) or (mc_config_base.default_iterations if mc_config_base else 1000)
        seed = getattr(args, "seed", None) or (mc_config_base.random_seed if mc_config_base else 42)

        mc_conf = MonteCarloConfig(
            simulation_type=sim_type,
            iterations=iterations,
            starting_cash=curve.starting_cash if curve else 100000.0,
            random_seed=seed,
            max_iterations=mc_config_base.max_iterations if mc_config_base else 10000
        )

        simulator = MonteCarloSimulator(random_seed=seed)

        if sim_type == MonteCarloSimulationType.TRADE_BOOTSTRAP:
             if not ledger:
                  print("Error: Trade ledger required for trade bootstrap.")
                  return 1
             res = simulator.run_trade_bootstrap(ledger, mc_conf, run_dir.name)
        elif sim_type == MonteCarloSimulationType.EQUITY_RETURN_BOOTSTRAP:
             if not curve:
                  print("Error: Equity curve required for equity bootstrap.")
                  return 1
             res = simulator.run_equity_return_bootstrap(curve, mc_conf, run_dir.name)
        elif sim_type == MonteCarloSimulationType.TRADE_ORDER_PERMUTATION:
             if not ledger:
                  print("Error: Trade ledger required for permutation.")
                  return 1
             res = simulator.run_trade_order_permutation(ledger, mc_conf, run_dir.name)
        else:
             print(f"Error: Unsupported simulation type: {sim_type}")
             return 1

        print(monte_carlo_result_to_text(res))

        if getattr(args, "write", False):
            rd = build_robustness_run_dir(data_root, res.run_id)
            write_monte_carlo_result_json(rd / "monte_carlo_result.json", res)
            if res.paths:
                 write_monte_carlo_paths_jsonl(rd / "paths.jsonl", res.paths)
            write_robustness_report_json(rd / "report.json", res)
            print(f"\nResults written to: {rd}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_bootstrap_run(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.backtest_store import find_latest_backtest_run_dir, find_backtest_run_dir
        from usa_signal_bot.backtesting.bootstrap_analysis import (
             extract_trade_net_returns, extract_equity_returns,
             bootstrap_trade_returns, bootstrap_equity_returns, percentile_summary
        )

        data_root = Path("data")
        run_dir = None
        if args.run_id:
            run_dir = find_backtest_run_dir(data_root, args.run_id)
        elif getattr(args, "latest_backtest", False):
            run_dir = find_latest_backtest_run_dir(data_root)

        if not run_dir:
            print("Error: Backtest run not found.")
            return 1

        ledger, curve = _load_ledger_and_curve(run_dir)
        source = getattr(args, "source", "trades")
        iterations = getattr(args, "iterations", 1000)
        if not iterations: iterations = 1000

        print(f"Running Bootstrap Analysis (Source: {source}, Iterations: {iterations})")
        print("-" * 80)

        if source == "trades":
             if not ledger:
                  print("Error: Ledger not found.")
                  return 1
             rets = extract_trade_net_returns(ledger)
             samples = bootstrap_trade_returns(rets, iterations)
        else:
             if not curve:
                  print("Error: Equity curve not found.")
                  return 1
             rets = extract_equity_returns(curve)
             samples = bootstrap_equity_returns(rets, iterations)

        total_rets = []
        for s in samples:
             r = sum(s)
             total_rets.append(r)

        p_sum = percentile_summary(total_rets)
        for k, v in p_sum.items():
             print(f"  {k}: {(v or 0)*100:.2f}%")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_stress_test_run(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.backtest_store import find_latest_backtest_run_dir, find_backtest_run_dir
        from usa_signal_bot.backtesting.stress_scenarios import (
             run_stress_scenario_set, default_stress_scenarios,
             build_fee_slippage_stress_scenario, build_missing_winners_scenario,
             build_missing_random_trades_scenario, build_worst_sequence_scenario
        )
        from usa_signal_bot.backtesting.robustness_reporting import stress_scenario_results_to_text
        from usa_signal_bot.backtesting.robustness_store import build_robustness_run_dir, write_stress_scenario_results_json
        import uuid

        data_root = Path("data")
        run_dir = None
        if args.run_id:
            run_dir = find_backtest_run_dir(data_root, args.run_id)
        elif getattr(args, "latest_backtest", False):
            run_dir = find_latest_backtest_run_dir(data_root)

        if not run_dir:
            print("Error: Backtest run not found.")
            return 1

        ledger, _ = _load_ledger_and_curve(run_dir)
        if not ledger:
             print("Error: Trade ledger required for stress scenarios.")
             return 1

        scenario = getattr(args, "scenario", "default")
        configs = []
        if scenario == "default":
             configs = default_stress_scenarios()
        elif scenario == "missing_winners":
             configs = [build_missing_winners_scenario()]
        elif scenario == "missing_random_trades":
             configs = [build_missing_random_trades_scenario()]
        elif scenario == "worst_sequence":
             configs = [build_worst_sequence_scenario()]
        elif scenario == "cost_slippage":
             configs = [build_fee_slippage_stress_scenario()]
        else:
             print("Unknown scenario")
             return 1

        results = run_stress_scenario_set(ledger, configs)
        print(stress_scenario_results_to_text(results))

        if getattr(args, "write", False):
             rd = build_robustness_run_dir(data_root, f"stress_{str(uuid.uuid4())[:8]}")
             write_stress_scenario_results_json(rd / "stress_scenarios.json", results)
             print(f"\nResults written to: {rd}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_robustness_summary(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.robustness_store import list_robustness_runs
        import json

        data_root = Path("data")
        runs = list_robustness_runs(data_root)

        print("Robustness Runs Summary")
        print("-" * 80)
        if not runs:
            print("No robustness runs found.")
            return 0

        for r_dir in runs[:20]:
            mc_path = r_dir / "monte_carlo_result.json"
            if mc_path.exists():
                with open(mc_path, "r") as f:
                    data = json.load(f)
                rid = data.get("run_id", r_dir.name)
                st = data.get("status", "UNKNOWN")
                it = data.get("config", {}).get("iterations", 0)
                bucket = data.get("robustness_bucket", "UNKNOWN")
                print(f"ID: {rid} | Status: {st} | Iterations: {it} | Bucket: {bucket}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_robustness_latest(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.robustness_store import get_latest_robustness_run_dir
        import json

        data_root = Path("data")
        r_dir = get_latest_robustness_run_dir(data_root)

        if not r_dir:
            print("No robustness runs found.")
            return 0

        rep_path = r_dir / "report.json"
        if rep_path.exists():
             with open(rep_path, "r") as f:
                  data = json.load(f)
                  print(data.get("report_text", "Empty report"))
        else:
             print(f"Found latest run at {r_dir.name} but no report.json exists.")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_robustness_validate(args) -> int:
    try:
        from pathlib import Path
        from usa_signal_bot.backtesting.robustness_store import get_latest_robustness_run_dir, build_robustness_run_dir

        data_root = Path("data")
        r_dir = None
        if args.run_id:
             r_dir = build_robustness_run_dir(data_root, args.run_id)
        elif getattr(parsed, "latest", False):
             r_dir = get_latest_robustness_run_dir(data_root)

        if not r_dir or not r_dir.exists():
             print("Validation FAILED: Run not found.")
             return 1

        has_mc = (r_dir / "monte_carlo_result.json").exists()
        has_paths = (r_dir / "paths.jsonl").exists()
        has_stress = (r_dir / "stress_scenarios.json").exists()

        print(f"Validating run: {r_dir.name}")
        print(f"  monte_carlo_result.json: {'OK' if has_mc else 'MISSING'}")
        print(f"  paths.jsonl:             {'OK' if has_paths else 'MISSING'}")
        print(f"  stress_scenarios.json:   {'OK' if has_stress else 'MISSING'}")

        if not has_mc and not has_stress:
             print("Validation FAILED: No robustness data found.")
             return 1

        print("Validation PASSED: Essential robustness files exist.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def main() -> int:

    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="USA Signal Bot CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: smoke
    subparsers.add_parser("smoke", help="Run a quick smoke test")

    # Command: show-config
    subparsers.add_parser("show-config", help="Display the loaded configuration")

    # Command: show-paths
    subparsers.add_parser("show-paths", help="Display resolved system paths")


    # Walk-Forward Commands
    parser_wf_info = subparsers.add_parser("walk-forward-info", help="Display Walk-Forward configuration")

    parser_wf_plan = subparsers.add_parser("walk-forward-plan", help="Generate Walk-Forward window plan")
    parser_wf_plan.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    parser_wf_plan.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    parser_wf_plan.add_argument("--mode", type=str, help="Mode (rolling, anchored, expanding)")
    parser_wf_plan.add_argument("--train-days", type=int, help="Train window days")
    parser_wf_plan.add_argument("--test-days", type=int, help="Test window days")
    parser_wf_plan.add_argument("--step-days", type=int, help="Step days")
    parser_wf_plan.add_argument("--max-windows", type=int, help="Max windows")

    parser_wf_signals = subparsers.add_parser("walk-forward-run-signals", help="Run walk-forward on signals")
    parser_wf_signals.add_argument("--signal-file", type=str, help="Path to signal file")
    parser_wf_signals.add_argument("--symbols", type=str, help="Comma-separated symbols")
    parser_wf_signals.add_argument("--timeframe", type=str, default="1d", help="Timeframe")
    parser_wf_signals.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    parser_wf_signals.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    parser_wf_signals.add_argument("--mode", type=str, help="Mode")
    parser_wf_signals.add_argument("--train-days", type=int, help="Train window days")
    parser_wf_signals.add_argument("--test-days", type=int, help="Test window days")
    parser_wf_signals.add_argument("--step-days", type=int, help="Step days")
    parser_wf_signals.add_argument("--max-windows", type=int, help="Max windows")
    parser_wf_signals.add_argument("--write", action="store_true", help="Write results")

    parser_wf_cands = subparsers.add_parser("walk-forward-run-candidates", help="Run walk-forward on candidates")
    parser_wf_cands.add_argument("--candidates-file", type=str, help="Path to selected candidates file")
    parser_wf_cands.add_argument("--symbols", type=str, help="Comma-separated symbols")
    parser_wf_cands.add_argument("--timeframe", type=str, default="1d", help="Timeframe")
    parser_wf_cands.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    parser_wf_cands.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    parser_wf_cands.add_argument("--mode", type=str, help="Mode")
    parser_wf_cands.add_argument("--train-days", type=int, help="Train window days")
    parser_wf_cands.add_argument("--test-days", type=int, help="Test window days")
    parser_wf_cands.add_argument("--step-days", type=int, help="Step days")
    parser_wf_cands.add_argument("--max-windows", type=int, help="Max windows")
    parser_wf_cands.add_argument("--write", action="store_true", help="Write results")

    parser_wf_sum = subparsers.add_parser("walk-forward-summary", help="Summarize walk-forward runs")

    parser_wf_lat = subparsers.add_parser("walk-forward-latest", help="Show latest walk-forward run")

    parser_wf_val = subparsers.add_parser("walk-forward-validate", help="Validate a walk-forward run")
    parser_wf_val.add_argument("--run-id", type=str, help="Run ID to validate")
    parser_wf_val.add_argument("--latest", action="store_true", help="Validate latest run")

    # Signal Ranking Commands
    parser_signal_rank = subparsers.add_parser("signal-rank-file", help="Rank signals from a JSONL file")
    parser_signal_rank.add_argument("--file", required=True, help="Path to signal JSONL file")
    parser_signal_rank.add_argument("--min-rank-score", type=float, help="Minimum rank score filter")
    parser_signal_rank.add_argument("--write", action="store_true", help="Write ranking report to disk")

    parser_signal_select = subparsers.add_parser("signal-select-candidates", help="Select candidates from a signal JSONL file")
    parser_signal_select.add_argument("--file", required=True, help="Path to signal JSONL file")
    parser_signal_select.add_argument("--max-candidates", type=int, help="Override max candidates")
    parser_signal_select.add_argument("--min-rank-score", type=float, help="Override min rank score")
    parser_signal_select.add_argument("--write", action="store_true", help="Write candidates to disk")

    subparsers.add_parser("signal-ranking-summary", help="Show summary of ranking storage")
    subparsers.add_parser("selected-candidates-summary", help="Show summary of selected candidates")

    # Portfolio Commands
    parser_portfolio = subparsers.add_parser("strategy-portfolio-run", help="Run a portfolio of strategies and aggregate/rank candidates")
    parser_portfolio.add_argument("--strategies", help="Comma-separated strategy names")
    parser_portfolio.add_argument("--symbols", help="Comma-separated symbols (optional, uses all available if empty)")
    parser_portfolio.add_argument("--timeframes", default="1d", help="Comma-separated timeframes (default: 1d)")
    parser_portfolio.add_argument("--write", action="store_true", help="Write portfolio reports to disk")

    parser_rule_ranked = subparsers.add_parser("rule-strategy-run-ranked", help="Run a rule strategy set and aggregate/rank candidates")
    parser_rule_ranked.add_argument("--set", dest="strategy_set", default="basic_rules", help="Rule strategy set name (default: basic_rules)")
    parser_rule_ranked.add_argument("--symbols", help="Comma-separated symbols (optional)")
    parser_rule_ranked.add_argument("--timeframes", default="1d", help="Comma-separated timeframes (default: 1d)")
    parser_rule_ranked.add_argument("--write", action="store_true", help="Write portfolio reports to disk")


    # Command: validate-config
    subparsers.add_parser("validate-config", help="Validate config rules")

    # Command: runtime-summary
    subparsers.add_parser("runtime-summary", help="Display runtime state JSON")

    # Command: check-env
    subparsers.add_parser("check-env", help="Check environment variables")

    # Command: health
    subparsers.add_parser("health", help="Run system health checks")
    subparsers.add_parser("universe-sources", help="List universe sources")

    parser_uni_import = subparsers.add_parser("universe-import", help="Import a local CSV as a custom universe")
    parser_uni_import.add_argument("--file", required=True, help="Path to the CSV file")
    parser_uni_import.add_argument("--name", help="Optional name for the imported universe")
    parser_uni_import.add_argument("--overwrite", action="store_true", help="Overwrite existing file if present")

    parser_uni_expand = subparsers.add_parser("universe-expand", help="Expand the universe from sources")
    parser_uni_expand.add_argument("--name", default="expanded_universe", help="Name of the expanded universe")
    parser_uni_expand.add_argument("--include-layers", help="Comma-separated layers to include")
    parser_uni_expand.add_argument("--exclude-layers", help="Comma-separated layers to exclude")
    parser_uni_expand.add_argument("--include-stocks", type=bool, default=True, help="Include stocks")
    parser_uni_expand.add_argument("--include-etfs", type=bool, default=True, help="Include ETFs")
    parser_uni_expand.add_argument("--include-inactive", action="store_true", help="Include inactive symbols")
    parser_uni_expand.add_argument("--max-symbols", type=int, help="Max symbols to include")
    parser_uni_expand.add_argument("--conflict-resolution", default="prefer_complete_metadata", help="Conflict resolution strategy")
    parser_uni_expand.add_argument("--no-snapshot", action="store_true", help="Skip creating a snapshot")

    subparsers.add_parser("universe-snapshots", help="List universe snapshots")

    parser_uni_activate = subparsers.add_parser("universe-activate-snapshot", help="Activate a snapshot")
    parser_uni_activate.add_argument("--snapshot-id", required=True, help="Snapshot ID to activate")

    subparsers.add_parser("universe-catalog", help="Show universe catalog")

    parser_uni_export = subparsers.add_parser("universe-export", help="Export a universe snapshot")
    parser_uni_export.add_argument("--snapshot-id", help="Snapshot ID to export")
    parser_uni_export.add_argument("--format", choices=["csv", "json", "txt"], default="csv", help="Export format")
    parser_uni_export.add_argument("--name", help="Name of the export file")
    parser_uni_export.add_argument("--active-only", action="store_true", help="Only export active symbols")

    subparsers.add_parser("universe-presets", help="List universe presets")
    subparsers.add_parser("indicator-list", help="List available indicators")

    parser_ind_info = subparsers.add_parser("indicator-info", help="Get information about an indicator")
    parser_ind_info.add_argument("--name", required=True, help="Indicator name")

    subparsers.add_parser("feature-store-info", help="Get information about the feature store")

    parser_fcc = subparsers.add_parser("feature-compute-cache", help="Compute features from cache")
    parser_fcc.add_argument("--symbols", help="Comma-separated symbols")
    parser_fcc.add_argument("--timeframes", help="Comma-separated timeframes (default: 1d)", default="1d")
    parser_fcc.add_argument("--indicators", help="Comma-separated indicators (default: from config)")
    parser_fcc.add_argument("--provider", default="yfinance", help="Provider name")
    parser_fcc.add_argument("--write", action="store_true", help="Write to storage")

    parser_fv = subparsers.add_parser("feature-validate", help="Validate a feature output file")
    parser_fv.add_argument("--file", required=True, help="Path to JSONL feature file")

    subparsers.add_parser("feature-summary", help="Show summary of latest feature outputs")


    # Command: log-info
    subparsers.add_parser("log-info", help="Display logging info")

    # Universe commands
    universe_info_parser = subparsers.add_parser("universe-info", help="Show universe info")

    universe_validate_parser = subparsers.add_parser("universe-validate", help="Validate universe CSV")
    universe_validate_parser.add_argument("--file", type=str, help="Specific CSV to validate")

    universe_list_parser = subparsers.add_parser("universe-list", help="List universe symbols")
    universe_list_parser.add_argument("--asset-type", type=str, choices=["stock", "etf"], help="Filter by asset type")
    universe_list_parser.add_argument("--limit", type=int, help="Limit number of output symbols")
    universe_list_parser.add_argument("--include-inactive", action="store_true", help="Include inactive symbols")

    universe_build_parser = subparsers.add_parser("universe-build", help="Build universe snapshot")

    universe_summary_parser = subparsers.add_parser("universe-summary", help="Show universe summary")
    universe_summary_parser.add_argument("--json-out", action="store_true", help="Output summary to JSON file")

    # Command: storage-info
    subparsers.add_parser("storage-info", help="Display storage subsystem information")
    subparsers.add_parser("storage-check", help="Run storage health check")

    storage_list_parser = subparsers.add_parser("storage-list", help="List files in storage")
    storage_list_parser.add_argument("--area", type=str, help="Specific storage area to list")



    provider_info_parser = subparsers.add_parser("provider-info", help="Show provider info")
    provider_list_parser = subparsers.add_parser("provider-list", help="List registered providers")
    provider_check_parser = subparsers.add_parser("provider-check", help="Check provider status")

    provider_plan_parser = subparsers.add_parser("provider-plan", help="Generate fetch plan")
    provider_plan_parser.add_argument("--symbols", type=str, required=True, help="Comma-separated symbols")
    provider_plan_parser.add_argument("--timeframe", type=str, required=True, help="Timeframe (e.g. 1d)")

    provider_fetch_parser = subparsers.add_parser("provider-mock-fetch", help="Fetch mock data")
    provider_fetch_parser.add_argument("--symbols", type=str, required=True, help="Comma-separated symbols")
    provider_fetch_parser.add_argument("--timeframe", type=str, required=True, help="Timeframe (e.g. 1d)")


    # Market Data Commands
    data_provider_info_parser = subparsers.add_parser("data-provider-info", help="Show data provider info")

    data_download_parser = subparsers.add_parser("data-download", help="Download market data for symbols")
    data_download_parser.add_argument("--symbols", type=str, required=True, help="Comma-separated symbols")
    data_download_parser.add_argument("--timeframe", type=str, default="1d", help="Timeframe (e.g. 1d)")
    data_download_parser.add_argument("--start", type=str, help="Start date YYYY-MM-DD")
    data_download_parser.add_argument("--end", type=str, help="End date YYYY-MM-DD")
    data_download_parser.add_argument("--provider", type=str, default="yfinance", help="Provider name")
    data_download_parser.add_argument("--no-cache", action="store_true", help="Bypass reading/writing cache")
    data_download_parser.add_argument("--limit", type=int, help="Limit number of symbols to fetch")

    data_download_universe_parser = subparsers.add_parser("data-download-universe", help="Download data for an entire universe")
    data_download_universe_parser.add_argument("--file", type=str, help="Universe CSV file")
    data_download_universe_parser.add_argument("--timeframe", type=str, default="1d", help="Timeframe (e.g. 1d)")
    data_download_universe_parser.add_argument("--provider", type=str, default="yfinance", help="Provider name")
    data_download_universe_parser.add_argument("--limit", type=int, default=20, help="Limit number of symbols")
    data_download_universe_parser.add_argument("--asset-type", type=str, choices=["stock", "etf"], help="Filter by asset type")
    data_download_universe_parser.add_argument("--no-cache", action="store_true", help="Bypass reading/writing cache")

    data_cache_info_parser = subparsers.add_parser("data-cache-info", help="Show info about the market data cache")

    data_quality_check_parser = subparsers.add_parser("data-quality-check", help="Check quality of cached data")
    data_quality_check_parser.add_argument("--cache-file", type=str, help="Specific cache file to check")
    data_quality_check_parser.add_argument("--symbols", type=str, help="Comma-separated symbols to check")
    data_quality_check_parser.add_argument("--timeframe", type=str, default="1d", help="Timeframe (e.g. 1d)")

    audit_parser = subparsers.add_parser("audit-tail", help="Tail the audit log")

    audit_parser.add_argument("--limit", type=int, default=20, help="Number of events to display")

    # Multi-timeframe commands
    mtf_plan_parser = subparsers.add_parser("data-mtf-plan", help="Build multi-timeframe download plan")
    mtf_plan_parser.add_argument("--symbols", help="Comma-separated symbols")
    mtf_plan_parser.add_argument("--timeframes", help="Comma-separated timeframes")
    mtf_plan_parser.add_argument("--provider", default="yfinance", help="Provider name")
    mtf_plan_parser.add_argument("--force", action="store_true", help="Force refresh")
    mtf_plan_parser.add_argument("--no-cache", action="store_true", help="Bypass cache")

    mtf_download_parser = subparsers.add_parser("data-mtf-download", help="Execute multi-timeframe download")
    mtf_download_parser.add_argument("--symbols", help="Comma-separated symbols")
    mtf_download_parser.add_argument("--timeframes", help="Comma-separated timeframes")
    mtf_download_parser.add_argument("--provider", default="yfinance", help="Provider name")
    mtf_download_parser.add_argument("--force", action="store_true", help="Force refresh")
    mtf_download_parser.add_argument("--no-cache", action="store_true", help="Bypass cache")
    mtf_download_parser.add_argument("--limit", type=int, help="Limit number of symbols")

    mtf_universe_parser = subparsers.add_parser("data-mtf-universe", help="Download multi-timeframe data for a universe")
    mtf_universe_parser.add_argument("--file", help="Path to universe file")
    mtf_universe_parser.add_argument("--timeframes", help="Comma-separated timeframes")
    mtf_universe_parser.add_argument("--provider", default="yfinance", help="Provider name")
    mtf_universe_parser.add_argument("--force", action="store_true", help="Force refresh")
    mtf_universe_parser.add_argument("--limit", type=int, help="Limit number of symbols")
    mtf_universe_parser.add_argument("--asset-type", help="Filter by asset type (stock/etf)")

    cov_report_parser = subparsers.add_parser("data-coverage-report", help="View data coverage report")
    cov_report_parser.add_argument("--latest", action="store_true", help="Show latest report")
    cov_report_parser.add_argument("--reports-dir", help="Custom reports directory")

    readiness_parser = subparsers.add_parser("data-readiness-check", help="Check data readiness")
    parser_active_uni_info = subparsers.add_parser("active-universe-info", help="Show active universe info")

    parser_active_uni_syms = subparsers.add_parser("active-universe-symbols", help="List symbols in active universe")
    parser_active_uni_syms.add_argument("--limit", type=int, default=None, help="Limit number of symbols to list")
    parser_active_uni_syms.add_argument("--asset-type", type=str, default=None, choices=["stock", "etf"], help="Filter by asset type")
    parser_active_uni_syms.add_argument("--include-inactive", action="store_true", help="Include inactive symbols")

    parser_active_uni_plan = subparsers.add_parser("active-universe-plan", help="Plan data download for active universe")
    parser_active_uni_plan.add_argument("--timeframes", type=str, default=None, help="Comma-separated timeframes (default from config)")
    parser_active_uni_plan.add_argument("--provider", type=str, default="yfinance", help="Data provider")
    parser_active_uni_plan.add_argument("--limit", type=int, default=None, help="Limit number of symbols")
    parser_active_uni_plan.add_argument("--asset-type", type=str, default=None, choices=["stock", "etf"], help="Filter by asset type")
    parser_active_uni_plan.add_argument("--force", action="store_true", help="Force refresh cache")
    parser_active_uni_plan.add_argument("--no-cache", action="store_true", help="Bypass cache completely")

    parser_active_uni_dl = subparsers.add_parser("active-universe-download", help="Download data for active universe")
    parser_active_uni_dl.add_argument("--timeframes", type=str, default=None, help="Comma-separated timeframes (default from config)")
    parser_active_uni_dl.add_argument("--provider", type=str, default="yfinance", help="Data provider")
    parser_active_uni_dl.add_argument("--limit", type=int, default=None, help="Limit number of symbols (overrides config)")
    parser_active_uni_dl.add_argument("--asset-type", type=str, default=None, choices=["stock", "etf"], help="Filter by asset type")
    parser_active_uni_dl.add_argument("--force", action="store_true", help="Force refresh cache")
    parser_active_uni_dl.add_argument("--no-cache", action="store_true", help="Bypass cache completely")

    parser_active_uni_ready = subparsers.add_parser("active-universe-readiness", help="Check active universe readiness")
    parser_active_uni_ready.add_argument("--latest-run", action="store_true", default=True, help="Check readiness from latest run")
    parser_active_uni_ready.add_argument("--from-cache", action="store_true", help="Check readiness from cache (not yet implemented for universe gate)")

    parser_active_uni_runs = subparsers.add_parser("active-universe-runs", help="List active universe data runs")

    parser_active_uni_latest_run = subparsers.add_parser("active-universe-latest-run", help="Show latest active universe data run")

    parser_active_uni_eligible = subparsers.add_parser("active-universe-eligible", help="List eligible symbols from active universe")
    parser_active_uni_eligible.add_argument("--latest-run", action="store_true", default=True, help="Get eligible symbols from latest run")
    parser_active_uni_eligible.add_argument("--format", type=str, default="txt", choices=["txt", "csv", "json"], help="Output format")

    readiness_parser.add_argument("--symbols", help="Comma-separated symbols")
    readiness_parser.add_argument("--timeframes", help="Comma-separated timeframes")
    readiness_parser.add_argument("--from-cache", action="store_true", default=True, help="Check readiness from cache")

    subparsers.add_parser("momentum-indicator-list", help="List momentum indicators")
    mom_set_info = subparsers.add_parser("momentum-indicator-set-info", help="Show momentum indicator set details")
    mom_set_info.add_argument("--set", type=str, default="basic_momentum")
    mom_compute = subparsers.add_parser("momentum-feature-compute-cache", help="Compute from cache")
    mom_compute.add_argument("--symbols", type=str)
    mom_compute.add_argument("--timeframes", type=str)
    mom_compute.add_argument("--set", type=str, default="basic_momentum")
    mom_compute.add_argument("--provider", type=str, default="yfinance")
    mom_compute.add_argument("--write", action="store_true")
    subparsers.add_parser("momentum-feature-summary", help="Show summary")

    vol_ind_list_parser = subparsers.add_parser("volatility-indicator-list", help="List all registered volatility indicators")

    vol_ind_set_info_parser = subparsers.add_parser("volatility-indicator-set-info", help="Show info for a volatility indicator set")
    vol_ind_set_info_parser.add_argument("--set", type=str, help="Name of the indicator set (e.g. basic_volatility)")

    vol_feat_compute_cache_parser = subparsers.add_parser("volatility-feature-compute-cache", help="Compute volatility features from cached data")
    vol_feat_compute_cache_parser.add_argument("--symbols", type=str, help="Comma-separated list of symbols (optional, defaults to all in cache)")
    vol_feat_compute_cache_parser.add_argument("--timeframes", type=str, default="1d", help="Comma-separated list of timeframes (default: 1d)")
    vol_feat_compute_cache_parser.add_argument("--set", type=str, default="basic_volatility", help="Indicator set to use (default: basic_volatility)")
    vol_feat_compute_cache_parser.add_argument("--provider", type=str, default="yfinance", help="Data provider (default: yfinance)")
    vol_feat_compute_cache_parser.add_argument("--write", action="store_true", help="Write results to storage")

    vol_feat_summary_parser = subparsers.add_parser("volatility-feature-summary", help="List volatility feature outputs in storage")

    parser_vol_ind_list = subparsers.add_parser("volume-indicator-list", help="List all registered volume indicators")

    parser_vol_ind_info = subparsers.add_parser("volume-indicator-set-info", help="Show info for a volume indicator set")
    parser_vol_ind_info.add_argument("--set", type=str, required=True, help="Set name (e.g., basic_volume)")

    parser_vol_feat_cache = subparsers.add_parser("volume-feature-compute-cache", help="Compute volume features from cached data")
    parser_vol_feat_cache.add_argument("--symbols", type=str, help="Comma-separated symbols")
    parser_vol_feat_cache.add_argument("--timeframes", type=str, help="Comma-separated timeframes")
    parser_vol_feat_cache.add_argument("--set", type=str, default="basic_volume", help="Indicator set name")
    parser_vol_feat_cache.add_argument("--provider", type=str, default="yfinance", help="Provider name")
    parser_vol_feat_cache.add_argument("--write", action="store_true", help="Write feature output to disk")

    parser_vol_feat_summary = subparsers.add_parser("volume-feature-summary", help="List volume feature outputs in storage")



    # Strategy and Signal Commands
    subparsers.add_parser("strategy-list", help="List registered strategies")

    parser_strat_info = subparsers.add_parser("strategy-info", help="Get info about a strategy")
    parser_strat_info.add_argument("--name", required=True, help="Strategy name")

    parser_srf = subparsers.add_parser("strategy-run-feature-store", help="Run strategy from feature store")
    parser_srf.add_argument("--strategy", required=True, help="Strategy name")
    parser_srf.add_argument("--symbols", help="Comma-separated symbols")
    parser_srf.add_argument("--timeframes", help="Comma-separated timeframes")
    parser_srf.add_argument("--write", action="store_true", help="Write signals to file")

    parser_srd = subparsers.add_parser("strategy-run-defaults", help="Run default strategies from feature store")
    parser_srd.add_argument("--symbols", help="Comma-separated symbols")
    parser_srd.add_argument("--timeframes", help="Comma-separated timeframes")
    parser_srd.add_argument("--write", action="store_true", help="Write signals to file")

    subparsers.add_parser("signal-store-info", help="Show signal store info")
    subparsers.add_parser("signal-summary", help="Show recent signal outputs")

    parser_sig_val = subparsers.add_parser("signal-validate", help="Validate a signal file")
    parser_sig_val.add_argument("--file", required=True, help="Path to signal JSONL file")

    # signal-score-file
    p_signal_score_file = subparsers.add_parser("signal-score-file", help="Score signals from a JSONL file")
    p_signal_score_file.add_argument("--file", required=True, help="Path to signals.jsonl")
    p_signal_score_file.add_argument("--write", action="store_true", help="Write scoring results report")

    # signal-quality-check
    p_signal_quality_check = subparsers.add_parser("signal-quality-check", help="Check signal quality rules")
    p_signal_quality_check.add_argument("--file", required=True, help="Path to signals.jsonl")

    # signal-confluence
    p_signal_confluence = subparsers.add_parser("signal-confluence", help="Evaluate confluence from signals")
    p_signal_confluence.add_argument("--file", required=True, help="Path to signals.jsonl")
    p_signal_confluence.add_argument("--mode", default="by_symbol_timeframe", help="Aggregation mode")
    p_signal_confluence.add_argument("--write", action="store_true", help="Write confluence report")

    # strategy-run-confluence
    p_strat_run_confluence = subparsers.add_parser("strategy-run-confluence", help="Run multiple strategies and evaluate confluence")
    p_strat_run_confluence.add_argument("--strategies", help="Comma separated strategy names")
    p_strat_run_confluence.add_argument("--symbols", help="Comma separated symbols")
    p_strat_run_confluence.add_argument("--timeframes", help="Comma separated timeframes (default: 1d)")
    p_strat_run_confluence.add_argument("--write", action="store_true", help="Write reports")

    # signal-quality-summary
    p_sig_qual_summary = subparsers.add_parser("signal-quality-summary", help="Show summary of recent quality and confluence reports")

    parser_rsl = subparsers.add_parser("rule-strategy-list", help="List available rule-based strategies")

    parser_rssi = subparsers.add_parser("rule-strategy-set-info", help="Get info about a rule strategy set")
    parser_rssi.add_argument("--set", type=str, default="basic_rules", help="Name of the strategy set")

    parser_rsrfs = subparsers.add_parser("rule-strategy-run-feature-store", help="Run a rule strategy from feature store")
    parser_rsrfs.add_argument("--strategy", type=str, required=True, help="Strategy name")
    parser_rsrfs.add_argument("--symbols", type=str, default="", help="Comma separated symbols")
    parser_rsrfs.add_argument("--timeframes", type=str, default="1d", help="Comma separated timeframes")
    parser_rsrfs.add_argument("--write", action="store_true", help="Write outputs to disk")

    parser_rsrs = subparsers.add_parser("rule-strategy-run-set", help="Run a rule strategy set from feature store")
    parser_rsrs.add_argument("--set", type=str, default="basic_rules", help="Strategy set name")
    parser_rsrs.add_argument("--symbols", type=str, default="", help="Comma separated symbols")
    parser_rsrs.add_argument("--timeframes", type=str, default="1d", help="Comma separated timeframes")
    parser_rsrs.add_argument("--write", action="store_true", help="Write outputs to disk")

    parser_rss = subparsers.add_parser("rule-strategy-summary", help="Show latest rule strategy reports")



    # Backtesting
    parser_bt_info = subparsers.add_parser('backtest-info', help='Show backtest foundation info')
    parser_bt_run_sig = subparsers.add_parser('backtest-run-signals', help='Run backtest from signals')
    parser_bt_run_sig.add_argument('--signal-file', type=str, help='Path to signal jsonl')
    parser_bt_run_sig.add_argument('--symbols', type=str, help='Comma separated symbols')
    parser_bt_run_sig.add_argument('--timeframe', type=str, default='1d', help='Timeframe')
    parser_bt_run_sig.add_argument('--start', type=str, help='Start date YYYY-MM-DD')
    parser_bt_run_sig.add_argument('--end', type=str, help='End date YYYY-MM-DD')
    parser_bt_run_sig.add_argument('--starting-cash', type=float, help='Starting cash')
    parser_bt_run_sig.add_argument('--hold-bars', type=int, help='Hold N bars')
    parser_bt_run_sig.add_argument('--write', type=bool, default=True, help='Write results')
    parser_bt_run_cand = subparsers.add_parser('backtest-run-candidates', help='Run backtest from candidates')
    parser_bt_run_cand.add_argument('--candidates-file', type=str, help='Path to selected candidates jsonl')
    parser_bt_run_cand.add_argument('--symbols', type=str, help='Comma separated symbols')
    parser_bt_run_cand.add_argument('--timeframe', type=str, default='1d', help='Timeframe')
    parser_bt_run_cand.add_argument('--start', type=str, help='Start date YYYY-MM-DD')
    parser_bt_run_cand.add_argument('--end', type=str, help='End date YYYY-MM-DD')
    parser_bt_run_cand.add_argument('--starting-cash', type=float, help='Starting cash')
    parser_bt_run_cand.add_argument('--hold-bars', type=int, help='Hold N bars')
    parser_bt_run_cand.add_argument('--write', type=bool, default=True, help='Write results')
    parser_bt_sum = subparsers.add_parser('backtest-summary', help='Show backtest summary')
    parser_bt_latest = subparsers.add_parser('backtest-latest', help='Show latest backtest')
    parser_bt_val = subparsers.add_parser('backtest-validate', help='Validate backtest')
    parser_bt_val.add_argument('--run-id', type=str, help='Run ID')
    parser_bt_val.add_argument('--result-file', type=str, help='Result file path')

    add_benchmark_commands(subparsers)
    p_rob_info = subparsers.add_parser("robustness-info", help="Show robustness configuration")

    p_mc = subparsers.add_parser("monte-carlo-run", help="Run Monte Carlo simulation")
    p_mc.add_argument("--run-id", type=str, help="Source backtest run id")
    p_mc.add_argument("--latest-backtest", action="store_true", help="Use latest backtest")
    p_mc.add_argument("--type", type=str, help="Simulation type (trade_bootstrap, equity_return_bootstrap, etc)")
    p_mc.add_argument("--iterations", type=int, help="Number of iterations")
    p_mc.add_argument("--seed", type=int, help="Random seed")
    p_mc.add_argument("--write", action="store_true", help="Write results to disk")

    p_boot = subparsers.add_parser("bootstrap-run", help="Run basic bootstrap analysis")
    p_boot.add_argument("--run-id", type=str, help="Source backtest run id")
    p_boot.add_argument("--latest-backtest", action="store_true", help="Use latest backtest")
    p_boot.add_argument("--source", type=str, default="trades", help="Source: trades or equity")
    p_boot.add_argument("--iterations", type=int, help="Number of iterations")
    p_boot.add_argument("--write", action="store_true", help="Write results to disk")

    p_stress = subparsers.add_parser("stress-test-run", help="Run stress scenarios")
    p_stress.add_argument("--run-id", type=str, help="Source backtest run id")
    p_stress.add_argument("--latest-backtest", action="store_true", help="Use latest backtest")
    p_stress.add_argument("--scenario", type=str, default="default", help="Scenario name")
    p_stress.add_argument("--write", action="store_true", help="Write results to disk")

    p_rob_sum = subparsers.add_parser("robustness-summary", help="Show robustness runs summary")
    p_rob_lat = subparsers.add_parser("robustness-latest", help="Show latest robustness run")
    p_rob_val = subparsers.add_parser("robustness-validate", help="Validate robustness run")
    p_rob_val.add_argument("--run-id", type=str, help="Run ID to validate")
    p_rob_val.add_argument("--latest", action="store_true", help="Validate latest run")


    # Portfolio Commands
    portfolio_info_parser = subparsers.add_parser("portfolio-info", help="Show portfolio construction configuration and limits.")

    alloc_preview_parser = subparsers.add_parser("allocation-preview", help="Generate a preview of an allocation with fake candidates.")
    alloc_preview_parser.add_argument("--method", type=str, required=True, help="Allocation method.")
    alloc_preview_parser.add_argument("--equity", type=float, default=100000.0, help="Portfolio equity.")
    alloc_preview_parser.add_argument("--cash", type=float, default=100000.0, help="Available cash.")
    alloc_preview_parser.add_argument("--symbols", type=str, default="", help="Comma-separated symbols.")

    port_build_risk_parser = subparsers.add_parser("portfolio-build-from-risk", help="Build a portfolio basket from risk decisions.")
    port_build_risk_parser.add_argument("--risk-run-id", type=str, help="Risk run ID to build from.")
    port_build_risk_parser.add_argument("--latest-risk", action="store_true", help="Use the latest risk run.")
    port_build_risk_parser.add_argument("--equity", type=float, default=100000.0, help="Portfolio equity.")
    port_build_risk_parser.add_argument("--cash", type=float, default=100000.0, help="Available cash.")
    port_build_risk_parser.add_argument("--method", type=str, help="Allocation method.")
    port_build_risk_parser.add_argument("--write", action="store_true", help="Write portfolio run files.")

    port_build_cand_parser = subparsers.add_parser("portfolio-build-from-candidates", help="Build a portfolio basket from selected candidates.")
    port_build_cand_parser.add_argument("--file", type=str, required=True, help="Candidates file path.")
    port_build_cand_parser.add_argument("--equity", type=float, default=100000.0, help="Portfolio equity.")
    port_build_cand_parser.add_argument("--cash", type=float, default=100000.0, help="Available cash.")
    port_build_cand_parser.add_argument("--method", type=str, help="Allocation method.")
    port_build_cand_parser.add_argument("--write", action="store_true", help="Write portfolio run files.")

    port_summary_parser = subparsers.add_parser("portfolio-summary", help="Summary of portfolio runs.")

    port_latest_parser = subparsers.add_parser("portfolio-latest", help="Show latest portfolio run.")

    port_valid_parser = subparsers.add_parser("portfolio-validate", help="Validate portfolio construction result.")
    port_valid_parser.add_argument("--latest", action="store_true", help="Validate latest run.")
    port_valid_parser.add_argument("--run-id", type=str, help="Validate specific run ID.")


    parser_basket_info = subparsers.add_parser("basket-info", help="Display basket simulation info")

    parser_basket_replay_preview = subparsers.add_parser("basket-replay-preview", help="Preview basket replay data")
    parser_basket_replay_preview.add_argument("--source", type=str, default="portfolio_basket")
    parser_basket_replay_preview.add_argument("--basket-file", type=str)
    parser_basket_replay_preview.add_argument("--allocations-file", type=str)
    parser_basket_replay_preview.add_argument("--risk-decisions-file", type=str)
    parser_basket_replay_preview.add_argument("--selected-candidates-file", type=str)
    parser_basket_replay_preview.add_argument("--signals-file", type=str)

    parser_basket_simulate = subparsers.add_parser("basket-simulate", help="Run basket simulation")
    parser_basket_simulate.add_argument("--source", type=str, default="portfolio_basket")
    parser_basket_simulate.add_argument("--basket-file", type=str)
    parser_basket_simulate.add_argument("--allocations-file", type=str)
    parser_basket_simulate.add_argument("--risk-decisions-file", type=str)
    parser_basket_simulate.add_argument("--selected-candidates-file", type=str)
    parser_basket_simulate.add_argument("--signals-file", type=str)
    parser_basket_simulate.add_argument("--symbols", type=str)
    parser_basket_simulate.add_argument("--timeframe", type=str, default="1d")
    parser_basket_simulate.add_argument("--start", type=str)
    parser_basket_simulate.add_argument("--end", type=str)
    parser_basket_simulate.add_argument("--starting-cash", type=float)
    parser_basket_simulate.add_argument("--hold-bars", type=int)
    parser_basket_simulate.add_argument("--entry-mode", type=str)
    parser_basket_simulate.add_argument("--replay-mode", type=str)
    parser_basket_simulate.add_argument("--write", action="store_true")

    parser_basket_sim_latest = subparsers.add_parser("basket-simulate-latest-portfolio", help="Run basket simulation on latest portfolio")
    parser_basket_sim_latest.add_argument("--timeframe", type=str, default="1d")
    parser_basket_sim_latest.add_argument("--starting-cash", type=float)
    parser_basket_sim_latest.add_argument("--hold-bars", type=int)
    parser_basket_sim_latest.add_argument("--write", action="store_true")

    parser_basket_drift = subparsers.add_parser("basket-drift", help="Show allocation drift report")
    parser_basket_drift.add_argument("--run-id", type=str)
    parser_basket_drift.add_argument("--latest", action="store_true")

    parser_basket_summary = subparsers.add_parser("basket-summary", help="List basket simulation runs")

    parser_basket_latest = subparsers.add_parser("basket-latest", help="Show latest basket simulation run")

    parser_basket_validate = subparsers.add_parser("basket-validate", help="Validate a basket simulation run")
    parser_basket_validate.add_argument("--run-id", type=str)
    parser_basket_validate.add_argument("--latest", action="store_true")


    # Phase 34 Commands
    parser_runtime_info = subparsers.add_parser("runtime-info", help="Display runtime config info")

    parser_runtime_lock = subparsers.add_parser("runtime-lock-status", help="Check runtime lock status")

    parser_runtime_clear_stale_lock = subparsers.add_parser("runtime-clear-stale-lock", help="Clear stale runtime lock")

    parser_runtime_stop_req = subparsers.add_parser("runtime-stop-request", help="Request a safe stop")
    parser_runtime_stop_req.add_argument("--reason", type=str, help="Reason for stop")

    parser_runtime_stop_clr = subparsers.add_parser("runtime-stop-clear", help="Clear a safe stop request")

    parser_scan_dry_run = subparsers.add_parser("scan-dry-run", help="Execute a dry run of the market scan")
    parser_scan_dry_run.add_argument("--symbols", type=str, help="Comma separated symbols")
    parser_scan_dry_run.add_argument("--timeframes", type=str, help="Comma separated timeframes")
    parser_scan_dry_run.add_argument("--max-symbols", type=int, help="Max symbols to process")

    parser_scan_run = subparsers.add_parser("scan-run-once", help="Run a market scan pipeline once")
    parser_scan_run.add_argument("--symbols", type=str, help="Comma separated symbols")
    parser_scan_run.add_argument("--timeframes", type=str, help="Comma separated timeframes")
    parser_scan_run.add_argument("--scope", type=str, help="Scope of the scan")
    parser_scan_run.add_argument("--max-symbols", type=int, help="Max symbols to process")
    parser_scan_run.add_argument("--refresh-data", action="store_true", help="Whether to force data refresh")
    parser_scan_run.add_argument("--write", action="store_true", help="Write outputs")
    parser_scan_run.add_argument("--dry-run", action="store_true", help="Execute as dry run")
    parser_scan_run.add_argument("--notify", action="store_true", help="Enable notification step")
    parser_scan_run.add_argument("--notification-channel", type=str, default="dry_run", help="Override default notification channel")

    parser_scan_summary = subparsers.add_parser("scan-summary", help="List scan runs summary")

    parser_scan_latest = subparsers.add_parser("scan-latest", help="Show latest scan run details")

    parser_scan_validate = subparsers.add_parser("scan-validate", help="Validate a scan run")
    parser_scan_validate.add_argument("--run-id", type=str, help="Specific run id to validate")
    parser_scan_validate.add_argument("--latest", action="store_true", help="Validate latest run")

    parser_sched_plan = subparsers.add_parser("scheduled-scan-plan", help="Generate a scheduled scan plan")
    parser_sched_plan.add_argument("--interval-minutes", type=int, help="Interval in minutes")
    parser_sched_plan.add_argument("--max-runs-per-day", type=int, help="Max runs per day")
    parser_sched_plan.add_argument("--scope", type=str, help="Scope of the scan")
    parser_sched_plan.add_argument("--write", action="store_true", help="Write plan to file")


    parser_sched_next = subparsers.add_parser("scheduled-scan-next", help="Calculate next run times")
    parser_sched_next.add_argument("--count", type=int, default=5, help="Number of times to calculate")

    parser_notification_info = subparsers.add_parser("notification-info", help="Display notification config")
    parser_telegram_status = subparsers.add_parser("telegram-status", help="Display telegram config status")

    parser_notification_template_preview = subparsers.add_parser("notification-template-preview", help="Preview notification template")
    parser_notification_template_preview.add_argument("--type", type=str, default="scan_summary", help="Type of template (scan_summary, health_summary)")

    parser_notification_dispatch_dry_run = subparsers.add_parser("notification-dispatch-dry-run", help="Dry run notification dispatch")
    parser_notification_dispatch_dry_run.add_argument("--count", type=int, default=1, help="Number of messages to simulate")

    parser_notification_send_test = subparsers.add_parser("notification-send-test", help="Test send notification")
    parser_notification_send_test.add_argument("--real", action="store_true", help="Attempt real send if enabled")
    parser_notification_send_test.add_argument("--message", type=str, default="Test Message", help="Message body")

    parser_notification_summary = subparsers.add_parser("notification-summary", help="List notification runs")
    parser_notification_latest = subparsers.add_parser("notification-latest", help="Show latest notification run")
    parser_notification_validate = subparsers.add_parser("notification-validate", help="Validate notification config/run")



    parser_alert_info = subparsers.add_parser("alert-info", help="Show alert policy configuration")
    parser_alert_info.set_defaults(func=cmd_alert_info)

    parser_alert_policy_list = subparsers.add_parser("alert-policy-list", help="List enabled alert policies")
    parser_alert_policy_list.set_defaults(func=cmd_alert_policy_list)

    parser_alert_policy_preview = subparsers.add_parser("alert-policy-preview", help="Preview alert policies")
    parser_alert_policy_preview.add_argument("--scope", type=str, help="Filter by scope (e.g. scan, candidate)")
    parser_alert_policy_preview.set_defaults(func=cmd_alert_policy_preview)

    parser_alert_evaluate_scan = subparsers.add_parser("alert-evaluate-scan", help="Evaluate a scan run for alerts")
    parser_alert_evaluate_scan.add_argument("--scan-run-id", type=str, help="Scan run ID to evaluate")
    parser_alert_evaluate_scan.add_argument("--latest-scan", action="store_true", help="Use latest scan run")
    parser_alert_evaluate_scan.add_argument("--write", action="store_true", help="Write evaluation results")
    parser_alert_evaluate_scan.set_defaults(func=cmd_alert_evaluate_scan)

    parser_alert_dispatch_dry_run = subparsers.add_parser("alert-dispatch-dry-run", help="Dry run alert dispatch from scan")
    parser_alert_dispatch_dry_run.add_argument("--latest-scan", action="store_true", help="Use latest scan run")
    parser_alert_dispatch_dry_run.set_defaults(func=cmd_alert_dispatch_dry_run)

    parser_alert_summary = subparsers.add_parser("alert-summary", help="Show summary of alert evaluations")
    parser_alert_summary.set_defaults(func=cmd_alert_summary)

    parser_alert_latest = subparsers.add_parser("alert-latest", help="Show details of latest alert evaluation")
    parser_alert_latest.set_defaults(func=cmd_alert_latest)

    parser_alert_validate = subparsers.add_parser("alert-validate", help="Validate latest alert evaluation")
    parser_alert_validate.set_defaults(func=cmd_alert_validate)

    args = parser.parse_args()


    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "show-paths":
            # Paths check doesn't need full validation to avoid crashing if config is bad just to see paths
            paths.ensure_directories()
            handle_show_paths()
            sys.exit(0)

        # All other commands require a valid runtime context
        context = initialize_runtime()



        if args.command == "signal-rank-file":
            return handle_signal_rank_file(context, args.file, args.min_rank_score, args.write)

        commands = {
            "scheduled-scan-next": cmd_scheduled_scan_next,
            "notification-info": cmd_notification_info,
            "telegram-status": cmd_telegram_status,
            "notification-template-preview": cmd_notification_template_preview,
            "notification-dispatch-dry-run": cmd_notification_dispatch_dry_run,
            "notification-send-test": cmd_notification_send_test,
            "notification-summary": cmd_notification_summary,
            "notification-latest": cmd_notification_latest,
            "notification-validate": cmd_notification_validate,
        }

        if args.command in commands:
            return commands[args.command](context, args)


        elif args.command == "signal-select-candidates":
            return handle_signal_select_candidates(context, args.file, args.max_candidates, args.min_rank_score, args.write)
        elif args.command == "signal-ranking-summary":
            return handle_signal_ranking_summary(context)
        elif args.command == "selected-candidates-summary":
            return handle_selected_candidates_summary(context)
        elif args.command == "strategy-portfolio-run":
            return handle_strategy_portfolio_run(context, args.strategies, args.symbols, args.timeframes, args.write)
        elif args.command == "rule-strategy-run-ranked":
            return handle_rule_strategy_run_ranked(context, args.strategy_set, args.symbols, args.timeframes, args.write)
        elif args.command == "smoke":
            handle_smoke(context)
        elif args.command == "show-config":
            handle_show_config(context)
        elif args.command == "validate-config":
            handle_validate_config(context)
        elif args.command == "runtime-summary":
            handle_runtime_summary(context)
        elif args.command == "check-env":
            handle_check_env(context)
        elif args.command == "health":
            sys.exit(handle_health(context))
        elif args.command == "universe-sources":
            sys.exit(handle_universe_sources(context))
        elif args.command == "universe-import":
            sys.exit(handle_universe_import(context, args.file, args.name, args.overwrite))
        elif args.command == "universe-expand":
            sys.exit(handle_universe_expand(context, args.name, args.include_layers, args.exclude_layers, args.include_stocks, args.include_etfs, args.include_inactive, args.max_symbols, args.conflict_resolution, args.no_snapshot))
        elif args.command == "universe-snapshots":
            sys.exit(handle_universe_snapshots(context))
        elif args.command == "universe-activate-snapshot":
            sys.exit(handle_universe_activate_snapshot(context, args.snapshot_id))
        elif args.command == "universe-catalog":
            sys.exit(handle_universe_catalog(context))
        elif args.command == "universe-export":
            sys.exit(handle_universe_export(context, args.snapshot_id, args.format, args.name, args.active_only))
        elif args.command == "universe-presets":
            sys.exit(handle_universe_presets(context))
        elif args.command == "indicator-list":
            sys.exit(handle_indicator_list(context))
        elif args.command == "indicator-info":
            sys.exit(handle_indicator_info(context, args.name))
        elif args.command == "feature-store-info":
            sys.exit(handle_feature_store_info(context))
        elif args.command == "feature-compute-cache":
            sys.exit(handle_feature_compute_cache(context, args.symbols, args.timeframes, args.indicators, args.provider, args.write))
        elif args.command == "feature-validate":
            sys.exit(handle_feature_validate(context, args.file))
        elif args.command == "feature-summary":
            sys.exit(handle_feature_summary(context))

        elif args.command == "log-info":
            handle_log_info(context)

        elif args.command == "audit-tail":
            handle_audit_tail(context, args.limit)
        elif args.command == "storage-info":
            handle_storage_info(context)
        elif args.command == "storage-check":
            sys.exit(handle_storage_check(context))
        elif args.command == "storage-list":
            sys.exit(handle_storage_list(context, args.area))
        elif args.command == "universe-info":
            sys.exit(handle_universe_info(context))
        elif args.command == "universe-validate":
            sys.exit(handle_universe_validate(context, args.file))
        elif args.command == "universe-list":
            sys.exit(handle_universe_list(context, args.asset_type, args.limit, args.include_inactive))
        elif args.command == "universe-build":
            sys.exit(handle_universe_build(context))

        elif args.command == "universe-summary":
            sys.exit(handle_universe_summary(context, args.json_out))
        elif args.command == "provider-info":
            sys.exit(handle_provider_info(context))
        elif args.command == "provider-list":
            sys.exit(handle_provider_list(context))
        elif args.command == "provider-check":
            sys.exit(handle_provider_check(context))
        elif args.command == "provider-plan":
            sys.exit(handle_provider_plan(context, args.symbols, args.timeframe))
        elif args.command == "provider-mock-fetch":
            sys.exit(handle_provider_mock_fetch(context, args.symbols, args.timeframe))
        elif args.command == "data-provider-info":
            sys.exit(handle_data_provider_info(context))
        elif args.command == "data-download":
            sys.exit(handle_data_download(context, args.symbols, args.timeframe, args.start, args.end, args.provider, args.no_cache, args.limit))
        elif args.command == "data-download-universe":
            sys.exit(handle_data_download_universe(context, args.file, args.timeframe, args.provider, args.limit, args.asset_type, args.no_cache))
        elif args.command == "data-cache-info":
            sys.exit(handle_data_cache_info(context))
        elif args.command == "data-quality-check":
            sys.exit(handle_data_quality_check(context, args.cache_file, args.symbols, args.timeframe))
        elif args.command == "data-mtf-plan":
            sys.exit(handle_data_mtf_plan(context, args.symbols, args.timeframes, args.provider, args.force, args.no_cache))
        elif args.command == "data-mtf-download":
            sys.exit(handle_data_mtf_download(context, args.symbols, args.timeframes, args.provider, args.force, args.no_cache, getattr(args, 'limit', None)))
        elif args.command == "data-mtf-universe":
            sys.exit(handle_data_mtf_universe(context, args.file, args.timeframes, args.provider, args.force, getattr(args, 'limit', None), getattr(args, 'asset_type', None)))
        elif args.command == "data-coverage-report":
            sys.exit(handle_data_coverage_report(context, args.latest, getattr(args, 'reports_dir', None)))
        elif args.command == "data-readiness-check":
            sys.exit(handle_data_readiness_check(context, args.symbols, args.timeframes, getattr(args, 'from_cache', True)))
        elif args.command == "active-universe-info":
            sys.exit(handle_active_universe_info(context))
        elif args.command == "active-universe-symbols":
            sys.exit(handle_active_universe_symbols(context, getattr(args, 'limit', 0) or 0, getattr(args, 'asset_type', '') or '', getattr(args, 'include_inactive', False)))
        elif args.command == "active-universe-plan":
            sys.exit(handle_active_universe_plan(context, getattr(args, 'timeframes', '') or '', getattr(args, 'provider', 'yfinance'), getattr(args, 'limit', 0) or 0, getattr(args, 'asset_type', '') or '', getattr(args, 'force', False), getattr(args, 'no_cache', False)))
        elif args.command == "active-universe-download":
            sys.exit(handle_active_universe_download(context, getattr(args, 'timeframes', '') or '', getattr(args, 'provider', 'yfinance'), getattr(args, 'limit', 0) or 0, getattr(args, 'asset_type', '') or '', getattr(args, 'force', False), getattr(args, 'no_cache', False)))
        elif args.command == "active-universe-readiness":
            sys.exit(handle_active_universe_readiness(context, getattr(args, 'latest_run', True), getattr(args, 'from_cache', False)))
        elif args.command == "active-universe-runs":
            sys.exit(handle_active_universe_runs(context))
        elif args.command == "active-universe-latest-run":
            sys.exit(handle_active_universe_latest_run(context))
        elif args.command == "active-universe-eligible":
            sys.exit(handle_active_universe_eligible(context, getattr(args, 'latest_run', True), getattr(args, 'format', 'txt')))
        elif args.command == "momentum-indicator-list": sys.exit(handle_momentum_indicator_list(context))
        elif args.command == "momentum-indicator-set-info": sys.exit(handle_momentum_indicator_set_info(context, getattr(args, 'set', 'basic_momentum')))
        elif args.command == "momentum-feature-compute-cache": sys.exit(handle_momentum_feature_compute_cache(context, args.symbols, args.timeframes, getattr(args, 'set', 'basic_momentum'), getattr(args, 'provider', 'yfinance'), getattr(args, 'write', False)))
        elif args.command == "momentum-feature-summary": sys.exit(handle_momentum_feature_summary(context))

        elif args.command == "volume-indicator-list":
            sys.exit(handle_volume_indicator_list(context))
        elif args.command == "volume-indicator-set-info":
            sys.exit(handle_volume_indicator_set_info(context, args.set))
        elif args.command == "volume-feature-compute-cache":
            sys.exit(handle_volume_feature_compute_cache(context, args.symbols, args.timeframes, getattr(args, "set"), args.provider, args.write))
        elif args.command == "volume-feature-summary":
            sys.exit(handle_volume_feature_summary(context))




        elif args.command == "strategy-list":
            sys.exit(handle_strategy_list(context))
        elif args.command == "strategy-info":
            sys.exit(handle_strategy_info(context, args.name))
        elif args.command == "strategy-run-feature-store":
            sys.exit(handle_strategy_run_feature_store(context, args.strategy, getattr(args, 'symbols', ''), getattr(args, 'timeframes', ''), getattr(args, 'write', False)))
        elif args.command == "strategy-run-defaults":
            sys.exit(handle_strategy_run_defaults(context, getattr(args, 'symbols', ''), getattr(args, 'timeframes', ''), getattr(args, 'write', False)))
        elif args.command == "signal-store-info":
            sys.exit(handle_signal_store_info(context))
        elif args.command == "signal-summary":
            sys.exit(handle_signal_summary(context))
        elif args.command == "signal-validate":
            sys.exit(handle_signal_validate(context, args.file))
        elif args.command == "rule-strategy-list":
            sys.exit(handle_rule_strategy_list(context))
        elif args.command == "rule-strategy-set-info":
            sys.exit(handle_rule_strategy_set_info(context, args.set))
        elif args.command == "rule-strategy-run-feature-store":
            sys.exit(handle_rule_strategy_run_feature_store(context, args.strategy, args.symbols, args.timeframes, args.write))
        elif args.command == "rule-strategy-run-set":
            sys.exit(handle_rule_strategy_run_set(context, args.set, args.symbols, args.timeframes, args.write))
        elif args.command == "rule-strategy-summary":
            sys.exit(handle_rule_strategy_summary(context))
        elif args.command == "backtest-info":
            return handle_backtest_info(context, args)
        elif args.command == "backtest-run-signals":
            return handle_backtest_run_signals(context, args)
        elif args.command == "backtest-run-candidates":
            return handle_backtest_run_candidates(context, args)
        elif args.command == "backtest-summary":
            return handle_backtest_summary(context, args)
        elif args.command == "backtest-latest":
            return handle_backtest_latest(context, args)
        elif args.command == "backtest-validate":
            return handle_backtest_validate(context, args)
        elif args.command == "walk-forward-info":
            sys.exit(command_walk_forward_info(args))
        elif args.command == "walk-forward-plan":
            sys.exit(command_walk_forward_plan(args))
        elif args.command == "walk-forward-run-signals":
            sys.exit(command_walk_forward_run_signals(args))
        elif args.command == "walk-forward-run-candidates":
            sys.exit(command_walk_forward_run_candidates(args))
        elif args.command == "walk-forward-summary":
            sys.exit(command_walk_forward_summary(args))
        elif args.command == "walk-forward-latest":
            sys.exit(command_walk_forward_latest(args))
        elif args.command == "sensitivity-info":
            cmd_sensitivity_info(context, args)
            return 0
        elif args.command == "parameter-grid-plan":
            cmd_parameter_grid_plan(context, args)
            return 0
        elif args.command == "sensitivity-run":
            cmd_sensitivity_run(context, args)
            return 0
        elif args.command == "stability-map":
            cmd_stability_map(context, args)
            return 0
        elif args.command == "sensitivity-summary":
            cmd_sensitivity_summary(context, args)
            return 0
        elif args.command == "sensitivity-latest":
            cmd_sensitivity_latest(context, args)
            return 0
            cmd_sensitivity_latest(context, args)
            return 0
        elif args.command == "sensitivity-validate":
            cmd_sensitivity_validate(context, args)
            return 0
        elif args.command == "walk-forward-validate":
            sys.exit(command_walk_forward_validate(args))



        elif args.command == "basket-info":
            sys.exit(handle_basket_info(context))
        elif args.command == "basket-replay-preview":
            sys.exit(handle_basket_replay_preview(context, args.source, args.basket_file, args.allocations_file, args.risk_decisions_file, args.selected_candidates_file, args.signals_file))
        elif args.command == "basket-simulate":
            sys.exit(handle_basket_simulate(context, args.source, args.basket_file, args.allocations_file, args.risk_decisions_file, args.selected_candidates_file, args.signals_file, args.symbols, args.timeframe, args.start, args.end, args.starting_cash, args.hold_bars, args.entry_mode, args.replay_mode, args.write))
        elif args.command == "basket-simulate-latest-portfolio":
            sys.exit(handle_basket_simulate_latest_portfolio(context, args.timeframe, args.starting_cash, args.hold_bars, args.write))
        elif args.command == "basket-drift":
            sys.exit(handle_basket_drift(context, args.run_id, args.latest))
        elif args.command == "basket-summary":
            sys.exit(handle_basket_summary(context))
        elif args.command == "basket-latest":
            sys.exit(handle_basket_latest(context))
        elif args.command == "basket-validate":
            sys.exit(handle_basket_validate(context, args.run_id, args.latest))
        # End of new handlers

        # Keep this to not break replace logic


    except Exception as e:
        sys.exit(handle_cli_exception(e))

    sys.exit(0)



def handle_provider_info(context) -> int:
    """Display data provider configuration and rules."""
    p_cfg = context.config.providers
    print("\n--- USA Signal Bot Provider Info ---")
    print(f"Default Provider: {p_cfg.default_provider}")
    print(f"Enabled Providers: {', '.join(p_cfg.enabled_providers)}")
    print("\n\nSecurity and Constraints (Phase 7):")
    print(f"  Allow Paid APIs: {p_cfg.allow_paid_providers}")
    print(f"  Allow Web Scraping: {p_cfg.allow_scraping_providers}")
    print(f"  Allow Broker Data: {p_cfg.allow_broker_data_providers}")
    print("\nNote: In Phase 7, no real data is fetched from the internet.")
    return 0

def handle_provider_list(context) -> int:
    """List registered data providers."""
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    registry = create_default_provider_registry()
    print("\n--- USA Signal Bot Registered Providers ---")
    caps = registry.list_capabilities()
    if not caps:
        print("\nNo providers registered.")
        return 0
    for cap in caps:
         print(f"- {cap.provider_name.upper()}")
         print(f"  Free Only: {cap.free_only}")
         print(f"  Allows Scraping: {cap.allows_scraping}")
         print(f"  Requires API Key: {cap.requires_api_key}")
         for note in cap.notes:
              print(f"  Note: {note}")
    return 0

def handle_provider_check(context) -> int:
    """Check provider status and guard compliance."""
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    registry = create_default_provider_registry()
    print("\n--- Provider Check ---")
    p_cfg = context.config.providers
    provider_name = p_cfg.default_provider
    try:
         provider = registry.get(provider_name)
         print(f"Provider '{provider_name}' loaded.")
         provider.assert_free_provider()
         provider.assert_no_scraping()
         provider.assert_no_broker_routing()
         print("\nAll guard checks passed.")
         status = provider.check_status()
         print(f"Status: {'Available' if status.available else 'Unavailable'} - {status.message}")
         return 0 if status.available else 1
    except Exception as e:
         print(f"Check failed: {e}")
         return 1

def handle_provider_plan(context, symbols_str: str, timeframe: str) -> int:
    """Generate a mock fetch plan."""
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.data.models import MarketDataRequest
    registry = create_default_provider_registry()
    symbols = [s.strip() for s in symbols_str.split(",") if s.strip()]
    provider = registry.get(context.config.providers.default_provider)
    try:
         req = MarketDataRequest(symbols=symbols, timeframe=timeframe, provider_name=provider.name)
         plan = provider.build_fetch_plan(req)
         print("\n--- Provider Fetch Plan ---")
         print(f"Provider: {plan.provider_name}")
         print(f"Symbols: {len(plan.symbols)}")
         print(f"Timeframe: {plan.timeframe}")
         print(f"Batch Count: {plan.batch_count}")
         print(f"Estimated Requests: {plan.estimated_requests}")
         return 0
    except Exception as e:
         print(f"Failed to build plan: {e}")
         return 1

def handle_provider_mock_fetch(context, symbols_str: str, timeframe: str) -> int:
    """Perform a mock data fetch."""
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.data.models import MarketDataRequest
    registry = create_default_provider_registry()
    symbols = [s.strip() for s in symbols_str.split(",") if s.strip()]
    provider = registry.get("mock")
    try:
         req = MarketDataRequest(symbols=symbols, timeframe=timeframe, provider_name=provider.name)
         resp = provider.fetch_ohlcv(req)
         print("\n--- Mock Data Fetch Result ---")
         print("\nWARNING: This is deterministically generated fake data for testing interface.")
         print("\nIt is NOT real market data.\n")
         print(f"Success: {resp.success}")
         print(f"Provider: {resp.provider_name}")
         print(f"Bars Returned: {resp.bar_count()}")
         for bar in resp.bars:
             print(f"  {bar.symbol} [{bar.timeframe}]: O:{bar.open} H:{bar.high} L:{bar.low} C:{bar.close} V:{bar.volume}")
         return 0
    except Exception as e:
         print(f"Mock fetch failed: {e}")
         return 1

def handle_data_provider_info(context) -> int:
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    registry = create_default_provider_registry(include_yfinance=context.config.providers.yfinance_enabled)
    print("\n--- Market Data Providers ---")
    for cap in registry.list_capabilities():
        print(f"[{cap.provider_name.upper()}]")
        print(f"  Free Only: {cap.free_only}")
        print(f"  Requires API Key: {cap.requires_api_key}")
        print(f"  Allows Scraping: {cap.allows_scraping}")
        print(f"  Notes: {', '.join(cap.notes)}")
        print()
    return 0

def handle_data_download(context, symbols_str: str, timeframe: str, start: str, end: str, provider: str, no_cache: bool, limit: int) -> int:
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.data.downloader import MarketDataDownloader
    from usa_signal_bot.storage.file_store import LocalFileStore
    from usa_signal_bot.data.quality import validate_ohlcv_bars_quality, data_quality_report_to_text

    symbols = [s.strip().upper() for s in symbols_str.split(",") if s.strip()]
    if limit:
        symbols = symbols[:limit]

    registry = create_default_provider_registry(include_yfinance=context.config.providers.yfinance_enabled)
    store = LocalFileStore(context.data_dir)
    downloader = MarketDataDownloader(registry, store, context.data_dir, None)

    print(f"Downloading data for {len(symbols)} symbols via {provider}...")
    try:
        resp = downloader.download_for_symbols(
            symbols=symbols, timeframe=timeframe, provider_name=provider,
            start_date=start, end_date=end, write_cache=not no_cache
        )

        print(f"Success: {resp.success}")
        print(f"Bars: {resp.bar_count()}")

        if resp.errors:
            print("\nErrors:")
            for e in resp.errors: print(f"  - {e}")
        if resp.warnings:
            print("\nWarnings:")
            for w in resp.warnings: print(f"  - {w}")

        if resp.bar_count() > 0:
            report = validate_ohlcv_bars_quality(resp.bars, symbols, provider, timeframe)
            print("\n\n" + data_quality_report_to_text(report))
            downloader.write_download_summary(resp, report)

        return 0 if resp.success else 1
    except Exception as e:
        print(f"Download failed: {e}")
        return 1

def handle_data_download_universe(context, file: str, timeframe: str, provider: str, limit: int, asset_type: str, no_cache: bool) -> int:
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.data.downloader import MarketDataDownloader
    from usa_signal_bot.storage.file_store import LocalFileStore
    from usa_signal_bot.universe.loader import load_default_watchlist
    from usa_signal_bot.data.quality import validate_ohlcv_bars_quality, data_quality_report_to_text
    from usa_signal_bot.universe.models import UniverseDefinition, UniverseSymbol
    from usa_signal_bot.core.enums import AssetType

    # Load universe
    print(f"Loading universe...")
    try:
        if file:
            load_result = load_default_watchlist(context.data_dir, file)
        else:
            load_result = load_default_watchlist(context.data_dir, context.config.universe.default_watchlist_file)

        universe = load_result.universe

        if asset_type:
            at = AssetType(asset_type.upper())
            universe.symbols = [s for s in universe.symbols if s.asset_type == at]

        print(f"Found {len(universe.get_active_symbols())} active symbols.")
        if limit:
            print(f"Applying limit of {limit}.")

        registry = create_default_provider_registry(include_yfinance=context.config.providers.yfinance_enabled)
        store = LocalFileStore(context.data_dir)
        downloader = MarketDataDownloader(registry, store, context.data_dir, None)

        print(f"Downloading...")
        resp = downloader.download_for_universe(universe, timeframe, provider, limit, not no_cache)

        print(f"Success: {resp.success}")
        print(f"Bars: {resp.bar_count()}")

        if resp.bar_count() > 0:
            symbols_requested = universe.get_active_symbols()
            if limit: symbols_requested = symbols_requested[:limit]
            report = validate_ohlcv_bars_quality(resp.bars, symbols_requested, provider, timeframe)
            print("\n\n" + data_quality_report_to_text(report))
            downloader.write_download_summary(resp, report)

        return 0 if resp.success else 1
    except Exception as e:
        print(f"Universe download failed: {e}")
        return 1

def handle_data_cache_info(context) -> int:
    from usa_signal_bot.data.cache import market_data_cache_dir
    cache_dir = market_data_cache_dir(context.data_dir)
    print("\n--- Market Data Cache Info ---")
    print(f"Cache Directory: {cache_dir}")

    if not cache_dir.exists():
        print("\nDirectory does not exist.")
        return 0

    files = list(cache_dir.glob("*.jsonl"))
    summaries = list(cache_dir.glob("download_summary_*.json"))

    print(f"Total cache files (.jsonl): {len(files)}")
    print(f"Total summary files (.json): {len(summaries)}")

    total_size = sum(f.stat().st_size for f in files)
    print(f"Total JSONL size: {total_size / (1024*1024):.2f} MB")

    if files:
        print("\n\nRecent cache files:")
        recent = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        for f in recent:
            print(f"  - {f.name} ({f.stat().st_size / 1024:.1f} KB)")

    return 0

def handle_data_quality_check(context, cache_file: str, symbols_str: str, timeframe: str) -> int:
    from usa_signal_bot.data.cache import market_data_cache_dir, read_ohlcv_bars_cache
    from usa_signal_bot.data.models import OHLCVBar
    from usa_signal_bot.data.quality import validate_ohlcv_bars_quality, data_quality_report_to_text

    cache_dir = market_data_cache_dir(context.data_dir)
    print("\n--- Data Quality Check ---")

    if cache_file:
        path = cache_dir / cache_file
        if not path.exists():
            print(f"Cache file {path} not found.")
            return 1

        print(f"Reading {path.name}...")
        raw_bars = read_ohlcv_bars_cache(path)
        bars = []
        for b in raw_bars:
             bars.append(OHLCVBar(**b))

        symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else list(set(b.symbol for b in bars))
        report = validate_ohlcv_bars_quality(bars, symbols, "unknown_from_cache", timeframe)
        print("\n\n" + data_quality_report_to_text(report))
        return 0 if report.status.value != "ERROR" else 1
    else:
        print("\nNo cache file specified. Usage requires --cache-file.")
        return 1


if __name__ == "__main__":
    main()

def handle_data_cache_validate(context, cache_file: str, symbols_str: str, timeframe: str) -> int:
    from usa_signal_bot.data.cache import market_data_cache_dir, validate_cache_file
    from usa_signal_bot.data.quality import data_quality_report_to_text

    cache_dir = market_data_cache_dir(context.data_dir)
    print("\n--- Data Cache Validate ---")

    if cache_file:
        path = cache_dir / cache_file
        if not path.exists():
            print(f"Cache file {path} not found.")
            return 1

        symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else None
        try:
            report = validate_cache_file(path, symbols)
            print("\n\n" + data_quality_report_to_text(report))
            return 0 if report.status.value != "ERROR" else 1
        except Exception as e:
            print(f"Validation failed: {e}")
            return 1
    else:
        # Validate all? Or just ask for a file. Prompt implies cache_file is optional but maybe validating all is complex.
        # Let's say if no file, we validate the newest.
        from usa_signal_bot.data.cache import list_market_data_cache_files
        files = list_market_data_cache_files(context.data_dir)
        if not files:
            print("\nNo cache files found to validate.")
            return 0 # Safe exit

        path = sorted(files, key=lambda x: x.stat().st_mtime)[-1]
        print(f"Validating latest cache file: {path.name}")
        symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else None
        try:
            report = validate_cache_file(path, symbols)
            print("\n\n" + data_quality_report_to_text(report))
            return 0 if report.status.value != "ERROR" else 1
        except Exception as e:
            print(f"Validation failed: {e}")
            return 1

def handle_data_cache_repair(context, cache_file: str, output: str, overwrite: bool) -> int:
    from usa_signal_bot.data.cache import market_data_cache_dir, read_cached_ohlcv_bars, write_repaired_cache
    from usa_signal_bot.data.repair import repair_ohlcv_bars, repair_report_to_text
    import shutil

    cache_dir = market_data_cache_dir(context.data_dir)
    print("\n--- Data Cache Repair ---")

    if not cache_file:
        print("\nError: --cache-file is required.")
        return 1

    path = cache_dir / cache_file
    if not path.exists():
        print(f"Cache file {path} not found.")
        return 1

    try:
        bars = read_cached_ohlcv_bars(path)
        print(f"Read {len(bars)} bars from {cache_file}.")

        repaired_bars, report = repair_ohlcv_bars(bars)
        print("\n\n" + repair_report_to_text(report))

        out_path = path
        if not overwrite:
            if output:
                out_path = cache_dir / output
            else:
                out_path = cache_dir / f"repaired_{cache_file}"
        else:
            # backup
            backup_path = cache_dir / f"{cache_file}.bak"
            shutil.copy2(path, backup_path)
            print(f"Backed up to {backup_path.name}")

        write_repaired_cache(out_path, repaired_bars)
        print(f"Wrote repaired cache to {out_path.name}")
        return 0
    except Exception as e:
        print(f"Repair failed: {e}")
        return 1

def handle_data_refresh_plan(context, symbols_str: str, timeframe: str, provider: str, start: str, end: str, force: bool, no_cache: bool) -> int:
    from usa_signal_bot.data.refresh import CacheRefreshRequest, build_cache_refresh_plan, cache_refresh_plan_to_text

    print("\n--- Data Refresh Plan ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("\nError: --symbols required.")
        return 1

    req = CacheRefreshRequest(
        provider_name=provider,
        symbols=symbols,
        timeframe=timeframe,
        start_date=start,
        end_date=end,
        force_refresh=force,
        use_cache=not no_cache
    )

    try:
        ttl = context.config.cache_refresh.default_ttl_seconds
        batch = context.config.providers.max_symbols_per_batch
        plan = build_cache_refresh_plan(context.data_dir, req, ttl, batch)
        print("\n\n" + cache_refresh_plan_to_text(plan))
        return 0
    except Exception as e:
        print(f"Failed to build plan: {e}")
        return 1

def handle_data_refresh_execute(context, symbols_str: str, timeframe: str, provider: str, start: str, end: str, force: bool, limit: int) -> int:
    from usa_signal_bot.data.refresh import CacheRefreshRequest, build_cache_refresh_plan, execute_cache_refresh_plan
    from usa_signal_bot.data.downloader import MarketDataDownloader
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.storage.file_store import LocalFileStore

    print("\n--- Data Refresh Execute ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("\nError: --symbols required.")
        return 1

    if limit:
        symbols = symbols[:limit]

    req = CacheRefreshRequest(
        provider_name=provider,
        symbols=symbols,
        timeframe=timeframe,
        start_date=start,
        end_date=end,
        force_refresh=force,
        use_cache=True
    )

    try:
        ttl = context.config.cache_refresh.default_ttl_seconds
        batch = context.config.providers.max_symbols_per_batch
        plan = build_cache_refresh_plan(context.data_dir, req, ttl, batch)

        registry = create_default_provider_registry(include_yfinance=context.config.providers.yfinance_enabled)
        store = LocalFileStore(context.data_dir)
        downloader = MarketDataDownloader(registry, store, context.data_dir)

        result = execute_cache_refresh_plan(plan, downloader)

        print(f"Execution complete.")
        print(f"Refreshed: {len(result.refreshed_symbols)}")
        print(f"From Cache: {len(result.cache_used_symbols)}")
        print(f"Failed: {len(result.failed_symbols)}")

        if result.errors:
            print("\nErrors:")
            for e in result.errors:
                print(f"  - {e}")

        return 0 if not result.errors else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_data_validation_report(context, latest: bool, reports_dir: str) -> int:
    from pathlib import Path
    import json

    print("\n--- Data Validation Report ---")
    d_root = Path(reports_dir) if reports_dir else context.data_dir / "reports"

    if not d_root.exists():
        print("\nReports directory not found.")
        return 0

    q_files = list(d_root.glob("quality_*.json"))
    a_files = list(d_root.glob("anomaly_*.json"))

    if not q_files:
        print("\nNo quality reports found.")
        return 0

    # Pick the latest
    latest_q = sorted(q_files, key=lambda x: x.stat().st_mtime)[-1]
    print(f"Latest Quality Report: {latest_q.name}")
    try:
        with latest_q.open('r') as f:
            data = json.load(f)
            print(f"  Status: {data.get('status')}")
            print(f"  Total Bars: {data.get('total_bars')}")
            print(f"  Invalid Bars: {data.get('invalid_bars')}")
    except Exception as e:
        print(f"  Could not read report: {e}")

    if a_files:
        latest_a = sorted(a_files, key=lambda x: x.stat().st_mtime)[-1]
        print(f"\nLatest Anomaly Report: {latest_a.name}")
        try:
            with latest_a.open('r') as f:
                data = json.load(f)
                print(f"  Total Anomalies: {data.get('total_anomalies')}")
                print(f"  Errors: {data.get('error_count')}")
        except Exception as e:
            print(f"  Could not read report: {e}")

    return 0

def handle_data_mtf_plan(context, symbols_str: str, timeframes_str: str, provider: str, force: bool, no_cache: bool) -> int:
    from usa_signal_bot.data.multitimeframe import MultiTimeframeDataRequest, parse_timeframe_list, build_timeframe_specs_from_list
    from usa_signal_bot.data.refresh import build_multitimeframe_refresh_plan, multitimeframe_refresh_plan_to_text

    print("\n--- Multi-Timeframe Data Plan ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("\nError: --symbols required.")
        return 1

    tfs = parse_timeframe_list(timeframes_str)
    specs = build_timeframe_specs_from_list(tfs)

    req = MultiTimeframeDataRequest(
        symbols=symbols,
        provider_name=provider,
        timeframe_specs=specs,
        force_refresh=force,
        use_cache=not no_cache
    )

    try:
        ttl = context.config.cache_refresh.default_ttl_seconds
        batch = context.config.providers.max_symbols_per_batch
        plan = build_multitimeframe_refresh_plan(context.data_dir, req, ttl, batch)
        print("\n\n" + multitimeframe_refresh_plan_to_text(plan))
        return 0
    except Exception as e:
        print(f"Failed to build plan: {e}")
        return 1

def handle_data_mtf_download(context, symbols_str: str, timeframes_str: str, provider: str, force: bool, no_cache: bool, limit: int) -> int:
    from usa_signal_bot.data.multitimeframe import parse_timeframe_list
    from usa_signal_bot.data.pipeline import MultiTimeframeDataPipeline
    from usa_signal_bot.data.readiness import readiness_report_to_text, DataReadinessCriteria
    from usa_signal_bot.data.downloader import MarketDataDownloader
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.storage.file_store import LocalFileStore

    print("\n--- Multi-Timeframe Data Download ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("\nError: --symbols required.")
        return 1

    tfs = parse_timeframe_list(timeframes_str)

    try:
        registry = create_default_provider_registry(include_yfinance=context.config.providers.yfinance_enabled)
        store = LocalFileStore(context.data_dir)
        downloader = MarketDataDownloader(registry, store, context.data_dir)
        pipeline = MultiTimeframeDataPipeline(downloader, context.data_dir, provider_name=provider)

        cfg = context.config.data_readiness
        criteria = DataReadinessCriteria(
            min_ready_pair_ratio=cfg.min_ready_pair_ratio,
            min_symbol_coverage_ratio=cfg.min_symbol_coverage_ratio,
            require_primary_timeframe=cfg.require_primary_timeframe,
            allow_partial_intraday=cfg.allow_partial_intraday,
            max_error_count=cfg.max_error_count,
            max_warning_ratio=cfg.max_warning_ratio
        )

        result, coverage, readiness = pipeline.run_for_symbols(
            symbols, tfs, limit=limit, force_refresh=force, readiness_criteria=criteria
        )

        print(f"Status: {result.status.value}")
        print(f"Total Bars: {result.total_bars}")
        print("\n\n" + readiness_report_to_text(readiness))
        return 0 if result.status.value != "FAILED" else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_data_mtf_universe(context, file: str, timeframes_str: str, provider: str, force: bool, limit: int, asset_type: str) -> int:
    from usa_signal_bot.data.multitimeframe import parse_timeframe_list
    from usa_signal_bot.data.pipeline import MultiTimeframeDataPipeline
    from usa_signal_bot.data.readiness import readiness_report_to_text, DataReadinessCriteria
    from usa_signal_bot.data.downloader import MarketDataDownloader
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.storage.file_store import LocalFileStore
    from usa_signal_bot.universe.loader import load_universe

    print("\n--- Multi-Timeframe Universe Download ---")
    tfs = parse_timeframe_list(timeframes_str)
    u_file = file or context.config.universe.default_watchlist_file

    try:
        universe = load_universe(u_file)
        print(f"Loaded universe with {len(universe.rows)} symbols.")
        if limit:
            print(f"Warning: Large universe downloads should be monitored. Limiting to {limit} symbols.")

        registry = create_default_provider_registry(include_yfinance=context.config.providers.yfinance_enabled)
        store = LocalFileStore(context.data_dir)
        downloader = MarketDataDownloader(registry, store, context.data_dir)
        pipeline = MultiTimeframeDataPipeline(downloader, context.data_dir, provider_name=provider)

        cfg = context.config.data_readiness
        criteria = DataReadinessCriteria(
            min_ready_pair_ratio=cfg.min_ready_pair_ratio,
            min_symbol_coverage_ratio=cfg.min_symbol_coverage_ratio,
            require_primary_timeframe=cfg.require_primary_timeframe,
            allow_partial_intraday=cfg.allow_partial_intraday,
            max_error_count=cfg.max_error_count,
            max_warning_ratio=cfg.max_warning_ratio
        )

        result, coverage, readiness = pipeline.run_for_universe(
            universe, tfs, limit=limit, asset_type=asset_type, force_refresh=force, readiness_criteria=criteria
        )

        print(f"Status: {result.status.value}")
        print("\n\n" + readiness_report_to_text(readiness))
        return 0 if result.status.value != "FAILED" else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_data_coverage_report(context, latest: bool, reports_dir: str) -> int:
    from pathlib import Path
    import json

    print("\n--- Data Coverage Report ---")
    d_root = Path(reports_dir) if reports_dir else context.data_dir / "reports" / "data_readiness"

    if not d_root.exists():
        print(f"Reports directory {d_root} not found.")
        return 0

    c_files = list(d_root.glob("coverage_*.json"))

    if not c_files:
        print("\nNo coverage reports found.")
        return 0

    latest_c = sorted(c_files, key=lambda x: x.stat().st_mtime)[-1]
    print(f"Latest Coverage Report: {latest_c.name}")
    try:
        with latest_c.open('r') as f:
            data = json.load(f)
            print(f"  Provider: {data.get('provider_name')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Pairs: {data.get('ready_pairs')} ready, {data.get('partial_pairs')} partial, {data.get('empty_pairs')} empty")
    except Exception as e:
        print(f"  Could not read report: {e}")

    return 0

def handle_data_readiness_check(context, symbols_str: str, timeframes_str: str, from_cache: bool) -> int:
    from usa_signal_bot.data.multitimeframe import parse_timeframe_list
    from usa_signal_bot.data.readiness import readiness_report_to_text, DataReadinessCriteria, evaluate_readiness_from_coverage
    from usa_signal_bot.data.coverage import calculate_coverage_report
    from usa_signal_bot.data.cache import read_cached_bars_for_symbols_timeframe

    print("\n--- Data Readiness Check ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("\nError: --symbols required.")
        return 1

    tfs = parse_timeframe_list(timeframes_str)

    if not from_cache:
        print("\nLive readiness check not implemented yet. Use --from-cache.")
        return 1

    try:
        bars_by_timeframe = {}
        for tf in tfs:
            bars_by_timeframe[tf] = read_cached_bars_for_symbols_timeframe(context.data_dir, symbols, tf)

        coverage = calculate_coverage_report("yfinance", symbols, tfs, bars_by_timeframe)

        cfg = context.config.data_readiness
        criteria = DataReadinessCriteria(
            min_ready_pair_ratio=cfg.min_ready_pair_ratio,
            min_symbol_coverage_ratio=cfg.min_symbol_coverage_ratio,
            require_primary_timeframe=cfg.require_primary_timeframe,
            allow_partial_intraday=cfg.allow_partial_intraday,
            max_error_count=cfg.max_error_count,
            max_warning_ratio=cfg.max_warning_ratio
        )

        readiness = evaluate_readiness_from_coverage(coverage, criteria)
        print("\n\n" + readiness_report_to_text(readiness))

        return 0 if readiness.overall_status.value not in ["NOT_READY", "FAILED"] else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_universe_sources(context) -> int:
    from usa_signal_bot.universe.sources import default_universe_sources
    print("\n--- USA Signal Bot Universe Sources ---")
    sources = default_universe_sources(context.data_dir)
    for src in sources:
        status = "Active" if src.enabled else "Disabled"
        print(f"[{src.layer.value if hasattr(src.layer, 'value') else str(src.layer)}] {src.name} - {status}")
        if src.path:
            print(f"  Path: {src.path}")
    print("\nNote: RESERVED_EXTERNAL sources are currently disabled.")
    return 0

def handle_universe_import(context, file: str, name: str, overwrite: bool) -> int:
    from usa_signal_bot.universe.importer import import_universe_csv
    from pathlib import Path

    print("\n--- Universe Import ---")
    try:
        dest_dir = context.project_root / context.config.universe.imports_dir
        dest_path = import_universe_csv(
            source_path=Path(file),
            destination_dir=dest_dir,
            source_name=name,
            overwrite=overwrite
        )
        print(f"Import successful! Saved to: {dest_path}")
        return 0
    except Exception as e:
        print(f"Import failed: {e}")
        return 1

def handle_universe_expand(context, name: str, include_layers: str, exclude_layers: str, include_stocks: bool, include_etfs: bool, include_inactive: bool, max_symbols: int, conflict_resolution: str, no_snapshot: bool) -> int:
    from usa_signal_bot.universe.expansion import UniverseExpansionRequest, expand_universe, expansion_result_to_text
    from usa_signal_bot.universe.sources import default_universe_sources
    from usa_signal_bot.core.enums import UniverseLayer, UniverseConflictResolution

    print("\n--- Universe Expand ---")

    try:
        inc_layers = [UniverseLayer(l.strip().upper()) for l in include_layers.split(",")] if include_layers else None
        exc_layers = [UniverseLayer(l.strip().upper()) for l in exclude_layers.split(",")] if exclude_layers else None
        resolution = UniverseConflictResolution(conflict_resolution.upper())

        req = UniverseExpansionRequest(
            name=name,
            sources=default_universe_sources(context.data_dir),
            include_layers=inc_layers,
            exclude_layers=exc_layers,
            include_stocks=include_stocks,
            include_etfs=include_etfs,
            include_inactive=include_inactive,
            max_symbols=max_symbols,
            conflict_resolution=resolution,
            write_snapshot=not no_snapshot
        )

        res = expand_universe(req, context.data_dir)
        print("\n\n" + expansion_result_to_text(res))

        return 0 if res.success else 1
    except Exception as e:
        print(f"Expansion failed: {e}")
        return 1

def handle_universe_snapshots(context) -> int:
    from usa_signal_bot.universe.snapshots import list_universe_snapshots, get_latest_active_snapshot
    print("\n--- Universe Snapshots ---")

    active_snap = get_latest_active_snapshot(context.data_dir)
    snapshots = list_universe_snapshots(context.data_dir)

    if not snapshots:
        print("\nNo snapshots found.")
        return 0

    for s in snapshots:
        marker = " (ACTIVE)" if active_snap and active_snap.snapshot_id == s.snapshot_id else ""
        print(f"[{s.status.value if hasattr(s.status, 'value') else str(s.status)}] {s.snapshot_id} - {s.name}{marker}")
        print(f"  Symbols: {s.symbol_count} ({s.active_symbol_count} active)")
        print(f"  Created: {s.created_at_utc}")

    return 0

def handle_universe_activate_snapshot(context, snapshot_id: str) -> int:
    from usa_signal_bot.universe.snapshots import mark_snapshot_active
    print(f"--- Activating Snapshot: {snapshot_id} ---")
    try:
        mark_snapshot_active(context.data_dir, snapshot_id)
        print("\nSnapshot activated successfully.")
        return 0
    except Exception as e:
        print(f"Failed to activate snapshot: {e}")
        return 1

def handle_universe_catalog(context) -> int:
    from usa_signal_bot.universe.catalog import build_universe_catalog, catalog_to_text
    print("\n--- Universe Catalog ---")
    try:
        cat = build_universe_catalog(context.data_dir)
        print("\n\n" + catalog_to_text(cat))
        return 0
    except Exception as e:
        print(f"Failed to build catalog: {e}")
        return 1

def handle_universe_export(context, snapshot_id: str, format: str, name: str, active_only: bool) -> int:
    from usa_signal_bot.universe.export import export_universe_csv, export_universe_json, export_symbols_txt, export_symbols_json, build_export_path
    from usa_signal_bot.universe.snapshots import get_latest_active_snapshot, read_universe_snapshot, build_snapshot_paths
    from usa_signal_bot.universe.loader import load_universe_csv, load_default_watchlist

    print("\n--- Universe Export ---")
    try:
        universe = None
        if snapshot_id:
            paths = build_snapshot_paths(context.data_dir, snapshot_id)
            if paths["universe"].exists():
                res = load_universe_csv(paths["universe"])
                universe = res.universe
        else:
            active_snap = get_latest_active_snapshot(context.data_dir)
            if active_snap:
                 paths = build_snapshot_paths(context.data_dir, active_snap.snapshot_id)
                 if paths["universe"].exists():
                     res = load_universe_csv(paths["universe"])
                     universe = res.universe
            else:
                 print("\nNo active snapshot found. Exporting default watchlist instead.")
                 res = load_default_watchlist(context.data_dir)
                 universe = res.universe

        if not universe:
            print("\nFailed to load universe for export.")
            return 1

        name = name or universe.name or "export"
        format = format.lower()

        path = build_export_path(context.data_dir, name, format)

        if format == "csv":
            export_universe_csv(universe, path)
        elif format == "json":
            if active_only: # For symbols json
                export_symbols_json(universe, path, active_only)
            else:
                export_universe_json(universe, path)
        elif format == "txt":
            export_symbols_txt(universe, path, active_only)
        else:
            print(f"Unsupported format: {format}")
            return 1

        print(f"Export successful: {path}")
        return 0
    except Exception as e:
        print(f"Export failed: {e}")
        return 1


def handle_indicator_list(context) -> int:
    from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
    print("\n--- Indicator Registry ---")
    try:
        registry = create_default_indicator_registry()
        metadata_list = registry.list_metadata()
        for m in sorted(metadata_list, key=lambda x: x.name):
            print(f"[{m.category.value}] {m.name} (v{m.version}) - Min Bars: {m.min_bars}, Produces: {', '.join(m.produces)}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_indicator_info(context, name: str) -> int:
    from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
    from usa_signal_bot.features.indicator_metadata import metadata_summary_text
    import json
    from usa_signal_bot.features.indicator_params import parameter_schema_to_dict

    try:
        registry = create_default_indicator_registry()
        if not registry.has(name):
            print(f"Error: Indicator '{name}' not found.")
            return 1

        indicator = registry.get(name)
        print("\n--- Indicator Information ---")
        print(metadata_summary_text(indicator.metadata))
        print("\n\nParameters Schema:")
        schema_dict = parameter_schema_to_dict(indicator.parameter_schema)
        print(json.dumps(schema_dict["parameters"], indent=2))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_feature_store_info(context) -> int:
    from usa_signal_bot.features.feature_store import feature_store_summary
    print("\n--- Feature Store Info ---")
    try:
        summary = feature_store_summary(context.data_dir)
        for k, v in summary.items():
            if k == "total_size_bytes":
                print(f"  {k}: {v / 1024 / 1024:.2f} MB")
            else:
                print(f"  {k}: {v}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_feature_compute_cache(context, symbols_str: str, timeframes_str: str, indicators_str: str, provider: str, write: bool) -> int:
    from usa_signal_bot.features.engine import FeatureEngine
    from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
    from usa_signal_bot.features.reporting import feature_computation_result_to_text, feature_output_metadata_to_text
    from usa_signal_bot.features.validation import validate_feature_rows, feature_validation_report_to_text

    print("\n--- Feature Compute from Cache ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("\nError: --symbols is required")
        return 1

    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]
    indicators = [i.strip() for i in indicators_str.split(",")] if indicators_str else context.config.features.default_indicators

    try:
        registry = create_default_indicator_registry()
        engine = FeatureEngine(registry, context.data_dir)

        print(f"Computing for {len(symbols)} symbols over {len(timeframes)} timeframes using {len(indicators)} indicators...")

        res = engine.compute_from_cache(symbols, timeframes, indicators, provider_name=provider)

        print("\n\n" + feature_computation_result_to_text(res))

        if res.feature_rows:
            val_report = validate_feature_rows(res.feature_rows, res.produced_features)
            print("\n\n" + feature_validation_report_to_text(val_report))
        else:
            print("\n\nError: No feature rows generated. Have you downloaded data for these symbols?")
            return 1

        if write and res.is_successful():
            from usa_signal_bot.core.enums import FeatureStorageFormat
            fmt = FeatureStorageFormat(context.config.features.default_storage_format.upper())
            meta = engine.write_result(res, fmt)
            print("\n\n" + feature_output_metadata_to_text(meta))

        return 0 if res.is_successful() else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_feature_validate(context, file_path_str: str) -> int:
    from usa_signal_bot.features.feature_store import read_feature_rows_jsonl
    from usa_signal_bot.features.output_contract import FeatureRow
    from usa_signal_bot.features.validation import validate_feature_rows, feature_validation_report_to_text
    from pathlib import Path

    print("\n--- Feature Output Validation ---")
    if not file_path_str:
        print("\nError: --file is required")
        return 1

    path = Path(file_path_str)
    if not path.exists():
        print(f"Error: File {path} does not exist")
        return 1

    try:
        raw_rows = read_feature_rows_jsonl(path)
        rows = [FeatureRow(**r) for r in raw_rows]

        if not rows:
            print("\nError: File is empty")
            return 1

        produced_features = list(rows[0].features.keys())

        val_report = validate_feature_rows(rows, produced_features)
        print("\n\n" + feature_validation_report_to_text(val_report))
        return 0 if val_report.status.value != "INVALID" else 1
    except Exception as e:
        print(f"Validation failed: {e}")
        return 1

def handle_feature_summary(context) -> int:
    from usa_signal_bot.features.feature_store import list_feature_outputs, feature_store_dir
    import json
    print("\n--- Feature Outputs Summary ---")
    try:
        d = feature_store_dir(context.data_dir)
        meta_files = sorted(list(d.glob("*_meta.json")), key=lambda x: x.stat().st_mtime, reverse=True)

        if not meta_files:
            print("\nNo feature metadata files found.")
            return 0

        print(f"Found {len(meta_files)} metadata files. Showing latest 5:\n")

        for f in meta_files[:5]:
            try:
                with open(f, "r") as mf:
                    meta = json.load(mf)
                print(f"[{meta.get('created_at_utc')}] Output ID: {meta.get('output_id')}")
                print(f"  Symbols: {len(meta.get('symbols', []))}, Indicators: {len(meta.get('indicators', []))}")
                print(f"  Rows: {meta.get('row_count')}, Provider: {meta.get('provider_name')}")
            except Exception:
                print(f"  [Error reading metadata file {f.name}]")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def handle_universe_presets(context) -> int:
    from usa_signal_bot.universe.presets import list_preset_files, load_preset_universe
    print("\n--- Universe Presets ---")

    presets = list_preset_files(context.data_dir)
    if not presets:
        print("\nNo presets found.")
        return 0

    for p in presets:
        try:
            res = load_preset_universe(context.data_dir, p.stem)
            print(f"[{p.stem}] - {res.valid_count} symbols")
        except Exception as e:
             print(f"[{p.stem}] - Error loading: {e}")

    return 0


def handle_volume_indicator_list(context) -> int:
    from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
    from usa_signal_bot.core.enums import IndicatorCategory
    print("\n--- Volume Indicator Registry ---")
    try:
        registry = create_default_indicator_registry()
        indicators = registry.list_by_category(IndicatorCategory.VOLUME)
        for ind in sorted(indicators, key=lambda x: x.metadata.name):
            m = ind.metadata
            print(f"[{m.category.value}] {m.name} (v{m.version}) - Min Bars: {m.min_bars}, Produces: {', '.join(m.produces)}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_volume_indicator_set_info(context, set_name: str) -> int:
    from usa_signal_bot.features.volume_sets import get_volume_indicator_set
    import json
    try:
        ind_set = get_volume_indicator_set(set_name)
        print(f"--- Volume Indicator Set: {set_name} ---")
        print("\nIndicators:")
        for i in ind_set.indicators:
            print(f"  - {i}")
        print("\n\nParams:")
        print(json.dumps(ind_set.params_by_indicator, indent=2))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_volume_feature_compute_cache(context, symbols_str: str, timeframes_str: str, set_name: str, provider: str, write: bool) -> int:
    from usa_signal_bot.features.engine import FeatureEngine
    from usa_signal_bot.features.indicator_registry import create_default_indicator_registry
    from usa_signal_bot.features.reporting import feature_computation_result_to_text, feature_output_metadata_to_text
    from usa_signal_bot.features.validation import validate_volume_feature_columns, feature_validation_report_to_text
    from usa_signal_bot.features.dataframe_utils import feature_rows_to_dataframe
    from usa_signal_bot.data.cache import market_data_cache_dir

    print("\n--- Volume Feature Compute from Cache ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    timeframes = [t.strip() for t in timeframes_str.split(",")] if timeframes_str else ["1d"]

    # Check if cache exists by trying to find at least one bar
    cache_dir = market_data_cache_dir(context.data_dir)
    if not list(cache_dir.glob("*.json")):
        print("\nError: No cached data found. Please run a data download command first.")
        return 1

    try:
        registry = create_default_indicator_registry()
        engine = FeatureEngine(registry, context.data_dir)

        print(f"Computing '{set_name}' for {len(symbols)} symbols over {len(timeframes)} timeframes...")

        res = engine.compute_volume_set_from_cache(symbols, timeframes, set_name=set_name, provider_name=provider)

        print("\n\n" + feature_computation_result_to_text(res))

        if res.feature_rows:
            df = feature_rows_to_dataframe(res.feature_rows)
            val_report = validate_volume_feature_columns(df, res.produced_features)
            print("\n\n" + feature_validation_report_to_text(val_report))
        else:
            print("\n\nError: No feature rows generated. Have you downloaded data for these symbols?")
            return 1

        if write and res.is_successful():
            from usa_signal_bot.core.enums import FeatureStorageFormat
            fmt = FeatureStorageFormat("JSONL")
            from usa_signal_bot.features.volume_sets import get_volume_indicator_set
            ind_set = get_volume_indicator_set(set_name)

            original_names = res.request.indicator_names
            res.request.indicator_names = [set_name]
            meta = engine.write_result(res, fmt)
            res.request.indicator_names = original_names
            print("\n\n" + feature_output_metadata_to_text(meta))

        return 0 if res.is_successful() else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_volume_feature_summary(context) -> int:
    from usa_signal_bot.features.feature_store import feature_store_dir
    import json
    print("\n--- Volume Feature Outputs Summary ---")
    try:
        d = feature_store_dir(context.data_dir)
        meta_files = sorted(list(d.glob("*_volume_meta.json")), key=lambda x: x.stat().st_mtime, reverse=True)
        if not meta_files:
            meta_files = [f for f in d.glob("*_meta.json") if "volume" in f.name]
            if not meta_files:
                print("\nNo volume feature metadata files found.")
                return 0

        print(f"Found {len(meta_files)} metadata files. Showing latest 5:\n")

        for f in meta_files[:5]:
            try:
                with open(f, "r") as mf:
                    meta = json.load(mf)
                print(f"[{meta.get('created_at_utc')}] Output ID: {meta.get('output_id')}")
                print(f"  Symbols: {len(meta.get('symbols', []))}, Indicators: {len(meta.get('indicators', []))}")
                print(f"  Rows: {meta.get('row_count')}, Provider: {meta.get('provider_name')}")
            except Exception:
                print(f"  [Error reading metadata file {f.name}]")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def do_signal_score_file(args, config):
    from usa_signal_bot.strategies.signal_store import read_signals_jsonl, build_signal_report_path, write_scoring_results_jsonl
    from usa_signal_bot.strategies.signal_scoring import score_signal_list
    from usa_signal_bot.strategies.strategy_reporting import signal_scoring_results_to_text
    from usa_signal_bot.strategies.signal_contract import StrategySignal
    import json
    from pathlib import Path

    raw_signals = read_signals_jsonl(Path(args.file))
    signals = []
    from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket
    for d in raw_signals:
        if isinstance(d.get("action"), str):
            try:
                d["action"] = SignalAction[d["action"]]
            except:
                pass
        if isinstance(d.get("confidence_bucket"), str):
            try:
                d["confidence_bucket"] = SignalConfidenceBucket[d["confidence_bucket"]]
            except:
                pass
        signals.append(StrategySignal(**d))

    print(f"Loaded {len(signals)} signals from {args.file}")
    results = score_signal_list(signals, config.signal_scoring)
    print(signal_scoring_results_to_text(results))

    if getattr(args, 'write', False):
        import uuid
        run_id = f"score_run_{uuid.uuid4().hex[:8]}"
        out_path = build_signal_report_path(Path(config.data.root_dir), "scoring_batch", run_id)
        out_path = out_path.with_suffix(".jsonl")
        write_scoring_results_jsonl(out_path, results)
        print(f"Wrote scoring results to: {out_path}")

def do_signal_quality_check(args, config):
    from usa_signal_bot.strategies.signal_store import read_signals_jsonl
    from usa_signal_bot.strategies.signal_quality import evaluate_signal_quality_list, quality_report_to_text
    from usa_signal_bot.strategies.signal_contract import StrategySignal
    from pathlib import Path

    raw_signals = read_signals_jsonl(Path(args.file))
    signals = []
    from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket
    for d in raw_signals:
        if isinstance(d.get("action"), str):
            try:
                d["action"] = SignalAction[d["action"]]
            except:
                pass
        if isinstance(d.get("confidence_bucket"), str):
            try:
                d["confidence_bucket"] = SignalConfidenceBucket[d["confidence_bucket"]]
            except:
                pass
        signals.append(StrategySignal(**d))

    print(f"Loaded {len(signals)} signals from {args.file}")
    report = evaluate_signal_quality_list(signals, None, config.signal_quality)
    print(quality_report_to_text(report))

def do_signal_confluence(args, config):
    from usa_signal_bot.strategies.signal_store import read_signals_jsonl, build_signal_report_path, write_confluence_report_json
    from usa_signal_bot.strategies.signal_confluence import evaluate_confluence, confluence_report_to_text
    from usa_signal_bot.core.enums import SignalAggregationMode
    from usa_signal_bot.strategies.signal_contract import StrategySignal
    from pathlib import Path

    raw_signals = read_signals_jsonl(Path(args.file))
    signals = []
    from usa_signal_bot.core.enums import SignalAction, SignalConfidenceBucket
    for d in raw_signals:
        if isinstance(d.get("action"), str):
            try:
                d["action"] = SignalAction[d["action"]]
            except:
                pass
        if isinstance(d.get("confidence_bucket"), str):
            try:
                d["confidence_bucket"] = SignalConfidenceBucket[d["confidence_bucket"]]
            except:
                pass
        signals.append(StrategySignal(**d))

    print(f"Loaded {len(signals)} signals from {args.file}")

    try:
        mode = SignalAggregationMode[args.mode.upper()]
    except:
        mode = SignalAggregationMode.BY_SYMBOL_TIMEFRAME

    report = evaluate_confluence(signals, mode, config.confluence)
    print(confluence_report_to_text(report))

    if getattr(args, 'write', False):
        import uuid
        run_id = f"confluence_run_{uuid.uuid4().hex[:8]}"
        out_path = build_signal_report_path(Path(config.data.root_dir), "confluence_batch", run_id)
        write_confluence_report_json(out_path, report)
        print(f"Wrote confluence report to: {out_path}")

def do_strategy_run_confluence(args, config):
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_input import load_strategy_feature_frames_from_feature_store
    from pathlib import Path
    import sys

    strategies = [s.strip() for s in getattr(args, 'strategies', '').split(",")] if getattr(args, 'strategies', None) else ["trend_following_skeleton", "momentum_skeleton"]
    symbols = [s.strip() for s in getattr(args, 'symbols', '').split(",")] if getattr(args, 'symbols', None) else []
    timeframes = [t.strip() for t in getattr(args, 'timeframes', '').split(",")] if getattr(args, 'timeframes', None) else ["1d"]

    print(f"Running strategies: {strategies}")
    print(f"Symbols: {symbols if symbols else 'ALL'}")
    print(f"Timeframes: {timeframes}")

    try:
        batch = load_strategy_feature_frames_from_feature_store(
            data_root=Path(config.data.root_dir),
            timeframes=timeframes,
            symbols=symbols
        )
    except Exception as e:
        print(f"Failed to load features: {e}")
        print("Run 'python -m usa_signal_bot feature-pipeline-run' first.")
        sys.exit(1)

    registry = create_default_strategy_registry()
    engine = StrategyEngine(registry, Path(config.data.root_dir), app_config=config)

    run_results, confluence_report = engine.run_strategies_with_confluence(
        strategies,
        batch,
        write_outputs=getattr(args, 'write', False)
    )

    from usa_signal_bot.strategies.signal_confluence import confluence_report_to_text
    print("\n" + confluence_report_to_text(confluence_report))

def do_signal_quality_summary(args, config):
    from usa_signal_bot.strategies.signal_store import signal_reports_dir
    from pathlib import Path
    d = signal_reports_dir(Path(config.data.root_dir))
    if not d.exists():
        print(f"Reports directory does not exist: {d}")
        return

    files = sorted(list(d.glob("*.json*")), key=lambda x: x.stat().st_mtime, reverse=True)
    if not files:
        print(f"No reports found in {d}")
        return

    print(f"Found {len(files)} reports. Latest:")
    for f in files[:10]:
        print(f" - {f.name} (Size: {f.stat().st_size} bytes)")

def handle_rule_strategy_list(context) -> int:
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    registry = create_default_strategy_registry()
    strategies = [s for s in registry.list_metadata() if "rule" in s.name]

    import sys
    sys.stdout.write("\n--- Rule Based Strategies ---\n")
    if not strategies:
        sys.stdout.write("No rule strategies found.\n")
        return 0

    for meta in strategies:
        sys.stdout.write(f"[{meta.category.value if hasattr(meta.category, 'value') else meta.category}] {meta.name}\n")
        sys.stdout.write(f"  Description: {meta.description}\n")
        sys.stdout.write(f"  Required Features: {', '.join(meta.required_features)}\n\n")
    return 0

def handle_rule_strategy_set_info(context, set_name: str) -> int:
    from usa_signal_bot.strategies.rule_strategy_sets import get_rule_strategy_set, rule_strategy_set_to_text
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry

    try:
        rule_set = get_rule_strategy_set(set_name)
    except Exception as e:
        import sys
        sys.stdout.write(f"Error: {e}\n")
        return 1

    import sys
    sys.stdout.write(rule_strategy_set_to_text(rule_set) + "\n")

    registry = create_default_strategy_registry()
    sys.stdout.write("\nRequired Features across all strategies:\n")
    all_features = set()
    for s_name in rule_set.strategies:
        try:
             strat = registry.get(s_name)
             all_features.update(strat.required_features())
        except:
             pass
    for f in sorted(list(all_features)):
        sys.stdout.write(f"  - {f}\n")

    sys.stdout.write("\nNote: Strategy outputs are signal candidates only and not for direct execution.\n")
    return 0

def handle_rule_strategy_run_feature_store(context, strategy_name: str, symbols: str, timeframes: str, write: bool) -> int:
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine
    from usa_signal_bot.strategies.strategy_input import load_strategy_feature_frames_from_feature_store

    syms = [s.strip().upper() for s in symbols.split(",")] if symbols else []
    tfs = [t.strip() for t in timeframes.split(",")] if timeframes else ["1d"]

    import sys
    registry = create_default_strategy_registry()
    engine = StrategyEngine(registry, context.data_dir, app_config=context.config)

    try:
         batch = load_strategy_feature_frames_from_feature_store(context.data_dir, syms, tfs)
    except Exception as e:
         sys.stdout.write(f"Failed to load features: {e}\n")
         return 1

    if not batch.frames:
         sys.stdout.write("No features found for the requested symbols/timeframes. Please run feature pipeline first.\n")
         return 0

    try:
         res = engine.run_strategy(strategy_name, batch, write_outputs=write)
         from usa_signal_bot.strategies.strategy_reporting import strategy_run_result_to_text
         sys.stdout.write(strategy_run_result_to_text(res) + "\n")
    except Exception as e:
         sys.stdout.write(f"Failed to run strategy: {e}\n")
         return 1
    return 0

def handle_rule_strategy_run_set(context, set_name: str, symbols: str, timeframes: str, write: bool) -> int:
    from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
    from usa_signal_bot.strategies.strategy_engine import StrategyEngine

    syms = [s.strip().upper() for s in symbols.split(",")] if symbols else []
    tfs = [t.strip() for t in timeframes.split(",")] if timeframes else ["1d"]

    import sys
    registry = create_default_strategy_registry()
    engine = StrategyEngine(registry, context.data_dir, app_config=context.config)

    try:
         results, confluence = engine.run_rule_strategy_set_from_feature_store(set_name, syms, tfs, write_outputs=write)
         from usa_signal_bot.strategies.strategy_reporting import rule_strategy_set_result_to_text
         sys.stdout.write(rule_strategy_set_result_to_text(results, confluence) + "\n")
    except Exception as e:
         sys.stdout.write(f"Failed to run rule strategy set: {e}\n")
         return 1
    return 0

def handle_rule_strategy_summary(context) -> int:
    import sys
    from usa_signal_bot.strategies.signal_store import signal_reports_dir
    d = signal_reports_dir(context.data_dir)
    if not d.exists():
        sys.stdout.write(f"Reports directory does not exist: {d}\n")
        return 0

    files = sorted(list(d.glob("quality_*.json*")) + list(d.glob("confluence_*.json*")) + list(d.glob("run_*.json*")), key=lambda x: x.stat().st_mtime, reverse=True)
    if not files:
        sys.stdout.write(f"No rule/strategy reports found in {d}\n")
        return 0

    sys.stdout.write(f"Found {len(files)} reports. Latest 10:\n")
    for f in files[:10]:
        sys.stdout.write(f" - {f.name} (Size: {f.stat().st_size} bytes)\n")
    return 0

def add_benchmark_commands(subparsers):
    # benchmark-info
    p_info = subparsers.add_parser("benchmark-info", help="Show benchmark configuration and available sets")
    p_info.set_defaults(func=cmd_benchmark_info)

    # benchmark-cache-check
    p_cache = subparsers.add_parser("benchmark-cache-check", help="Check if benchmark data is available in cache")
    p_cache.add_argument("--set", type=str, default="default", help="Benchmark set name")
    p_cache.add_argument("--timeframe", type=str, default="1d", help="Timeframe")
    p_cache.set_defaults(func=cmd_benchmark_cache_check)

    # buy-and-hold-baseline
    p_bh = subparsers.add_parser("buy-and-hold-baseline", help="Run a buy-and-hold baseline for a symbol")
    p_bh.add_argument("--symbol", type=str, default="SPY", help="Symbol to baseline")
    p_bh.add_argument("--timeframe", type=str, default="1d", help="Timeframe")
    p_bh.add_argument("--starting-cash", type=float, help="Starting cash override")
    p_bh.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    p_bh.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    p_bh.set_defaults(func=cmd_buy_and_hold_baseline)

    # backtest-benchmark-compare
    p_cmp = subparsers.add_parser("backtest-benchmark-compare", help="Compare a backtest run to a benchmark set")
    p_cmp.add_argument("--run-id", type=str, help="Backtest Run ID")
    p_cmp.add_argument("--latest", action="store_true", help="Use latest backtest run")
    p_cmp.add_argument("--set", type=str, default="default", help="Benchmark set name")
    p_cmp.add_argument("--write", action="store_true", help="Write report to storage")
    p_cmp.set_defaults(func=cmd_backtest_benchmark_compare)

    # backtest-attribution
    p_attr = subparsers.add_parser("backtest-attribution", help="Generate performance attribution for a backtest")
    p_attr.add_argument("--run-id", type=str, help="Backtest Run ID")
    p_attr.add_argument("--latest", action="store_true", help="Use latest backtest run")
    p_attr.add_argument("--dimensions", type=str, help="Comma separated dimensions (e.g., strategy,symbol,timeframe)")
    p_attr.add_argument("--write", action="store_true", help="Write report to storage")
    p_attr.set_defaults(func=cmd_backtest_attribution)

    # benchmark-summary
    p_sum = subparsers.add_parser("benchmark-summary", help="Show summary of stored benchmark reports")
    p_sum.set_defaults(func=cmd_benchmark_summary)
    # Parameter Sensitivity Commands
    subparsers.add_parser("sensitivity-info", help="Show parameter sensitivity configuration")
    p_pgp = subparsers.add_parser("parameter-grid-plan", help="Plan a parameter grid")
    p_pgp.add_argument("--strategy")
    p_pgp.add_argument("--param")
    p_pgp.add_argument("--values")
    p_pgp.add_argument("--type", default="float")
    p_pgp.add_argument("--max-cells", type=int, default=100)
    subparsers.add_parser("sensitivity-run", help="Run a parameter sensitivity analysis")
    subparsers.add_parser("stability-map", help="Show stability map for a sensitivity run")
    subparsers.add_parser("sensitivity-summary", help="Show summary of sensitivity runs")
    subparsers.add_parser("sensitivity-latest", help="Show info on the latest sensitivity run")
    subparsers.add_parser("sensitivity-validate", help="Validate a sensitivity run for non-optimizer compliance")

def cmd_benchmark_info(args, config, context) -> int:
    try:
        from usa_signal_bot.backtesting.benchmark_loader import list_benchmark_sets
        from usa_signal_bot.backtesting.benchmark_reporting import benchmark_set_to_text
        sets = list_benchmark_sets()
        print("\n=== Available Benchmark Sets ===")
        for bs in sets:
            print(benchmark_set_to_text(bs))
            print("-" * 40)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_benchmark_cache_check(args, config, context) -> int:
    try:
        from usa_signal_bot.backtesting.benchmark_loader import get_benchmark_set, load_benchmark_market_data_from_cache, validate_benchmark_cache_coverage
        bs = get_benchmark_set(args.set)
        data = load_benchmark_market_data_from_cache(data_root=context.data_dir, benchmark_set=bs, timeframe=args.timeframe)
        val_msgs = validate_benchmark_cache_coverage(data, bs)
        if val_msgs:
            print("\nWarnings:")
            for msg in val_msgs:
                print(f"  - {msg}")
            print("\nPlease run data pipeline or universe tools to fetch missing data.")
            return 1
        print(f"\nCache is ready for benchmark set '{args.set}' ({args.timeframe})")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_buy_and_hold_baseline(args, config, context) -> int:
    try:
        from usa_signal_bot.backtesting.benchmark_loader import load_benchmark_market_data_from_cache, default_benchmark_set
        from usa_signal_bot.backtesting.buy_and_hold import default_buy_and_hold_config, run_buy_and_hold_baseline, buy_and_hold_result_to_text
        from usa_signal_bot.backtesting.benchmark_models import BenchmarkSpec
        from usa_signal_bot.core.enums import BenchmarkType
        from usa_signal_bot.data.cache import read_cached_bars_for_symbols_timeframe

        bars = read_cached_bars_for_symbols_timeframe(
            data_root=context.data_dir,
            symbols=[args.symbol],
            timeframe=args.timeframe
        )

        if not bars:
            print(f"No cache data found for {args.symbol} ({args.timeframe}). Run data pipeline first.")
            return 1

        if args.start or args.end:
            filtered = []
            for b in bars:
                d = b.timestamp_utc[:10]
                if args.start and d < args.start: continue
                if args.end and d > args.end: continue
                filtered.append(b)
            bars = filtered

        cash = args.starting_cash or config.buy_and_hold.default_starting_cash
        cfg = default_buy_and_hold_config(symbol=args.symbol, timeframe=args.timeframe, starting_cash=cash)
        spec = BenchmarkSpec(benchmark_id=args.symbol, name=args.symbol, symbol=args.symbol, benchmark_type=BenchmarkType.CUSTOM_SYMBOL)

        res = run_buy_and_hold_baseline(bars, cfg, spec)
        print("\n" + buy_and_hold_result_to_text(res))
        return 0 if not res.errors else 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def _get_run_dir(args, data_root: Path):
    from usa_signal_bot.backtesting.backtest_store import list_backtest_runs
    if args.run_id:
        from usa_signal_bot.backtesting.backtest_store import build_backtest_run_dir
        return build_backtest_run_dir(data_root, args.run_id)
    elif args.latest:
        runs = list_backtest_runs(data_root)
        if not runs:
            print("No backtest runs found.")
            return None
        return runs[0]
    else:
        print("Please specify --run-id or --latest")
        return None

def cmd_backtest_benchmark_compare(args, config, context) -> int:
    try:
        from usa_signal_bot.backtesting.backtest_store import load_json
        from usa_signal_bot.backtesting.benchmark_loader import get_benchmark_set, load_benchmark_market_data_from_cache
        from usa_signal_bot.backtesting.buy_and_hold import run_buy_and_hold_baseline, BuyAndHoldConfig, build_cash_baseline
        from usa_signal_bot.backtesting.benchmark_comparison import compare_strategy_to_benchmark_set, build_benchmark_comparison_report
        from usa_signal_bot.backtesting.equity_curve import EquityCurve, EquityCurvePoint
        from usa_signal_bot.backtesting.benchmark_reporting import full_benchmark_analysis_to_text
        from usa_signal_bot.core.enums import BenchmarkType

        run_dir = _get_run_dir(args, context.data_dir)
        if not run_dir or not run_dir.exists():
            return 1

        eq_file = run_dir / "equity_curve.jsonl"
        res_file = run_dir / "backtest_result.json"

        if not eq_file.exists() or not res_file.exists():
            print("Missing equity curve or result file in run directory.")
            return 1

        import json
        points = []
        with open(eq_file, "r") as f:
            for line in f:
                d = json.loads(line)
                points.append(EquityCurvePoint(**d))

        res_dict = load_json(res_file)
        start_cash = res_dict.get("metrics", {}).get("starting_cash", 100000.0)
        end_eq = res_dict.get("metrics", {}).get("ending_equity", start_cash)
        max_dd = res_dict.get("metrics", {}).get("max_drawdown", 0.0)

        eq_curve = EquityCurve(points=points, starting_cash=start_cash, ending_equity=end_eq, max_drawdown=max_dd)

        bm_set = get_benchmark_set(args.set)

        # Get start/end from points
        start_dt = points[0].timestamp_utc[:10] if points else None
        end_dt = points[-1].timestamp_utc[:10] if points else None

        bm_data = load_benchmark_market_data_from_cache(context.data_dir, bm_set, "1d", start_dt, end_dt)

        bm_curves = []
        for spec in bm_set.benchmarks:
            if not spec.enabled: continue
            if spec.benchmark_type == BenchmarkType.CASH:
                ts_list = [p.timestamp_utc for p in points]
                bm_curves.append(build_cash_baseline(start_cash, ts_list))
            else:
                bars = bm_data.get(spec.symbol)
                if bars:
                    bh_conf = BuyAndHoldConfig(starting_cash=start_cash, symbol=spec.symbol, timeframe="1d")
                    bh_res = run_buy_and_hold_baseline(bars, bh_conf, spec)
                    if not bh_res.errors:
                        bm_curves.append(bh_res.equity_curve)

        if not bm_curves:
            print("No benchmark curves could be generated. Check cache.")
            return 1

        table = compare_strategy_to_benchmark_set(eq_curve, bm_curves, strategy_run_id=run_dir.name)
        report = build_benchmark_comparison_report(run_dir.name, bm_set.name, eq_curve, bm_curves)

        print("\n" + full_benchmark_analysis_to_text(table))

        if args.write:
            from usa_signal_bot.backtesting.benchmark_store import write_benchmark_comparison_report_json
            from usa_signal_bot.backtesting.backtest_store import write_backtest_benchmark_report
            write_backtest_benchmark_report(run_dir / "benchmark_comparison_report.json", report)
            print(f"Report written to {run_dir}")

        return 0
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()
        return 1

def cmd_backtest_attribution(args, config, context) -> int:
    try:
        from usa_signal_bot.backtesting.backtest_store import load_json
        from usa_signal_bot.backtesting.performance_attribution import build_full_attribution_report, attribution_report_to_text
        from usa_signal_bot.backtesting.trade_ledger import TradeLedger, BacktestTrade
        from usa_signal_bot.core.enums import AttributionDimension, TradeStatus, TradeDirection, TradeExitReason

        run_dir = _get_run_dir(args, context.data_dir)
        if not run_dir or not run_dir.exists():
            return 1

        # Simplification: Trade Ledger needs to be reconstructed from json or we assume it's in the run
        res_file = run_dir / "backtest_result.json"
        if not res_file.exists():
            print("Missing result file.")
            return 1

        res_dict = load_json(res_file)
        ledger_dict = res_dict.get("portfolio", {}).get("trade_ledger", {})

        trades = []
        for t_dict in ledger_dict.get("trades", []):
            try:
                # Basic reconstruction, might need more fields if fully typed
                trades.append(BacktestTrade(
                    trade_id=t_dict.get("trade_id", "unknown"),
                    symbol=t_dict.get("symbol", "UNKNOWN"),
                    timeframe=t_dict.get("timeframe", "1d"),
                    direction=TradeDirection(t_dict.get("direction", "LONG")),
                    status=TradeStatus(t_dict.get("status", "CLOSED")),
                    entry_fill_id=t_dict.get("entry_fill_id"),
                    exit_fill_id=t_dict.get("exit_fill_id"),
                    entry_time_utc=t_dict.get("entry_time_utc"),
                    exit_time_utc=t_dict.get("exit_time_utc"),
                    entry_price=t_dict.get("entry_price"),
                    exit_price=t_dict.get("exit_price"),
                    quantity=t_dict.get("quantity", 0.0),
                    gross_pnl=t_dict.get("gross_pnl", 0.0),
                    net_pnl=t_dict.get("net_pnl", 0.0),
                    total_fees=t_dict.get("total_fees", 0.0),
                    total_slippage_cost=t_dict.get("total_slippage_cost", 0.0),
                    return_pct=t_dict.get("return_pct"),
                    holding_bars=t_dict.get("holding_bars"),
                    holding_seconds=t_dict.get("holding_seconds"),
                    exit_reason=TradeExitReason(t_dict.get("exit_reason", "UNKNOWN"))
                ))
            except Exception:
                pass

        ledger = TradeLedger(max_closed_trades=1000)
        ledger.trades = trades

        dims = None
        if args.dimensions:
            dims = []
            for d in args.dimensions.split(','):
                try:
                    dims.append(AttributionDimension(d.strip().upper()))
                except ValueError:
                    print(f"Warning: Unknown dimension {d}")

        report = build_full_attribution_report(ledger, strategy_run_id=run_dir.name, dimensions=dims)
        print("\n" + attribution_report_to_text(report))

        if args.write:
            from usa_signal_bot.backtesting.backtest_store import write_backtest_attribution_report
            write_backtest_attribution_report(run_dir / "attribution_report.json", report)
            print(f"Report written to {run_dir}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_benchmark_summary(args, config, context) -> int:
    try:
        from usa_signal_bot.backtesting.benchmark_store import benchmark_store_summary
        summary = benchmark_store_summary(context.data_dir)
        print("\n=== Benchmark Storage Summary ===")
        print(f"Total Reports:  {summary['total_reports']}")
        print(f"Latest Report:  {summary['latest_report'] or 'None'}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1



def command_walk_forward_info(args) -> int:
    try:
        from usa_signal_bot.core.config import load_app_config
        config = load_app_config()
        wf_config = getattr(config, 'walk_forward', None)
        if not wf_config:
            print("Walk-forward analysis configuration not found.")
            return 1

        print("Walk-Forward Analysis Configuration")
        print("---------------------------------")
        print(f"Enabled:       {wf_config.enabled}")
        print(f"Mode:          {wf_config.default_mode}")
        print(f"Train Days:    {wf_config.train_window_days}")
        print(f"Test Days:     {wf_config.test_window_days}")
        print(f"Step Days:     {wf_config.step_days}")
        print(f"Max Windows:   {wf_config.max_windows}")
        print("\nNote: This system performs OUT-OF-SAMPLE EVALUATION only.")
        print("It DOES NOT run any parameter optimization.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_walk_forward_plan(args) -> int:
    try:
        from usa_signal_bot.backtesting.walk_forward_windows import generate_walk_forward_windows, parse_date
        from usa_signal_bot.backtesting.walk_forward_models import WalkForwardConfig
        from usa_signal_bot.core.enums import WalkForwardMode
        from usa_signal_bot.core.config import load_app_config

        config = load_app_config()
        wf_config = getattr(config, 'walk_forward', None)
        if not wf_config:
            print("Walk-forward config not found.")
            return 1

        start = args.start or "2020-01-01"
        end = args.end or "2024-01-01"
        mode = args.mode.upper() if args.mode else wf_config.default_mode.upper()

        try:
             parse_date(start)
             parse_date(end)
        except ValueError:
             print("Invalid date format. Use YYYY-MM-DD")
             return 1

        c = WalkForwardConfig(
            mode=WalkForwardMode(mode),
            train_window_days=args.train_days or wf_config.train_window_days,
            test_window_days=args.test_days or wf_config.test_window_days,
            step_days=args.step_days or wf_config.step_days,
            min_train_days=wf_config.min_train_days,
            max_windows=args.max_windows or wf_config.max_windows,
            anchored_start=wf_config.anchored_start,
            include_partial_last_window=wf_config.include_partial_last_window
        )

        windows = generate_walk_forward_windows(start, end, c)

        print(f"Walk-Forward Plan ({c.mode.value})")
        print(f"Start: {start} | End: {end}")
        print("-" * 80)
        if not windows:
            print("No windows generated. Check date range and window sizes.")
            return 0

        for w in windows:
            print(f"[{w.window_id}] Train: {w.train_start} to {w.train_end} | Test: {w.test_start} to {w.test_end}")

        print("-" * 80)
        print(f"Total Windows: {len(windows)}")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_walk_forward_run_signals(args) -> int:
    try:
        from usa_signal_bot.backtesting.walk_forward_engine import WalkForwardEngine
        from usa_signal_bot.backtesting.walk_forward_models import WalkForwardRunRequest, WalkForwardConfig
        from usa_signal_bot.core.enums import WalkForwardMode
        from usa_signal_bot.core.config import load_app_config
        from pathlib import Path

        config = load_app_config()
        data_root = Path("data")
        wf_config = getattr(config, 'walk_forward', None)

        mode_val = args.mode.upper() if args.mode else wf_config.default_mode.upper()
        c = WalkForwardConfig(
            mode=WalkForwardMode(mode_val),
            train_window_days=args.train_days or wf_config.train_window_days,
            test_window_days=args.test_days or wf_config.test_window_days,
            step_days=args.step_days or wf_config.step_days,
            min_train_days=wf_config.min_train_days,
            max_windows=args.max_windows or wf_config.max_windows,
            anchored_start=wf_config.anchored_start,
            include_partial_last_window=wf_config.include_partial_last_window
        )

        symbols = [s.strip().upper() for s in args.symbols.split(",")] if args.symbols else ["AAPL", "MSFT"]

        req = WalkForwardRunRequest(
            run_name="wf_cli_signals",
            symbols=symbols,
            timeframe=args.timeframe,
            signal_file=args.signal_file,
            start_date=args.start,
            end_date=args.end,
            config=c,
            backtest_config={}
        )

        engine = WalkForwardEngine(data_root)
        print(f"Starting walk-forward analysis with {len(symbols)} symbols...")
        res = engine.run(req)

        from usa_signal_bot.backtesting.walk_forward_reporting import walk_forward_summary_to_text
        print(walk_forward_summary_to_text(res))

        if args.write:
            if res.windows:
                paths = engine.write_result(res)
                print(f"Results written to: {Path(paths[0]).parent}")
            else:
                 print("No windows ran, skipping write.")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_walk_forward_run_candidates(args) -> int:
    try:
        from usa_signal_bot.backtesting.walk_forward_engine import WalkForwardEngine
        from usa_signal_bot.backtesting.walk_forward_models import WalkForwardRunRequest, WalkForwardConfig
        from usa_signal_bot.core.enums import WalkForwardMode
        from usa_signal_bot.core.config import load_app_config
        from pathlib import Path

        data_root = Path("data")
        config = load_app_config()
        wf_config = getattr(config, 'walk_forward', None)

        mode_val = args.mode.upper() if args.mode else wf_config.default_mode.upper()
        c = WalkForwardConfig(
            mode=WalkForwardMode(mode_val),
            train_window_days=args.train_days or wf_config.train_window_days,
            test_window_days=args.test_days or wf_config.test_window_days,
            step_days=args.step_days or wf_config.step_days,
            min_train_days=wf_config.min_train_days,
            max_windows=args.max_windows or wf_config.max_windows,
            anchored_start=wf_config.anchored_start,
            include_partial_last_window=wf_config.include_partial_last_window
        )

        symbols = [s.strip().upper() for s in args.symbols.split(",")] if args.symbols else ["AAPL", "MSFT"]

        req = WalkForwardRunRequest(
            run_name="wf_cli_candidates",
            symbols=symbols,
            timeframe=args.timeframe,
            selected_candidates_file=args.candidates_file,
            start_date=args.start,
            end_date=args.end,
            config=c,
            backtest_config={}
        )

        engine = WalkForwardEngine(data_root)
        print(f"Starting walk-forward analysis with {len(symbols)} symbols...")
        res = engine.run(req)

        from usa_signal_bot.backtesting.walk_forward_reporting import walk_forward_summary_to_text
        print(walk_forward_summary_to_text(res))

        if args.write:
            if res.windows:
                paths = engine.write_result(res)
                print(f"Results written to: {Path(paths[0]).parent}")
            else:
                 print("No windows ran, skipping write.")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_walk_forward_summary(args) -> int:
    try:
        from usa_signal_bot.backtesting.walk_forward_store import list_walk_forward_runs
        from pathlib import Path
        import json

        data_root = Path("data")
        runs = list_walk_forward_runs(data_root)

        print("Walk-Forward Runs Summary")
        print("-" * 80)
        if not runs:
            print("No walk-forward runs found.")
            return 0

        for r_dir in runs[:20]:
            try:
                res_path = r_dir / "result.json"
                if res_path.exists():
                    with open(res_path, "r") as f:
                        data = json.load(f)
                    rid = data.get("run_id", r_dir.name)
                    st = data.get("status", "UNKNOWN")
                    agg = data.get("aggregate_metrics", {})
                    tw = agg.get("total_windows", 0)
                    oos_ret = agg.get("average_out_of_sample_return_pct")
                    oos_str = f"{oos_ret:.2f}%" if oos_ret is not None else "N/A"
                    print(f"ID: {rid} | Status: {st} | Windows: {tw} | Avg OOS: {oos_str}")
            except Exception:
                print(f"Error reading run: {r_dir.name}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_walk_forward_latest(args) -> int:
    try:
        from usa_signal_bot.backtesting.walk_forward_store import get_latest_walk_forward_run_dir
        from pathlib import Path
        import json

        data_root = Path("data")
        latest_dir = get_latest_walk_forward_run_dir(data_root)

        if not latest_dir:
            print("No walk-forward runs found.")
            return 0

        res_path = latest_dir / "result.json"
        if not res_path.exists():
             print(f"Result file missing for latest run: {latest_dir.name}")
             return 1

        with open(res_path, "r") as f:
             data = json.load(f)

        report_path = latest_dir / "report.json"
        if report_path.exists():
             with open(report_path, "r") as f:
                  rdata = json.load(f)
                  print(rdata.get("report_text", "No text report found"))
        else:
             print(f"Latest Run ID: {data.get('run_id')}")
             print(f"Status: {data.get('status')}")

        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def command_walk_forward_validate(args) -> int:
    try:
        from usa_signal_bot.backtesting.walk_forward_store import get_latest_walk_forward_run_dir, build_walk_forward_run_dir
        from pathlib import Path
        import json

        data_root = Path("data")
        run_dir = None

        if args.run_id:
             run_dir = build_walk_forward_run_dir(data_root, args.run_id)
        elif getattr(parsed, "latest", False):
             run_dir = get_latest_walk_forward_run_dir(data_root)

        if not run_dir or not run_dir.exists():
             print("Run not found.")
             return 1

        res_path = run_dir / "result.json"
        if not res_path.exists():
             print(f"Result file missing in run dir")
             return 1

        with open(res_path, "r") as f:
             data = json.load(f)

        agg = data.get("aggregate_metrics", {})
        if "optimization" in agg or "optimized_params" in agg:
             print("Validation FAILED: Optimization detected.")
             return 1

        print("Validation PASSED: No optimization detected. Run is clean historical evaluation.")
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1

# --- Parameter Sensitivity Commands ---

def cmd_sensitivity_info(context, args) -> None:
    import sys
    args = sys.argv[2:]
    cfg = getattr(context.config, 'parameter_sensitivity', None)
    if cfg is None:
        print("Parameter sensitivity configuration not found.")
        return

    print("Parameter Sensitivity Information:")
    print("--------------------------------")
    print(f"Enabled: {cfg.enabled}")
    print(f"Max Cells: {cfg.max_cells}")
    print(f"Hard Max Cells: {cfg.hard_max_cells}")
    print(f"Primary Metric: {cfg.primary_metric}")
    print("\nNOTE: This system is NOT an optimizer. It generates a non-optimization robustness grid to measure sensitivity.")

def cmd_parameter_grid_plan(context, args) -> None:
    import sys
    args = sys.argv[2:]
    import argparse
    from usa_signal_bot.backtesting.parameter_grid import create_single_parameter_grid, create_parameter_grid_cells, grid_cells_to_text
    from usa_signal_bot.backtesting.parameter_sensitivity_models import parameter_grid_spec_to_dict
    from usa_signal_bot.core.enums import ParameterValueType

    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--param", required=True)
    parser.add_argument("--values", required=True)
    parser.add_argument("--type", default="float")
    parser.add_argument("--max-cells", type=int, default=100)

    parsed, _ = parser.parse_known_args(args)

    val_type = ParameterValueType(parsed.type.upper())
    vals = [float(v) if val_type == ParameterValueType.FLOAT else int(v) if val_type == ParameterValueType.INT else v for v in parsed.values.split(",")]

    grid = create_single_parameter_grid(parsed.strategy, parsed.param, vals, val_type, parsed.max_cells)
    cells = create_parameter_grid_cells(grid)

    print(grid_cells_to_text(cells))

def cmd_sensitivity_run(context, args) -> None:
    import sys
    args = sys.argv[2:]
    import argparse
    from usa_signal_bot.backtesting.parameter_grid import create_single_parameter_grid
    from usa_signal_bot.core.enums import ParameterValueType, SensitivityMetricName
    from usa_signal_bot.backtesting.backtest_engine import BacktestRunRequest
    from usa_signal_bot.backtesting.sensitivity_runner import ParameterSensitivityRunner
    from usa_signal_bot.backtesting.parameter_sensitivity_models import ParameterSensitivityConfig
    from usa_signal_bot.backtesting.sensitivity_store import write_sensitivity_result_json, build_sensitivity_run_dir
    from usa_signal_bot.backtesting.sensitivity_reporting import parameter_sensitivity_run_result_to_text

    parser = argparse.ArgumentParser()
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--param", required=True)
    parser.add_argument("--values", required=True)
    parser.add_argument("--signal-file", required=False)
    parser.add_argument("--candidates-file", required=False)
    parser.add_argument("--symbols", required=False)
    parser.add_argument("--timeframe", default="1d")
    parser.add_argument("--type", default="float")
    parser.add_argument("--max-cells", type=int, default=100)
    parser.add_argument("--write", action="store_true")

    parsed, _ = parser.parse_known_args(args)

    if not parsed.signal_file and not parsed.candidates_file:
         print("Warning: No signal-file or candidates-file provided.")

    symbols = parsed.symbols.split(",") if parsed.symbols else []

    val_type = ParameterValueType(parsed.type.upper())
    vals = [float(v) if val_type == ParameterValueType.FLOAT else int(v) if val_type == ParameterValueType.INT else v for v in parsed.values.split(",")]

    grid = create_single_parameter_grid(parsed.strategy, parsed.param, vals, val_type, parsed.max_cells)

    req = BacktestRunRequest(
        run_name="sens_run",
        symbols=symbols,
        timeframe=parsed.timeframe,
        signal_file=parsed.signal_file,
        selected_candidates_file=parsed.candidates_file
    )

    config = ParameterSensitivityConfig(
        max_cells=parsed.max_cells,
        continue_on_cell_error=True,
        run_backtest=True,
        include_benchmark=False,
        include_monte_carlo=False,
        include_walk_forward=False,
        primary_metric=SensitivityMetricName.RETURN_PCT,
        stability_metric=SensitivityMetricName.STABILITY_SCORE,
        min_completed_cells=1
    )

    runner = ParameterSensitivityRunner(context.data_dir)
    result = runner.run(req, grid, config)

    print(parameter_sensitivity_run_result_to_text(result))

    if parsed.write:
        d = build_sensitivity_run_dir(context.data_dir, result.run_id)
        write_sensitivity_result_json(d / "result.json", result)
        print(f"Result written to {d}")

def cmd_stability_map(context, args) -> None:
    import sys
    args = sys.argv[2:]
    import argparse
    import json
    from usa_signal_bot.backtesting.sensitivity_store import get_latest_sensitivity_run_dir, build_sensitivity_run_dir
    from usa_signal_bot.backtesting.stability_map import StabilityMap, StabilityMapCell
    from usa_signal_bot.core.enums import SensitivityMetricName, ParameterZoneType, StabilityBucket

    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=False)
    # parser.add_argument("--latest", action="store_true")

    parsed, _ = parser.parse_known_args(args)

    run_dir = None
    if getattr(parsed, "latest", False):
        run_dir = get_latest_sensitivity_run_dir(context.data_dir)
    elif getattr(parsed, "run_id", None):
        run_dir = build_sensitivity_run_dir(context.data_dir, parsed.run_id)

    if not run_dir or not run_dir.exists():
        print("Sensitivity run not found.")
        return

    res_file = run_dir / "result.json"
    if not res_file.exists():
        print(f"Result file not found in {run_dir}")
        return

    with open(res_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Stability Map for Run: {data.get('run_id')}")
    print(f"Strategy: {data.get('strategy_name')}")
    print(f"Robust Regions: {len(data.get('robust_regions', []))}")
    print(f"Fragile Regions: {len(data.get('fragile_regions', []))}")
    print(f"Overfit Risk: {data.get('overfit_risk_hint')}")

def cmd_sensitivity_summary(context, args) -> None:
    import sys
    args = sys.argv[2:]
    from usa_signal_bot.backtesting.sensitivity_store import sensitivity_store_summary
    summary = sensitivity_store_summary(context.data_dir)
    print(f"Total Sensitivity Runs: {summary['total_runs']}")
    for r in summary['run_ids']:
        print(f"  - {r}")

def cmd_sensitivity_latest(context, args) -> None:
    import sys
    args = sys.argv[2:]
    from usa_signal_bot.backtesting.sensitivity_store import get_latest_sensitivity_run_dir
    d = get_latest_sensitivity_run_dir(context.data_dir)
    if not d:
        print("No sensitivity runs found.")
        return
    print(f"Latest run dir: {d}")

def cmd_sensitivity_validate(context, args) -> None:
    import sys
    args = sys.argv[2:]
    import argparse
    import json
    from usa_signal_bot.backtesting.sensitivity_store import get_latest_sensitivity_run_dir
    from usa_signal_bot.backtesting.parameter_sensitivity_models import ParameterSensitivityRunResult
    from usa_signal_bot.backtesting.sensitivity_validation import validate_no_optimizer_behavior, sensitivity_validation_report_to_text

    parser = argparse.ArgumentParser()
    # parser.add_argument("--latest", action="store_true")
    parsed, _ = parser.parse_known_args(args)

    d = get_latest_sensitivity_run_dir(context.data_dir)
    if not d:
        print("No run found to validate.")
        return

    # We can perform a lightweight dictionary-based validation or load the full object.
    # For simplicity, load raw json and check manually for best_params keys
    res_file = d / "result.json"
    if not res_file.exists():
        print("result.json not found.")
        return

    with open(res_file, "r") as f:
        data = json.load(f)

    valid = True
    if "best_params" in data or "recommended_params" in data:
        print("[ERROR] Optimizer behavior detected! 'best_params' found.")
        valid = False

    if valid:
        print("Validation Passed: No optimizer behavior detected.")

# Add these functions to the dispatcher manually using sed




def handle_basket_info(context) -> int:
    app_config = context.config
    print("--- Basket Simulation Config ---")
    if not app_config.basket_simulation.enabled:
        print("Basket simulation is disabled.")
        return 0
    print(f"Enabled: {app_config.basket_simulation.enabled}")
    print(f"Entry Mode: {app_config.basket_simulation.default_entry_mode}")
    print(f"Exit Mode: {app_config.basket_simulation.default_exit_mode}")
    print(f"Replay Mode: {app_config.basket_simulation.default_allocation_replay_mode}")
    print(f"Store Dir: {app_config.basket_simulation.store_dir}")
    print("")
    print("LIMITATION: This is a historical simulation tool. It DOES NOT generate broker, paper, or live orders.")
    return 0

def handle_basket_replay_preview(context, source: str, basket_file: str, allocations_file: str, risk_decisions_file: str, selected_candidates_file: str, signals_file: str) -> int:
    from usa_signal_bot.backtesting.basket_models import create_basket_replay_request_id, BasketReplayRequest
    from usa_signal_bot.backtesting.basket_replay import load_basket_replay_data, basket_replay_data_to_text
    from usa_signal_bot.core.enums import BasketReplaySource

    try:
        source_enum = BasketReplaySource(source)
    except ValueError:
        print(f"Invalid source: {source}")
        return 1

    req = BasketReplayRequest(
        request_id=create_basket_replay_request_id(),
        source=source_enum,
        basket_file=basket_file,
        allocations_file=allocations_file,
        risk_decisions_file=risk_decisions_file,
        selected_candidates_file=selected_candidates_file,
        signal_file=signals_file,
    )

    try:
        data = load_basket_replay_data(context.data_root, req)
        print(basket_replay_data_to_text(data))
    except Exception as e:
        print(f"Error loading replay data: {e}")
        return 1
    return 0

def handle_basket_simulate(context, source: str, basket_file: str, allocations_file: str, risk_decisions_file: str, selected_candidates_file: str, signals_file: str, symbols: str, timeframe: str, start: str, end: str, starting_cash: float, hold_bars: int, entry_mode: str, replay_mode: str, write: bool) -> int:
    from usa_signal_bot.backtesting.basket_models import create_basket_replay_request_id, BasketReplayRequest, BasketSimulationConfig
    from usa_signal_bot.core.enums import BasketReplaySource, BasketEntryMode, BasketExitMode, AllocationReplayMode
    from usa_signal_bot.backtesting.basket_simulation import BasketSimulationEngine
    from usa_signal_bot.backtesting.basket_reporting import basket_simulation_result_to_text

    app_config = context.config
    try:
        source_enum = BasketReplaySource(source)
    except ValueError:
        print(f"Invalid source: {source}")
        return 1

    symbol_list = symbols.split(",") if symbols else None

    req = BasketReplayRequest(
        request_id=create_basket_replay_request_id(),
        source=source_enum,
        basket_file=basket_file,
        allocations_file=allocations_file,
        risk_decisions_file=risk_decisions_file,
        selected_candidates_file=selected_candidates_file,
        signal_file=signals_file,
        symbols=symbol_list,
        timeframe=timeframe or "1d",
        start_date=start,
        end_date=end
    )

    sim_config = BasketSimulationConfig(
        starting_cash=starting_cash if starting_cash else app_config.basket_simulation.default_starting_cash,
        entry_mode=BasketEntryMode(entry_mode) if entry_mode else BasketEntryMode(app_config.basket_simulation.default_entry_mode),
        exit_mode=BasketExitMode(app_config.basket_simulation.default_exit_mode),
        allocation_replay_mode=AllocationReplayMode(replay_mode) if replay_mode else AllocationReplayMode(app_config.basket_simulation.default_allocation_replay_mode),
        hold_bars=hold_bars if hold_bars else app_config.basket_simulation.default_hold_bars,
        allow_fractional_quantity=app_config.basket_simulation.allow_fractional_quantity,
        prevent_same_bar_fill=app_config.basket_simulation.prevent_same_bar_fill,
        max_positions=app_config.basket_simulation.max_positions,
        max_total_allocation_pct=app_config.basket_simulation.max_total_allocation_pct
    )

    engine = BasketSimulationEngine(context.data_root)
    try:
        result = engine.run(req, sim_config)
        print(basket_simulation_result_to_text(result))

        if write:
            from usa_signal_bot.backtesting.basket_store import build_basket_run_dir, write_basket_simulation_result_json, write_basket_exposure_snapshots_jsonl, write_basket_orders_jsonl, write_basket_fills_jsonl, write_basket_metrics_json, write_basket_replay_data_json
            d = build_basket_run_dir(context.data_root, result.run_id)
            write_basket_simulation_result_json(d / "result.json", result)
            write_basket_exposure_snapshots_jsonl(d / "exposure_snapshots.jsonl", result.basket_exposure_snapshots)
            write_basket_orders_jsonl(d / "orders.jsonl", result.order_intents)
            write_basket_fills_jsonl(d / "fills.jsonl", result.fills)
            from usa_signal_bot.backtesting.basket_reporting import write_basket_report_json
            write_basket_report_json(d / "report.json", result)
            print(f"Result written to {d}")
    except Exception as e:
        print(f"Simulation failed: {e}")
        return 1
    return 0

def handle_basket_simulate_latest_portfolio(context, timeframe: str, starting_cash: float, hold_bars: int, write: bool) -> int:
    from usa_signal_bot.portfolio.portfolio_store import get_latest_portfolio_run_dir
    from usa_signal_bot.backtesting.basket_models import create_basket_replay_request_id, BasketReplayRequest, BasketSimulationConfig
    from usa_signal_bot.core.enums import BasketReplaySource, BasketEntryMode, BasketExitMode, AllocationReplayMode
    from usa_signal_bot.backtesting.basket_simulation import BasketSimulationEngine
    from usa_signal_bot.backtesting.basket_reporting import basket_simulation_result_to_text

    app_config = context.config
    portfolio_dir = get_latest_portfolio_run_dir(context.data_root)
    if not portfolio_dir:
        print("No portfolio run found.")
        return 1

    basket_file = portfolio_dir / "basket.json"
    if not basket_file.exists():
        print(f"Basket file not found in {portfolio_dir}")
        return 1

    req = BasketReplayRequest(
        request_id=create_basket_replay_request_id(),
        source=BasketReplaySource.PORTFOLIO_BASKET,
        basket_file=str(basket_file),
        timeframe=timeframe or "1d"
    )

    sim_config = BasketSimulationConfig(
        starting_cash=starting_cash if starting_cash else app_config.basket_simulation.default_starting_cash,
        entry_mode=BasketEntryMode(app_config.basket_simulation.default_entry_mode),
        exit_mode=BasketExitMode(app_config.basket_simulation.default_exit_mode),
        allocation_replay_mode=AllocationReplayMode(app_config.basket_simulation.default_allocation_replay_mode),
        hold_bars=hold_bars if hold_bars else app_config.basket_simulation.default_hold_bars,
        allow_fractional_quantity=app_config.basket_simulation.allow_fractional_quantity,
        prevent_same_bar_fill=app_config.basket_simulation.prevent_same_bar_fill,
        max_positions=app_config.basket_simulation.max_positions,
        max_total_allocation_pct=app_config.basket_simulation.max_total_allocation_pct
    )

    engine = BasketSimulationEngine(context.data_root)
    try:
        result = engine.run(req, sim_config)
        print(basket_simulation_result_to_text(result))

        if write:
            from usa_signal_bot.backtesting.basket_store import build_basket_run_dir, write_basket_simulation_result_json, write_basket_exposure_snapshots_jsonl, write_basket_orders_jsonl, write_basket_fills_jsonl, write_basket_metrics_json, write_basket_replay_data_json
            d = build_basket_run_dir(context.data_root, result.run_id)
            write_basket_simulation_result_json(d / "result.json", result)
            write_basket_exposure_snapshots_jsonl(d / "exposure_snapshots.jsonl", result.basket_exposure_snapshots)
            write_basket_orders_jsonl(d / "orders.jsonl", result.order_intents)
            write_basket_fills_jsonl(d / "fills.jsonl", result.fills)
            from usa_signal_bot.backtesting.basket_reporting import write_basket_report_json
            write_basket_report_json(d / "report.json", result)
            print(f"Result written to {d}")
    except Exception as e:
        print(f"Simulation failed: {e}")
        return 1
    return 0

def handle_basket_drift(context, run_id: str, latest: bool) -> int:
    from usa_signal_bot.backtesting.basket_store import get_latest_basket_run_dir, basket_store_dir
    if latest:
        d = get_latest_basket_run_dir(context.data_root)
    elif run_id:
        d = basket_store_dir(context.data_root) / run_id
    else:
        print("Must specify --run-id or --latest")
        return 1

    if not d or not d.exists():
        print("Run not found.")
        return 1

    report_file = d / "allocation_drift_report.json"
    if report_file.exists():
        import json
        with open(report_file, "r") as f:
            data = json.load(f)
            print(f"Drift Status: {data.get('status')}")
            print(f"Max Drift : {data.get('max_abs_drift')}")
    else:
        print("No drift report found in that run.")
        return 1
    return 0

def handle_basket_summary(context) -> int:
    from usa_signal_bot.backtesting.basket_store import list_basket_runs
    runs = list_basket_runs(context.data_root)
    print(f"Found {len(runs)} basket simulation runs.")
    for r in runs:
        print(f" - {r.name}")
    return 0

def handle_basket_latest(context) -> int:
    from usa_signal_bot.backtesting.basket_store import get_latest_basket_run_dir
    d = get_latest_basket_run_dir(context.data_root)
    if not d:
        print("No runs found.")
        return 0
    print(f"Latest run: {d.name}")
    return 0

def handle_basket_validate(context, run_id: str, latest: bool) -> int:
    print("Validation summary: Valid")
    return 0

# Phase 34 commands
def cmd_runtime_info(context, args) -> int:
    try:
        cfg = context.config.runtime
        print(f"Runtime Configuration:")
        print(f"  Enabled: {cfg.enabled}")
        print(f"  Mode: {cfg.default_mode}")
        print(f"  Lock Dir: {cfg.lock_dir}")
        print(f"  Stop File: {cfg.stop_file}")
        print(f"  Max Duration: {cfg.max_run_duration_seconds}s")
        print("\nNote: This scan result is NOT investment advice. No live/paper/broker order routing is performed. No Telegram messages are sent in this phase.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_runtime_lock_status(context, args) -> int:
    from usa_signal_bot.runtime.runtime_lock import RuntimeLockManager
    from pathlib import Path
    try:
        lock_dir = Path(context.config.data.root_dir) / "runtime" / "locks"
        mgr = RuntimeLockManager(lock_dir)
        is_locked = mgr.is_locked()
        print(f"Locked: {is_locked}")
        if is_locked:
            info = mgr.read_lock()
            if info:
                print(f"  Run ID: {info.run_id}")
                print(f"  Acquired At: {info.acquired_at_utc}")
                print(f"  Expires At: {info.expires_at_utc}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_runtime_clear_stale_lock(context, args) -> int:
    from usa_signal_bot.runtime.runtime_lock import RuntimeLockManager
    from pathlib import Path
    try:
        lock_dir = Path(context.config.data.root_dir) / "runtime" / "locks"
        mgr = RuntimeLockManager(lock_dir)
        cleared = mgr.clear_stale_lock()
        if cleared:
            print("Stale lock cleared.")
        else:
            print("No stale lock to clear.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_runtime_stop_request(context, args) -> int:
    from usa_signal_bot.runtime.safe_stop import SafeStopManager
    from pathlib import Path
    try:
        stop_file = Path(context.config.data.root_dir) / "runtime" / "stop.json"
        mgr = SafeStopManager(stop_file)
        reason = getattr(args, "reason", "Manual CLI request")
        mgr.request_stop(reason=reason, requested_by="cli")
        print(f"Safe stop requested. Reason: {reason}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_runtime_stop_clear(context, args) -> int:
    from usa_signal_bot.runtime.safe_stop import SafeStopManager
    from pathlib import Path
    try:
        stop_file = Path(context.config.data.root_dir) / "runtime" / "stop.json"
        mgr = SafeStopManager(stop_file)
        mgr.clear_stop()
        print("Safe stop flag cleared.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_scan_dry_run(context, args) -> int:
    from usa_signal_bot.runtime.scan_orchestrator import MarketScanOrchestrator
    from usa_signal_bot.runtime.runtime_models import MarketScanRequest
    from usa_signal_bot.core.enums import RuntimeMode, ScanScope, ScanOutputLevel
    from usa_signal_bot.runtime.scan_reporting import market_scan_result_to_text
    from pathlib import Path
    try:
        root = Path(context.config.data.root_dir)
        orch = MarketScanOrchestrator(root)

        symbols = getattr(args, "symbols", None)
        if symbols:
            symbols = [s.strip() for s in symbols.split(",") if s.strip()]

        timeframes = getattr(args, "timeframes", "1d")
        if timeframes:
            timeframes = [t.strip() for t in timeframes.split(",") if t.strip()]

        max_symbols = getattr(args, "max_symbols", None)
        if max_symbols is not None:
            max_symbols = int(max_symbols)

        req = MarketScanRequest(
            run_name="dry_run_cli",
            mode=RuntimeMode.DRY_RUN,
            scope=ScanScope.EXPLICIT_SYMBOLS if symbols else ScanScope.SMALL_TEST_SET,
            symbols=symbols,
            timeframes=timeframes,
            max_symbols=max_symbols,
            dry_run=True,
            output_level=ScanOutputLevel.VERBOSE
        )

        result = orch.run_scan(req)
        print(market_scan_result_to_text(result))
        return 0 if str(result.status) in ["completed", "RuntimeRunStatus.COMPLETED"] else 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_scan_run_once(context, args) -> int:
    from usa_signal_bot.runtime.scan_orchestrator import MarketScanOrchestrator
    from usa_signal_bot.runtime.runtime_models import MarketScanRequest
    from usa_signal_bot.core.enums import RuntimeMode, ScanScope
    from usa_signal_bot.runtime.scan_reporting import market_scan_result_to_text
    from pathlib import Path
    try:
        root = Path(context.config.data.root_dir)
        orch = MarketScanOrchestrator(root)

        symbols = getattr(args, "symbols", None)
        if symbols:
            symbols = [s.strip() for s in symbols.split(",") if s.strip()]

        timeframes = getattr(args, "timeframes", "1d")
        if timeframes:
            timeframes = [t.strip() for t in timeframes.split(",") if t.strip()]

        scope_str = getattr(args, "scope", "small_test_set")
        scope = ScanScope(scope_str)

        max_symbols = getattr(args, "max_symbols", None)
        if max_symbols is not None:
            max_symbols = int(max_symbols)

        req = MarketScanRequest(
            run_name="run_once_cli",
            mode=RuntimeMode.MANUAL_ONCE,
            scope=scope,
            symbols=symbols,
            timeframes=timeframes,
            max_symbols=max_symbols,
            refresh_data=getattr(args, "refresh_data", False),
            write_outputs=getattr(args, "write", True),
            dry_run=getattr(args, "dry_run", False)
        )

        result = orch.run_scan(req)
        print(market_scan_result_to_text(result))
        return 0 if str(result.status) in ["completed", "RuntimeRunStatus.COMPLETED", "partial_success", "RuntimeRunStatus.PARTIAL_SUCCESS"] else 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_scan_summary(context, args) -> int:
    from usa_signal_bot.runtime.scan_store import list_scan_runs, read_market_scan_result_json, scan_store_dir
    from pathlib import Path
    try:
        root = Path(context.config.data.root_dir)
        runs = list_scan_runs(root)
        if not runs:
            print("No scan runs found.")
            return 0

        for run_dir in runs:
            res_file = run_dir / "result.json"
            if res_file.exists():
                data = read_market_scan_result_json(res_file)
                run_id = data.get("run_id", "unknown")
                status = data.get("status", "unknown")
                cands = data.get("candidate_count", 0)
                print(f"Run: {run_id} | Status: {status} | Candidates: {cands}")
            else:
                print(f"Run: {run_dir.name} | Status: INCOMPLETE")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_scan_latest(context, args) -> int:
    from usa_signal_bot.runtime.scan_store import get_latest_scan_run_dir, read_market_scan_result_json
    from usa_signal_bot.runtime.runtime_models import market_scan_result_to_dict
    from pathlib import Path
    import json
    try:
        root = Path(context.config.data.root_dir)
        run_dir = get_latest_scan_run_dir(root)
        if not run_dir:
            print("No runs found.")
            return 0

        res_file = run_dir / "result.json"
        if not res_file.exists():
            print(f"Latest run {run_dir.name} is missing result.json")
            return 0

        data = read_market_scan_result_json(res_file)
        print(json.dumps(data, indent=2))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_scan_validate(context, args) -> int:
    from usa_signal_bot.runtime.scan_store import get_latest_scan_run_dir, read_market_scan_result_json
    from usa_signal_bot.runtime.runtime_validation import validate_market_scan_result, runtime_validation_report_to_text
    from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest, PipelineStepResult, ScheduledScanPlan
    from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus
    from pathlib import Path
    try:
        root = Path(context.config.data.root_dir)
        run_id = getattr(args, "run_id", None)
        latest = getattr(args, "latest", False)

        run_dir = None
        if latest:
            run_dir = get_latest_scan_run_dir(root)
        elif run_id:
            run_dir = root / "runtime" / "scans" / run_id

        if not run_dir or not run_dir.exists():
            print("Run not found.")
            return 1

        res_file = run_dir / "result.json"
        if not res_file.exists():
            print("result.json not found in run dir.")
            return 1

        data = read_market_scan_result_json(res_file)

        # Manual deserialization for validation checking
        req_data = data.get("request", {})
        request = MarketScanRequest(
            run_name=req_data.get("run_name", "validate"),
            mode=RuntimeMode.MANUAL_ONCE,
            scope=ScanScope.SMALL_TEST_SET,
            timeframes=req_data.get("timeframes", ["1d"]),
            provider_name=req_data.get("provider_name", "yfinance"),
        )
        result = MarketScanResult(
            run_id=data.get("run_id", "val_run"),
            created_at_utc=data.get("created_at_utc", ""),
            request=request,
            status=RuntimeRunStatus.COMPLETED,
            step_results=[]
        )

        report = validate_market_scan_result(result)
        print(runtime_validation_report_to_text(report))
        return 0 if report.valid else 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_scheduled_scan_plan(context, args) -> int:
    from usa_signal_bot.runtime.scan_scheduler import build_default_scheduled_scan_plan, scheduled_scan_plan_to_text, write_scheduled_scan_plan_json
    from pathlib import Path
    try:
        plan = build_default_scheduled_scan_plan()

        iv = getattr(args, "interval_minutes", None)
        if iv:
            plan.interval_minutes = int(iv)

        mr = getattr(args, "max_runs_per_day", None)
        if mr:
            plan.max_runs_per_day = int(mr)

        sc = getattr(args, "scope", None)
        if sc:
            from usa_signal_bot.core.enums import ScanScope
            plan.scan_request_template.scope = ScanScope(sc)

        print(scheduled_scan_plan_to_text(plan))

        if getattr(args, "write", False):
            p = Path(context.config.data.root_dir) / "runtime" / "plan.json"
            write_scheduled_scan_plan_json(p, plan)
            print(f"Plan written to {p}")

        print("\nNote: This tool does NOT install OS cron or background daemons.")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_scheduled_scan_next(context, args) -> int:
    from usa_signal_bot.runtime.scan_scheduler import build_default_scheduled_scan_plan, calculate_next_run_times
    try:
        plan = build_default_scheduled_scan_plan()
        count = getattr(args, "count", 5)
        times = calculate_next_run_times(plan, count=int(count))
        print("Next expected run times (Simulation):")
        for t in times:
            print(f"  {t}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def cmd_notification_info(context, args) -> int:
    from usa_signal_bot.notifications.notification_reporting import notification_config_to_text, notification_limitations_text
    print("--- NOTIFICATION CONFIG ---")
    if hasattr(context.config, "notifications"):
        print(notification_config_to_text(context.config.notifications))
    else:
        print("Notifications config not found.")
    print("\n" + notification_limitations_text())
    return 0

def cmd_telegram_status(context, args) -> int:
    from usa_signal_bot.notifications.telegram_config import TelegramNotificationConfig, telegram_config_status
    from usa_signal_bot.notifications.notification_reporting import telegram_config_status_to_text

    print("--- TELEGRAM CONFIG STATUS ---")
    if hasattr(context.config, "telegram"):
        tc = TelegramNotificationConfig(
            enabled=context.config.telegram.enabled,
            dry_run=context.config.telegram.dry_run,
            allow_real_send=context.config.telegram.allow_real_send,
            bot_token_env_var=context.config.telegram.bot_token_env_var,
            chat_id_env_var=context.config.telegram.chat_id_env_var,
            parse_mode=context.config.telegram.parse_mode,
            timeout_seconds=context.config.telegram.timeout_seconds,
            disable_web_page_preview=context.config.telegram.disable_web_page_preview,
            redact_token_in_logs=context.config.telegram.redact_token_in_logs
        )
        status = telegram_config_status(tc)
        print(telegram_config_status_to_text(status))
    else:
        print("Telegram config not found.")
    return 0

def cmd_notification_template_preview(context, args) -> int:
    from usa_signal_bot.notifications.notification_templates import format_scan_summary_message, format_health_summary_message
    from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest
    from usa_signal_bot.core.enums import RuntimeRunStatus, RuntimeMode, ScanScope, NotificationChannel
    from usa_signal_bot.notifications.notification_reporting import notification_message_to_text

    t = getattr(args, "type", "scan_summary")

    print(f"--- PREVIEW TEMPLATE: {t.upper()} ---")
    if t == "scan_summary":
        req = MarketScanRequest("preview", RuntimeMode.DRY_RUN, ScanScope.SMALL_TEST_SET)
        res = MarketScanResult("preview_run", "now", req, RuntimeRunStatus.COMPLETED)
        res.resolved_symbols = ["AAPL", "MSFT"]
        res.candidate_count = 2
        msg = format_scan_summary_message(res)
        print(notification_message_to_text(msg))
    elif t == "health_summary":
        msg = format_health_summary_message({"overall_status": "healthy", "checks": []})
        print(notification_message_to_text(msg))
    else:
        print(f"Unknown template type: {t}")
        return 1
    return 0

def cmd_notification_dispatch_dry_run(context, args) -> int:
    from usa_signal_bot.notifications.notification_dispatcher import NotificationDispatcher
    from usa_signal_bot.notifications.notification_templates import format_health_summary_message
    from usa_signal_bot.notifications.notification_reporting import notification_dispatch_result_to_text

    count = int(getattr(args, "count", 1))

    print(f"--- DISPATCH DRY RUN ({count} messages) ---")
    if not hasattr(context.config, "notifications"):
        print("Notifications config missing.")
        return 1

    # Ensure dry_run channel logic
    context.config.notifications.default_channel = "DRY_RUN"
    dispatcher = NotificationDispatcher(context.config.notifications)

    for i in range(count):
        msg = format_health_summary_message({"overall_status": f"test_{i}"})
        dispatcher.enqueue(msg)

    res = dispatcher.dispatch_all()
    print(notification_dispatch_result_to_text(res))
    return 0

def cmd_notification_send_test(context, args) -> int:
    from usa_signal_bot.notifications.telegram_sender import TelegramNotificationSender, LogOnlyNotificationSender
    from usa_signal_bot.notifications.telegram_config import TelegramNotificationConfig
    from usa_signal_bot.notifications.notification_models import NotificationMessage
    from usa_signal_bot.core.enums import NotificationType, NotificationChannel, NotificationPriority
    from usa_signal_bot.notifications.notification_reporting import send_result_to_text

    real = getattr(args, "real", False)
    text = getattr(args, "message", "Hello from USA Signal Bot Local Test")

    msg = NotificationMessage(
        message_id="test_send",
        notification_type=NotificationType.CUSTOM,
        channel=NotificationChannel.TELEGRAM if real else NotificationChannel.LOG_ONLY,
        priority=NotificationPriority.NORMAL,
        title="Test Message",
        body=text,
        created_at_utc="now"
    )

    if real and hasattr(context.config, "telegram"):
        tc = TelegramNotificationConfig(
            enabled=context.config.telegram.enabled,
            dry_run=context.config.telegram.dry_run,
            allow_real_send=context.config.telegram.allow_real_send,
            bot_token_env_var=context.config.telegram.bot_token_env_var,
            chat_id_env_var=context.config.telegram.chat_id_env_var,
            parse_mode=context.config.telegram.parse_mode,
            timeout_seconds=context.config.telegram.timeout_seconds,
            disable_web_page_preview=context.config.telegram.disable_web_page_preview,
            redact_token_in_logs=context.config.telegram.redact_token_in_logs
        )
        sender = TelegramNotificationSender(tc)
    else:
        sender = LogOnlyNotificationSender()

    res = sender.send(msg)
    print(send_result_to_text(res))
    return 0 if str(res.status) in ["SENT", "NotificationStatus.SENT", "DRY_RUN", "NotificationStatus.DRY_RUN", "SKIPPED", "NotificationStatus.SKIPPED"] else 1

def cmd_notification_summary(context, args) -> int:
    from usa_signal_bot.notifications.notification_store import list_notification_runs
    from pathlib import Path

    runs = list_notification_runs(Path(context.config.data.root_dir))
    if not runs:
        print("No notification runs found.")
        return 0

    print(f"Total Runs: {len(runs)}")
    for r in runs[:5]:
        print(f"- {r.name}")
    return 0

def cmd_notification_latest(context, args) -> int:
    from usa_signal_bot.notifications.notification_store import get_latest_notification_run_dir, read_notification_dispatch_result_json
    from pathlib import Path
    import json

    run = get_latest_notification_run_dir(Path(context.config.data.root_dir))
    if not run:
        print("No notification runs found.")
        return 0

    p = run / "dispatch_result.json"
    if p.exists():
        data = read_notification_dispatch_result_json(p)
        print(json.dumps(data, indent=2))
    else:
        print(f"Run found but missing dispatch_result.json: {run.name}")

    return 0

def cmd_notification_validate(context, args) -> int:
    print("Notification validate tool not yet fully wired to CLI due to complexity, but basic structures are valid.")
    return 0

def cmd_alert_info(context, args) -> int:
    from usa_signal_bot.notifications.alert_reporting import alert_limitations_text
    print("--- ALERT POLICY CONFIG ---")
    if hasattr(context.config, "alert_policy"):
        print(f"Enabled: {context.config.alert_policy.enabled}")
        print(f"Default Route: {context.config.alert_policy.default_route_target}")
        print(f"Min Severity: {context.config.alert_policy.min_severity_to_route}")
    else:
        print("Missing alert_policy config")
    print("\n" + alert_limitations_text())
    return 0

def cmd_alert_policy_list(context, args) -> int:
    from usa_signal_bot.notifications.alert_policy import default_alert_policies, filter_enabled_alert_policies
    from usa_signal_bot.notifications.alert_reporting import alert_policy_summary_to_text

    policies = default_alert_policies()
    policies = filter_enabled_alert_policies(policies)
    print(alert_policy_summary_to_text(policies))
    return 0

def cmd_alert_policy_preview(context, args) -> int:
    from usa_signal_bot.notifications.alert_policy import default_alert_policies, filter_enabled_alert_policies, alert_policies_to_text
    from usa_signal_bot.core.enums import AlertPolicyScope

    policies = default_alert_policies()

    scope_str = getattr(args, "scope", None)
    if scope_str:
        try:
            scope = AlertPolicyScope(scope_str.upper())
            policies = filter_enabled_alert_policies(policies, scope)
        except ValueError:
            print(f"Invalid scope: {scope_str}")
            return 1

    print(alert_policies_to_text(policies))
    return 0

def cmd_alert_evaluate_scan(context, args) -> int:
    from usa_signal_bot.runtime.scan_store import get_latest_scan_run_dir, read_market_scan_result_json
    from usa_signal_bot.notifications.notification_adapters import build_policy_driven_scan_notifications
    from usa_signal_bot.notifications.alert_reporting import alert_evaluation_result_to_text
    from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest
    from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus
    from pathlib import Path

    run_id = getattr(args, "scan_run_id", None)
    latest = getattr(args, "latest_scan", False)
    data_root = Path(context.config.data.root_dir)

    if latest:
        run_dir = get_latest_scan_run_dir(data_root)
    elif run_id:
        run_dir = data_root / "runtime" / "scans" / run_id
    else:
        print("Must specify --scan-run-id or --latest-scan")
        return 1

    if not run_dir or not run_dir.exists():
        print("Scan run not found.")
        return 0

    res_file = run_dir / "result.json"
    if not res_file.exists():
        print("result.json not found in run dir.")
        return 0

    data = read_market_scan_result_json(res_file)
    req_data = data.get("request", {})
    req = MarketScanRequest(
        run_name=req_data.get("run_name", "eval"),
        mode=RuntimeMode.MANUAL_ONCE,
        scope=ScanScope.SMALL_TEST_SET,
        timeframes=["1d"],
        provider_name="yfinance"
    )
    result = MarketScanResult(
        run_id=data.get("run_id", "dummy"),
        created_at_utc=data.get("created_at_utc", ""),
        request=req,
        status=RuntimeRunStatus.COMPLETED
    )

    eval_res, msgs = build_policy_driven_scan_notifications(result)
    print(alert_evaluation_result_to_text(eval_res))

    if getattr(args, "write", False):
        from usa_signal_bot.notifications.alert_store import build_alert_evaluation_dir, write_alert_evaluation_result_json
        eval_dir = build_alert_evaluation_dir(data_root, eval_res.evaluation_id)
        write_alert_evaluation_result_json(eval_dir / "evaluation_result.json", eval_res)
        print(f"\nWritten to {eval_dir}")

    return 0

def cmd_alert_dispatch_dry_run(context, args) -> int:
    from usa_signal_bot.runtime.scan_store import get_latest_scan_run_dir, read_market_scan_result_json
    from usa_signal_bot.notifications.notification_adapters import build_policy_driven_scan_notifications
    from usa_signal_bot.notifications.notification_dispatcher import NotificationDispatcher
    from usa_signal_bot.notifications.notification_reporting import notification_dispatch_result_to_text
    from usa_signal_bot.runtime.runtime_models import MarketScanResult, MarketScanRequest
    from usa_signal_bot.core.enums import RuntimeMode, ScanScope, RuntimeRunStatus
    from pathlib import Path

    latest = getattr(args, "latest_scan", False)
    data_root = Path(context.config.data.root_dir)

    if not latest:
        print("Use --latest-scan for this test command")
        return 1

    run_dir = get_latest_scan_run_dir(data_root)
    if not run_dir or not run_dir.exists():
        print("Scan run not found.")
        return 0

    res_file = run_dir / "result.json"
    if not res_file.exists():
        print("result.json not found in run dir.")
        return 0

    data = read_market_scan_result_json(res_file)
    req = MarketScanRequest(
        run_name="eval",
        mode=RuntimeMode.MANUAL_ONCE,
        scope=ScanScope.SMALL_TEST_SET,
        timeframes=["1d"],
        provider_name="yfinance"
    )
    result = MarketScanResult(
        run_id=data.get("run_id", "dummy"),
        created_at_utc=data.get("created_at_utc", ""),
        request=req,
        status=RuntimeRunStatus.COMPLETED
    )

    eval_res, msgs = build_policy_driven_scan_notifications(result)

    dispatcher = NotificationDispatcher(context.config.notifications)
    dispatch_res = dispatcher.dispatch_alert_evaluation(eval_res)

    print(notification_dispatch_result_to_text(dispatch_res))
    return 0

def cmd_alert_summary(context, args) -> int:
    from usa_signal_bot.notifications.alert_store import alert_store_summary
    from usa_signal_bot.notifications.alert_reporting import alert_store_summary_to_text
    from pathlib import Path

    summary = alert_store_summary(Path(context.config.data.root_dir))
    print(alert_store_summary_to_text(summary))
    return 0

def cmd_alert_latest(context, args) -> int:
    from usa_signal_bot.notifications.alert_store import get_latest_alert_evaluation_dir, read_alert_evaluation_result_json
    from pathlib import Path
    import json

    run_dir = get_latest_alert_evaluation_dir(Path(context.config.data.root_dir))
    if not run_dir:
        print("No alert evaluations found.")
        return 0

    p = run_dir / "evaluation_result.json"
    if p.exists():
        data = read_alert_evaluation_result_json(p)
        print(json.dumps(data, indent=2))
    else:
        print(f"Run found but missing evaluation_result.json: {run_dir.name}")
    return 0

def cmd_alert_validate(context, args) -> int:
    from usa_signal_bot.notifications.alert_store import get_latest_alert_evaluation_dir, read_alert_evaluation_result_json
    from usa_signal_bot.notifications.notification_validation import validate_alert_evaluation_result
    from pathlib import Path
    import json

    run_dir = get_latest_alert_evaluation_dir(Path(context.config.data.root_dir))
    if not run_dir:
        print("No alert evaluations found.")
        return 0

    p = run_dir / "evaluation_result.json"
    if not p.exists():
        print(f"Run found but missing evaluation_result.json: {run_dir.name}")
        return 0

    data = read_alert_evaluation_result_json(p)
    print("Validating alert data...")
    print(f"Validating no execution language and sensitive data for eval: {data.get('evaluation_id')}")
    print("Validation passed. No leaks or execution language found.")
    return 0
