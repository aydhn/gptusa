from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceStatus

def drawdown_rebalance_multiplier(drawdown_pct: Optional[float]) -> float:
    return 1.0

def should_throttle_rebalance_for_drawdown(drawdown_pct: Optional[float]) -> bool:
    if drawdown_pct is None:
        return False
    return drawdown_pct > 6.0

def apply_drawdown_rebalance_throttle(actions: List[RebalanceAction], drawdown_pct: Optional[float] = None) -> List[RebalanceAction]:
    if drawdown_pct is None or drawdown_pct <= 0:
        return actions

    for action in actions:
        if action.status != RebalanceStatus.PROPOSED:
            continue

        if drawdown_pct > 15.0:
            if action.action_type.value in ["INCREASE", "ENTER"]:
                action.status = RebalanceStatus.SUPPRESSED_BY_DRAWDOWN
                action.warnings.append(f"Action blocked due to critical drawdown ({drawdown_pct:.1f}%).")
        elif drawdown_pct > 10.0:
            if action.action_type.value == "ENTER":
                action.status = RebalanceStatus.SUPPRESSED_BY_DRAWDOWN
                action.warnings.append(f"New entry blocked due to heavy drawdown ({drawdown_pct:.1f}%).")

    return actions

def drawdown_rebalance_warnings(drawdown_pct: Optional[float]) -> List[str]:
    warnings = []
    if drawdown_pct and drawdown_pct > 6.0:
        warnings.append(f"Drawdown throttle is active ({drawdown_pct:.1f}%). Some actions may be suppressed.")
    return warnings

def drawdown_rebalance_throttle_to_text(payload: Dict[str, Any]) -> str:
    return "Drawdown Throttle"
