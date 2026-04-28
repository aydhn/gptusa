"""Command Line Interface for USA Signal Bot."""

import argparse
import sys
import json
from pprint import pprint
import logging

from usa_signal_bot.app.runtime import initialize_runtime, run_startup_checks, build_runtime_summary
from usa_signal_bot.core import paths
from usa_signal_bot.core.config import config_to_dict
from usa_signal_bot.utils.dict_utils import redact_sensitive_keys
from usa_signal_bot.core.environment import get_env, mask_secret

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
    print(json.dumps(summary, indent=2))

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

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == "show-paths":
            # Paths check doesn't need full validation to avoid crashing if config is bad just to see paths
            paths.ensure_directories()
            handle_show_paths()
            return 0

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

    except Exception as e:
        print(f"Fatal Error: {e}", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
