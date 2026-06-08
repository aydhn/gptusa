from typing import Any
from usa_signal_bot.portfolio.sizing.phase154_models import (
    PortfolioFoundationIngestionResult, SizingInputReference, SizingCandidate,
    SizingPolicy, SizingMethodContract, SizingPrototypeResult, SizingCapFloorRule,
    SizingComparisonMatrix, SizingDiagnosticRecord, SizingSensitivityReport,
    RiskBudgetAdherenceReport, SizingSafetyBoundaryResult, Phase155ReadinessGate,
    SizingPrototypeContext, SizingPrototypeFullReview
)
from usa_signal_bot.portfolio.sizing.portfolio_foundation_ingestion import portfolio_foundation_ingestion_to_text
from usa_signal_bot.portfolio.sizing.sizing_input_resolver import sizing_input_resolver_to_text
from usa_signal_bot.portfolio.sizing.sizing_policy import sizing_policy_to_text
from usa_signal_bot.portfolio.sizing.sizing_method_contracts import sizing_method_contracts_to_text
from usa_signal_bot.portfolio.sizing.fixed_fractional_sizing import fixed_fractional_sizing_to_text
from usa_signal_bot.portfolio.sizing.sizing_cap_floor_rules import sizing_cap_floor_rules_to_text
from usa_signal_bot.portfolio.sizing.sizing_comparison_matrix import sizing_comparison_matrix_to_text
from usa_signal_bot.portfolio.sizing.sizing_diagnostics import sizing_diagnostics_to_text
from usa_signal_bot.portfolio.sizing.sizing_sensitivity_report import sizing_sensitivity_report_to_text
from usa_signal_bot.portfolio.sizing.risk_budget_adherence_report import risk_budget_adherence_report_to_text
from usa_signal_bot.portfolio.sizing.sizing_safety_boundary import sizing_safety_boundary_to_text
from usa_signal_bot.portfolio.sizing.phase155_readiness_gate import phase155_readiness_gate_to_text
from usa_signal_bot.portfolio.sizing.sizing_prototype_report import sizing_prototype_full_review_to_text, sizing_prototype_limitations_text

def portfolio_foundation_ingestion_result_to_text(item: PortfolioFoundationIngestionResult) -> str:
    return portfolio_foundation_ingestion_to_text(item)

def sizing_input_reference_to_text(item: SizingInputReference) -> str:
    return f"SizingInputRef(id={item.input_ref_id}, kind={item.input_kind.value})"

def sizing_candidate_to_text(item: SizingCandidate, limit: int = 300) -> str:
    return f"SizingCandidate(symbol={item.symbol}, valid={item.candidate_valid})"[:limit]

# Re-exports or wrappers
def sizing_prototype_results_to_text(items: list[SizingPrototypeResult], limit: int = 300) -> str:
    return f"SizingPrototypeResults: {len(items)}"[:limit]

def sizing_prototype_context_to_text(item: SizingPrototypeContext, limit: int = 300) -> str:
    return f"SizingPrototypeContext(id={item.context_id}, ready={item.ready_for_phase155})"[:limit]

def sizing_prototype_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary}"
