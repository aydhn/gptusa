from datetime import datetime, timezone

from usa_signal_bot.core.enums import TransactionSide, MarketImpactStatus
from usa_signal_bot.transaction_costs.cost_models import MarketImpactEstimate, create_market_impact_estimate_id, TransactionCostInput
from usa_signal_bot.transaction_costs.participation_cost import estimate_participation_cost_bps
from usa_signal_bot.transaction_costs.volatility_penalty import estimate_volatility_penalty_bps
from usa_signal_bot.transaction_costs.spread_cost import estimate_spread_cost_bps
from usa_signal_bot.transaction_costs.slippage_curves import classify_order_size_class
from usa_signal_bot.core.enums import OrderSizeClass

def estimate_market_impact_bps(
    participation_rate_pct: float | None,
    atr_pct: float | None = None,
    spread_proxy_bps: float | None = None
) -> float | None:
    if participation_rate_pct is None:
        return None

    base_impact = estimate_participation_cost_bps(participation_rate_pct)
    if base_impact is None:
        return None

    vol_pen = estimate_volatility_penalty_bps(atr_pct) or 0.0
    spread_pen = (spread_proxy_bps or 0.0) * 0.25  # 25% of spread contributes to impact

    return base_impact + vol_pen + spread_pen

def estimate_market_impact_usd(impact_bps: float | None, notional_usd: float | None) -> float | None:
    if impact_bps is None or notional_usd is None or notional_usd <= 0:
        return None
    return notional_usd * (impact_bps / 10000.0)

def classify_market_impact_status(impact_bps: float | None, participation_rate_pct: float | None = None) -> MarketImpactStatus:
    if impact_bps is None or participation_rate_pct is None:
        return MarketImpactStatus.INSUFFICIENT_DATA

    if participation_rate_pct > 10.0:
        return MarketImpactStatus.EXTREME

    if impact_bps < 5.0:
        return MarketImpactStatus.NEGLIGIBLE
    elif impact_bps < 20.0:
        return MarketImpactStatus.LOW
    elif impact_bps < 75.0:
        return MarketImpactStatus.MODERATE
    elif impact_bps < 200.0:
        return MarketImpactStatus.HIGH
    else:
        return MarketImpactStatus.EXTREME

def estimate_market_impact(
    tc_input: TransactionCostInput
) -> MarketImpactEstimate:

    participation_rate_pct = None
    if tc_input.notional_usd is not None and tc_input.avg_dollar_volume is not None and tc_input.avg_dollar_volume > 0:
        participation_rate_pct = (tc_input.notional_usd / tc_input.avg_dollar_volume) * 100.0

    impact_bps = estimate_market_impact_bps(participation_rate_pct, tc_input.atr_pct, tc_input.spread_proxy_bps)
    impact_usd = estimate_market_impact_usd(impact_bps, tc_input.notional_usd)
    status = classify_market_impact_status(impact_bps, participation_rate_pct)
    size_class = classify_order_size_class(participation_rate_pct)

    warnings = []
    if status in [MarketImpactStatus.HIGH, MarketImpactStatus.EXTREME]:
        warnings.append(f"Market impact is {status.value}. Real execution may suffer severe slippage.")
    if participation_rate_pct is None:
        warnings.append("Missing participation rate (no ADV or notional). Cannot estimate impact reliably.")

    return MarketImpactEstimate(
        estimate_id=create_market_impact_estimate_id(tc_input.symbol),
        symbol=tc_input.symbol,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        side=tc_input.side,
        notional_usd=tc_input.notional_usd,
        participation_rate_pct=participation_rate_pct,
        impact_bps=impact_bps,
        impact_usd=impact_usd,
        status=status,
        order_size_class=size_class,
        warnings=warnings,
        errors=[],
        metadata={
            "disclaimer": "Market impact is a heuristic local model and does not represent real order book execution."
        }
    )

def market_impact_to_text(estimate: MarketImpactEstimate) -> str:
    lines = [
        f"Market Impact Estimate (Symbol: {estimate.symbol})",
        f"  Side: {estimate.side.value if isinstance(estimate.side, TransactionSide) else estimate.side}",
        f"  Notional USD: ${estimate.notional_usd if estimate.notional_usd is not None else 'Unknown'}",
        f"  Participation Rate: {estimate.participation_rate_pct:.4f}%" if estimate.participation_rate_pct is not None else "  Participation Rate: Unknown",
        f"  Order Size Class: {estimate.order_size_class.value if isinstance(estimate.order_size_class, OrderSizeClass) else estimate.order_size_class}",
        f"  Status: {estimate.status.value if isinstance(estimate.status, MarketImpactStatus) else estimate.status}",
        f"  Impact BPS: {estimate.impact_bps:.2f}" if estimate.impact_bps is not None else "  Impact BPS: Unknown",
        f"  Impact USD: ${estimate.impact_usd:.2f}" if estimate.impact_usd is not None else "  Impact USD: Unknown"
    ]
    if estimate.warnings:
        lines.append("  Warnings:")
        for w in estimate.warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines)
