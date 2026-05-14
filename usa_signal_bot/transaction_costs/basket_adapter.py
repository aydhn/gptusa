from typing import Any

from usa_signal_bot.transaction_costs.backtest_adapter import apply_transaction_costs_to_backtest_trades

def apply_transaction_costs_to_basket_result(result: dict[str, Any], config: dict[str, Any] | None = None) -> dict[str, Any]:
    if not config or not config.get("transaction_cost_model", {}).get("enabled", False):
        return result

    trades = result.get("trades", [])
    trades = apply_transaction_costs_to_backtest_trades(trades, None, config)
    result["trades"] = trades

    total_cost = sum(t.get("estimated_total_cost_usd", 0.0) for t in trades)
    metrics = result.get("metrics", {})
    metrics["total_estimated_cost_usd"] = total_cost

    gross_pnl = metrics.get("total_pnl", 0.0)
    metrics["net_pnl_usd"] = gross_pnl - total_cost
    metrics["cost_adjusted"] = True

    return result

def basket_cost_summary(result: dict[str, Any]) -> dict[str, Any]:
    trades = result.get("trades", [])
    total_cost = sum(t.get("estimated_total_cost_usd", 0.0) for t in trades)

    # Calculate simple turnover proxy
    notional_traded = sum((t.get("quantity", 0.0) * t.get("entry_price", 0.0)) for t in trades) * 2.0
    turnover_cost_bps = (total_cost / notional_traded * 10000.0) if notional_traded > 0 else 0.0

    return {
        "total_estimated_cost_usd": total_cost,
        "notional_traded_usd": notional_traded,
        "turnover_cost_bps": turnover_cost_bps
    }

def basket_cost_adjusted_equity_curve(result: dict[str, Any]) -> dict[str, Any]:
    # Placeholder for curve adjusting based on daily trade costs.
    # Needs trade execution times mapped to equity snapshot index to be exact.
    # Currently just flags it.
    curve = result.get("equity_curve", {})
    return curve

def basket_cost_warnings(result: dict[str, Any]) -> list[str]:
    trades = result.get("trades", [])
    warnings = []

    high_impact_count = sum(1 for t in trades if t.get("market_impact_status") in ["HIGH", "EXTREME"])
    if high_impact_count > 0:
        warnings.append(f"Basket simulation contains {high_impact_count} trades with HIGH/EXTREME market impact.")

    return warnings
