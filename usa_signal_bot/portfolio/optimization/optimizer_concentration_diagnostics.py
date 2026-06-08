from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerDiagnosticRecord, OptimizerSandboxResult, OptimizerPolicy, OptimizerDiagnosticKind

def build_optimizer_concentration_diagnostics(results: List[OptimizerSandboxResult], policy: OptimizerPolicy) -> List[OptimizerDiagnosticRecord]:
    return [
        OptimizerDiagnosticRecord(
            diagnostic_kind=OptimizerDiagnosticKind.TOP_N_CONCENTRATION,
            value=calculate_optimizer_top_n_concentration(results),
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True
        )
    ]

def calculate_optimizer_top_n_concentration(results: List[OptimizerSandboxResult], n: int = 5) -> float:
    weights = sorted([r.normalized_sandbox_optimizer_weight or 0.0 for r in results], reverse=True)
    return sum(weights[:n])

def validate_optimizer_concentration_diagnostics(items: List[OptimizerDiagnosticRecord]) -> List[str]:
    return ["Missing research sandbox only"] if any(not i.research_sandbox_only for i in items) else []

def optimizer_concentration_diagnostics_summary(items: List[OptimizerDiagnosticRecord]) -> Dict[str, Any]:
    return {"count": len(items)}
