from typing import Any, Dict, List
import datetime

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    BlendContributionDiagnostic,
    EnsemblePrototypeSpec,
    create_blend_contribution_diagnostic_id,
    BlendDiagnosticKind
)

def build_blend_contribution_diagnostics(specs: List[EnsemblePrototypeSpec]) -> List[BlendContributionDiagnostic]:
    diagnostics = []
    for spec in specs:
        diagnostics.extend(build_blend_diagnostics_for_spec(spec))
    return diagnostics

def build_blend_diagnostics_for_spec(spec: EnsemblePrototypeSpec) -> List[BlendContributionDiagnostic]:
    return [check_coefficient_sum(spec)] + check_coefficient_range(spec)

def check_coefficient_sum(spec: EnsemblePrototypeSpec) -> BlendContributionDiagnostic:
    return BlendContributionDiagnostic(
        diagnostic_id=create_blend_contribution_diagnostic_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        prototype_id=spec.prototype_id,
        candidate_ref_id="all",
        blend_plan_id=spec.blend_plan_id,
        diagnostic_kind=BlendDiagnosticKind.COEFFICIENT_SUM_CHECK,
        coefficient_value=spec.coefficient_sum,
        contribution_share=None,
        contribution_valid=spec.coefficient_valid,
        dominant_candidate_warning=False,
        not_portfolio_weight=True,
        not_allocation=True,
        not_target_weight=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def check_coefficient_range(spec: EnsemblePrototypeSpec) -> List[BlendContributionDiagnostic]:
    return []

def check_dominant_candidate(spec: EnsemblePrototypeSpec, dominance_threshold: float = 0.80) -> List[BlendContributionDiagnostic]:
    return []

def validate_blend_contribution_diagnostics(items: List[BlendContributionDiagnostic]) -> List[str]:
    errors = []
    for item in items:
        if not item.not_portfolio_weight:
             errors.append("not_portfolio_weight must be True")
    return errors

def blend_diagnostics_summary(items: List[BlendContributionDiagnostic]) -> Dict[str, Any]:
    return {"diagnostic_count": len(items)}

def blend_diagnostics_to_text(items: List[BlendContributionDiagnostic], limit: int = 300) -> str:
    return str(blend_diagnostics_summary(items))
