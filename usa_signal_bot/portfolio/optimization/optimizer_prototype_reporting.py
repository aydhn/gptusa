from typing import Any, Dict, List
from usa_signal_bot.portfolio.optimization.phase156_models import (
    PortfolioConstructionIngestionResult, OptimizerInputReference, OptimizerSandboxCandidate, OptimizerPolicy,
    OptimizerObjectiveContract, OptimizerConstraintContract, OptimizerSandboxResult, OptimizerObjectiveScore,
    ObjectiveComparisonReport, OptimizerDiagnosticRecord, OptimizerValidationReport, OptimizerSafetyBoundaryResult,
    Phase157ReadinessGate, OptimizerPrototypeContext, OptimizerPrototypeFullReview
)
from usa_signal_bot.portfolio.optimization.optimizer_prototype_report import optimizer_prototype_limitations_text

def portfolio_construction_ingestion_result_to_text(item: PortfolioConstructionIngestionResult) -> str: return f"Valid: {item.valid_for_phase156}"
def optimizer_input_reference_to_text(item: OptimizerInputReference) -> str: return f"Available: {item.available}"
def optimizer_candidate_to_text(item: OptimizerSandboxCandidate, limit: int = 300) -> str: return str(item.to_dict())[:limit]
def optimizer_policy_to_text(item: OptimizerPolicy, limit: int = 300) -> str: return str(item.to_dict())[:limit]
def optimizer_objective_contracts_to_text(items: List[OptimizerObjectiveContract], limit: int = 300) -> str: return str([i.to_dict() for i in items])[:limit]
def optimizer_constraint_contracts_to_text(items: List[OptimizerConstraintContract], limit: int = 300) -> str: return str([i.to_dict() for i in items])[:limit]
def optimizer_results_to_text(items: List[OptimizerSandboxResult], limit: int = 300) -> str: return str([i.to_dict() for i in items])[:limit]
def optimizer_objective_scores_to_text(items: List[OptimizerObjectiveScore], limit: int = 300) -> str: return str([i.to_dict() for i in items])[:limit]
def objective_comparison_report_to_text(item: ObjectiveComparisonReport, limit: int = 300) -> str: return str(item.to_dict())[:limit]
def optimizer_diagnostics_to_text(items: List[OptimizerDiagnosticRecord], limit: int = 300) -> str: return str([i.to_dict() for i in items])[:limit]
def optimizer_validation_report_to_text(item: OptimizerValidationReport, limit: int = 300) -> str: return str(item.to_dict())[:limit]
def optimizer_safety_boundary_to_text(item: OptimizerSafetyBoundaryResult, limit: int = 300) -> str: return str(item.to_dict())[:limit]
def phase157_readiness_gate_to_text(item: Phase157ReadinessGate, limit: int = 300) -> str: return str(item.to_dict())[:limit]
def optimizer_prototype_context_to_text(item: OptimizerPrototypeContext, limit: int = 300) -> str: return str(item.to_dict())[:limit]
def optimizer_prototype_full_review_to_text(item: OptimizerPrototypeFullReview, limit: int = 300) -> str: return str(item.to_dict())[:limit]
def optimizer_prototype_store_summary_to_text(summary: Dict[str, Any]) -> str: return str(summary)

# Alias for external use
optimizer_prototype_limitations_text = optimizer_prototype_limitations_text
