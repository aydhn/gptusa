from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    BacktestClosureIngestionResult, PortfolioInputReference, CandidateUniverseContract,
    PortfolioEligibilityRule, PortfolioConstraintCatalog, RiskBudgetContract,
    PositionSizingBoundaryContract, PortfolioConstructionBoundary, CandidateUniverseDiagnostics,
    ConstraintValidationReport, RiskBudgetValidationReport, SizingBoundaryValidationReport,
    PortfolioFoundationSafetyBoundaryResult, Phase154ReadinessGate, PortfolioFoundationContext,
    PortfolioFoundationFullReview
)
from usa_signal_bot.portfolio.foundation.portfolio_foundation_report import portfolio_foundation_limitations_text

def portfolio_foundation_store_summary_to_text(summary: dict[str, Any]) -> str:
    return str(summary)

# Re-export text formatting functions (aliasing to match existing definitions if any, or defining them here)
# All these can just delegate back to the ones defined in the actual modules or just use __str__ for brevity if needed.
