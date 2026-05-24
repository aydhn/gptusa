from typing import Any, Dict, List, Optional
from usa_signal_bot.runtime_service_graph.phase103_models import (
    RuntimeServiceGraph,
    SafeOrchestrationPlan,
    OrchestrationDryRunResult
)
from usa_signal_bot.runtime_service_graph.orchestration_plan_builder import build_safe_orchestration_plan
from usa_signal_bot.runtime_service_graph.orchestration_dry_run import run_orchestration_dry_run

class SafeExecutionOrchestrationShell:
    def __init__(self, graph: Optional[RuntimeServiceGraph] = None, policy: Optional[Dict[str, Any]] = None):
        self.graph = graph
        self.policy = policy or {}

    def build_plan(self) -> SafeOrchestrationPlan:
        if not self.graph:
            raise ValueError("Graph not provided")
        return build_safe_orchestration_plan(self.graph)

    def dry_run(self, plan: Optional[SafeOrchestrationPlan] = None) -> OrchestrationDryRunResult:
        run_plan = plan or self.build_plan()
        return run_orchestration_dry_run(run_plan)

    def validate_shell_safety(self) -> List[str]:
        errors = []
        if self.policy.get("execution_allowed", False):
            errors.append("Shell policy allows execution")
        return errors

    def shell_summary(self) -> Dict[str, Any]:
        return {
            "has_graph": self.graph is not None,
            "policy": self.policy
        }
