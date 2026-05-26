from typing import List, Dict, Any, Optional
from usa_signal_bot.feature_engine.advanced_features.phase118_models import (
    AdvancedFeatureSpec,
    AdvancedFeatureFamily,
    NormalizationMethod,
    create_advanced_feature_spec_id
)
import datetime

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_advanced_feature_specs() -> List[AdvancedFeatureSpec]:
    specs = []

    # helper for creating specs
    def _make(name, family, input_cols, out_cols, norm_method=NormalizationMethod.NONE, cross=False):
        return AdvancedFeatureSpec(
            spec_id=create_advanced_feature_spec_id(),
            created_at_utc=_now(),
            feature_name=name,
            family=family,
            normalization_method=norm_method,
            input_columns=input_cols,
            output_columns=out_cols,
            parameters={},
            min_required_rows=30 if not cross else 0,
            min_required_symbols=2 if cross else 1,
            local_pandas_only=True,
            cross_sectional=cross,
            requires_network=False,
            requires_paid_api=False,
            requires_scraping=False,
            produces_trade_signal=False,
            produces_order_decision=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )

    # Volatility
    specs.append(_make("realized_vol_10", AdvancedFeatureFamily.ADVANCED_VOLATILITY, ["ret_1d"], ["realized_vol_10"]))
    specs.append(_make("realized_vol_20", AdvancedFeatureFamily.ADVANCED_VOLATILITY, ["ret_1d"], ["realized_vol_20"]))
    specs.append(_make("downside_vol_20", AdvancedFeatureFamily.ADVANCED_VOLATILITY, ["ret_1d"], ["downside_vol_20"]))
    specs.append(_make("upside_vol_20", AdvancedFeatureFamily.ADVANCED_VOLATILITY, ["ret_1d"], ["upside_vol_20"]))
    specs.append(_make("vol_of_vol_20", AdvancedFeatureFamily.ADVANCED_VOLATILITY, ["realized_vol_20"], ["vol_of_vol_20"]))
    specs.append(_make("atr_percentile_60", AdvancedFeatureFamily.ADVANCED_VOLATILITY, ["atr_14"], ["atr_percentile_60"], NormalizationMethod.PERCENTILE_RANK))

    # Momentum
    specs.append(_make("momentum_20", AdvancedFeatureFamily.ADVANCED_MOMENTUM, ["close"], ["momentum_20"]))
    specs.append(_make("momentum_60", AdvancedFeatureFamily.ADVANCED_MOMENTUM, ["close"], ["momentum_60"]))
    specs.append(_make("momentum_acceleration_20_60", AdvancedFeatureFamily.ADVANCED_MOMENTUM, ["momentum_20", "momentum_60"], ["momentum_accel_20_60"]))
    specs.append(_make("rsi_zscore_60", AdvancedFeatureFamily.ADVANCED_MOMENTUM, ["rsi_14"], ["rsi_14_zscore_60"], NormalizationMethod.Z_SCORE))
    specs.append(_make("macd_hist_zscore_60", AdvancedFeatureFamily.ADVANCED_MOMENTUM, ["macd_hist"], ["macd_hist_zscore_60"], NormalizationMethod.Z_SCORE))

    # Trend
    specs.append(_make("trend_slope_20", AdvancedFeatureFamily.ADVANCED_TREND, ["close"], ["trend_slope_20"]))
    specs.append(_make("trend_slope_60", AdvancedFeatureFamily.ADVANCED_TREND, ["close"], ["trend_slope_60"]))
    specs.append(_make("trend_strength_20", AdvancedFeatureFamily.ADVANCED_TREND, ["trend_slope_20", "close"], ["trend_strength_20"]))
    specs.append(_make("close_to_sma20_zscore_60", AdvancedFeatureFamily.ADVANCED_TREND, ["close"], ["close_to_sma20_zscore_60"], NormalizationMethod.Z_SCORE))

    # Normalizations (generic)
    specs.append(_make("rolling_zscore_close_60", AdvancedFeatureFamily.NORMALIZATION, ["close"], ["close_zscore_60"], NormalizationMethod.Z_SCORE))
    specs.append(_make("rolling_percentile_close_60", AdvancedFeatureFamily.NORMALIZATION, ["close"], ["close_percentile_60"], NormalizationMethod.PERCENTILE_RANK))

    # Cross-sectional
    specs.append(_make("cross_sectional_return_rank_20", AdvancedFeatureFamily.CROSS_SECTIONAL_RANK, ["ret_1d"], ["cs_ret_1d_percentile"], NormalizationMethod.CROSS_SECTIONAL_PERCENTILE, True))
    specs.append(_make("cross_sectional_momentum_rank_60", AdvancedFeatureFamily.CROSS_SECTIONAL_RANK, ["momentum_60"], ["cs_momentum_60_percentile"], NormalizationMethod.CROSS_SECTIONAL_PERCENTILE, True))
    specs.append(_make("cross_sectional_volatility_rank_20", AdvancedFeatureFamily.VOLATILITY_RANK, ["realized_vol_20"], ["cs_realized_vol_20_rank"], NormalizationMethod.CROSS_SECTIONAL_PERCENTILE, True))
    specs.append(_make("cross_sectional_liquidity_rank_20", AdvancedFeatureFamily.LIQUIDITY_RANK, ["volume"], ["cs_liquidity_rank_20"], NormalizationMethod.CROSS_SECTIONAL_PERCENTILE, True))

    # Relative Strength
    specs.append(_make("relative_strength_vs_spy_20", AdvancedFeatureFamily.RELATIVE_STRENGTH, ["ret_20d"], ["rs_ret_20d_vs_spy"], NormalizationMethod.NONE, True))
    specs.append(_make("relative_strength_vs_spy_60", AdvancedFeatureFamily.RELATIVE_STRENGTH, ["momentum_60"], ["rs_momentum_60_vs_spy"], NormalizationMethod.NONE, True))

    return specs

def advanced_feature_spec_by_name(name: str, specs: Optional[List[AdvancedFeatureSpec]] = None) -> Optional[AdvancedFeatureSpec]:
    specs = specs or build_advanced_feature_specs()
    for s in specs:
        if s.feature_name == name:
            return s
    return None

def advanced_feature_names() -> List[str]:
    return [s.feature_name for s in build_advanced_feature_specs()]

def validate_advanced_feature_registry(specs: List[AdvancedFeatureSpec]) -> List[str]:
    errors = []
    for s in specs:
        if s.requires_network:
            errors.append(f"{s.feature_name} has requires_network=True")
        if s.produces_trade_signal or s.produces_order_decision:
            errors.append(f"{s.feature_name} produces trade signal or order decision")
    return errors

def advanced_feature_registry_summary(specs: List[AdvancedFeatureSpec]) -> Dict[str, Any]:
    return {
        "spec_count": len(specs),
        "families": list(set([s.family.value for s in specs])),
        "is_valid": len(validate_advanced_feature_registry(specs)) == 0
    }

def advanced_feature_registry_to_text(specs: List[AdvancedFeatureSpec], limit: int = 200) -> str:
    lines = [f"{s.feature_name} ({s.family.value})" for s in specs[:limit]]
    return "Advanced Feature Registry:\n" + "\n".join(lines)
