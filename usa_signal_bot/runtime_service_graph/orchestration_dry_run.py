from datetime import datetime, timezone
from typing import Any, Dict, List
from usa_signal_bot.runtime_service_graph.phase103_models import (
    SafeOrchestrationPlan,
    OrchestrationDryRunResult,
    create_orchestration_dry_run_result_id,
    validate_orchestration_dry_run_result
)
from usa_signal_bot.core.enums import RuntimeServiceGraphStatus, OrchestrationStepStatus

def run_orchestration_dry_run(plan: SafeOrchestrationPlan) -> OrchestrationDryRunResult:
    executed = 0
    blocked = 0
    skipped = 0

    for step in plan.steps:
        if step.status == OrchestrationStepStatus.SKIPPED_DISABLED:
            skipped += 1
        elif step.status == OrchestrationStepStatus.BLOCKED:
            blocked += 1
        else:
            executed += 1

    passed = blocked == 0 and len(plan.errors) == 0

    result = OrchestrationDryRunResult(
        result_id=create_orchestration_dry_run_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        plan_id=plan.plan_id,
        graph_id=plan.graph_id,
        status=RuntimeServiceGraphStatus.VALIDATED if passed else RuntimeServiceGraphStatus.FAILED,
        executed_step_count=executed,
        blocked_step_count=blocked,
        skipped_step_count=skipped,
        dry_run_only=True,
        metadata_only=True,
        execution_performed=False,
        network_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        scraping_used=False,
        dashboard_started=False,
        passed=passed,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

    validate_orchestration_dry_run_result(result)
    return result

def validate_dry_run_result_safety(result: OrchestrationDryRunResult) -> List[str]:
    errors = []
    if result.execution_performed: errors.append("Execution performed in dry run")
    if result.network_used: errors.append("Network used in dry run")
    if result.broker_used: errors.append("Broker used in dry run")
    return errors

def orchestration_dry_run_summary(result: OrchestrationDryRunResult) -> Dict[str, Any]:
    return {
        "passed": result.passed,
        "executed": result.executed_step_count
    }

def orchestration_dry_run_to_text(result: OrchestrationDryRunResult) -> str:
    return f"Dry run result: {result.passed} with {result.executed_step_count} executed steps."
