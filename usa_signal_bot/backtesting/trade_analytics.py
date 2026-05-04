from dataclasses import dataclass, field
from typing import Optional, List, Dict
from usa_signal_bot.core.exceptions import TradeAnalyticsError
from usa_signal_bot.backtesting.trade_ledger import TradeLedger, BacktestTrade

@dataclass
class StrategyTradeBreakdown:
    strategy_name: str
    total_trades: int
    win_rate: Optional[float]
    net_pnl: float
    average_trade: Optional[float]
    profit_factor: Optional[float]

@dataclass
class SymbolTradeBreakdown:
    symbol: str
    total_trades: int
    win_rate: Optional[float]
    net_pnl: float
    average_trade: Optional[float]
    best_trade: Optional[float]
    worst_trade: Optional[float]

@dataclass
class TradeAnalytics:
    total_trades: int
    closed_trades: int
    open_trades: int
    winning_trades: int
    losing_trades: int
    breakeven_trades: int
    win_rate: Optional[float]
    loss_rate: Optional[float]
    average_win: Optional[float]
    average_loss: Optional[float]
    average_trade: Optional[float]
    median_trade: Optional[float]
    best_trade: Optional[float]
    worst_trade: Optional[float]
    gross_profit: float
    gross_loss: float
    profit_factor: Optional[float]
    payoff_ratio: Optional[float]
    expectancy: Optional[float]
    average_holding_bars: Optional[float]
    total_fees: float
    total_slippage_cost: float
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def _calc_stats(trades: List[BacktestTrade]) -> dict:
    if not trades:
         return {
             "total": 0, "winning": 0, "losing": 0, "breakeven": 0,
             "gross_profit": 0.0, "gross_loss": 0.0,
             "win_rate": None, "loss_rate": None, "avg_win": None, "avg_loss": None,
             "avg_trade": None, "best": None, "worst": None,
             "profit_factor": None, "payoff_ratio": None, "expectancy": None,
             "net_pnl": 0.0
         }

    winning = [t for t in trades if t.net_pnl > 0]
    losing = [t for t in trades if t.net_pnl < 0]
    breakeven = [t for t in trades if t.net_pnl == 0]

    gross_profit = sum(t.net_pnl for t in winning)
    gross_loss = sum(t.net_pnl for t in losing)
    net_pnl = sum(t.net_pnl for t in trades)

    total = len(trades)
    win_rate = len(winning) / total if total > 0 else None
    loss_rate = len(losing) / total if total > 0 else None

    avg_win = gross_profit / len(winning) if len(winning) > 0 else None
    avg_loss = gross_loss / len(losing) if len(losing) > 0 else None
    avg_trade = net_pnl / total if total > 0 else None

    best = max((t.net_pnl for t in trades), default=None)
    worst = min((t.net_pnl for t in trades), default=None)

    pf = (gross_profit / abs(gross_loss)) if gross_loss != 0 else None

    payoff = None
    if avg_win is not None and avg_loss is not None and avg_loss != 0:
         payoff = avg_win / abs(avg_loss)

    expectancy = None
    if win_rate is not None and loss_rate is not None:
         aw = avg_win or 0.0
         al = avg_loss or 0.0
         expectancy = (win_rate * aw) + (loss_rate * al)

    return {
         "total": total, "winning": len(winning), "losing": len(losing), "breakeven": len(breakeven),
         "gross_profit": gross_profit, "gross_loss": gross_loss,
         "win_rate": win_rate, "loss_rate": loss_rate, "avg_win": avg_win, "avg_loss": avg_loss,
         "avg_trade": avg_trade, "best": best, "worst": worst,
         "profit_factor": pf, "payoff_ratio": payoff, "expectancy": expectancy,
         "net_pnl": net_pnl
    }

def calculate_trade_analytics(ledger: TradeLedger) -> TradeAnalytics:
    warnings = []
    if not ledger.closed_trades:
        warnings.append("No closed trades available for analytics calculation.")

    stats = _calc_stats(ledger.closed_trades)

    # Fees and slippage across all trades (open + closed)
    total_fees = sum(t.total_fees for t in ledger.trades)
    total_slippage = sum(t.total_slippage_cost for t in ledger.trades)

    median = None
    if ledger.closed_trades:
        sorted_pnl = sorted([t.net_pnl for t in ledger.closed_trades])
        n = len(sorted_pnl)
        if n % 2 == 1:
            median = sorted_pnl[n // 2]
        else:
            median = (sorted_pnl[n // 2 - 1] + sorted_pnl[n // 2]) / 2.0

    avg_holding_bars = None
    bars = [t.holding_bars for t in ledger.closed_trades if t.holding_bars is not None]
    if bars:
         avg_holding_bars = sum(bars) / len(bars)

    return TradeAnalytics(
        total_trades=len(ledger.trades),
        closed_trades=len(ledger.closed_trades),
        open_trades=len(ledger.open_trades),
        winning_trades=stats["winning"],
        losing_trades=stats["losing"],
        breakeven_trades=stats["breakeven"],
        win_rate=stats["win_rate"],
        loss_rate=stats["loss_rate"],
        average_win=stats["avg_win"],
        average_loss=stats["avg_loss"],
        average_trade=stats["avg_trade"],
        median_trade=median,
        best_trade=stats["best"],
        worst_trade=stats["worst"],
        gross_profit=stats["gross_profit"],
        gross_loss=stats["gross_loss"],
        profit_factor=stats["profit_factor"],
        payoff_ratio=stats["payoff_ratio"],
        expectancy=stats["expectancy"],
        average_holding_bars=avg_holding_bars,
        total_fees=total_fees,
        total_slippage_cost=total_slippage,
        warnings=warnings
    )

def calculate_strategy_trade_breakdown(ledger: TradeLedger) -> List[StrategyTradeBreakdown]:
    by_strat = {}
    for t in ledger.closed_trades:
        s = t.strategy_name or "Unknown"
        if s not in by_strat:
            by_strat[s] = []
        by_strat[s].append(t)

    breakdowns = []
    for s, trades in by_strat.items():
        stats = _calc_stats(trades)
        breakdowns.append(StrategyTradeBreakdown(
            strategy_name=s,
            total_trades=stats["total"],
            win_rate=stats["win_rate"],
            net_pnl=stats["net_pnl"],
            average_trade=stats["avg_trade"],
            profit_factor=stats["profit_factor"]
        ))
    return breakdowns

def calculate_symbol_trade_breakdown(ledger: TradeLedger) -> List[SymbolTradeBreakdown]:
    by_sym = {}
    for t in ledger.closed_trades:
        s = t.symbol
        if s not in by_sym:
            by_sym[s] = []
        by_sym[s].append(t)

    breakdowns = []
    for s, trades in by_sym.items():
        stats = _calc_stats(trades)
        breakdowns.append(SymbolTradeBreakdown(
            symbol=s,
            total_trades=stats["total"],
            win_rate=stats["win_rate"],
            net_pnl=stats["net_pnl"],
            average_trade=stats["avg_trade"],
            best_trade=stats["best"],
            worst_trade=stats["worst"]
        ))
    return breakdowns

def trade_analytics_to_dict(analytics: TradeAnalytics) -> dict:
    return {
        "total_trades": analytics.total_trades,
        "closed_trades": analytics.closed_trades,
        "open_trades": analytics.open_trades,
        "winning_trades": analytics.winning_trades,
        "losing_trades": analytics.losing_trades,
        "breakeven_trades": analytics.breakeven_trades,
        "win_rate": analytics.win_rate,
        "loss_rate": analytics.loss_rate,
        "average_win": analytics.average_win,
        "average_loss": analytics.average_loss,
        "average_trade": analytics.average_trade,
        "median_trade": analytics.median_trade,
        "best_trade": analytics.best_trade,
        "worst_trade": analytics.worst_trade,
        "gross_profit": analytics.gross_profit,
        "gross_loss": analytics.gross_loss,
        "profit_factor": analytics.profit_factor,
        "payoff_ratio": analytics.payoff_ratio,
        "expectancy": analytics.expectancy,
        "average_holding_bars": analytics.average_holding_bars,
        "total_fees": analytics.total_fees,
        "total_slippage_cost": analytics.total_slippage_cost,
        "warnings": analytics.warnings,
        "errors": analytics.errors
    }

def strategy_breakdown_to_dict(rows: List[StrategyTradeBreakdown]) -> List[dict]:
    return [{"strategy_name": r.strategy_name, "total_trades": r.total_trades, "win_rate": r.win_rate, "net_pnl": r.net_pnl, "average_trade": r.average_trade, "profit_factor": r.profit_factor} for r in rows]

def symbol_breakdown_to_dict(rows: List[SymbolTradeBreakdown]) -> List[dict]:
    return [{"symbol": r.symbol, "total_trades": r.total_trades, "win_rate": r.win_rate, "net_pnl": r.net_pnl, "average_trade": r.average_trade, "best_trade": r.best_trade, "worst_trade": r.worst_trade} for r in rows]

def trade_analytics_to_text(analytics: TradeAnalytics) -> str:
    lines = [
        "Trade Analytics Report",
        f"  Total Trades:  {analytics.total_trades}",
        f"  Closed Trades: {analytics.closed_trades}",
        f"  Open Trades:   {analytics.open_trades}",
        f"  Win Rate:      {analytics.win_rate*100:.1f}%" if analytics.win_rate is not None else "  Win Rate:      N/A",
        f"  Avg Trade:     {analytics.average_trade:.2f}" if analytics.average_trade is not None else "  Avg Trade:     N/A",
        f"  Profit Factor: {analytics.profit_factor:.2f}" if analytics.profit_factor is not None else "  Profit Factor: N/A",
        f"  Expectancy:    {analytics.expectancy:.2f}" if analytics.expectancy is not None else "  Expectancy:    N/A",
        f"  Total Fees:    {analytics.total_fees:.2f}",
        f"  Total Slippage:{analytics.total_slippage_cost:.2f}"
    ]
    if analytics.warnings:
         lines.append("  Warnings:")
         for w in analytics.warnings:
             lines.append(f"   - {w}")
    return "\n".join(lines)
