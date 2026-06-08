from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    SizingPrototypeIngestionResult,
    PortfolioConstructionInputReference,
    PortfolioSandboxCandidate,
    PortfolioConstructionPolicy,
    SandboxAllocationMethodContract,
    ConstraintAwareScore,
    SandboxAllocationResult,
    PrototypeExposureTable,
    PortfolioSandboxDiagnosticRecord,
    AllocationSandboxComparisonReport,
    PortfolioConstructionValidationReport,
    AllocationSandboxSafetyBoundaryResult,
    Phase156ReadinessGate,
    PortfolioConstructionContext,
    PortfolioConstructionFullReview
)
from usa_signal_bot.portfolio.construction.sizing_prototype_ingestion import sizing_prototype_ingestion_to_text
from usa_signal_bot.portfolio.construction.portfolio_construction_input_resolver import portfolio_construction_input_resolver_to_text
from usa_signal_bot.portfolio.construction.sandbox_candidate_builder import portfolio_sandbox_candidates_to_text
from usa_signal_bot.portfolio.construction.portfolio_construction_policy import portfolio_construction_policy_to_text
from usa_signal_bot.portfolio.construction.sandbox_allocation_method_contracts import sandbox_allocation_method_contracts_to_text
from usa_signal_bot.portfolio.construction.constraint_aware_scoring import constraint_aware_scores_to_text
from usa_signal_bot.portfolio.construction.equal_sandbox_allocation import equal_sandbox_allocation_to_text
from usa_signal_bot.portfolio.construction.prototype_exposure_table import prototype_exposure_table_to_text
from usa_signal_bot.portfolio.construction.diversification_diagnostics import diversification_diagnostics_summary
from usa_signal_bot.portfolio.construction.allocation_sandbox_comparison_report import allocation_sandbox_comparison_report_to_text
from usa_signal_bot.portfolio.construction.portfolio_construction_validation_report import portfolio_construction_validation_report_to_text
from usa_signal_bot.portfolio.construction.allocation_sandbox_safety_boundary import allocation_sandbox_safety_boundary_to_text
from usa_signal_bot.portfolio.construction.phase156_readiness_gate import phase156_readiness_gate_to_text
from usa_signal_bot.portfolio.construction.portfolio_construction_report import portfolio_construction_full_review_to_text, portfolio_construction_limitations_text

def sizing_prototype_ingestion_result_to_text(item: SizingPrototypeIngestionResult) -> str:
    return sizing_prototype_ingestion_to_text(item)

def construction_input_reference_to_text(item: PortfolioConstructionInputReference) -> str:
    return f"Input Ref: {item.source_artifact_name} ({item.input_kind.value})"

def portfolio_sandbox_candidate_to_text(item: PortfolioSandboxCandidate, limit: int = 300) -> str:
    return f"Candidate: {item.symbol} (Eligible: {item.eligible_for_sandbox})"

def sandbox_allocation_results_to_text(items: List[SandboxAllocationResult], limit: int = 300) -> str:
    return equal_sandbox_allocation_to_text(items, limit)

def portfolio_sandbox_diagnostics_to_text(items: List[PortfolioSandboxDiagnosticRecord], limit: int = 300) -> str:
    summary = diversification_diagnostics_summary(items)
    return f"Diagnostics: {summary['count']} items, Kinds: {', '.join(summary['kinds'])}"

def portfolio_construction_context_to_text(item: PortfolioConstructionContext, limit: int = 300) -> str:
    return (
        f"Context ID: {item.context_id}\n"
        f"Status: {item.status.value}\n"
        f"Ready for Phase 156: {item.ready_for_phase156}"
    )

def portfolio_construction_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return f"Store: {summary['reviews']} reviews."
