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



def check_universe_health(context) -> HealthCheckResult:
    """Checks universe readiness."""
    from usa_signal_bot.universe.loader import load_default_watchlist
    from usa_signal_bot.core.exceptions import UniverseLoadError, UniverseValidationError

    universe_dir = context.data_dir / "universe"
    details = {}

    if not universe_dir.exists():
        return HealthCheckResult(
            name="Universe Check",
            passed=False,
            message="Universe directory missing.",
            details={"path": str(universe_dir)}
        )

    try:
        load_result = load_default_watchlist(context.data_dir, context.config.universe.default_watchlist_file)

        details["source"] = load_result.source_path
        details["total_rows"] = load_result.row_count
        details["valid_symbols"] = load_result.valid_count
        details["invalid_symbols"] = load_result.invalid_count
        details["duplicates"] = load_result.duplicate_count

        if load_result.invalid_count > 0:
            details["warnings"] = load_result.errors[:5]

        if load_result.valid_count == 0:
            return HealthCheckResult(
                name="Universe Check",
                passed=False,
                message="Watchlist contains no valid symbols.",
                details=details
            )

        return HealthCheckResult(
            name="Universe Check",
            passed=True,
            message=f"Universe healthy with {load_result.valid_count} valid symbols.",
            details=details
        )

    except (UniverseLoadError, UniverseValidationError) as e:
        return HealthCheckResult(
            name="Universe Check",
            passed=False,
            message=f"Failed to load universe: {e}"
        )
    except Exception as e:
        return HealthCheckResult(
            name="Universe Check",
            passed=False,
            message=f"Unexpected error checking universe: {e}"
        )



def check_universe_health(context) -> HealthCheckResult:
    """Checks universe readiness."""
    from usa_signal_bot.universe.loader import load_default_watchlist
    from usa_signal_bot.core.exceptions import UniverseLoadError, UniverseValidationError

    universe_dir = context.data_dir / "universe"
    details = {}

    if not universe_dir.exists():
        return HealthCheckResult(
            name="Universe Check",
            passed=False,
            message="Universe directory missing.",
            details={"path": str(universe_dir)}
        )

    try:
        load_result = load_default_watchlist(context.data_dir, context.config.universe.default_watchlist_file)

        details["source"] = load_result.source_path
        details["total_rows"] = load_result.row_count
        details["valid_symbols"] = load_result.valid_count
        details["invalid_symbols"] = load_result.invalid_count
        details["duplicates"] = load_result.duplicate_count

        if load_result.invalid_count > 0:
            details["warnings"] = load_result.errors[:5]

        if load_result.valid_count == 0:
            return HealthCheckResult(
                name="Universe Check",
                passed=False,
                message="Watchlist contains no valid symbols.",
                details=details
            )

        return HealthCheckResult(
            name="Universe Check",
            passed=True,
            message=f"Universe healthy with {load_result.valid_count} valid symbols.",
            details=details
        )

    except (UniverseLoadError, UniverseValidationError) as e:
        return HealthCheckResult(
            name="Universe Check",
            passed=False,
            message=f"Failed to load universe: {e}"
        )
    except Exception as e:
        return HealthCheckResult(
            name="Universe Check",
            passed=False,
            message=f"Unexpected error checking universe: {e}"
        )


def check_storage_health(context) -> HealthCheckResult:
    """Checks if the storage layer is healthy and accessible."""
    import uuid
    from usa_signal_bot.storage.paths import ensure_storage_areas
    from usa_signal_bot.utils.file_utils import atomic_write_text

    try:
        # Check data root
        if not context.data_dir.exists():
            return HealthCheckResult(name="Storage Check", passed=False, message="Data root directory missing")

        # Ensure all standard storage areas exist
        areas = ensure_storage_areas(context.data_dir)

        # Test writing and deleting a temp file in the root
        test_file = context.data_dir / f".health_{uuid.uuid4().hex}.tmp"
        atomic_write_text(test_file, "healthcheck")

        if not test_file.exists():
            return HealthCheckResult(name="Storage Check", passed=False, message="Failed to write test file")

        test_file.unlink()

        return HealthCheckResult(
            name="Storage Check",
            passed=True,
            message="Storage areas and write access OK",
            details={"areas_checked": list(areas.keys())}
        )
    except Exception as e:
        return HealthCheckResult(name="Storage Check", passed=False, message=f"Storage check failed: {e}")

def run_health_checks(context) -> List[HealthCheckResult]:
    """Runs all health checks and returns the results."""
    return [
        check_config_health(context),
        check_paths_health(context),
        check_logging_health(context),
        check_safe_mode_health(context),
        check_storage_health(context),
        check_universe_health(context),
        check_universe_health(context)
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
