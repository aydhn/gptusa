from typing import Any
from usa_signal_bot.core.enums import MarketBehaviorProfileKind
from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import MarketBehaviorProfileSpec

def build_default_market_behavior_profile_specs() -> list[MarketBehaviorProfileSpec]:
    return [
        MarketBehaviorProfileSpec(
            profile_name="transition_behavior_profile",
            profile_kind=MarketBehaviorProfileKind.TRANSITION_BEHAVIOR,
            required_artifacts=["transition_matrices"],
            source_fields=["symbol", "transition_matrix", "dominant_transition"],
            summary_fields=["dominant_transition_summary"]
        ),
        MarketBehaviorProfileSpec(
            profile_name="persistence_behavior_profile",
            profile_kind=MarketBehaviorProfileKind.PERSISTENCE_BEHAVIOR,
            required_artifacts=["persistence_profiles"],
            source_fields=["symbol", "median_run_length", "self_persistence_rate"],
            summary_fields=["persistence_summary"]
        ),
        MarketBehaviorProfileSpec(
            profile_name="duration_behavior_profile",
            profile_kind=MarketBehaviorProfileKind.UNKNOWN,
            required_artifacts=["duration_profiles"],
            source_fields=["symbol", "average_duration"],
            summary_fields=["duration_summary"]
        ),
        MarketBehaviorProfileSpec(
            profile_name="churn_behavior_profile",
            profile_kind=MarketBehaviorProfileKind.CHURN_BEHAVIOR,
            required_artifacts=["churn_diagnostics"],
            source_fields=["symbol", "churn_level", "switch_rate"],
            summary_fields=["churn_summary"]
        ),
        MarketBehaviorProfileSpec(
            profile_name="stability_behavior_profile",
            profile_kind=MarketBehaviorProfileKind.STABILITY_BEHAVIOR,
            required_artifacts=["stability_diagnostics"],
            source_fields=["symbol", "stability_score"],
            summary_fields=["stability_summary"]
        ),
        MarketBehaviorProfileSpec(
            profile_name="cross_symbol_behavior_profile",
            profile_kind=MarketBehaviorProfileKind.CROSS_SYMBOL_BEHAVIOR,
            required_artifacts=["transition_matrices", "persistence_profiles"],
            source_fields=["symbol_count", "dominant_regime_distribution"],
            summary_fields=["cross_symbol_summary"]
        ),
        MarketBehaviorProfileSpec(
            profile_name="data_quality_behavior_profile",
            profile_kind=MarketBehaviorProfileKind.DATA_QUALITY_BEHAVIOR,
            required_artifacts=["stability_diagnostics"],
            source_fields=["symbol", "data_quality_context"],
            summary_fields=["data_quality_summary"]
        )
    ]

def market_behavior_profile_spec_by_name(name: str, specs: list[MarketBehaviorProfileSpec] | None = None) -> MarketBehaviorProfileSpec | None:
    if specs is None:
        specs = build_default_market_behavior_profile_specs()
    for s in specs:
        if s.profile_name == name:
            return s
    return None

def validate_market_behavior_profile_specs(specs: list[MarketBehaviorProfileSpec]) -> list[str]:
    errs = []
    names = set()
    for s in specs:
        if s.profile_name in names:
            errs.append(f"Duplicate spec name: {s.profile_name}")
        names.add(s.profile_name)
        if not s.research_metadata_only: errs.append(f"Spec {s.profile_name} research_metadata_only must be true")
        if s.produces_trade_signal: errs.append(f"Spec {s.profile_name} produces_trade_signal must be false")
        if s.produces_order_decision: errs.append(f"Spec {s.profile_name} produces_order_decision must be false")
        if s.produces_portfolio_weights: errs.append(f"Spec {s.profile_name} produces_portfolio_weights must be false")
    return errs

def market_behavior_profile_specs_summary(specs: list[MarketBehaviorProfileSpec]) -> dict[str, Any]:
    return {"spec_count": len(specs), "names": [s.profile_name for s in specs]}

def market_behavior_profile_specs_to_text(specs: list[MarketBehaviorProfileSpec], limit: int = 200) -> str:
    lines = [f"Profile Specs ({len(specs)}):"]
    for s in specs:
        lines.append(f"- {s.profile_name} ({s.profile_kind.value})")
    return "\n".join(lines)[:limit]
