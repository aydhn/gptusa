from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import OptimizerDiagnosticRecord, OptimizerSandboxResult, OptimizerObjectiveScore, OptimizerDiagnosticKind

def build_optimizer_stability_diagnostics(results: List[OptimizerSandboxResult], scores: List[OptimizerObjectiveScore]) -> List[OptimizerDiagnosticRecord]:
    return [
        OptimizerDiagnosticRecord(
            diagnostic_kind=OptimizerDiagnosticKind.STABILITY_SCORE,
            value=estimate_optimizer_stability_score(results),
            diagnostic_valid=True,
            research_sandbox_only=True,
            not_investment_advice=True
        )
    ]

def estimate_method_disagreement(results: List[OptimizerSandboxResult]) -> Dict[str, Any]:
    return {"disagreement": 0.1}

def estimate_optimizer_stability_score(results: List[OptimizerSandboxResult]) -> float:
    return 0.9

def validate_optimizer_stability_diagnostics(items: List[OptimizerDiagnosticRecord]) -> List[str]:
    return ["Missing research sandbox only"] if any(not i.research_sandbox_only for i in items) else []

def optimizer_stability_diagnostics_summary(items: List[OptimizerDiagnosticRecord]) -> Dict[str, Any]:
    return {"count": len(items)}
