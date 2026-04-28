"""Command Line Interface for USA Signal Bot."""

import argparse
import sys
import json
from pprint import pprint

from usa_signal_bot.app.runtime import init_runtime
from usa_signal_bot.core import paths

def handle_smoke(config):
    """Run smoke checks to ensure basic components load correctly."""
    print("USA Signal Bot smoke check")
    print(f"Project: {config.get('project', {}).get('name')}")
    print(f"Mode: {config.get('runtime', {}).get('mode')}")
    print(f"Broker routing enabled: {config.get('runtime', {}).get('broker_order_routing_enabled')}")
    print(f"Web scraping allowed: {config.get('runtime', {}).get('web_scraping_allowed')}")
    print(f"Dashboard enabled: {config.get('runtime', {}).get('dashboard_enabled')}")
    print("Config loaded: OK")
    print("Directories checked: OK")
    print("Logging checked: OK")
    print("Status: OK")

def handle_show_config(config):
    """Display the loaded configuration."""
    print("--- USA Signal Bot Configuration ---")
    print(json.dumps(config, indent=2))

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

def main() -> int:
    parser = argparse.ArgumentParser(description="USA Signal Bot CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommands
    subparsers.add_parser("smoke", help="Run system smoke check")
    subparsers.add_parser("show-config", help="Display the active configuration")
    subparsers.add_parser("show-paths", help="Display application paths")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        # For 'show-paths', we don't necessarily need the full config, but we init to ensure dirs exist
        if args.command == "show-paths":
            init_runtime()
            handle_show_paths()
            return 0

        # Commands that require fully loaded config
        config = init_runtime()

        if args.command == "smoke":
            handle_smoke(config)
        elif args.command == "show-config":
            handle_show_config(config)

    except Exception as e:
        print(f"Fatal Error: {e}", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
