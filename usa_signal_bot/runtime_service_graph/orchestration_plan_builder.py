from datetime import datetime, timezone
from typing import Any, Dict, List
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceGraph,
    SafeOrchestrationPlan,
    OrchestrationStep,
    create_orchestration_plan_id,
    create_orchestration_step_id,
    validate_safe_orchestration_plan
)
from usa_signal_bot.core.enums import OrchestrationDecision, OrchestrationMode, OrchestrationStepStatus
from usa_signal_bot.runtime_service_graph.orchestration_policy import resolve_orchestration_mode
from usa_signal_bot.runtime_service_graph.startup_order_planner import plan_startup_order

def build_orchestration_steps(graph: RuntimeServiceGraph, startup_order: List[str]) -> List[OrchestrationStep]:
    steps = []
    nodes_by_id = {n.service_id: n for n in graph.nodes}

    for idx, service_id in enumerate(startup_order):
        node = nodes_by_id.get(service_id)
        if not node:
            continue

        mode = resolve_orchestration_mode(node)
        status = OrchestrationStepStatus.PLANNED

        if mode == OrchestrationMode.EXECUTION_DISABLED:
            status = OrchestrationStepStatus.SKIPPED_DISABLED

        step = OrchestrationStep(
            step_id=create_orchestration_step_id(),
            service_id=node.service_id,
            service_name=node.service_name,
            order_index=idx,
            mode=mode,
            status=status,
            action="validate_metadata_contract",
            metadata_only=True,
            read_only=True,
            execution_allowed=False,
            network_allowed=False,
            broker_allowed=False,
            order_allowed=False,
            paper_mutation_allowed=False,
            telegram_real_send_allowed=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        steps.append(step)
    return steps

def build_safe_orchestration_plan(graph: RuntimeServiceGraph) -> SafeOrchestrationPlan:
    startup_order = plan_startup_order(graph)

    if not startup_order or not graph.graph_valid:
        return SafeOrchestrationPlan(
            plan_id=create_orchestration_plan_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            decision=OrchestrationDecision.BLOCK,
            mode=OrchestrationMode.EXECUTION_DISABLED,
            graph_id=graph.graph_id,
            steps=[],
            startup_order=[],
            dry_run_only=True,
            metadata_only=True,
            read_only=True,
            execution_allowed=False,
            network_allowed=False,
            broker_allowed=False,
            order_allowed=False,
            paper_mutation_allowed=False,
            telegram_real_send_allowed=False,
            scraping_allowed=False,
            dashboard_allowed=False,
            risk_flags=[],
            warnings=[],
            errors=["Graph invalid or cycles detected"],
            metadata={}
        )

    steps = build_orchestration_steps(graph, startup_order)

    plan = SafeOrchestrationPlan(
        plan_id=create_orchestration_plan_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        decision=OrchestrationDecision.BUILD_DRY_RUN_PLAN,
        mode=OrchestrationMode.METADATA_ONLY_DRY_RUN,
        graph_id=graph.graph_id,
        steps=steps,
        startup_order=startup_order,
        dry_run_only=True,
        metadata_only=True,
        read_only=True,
        execution_allowed=False,
        network_allowed=False,
        broker_allowed=False,
        order_allowed=False,
        paper_mutation_allowed=False,
        telegram_real_send_allowed=False,
        scraping_allowed=False,
        dashboard_allowed=False,
        risk_flags=[],
        warnings=[],
        errors=[],
        metadata={}
    )

    validate_safe_orchestration_plan(plan)
    return plan

def validate_orchestration_plan_safety(plan: SafeOrchestrationPlan) -> List[str]:
    errors = []
    if plan.execution_allowed: errors.append("Plan allows execution")
    if plan.network_allowed: errors.append("Plan allows network")
    if plan.broker_allowed: errors.append("Plan allows broker")
    return errors

def orchestration_plan_summary(plan: SafeOrchestrationPlan) -> Dict[str, Any]:
    return {
        "steps": len(plan.steps),
        "decision": plan.decision.value
    }

def orchestration_plan_to_text(plan: SafeOrchestrationPlan, limit: int = 300) -> str:
    return f"Plan {plan.plan_id} with {len(plan.steps)} steps."
