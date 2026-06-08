from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    RiskBudgetContract, RiskBudgetContractItem, RiskBudgetContractKind
)

def build_default_risk_budget_contract() -> RiskBudgetContract:
    contract = RiskBudgetContract()

    kinds = [
        RiskBudgetContractKind.TOTAL_RISK_BUDGET_CONTRACT,
        RiskBudgetContractKind.PER_SYMBOL_RISK_BUDGET_CONTRACT,
        RiskBudgetContractKind.DRAWDOWN_RISK_BUDGET_CONTRACT,
        RiskBudgetContractKind.COST_RISK_BUDGET_CONTRACT,
        RiskBudgetContractKind.LIQUIDITY_RISK_BUDGET_CONTRACT,
        RiskBudgetContractKind.VOLATILITY_RISK_BUDGET_CONTRACT,
        RiskBudgetContractKind.TAIL_RISK_BUDGET_CONTRACT
    ]

    for kind in kinds:
        item = RiskBudgetContractItem()
        item.budget_kind = kind
        item.name = kind.value
        contract.items.append(item)

    contract.item_count = len(contract.items)
    contract.contract_valid = True

    return contract

def build_risk_budget_contract_from_risk_notes(risk_notes: list[dict[str, Any]] | None = None) -> RiskBudgetContract:
    return build_default_risk_budget_contract()

def validate_risk_budget_contract(contract: RiskBudgetContract) -> list[str]:
    errors = []
    if not contract.contract_only:
        errors.append("Risk budget contract must be contract_only")
    if not contract.no_capital_allocation:
        errors.append("no_capital_allocation must be True")
    if not contract.no_position_sizing:
        errors.append("no_position_sizing must be True")
    if not contract.no_target_weights:
        errors.append("no_target_weights must be True")
    if not contract.no_portfolio_optimization:
        errors.append("no_portfolio_optimization must be True")

    for item in contract.items:
        if item.actual_capital_allocation or item.actual_position_size:
            errors.append(f"Risk budget item {item.name} has active allocation/sizing")

    return errors

def risk_budget_contract_summary(contract: RiskBudgetContract) -> dict[str, Any]:
    return {
        "item_count": contract.item_count,
        "valid": contract.contract_valid
    }

def risk_budget_contract_to_text(contract: RiskBudgetContract, limit: int = 300) -> str:
    return f"RiskBudgetContract: {contract.item_count} items, valid: {contract.contract_valid}"
