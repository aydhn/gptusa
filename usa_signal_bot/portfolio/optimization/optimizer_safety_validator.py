from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerPrototypeContext, OptimizerPolicy, OptimizerObjectiveContract, OptimizerConstraintContract, OptimizerSandboxResult, ObjectiveComparisonReport, OptimizerSafetyBoundaryResult, Phase157ReadinessGate, OptimizerPrototypeRiskFlag
from usa_signal_bot.portfolio.optimization.optimizer_input_resolver import detect_forbidden_optimizer_columns, detect_forbidden_optimizer_fields

def validate_optimizer_context_safety(context: OptimizerPrototypeContext) -> List[str]:
    errs = []
    if context.actual_target_weights_produced: errs.append("actual_target_weights_produced")
    if context.actual_allocation_produced: errs.append("actual_allocation_produced")
    if context.actual_position_size_produced: errs.append("actual_position_size_produced")
    if context.order_size_produced: errs.append("order_size_produced")
    if context.capital_deployment_allowed: errs.append("capital_deployment_allowed")
    if context.actual_portfolio_optimization_enabled: errs.append("actual_portfolio_optimization_enabled")
    if context.broker_execution_enabled: errs.append("broker_execution_enabled")
    if context.real_order_creation_enabled: errs.append("real_order_creation_enabled")
    if context.paper_state_mutation_enabled: errs.append("paper_state_mutation_enabled")
    if context.deployment_allowed: errs.append("deployment_allowed")
    if context.investment_advice: errs.append("investment_advice")
    return errs

def validate_optimizer_policy_safety(policy: OptimizerPolicy) -> List[str]:
    errs = []
    if policy.actual_target_weights_allowed: errs.append("actual_target_weights_allowed")
    if policy.actual_allocation_allowed: errs.append("actual_allocation_allowed")
    return errs

def validate_optimizer_objective_contract_safety(contract: OptimizerObjectiveContract) -> List[str]:
    errs = []
    if contract.produces_actual_target_weight: errs.append("produces_actual_target_weight")
    return errs

def validate_optimizer_constraint_contract_safety(contract: OptimizerConstraintContract) -> List[str]:
    errs = []
    if contract.produces_actual_target_weight: errs.append("produces_actual_target_weight")
    return errs

def validate_optimizer_results_safety(items: List[OptimizerSandboxResult]) -> List[str]:
    errs = []
    for i in items:
        if i.actual_target_weight is not None: errs.append("actual_target_weight not None")
        if i.order_size is not None: errs.append("order_size not None")
    return errs

def validate_objective_comparison_report_safety(report: ObjectiveComparisonReport) -> List[str]:
    errs = []
    if report.investment_advice: errs.append("investment_advice")
    return errs

def validate_optimizer_safety_boundary_safety(boundary: OptimizerSafetyBoundaryResult) -> List[str]:
    return [] if boundary.boundary_passed else ["Safety boundary failed"]

def validate_phase157_readiness_gate_safety(gate: Phase157ReadinessGate) -> List[str]:
    return [] if gate.ready_for_phase157 else ["Phase 157 gate failed"]


def optimizer_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    return any(w in t for w in ["buy_signal", "sell_signal", "sent_to_broker", "actual target weight", "capital deployment", "guaranteed profit"])

def optimizer_payload_has_forbidden_fields(payload: Dict[str, Any]) -> bool:
    return bool(detect_forbidden_optimizer_fields(payload))

def collect_optimizer_risk_flags(context: Optional[OptimizerPrototypeContext] = None) -> List[OptimizerPrototypeRiskFlag]:
    flags = []
    if context:
        if context.actual_target_weights_produced: flags.append(OptimizerPrototypeRiskFlag.ACTUAL_TARGET_WEIGHT_RISK)
        if context.investment_advice: flags.append(OptimizerPrototypeRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK)
    return flags

def optimizer_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors": len(errors)}

def optimizer_safety_to_text(errors: List[str]) -> str:
    return str(errors)
