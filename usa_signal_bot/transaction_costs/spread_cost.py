from typing import Any
from usa_signal_bot.core.enums import TransactionSide

def estimate_spread_cost_bps(spread_proxy_bps: float | None, side: TransactionSide, crossing_fraction: float = 0.5) -> float | None:
    """
    Estimates the spread cost in bps. Default crossing fraction is 0.5 (half-spread),
    which assumes filling exactly at the bid/ask depending on side.
    """
    if spread_proxy_bps is None or spread_proxy_bps < 0:
        return None

    return spread_proxy_bps * crossing_fraction

def estimate_spread_cost_usd(spread_cost_bps: float | None, notional_usd: float | None) -> float | None:
    if spread_cost_bps is None or notional_usd is None or notional_usd <= 0:
        return None

    return notional_usd * (spread_cost_bps / 10000.0)

def spread_cost_component(symbol: str, spread_proxy_bps: float | None, side: TransactionSide, notional_usd: float | None) -> dict[str, Any]:
    cost_bps = estimate_spread_cost_bps(spread_proxy_bps, side)
    cost_usd = estimate_spread_cost_usd(cost_bps, notional_usd)

    return {
        "symbol": symbol,
        "spread_proxy_bps": spread_proxy_bps,
        "spread_cost_bps": cost_bps,
        "spread_cost_usd": cost_usd,
        "notes": [
            "Assumes default half-spread crossing fraction (0.5).",
            "Spread proxy is heuristic, not a real bid/ask."
        ]
    }

def spread_cost_to_text(component: dict[str, Any]) -> str:
    lines = [
        f"Spread Cost Estimate ({component.get('symbol', 'UNKNOWN')}):",
        f"  Spread Proxy: {component.get('spread_proxy_bps')} bps",
        f"  Estimated Cost: {component.get('spread_cost_bps')} bps",
        f"  Estimated Cost USD: ${component.get('spread_cost_usd') if component.get('spread_cost_usd') is not None else 'None'}",
        "  Notes:"
    ]
    for note in component.get("notes", []):
        lines.append(f"    - {note}")
    return "\n".join(lines)
