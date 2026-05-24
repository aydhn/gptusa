from typing import Any, Dict, List, Optional
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceGraph,
    SafeOrchestrationPlan,
    OrchestrationDryRunResult
)
from usa_signal_bot.core.enums import RuntimeServiceGraphRiskFlag

def collect_orchestration_risk_flags(
    graph: RuntimeServiceGraph,
    plan: Optional[SafeOrchestrationPlan] = None,
    result: Optional[OrchestrationDryRunResult] = None
) -> List[RuntimeServiceGraphRiskFlag]:
    flags = set()

    if graph.graph_has_cycles:
        flags.add(RuntimeServiceGraphRiskFlag.DEPENDENCY_CYCLE)
    if graph.missing_dependency_count > 0:
        flags.add(RuntimeServiceGraphRiskFlag.DEPENDENCY_MISSING)
    if graph.invalid_contract_count > 0:
        flags.add(RuntimeServiceGraphRiskFlag.DEPENDENCY_CONTRACT_INVALID)

    return list(flags)

def validate_orchestration_route_safety(
    graph: RuntimeServiceGraph,
    plan: Optional[SafeOrchestrationPlan] = None,
    result: Optional[OrchestrationDryRunResult] = None
) -> List[str]:
    errors = []

    if graph.broker_execution_enabled:
        errors.append("Broker execution enabled in graph")

    if plan and plan.execution_allowed:
        errors.append("Execution allowed in plan")

    if result and result.execution_performed:
        errors.append("Execution performed in result")

    return errors

def orchestration_has_blocking_flags(flags: List[RuntimeServiceGraphRiskFlag]) -> bool:
    blocking = {
        RuntimeServiceGraphRiskFlag.DEPENDENCY_CYCLE,
        RuntimeServiceGraphRiskFlag.EXECUTION_ROUTE_RISK,
        RuntimeServiceGraphRiskFlag.BROKER_ROUTE_RISK,
        RuntimeServiceGraphRiskFlag.PAPER_MUTATION_ROUTE_RISK
    }
    return any(f in blocking for f in flags)

def orchestration_safety_summary(flags: List[RuntimeServiceGraphRiskFlag]) -> Dict[str, Any]:
    return {
        "flags": [f.value for f in flags],
        "blocking": orchestration_has_blocking_flags(flags)
    }

def orchestration_safety_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Orchestration routes are safe."
    return f"Orchestration unsafe: {len(errors)} errors found."
