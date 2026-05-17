import datetime
from typing import List, Optional
from datetime import timezone

from usa_signal_bot.core.enums import TurnoverStatus, RebalanceStatus
from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    RebalanceAction, TurnoverAssessment, create_turnover_assessment_id
)

def estimate_rebalance_turnover_usd(actions: List[RebalanceAction]) -> float:
    return sum(abs(a.delta_notional_usd) for a in actions if a.delta_notional_usd is not None and a.status in [RebalanceStatus.PROPOSED])

def estimate_rebalance_turnover_pct_equity(turnover_usd: float, total_equity_usd: Optional[float]) -> Optional[float]:
    if total_equity_usd and total_equity_usd > 0:
        return (turnover_usd / total_equity_usd) * 100.0
    return None

def classify_turnover_status(turnover_pct_equity: Optional[float], max_turnover_pct_equity: Optional[float]) -> TurnoverStatus:
    if turnover_pct_equity is None or max_turnover_pct_equity is None:
        return TurnoverStatus.INSUFFICIENT_DATA
    if turnover_pct_equity > max_turnover_pct_equity * 2.0:
        return TurnoverStatus.EXCESSIVE
    if turnover_pct_equity > max_turnover_pct_equity:
        return TurnoverStatus.HIGH
    if turnover_pct_equity > max_turnover_pct_equity * 0.75:
        return TurnoverStatus.WARNING
    return TurnoverStatus.ACCEPTABLE

def assess_turnover(actions: List[RebalanceAction], total_equity_usd: Optional[float], max_turnover_pct_equity: float) -> TurnoverAssessment:
    turnover_usd = estimate_rebalance_turnover_usd(actions)
    turnover_pct = estimate_rebalance_turnover_pct_equity(turnover_usd, total_equity_usd)
    status = classify_turnover_status(turnover_pct, max_turnover_pct_equity)

    proposed_count = sum(1 for a in actions if a.status == RebalanceStatus.PROPOSED)
    suppressed_count = sum(1 for a in actions if a.status == RebalanceStatus.REDUCED_BY_TURNOVER)

    warnings = []
    if status in [TurnoverStatus.HIGH, TurnoverStatus.EXCESSIVE]:
        warnings.append(f"Turnover {turnover_pct:.2f}% exceeds or heavily risks limit of {max_turnover_pct_equity}%")

    return TurnoverAssessment(
        assessment_id=create_turnover_assessment_id(),
        created_at_utc=datetime.datetime.now(timezone.utc).isoformat(),
        estimated_turnover_usd=turnover_usd,
        status=status,
        action_count=proposed_count,
        suppressed_action_count=suppressed_count,
        estimated_turnover_pct_equity=turnover_pct,
        max_turnover_pct_equity=max_turnover_pct_equity,
        warnings=warnings
    )

def suppress_actions_to_fit_turnover(
    actions: List[RebalanceAction],
    total_equity_usd: Optional[float],
    max_turnover_pct_equity: float
) -> List[RebalanceAction]:

    if not total_equity_usd or total_equity_usd <= 0:
        return actions

    max_turnover_usd = total_equity_usd * (max_turnover_pct_equity / 100.0)
    current_turnover = estimate_rebalance_turnover_usd(actions)

    if current_turnover <= max_turnover_usd:
        return actions

    # We need to reduce turnover. Sort actions by priority:
    # 1. EXITS (highest priority, we want to get out of things we shouldn't hold)
    # 2. Largest absolute delta (most important to align)

    def action_priority(action: RebalanceAction) -> tuple:
        is_exit = action.action_type == "EXIT"
        size = abs(action.delta_notional_usd) if action.delta_notional_usd else 0.0
        return (not is_exit, -size) # Lower tuple is higher priority

    sorted_actions = sorted([a for a in actions if a.status == RebalanceStatus.PROPOSED], key=action_priority)

    accumulated_turnover = 0.0
    for action in sorted_actions:
        action_size = abs(action.delta_notional_usd) if action.delta_notional_usd else 0.0

        if accumulated_turnover + action_size <= max_turnover_usd:
            accumulated_turnover += action_size
        else:
            action.status = RebalanceStatus.REDUCED_BY_TURNOVER
            action.warnings.append("Action suppressed to fit turnover cap.")

    return actions

def turnover_assessment_to_text(assessment: TurnoverAssessment) -> str:
    lines = [f"Turnover Assessment: {assessment.status.value}"]
    lines.append(f"  Estimated USD: ${assessment.estimated_turnover_usd:.2f}")
    if assessment.estimated_turnover_pct_equity is not None:
        lines.append(f"  Estimated %: {assessment.estimated_turnover_pct_equity:.2f}% (Limit: {assessment.max_turnover_pct_equity}%)")
    lines.append(f"  Actions: {assessment.action_count} proposed, {assessment.suppressed_action_count} suppressed")
    return "\n".join(lines)
