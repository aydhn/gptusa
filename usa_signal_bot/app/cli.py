"""Command Line Interface for USA Signal Bot."""

import argparse
import sys
import json
from pprint import pprint
import logging
from pathlib import Path

from usa_signal_bot.app.runtime import initialize_runtime, run_startup_checks, build_runtime_summary
from usa_signal_bot.core import paths
from usa_signal_bot.core.config import config_to_dict
from usa_signal_bot.utils.dict_utils import redact_sensitive_keys
from usa_signal_bot.core.environment import get_env, mask_secret
from usa_signal_bot.core.error_handling import handle_cli_exception
from usa_signal_bot.core.health import run_health_checks, health_results_to_dict
from usa_signal_bot.core.audit import tail_audit_events
from usa_signal_bot.utils.json_utils import safe_json_dumps

def handle_smoke(context):
    """Run smoke checks to ensure basic components load correctly."""
    print("USA Signal Bot smoke check")
    print(f"Project: {context.config.project.name}")
    print(f"Mode: {context.config.runtime.mode}")
    print(f"Broker routing enabled: {context.config.runtime.broker_order_routing_enabled}")
    print(f"Web scraping allowed: {context.config.runtime.web_scraping_allowed}")
    print(f"Dashboard enabled: {context.config.runtime.dashboard_enabled}")

    checks = run_startup_checks(context)
    for check in checks:
        print(f"Check: {check} - OK")

    print("Status: OK")

def handle_show_config(context):
    """Display the loaded configuration with redacted secrets."""
    print("--- USA Signal Bot Configuration ---")
    config_dict = config_to_dict(context.config)
    safe_config = redact_sensitive_keys(config_dict)
    print(json.dumps(safe_config, indent=2))

def handle_show_paths():
    """Display the core directory paths."""
    print("--- USA Signal Bot Paths ---")
    print(f"PROJECT_ROOT: {paths.PROJECT_ROOT}")
    print(f"CONFIG_DIR: {paths.CONFIG_DIR}")
    print(f"DATA_DIR: {paths.DATA_DIR}")
    print(f"LOGS_DIR: {paths.LOGS_DIR}")
    print(f"REPORTS_DIR: {paths.REPORTS_DIR}")
    print(f"CACHE_DIR: {paths.CACHE_DIR}")
    print(f"PAPER_DIR: {paths.PAPER_DIR}")
    print(f"BACKTESTS_DIR: {paths.BACKTESTS_DIR}")

def handle_validate_config(context):
    """Explicitly validate the loaded configuration."""
    # initialize_runtime already validates the config fully.
    print("Config validation: OK")

def handle_runtime_summary(context):
    """Display a summary of the current runtime context."""
    print("--- USA Signal Bot Runtime Summary ---")
    summary = build_runtime_summary(context)
    print(safe_json_dumps(summary))

def handle_check_env(context):
    """Check required environment variables, specially for Telegram."""
    print("--- USA Signal Bot Environment Check ---")
    telegram_config = context.config.telegram

    print(f"Telegram Enabled: {telegram_config.enabled}")

    bot_token_env = telegram_config.bot_token_env
    chat_id_env = telegram_config.chat_id_env

    bot_token_val = get_env(bot_token_env)
    chat_id_val = get_env(chat_id_env)

    print(f"Env {bot_token_env}: {mask_secret(bot_token_val)}")
    print(f"Env {chat_id_env}: {mask_secret(chat_id_val)}")

    if telegram_config.enabled:
        if not bot_token_val:
            print(f"WARNING: Telegram is enabled but {bot_token_env} is not set!")
        if not chat_id_val:
            print(f"WARNING: Telegram is enabled but {chat_id_env} is not set!")
        if bot_token_val and chat_id_val:
            print("Telegram environment variables are properly set.")
    else:
        print("Telegram is disabled, missing tokens are expected.")

def handle_health(context) -> int:
    """Run full health checks and report."""
    print("--- USA Signal Bot Health Check ---")
    results = run_health_checks(context)

    all_passed = True
    for res in results:
        status = "PASS" if res.passed else "FAIL"
        print(f"[{status}] {res.name}: {res.message}")
        if not res.passed:
            all_passed = False

    if all_passed:
        print("\nOverall Status: HEALTHY")
        return 0
    else:
        print("\nOverall Status: UNHEALTHY")
        return 1

def handle_audit_tail(context, limit: int):
    """Tail the audit log."""
    print(f"--- USA Signal Bot Audit Trail (last {limit} events) ---")
    log_dir = Path(context.config.logging.log_dir)
    events = tail_audit_events(log_dir, n=limit)

    if not events:
        print("No audit events found.")
        return

    for ev in events:
        # Simple string representation for CLI
        ts = ev.get('timestamp_utc', 'N/A')
        sev = ev.get('severity', 'UNK')
        typ = ev.get('event_type', 'UNK')
        msg = ev.get('message', '')
        print(f"[{ts}] [{sev}] {typ}: {msg}")

def handle_log_info(context):
    """Display logging subsystem information."""
    print("--- USA Signal Bot Logging Info ---")
    print(f"Log Level: {context.config.logging.level}")
    print(f"Console Logging: {'Enabled' if context.config.logging.enable_console else 'Disabled'}")
    print(f"File Logging: {'Enabled' if context.config.logging.enable_file else 'Disabled'}")
    print(f"Log Directory: {context.config.logging.log_dir}")
    print(f"App Log File: {context.log_file_path}")
    print(f"Audit Log File: {context.audit_log_path}")


def handle_storage_info(context):
    """Displays storage subsystem info."""
    from usa_signal_bot.storage.formats import StorageFormat
    from usa_signal_bot.storage.paths import StorageArea, get_storage_area_path

    print("--- USA Signal Bot Storage Info ---")
    print(f"Data Root: {context.data_dir}")
    print("\nStorage Areas:")
    for area in StorageArea:
        path = get_storage_area_path(context.data_dir, area)
        print(f"  - {area.value}: {path}")

    print("\nSupported Formats:")
    for fmt in StorageFormat:
        if fmt == StorageFormat.PARQUET_RESERVED:
            print(f"  - {fmt.name}: Reserved for future use (currently unsupported)")
        else:
            print(f"  - {fmt.name}")

    print("\nStorage Config:")
    print(f"  - enabled: {context.config.storage.enabled}")
    print(f"  - atomic_writes: {context.config.storage.atomic_writes}")
    print(f"  - parquet_enabled: {context.config.storage.parquet_enabled}")

def handle_storage_check(context) -> int:
    """Runs storage specific health checks."""
    from usa_signal_bot.core.health import check_storage_health
    print("--- USA Signal Bot Storage Check ---")
    result = check_storage_health(context)
    status = "PASS" if result.passed else "FAIL"
    print(f"[{status}] {result.name}: {result.message}")
    if result.details:
        print(f"Details: {result.details}")

    return 0 if result.passed else 1

def handle_storage_list(context, area: str = None) -> int:
    """Lists files in the storage system."""
    from usa_signal_bot.storage.file_store import LocalFileStore
    from usa_signal_bot.storage.paths import StorageArea
    from usa_signal_bot.utils.file_utils import normalize_safe_filename

    print("--- USA Signal Bot Storage List ---")
    store = LocalFileStore(context.data_dir)

    try:
        if area:
            safe_area = normalize_safe_filename(area)
            files = store.list_files(safe_area)
            print(f"Files in area '{safe_area}': {len(files)}")
            for f in files:
                size = f.stat().st_size
                print(f"  - {f.name} ({size} bytes)")
        else:
            print("Summary of all areas:")
            for a in StorageArea:
                files = store.list_files(a.value)
                print(f"  - {a.value}: {len(files)} files")
        return 0
    except Exception as e:
        print(f"Error listing storage files: {e}")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="USA Signal Bot CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommands
    subparsers.add_parser("smoke", help="Run system smoke check")
    subparsers.add_parser("show-config", help="Display the active configuration")
    subparsers.add_parser("show-paths", help="Display application paths")
    subparsers.add_parser("validate-config", help="Validate the configuration")
    subparsers.add_parser("runtime-summary", help="Show a summary of the runtime environment")
    subparsers.add_parser("check-env", help="Check and mask environment variables")
    subparsers.add_parser("health", help="Run full system health check")

    subparsers.add_parser("log-info", help="Display information about logging configuration")

    # Storage commands
    subparsers.add_parser("storage-info", help="Display storage subsystem information")
    subparsers.add_parser("storage-check", help="Run storage health check")

    storage_list_parser = subparsers.add_parser("storage-list", help="List files in storage")
    storage_list_parser.add_argument("--area", type=str, help="Specific storage area to list")


    audit_parser = subparsers.add_parser("audit-tail", help="Tail the audit log")
    audit_parser.add_argument("--limit", type=int, default=20, help="Number of events to display")

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


    except Exception as e:
        sys.exit(handle_cli_exception(e))

    sys.exit(0)

if __name__ == "__main__":
    main()
