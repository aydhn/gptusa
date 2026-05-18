from typing import Any
from datetime import datetime, timezone

from usa_signal_bot.core.enums import GateEvaluationMode
from usa_signal_bot.research_execution.execution_models import AcceptanceGateEvaluation, ResearchRun, create_acceptance_gate_evaluation_id

def evaluate_acceptance_gate(gate_payload: dict[str, Any], baseline: ResearchRun, candidate: ResearchRun, mode: GateEvaluationMode = GateEvaluationMode.PRELIMINARY) -> AcceptanceGateEvaluation:
    gate_type = gate_payload.get("gate_type", "unknown")

    if gate_type == "min_sample_size":
        return evaluate_min_sample_size_gate(gate_payload, candidate)
    elif gate_type == "oos_improvement":
        return evaluate_oos_improvement_gate(gate_payload, baseline, candidate)
    elif gate_type == "cost_robustness":
        return evaluate_cost_robustness_gate(gate_payload, candidate)
    elif gate_type == "drawdown_limit":
        return evaluate_drawdown_gate(gate_payload, baseline, candidate)
    else:
        return AcceptanceGateEvaluation(
            evaluation_id=create_acceptance_gate_evaluation_id(gate_type),
            gate_type=gate_type,
            gate_status="SKIPPED",
            evaluation_mode=mode,
            baseline_value=None,
            candidate_value=None,
            threshold=None,
            passed=None,
            explanation="Unsupported gate type.",
            warnings=["Gate type not supported by local evaluator."],
            errors=[]
        )

def evaluate_acceptance_gates(gates: list[dict[str, Any]], baseline: ResearchRun, candidate: ResearchRun) -> list[AcceptanceGateEvaluation]:
    return [evaluate_acceptance_gate(g, baseline, candidate) for g in gates]

def evaluate_min_sample_size_gate(gate_payload: dict[str, Any], candidate: ResearchRun) -> AcceptanceGateEvaluation:
    threshold = gate_payload.get("threshold", 30)
    c_val = candidate.metrics.get("trade_count")

    passed = False
    if c_val is not None and c_val >= threshold:
        passed = True

    return AcceptanceGateEvaluation(
        evaluation_id=create_acceptance_gate_evaluation_id("min_sample_size"),
        gate_type="min_sample_size",
        gate_status="PASS" if passed else "FAIL",
        evaluation_mode=GateEvaluationMode.PRELIMINARY,
        baseline_value=None,
        candidate_value=c_val,
        threshold=threshold,
        passed=passed,
        explanation=f"Required >={threshold} trades, got {c_val}.",
        warnings=["Insufficient sample size."] if not passed else [],
        errors=[]
    )

def evaluate_oos_improvement_gate(gate_payload: dict[str, Any], baseline: ResearchRun, candidate: ResearchRun) -> AcceptanceGateEvaluation:
    threshold = gate_payload.get("threshold", 0.0)
    b_val = baseline.metrics.get("walk_forward_pass_ratio")
    c_val = candidate.metrics.get("walk_forward_pass_ratio")

    passed = False
    if b_val is not None and c_val is not None:
        if c_val >= b_val * (1 + threshold):
            passed = True

    return AcceptanceGateEvaluation(
        evaluation_id=create_acceptance_gate_evaluation_id("oos_improvement"),
        gate_type="oos_improvement",
        gate_status="PASS" if passed else "FAIL",
        evaluation_mode=GateEvaluationMode.PRELIMINARY,
        baseline_value=b_val,
        candidate_value=c_val,
        threshold=threshold,
        passed=passed,
        explanation=f"Required {threshold*100}% improvement over baseline.",
        warnings=["Missing OOS metrics."] if (b_val is None or c_val is None) else [],
        errors=[]
    )

def evaluate_cost_robustness_gate(gate_payload: dict[str, Any], candidate: ResearchRun) -> AcceptanceGateEvaluation:
    threshold = gate_payload.get("threshold", 50.0)
    c_val = candidate.metrics.get("robustness_score")

    passed = False
    if c_val is not None and c_val >= threshold:
        passed = True

    return AcceptanceGateEvaluation(
        evaluation_id=create_acceptance_gate_evaluation_id("cost_robustness"),
        gate_type="cost_robustness",
        gate_status="PASS" if passed else "FAIL",
        evaluation_mode=GateEvaluationMode.PRELIMINARY,
        baseline_value=None,
        candidate_value=c_val,
        threshold=threshold,
        passed=passed,
        explanation=f"Required score >={threshold}, got {c_val}.",
        warnings=["Missing robustness score."] if c_val is None else [],
        errors=[]
    )

def evaluate_drawdown_gate(gate_payload: dict[str, Any], baseline: ResearchRun, candidate: ResearchRun) -> AcceptanceGateEvaluation:
    threshold = gate_payload.get("threshold", 20.0)
    c_val = candidate.metrics.get("max_drawdown_pct")

    passed = False
    if c_val is not None and c_val <= threshold:
        passed = True

    return AcceptanceGateEvaluation(
        evaluation_id=create_acceptance_gate_evaluation_id("drawdown_limit"),
        gate_type="drawdown_limit",
        gate_status="PASS" if passed else "FAIL",
        evaluation_mode=GateEvaluationMode.PRELIMINARY,
        baseline_value=baseline.metrics.get("max_drawdown_pct"),
        candidate_value=c_val,
        threshold=threshold,
        passed=passed,
        explanation=f"Max drawdown must be <={threshold}%, got {c_val}%.",
        warnings=["Missing drawdown metric."] if c_val is None else [],
        errors=[]
    )

def gate_evaluations_to_text(evaluations: list[AcceptanceGateEvaluation]) -> str:
    lines = ["--- ACCEPTANCE GATES (PRELIMINARY) ---"]
    for e in evaluations:
        lines.append(f"{e.gate_type}: {e.gate_status} (Candidate: {e.candidate_value}, Threshold: {e.threshold})")
        if e.explanation:
            lines.append(f"  > {e.explanation}")
    lines.append("\nNOTE: Gate PASS is NOT a live trading approval. This is an advisory preliminary check.")
    return "\n".join(lines)
