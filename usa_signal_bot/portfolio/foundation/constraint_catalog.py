from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioConstraintCatalog, PortfolioConstraint, PortfolioConstraintKind
)

def build_default_portfolio_constraint_catalog() -> PortfolioConstraintCatalog:
    catalog = PortfolioConstraintCatalog()

    constraints = [
        (PortfolioConstraintKind.LONG_ONLY_CONTRACT, "Long Only Contract", True),
        (PortfolioConstraintKind.NO_LEVERAGE_CONTRACT, "No Leverage Contract", True),
        (PortfolioConstraintKind.NO_SHORTING_CONTRACT, "No Shorting Contract", True),
        (PortfolioConstraintKind.NO_DERIVATIVES_CONTRACT, "No Derivatives Contract", True),
        (PortfolioConstraintKind.NO_MARGIN_CONTRACT, "No Margin Contract", True),
        (PortfolioConstraintKind.MAX_SINGLE_NAME_EXPOSURE_CONTRACT, "Max Single Name Exposure Metadata", False),
        (PortfolioConstraintKind.MAX_TURNOVER_CONTRACT, "Max Turnover Metadata", False),
        (PortfolioConstraintKind.MAX_DRAWDOWN_TOLERANCE_CONTRACT, "Max Drawdown Metadata", False),
        (PortfolioConstraintKind.MAX_COST_DRAG_CONTRACT, "Max Cost Drag Metadata", False),
        (PortfolioConstraintKind.MIN_LIQUIDITY_METADATA, "Min Liquidity Metadata", False)
    ]

    for kind, name, hard in constraints:
        c = PortfolioConstraint()
        c.constraint_kind = kind
        c.name = name
        c.hard_constraint = hard
        c.soft_constraint = not hard
        c.contract_only = True
        c.actual_weight_output = False
        c.actual_allocation_output = False
        catalog.constraints.append(c)

    catalog.constraint_count = len(catalog.constraints)
    catalog.catalog_valid = True

    return catalog

def build_portfolio_constraint_catalog_from_handoff(handoff_payload: dict[str, Any]) -> PortfolioConstraintCatalog:
    return build_default_portfolio_constraint_catalog()

def validate_portfolio_constraint_catalog(catalog: PortfolioConstraintCatalog) -> list[str]:
    errors = []
    if not catalog.contract_only:
        errors.append("Constraint catalog must be contract_only")
    if not catalog.no_actual_weights:
        errors.append("no_actual_weights must be True")
    if not catalog.no_actual_allocation:
        errors.append("no_actual_allocation must be True")
    for c in catalog.constraints:
        if c.actual_weight_output or c.actual_allocation_output:
            errors.append(f"Constraint {c.name} produces actual weight/allocation")
    return errors

def constraint_catalog_summary(catalog: PortfolioConstraintCatalog) -> dict[str, Any]:
    return {
        "constraint_count": catalog.constraint_count,
        "valid": catalog.catalog_valid
    }

def constraint_catalog_to_text(catalog: PortfolioConstraintCatalog, limit: int = 300) -> str:
    return f"ConstraintCatalog: {catalog.constraint_count} constraints, valid: {catalog.catalog_valid}"
