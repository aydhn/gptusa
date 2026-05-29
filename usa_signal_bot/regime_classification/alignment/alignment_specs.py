from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    RegimeAwareAlignmentSpec, MarketBehaviorOverlaySpec, create_regime_aware_alignment_spec_id,
    create_market_behavior_overlay_spec_id, RegimeAlignmentKind, RegimeCompatibilityMetricKind,
    MarketBehaviorOverlayKind, _now
)
from usa_signal_bot.core.enums import RegimeAlignmentRiskFlag

def build_default_regime_alignment_specs() -> list[RegimeAwareAlignmentSpec]:
    return [
        RegimeAwareAlignmentSpec(
            spec_id=create_regime_aware_alignment_spec_id(),
            created_at_utc=_now(),
            spec_name="factor_to_regime_stability_alignment",
            alignment_kind=RegimeAlignmentKind.FACTOR_TO_REGIME_CONTEXT,
            compatibility_metric_kind=RegimeCompatibilityMetricKind.FACTOR_STABILITY_ALIGNMENT
        ),
        RegimeAwareAlignmentSpec(
            spec_id=create_regime_aware_alignment_spec_id(),
            created_at_utc=_now(),
            spec_name="factor_to_churn_context_alignment",
            alignment_kind=RegimeAlignmentKind.FACTOR_TO_REGIME_CONTEXT,
            compatibility_metric_kind=RegimeCompatibilityMetricKind.CHURN_SENSITIVITY_CONTEXT
        ),
        RegimeAwareAlignmentSpec(
            spec_id=create_regime_aware_alignment_spec_id(),
            created_at_utc=_now(),
            spec_name="factor_to_persistence_context_alignment",
            alignment_kind=RegimeAlignmentKind.FACTOR_TO_REGIME_CONTEXT,
            compatibility_metric_kind=RegimeCompatibilityMetricKind.PERSISTENCE_CONTEXT
        ),
        RegimeAwareAlignmentSpec(
            spec_id=create_regime_aware_alignment_spec_id(),
            created_at_utc=_now(),
            spec_name="feature_to_data_quality_context_alignment",
            alignment_kind=RegimeAlignmentKind.FEATURE_TO_REGIME_CONTEXT,
            compatibility_metric_kind=RegimeCompatibilityMetricKind.DATA_QUALITY_ALIGNMENT
        ),
        RegimeAwareAlignmentSpec(
            spec_id=create_regime_aware_alignment_spec_id(),
            created_at_utc=_now(),
            spec_name="factor_to_cross_symbol_behavior_alignment",
            alignment_kind=RegimeAlignmentKind.CROSS_SYMBOL_ALIGNMENT,
            compatibility_metric_kind=RegimeCompatibilityMetricKind.CROSS_SYMBOL_ALIGNMENT
        ),
        RegimeAwareAlignmentSpec(
            spec_id=create_regime_aware_alignment_spec_id(),
            created_at_utc=_now(),
            spec_name="diagnostic_to_factor_context_alignment",
            alignment_kind=RegimeAlignmentKind.DIAGNOSTIC_TO_FACTOR_CONTEXT,
            compatibility_metric_kind=RegimeCompatibilityMetricKind.DIAGNOSTIC_CONTEXT_ALIGNMENT
        )
    ]

def build_default_market_behavior_overlay_specs() -> list[MarketBehaviorOverlaySpec]:
    return [
        MarketBehaviorOverlaySpec(
            spec_id=create_market_behavior_overlay_spec_id(),
            created_at_utc=_now(),
            overlay_name="regime_label_overlay",
            overlay_kind=MarketBehaviorOverlayKind.REGIME_LABEL_OVERLAY
        ),
        MarketBehaviorOverlaySpec(
            spec_id=create_market_behavior_overlay_spec_id(),
            created_at_utc=_now(),
            overlay_name="transition_behavior_overlay",
            overlay_kind=MarketBehaviorOverlayKind.TRANSITION_BEHAVIOR_OVERLAY
        ),
        MarketBehaviorOverlaySpec(
            spec_id=create_market_behavior_overlay_spec_id(),
            created_at_utc=_now(),
            overlay_name="persistence_behavior_overlay",
            overlay_kind=MarketBehaviorOverlayKind.PERSISTENCE_BEHAVIOR_OVERLAY
        ),
        MarketBehaviorOverlaySpec(
            spec_id=create_market_behavior_overlay_spec_id(),
            created_at_utc=_now(),
            overlay_name="churn_behavior_overlay",
            overlay_kind=MarketBehaviorOverlayKind.CHURN_BEHAVIOR_OVERLAY
        ),
        MarketBehaviorOverlaySpec(
            spec_id=create_market_behavior_overlay_spec_id(),
            created_at_utc=_now(),
            overlay_name="stability_behavior_overlay",
            overlay_kind=MarketBehaviorOverlayKind.STABILITY_BEHAVIOR_OVERLAY
        ),
        MarketBehaviorOverlaySpec(
            spec_id=create_market_behavior_overlay_spec_id(),
            created_at_utc=_now(),
            overlay_name="data_quality_overlay",
            overlay_kind=MarketBehaviorOverlayKind.DATA_QUALITY_OVERLAY
        )
    ]

def validate_regime_alignment_specs(specs: list[RegimeAwareAlignmentSpec]) -> list[str]:
    errs = []
    for s in specs:
        if s.produces_trade_signal or s.produces_order_decision:
            errs.append(f"Spec {s.spec_name} produces trade signal/order")
    return errs

def validate_market_behavior_overlay_specs(specs: list[MarketBehaviorOverlaySpec]) -> list[str]:
    errs = []
    for s in specs:
        if s.produces_trade_signal or s.produces_order_decision:
            errs.append(f"Spec {s.overlay_name} produces trade signal/order")
    return errs

def alignment_specs_summary(alignment_specs: list[RegimeAwareAlignmentSpec], overlay_specs: list[MarketBehaviorOverlaySpec]) -> dict[str, Any]:
    return {"align_count": len(alignment_specs), "overlay_count": len(overlay_specs)}

def alignment_specs_to_text(alignment_specs: list[RegimeAwareAlignmentSpec], overlay_specs: list[MarketBehaviorOverlaySpec], limit: int = 300) -> str:
    return f"Specs: {len(alignment_specs)} align, {len(overlay_specs)} overlays."
