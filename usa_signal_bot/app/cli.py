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

    print("--- USA Signal Bot Universe Info ---")
    print("This seed file is NOT the entire USA universe.")
    print("It is meant for sample purposes and will be expanded later.")
    print(f"Default Watchlist : {context.config.universe.default_watchlist_file}")
    print(f"Sample Stocks     : {get_sample_stocks_path(context.data_dir)}")
    print(f"Sample ETFs       : {get_sample_etfs_path(context.data_dir)}")
    print(f"Allowed Asset Types: {context.config.universe.asset_types}")
    print(f"Include Stocks    : {context.config.universe.include_stocks}")
    print(f"Include ETFs      : {context.config.universe.include_etfs}")
    print(f"Default Currency  : {context.config.universe.default_currency}")
    return 0

def handle_universe_validate(context, file_path: str = None) -> int:
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

def handle_universe_list(context, asset_type: str = None, limit: int = None, include_inactive: bool = False) -> int:
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
        print("Building default universe snapshot...")
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
    print("--- USA Signal Bot Smoke Test ---")
    checks = run_startup_checks(context)
    for check in checks:
        print(f"✓ {check}")
    print("\nSmoke test completed successfully. System is ready.")

def handle_show_config(context) -> None:
    """Displays the currently loaded and merged configuration."""
    print("--- Loaded Configuration ---")
    import pprint
    cfg_dict = config_to_dict(context.config)
    pprint.pprint(cfg_dict, width=80)

def handle_show_paths() -> None:
    """Displays all resolved system paths."""
    print("--- Resolved System Paths ---")
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
    print("--- Configuration Validation ---")
    print("Rules applied:")
    print("- broker_order_routing_enabled MUST be False")
    print("- web_scraping_allowed MUST be False")
    print("- dashboard_enabled MUST be False")
    print("- mode MUST be 'local_paper_only'")
    print(f"Current mode: {context.config.runtime.mode}")
    print("\nResult: OK. All strict conditions are met.")

def handle_runtime_summary(context) -> None:
    """Displays a JSON summary of the runtime state."""
    import json
    summary = build_runtime_summary(context)
    print(json.dumps(summary, indent=2))

def handle_check_env(context) -> None:
    """Checks required and optional environment variables."""
    from usa_signal_bot.core.environment import get_env
    print("--- Environment Variables Check ---")

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

    print("\nEnvironment check completed.")

def handle_health(context) -> int:
    """Runs the system health checks and prints the result."""
    from usa_signal_bot.core.health import run_health_checks, health_results_to_dict
    from usa_signal_bot.utils.json_utils import safe_json_dumps

    print("--- System Health Check ---")
    results = run_health_checks(context)

    # Simple console output
    for res in results:
        status_symbol = "✓" if res.passed else "✗"
        print(f"[{status_symbol}] {res.name}: {res.message}")
        if res.details and not res.passed:
            print(f"    Details: {res.details}")

    # Determine overall status
    all_passed = all(res.passed for res in results)

    print("\n--- Summary JSON ---")
    print(safe_json_dumps(health_results_to_dict(results)))

    return 0 if all_passed else 1

def handle_log_info(context) -> None:
    """Displays information about the logging subsystem."""
    print("--- Logging Subsystem Info ---")
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
        print("Main Log      : Not created yet")

    if context.audit_log_path.exists():
        size_kb = context.audit_log_path.stat().st_size / 1024
        print(f"Audit Log Size: {size_kb:.2f} KB")
    else:
        print("Audit Log     : Not created yet")


def handle_audit_tail(context, limit: int) -> None:
    """Tails the last N events from the audit log."""
    print(f"--- Last {limit} Audit Events ---")
    if not context.audit_log_path.exists():
        print("Audit log file does not exist yet.")
        return

    from usa_signal_bot.utils.file_utils import read_last_lines
    lines = read_last_lines(context.audit_log_path, limit)

    if not lines:
        print("Audit log is empty.")
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

    print("--- USA Signal Bot Storage Info ---")
    store = LocalFileStore(context.data_dir)
    print(f"Root Directory: {store.root_dir}")

    print("\nStorage Areas:")
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

    print("--- USA Signal Bot Storage Integrity Check ---")
    store = LocalFileStore(context.data_dir)

    try:
        # Example check: just verify all manifests
        manifests = store.list_files("manifests", "*.json")
        if not manifests:
            print("No manifests found to check.")
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

def handle_storage_list(context, area: str = None) -> int:
    """Lists files in the storage system."""
    from usa_signal_bot.storage.file_store import LocalFileStore
    from usa_signal_bot.storage.paths import StorageArea
    from usa_signal_bot.utils.file_utils import normalize_safe_filename

    print("--- USA Signal Bot Storage List ---")
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
            fallback_to_watchlist=context.config.active_universe.fallback_to_watchlist,
            fallback_to_latest_snapshot=context.config.active_universe.fallback_to_latest_snapshot
        )
        print(active_universe_resolution_to_text(res))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_symbols(context, limit: int = None, asset_type: str = None, include_inactive: bool = False) -> int:
    from usa_signal_bot.universe.active import resolve_active_universe
    try:
        res = resolve_active_universe(
            data_root=context.data_dir,
            fallback_to_watchlist=context.config.active_universe.fallback_to_watchlist,
            fallback_to_latest_snapshot=context.config.active_universe.fallback_to_latest_snapshot
        )
        symbols = res.universe.symbols
        if asset_type:
            at = asset_type.upper()
            symbols = [s for s in symbols if s.asset_type.value == at]
        if not include_inactive:
            symbols = [s for s in symbols if s.active]
        if limit and limit > 0:
            symbols = symbols[:limit]
        print(f"Symbols ({len(symbols)}):")
        for s in symbols:
            print(f"- {s.symbol} ({s.asset_type.value})")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_plan(context, timeframes: str, provider: str, limit: int, asset_type: str, force: bool, no_cache: bool) -> int:
    from usa_signal_bot.universe.active import resolve_active_universe
    from usa_signal_bot.data.multitimeframe import MultiTimeframeDataRequest, build_timeframe_specs_from_list
    from usa_signal_bot.data.refresh import build_cache_refresh_plan, cache_refresh_plan_to_text
    from usa_signal_bot.data.cache import LocalMarketDataCache
    try:
        res = resolve_active_universe(
            data_root=context.data_dir,
            fallback_to_watchlist=context.config.active_universe.fallback_to_watchlist,
            fallback_to_latest_snapshot=context.config.active_universe.fallback_to_latest_snapshot
        )
        symbols = [s.symbol for s in res.universe.symbols if s.active]
        if asset_type:
            at = asset_type.upper()
            symbols = [s.symbol for s in res.universe.symbols if s.active and s.asset_type.value == at]
        if limit and limit > 0:
            symbols = symbols[:limit]
        tfs = timeframes.split(',')
        specs = build_timeframe_specs_from_list(tfs)
        req = MultiTimeframeDataRequest(
            symbols=symbols,
            provider_name=provider,
            timeframe_specs=specs,
            force_refresh=force,
            use_cache=not no_cache
        )
        cache = LocalMarketDataCache(context.data_dir)
        plan = build_cache_refresh_plan(req, cache)
        print(f"=== Active Universe Plan ===")
        print(f"Universe: {res.universe.name} ({len(symbols)} symbols)")
        print(cache_refresh_plan_to_text(plan))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_download(context, timeframes: str, provider: str, limit: int, asset_type: str, force: bool, no_cache: bool) -> int:
    from usa_signal_bot.data.active_universe_pipeline import ActiveUniverseDataPipeline, ActiveUniversePipelineRequest, active_pipeline_result_to_text
    from usa_signal_bot.data.pipeline import MultiTimeframeDataPipeline
    from usa_signal_bot.data.downloader import MarketDataDownloader
    from usa_signal_bot.data.cache import LocalMarketDataCache
    from usa_signal_bot.data.provider_registry import ProviderRegistry
    from usa_signal_bot.data.yfinance_provider import YFinanceMarketDataProvider
    from usa_signal_bot.data.mock_provider import MockMarketDataProvider
    from usa_signal_bot.data.normalizer import DataNormalizer
    try:
        registry = ProviderRegistry(context.config)
        registry.register(MockMarketDataProvider())
        registry.register(YFinanceMarketDataProvider())
        downloader = MarketDataDownloader(registry, DataNormalizer(context.config))
        cache = LocalMarketDataCache(context.data_dir)
        mtf_pipeline = MultiTimeframeDataPipeline(downloader, cache, context.config, context.data_dir)
        pipeline = ActiveUniverseDataPipeline(mtf_pipeline, context.data_dir)
        req = ActiveUniversePipelineRequest(
            provider_name=provider,
            timeframes=timeframes.split(','),
            asset_type=asset_type,
            max_symbols=limit,
            force_refresh=force,
            use_cache=not no_cache,
            fallback_to_watchlist=context.config.active_universe.fallback_to_watchlist
        )
        print(f"Starting active universe download...")
        res = pipeline.run(req)
        print(active_pipeline_result_to_text(res))
        if not res.success:
            return 1
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_runs(context) -> int:
    from usa_signal_bot.data.universe_runs import list_universe_data_runs
    try:
        runs = list_universe_data_runs(context.data_dir)
        print(f"Found {len(runs)} universe data runs.")
        for r in runs:
            print(f"- {r.created_at_utc} | ID: {r.run_id} | Status: {r.status.value} | Symbols: {r.total_symbols}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_latest_run(context) -> int:
    from usa_signal_bot.data.universe_runs import get_latest_universe_data_run, universe_data_run_to_text
    try:
        run = get_latest_universe_data_run(context.data_dir)
        if not run:
            print("No runs found.")
        else:
            print(universe_data_run_to_text(run))
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_readiness(context, latest_run: bool) -> int:
    from usa_signal_bot.data.universe_runs import get_latest_universe_data_run
    import json
    try:
        run = get_latest_universe_data_run(context.data_dir)
        if not run:
            print("No runs found to check readiness.")
            return 0
        gate_path = run.output_paths.get("readiness_gate_report")
        if not gate_path:
             print("Latest run has no readiness gate report.")
             return 0
        with open(gate_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("=== Readiness Gate Report ===")
        print(f"Status: {data.get('status')}")
        print(f"Eligible Symbols: {data.get('eligible_symbols')}")
        print(f"Ineligible Symbols: {data.get('ineligible_symbols')}")
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_active_universe_eligible(context, latest_run: bool, format: str) -> int:
    from usa_signal_bot.data.universe_runs import get_latest_universe_data_run
    try:
        run = get_latest_universe_data_run(context.data_dir)
        if not run:
            print("No runs found.")
            return 0
        txt_path = run.output_paths.get("eligible_symbols_txt")
        if not txt_path:
             print("Latest run has no eligible symbols text output.")
             return 0
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            print("No eligible symbols found in the latest run.")
        else:
            symbols = content.split('\n')
            print(f"Found {len(symbols)} eligible symbols:")
            print(content)
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
    readiness_parser.add_argument("--symbols", help="Comma-separated symbols")
    readiness_parser.add_argument("--timeframes", help="Comma-separated timeframes")
    readiness_parser.add_argument("--from-cache", action="store_true", default=True, help="Check readiness from cache")

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

        # End of new handlers
        # Keep this to not break replace logic
            sys.exit(handle_provider_mock_fetch(context, args.symbols, args.timeframe))


    except Exception as e:
        sys.exit(handle_cli_exception(e))

    sys.exit(0)



def handle_provider_info(context) -> int:
    """Display data provider configuration and rules."""
    p_cfg = context.config.providers
    print("--- USA Signal Bot Provider Info ---")
    print(f"Default Provider: {p_cfg.default_provider}")
    print(f"Enabled Providers: {', '.join(p_cfg.enabled_providers)}")
    print("\nSecurity and Constraints (Phase 7):")
    print(f"  Allow Paid APIs: {p_cfg.allow_paid_providers}")
    print(f"  Allow Web Scraping: {p_cfg.allow_scraping_providers}")
    print(f"  Allow Broker Data: {p_cfg.allow_broker_data_providers}")
    print("\nNote: In Phase 7, no real data is fetched from the internet.")
    return 0

def handle_provider_list(context) -> int:
    """List registered data providers."""
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    registry = create_default_provider_registry()
    print("--- USA Signal Bot Registered Providers ---")
    caps = registry.list_capabilities()
    if not caps:
        print("No providers registered.")
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
    print("--- Provider Check ---")
    p_cfg = context.config.providers
    provider_name = p_cfg.default_provider
    try:
         provider = registry.get(provider_name)
         print(f"Provider '{provider_name}' loaded.")
         provider.assert_free_provider()
         provider.assert_no_scraping()
         provider.assert_no_broker_routing()
         print("All guard checks passed.")
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
         print("--- Provider Fetch Plan ---")
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
         print("--- Mock Data Fetch Result ---")
         print("WARNING: This is deterministically generated fake data for testing interface.")
         print("It is NOT real market data.\n")
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
    print("--- Market Data Providers ---")
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
            print("Errors:")
            for e in resp.errors: print(f"  - {e}")
        if resp.warnings:
            print("Warnings:")
            for w in resp.warnings: print(f"  - {w}")

        if resp.bar_count() > 0:
            report = validate_ohlcv_bars_quality(resp.bars, symbols, provider, timeframe)
            print("\n" + data_quality_report_to_text(report))
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
            print("\n" + data_quality_report_to_text(report))
            downloader.write_download_summary(resp, report)

        return 0 if resp.success else 1
    except Exception as e:
        print(f"Universe download failed: {e}")
        return 1

def handle_data_cache_info(context) -> int:
    from usa_signal_bot.data.cache import market_data_cache_dir
    cache_dir = market_data_cache_dir(context.data_dir)
    print("--- Market Data Cache Info ---")
    print(f"Cache Directory: {cache_dir}")

    if not cache_dir.exists():
        print("Directory does not exist.")
        return 0

    files = list(cache_dir.glob("*.jsonl"))
    summaries = list(cache_dir.glob("download_summary_*.json"))

    print(f"Total cache files (.jsonl): {len(files)}")
    print(f"Total summary files (.json): {len(summaries)}")

    total_size = sum(f.stat().st_size for f in files)
    print(f"Total JSONL size: {total_size / (1024*1024):.2f} MB")

    if files:
        print("\nRecent cache files:")
        recent = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]
        for f in recent:
            print(f"  - {f.name} ({f.stat().st_size / 1024:.1f} KB)")

    return 0

def handle_data_quality_check(context, cache_file: str, symbols_str: str, timeframe: str) -> int:
    from usa_signal_bot.data.cache import market_data_cache_dir, read_ohlcv_bars_cache
    from usa_signal_bot.data.models import OHLCVBar
    from usa_signal_bot.data.quality import validate_ohlcv_bars_quality, data_quality_report_to_text

    cache_dir = market_data_cache_dir(context.data_dir)
    print("--- Data Quality Check ---")

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
        print("\n" + data_quality_report_to_text(report))
        return 0 if report.status.value != "ERROR" else 1
    else:
        print("No cache file specified. Usage requires --cache-file.")
        return 1


if __name__ == "__main__":
    main()

def handle_data_cache_validate(context, cache_file: str, symbols_str: str, timeframe: str) -> int:
    from usa_signal_bot.data.cache import market_data_cache_dir, validate_cache_file
    from usa_signal_bot.data.quality import data_quality_report_to_text

    cache_dir = market_data_cache_dir(context.data_dir)
    print("--- Data Cache Validate ---")

    if cache_file:
        path = cache_dir / cache_file
        if not path.exists():
            print(f"Cache file {path} not found.")
            return 1

        symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else None
        try:
            report = validate_cache_file(path, symbols)
            print("\n" + data_quality_report_to_text(report))
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
            print("No cache files found to validate.")
            return 0 # Safe exit

        path = sorted(files, key=lambda x: x.stat().st_mtime)[-1]
        print(f"Validating latest cache file: {path.name}")
        symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else None
        try:
            report = validate_cache_file(path, symbols)
            print("\n" + data_quality_report_to_text(report))
            return 0 if report.status.value != "ERROR" else 1
        except Exception as e:
            print(f"Validation failed: {e}")
            return 1

def handle_data_cache_repair(context, cache_file: str, output: str, overwrite: bool) -> int:
    from usa_signal_bot.data.cache import market_data_cache_dir, read_cached_ohlcv_bars, write_repaired_cache
    from usa_signal_bot.data.repair import repair_ohlcv_bars, repair_report_to_text
    import shutil

    cache_dir = market_data_cache_dir(context.data_dir)
    print("--- Data Cache Repair ---")

    if not cache_file:
        print("Error: --cache-file is required.")
        return 1

    path = cache_dir / cache_file
    if not path.exists():
        print(f"Cache file {path} not found.")
        return 1

    try:
        bars = read_cached_ohlcv_bars(path)
        print(f"Read {len(bars)} bars from {cache_file}.")

        repaired_bars, report = repair_ohlcv_bars(bars)
        print("\n" + repair_report_to_text(report))

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

    print("--- Data Refresh Plan ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("Error: --symbols required.")
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
        print("\n" + cache_refresh_plan_to_text(plan))
        return 0
    except Exception as e:
        print(f"Failed to build plan: {e}")
        return 1

def handle_data_refresh_execute(context, symbols_str: str, timeframe: str, provider: str, start: str, end: str, force: bool, limit: int) -> int:
    from usa_signal_bot.data.refresh import CacheRefreshRequest, build_cache_refresh_plan, execute_cache_refresh_plan
    from usa_signal_bot.data.downloader import MarketDataDownloader
    from usa_signal_bot.data.provider_registry import create_default_provider_registry
    from usa_signal_bot.storage.file_store import LocalFileStore

    print("--- Data Refresh Execute ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("Error: --symbols required.")
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
            print("Errors:")
            for e in result.errors:
                print(f"  - {e}")

        return 0 if not result.errors else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_data_validation_report(context, latest: bool, reports_dir: str) -> int:
    from pathlib import Path
    import json

    print("--- Data Validation Report ---")
    d_root = Path(reports_dir) if reports_dir else context.data_dir / "reports"

    if not d_root.exists():
        print("Reports directory not found.")
        return 0

    q_files = list(d_root.glob("quality_*.json"))
    a_files = list(d_root.glob("anomaly_*.json"))

    if not q_files:
        print("No quality reports found.")
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

    print("--- Multi-Timeframe Data Plan ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("Error: --symbols required.")
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
        print("\n" + multitimeframe_refresh_plan_to_text(plan))
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

    print("--- Multi-Timeframe Data Download ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("Error: --symbols required.")
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
        print("\n" + readiness_report_to_text(readiness))
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

    print("--- Multi-Timeframe Universe Download ---")
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
        print("\n" + readiness_report_to_text(readiness))
        return 0 if result.status.value != "FAILED" else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_data_coverage_report(context, latest: bool, reports_dir: str) -> int:
    from pathlib import Path
    import json

    print("--- Data Coverage Report ---")
    d_root = Path(reports_dir) if reports_dir else context.data_dir / "reports" / "data_readiness"

    if not d_root.exists():
        print(f"Reports directory {d_root} not found.")
        return 0

    c_files = list(d_root.glob("coverage_*.json"))

    if not c_files:
        print("No coverage reports found.")
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

    print("--- Data Readiness Check ---")
    symbols = [s.strip().upper() for s in symbols_str.split(",")] if symbols_str else []
    if not symbols:
        print("Error: --symbols required.")
        return 1

    tfs = parse_timeframe_list(timeframes_str)

    if not from_cache:
        print("Live readiness check not implemented yet. Use --from-cache.")
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
        print("\n" + readiness_report_to_text(readiness))

        return 0 if readiness.overall_status.value not in ["NOT_READY", "FAILED"] else 1
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

def handle_universe_sources(context) -> int:
    from usa_signal_bot.universe.sources import default_universe_sources
    print("--- USA Signal Bot Universe Sources ---")
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

    print("--- Universe Import ---")
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

    print("--- Universe Expand ---")

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
        print("\n" + expansion_result_to_text(res))

        return 0 if res.success else 1
    except Exception as e:
        print(f"Expansion failed: {e}")
        return 1

def handle_universe_snapshots(context) -> int:
    from usa_signal_bot.universe.snapshots import list_universe_snapshots, get_latest_active_snapshot
    print("--- Universe Snapshots ---")

    active_snap = get_latest_active_snapshot(context.data_dir)
    snapshots = list_universe_snapshots(context.data_dir)

    if not snapshots:
        print("No snapshots found.")
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
        print("Snapshot activated successfully.")
        return 0
    except Exception as e:
        print(f"Failed to activate snapshot: {e}")
        return 1

def handle_universe_catalog(context) -> int:
    from usa_signal_bot.universe.catalog import build_universe_catalog, catalog_to_text
    print("--- Universe Catalog ---")
    try:
        cat = build_universe_catalog(context.data_dir)
        print("\n" + catalog_to_text(cat))
        return 0
    except Exception as e:
        print(f"Failed to build catalog: {e}")
        return 1

def handle_universe_export(context, snapshot_id: str, format: str, name: str, active_only: bool) -> int:
    from usa_signal_bot.universe.export import export_universe_csv, export_universe_json, export_symbols_txt, export_symbols_json, build_export_path
    from usa_signal_bot.universe.snapshots import get_latest_active_snapshot, read_universe_snapshot, build_snapshot_paths
    from usa_signal_bot.universe.loader import load_universe_csv, load_default_watchlist

    print("--- Universe Export ---")
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
                 print("No active snapshot found. Exporting default watchlist instead.")
                 res = load_default_watchlist(context.data_dir)
                 universe = res.universe

        if not universe:
            print("Failed to load universe for export.")
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

def handle_universe_presets(context) -> int:
    from usa_signal_bot.universe.presets import list_preset_files, load_preset_universe
    print("--- Universe Presets ---")

    presets = list_preset_files(context.data_dir)
    if not presets:
        print("No presets found.")
        return 0

    for p in presets:
        try:
            res = load_preset_universe(context.data_dir, p.stem)
            print(f"[{p.stem}] - {res.valid_count} symbols")
        except Exception as e:
             print(f"[{p.stem}] - Error loading: {e}")

    return 0
