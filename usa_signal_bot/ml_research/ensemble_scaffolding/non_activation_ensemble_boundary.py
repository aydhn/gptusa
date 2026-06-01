from typing import Any, Dict, List, Optional
from .phase142_models import (
    NonActivationEnsembleBoundaryResult,
    NonActivationEnsembleBoundaryRule,
    NonActivationEnsembleRuleKind,
    create_non_activation_ensemble_boundary_rule_id,
    create_non_activation_ensemble_boundary_result_id,
    validate_non_activation_ensemble_boundary_result,
    _now
)

def build_non_activation_ensemble_boundary_rules(context_payload: Optional[Dict[str, Any]] = None) -> List[NonActivationEnsembleBoundaryRule]:
    p = context_payload or {}
    rules = []

    checks = [
        (NonActivationEnsembleRuleKind.NO_ENSEMBLE_FITTING, "No Ensemble Fitting", p.get('ensemble_fitting_performed', False)),
        (NonActivationEnsembleRuleKind.NO_LIVE_INFERENCE, "No Live Inference", p.get('live_inference_enabled', False)),
        (NonActivationEnsembleRuleKind.NO_TRADE_SIGNAL_OUTPUT, "No Trade Signal", p.get('produces_trade_signal', False)),
        (NonActivationEnsembleRuleKind.NO_BROKER_EXECUTION, "No Broker Execution", p.get('broker_execution_enabled', False)),
    ]

    for kind, name, val in checks:
        rules.append(NonActivationEnsembleBoundaryRule(
            rule_id=create_non_activation_ensemble_boundary_rule_id(),
            created_at_utc=_now(),
            rule_kind=kind,
            name=name,
            required=True,
            passed=not val,
            expected_value=False,
            observed_value=val,
            rationale="Non-activation boundary check",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return rules

def build_non_activation_ensemble_boundary_result(rules: List[NonActivationEnsembleBoundaryRule]) -> NonActivationEnsembleBoundaryResult:
    passed = all(r.passed for r in rules if r.required)

    res = NonActivationEnsembleBoundaryResult(
        boundary_id=create_non_activation_ensemble_boundary_result_id(),
        created_at_utc=_now(),
        rules=rules,
        boundary_passed=passed,
        no_ensemble_fitting=True,
        no_final_ensemble_prediction=True,
        no_live_inference=True,
        no_online_inference=True,
        no_trade_signal_output=True,
        no_order_decision_output=True,
        no_portfolio_weight_output=True,
        no_strategy_activation=True,
        no_broker_execution=True,
        no_paper_mutation=True,
        no_telegram_real_send=True,
        no_deployment=True,
        no_dashboard=True,
        no_live_daemon=True,
        no_scheduler=True,
        research_data_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    val_errs = validate_non_activation_ensemble_boundary_result(res)
    if val_errs:
        res.boundary_passed = False
        res.errors.extend(val_errs)

    return res

def non_activation_ensemble_boundary_passed(result: NonActivationEnsembleBoundaryResult) -> bool:
    return result.boundary_passed

def non_activation_ensemble_boundary_summary(result: NonActivationEnsembleBoundaryResult) -> Dict[str, Any]:
    return {"passed": result.boundary_passed}

def non_activation_ensemble_boundary_to_text(result: NonActivationEnsembleBoundaryResult, limit: int = 300) -> str:
    return f"Boundary Passed: {result.boundary_passed}"
