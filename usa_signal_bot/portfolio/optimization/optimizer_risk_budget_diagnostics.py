from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerDiagnosticRecord, OptimizerSandboxResult, OptimizerSandboxCandidate, OptimizerPolicy, OptimizerDiagnosticKind

def build_optimizer_risk_budget_diagnostics(results: List[OptimizerSandboxResult], candidates: List[OptimizerSandboxCandidate], policy: OptimizerPolicy) -> List[OptimizerDiagnosticRecord]:
    return [
        OptimizerDiagnosticRecord(
            diagnostic_kind=OptimizerDiagnosticKind.RISK_BUDGET_USAGE,
            value=estimate_optimizer_risk_budget_usage(results, candidates),
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True
        )
    ]

def estimate_optimizer_risk_budget_usage(results: List[OptimizerSandboxResult], candidates: List[OptimizerSandboxCandidate]) -> Dict[str, Any]:
    # Mock return
    return {"total_usage": 0.15}

def validate_optimizer_risk_budget_diagnostics(items: List[OptimizerDiagnosticRecord]) -> List[str]:
    return ["Missing research sandbox only"] if any(not i.research_sandbox_only for i in items) else []

def optimizer_risk_budget_diagnostics_summary(items: List[OptimizerDiagnosticRecord]) -> Dict[str, Any]:
    return {"count": len(items)}
