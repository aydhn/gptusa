with open("usa_signal_bot/core/health.py", "r") as f:
    content = f.read()

correct_funcs = """
def check_walk_forward_config_health(context: 'RuntimeContext') -> HealthCheckResult:
    config = context.app_config
    wf_config = getattr(config, 'walk_forward', None)

    if not wf_config or not getattr(wf_config, 'enabled', False):
         return HealthCheckResult(component="walk_forward_config", status=HealthStatus.PASS, message="Walk-Forward is disabled in config.", details={"enabled": False})

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
        return HealthCheckResult(component="walk_forward_config", status=HealthStatus.PASS, message="Walk-Forward config is valid.", details={"mode": str(mode)})
    except Exception as e:
        return HealthCheckResult(component="walk_forward_config", status=HealthStatus.FAIL, message=f"Walk-Forward config validation failed: {e}", details={"error": str(e)})

def check_walk_forward_windows_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.walk_forward_windows import generate_rolling_windows
        windows = generate_rolling_windows("2020-01-01", "2021-01-01", 100, 30, 30, 10)
        if len(windows) > 0:
             return HealthCheckResult(component="walk_forward_windows", status=HealthStatus.PASS, message="Window generator working.", details={"windows_generated": len(windows)})
        else:
             return HealthCheckResult(component="walk_forward_windows", status=HealthStatus.FAIL, message="Window generator produced 0 windows.", details={})
    except Exception as e:
         return HealthCheckResult(component="walk_forward_windows", status=HealthStatus.FAIL, message=f"Window generator failed: {e}", details={"error": str(e)})

def check_walk_forward_metrics_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.walk_forward_metrics import calculate_walk_forward_aggregate_metrics
        from usa_signal_bot.backtesting.walk_forward_models import WalkForwardWindowResult, WalkForwardWindow
        from usa_signal_bot.core.enums import WalkForwardMode, WalkForwardWindowStatus

        w = WalkForwardWindow("win_001", 1, WalkForwardMode.ROLLING, "2020-01-01", "2020-02-01", "2020-02-01", "2020-03-01", "2020-01-01", "2020-03-01", WalkForwardWindowStatus.COMPLETED)
        r = WalkForwardWindowResult(w, "is1", "oos1", {"total_return_pct": 5.0}, {"total_return_pct": 2.0}, {}, {}, [], [])
        metrics = calculate_walk_forward_aggregate_metrics([r])

        if getattr(metrics.status, "value", metrics.status) == "OK":
             return HealthCheckResult(component="walk_forward_metrics", status=HealthStatus.PASS, message="Aggregate metrics calculator working.", details={"status": getattr(metrics.status, "value", metrics.status)})
        else:
             return HealthCheckResult(component="walk_forward_metrics", status=HealthStatus.FAIL, message="Aggregate metrics calculator produced unexpected status.", details={"status": getattr(metrics.status, "value", metrics.status)})
    except Exception as e:
         return HealthCheckResult(component="walk_forward_metrics", status=HealthStatus.FAIL, message=f"Aggregate metrics calculator failed: {e}", details={"error": str(e)})

def check_walk_forward_store_health(context: 'RuntimeContext') -> HealthCheckResult:
    try:
        from usa_signal_bot.backtesting.walk_forward_store import walk_forward_store_dir
        path = walk_forward_store_dir(context.data_dir)
        if path.exists() and path.is_dir():
            return HealthCheckResult(component="walk_forward_store", status=HealthStatus.PASS, message="Walk-Forward store directory is accessible.", details={"path": str(path)})
        else:
            return HealthCheckResult(component="walk_forward_store", status=HealthStatus.FAIL, message="Walk-Forward store directory is not accessible.", details={"path": str(path)})
    except Exception as e:
         return HealthCheckResult(component="walk_forward_store", status=HealthStatus.FAIL, message=f"Walk-Forward store health check failed: {e}", details={"error": str(e)})
"""

content = content.replace("check_storage_health(context),", "check_storage_health(context),\n        check_walk_forward_config_health(context),\n        check_walk_forward_windows_health(context),\n        check_walk_forward_metrics_health(context),\n        check_walk_forward_store_health(context),")

with open("usa_signal_bot/core/health.py", "w") as f:
    f.write(content.strip() + "\n\n" + correct_funcs)
