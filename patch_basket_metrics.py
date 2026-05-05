def fix():
    with open("usa_signal_bot/backtesting/basket_metrics.py", "r") as f:
        content = f.read()

    new_dict_fn = """
def basket_metrics_to_dict(metrics: BasketMetrics) -> dict:
    return {
        "status": metrics.status.value,
        "starting_cash": metrics.starting_cash,
        "ending_equity": metrics.ending_equity,
        "total_return_pct": metrics.total_return_pct,
        "max_drawdown_pct": metrics.max_drawdown_pct,
        "total_fills": metrics.total_fills,
        "total_trades": metrics.total_trades,
        "open_positions_final": metrics.open_positions_final,
        "average_gross_exposure": metrics.average_gross_exposure,
        "max_gross_exposure": metrics.max_gross_exposure,
        "average_allocation_drift": metrics.average_allocation_drift,
        "max_allocation_drift": metrics.max_allocation_drift,
        "basket_turnover_proxy": metrics.basket_turnover_proxy,
        "total_fees": metrics.total_fees,
        "total_slippage_cost": metrics.total_slippage_cost,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }
"""
    if "basket_metrics_to_dict" not in content:
        content = content + "\n" + new_dict_fn

    with open("usa_signal_bot/backtesting/basket_metrics.py", "w") as f:
        f.write(content)

if __name__ == "__main__":
    fix()
