from typing import Any
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureGroupDefinition,
    FactorCandidateDefinition,
    FactorCompositionSpec,
    create_factor_composition_spec_id,
    validate_factor_composition_spec,
    _now_str
)

def build_factor_composition_spec(groups: list[FeatureGroupDefinition], candidates: list[FactorCandidateDefinition]) -> FactorCompositionSpec:
    spec = FactorCompositionSpec(
        spec_id=create_factor_composition_spec_id(),
        created_at_utc=_now_str(),
        factor_candidates=candidates,
        feature_groups=groups,
        composition_version="1.0",
        local_pandas_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False
    )
    validate_factor_composition_spec(spec)
    return spec

def factor_composition_spec_summary(spec: FactorCompositionSpec) -> dict[str, Any]:
    return {
        "spec_id": spec.spec_id,
        "candidate_count": len(spec.factor_candidates),
        "group_count": len(spec.feature_groups),
        "version": spec.composition_version,
        "is_safe_research_only": spec.research_data_only and not spec.produces_trade_signal
    }

def factor_composition_spec_to_text(spec: FactorCompositionSpec, limit: int = 300) -> str:
    summary = factor_composition_spec_summary(spec)
    lines = [
        f"Factor Composition Spec: {spec.spec_id}",
        f"Version: {summary['version']}",
        f"Safe Research Only: {summary['is_safe_research_only']}",
        f"Groups: {summary['group_count']}, Candidates: {summary['candidate_count']}"
    ]
    return "\n".join(lines)
