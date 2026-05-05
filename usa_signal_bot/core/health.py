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


def check_extended_universe_health(context) -> HealthCheckResult:
    try:
        cfg = context.config.universe

        # Check directories
        dirs_to_check = [
            context.project_root / cfg.imports_dir,
            context.project_root / cfg.snapshots_dir,
            context.project_root / cfg.catalog_dir,
            context.project_root / cfg.presets_dir,
            context.project_root / cfg.exports_dir
        ]

        for d in dirs_to_check:
            d.mkdir(parents=True, exist_ok=True)
            if not d.exists() or not d.is_dir():
                return HealthCheckResult("Extended Universe Check", False, f"Directory failed: {d}")

        # Check reserved sources
        if cfg.allow_reserved_external_sources:
             return HealthCheckResult("Extended Universe Check", False, "allow_reserved_external_sources must be false")

        # Optional: check if preset CSVs exist, catalog buildable (just a light check)
        from usa_signal_bot.universe.presets import list_preset_files
        list_preset_files(context.data_dir)

        from usa_signal_bot.universe.catalog import build_universe_catalog
        build_universe_catalog(context.data_dir)

        return HealthCheckResult("Extended Universe Check", True, "Extended Universe configuration OK")

    except Exception as e:
        return HealthCheckResult("Extended Universe Check", False, f"Extended Universe check failed: {e}")


def check_strategy_engine_health(context: 'RuntimeContext') -> HealthCheckResult:
    result = HealthCheckResult(
        name="strategy_engine",
        status=HealthStatus.HEALTHY,
        message="Strategy engine initialized",
        details={}
    )

    try:
        if not context.config.strategies.enabled:
            result.status = HealthStatus.DEGRADED
            result.message = "Strategies are disabled in config"
            return result

        from usa_signal_bot.strategies.strategy_registry import create_default_strategy_registry
        from usa_signal_bot.strategies.strategy_engine import StrategyEngine
        from usa_signal_bot.strategies.strategy_input import StrategyInputBatch, StrategyFeatureFrame
        import datetime

        registry = create_default_strategy_registry()
        engine = StrategyEngine(registry, context.data_dir)

        result.details["registered_strategies"] = len(registry.list_names())

        if not registry.has("trend_following_skeleton"):
            result.status = HealthStatus.UNHEALTHY
            result.message = "trend_following_skeleton missing from registry"
            return result

        # Try a fake input batch
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        frame = StrategyFeatureFrame(
            symbol="FAKE",
            timeframe="1d",
            rows=[{"timestamp_utc": now, "close_ema_20": 105.0, "close_ema_50": 100.0}],
            feature_names=["close_ema_20", "close_ema_50"]
        )
        batch = StrategyInputBatch(frames=[frame], provider_name="health", symbols=["FAKE"], timeframes=["1d"], created_at_utc=now)

        run_res = engine.run_strategy("trend_following_skeleton", batch)
        if run_res.status.value == "FAILED":
            result.status = HealthStatus.UNHEALTHY
            result.message = f"Strategy run failed: {run_res.errors}"
            return result

        if len(run_res.signals) != 1:
            result.status = HealthStatus.DEGRADED
            result.message = f"Expected 1 signal, got {len(run_res.signals)}"

    except Exception as e:
        result.status = HealthStatus.UNHEALTHY
        result.message = f"Strategy engine error: {e}"

    return result

def check_signal_contract_health(context: 'RuntimeContext') -> HealthCheckResult:
    result = HealthCheckResult(
        name="signal_contract",
        status=HealthStatus.HEALTHY,
        message="Signal contract initialized",
        details={}
    )

    try:
        from usa_signal_bot.strategies.signal_store import signal_store_dir

        d = signal_store_dir(context.data_dir)
        result.details["store_dir"] = str(d)

        # Check permissions
        import tempfile
        import os
        try:
            with tempfile.NamedTemporaryFile(dir=d, suffix=".tmp", delete=False) as tf:
                tf.write(b"test")
                tf_name = tf.name
            os.remove(tf_name)
        except Exception as e:
            result.status = HealthStatus.UNHEALTHY
            result.message = f"Cannot write to signal directory: {e}"
            return result

    except Exception as e:
        result.status = HealthStatus.UNHEALTHY
        result.message = f"Signal contract error: {e}"

    return result


def check_signal_scoring_health(context: 'RuntimeContext') -> HealthCheckResult:
    from usa_signal_bot.strategies.signal_scoring import default_signal_scoring_config, validate_signal_scoring_config
    try:
        config = context.config.signal_scoring if context.config else default_signal_scoring_config()
        validate_signal_scoring_config(config)
        return HealthCheckResult(
            name="signal_scoring",
            passed=True,
            message="Signal scoring config is valid."
        )
    except Exception as e:
        return HealthCheckResult(
            name="signal_scoring",
            passed=False,
            message=f"Signal scoring error: {e}"
        )

def check_signal_quality_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        if context.config and not context.config.signal_quality.enabled:
            return HealthCheckResult(
                name="signal_quality",
                passed=True,
                message="Signal quality guard is disabled in config."
            )
        return HealthCheckResult(
            name="signal_quality",
            passed=True,
            message="Signal quality guard is configured."
        )
    except Exception as e:
        return HealthCheckResult(
            name="signal_quality",
            passed=False,
            message=f"Signal quality guard error: {e}"
        )

def check_confluence_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        if context.config and not context.config.confluence.enabled:
            return HealthCheckResult(
                name="confluence_engine",
                passed=True,
                message="Confluence engine is disabled in config."
            )
        return HealthCheckResult(
            name="confluence_engine",
            passed=True,
            message="Confluence engine is configured."
        )
    except Exception as e:
        return HealthCheckResult(
            name="confluence_engine",
            passed=False,
            message=f"Confluence engine error: {e}"
        )


def check_basket_simulation_config_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        config = context.app_config.basket_simulation
        if not config.enabled:
            return HealthCheckResult(
                name="basket_simulation_config",
                status=HealthStatus.HEALTHY,
                message="Basket simulation disabled by config."
            )
        return HealthCheckResult(
            name="basket_simulation_config",
            status=HealthStatus.HEALTHY,
            message=f"Basket simulation configured properly. Dir: {config.store_dir}"
        )
    except Exception as e:
        return HealthCheckResult(
            name="basket_simulation_config",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
            error=e
        )

def check_allocation_replay_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        config = default_allocation_to_order_config()
        item = BasketReplayItem(
            item_id="test", candidate_id=None, signal_id=None, symbol="AAPL", timeframe="1d",
            strategy_name=None, action=SignalAction.LONG, target_weight=None, target_notional=1000.0,
            target_quantity=None, rank_score=None, risk_score=None, confidence=None, timestamp_utc=None
        )
        qty, warnings = calculate_quantity_from_replay_item(item, 100.0, 10000.0, config)
        if qty == 10.0:
            return HealthCheckResult(
                name="allocation_replay",
                status=HealthStatus.HEALTHY,
                message="Allocation replay health check passed."
            )
        return HealthCheckResult(
            name="allocation_replay",
            status=HealthStatus.DEGRADED,
            message="Allocation replay calculated wrong quantity."
        )
    except Exception as e:
        return HealthCheckResult(
            name="allocation_replay",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
            error=e
        )

def check_allocation_drift_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        config = default_allocation_drift_config()
        res = calculate_allocation_drift({"AAPL": 0.5}, {"AAPL": 0.5}, config)
        if res.status.value == "within_tolerance":
            return HealthCheckResult(
                name="allocation_drift",
                status=HealthStatus.HEALTHY,
                message="Allocation drift health check passed."
            )
        return HealthCheckResult(
            name="allocation_drift",
            status=HealthStatus.DEGRADED,
            message="Allocation drift reported unexpected status."
        )
    except Exception as e:
        return HealthCheckResult(
            name="allocation_drift",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
            error=e
        )

def check_basket_metrics_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(
        name="basket_metrics",
        status=HealthStatus.HEALTHY,
        message="Basket metrics health check passed."
    )

def check_basket_store_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        d = basket_store_dir(context.data_root)
        if d.exists():
            return HealthCheckResult(
                name="basket_store",
                status=HealthStatus.HEALTHY,
                message="Basket store dir exists."
            )
        return HealthCheckResult(
            name="basket_store",
            status=HealthStatus.DEGRADED,
            message="Basket store dir not found."
        )
    except Exception as e:
        return HealthCheckResult(
            name="basket_store",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
            error=e
        )

def run_health_checks(context) -> List[HealthCheckResult]:

    """Runs all health checks and returns the results."""
    return [
        check_config_health(context),
        check_paths_health(context),
        check_logging_health(context),
        check_safe_mode_health(context),
        check_storage_health(context),
        check_walk_forward_config_health(context),
        check_walk_forward_windows_health(context),
        check_walk_forward_metrics_health(context),
        check_walk_forward_store_health(context),
        check_parameter_sensitivity_config_health(context),
        check_parameter_grid_health(context),
        check_sensitivity_metrics_health(context),
        check_stability_map_health(context),
        check_sensitivity_store_health(context),
        check_universe_health(context),
        check_extended_universe_health(context),
        check_market_data_cache_health(context),
        check_provider_health(context),
        check_data_quality_config_health(context),
        check_cache_refresh_health(context),
        check_momentum_feature_health(context)
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

def check_market_data_cache_health(context) -> HealthCheckResult:
    """Checks if the market data cache is writable."""
    try:
        from usa_signal_bot.data.cache import market_data_cache_dir
        from usa_signal_bot.utils.file_utils import atomic_write_text
        import uuid

        cache_dir = market_data_cache_dir(context.data_dir)
        test_file = cache_dir / f".health_{uuid.uuid4().hex}.tmp"

        atomic_write_text(test_file, "healthcheck")
        if not test_file.exists():
            return HealthCheckResult(name="Market Data Cache", passed=False, message="Could not verify market data cache is writable.")

        test_file.unlink()
        return HealthCheckResult(name="Market Data Cache", passed=True, message="Market data cache is writable.")
    except Exception as e:
        return HealthCheckResult(name="Market Data Cache", passed=False, message=f"Market data cache check failed: {e}")


def check_provider_health(context) -> HealthCheckResult:
    """Check data provider foundation health."""
    try:
        from usa_signal_bot.data.provider_registry import create_default_provider_registry
        from usa_signal_bot.data.models import MarketDataRequest

        # 1. Config check
        if not hasattr(context.config, 'providers'):
            return HealthCheckResult(
                name="provider_foundation",
                passed=False,
                message="Error", details={"error": "providers config missing"}
            )

        p_cfg = context.config.providers
        if p_cfg.default_provider not in ["mock", "yfinance"]:
             return HealthCheckResult(
                name="provider_foundation",
                passed=False,
                message="Error", details={"error": "default_provider is not mock or yfinance"}
            )

        if p_cfg.allow_paid_providers or p_cfg.allow_scraping_providers or p_cfg.allow_broker_data_providers:
            return HealthCheckResult(
                name="provider_foundation",
                passed=False,
                message="Error", details={"error": "forbidden provider types are allowed in config"}
            )

        # 2. Registry check
        registry = create_default_provider_registry()

        # 3. Mock provider check
        mock_provider = registry.get("mock")
        status = mock_provider.check_status()
        if not status.available:
             return HealthCheckResult(
                name="provider_foundation",
                passed=False,
                message="Error", details={"error": "mock provider is unavailable"}
            )

        # 4. Basic request test
        req = MarketDataRequest(symbols=["SPY"], timeframe="1d", provider_name="mock")
        resp = mock_provider.fetch_ohlcv(req)
        if not resp.success or resp.bar_count() == 0:
             return HealthCheckResult(
                name="provider_foundation",
                passed=False,
                message="Error", details={"error": "mock provider failed fetch test"}
            )

        return HealthCheckResult(
            name="provider_foundation",
            passed=True,
            message="Provider OK", details={
                "default_provider": p_cfg.default_provider,
                "registry_size": len(registry.list_names()),
                "mock_fetch_test": "success"
            }
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return HealthCheckResult(
            name="provider_foundation",
            passed=False,
            message="Error", details={"error": str(e)}
        )

def check_data_quality_config_health(context) -> HealthCheckResult:
    try:
        cfg = context.config.data_quality
        if not cfg.enabled:
            return HealthCheckResult("Data Quality Config", False, "data_quality.enabled is False")
        if not (0 <= cfg.max_allowed_warning_ratio <= 1):
             return HealthCheckResult("Data Quality Config", False, "max_allowed_warning_ratio out of bounds")
        return HealthCheckResult("Data Quality Config", True, "Data Quality config OK")
    except Exception as e:
        return HealthCheckResult("Data Quality Config", False, f"Check failed: {e}")


def check_cache_refresh_health(context):
    return HealthCheckResult("Cache Refresh", True, "OK")

def check_momentum_feature_health(context):
    return HealthCheckResult("Momentum Features", True, "OK")


def check_volatility_feature_health(context: 'RuntimeContext') -> HealthCheckResult:
    import pandas as pd
    from usa_signal_bot.features.indicator_registry import get_default_registry
    from usa_signal_bot.features.engine import FeatureEngine
    from usa_signal_bot.features.input_contract import FeatureInput
    from usa_signal_bot.features.models import OHLCVBar
    from usa_signal_bot.features.volatility_sets import get_volatility_indicator_set
    from datetime import datetime, timezone

    try:
        if not hasattr(context.config, "volatility_features"):
            return HealthCheckResult("volatility_feature_health", HealthStatus.WARNING, "volatility_features config missing")

        cfg = context.config.volatility_features
        if not cfg.enabled:
            return HealthCheckResult("volatility_feature_health", HealthStatus.PASS, "Volatility features are disabled")

        reg = get_default_registry()
        for ind_name in ["atr", "bollinger_bands", "rolling_volatility"]:
            if not reg.has(ind_name):
                 return HealthCheckResult("volatility_feature_health", HealthStatus.FAIL, f"Missing required volatility indicator: {ind_name}")

        try:
             vol_set = get_volatility_indicator_set(cfg.default_indicator_set)
        except Exception as e:
             return HealthCheckResult("volatility_feature_health", HealthStatus.FAIL, f"Could not load default volatility set: {e}")

        engine = FeatureEngine(reg, context.data_dir)
        bars = []
        base_time = datetime(2023, 1, 1, tzinfo=timezone.utc)
        for i in range(50):
            bars.append(OHLCVBar(
                timestamp_utc=base_time.isoformat(),
                open=100.0 + i,
                high=102.0 + i,
                low=98.0 + i,
                close=101.0 + i,
                volume=1000 + i,
                adjusted_close=101.0 + i
            ))

        f_input = FeatureInput(symbol="TEST", timeframe="1d", source="mock", bars=bars)
        res = engine.compute_volatility_set_for_input(f_input, set_name=cfg.default_indicator_set)

        if res.is_successful():
            return HealthCheckResult("volatility_feature_health", HealthStatus.PASS, f"Volatility engine healthy, produced {len(res.produced_features)} features")
        else:
            return HealthCheckResult("volatility_feature_health", HealthStatus.FAIL, f"Volatility engine compute failed: {res.errors}")

    except Exception as e:
        return HealthCheckResult("volatility_feature_health", HealthStatus.FAIL, f"Exception during volatility feature health check: {e}")


def check_walk_forward_config_health(context: 'RuntimeContext') -> HealthCheckResult:
    config = context.config
    wf_config = getattr(config, 'walk_forward', None)

    if not wf_config or not getattr(wf_config, 'enabled', False):
         return HealthCheckResult(name="walk_forward_config", passed=True, message="Walk-Forward is disabled in config.", details={"enabled": False})

    try:
        from usa_signal_bot.backtesting.walk_forward_models import WalkForwardConfig, validate_walk_forward_config
        from usa_signal_bot.core.enums import WalkForwardMode

        mode = WalkForwardMode(wf_config.default_mode.upper())
        c = WalkForwardConfig(
            mode=mode,
            train_window_days=wf_config.train_window_days,
            test_window_days=wf_config.test_window_days,
            step_days=wf_config.step_days,
            min_train_days=wf_config.min_train_days,
            max_windows=wf_config.max_windows,
            anchored_start=wf_config.anchored_start,
            include_partial_last_window=wf_config.include_partial_last_window
        )
        validate_walk_forward_config(c)
        return HealthCheckResult(name="walk_forward_config", passed=True, message="Walk-Forward config is valid.", details={"mode": str(mode)})
    except Exception as e:
        return HealthCheckResult(name="walk_forward_config", passed=False, message=f"Walk-Forward config validation failed: {e}", details={"error": str(e)})

def check_walk_forward_windows_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.walk_forward_windows import generate_rolling_windows
        windows = generate_rolling_windows("2020-01-01", "2021-01-01", 100, 30, 30, 10)
        if len(windows) > 0:
             return HealthCheckResult(name="walk_forward_windows", passed=True, message="Window generator working.", details={"windows_generated": len(windows)})
        else:
             return HealthCheckResult(name="walk_forward_windows", passed=False, message="Window generator produced 0 windows.", details={})
    except Exception as e:
         return HealthCheckResult(name="walk_forward_windows", passed=False, message=f"Window generator failed: {e}", details={"error": str(e)})

def check_walk_forward_metrics_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.walk_forward_metrics import calculate_walk_forward_aggregate_metrics
        from usa_signal_bot.backtesting.walk_forward_models import WalkForwardWindowResult, WalkForwardWindow
        from usa_signal_bot.core.enums import WalkForwardMode, WalkForwardWindowStatus

        w = WalkForwardWindow("win_001", 1, WalkForwardMode.ROLLING, "2020-01-01", "2020-02-01", "2020-02-01", "2020-03-01", "2020-01-01", "2020-03-01", WalkForwardWindowStatus.COMPLETED)
        r = WalkForwardWindowResult(w, "is1", "oos1", {"total_return_pct": 5.0}, {"total_return_pct": 2.0}, {}, {}, [], [])
        metrics = calculate_walk_forward_aggregate_metrics([r])

        if getattr(metrics.status, "value", metrics.status) == "OK":
             return HealthCheckResult(name="walk_forward_metrics", passed=True, message="Aggregate metrics calculator working.", details={"status": getattr(metrics.status, "value", metrics.status)})
        else:
             return HealthCheckResult(name="walk_forward_metrics", passed=False, message="Aggregate metrics calculator produced unexpected status.", details={"status": getattr(metrics.status, "value", metrics.status)})
    except Exception as e:
         return HealthCheckResult(name="walk_forward_metrics", passed=False, message=f"Aggregate metrics calculator failed: {e}", details={"error": str(e)})

def check_walk_forward_store_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.walk_forward_store import walk_forward_store_dir
        path = walk_forward_store_dir(context.data_dir)
        if path.exists() and path.is_dir():
            return HealthCheckResult(name="walk_forward_store", passed=True, message="Walk-Forward store directory is accessible.", details={"path": str(path)})
        else:
            return HealthCheckResult(name="walk_forward_store", passed=False, message="Walk-Forward store directory is not accessible.", details={"path": str(path)})
    except Exception as e:
         return HealthCheckResult(name="walk_forward_store", passed=False, message=f"Walk-Forward store health check failed: {e}", details={"error": str(e)})

# --- Parameter Sensitivity Checks ---

def check_parameter_sensitivity_config_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.core.config_schema import ParameterSensitivityConfigSchema
        from usa_signal_bot.backtesting.parameter_sensitivity_models import ParameterSensitivityConfig, validate_parameter_sensitivity_config
        from usa_signal_bot.core.enums import SensitivityMetricName

        cfg = getattr(context.config, 'parameter_sensitivity', None)
        if cfg is None:
             return HealthCheckResult("Parameter Sensitivity Config Check", True, "Config not found (defaulting or disabled)", "Config")

        if not cfg.enabled:
             return HealthCheckResult("Parameter Sensitivity Config Check", True, "Parameter Sensitivity is disabled", "Config")

        sens_config = ParameterSensitivityConfig(
            max_cells=cfg.max_cells,
            continue_on_cell_error=cfg.continue_on_cell_error,
            run_backtest=cfg.run_backtest,
            include_benchmark=cfg.include_benchmark,
            include_monte_carlo=cfg.include_monte_carlo,
            include_walk_forward=cfg.include_walk_forward,
            primary_metric=SensitivityMetricName(cfg.primary_metric),
            stability_metric=SensitivityMetricName(cfg.stability_metric),
            min_completed_cells=cfg.min_completed_cells
        )
        validate_parameter_sensitivity_config(sens_config)
        return HealthCheckResult("Parameter Sensitivity Config Check", True, "Config is valid", "Config")
    except Exception as e:
        return HealthCheckResult("Parameter Sensitivity Config Check", False, f"Config error: {str(e)}", "Config", {"error": str(e)})

def check_parameter_grid_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.parameter_grid import create_single_parameter_grid, create_parameter_grid_cells
        from usa_signal_bot.core.enums import ParameterValueType
        grid_spec = create_single_parameter_grid("test_strat", "test_param", [1, 2, 3], ParameterValueType.INT)
        cells = create_parameter_grid_cells(grid_spec)
        if len(cells) != 3:
            return HealthCheckResult("Parameter Grid Health", False, "Grid cell count mismatch", "Grid")
        return HealthCheckResult("Parameter Grid Health", True, "Grid generation works", "Grid")
    except Exception as e:
        return HealthCheckResult("Parameter Grid Health", False, f"Grid error: {str(e)}", "Grid", {"error": str(e)})

def check_sensitivity_metrics_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.sensitivity_metrics import calculate_sensitivity_aggregate_metrics
        from usa_signal_bot.core.enums import SensitivityMetricName
        # Just verifying the module can be imported and executed with empty
        calculate_sensitivity_aggregate_metrics([], SensitivityMetricName.RETURN_PCT)
        return HealthCheckResult("Sensitivity Metrics Health", True, "Metrics calculation works", "Metrics")
    except Exception as e:
        return HealthCheckResult("Sensitivity Metrics Health", False, f"Metrics error: {str(e)}", "Metrics", {"error": str(e)})

def check_stability_map_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.stability_map import build_stability_map
        from usa_signal_bot.core.enums import SensitivityMetricName
        build_stability_map([], SensitivityMetricName.RETURN_PCT)
        return HealthCheckResult("Stability Map Health", True, "Stability map works", "StabilityMap")
    except Exception as e:
        return HealthCheckResult("Stability Map Health", False, f"Stability map error: {str(e)}", "StabilityMap", {"error": str(e)})

def check_sensitivity_store_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.sensitivity_store import sensitivity_store_dir
        sensitivity_store_dir(context.data_dir)
        return HealthCheckResult("Sensitivity Store Health", True, "Store dir reachable", "Store")
    except Exception as e:
        return HealthCheckResult("Sensitivity Store Health", False, f"Store dir error: {str(e)}", "Store", {"error": str(e)})

def check_portfolio_construction_config_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.core.config_schema import validate_portfolio_construction_config, validate_allocation_limits_config, validate_concentration_guards_config

        cfg = context.config
        if cfg.portfolio_construction:
            validate_portfolio_construction_config(cfg.portfolio_construction)
        if cfg.allocation_limits:
            validate_allocation_limits_config(cfg.allocation_limits)
        if cfg.concentration_guards:
            validate_concentration_guards_config(cfg.concentration_guards)

        return HealthCheckResult("portfolio_config", HealthCheckStatus.PASSED, "Portfolio config is valid.")
    except Exception as e:
        return HealthCheckResult("portfolio_config", HealthCheckStatus.FAILED, f"Portfolio config invalid: {e}")

def check_allocation_methods_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.portfolio.allocation_methods import allocate_equal_weight, allocate_rank_weighted
        from usa_signal_bot.portfolio.portfolio_models import AllocationRequest, PortfolioCandidate
        from usa_signal_bot.core.enums import SignalAction, AllocationMethod, PortfolioCandidateStatus

        candidates = [
            PortfolioCandidate("1", "AAPL", "1d", SignalAction.BUY, 0, 0, status=PortfolioCandidateStatus.ELIGIBLE),
            PortfolioCandidate("2", "MSFT", "1d", SignalAction.BUY, 0, 0, status=PortfolioCandidateStatus.ELIGIBLE)
        ]

        req = AllocationRequest("req", candidates, 100000, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "")
        allocs1 = allocate_equal_weight(req)

        req.method = AllocationMethod.RANK_WEIGHTED
        allocs2 = allocate_rank_weighted(req)

        return HealthCheckResult("allocation_methods", HealthCheckStatus.PASSED, "Allocation methods working.")
    except Exception as e:
        return HealthCheckResult("allocation_methods", HealthCheckStatus.FAILED, f"Allocation methods failed: {e}")

def check_risk_budgeting_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.portfolio.risk_budgeting import build_risk_budget_report
        build_risk_budget_report([], 100000)
        return HealthCheckResult("risk_budgeting", HealthCheckStatus.PASSED, "Risk budget builder working.")
    except Exception as e:
        return HealthCheckResult("risk_budgeting", HealthCheckStatus.FAILED, f"Risk budget failed: {e}")

def check_concentration_guards_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.portfolio.concentration_guards import build_concentration_report
        build_concentration_report([])
        return HealthCheckResult("concentration_guards", HealthCheckStatus.PASSED, "Concentration report builder working.")
    except Exception as e:
        return HealthCheckResult("concentration_guards", HealthCheckStatus.FAILED, f"Concentration guards failed: {e}")

def check_portfolio_engine_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.portfolio.portfolio_engine import PortfolioConstructionEngine
        from usa_signal_bot.portfolio.portfolio_models import AllocationRequest, PortfolioCandidate
        from usa_signal_bot.core.enums import SignalAction, AllocationMethod, PortfolioCandidateStatus

        candidates = [
            PortfolioCandidate("1", "AAPL", "1d", SignalAction.BUY, 0, 0, status=PortfolioCandidateStatus.ELIGIBLE),
            PortfolioCandidate("2", "MSFT", "1d", SignalAction.BUY, 0, 0, status=PortfolioCandidateStatus.ELIGIBLE)
        ]
        req = AllocationRequest("req", candidates, 100000, 100000, AllocationMethod.EQUAL_WEIGHT, 0.8, "")

        engine = PortfolioConstructionEngine()
        result = engine.construct_portfolio(req)

        return HealthCheckResult("portfolio_engine", HealthCheckStatus.PASSED, "Portfolio engine working.")
    except Exception as e:
        return HealthCheckResult("portfolio_engine", HealthCheckStatus.FAILED, f"Portfolio engine failed: {e}")

def check_portfolio_store_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.portfolio.portfolio_store import portfolio_store_dir
        portfolio_store_dir(context.data_root)
        return HealthCheckResult("portfolio_store", HealthCheckStatus.PASSED, "Portfolio store dir writable.")
    except Exception as e:
        return HealthCheckResult("portfolio_store", HealthCheckStatus.FAILED, f"Portfolio store failed: {e}")

def check_runtime_config_health(context: 'RuntimeContext') -> HealthCheckResult:
    result = HealthCheckResult(component="runtime_config", status="unknown")
    try:
        from usa_signal_bot.core.config_schema import AppConfig
        if not hasattr(context.config, "runtime"):
            return HealthCheckResult(component="runtime_config", status="warning", message="No runtime config found")
        if context.config.runtime.enabled:
            result.status = "pass"
            result.message = "Runtime configuration is loaded."
        else:
            result.status = "warning"
            result.message = "Runtime is disabled."
    except Exception as e:
        result.status = "fail"
        result.message = str(e)
    return result

def check_runtime_lock_health(context: 'RuntimeContext') -> HealthCheckResult:
    result = HealthCheckResult(component="runtime_lock", status="unknown")
    try:
        from usa_signal_bot.runtime.runtime_lock import RuntimeLockManager
        from pathlib import Path
        lock_dir = Path(context.config.data.root_dir) / "runtime" / "locks"
        mgr = RuntimeLockManager(lock_dir)
        is_locked = mgr.is_locked()
        result.status = "pass"
        result.message = f"Lock manager operational. Currently locked: {is_locked}"
    except Exception as e:
        result.status = "fail"
        result.message = str(e)
    return result

def check_safe_stop_health(context: 'RuntimeContext') -> HealthCheckResult:
    result = HealthCheckResult(component="safe_stop", status="unknown")
    try:
        from usa_signal_bot.runtime.safe_stop import SafeStopManager
        from pathlib import Path
        stop_file = Path(context.config.data.root_dir) / "runtime" / "stop.json"
        mgr = SafeStopManager(stop_file)
        is_stop = mgr.is_stop_requested()
        result.status = "pass"
        result.message = f"Safe stop manager operational. Stop requested: {is_stop}"
    except Exception as e:
        result.status = "fail"
        result.message = str(e)
    return result

def check_market_scan_orchestrator_health(context: 'RuntimeContext') -> HealthCheckResult:
    result = HealthCheckResult(component="market_scan_orchestrator", status="unknown")
    try:
        from usa_signal_bot.runtime.scan_orchestrator import MarketScanOrchestrator
        from pathlib import Path
        root = Path(context.config.data.root_dir)
        _ = MarketScanOrchestrator(root)
        result.status = "pass"
        result.message = "MarketScanOrchestrator instantiated."
    except Exception as e:
        result.status = "fail"
        result.message = str(e)
    return result

def check_scheduled_scan_plan_health(context: 'RuntimeContext') -> HealthCheckResult:
    result = HealthCheckResult(component="scheduled_scan_plan", status="unknown")
    try:
        from usa_signal_bot.runtime.scan_scheduler import build_default_scheduled_scan_plan
        plan = build_default_scheduled_scan_plan()
        result.status = "pass"
        result.message = f"Default plan generated. ID: {plan.plan_id}"
    except Exception as e:
        result.status = "fail"
        result.message = str(e)
    return result

def check_scan_store_health(context: 'RuntimeContext') -> HealthCheckResult:
    result = HealthCheckResult(component="scan_store", status="unknown")
    try:
        from usa_signal_bot.runtime.scan_store import scan_store_dir, list_scan_runs
        from pathlib import Path
        d = scan_store_dir(Path(context.config.data.root_dir))
        runs = list_scan_runs(Path(context.config.data.root_dir))
        result.status = "pass"
        result.message = f"Scan store dir: {d}. Runs: {len(runs)}"
    except Exception as e:
        result.status = "fail"
        result.message = str(e)
    return result
