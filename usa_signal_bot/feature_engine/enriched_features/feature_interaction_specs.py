from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import FeatureInteractionKind
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureInteractionSpec,
    create_feature_interaction_spec_id
)

def build_default_feature_interaction_specs() -> list[FeatureInteractionSpec]:
    return [
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="momentum_60_x_quality_confidence",
            interaction_kind=FeatureInteractionKind.MULTIPLICATIVE,
            left_feature="momentum_60",
            right_feature="data_confidence_score_feature",
            output_column="momentum_60_x_quality_confidence",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="trend_strength_20_x_data_confidence",
            interaction_kind=FeatureInteractionKind.MULTIPLICATIVE,
            left_feature="trend_strength_20",
            right_feature="data_confidence_score_feature",
            output_column="trend_strength_20_x_data_confidence",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="realized_vol_20_x_event_importance",
            interaction_kind=FeatureInteractionKind.MULTIPLICATIVE,
            left_feature="realized_vol_20",
            right_feature="event_importance_score",
            output_column="realized_vol_20_x_event_importance",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="rs_ret_60_vs_spy_x_source_trust",
            interaction_kind=FeatureInteractionKind.MULTIPLICATIVE,
            left_feature="rs_ret_60_vs_spy",
            right_feature="source_trust_score_feature",
            output_column="rs_ret_60_vs_spy_x_source_trust",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="rolling_vol_20_x_unexplained_anomaly_count",
            interaction_kind=FeatureInteractionKind.MULTIPLICATIVE,
            left_feature="rolling_vol_20",
            right_feature="unexplained_anomaly_count",
            output_column="rolling_vol_20_x_unexplained_anomaly_count",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="momentum_20_minus_realized_vol_20",
            interaction_kind=FeatureInteractionKind.DIFFERENCE,
            left_feature="momentum_20",
            right_feature="realized_vol_20",
            output_column="momentum_20_minus_realized_vol_20",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="trend_strength_60_minus_vol_of_vol_20",
            interaction_kind=FeatureInteractionKind.DIFFERENCE,
            left_feature="trend_strength_60",
            right_feature="vol_of_vol_20",
            output_column="trend_strength_60_minus_vol_of_vol_20",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="event_conditioned_momentum_20",
            interaction_kind=FeatureInteractionKind.EVENT_CONDITIONED,
            left_feature="momentum_20",
            conditioning_feature="event_day_flag",
            output_column="event_conditioned_momentum_20",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="quality_weighted_momentum_60",
            interaction_kind=FeatureInteractionKind.QUALITY_WEIGHTED,
            left_feature="momentum_60",
            conditioning_feature="provider_quality_score_feature",
            output_column="quality_weighted_momentum_60",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
        FeatureInteractionSpec(
            interaction_id=create_feature_interaction_spec_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            name="calendar_conditioned_volatility_20",
            interaction_kind=FeatureInteractionKind.CALENDAR_CONDITIONED,
            left_feature="realized_vol_20",
            conditioning_feature="market_holiday_context_flag",
            output_column="calendar_conditioned_volatility_20",
            local_pandas_only=True,
            safe_for_research_only=True,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
        ),
    ]

def feature_interaction_spec_by_name(name: str, specs: list[FeatureInteractionSpec] | None = None) -> FeatureInteractionSpec | None:
    specs = specs or build_default_feature_interaction_specs()
    for s in specs:
        if s.name == name:
            return s
    return None

def validate_feature_interaction_specs(specs: list[FeatureInteractionSpec]) -> list[str]:
    return []

def feature_interaction_specs_summary(specs: list[FeatureInteractionSpec]) -> dict[str, Any]:
    return {"spec_count": len(specs)}

def feature_interaction_specs_to_text(specs: list[FeatureInteractionSpec], limit: int = 200) -> str:
    return f"{len(specs)} interaction specs"
