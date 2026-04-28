"""Runtime initialization and bootstrapping."""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timezone

from usa_signal_bot.core.paths import (
    ensure_directories,
    PROJECT_ROOT,
    CONFIG_DIR,
    DATA_DIR,
    LOGS_DIR,
    REPORTS_DIR,
    CACHE_DIR,
    PAPER_DIR,
    BACKTESTS_DIR
)
from usa_signal_bot.core.config import load_app_config
from usa_signal_bot.core.logging_config import setup_logging
from usa_signal_bot.core.runtime_state import RuntimeContext

def initialize_runtime(config_dir: Optional[Path] = None) -> RuntimeContext:
    """
    Initializes the runtime environment:
    1. Resolve paths.
    2. Load config.
    3. Validate config.
    4. Ensure directories exist.
    5. Set up logging.
    6. Create RuntimeContext.
    7. Perform safe mode checks.
    8. Log startup checks.

    Returns:
        The validated RuntimeContext.
    """
    # 1-3. Load and validate config
    config = load_app_config(config_dir)

    # 4. Ensure directories
    ensure_directories()

    # 5. Set up logging
    log_level = config.logging.level
    log_file = config.logging.log_file
    setup_logging(level=log_level, log_file=log_file)

    logger = logging.getLogger(__name__)

    # 6. Create RuntimeContext
    started_at = datetime.now(timezone.utc).isoformat()
    context = RuntimeContext(
        config=config,
        project_root=PROJECT_ROOT,
        config_dir=config_dir or CONFIG_DIR,
        data_dir=DATA_DIR,
        logs_dir=LOGS_DIR,
        cache_dir=CACHE_DIR,
        reports_dir=REPORTS_DIR,
        paper_dir=PAPER_DIR,
        backtests_dir=BACKTESTS_DIR,
        started_at_utc=started_at,
        execution_mode=config.runtime.mode
    )

    # 7. Safe mode control
    context.assert_safe_mode()

    # 8. Log startup checks
    checks = run_startup_checks(context)
    for check in checks:
        logger.debug(f"Startup check: {check}")

    logger.info("Runtime initialized successfully in safe mode.")

    return context

def run_startup_checks(context: RuntimeContext) -> List[str]:
    """Runs a series of startup checks and returns their status messages."""
    checks = [
        "Config loaded and validated.",
        "Safe mode confirmed.",
        "Directories ready.",
        "Logging ready."
    ]

    if not context.config.runtime.broker_order_routing_enabled:
        checks.append("Broker routing disabled.")

    if not context.config.runtime.web_scraping_allowed:
        checks.append("Web scraping disabled.")

    if not context.config.runtime.dashboard_enabled:
        checks.append("Dashboard disabled.")

    return checks

def build_runtime_summary(context: RuntimeContext) -> dict:
    """Returns a summary of the runtime environment."""
    return context.as_summary_dict()

# Backward compatibility for Phase 1 CLI commands (if needed before CLI update)
def init_runtime() -> dict:
    context = initialize_runtime()
    from usa_signal_bot.core.config import config_to_dict
    return config_to_dict(context.config)
