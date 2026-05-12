from typing import Dict, Any, Optional

from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample
from usa_signal_bot.performance.baseline_collectors import normalize_taskqueue_result_to_sample
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult
from usa_signal_bot.core.enums import BaselineComparisonStatus

def performance_sample_from_taskqueue_run(payload: Dict[str, Any]) -> CurrentPerformanceSample:
    return normalize_taskqueue_result_to_sample(payload)

def taskqueue_budget_adjustments_from_performance_gate(result: PerformanceAcceptanceGateResult) -> Dict[str, Any]:
    adjustments = {"cpu_budget_modifier": 1.0, "reason": None}

    if result.status == BaselineComparisonStatus.BLOCKED:
        adjustments["cpu_budget_modifier"] = 0.5
        adjustments["reason"] = "BLOCKED performance gate, reducing queue workload heavily."
    elif result.status == BaselineComparisonStatus.FAIL:
        adjustments["cpu_budget_modifier"] = 0.75
        adjustments["reason"] = "FAIL performance gate, throttling queue workload."
    elif result.status == BaselineComparisonStatus.WARN:
        adjustments["cpu_budget_modifier"] = 0.90
        adjustments["reason"] = "WARN performance gate, minor throttling applied."

    return adjustments

def annotate_taskqueue_plan_with_performance_baseline(plan: Any, baseline: Optional[Any], gate_result: Optional[PerformanceAcceptanceGateResult] = None) -> Any:
    # Safely annotate avoiding destructive modification
    try:
        if not hasattr(plan, 'metadata'):
            plan.metadata = {}

        if baseline:
            plan.metadata["performance_baseline_id"] = baseline.baseline_id

        if gate_result:
            adj = taskqueue_budget_adjustments_from_performance_gate(gate_result)
            plan.metadata["performance_gate_status"] = gate_result.status.value
            plan.metadata["budget_adjustments"] = adj

    except Exception:
        pass

    return plan

def taskqueue_performance_adapter_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Taskqueue Performance Adapter Summary:\n{summary}"
