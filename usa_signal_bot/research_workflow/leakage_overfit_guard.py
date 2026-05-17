from typing import Any, List
from .workflow_models import ExperimentPlan, AcceptanceGate, create_acceptance_gate_id
from ..core.enums import AcceptanceGateType, AcceptanceGateStatus

def leakage_risk_warnings(experiment_plan: ExperimentPlan) -> List[str]:
    warnings = []
    val_plan = experiment_plan.validation_plan
    if not val_plan.get("requires_oos", False):
        warnings.append("Missing OOS validation requirement.")
    return warnings

def overfit_risk_warnings(experiment_plan: ExperimentPlan) -> List[str]:
    warnings = []
    if len(experiment_plan.parameter_change_proposals) > 5:
        warnings.append("Too many parameter changes in a single experiment risk overfitting.")
    return warnings

def validate_experiment_has_oos_guard(experiment_plan: ExperimentPlan) -> AcceptanceGate:
    warnings = leakage_risk_warnings(experiment_plan)
    status = AcceptanceGateStatus.WARNING if warnings else AcceptanceGateStatus.PASS
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.NO_LEAKAGE),
        gate_type=AcceptanceGateType.NO_LEAKAGE,
        status=status,
        threshold=None,
        observed_value=None,
        description="Checks for OOS validation requirement",
        warnings=warnings,
        errors=[],
        metadata={}
    )

def validate_experiment_has_no_auto_apply(experiment_plan: ExperimentPlan) -> AcceptanceGate:
    errors = []
    if experiment_plan.allowed_for_auto_execution:
        errors.append("Experiment plan incorrectly allows auto execution.")
    for p in experiment_plan.parameter_change_proposals:
        if p.allowed_for_auto_apply:
            errors.append(f"Proposal {p.parameter_name} incorrectly allows auto apply.")

    status = AcceptanceGateStatus.FAIL if errors else AcceptanceGateStatus.PASS
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.MANUAL_REVIEW),
        gate_type=AcceptanceGateType.MANUAL_REVIEW,
        status=status,
        threshold=None,
        observed_value=None,
        description="Checks that auto apply/execute is disabled",
        warnings=[],
        errors=errors,
        metadata={}
    )

def apply_leakage_overfit_guards(experiment_plan: ExperimentPlan) -> ExperimentPlan:
    leakage_warnings = leakage_risk_warnings(experiment_plan)
    overfit_warnings = overfit_risk_warnings(experiment_plan)
    experiment_plan.warnings.extend(leakage_warnings + overfit_warnings)
    experiment_plan.acceptance_gates.append(validate_experiment_has_oos_guard(experiment_plan))
    experiment_plan.acceptance_gates.append(validate_experiment_has_no_auto_apply(experiment_plan))
    return experiment_plan

def leakage_overfit_guard_to_text(experiment_plan: ExperimentPlan) -> str:
    lines = [f"Leakage/Overfit Guard for {experiment_plan.experiment_id}:"]
    for w in experiment_plan.warnings:
        lines.append(f"  WARNING: {w}")
    for g in experiment_plan.acceptance_gates:
        if g.gate_type in [AcceptanceGateType.NO_LEAKAGE, AcceptanceGateType.MANUAL_REVIEW]:
            lines.append(f"  GATE [{g.gate_type.value}]: {g.status.value}")
    return "\n".join(lines)
