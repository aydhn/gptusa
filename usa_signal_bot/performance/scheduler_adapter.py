from typing import Dict, Any, Optional
from usa_signal_bot.performance.baseline_models import CurrentPerformanceSample
from usa_signal_bot.performance.baseline_collectors import normalize_scheduler_result_to_sample
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult
from usa_signal_bot.core.enums import BaselineComparisonStatus

def performance_sample_from_scheduler_run(payload: Dict[str, Any]) -> CurrentPerformanceSample:
    return normalize_scheduler_result_to_sample(payload)

def scheduler_hints_from_performance_gate(result: PerformanceAcceptanceGateResult) -> Dict[str, Any]:
    hints = {
        "action": "PROCEED",
        "delay_minutes": 0,
        "reason": None
    }

    if result.status == BaselineComparisonStatus.BLOCKED:
        hints["action"] = "BLOCK"
        hints["delay_minutes"] = 120
        hints["reason"] = "Performance BLOCKED. Temporarily suspending scheduler dispatch."
    elif result.status == BaselineComparisonStatus.FAIL:
        hints["action"] = "DELAY"
        hints["delay_minutes"] = 60
        hints["reason"] = "Performance FAIL. Delaying scheduler tasks to clear local resources."
    elif result.status == BaselineComparisonStatus.WARN:
        hints["action"] = "REVIEW"
        hints["reason"] = "Performance WARN. Proceeding but logged for operator review."

    return hints

def annotate_scheduler_plan_with_performance_gate(plan: Any, gate_result: PerformanceAcceptanceGateResult) -> Any:
    try:
        if not hasattr(plan, 'metadata'):
            plan.metadata = {}

        hints = scheduler_hints_from_performance_gate(gate_result)
        plan.metadata["performance_hints"] = hints
        plan.metadata["performance_gate_status"] = gate_result.status.value
    except Exception:
        pass
    return plan

def scheduler_performance_adapter_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Scheduler Performance Adapter Summary:\n{summary}"
