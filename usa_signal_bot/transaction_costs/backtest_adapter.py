from typing import Any
from usa_signal_bot.core.enums import TransactionSide, MarketImpactStatus
from usa_signal_bot.transaction_costs.cost_models import TransactionCostInput
from usa_signal_bot.transaction_costs.fee_schedule import load_fee_schedule_from_config
from usa_signal_bot.transaction_costs.slippage_curve_builder import build_liquidity_adjusted_slippage_curve
from usa_signal_bot.transaction_costs.market_impact import estimate_market_impact
from usa_signal_bot.transaction_costs.cost_adjusted_trade import build_transaction_cost_breakdown

def apply_transaction_costs_to_backtest_trades(
    trades: list[dict[str, Any]],
    symbol_rows: dict[str, list[dict[str, Any]]] | None = None,
    config: dict[str, Any] | None = None
) -> list[dict[str, Any]]:

    # Heuristic adapter that doesn't break backtest result schema
    # but decorates trades with cost metadata

    if not config or not config.get("transaction_cost_model", {}).get("enabled", False):
        return trades

    fee_schedule = load_fee_schedule_from_config(config)

    for trade in trades:
        symbol = trade.get("symbol", "UNKNOWN")
        quantity = trade.get("quantity")
        entry_price = trade.get("entry_price", 0.0)
        exit_price = trade.get("exit_price", 0.0)

        notional_usd = None
        if quantity and entry_price:
            notional_usd = quantity * entry_price

        # Try to infer direction
        side = TransactionSide.BUY
        if trade.get("direction", "long") == "short":
            side = TransactionSide.SHORT

        # Fake input for proxy
        input_payload = TransactionCostInput(
            input_id="bt_proxy",
            symbol=symbol,
            side=side,
            quantity=quantity,
            notional_usd=notional_usd,
            price=entry_price,
            avg_dollar_volume=None,  # No easy ADV access here unless passed
            atr_pct=None,
            spread_proxy_bps=10.0, # default fallback
            participation_rate_pct=0.5, # default fallback
            liquidity_status=None
        )

        curve = build_liquidity_adjusted_slippage_curve(symbol)
        breakdown = build_transaction_cost_breakdown(input_payload, fee_schedule, curve)
        impact = estimate_market_impact(input_payload)

        gross_pnl = trade.get("pnl_usd", 0.0)
        cost_usd = breakdown.total_cost_usd or 0.0
        # Round trip
        cost_usd *= 2.0

        trade["gross_pnl_usd"] = gross_pnl
        trade["estimated_total_cost_usd"] = cost_usd
        trade["net_pnl_usd"] = gross_pnl - cost_usd
        trade["estimated_cost_bps"] = (breakdown.total_cost_bps or 0.0) * 2.0
        trade["market_impact_status"] = impact.status.value if isinstance(impact.status, MarketImpactStatus) else impact.status

    return trades

def apply_transaction_costs_to_backtest_result(result: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
    if not config or not config.get("transaction_cost_model", {}).get("enabled", False):
        return result

    metrics = result.get("metrics", {})
    trades = result.get("trades", [])

    trades = apply_transaction_costs_to_backtest_trades(trades, None, config)
    result["trades"] = trades

    total_gross = metrics.get("total_pnl", 0.0)
    total_cost = sum(t.get("estimated_total_cost_usd", 0.0) for t in trades)

    metrics["gross_total_return"] = metrics.get("total_return", 0.0)
    # Simple heuristic
    metrics["total_estimated_cost_usd"] = total_cost
    metrics["net_pnl_usd"] = total_gross - total_cost

    # Replace PnL loosely for reporting
    metrics["cost_adjusted"] = True

    return result

def backtest_cost_summary(trades: list[dict[str, Any]]) -> dict[str, Any]:
    total_cost = sum(t.get("estimated_total_cost_usd", 0.0) for t in trades)
    high_impact_count = sum(1 for t in trades if t.get("market_impact_status") in ["HIGH", "EXTREME"])

    return {
        "total_estimated_cost_usd": total_cost,
        "high_impact_trade_count": high_impact_count,
        "average_cost_per_trade_usd": total_cost / len(trades) if trades else 0.0
    }

def backtest_cost_warnings(trades: list[dict[str, Any]]) -> list[str]:
    warnings = []
    high_impact_count = sum(1 for t in trades if t.get("market_impact_status") in ["HIGH", "EXTREME"])
    if high_impact_count > 0:
        warnings.append(f"{high_impact_count} trades had HIGH/EXTREME market impact proxy.")
    return warnings

def backtest_cost_adjusted_report_to_text(result: dict[str, Any]) -> str:
    metrics = result.get("metrics", {})
    return f"Cost Adjusted Backtest:\n  Gross PnL: ${metrics.get('total_pnl', 0.0)}\n  Total Cost: ${metrics.get('total_estimated_cost_usd', 0.0)}\n  Net PnL: ${metrics.get('net_pnl_usd', 0.0)}"
