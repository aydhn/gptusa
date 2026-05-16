from typing import Optional, Tuple, List
from usa_signal_bot.core.enums import SizingAdjustmentReason
from usa_signal_bot.allocation.allocation_models import SizingAdjustment, create_sizing_adjustment_id, CapitalState, RiskBudget
from usa_signal_bot.allocation.risk_budget import max_trade_notional_from_budget

def apply_max_position_notional_cap(notional_usd: Optional[float], capital_state: CapitalState, budget: RiskBudget) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None:
        return None, None

    cap_usd = max_trade_notional_from_budget(capital_state, budget)
    if notional_usd > cap_usd:
        multiplier = cap_usd / notional_usd if notional_usd > 0 else 0
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.PORTFOLIO_CAP),
            reason=SizingAdjustmentReason.PORTFOLIO_CAP,
            multiplier=multiplier,
            delta_notional_usd=cap_usd - notional_usd,
            description=f"Capped notional at {cap_usd:.2f} due to max position notional limit."
        )
        return cap_usd, adj
    return notional_usd, None

def apply_min_position_notional_floor(notional_usd: Optional[float], min_notional_usd: float = 10.0) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None:
        return None, None

    if notional_usd < min_notional_usd:
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.INSUFFICIENT_CAPITAL),
            reason=SizingAdjustmentReason.INSUFFICIENT_CAPITAL,
            multiplier=0.0,
            delta_notional_usd=-notional_usd,
            description=f"Blocked position due to notional {notional_usd:.2f} being below minimum floor {min_notional_usd:.2f}."
        )
        return 0.0, adj
    return notional_usd, None

def apply_symbol_cap(notional_usd: Optional[float], symbol_exposure_usd: Optional[float], cap_usd: Optional[float]) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None or symbol_exposure_usd is None or cap_usd is None:
        return notional_usd, None

    if symbol_exposure_usd + notional_usd > cap_usd:
        allowed = max(0.0, cap_usd - symbol_exposure_usd)
        multiplier = allowed / notional_usd if notional_usd > 0 else 0
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.SYMBOL_CAP),
            reason=SizingAdjustmentReason.SYMBOL_CAP,
            multiplier=multiplier,
            delta_notional_usd=allowed - notional_usd,
            description=f"Capped notional to {allowed:.2f} due to symbol exposure limit."
        )
        return allowed, adj
    return notional_usd, None

def apply_strategy_cap(notional_usd: Optional[float], strategy_exposure_usd: Optional[float], cap_usd: Optional[float]) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None or strategy_exposure_usd is None or cap_usd is None:
        return notional_usd, None

    if strategy_exposure_usd + notional_usd > cap_usd:
        allowed = max(0.0, cap_usd - strategy_exposure_usd)
        multiplier = allowed / notional_usd if notional_usd > 0 else 0
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.STRATEGY_CAP),
            reason=SizingAdjustmentReason.STRATEGY_CAP,
            multiplier=multiplier,
            delta_notional_usd=allowed - notional_usd,
            description=f"Capped notional to {allowed:.2f} due to strategy exposure limit."
        )
        return allowed, adj
    return notional_usd, None

def apply_portfolio_cap(notional_usd: Optional[float], capital_state: CapitalState) -> Tuple[Optional[float], Optional[SizingAdjustment]]:
    if notional_usd is None:
        return None, None

    if notional_usd > capital_state.available_cash_usd:
        allowed = capital_state.available_cash_usd
        multiplier = allowed / notional_usd if notional_usd > 0 else 0
        adj = SizingAdjustment(
            adjustment_id=create_sizing_adjustment_id(SizingAdjustmentReason.INSUFFICIENT_CAPITAL),
            reason=SizingAdjustmentReason.INSUFFICIENT_CAPITAL,
            multiplier=multiplier,
            delta_notional_usd=allowed - notional_usd,
            description=f"Capped notional to available cash {allowed:.2f}."
        )
        return allowed, adj
    return notional_usd, None

def position_caps_to_text(adjustments: List[SizingAdjustment]) -> str:
    if not adjustments:
        return "No position cap adjustments applied."
    lines = ["Position Cap Adjustments:"]
    for adj in adjustments:
        lines.append(f" - {adj.reason.value}: x{adj.multiplier:.2f} ({adj.description})")
    return "\n".join(lines)
