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
from usa_signal_bot.core.logging_config import setup_logging, get_logger, log_system_event
from usa_signal_bot.core.runtime_state import RuntimeContext
from usa_signal_bot.core.events import create_event
from usa_signal_bot.core.audit import write_audit_event, get_audit_log_path
from usa_signal_bot.core.health import run_health_checks, assert_health_ok, health_results_to_dict
from usa_signal_bot.core.exceptions import RuntimeInitializationError

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
    8. Create and log initialization events.
    9. Run health checks.

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
    log_dir_str = config.logging.log_dir
    setup_logging(
        level=log_level,
        log_dir=log_dir_str,
        log_file=log_file,
        enable_console=config.logging.enable_console,
        enable_file=config.logging.enable_file,
        max_bytes=config.logging.max_bytes,
        backup_count=config.logging.backup_count
    )

    logger = get_logger(__name__)

    # 6. Create RuntimeContext
    started_at = datetime.now(timezone.utc).isoformat()
    log_path_dir = Path(log_dir_str)

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
        execution_mode=config.runtime.mode,
        log_file_path=log_path_dir / log_file,
        audit_log_path=get_audit_log_path(log_path_dir)
    )

    # 7. Safe mode control
    try:
        context.assert_safe_mode()
    except Exception as e:
        # If safe mode fails, try to audit before crashing
        try:
            from usa_signal_bot.core.audit import audit_forbidden_operation
            audit_forbidden_operation("RuntimeInit", str(e), log_path_dir)
        except:
            pass
        raise e

    # 8. Create and log initialization events
    events_to_log = [
        create_event("RUNTIME_STARTED", "INFO", "Runtime initialization started.", "runtime", {"version": config.project.version}),
        create_event("CONFIG_VALIDATED", "INFO", "Configuration loaded and validated.", "runtime"),
        create_event("SAFE_MODE_CONFIRMED", "INFO", "Safe mode constraints verified.", "security", context.as_summary_dict().get("safe_mode", {})),
        create_event("LOGGING_READY", "INFO", "Logging subsystem ready.", "runtime")
    ]

    for event in events_to_log:
        log_system_event(event, logger)
        try:
            write_audit_event(event, log_path_dir)
        except Exception as e:
            # If we can't write to audit log during initialization, we fail fast for Phase 3
            raise RuntimeInitializationError(f"Failed to write audit event: {e}")

    # 9. Health check
    health_results = run_health_checks(context)
    try:
        assert_health_ok(health_results)
        context.health_status = "HEALTHY"
        health_event = create_event("HEALTH_CHECK_PASSED", "INFO", "Initial health check passed.", "runtime")
    except Exception as e:
        context.health_status = "UNHEALTHY"
        health_event = create_event("HEALTH_CHECK_FAILED", "ERROR", f"Health check failed: {e}", "runtime")
        log_system_event(health_event, logger)
        write_audit_event(health_event, log_path_dir)
        raise RuntimeInitializationError(str(e))

    log_system_event(health_event, logger)
    write_audit_event(health_event, log_path_dir)

    logger.info("Runtime initialized successfully.")

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

# Backward compatibility for Phase 1 CLI commands
def init_runtime() -> dict:
    context = initialize_runtime()
    from usa_signal_bot.core.config import config_to_dict
    return config_to_dict(context.config)
