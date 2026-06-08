from typing import Any, Dict, List
from usa_signal_bot.portfolio.construction.phase155_models import (
    SandboxAllocationResult,
    SandboxAllocationMethodKind,
    PortfolioSandboxCandidate,
    ConstraintAwareScore,
    ConstraintAwareScoreKind,
    PortfolioConstructionPolicy,
    create_sandbox_allocation_result_id,
    _now_str
)
from usa_signal_bot.core.enums import PortfolioConstructionRiskFlag

def build_risk_budget_sandbox_allocation(
    candidates: List[PortfolioSandboxCandidate],
    scores: List[ConstraintAwareScore],
    policy: PortfolioConstructionPolicy
) -> List[SandboxAllocationResult]:

    results = []

    budget_scores = {s.symbol: s for s in scores if s.score_kind == ConstraintAwareScoreKind.RISK_BUDGET_SCORE}

    for cand in candidates:
        is_eligible = cand.eligible_for_sandbox
        score_obj = budget_scores.get(cand.symbol)

        weight = score_obj.normalized_score if score_obj and is_eligible else 0.0

        results.append(SandboxAllocationResult(
            result_id=create_sandbox_allocation_result_id(),
            created_at_utc=_now_str(),
            symbol=cand.symbol,
            method_kind=SandboxAllocationMethodKind.RISK_BUDGET_SANDBOX_ALLOCATION,
            method_name="Risk Budget Sandbox Allocation",
            raw_sandbox_score=score_obj.raw_score if score_obj else None,
            sandbox_prototype_weight=weight,
            normalized_sandbox_weight=None,
            group_sandbox_weight=None,
            constraint_penalty=None,
            cap_applied=False,
            floor_applied=False,
            zeroed_by_constraint=not is_eligible or weight == 0,
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

def validate_risk_budget_sandbox_allocation(items: List[SandboxAllocationResult]) -> List[str]:
    from usa_signal_bot.portfolio.construction.equal_sandbox_allocation import validate_equal_sandbox_allocation
    return validate_equal_sandbox_allocation(items)

def risk_budget_sandbox_allocation_summary(items: List[SandboxAllocationResult]) -> Dict[str, Any]:
    non_zero = [i for i in items if i.sandbox_prototype_weight is not None and i.sandbox_prototype_weight > 0]
    return {
        "count": len(items),
        "non_zero_count": len(non_zero)
    }

def risk_budget_sandbox_allocation_to_text(items: List[SandboxAllocationResult], limit: int = 300) -> str:
    summary = risk_budget_sandbox_allocation_summary(items)
    return (
        f"Risk Budget Sandbox Allocation: {summary['count']} total\n"
        f"Allocated Symbols: {summary['non_zero_count']}"
    )
