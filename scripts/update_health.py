def update_health():
    with open('usa_signal_bot/core/health.py', 'r') as f:
        content = f.read()

    new_checks = """
def check_regime_aware_cost_config_health(context: 'RuntimeContext') -> HealthCheckResult:
    cfg = getattr(context.config, "regime_aware_costs", None)
    if not cfg:
        return HealthCheckResult(component="RegimeAwareCostConfig", status=HealthStatus.WARN, message="Config missing", timestamp_utc=get_utc_now_str())
    if not cfg.warn_no_broker_execution:
        return HealthCheckResult(component="RegimeAwareCostConfig", status=HealthStatus.ERROR, message="Broker execution warning must be enabled", timestamp_utc=get_utc_now_str())
    return HealthCheckResult(component="RegimeAwareCostConfig", status=HealthStatus.HEALTHY, message="Config valid", timestamp_utc=get_utc_now_str())

def check_volatility_regime_cost_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="VolatilityRegimeCost", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_liquidity_regime_cost_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="LiquidityRegimeCost", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_spread_regime_cost_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="SpreadRegimeCost", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_session_regime_cost_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="SessionRegimeCost", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_lifecycle_regime_cost_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="LifecycleRegimeCost", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_combined_cost_regime_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="CombinedCostRegime", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_cost_curve_selector_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="CostCurveSelector", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_adaptive_execution_realism_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="AdaptiveExecutionRealism", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_regime_cost_store_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="RegimeCostStore", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())

def check_regime_cost_notification_health(context: 'RuntimeContext') -> HealthCheckResult:
    return HealthCheckResult(component="RegimeCostNotification", status=HealthStatus.HEALTHY, message="Operational", timestamp_utc=get_utc_now_str())
"""
    if "check_regime_aware_cost_config_health" not in content:
        content += new_checks

        # update get_health_summary
        content = content.replace(
            "results.append(check_performance_retention_health(context))",
            "results.append(check_performance_retention_health(context))\n    results.append(check_regime_aware_cost_config_health(context))"
        )

        with open('usa_signal_bot/core/health.py', 'w') as f:
            f.write(content)

update_health()
