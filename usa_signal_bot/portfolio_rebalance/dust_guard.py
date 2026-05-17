from typing import Any, Dict, List
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceStatus

def is_dust_rebalance_action(action: RebalanceAction, min_trade_notional_usd: float) -> bool:
    if action.delta_notional_usd is None:
        return False
    return abs(action.delta_notional_usd) < min_trade_notional_usd

def suppress_dust_rebalance_actions(actions: List[RebalanceAction], min_trade_notional_usd: float) -> List[RebalanceAction]:
    for action in actions:
        if action.status.value != "PROPOSED":
            continue

        if is_dust_rebalance_action(action, min_trade_notional_usd):
            if action.action_type.value == "EXIT":
                # For tiny exits, we might still want to clean them up, but let's review
                action.warnings.append(f"Dust exit (${abs(action.delta_notional_usd or 0):.2f} < ${min_trade_notional_usd:.2f})")
            else:
                action.status = RebalanceStatus.SUPPRESSED_BY_COST
                action.warnings.append(f"Suppressed dust action (${abs(action.delta_notional_usd or 0):.2f} < ${min_trade_notional_usd:.2f})")

    return actions

def dust_guard_summary(actions: List[RebalanceAction]) -> Dict[str, Any]:
    suppressed = [a for a in actions if a.status == RebalanceStatus.SUPPRESSED_BY_COST and any("dust" in w.lower() for w in a.warnings)]
    return {
        "suppressed_count": len(suppressed),
        "symbols": [a.symbol for a in suppressed]
    }

def dust_guard_summary_to_text(summary: Dict[str, Any]) -> str:
    count = summary.get("suppressed_count", 0)
    return f"Dust Guard: Suppressed {count} tiny actions."
