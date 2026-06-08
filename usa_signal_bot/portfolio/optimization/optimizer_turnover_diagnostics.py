from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerDiagnosticRecord, OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerDiagnosticKind

def build_optimizer_turnover_diagnostics(results: List[OptimizerSandboxResult], candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerDiagnosticRecord]:
    return [
        OptimizerDiagnosticRecord(
            diagnostic_kind=OptimizerDiagnosticKind.TURNOVER_SANDBOX_ESTIMATE,
            value=estimate_optimizer_turnover(results, candidates),
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True
        )
    ]

def estimate_optimizer_turnover(results: List[OptimizerSandboxResult], candidates: List[OptimizerSandboxCandidate]) -> float:
    return sum(abs((r.normalized_sandbox_optimizer_weight or 0.0) - 0.01) for r in results) # Mock

def validate_optimizer_turnover_diagnostics(items: List[OptimizerDiagnosticRecord]) -> List[str]:
    return ["Missing research sandbox only"] if any(not i.research_sandbox_only for i in items) else []

def optimizer_turnover_diagnostics_summary(items: List[OptimizerDiagnosticRecord]) -> Dict[str, Any]:
    return {"count": len(items)}
