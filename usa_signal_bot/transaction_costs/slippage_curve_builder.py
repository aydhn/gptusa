import datetime
import uuid
from typing import Optional

from usa_signal_bot.core.enums import SlippageCurveType, LiquidityStatus
from usa_signal_bot.transaction_costs.cost_models import SlippageCurve, create_slippage_curve_id
from usa_signal_bot.transaction_costs.slippage_curves import build_default_slippage_curve, build_conservative_slippage_curve
from usa_signal_bot.execution.liquidity_models import LiquidityProfile, TradabilityGuardResult

def liquidity_multiplier_from_profile(profile: LiquidityProfile | None) -> float:
    if not profile:
        return 1.0

    status = profile.status
    if status == LiquidityStatus.EXCELLENT:
        return 0.8
    elif status == LiquidityStatus.GOOD:
        return 1.0
    elif status == LiquidityStatus.ACCEPTABLE:
        return 1.2
    elif status == LiquidityStatus.THIN:
        return 2.0
    elif status == LiquidityStatus.ILLIQUID:
        return 3.0
    return 1.0

def volatility_multiplier_from_atr_pct(atr_pct: float | None) -> float:
    if atr_pct is None:
        return 1.0

    if atr_pct < 1.0:
        return 0.9
    elif atr_pct < 2.0:
        return 1.0
    elif atr_pct < 4.0:
        return 1.2
    elif atr_pct < 8.0:
        return 1.5
    else:
        return 2.0

def spread_multiplier_from_proxy(spread_proxy_bps: float | None) -> float:
    if spread_proxy_bps is None:
        return 1.0

    if spread_proxy_bps < 5.0:
        return 0.9
    elif spread_proxy_bps < 15.0:
        return 1.0
    elif spread_proxy_bps < 50.0:
        return 1.2
    else:
        return 1.5

def build_liquidity_adjusted_slippage_curve(
    symbol: str,
    liquidity_profile: LiquidityProfile | None = None,
    spread_proxy_bps: float | None = None,
    atr_pct: float | None = None
) -> SlippageCurve:

    # Start with base curve depending on liquidity
    if liquidity_profile and liquidity_profile.status in [LiquidityStatus.THIN, LiquidityStatus.ILLIQUID]:
        curve = build_conservative_slippage_curve(symbol)
    else:
        curve = build_default_slippage_curve(symbol)

    curve.curve_type = SlippageCurveType.LIQUIDITY_ADJUSTED

    liq_mult = liquidity_multiplier_from_profile(liquidity_profile)
    spread_mult = spread_multiplier_from_proxy(spread_proxy_bps)

    # Combined liquidity multiplier bounded safely
    curve.liquidity_multiplier = min(max(liq_mult * spread_mult, 0.5), 5.0)

    vol_mult = volatility_multiplier_from_atr_pct(atr_pct)
    if liquidity_profile and liquidity_profile.gap_pct and liquidity_profile.gap_pct > 5.0:
        vol_mult *= 1.2

    curve.volatility_multiplier = min(max(vol_mult, 0.5), 5.0)
    curve.base_spread_bps = spread_proxy_bps

    return curve

def curve_from_tradability_guard_result(result: TradabilityGuardResult) -> SlippageCurve:
    return build_liquidity_adjusted_slippage_curve(
        symbol=result.symbol,
        liquidity_profile=result.liquidity_profile,
        spread_proxy_bps=result.spread_estimate.spread_proxy_bps if result.spread_estimate else None,
        atr_pct=result.liquidity_profile.atr_pct if result.liquidity_profile else None
    )

def slippage_curve_builder_summary_to_text(curve: SlippageCurve) -> str:
    lines = [
        f"Liquidity-Adjusted Slippage Curve (Symbol: {curve.symbol})",
        f"  Liquidity Multiplier: {curve.liquidity_multiplier:.2f}",
        f"  Volatility Multiplier: {curve.volatility_multiplier:.2f}"
    ]
    return "\n".join(lines)
