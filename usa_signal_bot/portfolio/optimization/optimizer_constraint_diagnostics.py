from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerDiagnosticRecord, OptimizerSandboxResult, OptimizerPolicy, OptimizerDiagnosticKind

def build_optimizer_constraint_diagnostics(results: List[OptimizerSandboxResult], policy: OptimizerPolicy) -> List[OptimizerDiagnosticRecord]:
    return [
        OptimizerDiagnosticRecord(
            diagnostic_kind=OptimizerDiagnosticKind.CONSTRAINT_BREACH_COUNT,
            value=count_optimizer_constraint_breaches(results, policy),
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True
        )
    ]

def count_optimizer_constraint_breaches(results: List[OptimizerSandboxResult], policy: OptimizerPolicy) -> int:
    return sum(1 for r in results if (r.normalized_sandbox_optimizer_weight or 0.0) > policy.max_sandbox_optimizer_weight)

def validate_optimizer_constraint_diagnostics(items: List[OptimizerDiagnosticRecord]) -> List[str]:
    return ["Missing research sandbox only"] if any(not i.research_sandbox_only for i in items) else []

def optimizer_constraint_diagnostics_summary(items: List[OptimizerDiagnosticRecord]) -> Dict[str, Any]:
    return {"count": len(items)}
