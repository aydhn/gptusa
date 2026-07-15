from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    SandboxAllocationMethodContract,
    SandboxAllocationMethodKind,
    PortfolioConstructionPolicy,
    create_sandbox_allocation_method_contract_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def _build_equal_sandbox_contract() -> SandboxAllocationMethodContract:
    return SandboxAllocationMethodContract(
        contract_id=create_sandbox_allocation_method_contract_id(),
        created_at_utc=_now_str(),
        method_kind=SandboxAllocationMethodKind.EQUAL_SANDBOX_ALLOCATION,
        method_name="Equal Sandbox Allocation",
        enabled=True,
        deterministic=True,
        contract_only=True,
        produces_sandbox_prototype_weight=True,
        produces_actual_target_weight=False,
        produces_actual_portfolio_weight=False,
        produces_actual_allocation=False,
        produces_order_size=False,
        produces_capital_allocation=False,
        rationale="Distributes sandbox weights equally among eligible candidates.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"weight": 1.0}
    )

def _build_sizing_score_sandbox_contract(policy: PortfolioConstructionPolicy) -> SandboxAllocationMethodContract:
    return SandboxAllocationMethodContract(
        contract_id=create_sandbox_allocation_method_contract_id(),
        created_at_utc=_now_str(),
        method_kind=SandboxAllocationMethodKind.SIZING_SCORE_SANDBOX_ALLOCATION,
        method_name="Sizing Score Sandbox Allocation",
        enabled=policy.sizing_weight > 0,
        deterministic=True,
        contract_only=True,
        produces_sandbox_prototype_weight=True,
        produces_actual_target_weight=False,
        produces_actual_portfolio_weight=False,
        produces_actual_allocation=False,
        produces_order_size=False,
        produces_capital_allocation=False,
        rationale="Distributes sandbox weights proportional to normalized sizing scores.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"weight": policy.sizing_weight}
    )

def _build_risk_budget_sandbox_contract(policy: PortfolioConstructionPolicy) -> SandboxAllocationMethodContract:
    return SandboxAllocationMethodContract(
        contract_id=create_sandbox_allocation_method_contract_id(),
        created_at_utc=_now_str(),
        method_kind=SandboxAllocationMethodKind.RISK_BUDGET_SANDBOX_ALLOCATION,
        method_name="Risk Budget Sandbox Allocation",
        enabled=policy.risk_budget_weight > 0,
        deterministic=True,
        contract_only=True,
        produces_sandbox_prototype_weight=True,
        produces_actual_target_weight=False,
        produces_actual_portfolio_weight=False,
        produces_actual_allocation=False,
        produces_order_size=False,
        produces_capital_allocation=False,
        rationale="Distributes sandbox weights proportional to normalized risk budget scores.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"weight": policy.risk_budget_weight}
    )

def _build_robustness_sandbox_contract(policy: PortfolioConstructionPolicy) -> SandboxAllocationMethodContract:
    return SandboxAllocationMethodContract(
        contract_id=create_sandbox_allocation_method_contract_id(),
        created_at_utc=_now_str(),
        method_kind=SandboxAllocationMethodKind.ROBUSTNESS_SANDBOX_ALLOCATION,
        method_name="Robustness Sandbox Allocation",
        enabled=policy.robustness_weight > 0,
        deterministic=True,
        contract_only=True,
        produces_sandbox_prototype_weight=True,
        produces_actual_target_weight=False,
        produces_actual_portfolio_weight=False,
        produces_actual_allocation=False,
        produces_order_size=False,
        produces_capital_allocation=False,
        rationale="Distributes sandbox weights proportional to normalized robustness scores.",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"weight": policy.robustness_weight}
    )

def build_sandbox_allocation_method_contracts(policy: PortfolioConstructionPolicy) -> List[SandboxAllocationMethodContract]:
    return [
        _build_equal_sandbox_contract(),
        _build_sizing_score_sandbox_contract(policy),
        _build_risk_budget_sandbox_contract(policy),
        _build_robustness_sandbox_contract(policy)
    ]

def validate_sandbox_allocation_method_contracts(items: List[SandboxAllocationMethodContract]) -> List[str]:
    errors = []

    if not items:
        errors.append("No sandbox allocation method contracts provided.")
        return errors

    for item in items:
        if not item.produces_sandbox_prototype_weight:
            errors.append(f"Contract {item.method_name} must produce sandbox prototype weight.")

        if item.produces_actual_target_weight:
            errors.append(f"Contract {item.method_name} produces_actual_target_weight=True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK)
        if item.produces_actual_portfolio_weight:
            errors.append(f"Contract {item.method_name} produces_actual_portfolio_weight=True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_PORTFOLIO_WEIGHT_RISK)
        if item.produces_actual_allocation:
            errors.append(f"Contract {item.method_name} produces_actual_allocation=True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK)
        if item.produces_order_size:
            errors.append(f"Contract {item.method_name} produces_order_size=True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ORDER_SIZE_RISK)
        if item.produces_capital_allocation:
            errors.append(f"Contract {item.method_name} produces_capital_allocation=True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK)

    return errors

def sandbox_allocation_method_contracts_summary(items: List[SandboxAllocationMethodContract]) -> Dict[str, Any]:
    return {
        "count": len(items),
        "enabled_count": sum(1 for item in items if item.enabled),
        "method_names": [item.method_name for item in items]
    }

def sandbox_allocation_method_contracts_to_text(items: List[SandboxAllocationMethodContract], limit: int = 300) -> str:
    summary = sandbox_allocation_method_contracts_summary(items)
    return (
        f"Method Contracts: {summary['count']} total ({summary['enabled_count']} enabled)\n"
        f"Methods: {', '.join(summary['method_names'])}"
    )
