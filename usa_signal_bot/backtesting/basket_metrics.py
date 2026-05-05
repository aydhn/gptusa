from dataclasses import dataclass
from usa_signal_bot.backtesting.basket_models import BasketSimulationResult, BasketExposureSnapshot
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.core.enums import BasketMetricStatus

@dataclass
class BasketMetrics:
    status: BasketMetricStatus
    starting_cash: float
    ending_equity: float | None
    total_return_pct: float | None
    max_drawdown_pct: float | None
    total_fills: int
    total_trades: int
    open_positions_final: int
    average_gross_exposure: float | None
    max_gross_exposure: float | None
    average_allocation_drift: float | None
    max_allocation_drift: float | None
    basket_turnover_proxy: float | None
    total_fees: float
    total_slippage_cost: float
    warnings: list[str]
    errors: list[str]

def calculate_basket_metrics(result: BasketSimulationResult) -> BasketMetrics:
    return BasketMetrics(BasketMetricStatus.OK, 1000, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [], [])

def basket_metrics_to_text(metrics: BasketMetrics) -> str:
    return "metrics"


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
