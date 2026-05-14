import datetime
import uuid
from typing import Any, Optional

from usa_signal_bot.core.enums import SlippageCurveType, OrderSizeClass
from usa_signal_bot.transaction_costs.cost_models import SlippageCurvePoint, SlippageCurve, create_slippage_curve_id

def build_default_slippage_curve(symbol: str | None = None) -> SlippageCurve:
    points = [
        SlippageCurvePoint(participation_rate_pct=0.01, slippage_bps=2.0),
        SlippageCurvePoint(participation_rate_pct=0.10, slippage_bps=5.0),
        SlippageCurvePoint(participation_rate_pct=0.50, slippage_bps=15.0),
        SlippageCurvePoint(participation_rate_pct=1.00, slippage_bps=30.0),
        SlippageCurvePoint(participation_rate_pct=5.00, slippage_bps=120.0),
        SlippageCurvePoint(participation_rate_pct=10.00, slippage_bps=300.0)
    ]
    return SlippageCurve(
        curve_id=create_slippage_curve_id(symbol),
        symbol=symbol,
        curve_type=SlippageCurveType.CONVEX,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        points=points,
        base_spread_bps=None,
        volatility_multiplier=1.0,
        liquidity_multiplier=1.0,
        warnings=[],
        errors=[],
        metadata={"description": "Default heuristic slippage curve"}
    )

def build_conservative_slippage_curve(symbol: str | None = None) -> SlippageCurve:
    points = [
        SlippageCurvePoint(participation_rate_pct=0.01, slippage_bps=5.0),
        SlippageCurvePoint(participation_rate_pct=0.10, slippage_bps=10.0),
        SlippageCurvePoint(participation_rate_pct=0.50, slippage_bps=25.0),
        SlippageCurvePoint(participation_rate_pct=1.00, slippage_bps=50.0),
        SlippageCurvePoint(participation_rate_pct=5.00, slippage_bps=200.0),
        SlippageCurvePoint(participation_rate_pct=10.00, slippage_bps=500.0)
    ]
    return SlippageCurve(
        curve_id=create_slippage_curve_id(symbol),
        symbol=symbol,
        curve_type=SlippageCurveType.CONVEX,
        created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        points=points,
        base_spread_bps=None,
        volatility_multiplier=1.0,
        liquidity_multiplier=1.0,
        warnings=[],
        errors=[],
        metadata={"description": "Conservative heuristic slippage curve"}
    )

def interpolate_curve_points(points: list[SlippageCurvePoint], x: float) -> float | None:
    if not points:
        return None

    sorted_points = sorted(points, key=lambda p: p.participation_rate_pct)

    if x <= sorted_points[0].participation_rate_pct:
        return sorted_points[0].slippage_bps

    if x >= sorted_points[-1].participation_rate_pct:
        # Extrapolate linearly beyond max point or just cap
        # Capping is safer for heuristic
        return sorted_points[-1].slippage_bps

    for i in range(len(sorted_points) - 1):
        x0 = sorted_points[i].participation_rate_pct
        x1 = sorted_points[i+1].participation_rate_pct
        y0 = sorted_points[i].slippage_bps
        y1 = sorted_points[i+1].slippage_bps

        if x0 <= x <= x1:
            # Linear interpolation between points
            slope = (y1 - y0) / (x1 - x0)
            return y0 + slope * (x - x0)

    return None

def apply_curve_multipliers(slippage_bps: float | None, curve: SlippageCurve) -> float | None:
    if slippage_bps is None:
        return None
    return slippage_bps * curve.liquidity_multiplier * curve.volatility_multiplier

def evaluate_slippage_curve(curve: SlippageCurve, participation_rate_pct: float | None) -> float | None:
    if participation_rate_pct is None:
        return None

    base_slippage = interpolate_curve_points(curve.points, participation_rate_pct)
    if base_slippage is None:
        return None

    return apply_curve_multipliers(base_slippage, curve)

def classify_order_size_class(participation_rate_pct: float | None) -> OrderSizeClass:
    if participation_rate_pct is None:
        return OrderSizeClass.UNKNOWN
    if participation_rate_pct < 0.1:
        return OrderSizeClass.MICRO
    elif participation_rate_pct < 0.5:
        return OrderSizeClass.SMALL
    elif participation_rate_pct < 1.0:
        return OrderSizeClass.MEDIUM
    elif participation_rate_pct < 5.0:
        return OrderSizeClass.LARGE
    else:
        return OrderSizeClass.OVERSIZED

def slippage_curve_to_text(curve: SlippageCurve) -> str:
    lines = [
        f"Slippage Curve: {curve.curve_id} (Symbol: {curve.symbol})",
        f"  Type: {curve.curve_type.value if isinstance(curve.curve_type, SlippageCurveType) else curve.curve_type}",
        f"  Liquidity Multiplier: {curve.liquidity_multiplier:.2f}",
        f"  Volatility Multiplier: {curve.volatility_multiplier:.2f}",
        "  Points:"
    ]
    for p in sorted(curve.points, key=lambda x: x.participation_rate_pct):
        lines.append(f"    - {p.participation_rate_pct}% participation -> {p.slippage_bps} bps")
    return "\n".join(lines)
