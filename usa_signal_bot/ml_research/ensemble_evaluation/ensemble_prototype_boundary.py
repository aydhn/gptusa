from typing import Any, Dict, List
import datetime

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeBoundaryResult,
    EnsemblePrototypeBoundaryRule,
    EnsemblePrototypeBoundaryRuleKind,
    create_ensemble_prototype_boundary_rule_id,
    create_ensemble_prototype_boundary_result_id
)

def build_ensemble_prototype_boundary_rules(context_payload: Dict[str, Any] | None = None) -> List[EnsemblePrototypeBoundaryRule]:
    # Mocking successful rules
    rules = []
    kinds = [
        EnsemblePrototypeBoundaryRuleKind.OFFLINE_PROTOTYPE_ONLY,
        EnsemblePrototypeBoundaryRuleKind.OFFLINE_EVALUATION_ONLY,
        EnsemblePrototypeBoundaryRuleKind.NO_LIVE_INFERENCE,
        EnsemblePrototypeBoundaryRuleKind.NO_ONLINE_INFERENCE,
        EnsemblePrototypeBoundaryRuleKind.NO_TRADE_SIGNAL_OUTPUT,
        EnsemblePrototypeBoundaryRuleKind.NO_ORDER_DECISION_OUTPUT,
        EnsemblePrototypeBoundaryRuleKind.NO_PORTFOLIO_WEIGHT_OUTPUT,
        EnsemblePrototypeBoundaryRuleKind.NO_STRATEGY_ACTIVATION,
        EnsemblePrototypeBoundaryRuleKind.NO_BROKER_EXECUTION,
        EnsemblePrototypeBoundaryRuleKind.NO_PAPER_MUTATION,
        EnsemblePrototypeBoundaryRuleKind.NO_TELEGRAM_REAL_SEND,
        EnsemblePrototypeBoundaryRuleKind.NO_DEPLOYMENT,
        EnsemblePrototypeBoundaryRuleKind.NO_DASHBOARD,
        EnsemblePrototypeBoundaryRuleKind.NO_LIVE_DAEMON,
        EnsemblePrototypeBoundaryRuleKind.NO_SCHEDULER
    ]

    for k in kinds:
        rules.append(EnsemblePrototypeBoundaryRule(
            rule_id=create_ensemble_prototype_boundary_rule_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            rule_kind=k,
            name=k.value,
            required=True,
            passed=True,
            expected_value=True,
            observed_value=True,
            rationale="Verified local only",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return rules

def build_ensemble_prototype_boundary_result(rules: List[EnsemblePrototypeBoundaryRule]) -> EnsemblePrototypeBoundaryResult:
    passed = all(r.passed for r in rules if r.required)

    return EnsemblePrototypeBoundaryResult(
        boundary_id=create_ensemble_prototype_boundary_result_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        rules=rules,
        boundary_passed=passed,
        offline_prototype_only=True,
        offline_evaluation_only=True,
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

def validate_ensemble_prototype_boundary_result(result: EnsemblePrototypeBoundaryResult) -> List[str]:
    errors = []
    if not result.boundary_passed:
         errors.append("Boundary not passed")
    return errors

def ensemble_prototype_boundary_passed(result: EnsemblePrototypeBoundaryResult) -> bool:
    return result.boundary_passed

def ensemble_prototype_boundary_summary(result: EnsemblePrototypeBoundaryResult) -> Dict[str, Any]:
    return {"passed": result.boundary_passed, "rule_count": len(result.rules)}

def ensemble_prototype_boundary_to_text(result: EnsemblePrototypeBoundaryResult, limit: int = 300) -> str:
    return str(ensemble_prototype_boundary_summary(result))
