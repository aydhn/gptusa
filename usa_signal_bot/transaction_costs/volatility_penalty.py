from typing import Any

def estimate_volatility_penalty_bps(atr_pct: float | None, base_threshold_pct: float = 2.0) -> float | None:
    if atr_pct is None or atr_pct < 0:
        return None

    if atr_pct <= base_threshold_pct:
        return 0.0

    # Heuristic penalty: 5 bps for every 1% ATR above threshold
    excess_atr = atr_pct - base_threshold_pct
    return excess_atr * 5.0

def estimate_gap_penalty_bps(gap_pct: float | None, threshold_pct: float = 3.0) -> float | None:
    if gap_pct is None or gap_pct < 0:
        return None

    if gap_pct <= threshold_pct:
        return 0.0

    # Heuristic penalty: 10 bps for every 1% gap above threshold
    excess_gap = gap_pct - threshold_pct
    return excess_gap * 10.0

def combined_volatility_gap_penalty_bps(atr_pct: float | None, gap_pct: float | None) -> float | None:
    vol_pen = estimate_volatility_penalty_bps(atr_pct)
    gap_pen = estimate_gap_penalty_bps(gap_pct)

    if vol_pen is None and gap_pen is None:
        return None

    return (vol_pen or 0.0) + (gap_pen or 0.0)

def volatility_penalty_component(atr_pct: float | None, gap_pct: float | None, notional_usd: float | None) -> dict[str, Any]:
    penalty_bps = combined_volatility_gap_penalty_bps(atr_pct, gap_pct)

    penalty_usd = None
    if penalty_bps is not None and notional_usd is not None and notional_usd > 0:
        penalty_usd = notional_usd * (penalty_bps / 10000.0)

    return {
        "atr_pct": atr_pct,
        "gap_pct": gap_pct,
        "penalty_bps": penalty_bps,
        "penalty_usd": penalty_usd,
        "notes": [
            "Volatility and gap penalties are heuristic.",
            "They capture the cost of demanding liquidity in fast markets."
        ]
    }

def volatility_penalty_to_text(component: dict[str, Any]) -> str:
    lines = [
        "Volatility/Gap Penalty Estimate:",
        f"  ATR %: {component.get('atr_pct')}%",
        f"  Gap %: {component.get('gap_pct')}%",
        f"  Estimated Penalty: {component.get('penalty_bps')} bps",
        f"  Estimated Penalty USD: ${component.get('penalty_usd') if component.get('penalty_usd') is not None else 'Unknown'}"
    ]
    return "\n".join(lines)
