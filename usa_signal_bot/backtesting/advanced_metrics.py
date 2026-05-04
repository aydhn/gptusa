import math
from dataclasses import dataclass, field
from typing import Optional, List, Any
from usa_signal_bot.core.enums import AdvancedMetricStatus
from usa_signal_bot.core.exceptions import AdvancedBacktestMetricError
from usa_signal_bot.backtesting.equity_curve import EquityCurve
from usa_signal_bot.backtesting.trade_ledger import TradeLedger
from usa_signal_bot.backtesting.trade_analytics import TradeAnalytics, calculate_trade_analytics
from usa_signal_bot.backtesting.drawdown_analytics import DrawdownAnalytics, calculate_drawdown_analytics

@dataclass
class AdvancedBacktestMetrics:
    status: AdvancedMetricStatus
    total_return: float
    total_return_pct: float
    annualized_return_pct: Optional[float]
    max_drawdown_pct: Optional[float]
    calmar_ratio: Optional[float]
    exposure_ratio: Optional[float]
    average_equity: Optional[float]
    equity_volatility: Optional[float]
    daily_return_mean: Optional[float]
    daily_return_std: Optional[float]
    sharpe_like_ratio: Optional[float]
    sortino_like_ratio: Optional[float]
    trade_analytics: Optional[TradeAnalytics]
    drawdown_analytics: Optional[DrawdownAnalytics]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def calculate_equity_returns(curve: EquityCurve) -> List[float]:
    if not curve.points or len(curve.points) < 2:
        return []
    returns = []
    prev_eq = curve.points[0].equity
    for pt in curve.points[1:]:
        eq = pt.equity
        if prev_eq > 0:
            returns.append((eq - prev_eq) / prev_eq)
        else:
            returns.append(0.0)
        prev_eq = eq
    return returns

def calculate_annualized_return(starting_cash: float, ending_equity: float, periods: int, periods_per_year: int = 252) -> Optional[float]:
    if starting_cash <= 0 or ending_equity <= 0 or periods <= 0:
        return None
    total_return = ending_equity / starting_cash
    return (total_return ** (periods_per_year / periods)) - 1.0

def _mean(values: List[float]) -> float:
    if not values: return 0.0
    return sum(values) / len(values)

def _std(values: List[float], mean_val: float) -> float:
    if len(values) < 2: return 0.0
    variance = sum((x - mean_val) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)

def calculate_sharpe_like_ratio(returns: List[float], periods_per_year: int = 252) -> Optional[float]:
    if not returns: return None
    mean_ret = _mean(returns)
    std_ret = _std(returns, mean_ret)
    if std_ret == 0: return None
    # Assuming risk free rate is 0 for this phase
    return (mean_ret / std_ret) * math.sqrt(periods_per_year)

def calculate_sortino_like_ratio(returns: List[float], periods_per_year: int = 252) -> Optional[float]:
    if not returns: return None
    mean_ret = _mean(returns)
    downside_returns = [r for r in returns if r < 0]
    if not downside_returns: return None

    downside_mean = 0.0 # Calculate std dev of negative returns relative to 0
    downside_variance = sum(r ** 2 for r in downside_returns) / len(returns) # use total length for sortino
    downside_std = math.sqrt(downside_variance)

    if downside_std == 0: return None
    return (mean_ret / downside_std) * math.sqrt(periods_per_year)

def calculate_exposure_ratio(snapshots: List[Any]) -> Optional[float]:
    if not snapshots: return None
    invested_points = sum(1 for s in snapshots if s.equity - s.cash > 0.01) # Small epsilon
    return invested_points / len(snapshots)

def calculate_advanced_backtest_metrics(
    starting_cash: float,
    equity_curve: EquityCurve,
    ledger: TradeLedger,
    periods_per_year: int = 252
) -> AdvancedBacktestMetrics:

    warnings = []
    if not equity_curve.points:
        warnings.append("Empty equity curve.")
        return AdvancedBacktestMetrics(
            status=AdvancedMetricStatus.EMPTY,
            total_return=0.0, total_return_pct=0.0, annualized_return_pct=None,
            max_drawdown_pct=None, calmar_ratio=None, exposure_ratio=None,
            average_equity=None, equity_volatility=None,
            daily_return_mean=None, daily_return_std=None,
            sharpe_like_ratio=None, sortino_like_ratio=None,
            trade_analytics=None, drawdown_analytics=None,
            warnings=warnings
        )

    ending_equity = equity_curve.ending_equity or starting_cash
    total_return = ending_equity - starting_cash
    total_return_pct = total_return / starting_cash if starting_cash > 0 else 0.0

    periods = len(equity_curve.points)
    ann_ret = calculate_annualized_return(starting_cash, ending_equity, periods, periods_per_year)

    max_dd_pct = equity_curve.max_drawdown_pct

    calmar = None
    if ann_ret is not None and max_dd_pct is not None and max_dd_pct > 0:
        calmar = ann_ret / max_dd_pct

    returns = calculate_equity_returns(equity_curve)
    ret_mean = _mean(returns) if returns else None
    ret_std = _std(returns, ret_mean) if returns and ret_mean is not None else None

    sharpe = calculate_sharpe_like_ratio(returns, periods_per_year)
    sortino = calculate_sortino_like_ratio(returns, periods_per_year)

    # We don't have access to snapshots directly here unless we pass them or reconstruct from curve points.
    # Curve points have cash and equity, so we can calculate exposure.
    invested_points = sum(1 for p in equity_curve.points if p.equity - p.cash > 0.01)
    exposure = invested_points / periods if periods > 0 else None

    avg_eq = _mean([p.equity for p in equity_curve.points])
    eq_std = _std([p.equity for p in equity_curve.points], avg_eq)

    trade_analytics = calculate_trade_analytics(ledger)
    drawdown_analytics = calculate_drawdown_analytics(equity_curve)

    status = AdvancedMetricStatus.OK
    if warnings:
        status = AdvancedMetricStatus.WARNING

    return AdvancedBacktestMetrics(
        status=status,
        total_return=total_return,
        total_return_pct=total_return_pct,
        annualized_return_pct=ann_ret,
        max_drawdown_pct=max_dd_pct,
        calmar_ratio=calmar,
        exposure_ratio=exposure,
        average_equity=avg_eq,
        equity_volatility=eq_std,
        daily_return_mean=ret_mean,
        daily_return_std=ret_std,
        sharpe_like_ratio=sharpe,
        sortino_like_ratio=sortino,
        trade_analytics=trade_analytics,
        drawdown_analytics=drawdown_analytics,
        warnings=warnings
    )

def advanced_metrics_to_dict(metrics: AdvancedBacktestMetrics) -> dict:
    from usa_signal_bot.backtesting.trade_analytics import trade_analytics_to_dict
    from usa_signal_bot.backtesting.drawdown_analytics import drawdown_analytics_to_dict

    ta_dict = trade_analytics_to_dict(metrics.trade_analytics) if metrics.trade_analytics else None
    dd_dict = drawdown_analytics_to_dict(metrics.drawdown_analytics) if metrics.drawdown_analytics else None

    return {
        "status": metrics.status.value if hasattr(metrics.status, 'value') else metrics.status,
        "total_return": metrics.total_return,
        "total_return_pct": metrics.total_return_pct,
        "annualized_return_pct": metrics.annualized_return_pct,
        "max_drawdown_pct": metrics.max_drawdown_pct,
        "calmar_ratio": metrics.calmar_ratio,
        "exposure_ratio": metrics.exposure_ratio,
        "average_equity": metrics.average_equity,
        "equity_volatility": metrics.equity_volatility,
        "daily_return_mean": metrics.daily_return_mean,
        "daily_return_std": metrics.daily_return_std,
        "sharpe_like_ratio": metrics.sharpe_like_ratio,
        "sortino_like_ratio": metrics.sortino_like_ratio,
        "trade_analytics": ta_dict,
        "drawdown_analytics": dd_dict,
        "warnings": metrics.warnings,
        "errors": metrics.errors
    }

def advanced_metrics_to_text(metrics: AdvancedBacktestMetrics) -> str:
    lines = [
        "=== Advanced Backtest Metrics ===",
        f"Status:             {metrics.status.value if hasattr(metrics.status, 'value') else metrics.status}",
        f"Total Return %:     {metrics.total_return_pct*100:.2f}%",
        f"Annualized Return:  {(metrics.annualized_return_pct or 0)*100:.2f}%",
        f"Max Drawdown %:     {(metrics.max_drawdown_pct or 0)*100:.2f}%",
        f"Calmar Ratio:       {metrics.calmar_ratio:.2f}" if metrics.calmar_ratio is not None else "Calmar Ratio:       N/A",
        f"Sharpe-like Ratio:  {metrics.sharpe_like_ratio:.2f}" if metrics.sharpe_like_ratio is not None else "Sharpe-like Ratio:  N/A",
        f"Sortino-like Ratio: {metrics.sortino_like_ratio:.2f}" if metrics.sortino_like_ratio is not None else "Sortino-like Ratio: N/A",
        f"Exposure Ratio:     {(metrics.exposure_ratio or 0)*100:.2f}%"
    ]
    if metrics.warnings:
         lines.append("Warnings:")
         for w in metrics.warnings:
             lines.append(f"  - {w}")
    return "\n".join(lines)
