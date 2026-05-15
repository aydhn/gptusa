from typing import Optional, Dict, Any, List
from usa_signal_bot.core.enums import CostSessionRegime

def classify_cost_session_regime(session_type: Optional[Any] = None, timestamp: Optional[str] = None) -> CostSessionRegime:
    st = str(session_type).upper() if session_type else "REGULAR"
    if st == "CLOSED" or st == "HOLIDAY":
        return CostSessionRegime.CLOSED
    elif st == "PREMARKET":
        return CostSessionRegime.PREMARKET
    elif st == "AFTER_HOURS":
        return CostSessionRegime.AFTER_HOURS
    elif st == "OPENING_WINDOW":
        return CostSessionRegime.OPENING_WINDOW
    elif st == "CLOSING_WINDOW":
        return CostSessionRegime.CLOSING_WINDOW
    return CostSessionRegime.REGULAR

def session_cost_multiplier(regime: CostSessionRegime) -> float:
    mapping = {
        CostSessionRegime.REGULAR: 1.00,
        CostSessionRegime.OPENING_WINDOW: 1.40,
        CostSessionRegime.CLOSING_WINDOW: 1.25,
        CostSessionRegime.PREMARKET: 2.50,
        CostSessionRegime.AFTER_HOURS: 2.25,
        CostSessionRegime.CLOSED: 5.00,
        CostSessionRegime.HOLIDAY: 5.00,
        CostSessionRegime.UNKNOWN: 1.00,
    }
    return mapping.get(regime, 1.00)

def session_cost_warnings(regime: CostSessionRegime, evidence: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if regime in (CostSessionRegime.PREMARKET, CostSessionRegime.AFTER_HOURS):
        warnings.append(f"Extended hours session ({regime.value}). Execution realism is low.")
    elif regime in (CostSessionRegime.CLOSED, CostSessionRegime.HOLIDAY):
        warnings.append("Market closed. Simulation fills should be blocked.")
    return warnings

def session_regime_to_text(regime: CostSessionRegime, multiplier: Optional[float] = None) -> str:
    mult_text = f" (Multiplier: {multiplier:.2f})" if multiplier is not None else ""
    return f"Session Regime: {regime.value}{mult_text}"
