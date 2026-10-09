"""Exit rules, volatility-based sizing and portfolio risk limits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Mapping, Tuple

import pandas as pd


@dataclass(frozen=True)
class ExitRules:
    stop_loss: float = 0.10  # exit when price <= entry * (1 - stop_loss)
    trailing_stop: float = 0.15  # exit when price <= peak * (1 - trailing_stop)
    max_hold_days: int = 60
    exit_on_risk_off: bool = True


@dataclass
class PositionState:
    quantity: float
    entry_price: float
    peak_price: float
    entry_index: int  # trading-day index of entry


def evaluate_exits(
    positions: Mapping[str, PositionState], prices: Mapping[str, float], day_index: int, regime: str, rules: ExitRules
) -> Dict[str, str]:
    """Return {symbol: reason} for positions that must be closed."""
    out: Dict[str, str] = {}
    for sym, pos in positions.items():
        px = prices.get(sym)
        if px is None or pd.isna(px):
            continue
        peak = max(pos.peak_price, px)
        if px <= pos.entry_price * (1.0 - rules.stop_loss):
            out[sym] = "STOP_LOSS"
        elif px <= peak * (1.0 - rules.trailing_stop):
            out[sym] = "TRAILING_STOP"
        elif day_index - pos.entry_index >= rules.max_hold_days:
            out[sym] = "MAX_HOLD"
        elif rules.exit_on_risk_off and regime == "RISK_OFF":
            out[sym] = "REGIME_RISK_OFF"
    return out


def inverse_vol_weights(vols: Mapping[str, float], gross: float, max_weight: float) -> Dict[str, float]:
    """Weights proportional to 1/vol summing to ``gross`` (iteratively capped at ``max_weight``)."""
    vols = {s: v for s, v in vols.items() if v is not None and v == v and v > 0}
    if not vols or gross <= 0:
        return {}
    free = dict(vols)
    fixed: Dict[str, float] = {}
    remaining = gross
    while free:
        inv = {s: 1.0 / v for s, v in free.items()}
        total = sum(inv.values())
        raw = {s: remaining * x / total for s, x in inv.items()}
        over = [s for s, w in raw.items() if w > max_weight + 1e-12]
        if not over:
            fixed.update(raw)
            break
        for s in over:
            fixed[s] = max_weight
            remaining -= max_weight
            del free[s]
        if remaining <= 0:
            break
    return fixed


@dataclass(frozen=True)
class RiskLimits:
    max_positions: int = 10
    max_weight: float = 0.15
    max_gross: float = 1.0
    max_daily_turnover: float = 0.5
    drawdown_kill: float = 0.20  # flat while portfolio drawdown from peak exceeds this


def apply_risk_limits(
    target: Mapping[str, float], current: Mapping[str, float], drawdown: float, limits: RiskLimits
) -> Tuple[Dict[str, float], List[str]]:
    """Clamp a target weight map to the risk limits; return (weights, reasons)."""
    reasons: List[str] = []
    if drawdown <= -limits.drawdown_kill:
        return {}, [f"KILL_SWITCH drawdown {drawdown:.1%}"]
    w = {s: min(x, limits.max_weight) for s, x in target.items() if x > 0}
    if len(w) > limits.max_positions:
        keep = sorted(w, key=lambda s: -w[s])[: limits.max_positions]
        w = {s: w[s] for s in keep}
        reasons.append("MAX_POSITIONS")
    gross = sum(w.values())
    if gross > limits.max_gross:
        scale = limits.max_gross / gross
        w = {s: x * scale for s, x in w.items()}
        reasons.append("MAX_GROSS")
    syms = set(w) | set(current)
    turnover = sum(abs(w.get(s, 0.0) - current.get(s, 0.0)) for s in syms)
    if turnover > limits.max_daily_turnover and turnover > 0:
        alpha = limits.max_daily_turnover / turnover
        w = {s: current.get(s, 0.0) + alpha * (w.get(s, 0.0) - current.get(s, 0.0)) for s in syms}
        w = {s: x for s, x in w.items() if x > 1e-9}
        reasons.append("TURNOVER_CAP")
        # drifted holdings can sit above the caps while turnover is throttled: hard caps win
        clamped = {s: min(x, limits.max_weight) for s, x in w.items()}
        gross = sum(clamped.values())
        if gross > limits.max_gross:
            clamped = {s: x * limits.max_gross / gross for s, x in clamped.items()}
        if len(clamped) > limits.max_positions:
            keep = sorted(clamped, key=lambda s: -clamped[s])[: limits.max_positions]
            clamped = {s: clamped[s] for s in keep}
        if clamped != w:
            reasons.append("DRIFT_CLAMP")
        w = clamped
    return w, reasons
