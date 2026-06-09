content = """
from typing import Any, Dict, List
import hashlib

from usa_signal_bot.integration.phase158_models import (
    E2ERehearsalPlan, E2ERehearsalScenario, E2ERehearsalScenarioKind,
    SystemArtifactInventory, IntegrationDependencyGraph
)

def build_e2e_rehearsal_plan(inventory: SystemArtifactInventory, graph: IntegrationDependencyGraph) -> E2ERehearsalPlan:
    plan = E2ERehearsalPlan()
    plan.scenarios = build_default_e2e_rehearsal_scenarios()
    plan.scenario_count = len(plan.scenarios)
    plan.plan_hash = compute_e2e_rehearsal_plan_hash(plan)
    plan.plan_valid = len(validate_e2e_rehearsal_plan(plan)) == 0
    return plan

def build_default_e2e_rehearsal_scenarios() -> List[E2ERehearsalScenario]:
    kinds = [
        E2ERehearsalScenarioKind.CONFIG_LOAD_REHEARSAL,
        E2ERehearsalScenarioKind.DATA_PROVIDER_DRY_RUN_REHEARSAL,
        E2ERehearsalScenarioKind.FEATURE_ENGINE_DRY_RUN_REHEARSAL,
        E2ERehearsalScenarioKind.REGIME_CLASSIFICATION_DRY_RUN_REHEARSAL,
        E2ERehearsalScenarioKind.ML_GOVERNANCE_DRY_RUN_REHEARSAL,
        E2ERehearsalScenarioKind.BACKTEST_CLOSURE_DRY_RUN_REHEARSAL,
        E2ERehearsalScenarioKind.PORTFOLIO_GOVERNANCE_DRY_RUN_REHEARSAL,
        E2ERehearsalScenarioKind.NOTIFICATION_PREVIEW_DRY_RUN_REHEARSAL,
        E2ERehearsalScenarioKind.QUALITY_OBSERVABILITY_DRY_RUN_REHEARSAL,
        E2ERehearsalScenarioKind.FULL_CHAIN_DRY_RUN_REHEARSAL
    ]

    scenarios = []
    for kind in kinds:
        scenarios.append(E2ERehearsalScenario(
            scenario_kind=kind,
            name=kind.value.replace("_", " ").title(),
            forbidden_actions=["network", "broker", "telegram", "mutation", "deployment"]
        ))
    return scenarios

def compute_e2e_rehearsal_plan_hash(plan: E2ERehearsalPlan) -> str:
    h = hashlib.sha256()
    for sc in plan.scenarios:
        h.update(sc.scenario_id.encode('utf-8'))
    return h.hexdigest()

def validate_e2e_rehearsal_plan(plan: E2ERehearsalPlan) -> List[str]:
    violations = []
    if not plan.dry_run:
        violations.append("Plan must be in dry-run mode.")
    if not plan.local_fixture_only:
        violations.append("Plan must use local fixtures only.")
    for sc in plan.scenarios:
        if not sc.dry_run or not sc.local_fixture_only:
            violations.append(f"Scenario {sc.name} is not fully restricted.")
    return violations

def e2e_rehearsal_plan_to_text(plan: E2ERehearsalPlan, limit: int = 300) -> str:
    text = f"E2E Rehearsal Plan with {plan.scenario_count} scenarios. Valid: {plan.plan_valid}"
    return text[:limit] + "..." if len(text) > limit else text
"""

with open("usa_signal_bot/integration/e2e_rehearsal_plan.py", "w") as f:
    f.write(content)

content_exec = """
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
"""

with open("usa_signal_bot/integration/dry_run_rehearsal_executor.py", "w") as f:
    f.write(content_exec)

content_result = """
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
"""

with open("usa_signal_bot/integration/acceptance_rehearsal_result.py", "w") as f:
    f.write(content_result)
