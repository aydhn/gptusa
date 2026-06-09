
from typing import Any, Dict, List
import hashlib

from usa_signal_bot.integration.phase158_models import AcceptanceRehearsalResult, E2ERehearsalPlan, DryRunExecutionStep, RehearsalStepStatus

def build_acceptance_rehearsal_result(plan: E2ERehearsalPlan, steps: List[DryRunExecutionStep]) -> AcceptanceRehearsalResult:
    result = AcceptanceRehearsalResult(plan=plan, execution_steps=steps)
    result.passed_count = sum(1 for s in steps if s.status == RehearsalStepStatus.PASSED)
    result.warning_count = sum(1 for s in steps if s.status == RehearsalStepStatus.WARNING)
    result.failed_count = sum(1 for s in steps if s.status == RehearsalStepStatus.FAILED)
    result.blocked_count = sum(1 for s in steps if s.status == RehearsalStepStatus.BLOCKED)

    result.result_hash = compute_acceptance_rehearsal_result_hash(result)
    result.result_valid = len(validate_acceptance_rehearsal_result(result)) == 0
    return result

def compute_acceptance_rehearsal_result_hash(result: AcceptanceRehearsalResult) -> str:
    h = hashlib.sha256()
    for step in result.execution_steps:
        h.update(step.step_id.encode('utf-8'))
    return h.hexdigest()

def validate_acceptance_rehearsal_result(result: AcceptanceRehearsalResult) -> List[str]:
    violations = []
    if result.failed_count > 0 or result.blocked_count > 0:
        violations.append("Acceptance rehearsal has failed or blocked steps.")
    for step in result.execution_steps:
        if step.executed_real_side_effect:
            violations.append("Real side effects detected.")
    return violations

def acceptance_rehearsal_result_summary(result: AcceptanceRehearsalResult) -> Dict[str, Any]:
    return {
        "passed": result.passed_count,
        "failed": result.failed_count,
        "valid": result.result_valid
    }

def acceptance_rehearsal_result_to_text(result: AcceptanceRehearsalResult, limit: int = 300) -> str:
    summary = acceptance_rehearsal_result_summary(result)
    text = f"Acceptance Result: {summary}"
    return text[:limit] + "..." if len(text) > limit else text
