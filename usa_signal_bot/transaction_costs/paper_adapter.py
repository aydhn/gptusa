from typing import Any
from usa_signal_bot.core.enums import TransactionSide, MarketImpactStatus
from usa_signal_bot.execution.liquidity_models import LiquidityProfile
from usa_signal_bot.transaction_costs.cost_models import TransactionCostInput, FillSimulationRequest
from usa_signal_bot.transaction_costs.fee_schedule import load_fee_schedule_from_config
from usa_signal_bot.transaction_costs.slippage_curve_builder import (
    build_liquidity_adjusted_slippage_curve,
)
from usa_signal_bot.transaction_costs.market_impact import estimate_market_impact
from usa_signal_bot.transaction_costs.cost_adjusted_trade import (
    build_transaction_cost_breakdown,
)
from usa_signal_bot.transaction_costs.fill_simulator import simulate_fill


def _resolve_side(action: str) -> TransactionSide:
    action = action.lower()
    if action == "buy":
        return TransactionSide.BUY
    elif action == "sell":
        return TransactionSide.SELL
    elif action == "short":
        return TransactionSide.SHORT
    elif action == "cover":
        return TransactionSide.COVER
    return TransactionSide.BUY


def apply_transaction_costs_to_paper_order(
    order: dict[str, Any],
    liquidity_profile: LiquidityProfile | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:

    if not config or not config.get("transaction_cost_model", {}).get("enabled", False):
        return order

    symbol = order.get("symbol", "UNKNOWN")
    action = order.get("action", "buy")
    quantity = order.get("quantity")

    # We might not have a price on order creation if market order,
    # but let's assume limit_price or some reference price is available.
    price = order.get("limit_price") or order.get("estimated_price") or 100.0

    notional_usd = None
    if quantity and price:
        notional_usd = quantity * price

    side = _resolve_side(action)

    fee_schedule = load_fee_schedule_from_config(config)

    input_payload = TransactionCostInput(
        input_id="paper_ord",
        symbol=symbol,
        side=side,
        quantity=quantity,
        notional_usd=notional_usd,
        price=price,
        avg_dollar_volume=(
            liquidity_profile.avg_dollar_volume if liquidity_profile else None
        ),
        atr_pct=liquidity_profile.atr_pct if liquidity_profile else None,
        spread_proxy_bps=10.0,
        participation_rate_pct=None,
        liquidity_status=liquidity_profile.status if liquidity_profile else None,
    )

    curve = build_liquidity_adjusted_slippage_curve(symbol, liquidity_profile)
    breakdown = build_transaction_cost_breakdown(input_payload, fee_schedule, curve)
    impact = estimate_market_impact(input_payload)

    order["estimated_cost_usd"] = breakdown.total_cost_usd
    order["estimated_cost_bps"] = breakdown.total_cost_bps
    order["market_impact_status"] = (
        impact.status.value
        if isinstance(impact.status, MarketImpactStatus)
        else impact.status
    )

    return order


def apply_transaction_costs_to_paper_fill(
    fill: dict[str, Any], config: dict[str, Any] | None = None
) -> dict[str, Any]:
    if not config or not config.get("transaction_cost_model", {}).get("enabled", False):
        return fill

    # Assume fill already has some basic data
    symbol = fill.get("symbol", "UNKNOWN")
    action = fill.get("action", "buy")
    quantity = fill.get("quantity")
    base_price = fill.get("fill_price")

    side = _resolve_side(action)
    notional_usd = None
    if quantity and base_price:
        notional_usd = quantity * base_price

    fee_schedule = load_fee_schedule_from_config(config)
    input_payload = TransactionCostInput(
        input_id="paper_fill",
        symbol=symbol,
        side=side,
        quantity=quantity,
        notional_usd=notional_usd,
        price=base_price,
        avg_dollar_volume=None,
        atr_pct=None,
        spread_proxy_bps=10.0,
        participation_rate_pct=0.5,
        liquidity_status=None,
    )

    curve = build_liquidity_adjusted_slippage_curve(symbol)
    breakdown = build_transaction_cost_breakdown(input_payload, fee_schedule, curve)
    impact = estimate_market_impact(input_payload)

    sim_result = simulate_fill(
        FillSimulationRequest(
            symbol=symbol,
            side=side,
            quantity=quantity,
            notional_usd=notional_usd,
            reference_price=base_price,
            cost_breakdown=breakdown,
            market_impact=impact
        )
    )

    if sim_result.simulated_fill_price:
        fill["cost_adjusted_fill_price"] = sim_result.simulated_fill_price
        fill["estimated_cost_usd"] = breakdown.total_cost_usd
        fill["fill_realism_status"] = (
            sim_result.status.value
            if hasattr(sim_result.status, "value")
            else sim_result.status
        )

    return fill


def paper_cost_summary(orders_or_fills: list[dict[str, Any]]) -> dict[str, Any]:
    total_cost = 0.0
    for i in orders_or_fills:
        if "estimated_cost_usd" in i:
            total_cost += i["estimated_cost_usd"]
    return {"total_estimated_cost_usd": total_cost, "count": len(orders_or_fills)}


def paper_cost_warnings(order_or_fill: dict[str, Any]) -> list[str]:
    warnings = []
    if order_or_fill.get("market_impact_status") in ["HIGH", "EXTREME"]:
        warnings.append(
            f"HIGH/EXTREME market impact expected for paper order on {order_or_fill.get('symbol')}."
        )
    return warnings
