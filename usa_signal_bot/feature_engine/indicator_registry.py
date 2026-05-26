import datetime
from typing import Any
from usa_signal_bot.core.enums import IndicatorCategory, FeatureComputationMode, FeatureFoundationRiskFlag
from usa_signal_bot.feature_engine.phase116_models import IndicatorDefinition, create_indicator_definition_id, validate_indicator_definition

def build_default_indicator_definitions() -> list[IndicatorDefinition]:
    default_indicators = [
        "sma", "ema", "wma", "rsi", "macd", "stochastic", "atr", "true_range",
        "bollinger_band_width", "rolling_volatility", "rolling_return",
        "cumulative_return", "rate_of_change", "zscore_close", "volume_sma",
        "volume_zscore", "obv_metadata", "vwap_metadata", "price_gap",
        "candle_body", "upper_shadow", "lower_shadow", "range_pct",
        "event_day_flag", "earnings_context_flag", "macro_context_flag",
        "data_quality_score_feature"
    ]

    out = []
    for name in default_indicators:
        item = IndicatorDefinition(
            indicator_id=create_indicator_definition_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            name=name,
            category=IndicatorCategory.TREND if "sma" in name else IndicatorCategory.UNKNOWN,
            description=f"Placeholder indicator for {name}",
            input_columns=["close"],
            output_columns=[f"{name}_out"],
            parameters={},
            computation_mode=FeatureComputationMode.PLANNED,
            requires_network=False,
            requires_paid_api=False,
            requires_scraping=False,
            produces_trade_signal=False,
            produces_order_decision=False,
            enabled_for_phase116=True,
            implementation_phase=117,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        out.append(item)
    return out

def indicator_definition_by_name(name: str, indicators: list[IndicatorDefinition] | None = None) -> IndicatorDefinition | None:
    if indicators is None:
        indicators = build_default_indicator_definitions()
    for ind in indicators:
        if ind.name == name:
            return ind
    return None

def validate_indicator_registry(indicators: list[IndicatorDefinition]) -> list[str]:
    errors = []
    for ind in indicators:
        validate_indicator_definition(ind)
        if ind.errors:
            errors.extend([f"Indicator {ind.name} error: {e}" for e in ind.errors])
    return errors

def indicator_registry_summary(indicators: list[IndicatorDefinition]) -> dict[str, Any]:
    return {"total": len(indicators)}

def indicator_registry_to_text(indicators: list[IndicatorDefinition], limit: int = 200) -> str:
    lines = [f"Total Indicators: {len(indicators)}"]
    for i, ind in enumerate(indicators):
        if i >= limit:
            lines.append("... [truncated]")
            break
        lines.append(f" - {ind.name} [{ind.category.value}]")
    return "\n".join(lines)
