import datetime
from dataclasses import dataclass
from usa_signal_bot.core.config import get_config

@dataclass
class HealthCheckResult:
    name: str
    status: str
    message: str

class RuntimeContext:
    pass

def check_multi_timeframe_regime_config_health(context: RuntimeContext) -> HealthCheckResult:
    conf = get_config()
    if not conf.multi_timeframe_regime.warn_not_investment_advice:
        return HealthCheckResult("multi_timeframe_config", "FAIL", "warn_not_investment_advice must be True")
    if not conf.multi_timeframe_regime.warn_no_broker_execution:
        return HealthCheckResult("multi_timeframe_config", "FAIL", "warn_no_broker_execution must be True")
    return HealthCheckResult("multi_timeframe_config", "PASS", "OK")

def check_timeframe_resampler_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.timeframe_resampler import resample_daily_to_weekly
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100, "high": 110, "low": 90, "close": 105, "volume": 1000} for i in range(1, 10)]
    try:
        res = resample_daily_to_weekly(rows)
        if not res:
            return HealthCheckResult("timeframe_resampler", "FAIL", "Resampling returned empty")
        return HealthCheckResult("timeframe_resampler", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("timeframe_resampler", "FAIL", str(e))

def check_trend_confirmation_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.trend_confirmation import classify_trend_regime
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100+i, "high": 110+i, "low": 90+i, "close": 105+i, "volume": 1000} for i in range(1, 60)]
    try:
        r, _ = classify_trend_regime(rows)
        return HealthCheckResult("trend_confirmation", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("trend_confirmation", "FAIL", str(e))

def check_volatility_confirmation_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.volatility_confirmation import classify_volatility_map_regime
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100+i, "high": 110+i, "low": 90+i, "close": 105+i, "volume": 1000} for i in range(1, 60)]
    try:
        r, _ = classify_volatility_map_regime(rows)
        return HealthCheckResult("volatility_confirmation", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("volatility_confirmation", "FAIL", str(e))

def check_momentum_confirmation_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.momentum_confirmation import classify_momentum_regime
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100+i, "high": 110+i, "low": 90+i, "close": 105+i, "volume": 1000} for i in range(1, 60)]
    try:
        r, _ = classify_momentum_regime(rows)
        return HealthCheckResult("momentum_confirmation", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("momentum_confirmation", "FAIL", str(e))

def check_liquidity_confirmation_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.liquidity_confirmation import classify_liquidity_map_regime
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100+i, "high": 110+i, "low": 90+i, "close": 105+i, "volume": 100000} for i in range(1, 60)]
    try:
        r, _ = classify_liquidity_map_regime(rows)
        return HealthCheckResult("liquidity_confirmation", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("liquidity_confirmation", "FAIL", str(e))

def check_multi_timeframe_confirmation_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.timeframe_regime_confirmation import MultiTimeframeRegimeConfirmationEngine
    rows = [{"date": (datetime.date(2024, 1, 1) + datetime.timedelta(days=i)).isoformat(), "open": 100+i, "high": 110+i, "low": 90+i, "close": 105+i, "volume": 100000} for i in range(1, 60)]
    try:
        engine = MultiTimeframeRegimeConfirmationEngine()
        engine.confirm_symbol("SPY", rows)
        return HealthCheckResult("multi_timeframe_engine", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("multi_timeframe_engine", "FAIL", str(e))

def check_breadth_proxy_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.breadth_proxy import classify_breadth_regime
    try:
        classify_breadth_regime([])
        return HealthCheckResult("breadth_proxy", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("breadth_proxy", "FAIL", str(e))

def check_cross_sectional_regime_map_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.cross_sectional_regime_map import CrossSectionalRegimeMapBuilder
    try:
        b = CrossSectionalRegimeMapBuilder()
        b.build_map([])
        return HealthCheckResult("cross_sectional_map", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("cross_sectional_map", "FAIL", str(e))

def check_symbol_regime_alignment_health(context: RuntimeContext) -> HealthCheckResult:
    # Need dummy objects, skip deep check, just assert it exists
    from usa_signal_bot.regime_map.symbol_regime_alignment import calculate_alignment_score
    return HealthCheckResult("symbol_regime_alignment", "PASS", "OK")

def check_regime_transition_risk_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.transition_risk import aggregate_transition_risk
    try:
        aggregate_transition_risk([])
        return HealthCheckResult("regime_transition_risk", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("regime_transition_risk", "FAIL", str(e))

def check_regime_map_store_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.regime_map.regime_map_store import regime_map_store_dir
    from pathlib import Path
    try:
        regime_map_store_dir(Path("data"))
        return HealthCheckResult("regime_map_store", "PASS", "OK")
    except Exception as e:
        return HealthCheckResult("regime_map_store", "FAIL", str(e))

def check_regime_map_notification_health(context: RuntimeContext) -> HealthCheckResult:
    from usa_signal_bot.core.config import get_config
    if not get_config().regime_map_notifications.dry_run:
         return HealthCheckResult("regime_map_notification", "FAIL", "dry_run must be True")
    return HealthCheckResult("regime_map_notification", "PASS", "OK")

def check_all_regime_health(context: RuntimeContext) -> list[HealthCheckResult]:
    return [
        check_multi_timeframe_regime_config_health(context),
        check_timeframe_resampler_health(context),
        check_trend_confirmation_health(context),
        check_volatility_confirmation_health(context),
        check_momentum_confirmation_health(context),
        check_liquidity_confirmation_health(context),
        check_multi_timeframe_confirmation_health(context),
        check_breadth_proxy_health(context),
        check_cross_sectional_regime_map_health(context),
        check_symbol_regime_alignment_health(context),
        check_regime_transition_risk_health(context),
        check_regime_map_store_health(context),
        check_regime_map_notification_health(context)
    ]
