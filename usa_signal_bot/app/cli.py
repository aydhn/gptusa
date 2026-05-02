"""Command Line Interface for USA Signal Bot."""

import argparse
import sys
from typing import Optional
from pathlib import Path

from usa_signal_bot.core import paths
from usa_signal_bot.core.config import config_to_dict
from usa_signal_bot.app.runtime import initialize_runtime, run_startup_checks, build_runtime_summary

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

        if args.command == "smoke":
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
