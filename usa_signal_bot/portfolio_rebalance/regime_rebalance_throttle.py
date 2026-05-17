from typing import Any, Dict, List, Optional
from usa_signal_bot.portfolio_rebalance.rebalance_models import RebalanceAction
from usa_signal_bot.core.enums import RebalanceStatus

def regime_rebalance_throttle_multiplier(regime_payload: Optional[Dict[str, Any]] = None, transition_payload: Optional[Dict[str, Any]] = None) -> float:
    return 1.0

def should_throttle_rebalance_for_regime(regime_payload: Optional[Dict[str, Any]] = None, transition_payload: Optional[Dict[str, Any]] = None) -> bool:
    if transition_payload:
        if transition_payload.get("risk") in ["HIGH", "CRITICAL"]:
            return True

    if regime_payload:
        if regime_payload.get("breadth") == "RISK_OFF" or regime_payload.get("cross_sectional") == "RISK_OFF":
            return True

    return False

def apply_regime_rebalance_throttle(
    actions: List[RebalanceAction],
    regime_payload: Optional[Dict[str, Any]] = None,
    transition_payload: Optional[Dict[str, Any]] = None
) -> List[RebalanceAction]:

    if not should_throttle_rebalance_for_regime(regime_payload, transition_payload):
        return actions

    for action in actions:
        if action.status != RebalanceStatus.PROPOSED:
            continue

        # We generally allow exits even in bad regimes, but throttle increases
        if action.action_type.value in ["INCREASE", "ENTER"]:
            action.status = RebalanceStatus.SUPPRESSED_BY_REGIME
            action.warnings.append("Increase/Enter action suppressed due to high regime transition risk or risk-off environment.")

    return actions

def regime_rebalance_warnings(regime_payload: Optional[Dict[str, Any]] = None, transition_payload: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if should_throttle_rebalance_for_regime(regime_payload, transition_payload):
        warnings.append("Regime throttle is active: High transition risk or risk-off environment detected. Increases are suppressed.")
    return warnings

def regime_rebalance_throttle_to_text(payload: Dict[str, Any]) -> str:
    return "Regime Rebalance Throttle Active"
