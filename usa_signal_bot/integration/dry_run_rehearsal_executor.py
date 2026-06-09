
from typing import Any, Dict, List

from usa_signal_bot.integration.phase158_models import (
    E2ERehearsalPlan, E2ERehearsalScenario, DryRunExecutionStep,
    IntegrationBoundaryContract, RehearsalStepStatus
)

def execute_dry_run_rehearsal_plan(plan: E2ERehearsalPlan, boundary: IntegrationBoundaryContract) -> List[DryRunExecutionStep]:
    all_steps = []
    for scenario in plan.scenarios:
        if scenario.enabled:
            all_steps.extend(execute_dry_run_scenario(scenario, boundary))
    return all_steps

def execute_dry_run_scenario(scenario: E2ERehearsalScenario, boundary: IntegrationBoundaryContract) -> List[DryRunExecutionStep]:
    step = DryRunExecutionStep(
        scenario_id=scenario.scenario_id,
        step_name=f"Execute {scenario.name}",
        command_preview=build_dry_run_command_preview(scenario),
        status=RehearsalStepStatus.PASSED,
        dry_run=True,
        executed_real_side_effect=False,
        used_network=False,
        mutated_paper_state=False,
        sent_telegram=False,
        used_broker=False,
        created_order=False,
        deployed=False,
        output_summary=f"Dry run success for {scenario.name}"
    )
    return [step]

def build_dry_run_command_preview(scenario: E2ERehearsalScenario) -> str:
    return f"python -m usa_signal_bot execute_scenario --scenario {scenario.scenario_kind.value} --dry-run"

def validate_dry_run_execution_steps(steps: List[DryRunExecutionStep]) -> List[str]:
    violations = []
    for step in steps:
        if step.executed_real_side_effect: violations.append(f"Step {step.step_name} produced real side effects.")
        if step.used_network: violations.append(f"Step {step.step_name} used network.")
        if step.mutated_paper_state: violations.append(f"Step {step.step_name} mutated paper state.")
        if step.sent_telegram: violations.append(f"Step {step.step_name} sent a Telegram message.")
        if step.used_broker: violations.append(f"Step {step.step_name} used a real broker.")
        if step.created_order: violations.append(f"Step {step.step_name} created an order.")
        if step.deployed: violations.append(f"Step {step.step_name} executed a deployment.")
    return violations

def dry_run_rehearsal_executor_summary(steps: List[DryRunExecutionStep]) -> Dict[str, Any]:
    return {
        "total_steps": len(steps),
        "passed_steps": sum(1 for s in steps if s.status == RehearsalStepStatus.PASSED),
        "violations": len(validate_dry_run_execution_steps(steps))
    }

def dry_run_rehearsal_executor_to_text(steps: List[DryRunExecutionStep], limit: int = 300) -> str:
    summary = dry_run_rehearsal_executor_summary(steps)
    text = f"Dry Run Executor: {summary}"
    return text[:limit] + "..." if len(text) > limit else text
