from typing import Any
from usa_signal_bot.core.enums import SlippageCurveType
from usa_signal_bot.transaction_costs.slippage_curves import build_default_slippage_curve, build_conservative_slippage_curve, evaluate_slippage_curve

def estimate_participation_cost_bps(participation_rate_pct: float | None, curve_type: SlippageCurveType = SlippageCurveType.CONVEX) -> float | None:
    if participation_rate_pct is None or participation_rate_pct < 0:
        return None

    if curve_type == SlippageCurveType.LINEAR:
        # Simple linear approximation for testing
        return participation_rate_pct * 15.0

    # By default, evaluate on the default convex curve
    curve = build_default_slippage_curve()
    return evaluate_slippage_curve(curve, participation_rate_pct)

def estimate_participation_cost_usd(participation_cost_bps: float | None, notional_usd: float | None) -> float | None:
    if participation_cost_bps is None or notional_usd is None or notional_usd <= 0:
        return None
    return notional_usd * (participation_cost_bps / 10000.0)

def participation_cost_component(participation_rate_pct: float | None, notional_usd: float | None) -> dict[str, Any]:
    cost_bps = estimate_participation_cost_bps(participation_rate_pct)
    cost_usd = estimate_participation_cost_usd(cost_bps, notional_usd)

    return {
        "participation_rate_pct": participation_rate_pct,
        "participation_cost_bps": cost_bps,
        "participation_cost_usd": cost_usd,
        "notes": [
            "Cost is estimated using heuristic convex curve."
        ]
    }

def participation_cost_to_text(component: dict[str, Any]) -> str:
    lines = [
        "Participation Cost Estimate:",
        f"  Participation Rate: {component.get('participation_rate_pct', 'Unknown')}%",
        f"  Estimated Cost: {component.get('participation_cost_bps', 'Unknown')} bps",
        f"  Estimated Cost USD: ${component.get('participation_cost_usd') if component.get('participation_cost_usd') is not None else 'Unknown'}"
    ]
    return "\n".join(lines)
