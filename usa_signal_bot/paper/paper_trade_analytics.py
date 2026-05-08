from typing import List, Tuple, Optional
from usa_signal_bot.paper.paper_models import PaperTrade
from usa_signal_bot.paper.paper_analytics_models import PaperTradeMetrics
from usa_signal_bot.core.enums import PaperMetricStatus, PaperTradeStatus

def filter_closed_paper_trades(trades: List[PaperTrade]) -> List[PaperTrade]:
    return [t for t in trades if t.status == PaperTradeStatus.CLOSED]

def filter_open_paper_trades(trades: List[PaperTrade]) -> List[PaperTrade]:
    return [t for t in trades if t.status == PaperTradeStatus.OPEN]

def calculate_paper_win_rate(closed_trades: List[PaperTrade]) -> Optional[float]:
    if not closed_trades:
        return None
    winning_trades = sum(1 for t in closed_trades if t.net_pnl > 0)
    return winning_trades / len(closed_trades)

def calculate_paper_profit_factor(closed_trades: List[PaperTrade]) -> Optional[float]:
    if not closed_trades:
        return None
    gross_profit = sum(t.net_pnl for t in closed_trades if t.net_pnl > 0)
    gross_loss = abs(sum(t.net_pnl for t in closed_trades if t.net_pnl < 0))
    if gross_loss == 0:
        return None if gross_profit > 0 else 1.0 # undefined
    return gross_profit / gross_loss

def calculate_paper_expectancy(closed_trades: List[PaperTrade]) -> Optional[float]:
    if not closed_trades:
        return None
    net_pnl = sum(t.net_pnl for t in closed_trades)
    return net_pnl / len(closed_trades)

def calculate_average_win_loss(closed_trades: List[PaperTrade]) -> Tuple[Optional[float], Optional[float]]:
    wins = [t.net_pnl for t in closed_trades if t.net_pnl > 0]
    losses = [t.net_pnl for t in closed_trades if t.net_pnl < 0]

    avg_win = sum(wins) / len(wins) if wins else None
    avg_loss = sum(losses) / len(losses) if losses else None
    return avg_win, avg_loss

def calculate_best_worst_trade(closed_trades: List[PaperTrade]) -> Tuple[Optional[float], Optional[float]]:
    if not closed_trades:
        return None, None
    pnls = [t.net_pnl for t in closed_trades]
    return max(pnls), min(pnls)

def calculate_win_loss_streaks(closed_trades: List[PaperTrade]) -> Tuple[int, int]:
    if not closed_trades:
        return 0, 0

    max_win = 0
    max_loss = 0
    curr_win = 0
    curr_loss = 0

    for t in closed_trades:
        if t.net_pnl > 0:
            curr_win += 1
            curr_loss = 0
            if curr_win > max_win: max_win = curr_win
        elif t.net_pnl < 0:
            curr_loss += 1
            curr_win = 0
            if curr_loss > max_loss: max_loss = curr_loss
        else:
            curr_win = 0
            curr_loss = 0

    return max_win, max_loss

def calculate_paper_trade_metrics(trades: List[PaperTrade]) -> PaperTradeMetrics:
    if not trades:
        return PaperTradeMetrics(
            status=PaperMetricStatus.EMPTY,
            total_trades=0, closed_trades=0, open_trades=0,
            winning_trades=0, losing_trades=0, breakeven_trades=0,
            win_rate=None, loss_rate=None, average_win=None, average_loss=None, average_trade=None,
            gross_profit=0.0, gross_loss=0.0, net_pnl=0.0,
            profit_factor=None, expectancy=None, best_trade=None, worst_trade=None,
            max_win_streak=0, max_loss_streak=0,
            warnings=["No trades provided."], errors=[]
        )

    closed = filter_closed_paper_trades(trades)
    open_trades = filter_open_paper_trades(trades)

    if not closed:
        return PaperTradeMetrics(
            status=PaperMetricStatus.INSUFFICIENT_DATA,
            total_trades=len(trades), closed_trades=0, open_trades=len(open_trades),
            winning_trades=0, losing_trades=0, breakeven_trades=0,
            win_rate=None, loss_rate=None, average_win=None, average_loss=None, average_trade=None,
            gross_profit=0.0, gross_loss=0.0, net_pnl=0.0,
            profit_factor=None, expectancy=None, best_trade=None, worst_trade=None,
            max_win_streak=0, max_loss_streak=0,
            warnings=["No closed trades available for metrics."], errors=[]
        )

    winning = [t for t in closed if t.net_pnl > 0]
    losing = [t for t in closed if t.net_pnl < 0]
    breakeven = [t for t in closed if t.net_pnl == 0]

    win_rate = calculate_paper_win_rate(closed)
    loss_rate = len(losing) / len(closed) if closed else None

    avg_win, avg_loss = calculate_average_win_loss(closed)
    expectancy = calculate_paper_expectancy(closed)

    gross_profit = sum(t.net_pnl for t in winning)
    gross_loss = abs(sum(t.net_pnl for t in losing))
    net_pnl = sum(t.net_pnl for t in closed)

    profit_factor = calculate_paper_profit_factor(closed)
    best, worst = calculate_best_worst_trade(closed)
    max_win_streak, max_loss_streak = calculate_win_loss_streaks(closed)

    return PaperTradeMetrics(
        status=PaperMetricStatus.OK,
        total_trades=len(trades),
        closed_trades=len(closed),
        open_trades=len(open_trades),
        winning_trades=len(winning),
        losing_trades=len(losing),
        breakeven_trades=len(breakeven),
        win_rate=win_rate,
        loss_rate=loss_rate,
        average_win=avg_win,
        average_loss=avg_loss,
        average_trade=expectancy,
        gross_profit=gross_profit,
        gross_loss=gross_loss,
        net_pnl=net_pnl,
        profit_factor=profit_factor,
        expectancy=expectancy,
        best_trade=best,
        worst_trade=worst,
        max_win_streak=max_win_streak,
        max_loss_streak=max_loss_streak,
        warnings=[],
        errors=[]
    )

def paper_trade_metrics_to_text(metrics: PaperTradeMetrics) -> str:
    lines = [
        "--- Paper Trade Metrics ---",
        f"Status: {metrics.status.value}",
        f"Total Trades: {metrics.total_trades} (Closed: {metrics.closed_trades}, Open: {metrics.open_trades})",
        f"Win/Loss/Breakeven: {metrics.winning_trades} / {metrics.losing_trades} / {metrics.breakeven_trades}"
    ]
    if metrics.win_rate is not None:
        lines.append(f"Win Rate: {metrics.win_rate * 100:.2f}%")
    if metrics.profit_factor is not None:
        lines.append(f"Profit Factor: {metrics.profit_factor:.2f}")
    if metrics.expectancy is not None:
        lines.append(f"Expectancy: {metrics.expectancy:.2f}")

    lines.append(f"Gross Profit: {metrics.gross_profit:.2f}")
    lines.append(f"Gross Loss: {metrics.gross_loss:.2f}")
    lines.append(f"Net PnL: {metrics.net_pnl:.2f}")

    if metrics.average_win is not None:
         lines.append(f"Avg Win: {metrics.average_win:.2f}")
    if metrics.average_loss is not None:
         lines.append(f"Avg Loss: {metrics.average_loss:.2f}")

    lines.append(f"Max Win Streak: {metrics.max_win_streak}")
    lines.append(f"Max Loss Streak: {metrics.max_loss_streak}")

    if metrics.warnings:
        lines.append("\nWarnings: " + ", ".join(metrics.warnings))
    if metrics.errors:
        lines.append("\nErrors: " + ", ".join(metrics.errors))

    lines.append("")
    return "\n".join(lines)
