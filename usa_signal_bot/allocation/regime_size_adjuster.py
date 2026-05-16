from typing import Any, Dict, Optional, Tuple, List
from usa_signal_bot.core.enums import SizingAdjustmentReason
from usa_signal_bot.allocation.allocation_models import SizingAdjustment, create_sizing_adjustment_id

def regime_size_multiplier(regime_payload: Optional[Dict[str, Any]] = None) -> float:
    if regime_payload is None:
        return 1.0

    state = regime_payload.get("regime_state", "UNKNOWN")
    if state == "RISK_OFF":
        return 0.50
    elif state == "BULL_TREND":
        return 1.10

    return 1.0

def transition_risk_size_multiplier(transition_payload: Optional[Dict[str, Any]] = None) -> float:
    if transition_payload is None:
        return 1.0

    if transition_payload.get("is_high_risk", False):
        return 0.50

    return 1.0

def alignment_size_multiplier(alignment_payload: Optional[Dict[str, Any]] = None) -> float:
    if alignment_payload is None:
        return 1.0

    status = alignment_payload.get("status", "UNKNOWN")
    if status == "BLOCK_SIGNAL":
        return 0.0
    elif status == "CONFLICTED":
        return 0.25

    return 1.0

def apply_regime_size_adjustment(notional_usd: Optional[float], regime_payload: Optional[Dict[str, Any]] = None, transition_payload: Optional[Dict[str, Any]] = None, alignment_payload: Optional[Dict[str, Any]] = None) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None:
        return None, None

    reg_mult = regime_size_multiplier(regime_payload)
    tran_mult = transition_risk_size_multiplier(transition_payload)
    align_mult = alignment_size_multiplier(alignment_payload)

    final_mult = min(reg_mult, tran_mult, align_mult)

    if final_mult < 1.0:
        adjusted_notional = notional_usd * final_mult
        reason = SizingAdjustmentReason.REGIME_CONFLICT
        if tran_mult < 1.0 and tran_mult == final_mult:
            reason = SizingAdjustmentReason.HIGH_TRANSITION_RISK

        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(reason),
            reason=reason,
            multiplier=final_mult,
            delta_notional_usd=adjusted_notional - notional_usd,
            description="Reduced size due to regime or transition alignment constraints."
        )
        return adjusted_notional, adj

    return notional_usd, None

def regime_size_warnings(regime_payload: Optional[Dict[str, Any]] = None, transition_payload: Optional[Dict[str, Any]] = None, alignment_payload: Optional[Dict[str, Any]] = None) -> List[str]:
    warnings = []
    if regime_payload and regime_payload.get("regime_state") == "RISK_OFF":
        warnings.append("Risk-off regime active.")
    if transition_payload and transition_payload.get("is_high_risk", False):
        warnings.append("High transition risk active.")
    if alignment_payload and alignment_payload.get("status") in ["CONFLICTED", "BLOCK_SIGNAL"]:
        warnings.append("Strategy regime alignment is conflicted or blocked.")
    return warnings

def regime_size_adjuster_to_text(payload: Dict[str, Any]) -> str:
    return (
        f"Regime Multiplier: {payload.get('multiplier', 'N/A')}\n"
    )
