from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioConstructionBoundary, PortfolioConstructionBoundaryKind
)

def build_portfolio_construction_boundary() -> PortfolioConstructionBoundary:
    boundary = PortfolioConstructionBoundary()

    boundary.boundary_kinds = [
        PortfolioConstructionBoundaryKind.CONTRACT_ONLY_PHASE153,
        PortfolioConstructionBoundaryKind.NO_OPTIMIZATION_PHASE153,
        PortfolioConstructionBoundaryKind.NO_REBALANCING_PHASE153,
        PortfolioConstructionBoundaryKind.NO_EXECUTION_PHASE153,
        PortfolioConstructionBoundaryKind.NO_DEPLOYMENT_PHASE153,
        PortfolioConstructionBoundaryKind.RESEARCH_ONLY_PHASE153
    ]

    boundary.boundary_valid = True
    return boundary

def validate_portfolio_construction_boundary(boundary: PortfolioConstructionBoundary) -> list[str]:
    errors = []
    if not boundary.contract_only_phase153:
        errors.append("contract_only_phase153 must be True")
    if not boundary.no_optimization_phase153:
        errors.append("no_optimization_phase153 must be True")
    if not boundary.no_rebalancing_phase153:
        errors.append("no_rebalancing_phase153 must be True")
    if not boundary.no_execution_phase153:
        errors.append("no_execution_phase153 must be True")
    if not boundary.no_deployment_phase153:
        errors.append("no_deployment_phase153 must be True")
    if not boundary.research_only_phase153:
        errors.append("research_only_phase153 must be True")
    return errors

def portfolio_construction_boundary_summary(boundary: PortfolioConstructionBoundary) -> dict[str, Any]:
    return {
        "kind_count": len(boundary.boundary_kinds),
        "valid": boundary.boundary_valid
    }

def portfolio_construction_boundary_to_text(boundary: PortfolioConstructionBoundary, limit: int = 300) -> str:
    return f"PortfolioConstructionBoundary: valid={boundary.boundary_valid}"
