
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
