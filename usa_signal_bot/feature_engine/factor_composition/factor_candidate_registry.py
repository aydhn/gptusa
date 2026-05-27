from typing import Any
from usa_signal_bot.core.enums import FactorCandidateKind
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FactorComponent,
    FactorCandidateDefinition,
    create_factor_candidate_id,
    validate_factor_candidate_definition,
    _now_str
)

def build_factor_candidate_definitions(components: list[FactorComponent]) -> list[FactorCandidateDefinition]:
    candidates = []

    candidate_mappings = [
        ("momentum_research_factor", FactorCandidateKind.MOMENTUM_FACTOR, ["momentum_component"], "factor_momentum"),
        ("trend_research_factor", FactorCandidateKind.TREND_FACTOR, ["trend_component"], "factor_trend"),
        ("volatility_research_factor", FactorCandidateKind.VOLATILITY_FACTOR, ["volatility_component"], "factor_volatility"),
        ("liquidity_research_factor", FactorCandidateKind.LIQUIDITY_FACTOR, ["liquidity_component"], "factor_liquidity"),
        ("relative_strength_research_factor", FactorCandidateKind.RELATIVE_STRENGTH_FACTOR, ["relative_strength_component"], "factor_relative_strength"),
        ("quality_context_research_factor", FactorCandidateKind.QUALITY_CONTEXT_FACTOR, ["quality_context_component"], "factor_quality_context"),
        ("event_context_research_factor", FactorCandidateKind.EVENT_CONTEXT_FACTOR, ["event_context_component"], "factor_event_context"),
        ("calendar_context_research_factor", FactorCandidateKind.CALENDAR_CONTEXT_FACTOR, ["calendar_context_component"], "factor_calendar_context"),
        ("data_confidence_research_factor", FactorCandidateKind.DATA_CONFIDENCE_FACTOR, ["confidence_component"], "factor_data_confidence"),
        ("composite_research_factor", FactorCandidateKind.COMPOSITE_RESEARCH_FACTOR, ["momentum_component", "trend_component", "volatility_component", "quality_context_component"], "factor_composite")
    ]

    for c_name, kind, comp_names, out_col in candidate_mappings:
        comps = [c for c in components if c.component_name in comp_names]
        input_cols = []
        for c in comps:
            input_cols.extend(c.source_feature_columns)
        input_cols = list(set(input_cols)) # unique

        cand = FactorCandidateDefinition(
            factor_id=create_factor_candidate_id(),
            created_at_utc=_now_str(),
            factor_name=c_name,
            factor_kind=kind,
            components=comps,
            input_feature_columns=input_cols,
            output_column=out_col,
            description=f"Research factor for {c_name}",
            composition_method="linear_weighted_sum",
            normalization_required=True,
            diagnostics_required=True,
            implementation_phase=121,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False
        )
        candidates.append(cand)

    return candidates

def factor_candidate_by_name(name: str, candidates: list[FactorCandidateDefinition] | None = None) -> FactorCandidateDefinition | None:
    if not candidates: return None
    for c in candidates:
        if c.factor_name == name:
            return c
    return None

def validate_factor_candidates(candidates: list[FactorCandidateDefinition]) -> list[str]:
    errors = []
    for c in candidates:
        validate_factor_candidate_definition(c)
        if c.errors:
            errors.extend([f"Candidate {c.factor_name} error: {e}" for e in c.errors])
    return errors

def factor_candidate_registry_summary(candidates: list[FactorCandidateDefinition]) -> dict[str, Any]:
    return {
        "candidate_count": len(candidates),
        "candidates": [c.factor_name for c in candidates]
    }

def factor_candidate_registry_to_text(candidates: list[FactorCandidateDefinition], limit: int = 200) -> str:
    summary = factor_candidate_registry_summary(candidates)
    lines = [f"Factor Candidate Registry: {summary['candidate_count']} candidates"]
    for c in candidates[:limit]:
        lines.append(f"  - {c.factor_name} ({c.factor_kind.value}) - output: {c.output_column}")
    return "\n".join(lines)
