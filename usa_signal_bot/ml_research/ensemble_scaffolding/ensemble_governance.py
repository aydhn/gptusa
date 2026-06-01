from typing import Any, Dict, List
from .phase142_models import (
    EnsembleGovernanceResult,
    EnsembleGovernanceRule,
    EnsemblePreparationReport,
    CandidateGroupSpec,
    BlendCoefficientPlan,
    EnsembleGovernanceRuleKind,
    EnsembleGovernanceStatus,
    create_ensemble_governance_rule_id,
    create_ensemble_governance_result_id,
    validate_ensemble_governance_result,
    _now
)

def build_ensemble_governance_rules(reports: List[EnsemblePreparationReport], groups: List[CandidateGroupSpec], blend_plans: List[BlendCoefficientPlan]) -> List[EnsembleGovernanceRule]:
    rules = []

    # Check no ensemble fitting
    fitting = any(r.fitting_performed for r in reports) or any(b.fitting_performed for b in blend_plans)
    r1 = EnsembleGovernanceRule(
        rule_id=create_ensemble_governance_rule_id(),
        created_at_utc=_now(),
        rule_kind=EnsembleGovernanceRuleKind.NO_ENSEMBLE_FITTING,
        name="No Ensemble Fitting",
        status=EnsembleGovernanceStatus.FAILED if fitting else EnsembleGovernanceStatus.PASSED,
        required=True,
        passed=not fitting,
        expected_value=False,
        observed_value=fitting,
        rationale="Phase 142 is scaffolding only",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    rules.append(r1)

    # Check blend coefficients are not portfolio weights
    is_pw = any(not b.not_portfolio_weight for b in blend_plans)
    r2 = EnsembleGovernanceRule(
        rule_id=create_ensemble_governance_rule_id(),
        created_at_utc=_now(),
        rule_kind=EnsembleGovernanceRuleKind.BLEND_COEFFICIENTS_NOT_PORTFOLIO_WEIGHTS,
        name="Blend Coefficients Not Portfolio Weights",
        status=EnsembleGovernanceStatus.FAILED if is_pw else EnsembleGovernanceStatus.PASSED,
        required=True,
        passed=not is_pw,
        expected_value=True,
        observed_value=not is_pw,
        rationale="Blend coefficients must not be interpreted as allocations",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    rules.append(r2)

    return rules

def build_ensemble_governance_result(reports: List[EnsemblePreparationReport], groups: List[CandidateGroupSpec], blend_plans: List[BlendCoefficientPlan]) -> EnsembleGovernanceResult:
    rules = build_ensemble_governance_rules(reports, groups, blend_plans)
    passed = all(r.passed for r in rules if r.required)

    res = EnsembleGovernanceResult(
        governance_id=create_ensemble_governance_result_id(),
        created_at_utc=_now(),
        rules=rules,
        governance_status=EnsembleGovernanceStatus.PASSED if passed else EnsembleGovernanceStatus.FAILED,
        governance_passed=passed,
        preparation_reports=reports,
        candidate_groups=groups,
        blend_plans=blend_plans,
        research_only_ensemble_preparation=True,
        live_use_allowed=False,
        paper_use_allowed=False,
        broker_use_allowed=False,
        deployment_allowed=False,
        strategy_activation_allowed=False,
        fitting_performed=any(r.fitting_performed for r in reports),
                threshold_optimization_performed=any(r.threshold_optimization_performed for r in reports),
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    val_errs = validate_ensemble_governance_result(res)
    if val_errs:
        res.governance_passed = False
        res.governance_status = EnsembleGovernanceStatus.FAILED
        res.errors.extend(val_errs)

    return res

def ensemble_governance_passed(result: EnsembleGovernanceResult) -> bool:
    return result.governance_passed

def ensemble_governance_summary(result: EnsembleGovernanceResult) -> Dict[str, Any]:
    return {"passed": result.governance_passed, "rules": len(result.rules)}

def ensemble_governance_to_text(result: EnsembleGovernanceResult, limit: int = 300) -> str:
    return f"Governance Passed: {result.governance_passed}"
