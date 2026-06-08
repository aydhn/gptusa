from typing import Any
import pandas
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioInputReference, CandidateUniverseContract, PortfolioEligibilityRule,
    PortfolioConstraintCatalog, RiskBudgetContract, PositionSizingBoundaryContract,
    PortfolioConstructionBoundary, PortfolioFoundationContext
)

def validate_portfolio_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_portfolio_columns(columns)

def validate_no_forbidden_portfolio_columns(columns: list[str]) -> list[str]:
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "portfolio_weight",
        "target_weight", "allocation", "capital_allocation", "position_size",
        "order_size", "real_order", "live_signal", "buy_signal", "sell_signal",
        "recommended_weight", "production_patch"
    ]
    detected = [c for c in columns if c in forbidden]
    if detected:
        return [f"Forbidden portfolio columns detected: {detected}"]
    return []

def validate_portfolio_input_reference_schema(item: PortfolioInputReference) -> list[str]:
    return validate_no_forbidden_portfolio_columns(item.columns)

def validate_candidate_universe_contract_schema(item: CandidateUniverseContract) -> list[str]:
    return []

def validate_eligibility_rules_schema(items: list[PortfolioEligibilityRule]) -> list[str]:
    return []

def validate_constraint_catalog_schema(item: PortfolioConstraintCatalog) -> list[str]:
    return []

def validate_risk_budget_contract_schema(item: RiskBudgetContract) -> list[str]:
    return []

def validate_position_sizing_boundary_schema(item: PositionSizingBoundaryContract) -> list[str]:
    return []

def validate_portfolio_construction_boundary_schema(item: PortfolioConstructionBoundary) -> list[str]:
    return []

def validate_portfolio_foundation_context_schema(context: PortfolioFoundationContext) -> list[str]:
    errors = []
    for ref in context.input_references:
        errors.extend(validate_portfolio_input_reference_schema(ref))
    return errors

def portfolio_foundation_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def portfolio_foundation_schema_to_text(errors: list[str]) -> str:
    if not errors:
        return "Schema Valid"
    return "Schema Errors:\n" + "\n".join(f"- {e}" for e in errors)
