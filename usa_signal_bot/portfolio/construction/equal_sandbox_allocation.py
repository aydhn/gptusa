from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    SandboxAllocationResult,
    SandboxAllocationMethodKind,
    PortfolioSandboxCandidate,
    PortfolioConstructionPolicy,
    create_sandbox_allocation_result_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_equal_sandbox_allocation(
    candidates: List[PortfolioSandboxCandidate],
    policy: PortfolioConstructionPolicy
) -> List[SandboxAllocationResult]:

    results = []
    eligible = [c for c in candidates if c.eligible_for_sandbox]
    count = len(eligible)

    weight = 1.0 / count if count > 0 else 0.0

    for cand in candidates:
        is_eligible = cand.eligible_for_sandbox
        cand_weight = weight if is_eligible else 0.0

        results.append(SandboxAllocationResult(
            result_id=create_sandbox_allocation_result_id(),
            created_at_utc=_now_str(),
            symbol=cand.symbol,
            method_kind=SandboxAllocationMethodKind.EQUAL_SANDBOX_ALLOCATION,
            method_name="Equal Sandbox Allocation",
            raw_sandbox_score=1.0 if is_eligible else 0.0,
            sandbox_prototype_weight=cand_weight,
            normalized_sandbox_weight=None,
            group_sandbox_weight=None,
            constraint_penalty=None,
            cap_applied=False,
            floor_applied=False,
            zeroed_by_constraint=not is_eligible,
            result_valid=True,
            research_allocation_sandbox=True,
            actual_target_weight=None,
            actual_portfolio_weight=None,
            actual_allocation=None,
            actual_position_size=None,
            order_size=None,
            capital_allocation=None,
            live_signal=False,
            order_decision=False,
            not_investment_advice=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    return results

def validate_equal_sandbox_allocation(items: List[SandboxAllocationResult]) -> List[str]:
    errors = []

    for item in items:
        if item.actual_target_weight is not None:
            errors.append(f"Result {item.symbol} has actual_target_weight set.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_TARGET_WEIGHT_RISK)
        if item.actual_portfolio_weight is not None:
            errors.append(f"Result {item.symbol} has actual_portfolio_weight set.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_PORTFOLIO_WEIGHT_RISK)
        if item.actual_allocation is not None:
            errors.append(f"Result {item.symbol} has actual_allocation set.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_ALLOCATION_RISK)
        if item.actual_position_size is not None:
            errors.append(f"Result {item.symbol} has actual_position_size set.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ACTUAL_POSITION_SIZE_RISK)
        if item.order_size is not None:
            errors.append(f"Result {item.symbol} has order_size set.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.ORDER_SIZE_RISK)
        if item.capital_allocation is not None:
            errors.append(f"Result {item.symbol} has capital_allocation set.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.CAPITAL_DEPLOYMENT_RISK)
        if item.live_signal:
            errors.append(f"Result {item.symbol} has live_signal set to True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.LIVE_TRADING_RISK)
        if item.order_decision:
            errors.append(f"Result {item.symbol} has order_decision set to True.")
            item.risk_flags.append(PortfolioConstructionRiskFlag.REAL_ORDER_RISK)

    return errors

def equal_sandbox_allocation_summary(items: List[SandboxAllocationResult]) -> Dict[str, Any]:
    non_zero = [i for i in items if i.sandbox_prototype_weight is not None and i.sandbox_prototype_weight > 0]
    return {
        "count": len(items),
        "non_zero_count": len(non_zero),
        "weight_per_symbol": non_zero[0].sandbox_prototype_weight if non_zero else 0.0
    }

def equal_sandbox_allocation_to_text(items: List[SandboxAllocationResult], limit: int = 300) -> str:
    summary = equal_sandbox_allocation_summary(items)
    return (
        f"Equal Sandbox Allocation: {summary['count']} total\n"
        f"Allocated Symbols: {summary['non_zero_count']}\n"
        f"Weight: {summary['weight_per_symbol']:.4f}"
    )
