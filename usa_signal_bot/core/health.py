"""System health check logic."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

from usa_signal_bot.core.exceptions import HealthCheckError
from usa_signal_bot.utils.file_utils import is_writable_dir

@dataclass
class HealthCheckResult:
    name: str
    passed: bool
    message: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    details: Dict[str, Any] = field(default_factory=dict)

def check_config_health(context) -> HealthCheckResult:
    """Checks if the configuration is loaded."""
    passed = context.config is not None
    msg = "Config loaded successfully" if passed else "Config is missing"
    return HealthCheckResult(name="Config Check", passed=passed, message=msg)

def check_paths_health(context) -> HealthCheckResult:
    """Checks if essential directories exist."""
    missing = []
    if not context.data_dir.exists(): missing.append("data_dir")
    if not context.logs_dir.exists(): missing.append("logs_dir")

    passed = len(missing) == 0
    msg = "All paths exist" if passed else f"Missing paths: {', '.join(missing)}"
    return HealthCheckResult(name="Path Check", passed=passed, message=msg)

def check_logging_health(context) -> HealthCheckResult:
    """Checks if the logging directory is writable."""
    passed = is_writable_dir(context.logs_dir)
    msg = "Logs directory is writable" if passed else "Logs directory is not writable"
    return HealthCheckResult(name="Logging Check", passed=passed, message=msg)

def check_safe_mode_health(context) -> HealthCheckResult:
    """Checks if safe mode restrictions are active."""
    issues = []
    if context.config.runtime.broker_order_routing_enabled:
        issues.append("Broker order routing is enabled")
    if context.config.runtime.web_scraping_allowed:
        issues.append("Web scraping is allowed")
    if context.config.runtime.dashboard_enabled:
        issues.append("Dashboard is enabled")
    if context.config.runtime.mode != "local_paper_only":
        issues.append(f"Invalid mode: {context.config.runtime.mode}")

    passed = len(issues) == 0
    msg = "Safe mode active" if passed else f"Safe mode violations: {', '.join(issues)}"
    return HealthCheckResult(name="Safe Mode Check", passed=passed, message=msg)

def run_health_checks(context) -> List[HealthCheckResult]:
    """Runs all health checks and returns the results."""
    return [
        check_config_health(context),
        check_paths_health(context),
        check_logging_health(context),
        check_safe_mode_health(context)
    ]

def health_results_to_dict(results: List[HealthCheckResult]) -> List[Dict]:
    """Converts a list of health check results to dictionaries."""
    return [
        {
            "name": r.name,
            "passed": r.passed,
            "message": r.message,
            "timestamp_utc": r.timestamp_utc,
            "details": r.details
        }
        for r in results
    ]

def assert_health_ok(results: List[HealthCheckResult]) -> None:
    """Asserts that all health checks passed, raising HealthCheckError if not."""
    failed = [r for r in results if not r.passed]
    if failed:
        msgs = [f"{r.name}: {r.message}" for r in failed]
        raise HealthCheckError(f"Health checks failed: {'; '.join(msgs)}")
