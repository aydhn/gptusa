from typing import Any, List, Optional
from .workflow_models import AcceptanceGate, create_acceptance_gate_id
from ..core.enums import AcceptanceGateType, AcceptanceGateStatus, ExperimentType, ExperimentScope

def build_min_sample_size_gate(threshold: int = 30) -> AcceptanceGate:
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.MIN_SAMPLE_SIZE),
        gate_type=AcceptanceGateType.MIN_SAMPLE_SIZE,
        status=AcceptanceGateStatus.NOT_EVALUATED,
        threshold=threshold,
        observed_value=None,
        description=f"Requires at least {threshold} samples",
        warnings=[],
        errors=[],
        metadata={}
    )

def build_oos_improvement_gate(metric_name: str = "net_pnl", min_improvement_pct: float = 0.0) -> AcceptanceGate:
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.OUT_OF_SAMPLE_IMPROVEMENT),
        gate_type=AcceptanceGateType.OUT_OF_SAMPLE_IMPROVEMENT,
        status=AcceptanceGateStatus.NOT_EVALUATED,
        threshold=min_improvement_pct,
        observed_value=None,
        description=f"OOS {metric_name} improvement must be > {min_improvement_pct}%",
        warnings=[],
        errors=[],
        metadata={"metric_name": metric_name}
    )

def build_walk_forward_stability_gate(min_pass_ratio: float = 0.60) -> AcceptanceGate:
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.WALK_FORWARD_STABILITY),
        gate_type=AcceptanceGateType.WALK_FORWARD_STABILITY,
        status=AcceptanceGateStatus.NOT_EVALUATED,
        threshold=min_pass_ratio,
        observed_value=None,
        description=f"WF window pass ratio must be >= {min_pass_ratio}",
        warnings=[],
        errors=[],
        metadata={}
    )

def build_cost_robustness_gate(max_cost_drag_pct: float = 50.0) -> AcceptanceGate:
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.COST_ROBUSTNESS),
        gate_type=AcceptanceGateType.COST_ROBUSTNESS,
        status=AcceptanceGateStatus.NOT_EVALUATED,
        threshold=max_cost_drag_pct,
        observed_value=None,
        description=f"Max cost drag must be <= {max_cost_drag_pct}%",
        warnings=[],
        errors=[],
        metadata={}
    )

def build_drawdown_reduction_gate(max_drawdown_worsening_pct: float = 0.0) -> AcceptanceGate:
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.DRAWDOWN_REDUCTION),
        gate_type=AcceptanceGateType.DRAWDOWN_REDUCTION,
        status=AcceptanceGateStatus.NOT_EVALUATED,
        threshold=max_drawdown_worsening_pct,
        observed_value=None,
        description=f"Drawdown worsening must be <= {max_drawdown_worsening_pct}%",
        warnings=[],
        errors=[],
        metadata={}
    )

def build_no_leakage_gate() -> AcceptanceGate:
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.NO_LEAKAGE),
        gate_type=AcceptanceGateType.NO_LEAKAGE,
        status=AcceptanceGateStatus.NOT_EVALUATED,
        threshold=None,
        observed_value=None,
        description="Must pass leakage/overfit checks",
        warnings=[],
        errors=[],
        metadata={}
    )

def build_manual_review_gate() -> AcceptanceGate:
    return AcceptanceGate(
        gate_id=create_acceptance_gate_id(AcceptanceGateType.MANUAL_REVIEW),
        gate_type=AcceptanceGateType.MANUAL_REVIEW,
        status=AcceptanceGateStatus.NOT_EVALUATED,
        threshold=None,
        observed_value=None,
        description="Requires manual research review",
        warnings=[],
        errors=[],
        metadata={}
    )

def default_acceptance_gates_for_experiment(experiment_type: ExperimentType, scope: ExperimentScope) -> List[AcceptanceGate]:
    return [
        build_min_sample_size_gate(),
        build_oos_improvement_gate(),
        build_walk_forward_stability_gate(),
        build_no_leakage_gate(),
        build_manual_review_gate()
    ]

def acceptance_gates_to_text(gates: List[AcceptanceGate]) -> str:
    return "\n".join([f"[{g.gate_type.value}] {g.description} - Status: {g.status.value}" for g in gates])
