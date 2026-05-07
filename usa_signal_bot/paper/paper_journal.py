from typing import Any, Dict, List, Tuple, Optional
from datetime import datetime

from usa_signal_bot.core.enums import PaperOrderSide, PaperTradeStatus
from usa_signal_bot.paper.paper_models import PaperFill, PaperTrade, PaperPosition, create_paper_trade_id

def build_paper_trades_from_fills(fills: List[PaperFill], orders: Optional[List[Any]] = None) -> List[PaperTrade]:
    fills_by_symbol = {}
    for f in fills:
        fills_by_symbol.setdefault(f.symbol, []).append(f)

    all_trades = []

    for symbol, symbol_fills in fills_by_symbol.items():
        sorted_fills = sorted(symbol_fills, key=lambda x: x.filled_at_utc)
        closed_trades, open_trades, _ = pair_paper_buy_sell_fills(sorted_fills)
        all_trades.extend(closed_trades)
        all_trades.extend(open_trades)

    return all_trades

def pair_paper_buy_sell_fills(fills: List[PaperFill]) -> Tuple[List[PaperTrade], List[PaperTrade], List[str]]:
    closed_trades = []
    open_trades = []
    warnings = []

    if not fills:
        return closed_trades, open_trades, warnings

    symbol = fills[0].symbol
    buy_queue = []

    for fill in fills:
        if fill.side == PaperOrderSide.BUY:
            trade = PaperTrade(
                trade_id=create_paper_trade_id(symbol, fill.filled_at_utc),
                account_id=fill.account_id,
                symbol=fill.symbol,
                timeframe=fill.timeframe,
                status=PaperTradeStatus.OPEN,
                entry_order_id=fill.order_id,
                exit_order_id=None,
                entry_fill_id=fill.fill_id,
                exit_fill_id=None,
                entry_time_utc=fill.filled_at_utc,
                exit_time_utc=None,
                entry_price=fill.fill_price,
                exit_price=None,
                quantity=fill.quantity,
                gross_pnl=0.0,
                net_pnl=-fill.fees,
                total_fees=fill.fees,
                return_pct=None
            )
            buy_queue.append(trade)

        elif fill.side == PaperOrderSide.SELL:
            sell_qty = fill.quantity
            sell_price = fill.fill_price
            sell_fees = fill.fees

            while sell_qty > 1e-6 and buy_queue:
                open_trade = buy_queue[0]
                matched_qty = min(open_trade.quantity, sell_qty)
                gross_pnl = (sell_price - open_trade.entry_price) * matched_qty
                matched_sell_fee = (matched_qty / fill.quantity) * sell_fees

                if abs(matched_qty - open_trade.quantity) < 1e-6:
                    open_trade.status = PaperTradeStatus.CLOSED
                    open_trade.exit_order_id = fill.order_id
                    open_trade.exit_fill_id = fill.fill_id
                    open_trade.exit_time_utc = fill.filled_at_utc
                    open_trade.exit_price = sell_price
                    open_trade.gross_pnl += gross_pnl
                    open_trade.total_fees += matched_sell_fee
                    open_trade.net_pnl = open_trade.gross_pnl - open_trade.total_fees

                    if open_trade.entry_price > 0:
                        open_trade.return_pct = open_trade.gross_pnl / (open_trade.entry_price * open_trade.quantity)

                    closed_trades.append(open_trade)
                    buy_queue.pop(0)
                    sell_qty -= matched_qty
                else:
                    open_trade.quantity -= matched_qty
                    closed_trade = PaperTrade(
                        trade_id=f"{open_trade.trade_id}_partial",
                        account_id=open_trade.account_id,
                        symbol=open_trade.symbol,
                        timeframe=open_trade.timeframe,
                        status=PaperTradeStatus.CLOSED,
                        entry_order_id=open_trade.entry_order_id,
                        exit_order_id=fill.order_id,
                        entry_fill_id=open_trade.entry_fill_id,
                        exit_fill_id=fill.fill_id,
                        entry_time_utc=open_trade.entry_time_utc,
                        exit_time_utc=fill.filled_at_utc,
                        entry_price=open_trade.entry_price,
                        exit_price=sell_price,
                        quantity=matched_qty,
                        gross_pnl=gross_pnl,
                        total_fees=(open_trade.total_fees * (matched_qty / (open_trade.quantity + matched_qty))) + matched_sell_fee,
                        net_pnl=0.0,
                        return_pct=None
                    )

                    closed_trade.net_pnl = closed_trade.gross_pnl - closed_trade.total_fees
                    if closed_trade.entry_price > 0:
                        closed_trade.return_pct = closed_trade.gross_pnl / (closed_trade.entry_price * closed_trade.quantity)

                    closed_trades.append(closed_trade)
                    open_trade.total_fees -= (open_trade.total_fees * (matched_qty / (open_trade.quantity + matched_qty)))
                    open_trade.net_pnl = -open_trade.total_fees
                    sell_qty -= matched_qty

            if sell_qty > 1e-6:
                warnings.append(f"Unmatched sell quantity {sell_qty} for {symbol}. Short positions not fully supported.")

    return closed_trades, buy_queue, warnings

def update_open_paper_trades_with_positions(trades: List[PaperTrade], positions: List[PaperPosition]) -> List[PaperTrade]:
    pos_map = {p.symbol: p for p in positions}
    for t in trades:
        if t.status == PaperTradeStatus.OPEN:
            pos = pos_map.get(t.symbol)
            if pos and pos.market_price:
                t.metadata["unrealized_exit_price"] = pos.market_price
                t.metadata["unrealized_gross_pnl"] = (pos.market_price - t.entry_price) * t.quantity
                t.metadata["unrealized_net_pnl"] = t.metadata["unrealized_gross_pnl"] - t.total_fees

                if t.entry_price > 0:
                    t.metadata["unrealized_return_pct"] = t.metadata["unrealized_gross_pnl"] / (t.entry_price * t.quantity)

    return trades

def paper_trades_to_text(trades: List[PaperTrade], limit: int = 30) -> str:
    lines = ["--- PAPER TRADE JOURNAL ---"]
    if not trades:
        lines.append("No trades recorded.")
        return "\n".join(lines)

    sorted_trades = sorted(trades, key=lambda x: x.entry_time_utc or "9999", reverse=True)

    for t in sorted_trades[:limit]:
        status_str = t.status.value if hasattr(t.status, 'value') else t.status
        entry = f"${t.entry_price:,.2f}" if t.entry_price else "Unknown"

        if status_str == "CLOSED":
            exit_price = f"${t.exit_price:,.2f}" if t.exit_price else "Unknown"
            ret = f"{t.return_pct*100:.2f}%" if t.return_pct is not None else "Unknown"
            lines.append(
                f"{t.symbol} | {status_str} | Qty: {t.quantity:.4f} | "
                f"Entry: {entry} ({t.entry_time_utc}) | Exit: {exit_price} ({t.exit_time_utc}) | "
                f"Net PnL: ${t.net_pnl:,.2f} ({ret})"
            )
        else:
            umkt = t.metadata.get("unrealized_exit_price")
            umkt_str = f"${umkt:,.2f}" if umkt else "Unknown"
            upnl = t.metadata.get("unrealized_net_pnl", 0.0)
            lines.append(
                f"{t.symbol} | {status_str} | Qty: {t.quantity:.4f} | "
                f"Entry: {entry} ({t.entry_time_utc}) | Current Mkt: {umkt_str} | "
                f"uPnL: ${upnl:,.2f}"
            )

    if len(sorted_trades) > limit:
        lines.append(f"... and {len(sorted_trades) - limit} more")

    return "\n".join(lines)

def paper_trade_summary(trades: List[PaperTrade]) -> Dict[str, Any]:
    closed = [t for t in trades if t.status == PaperTradeStatus.CLOSED]
    open_trades = [t for t in trades if t.status == PaperTradeStatus.OPEN]

    winning = [t for t in closed if t.net_pnl > 0]
    losing = [t for t in closed if t.net_pnl <= 0]

    total_net_pnl = sum(t.net_pnl for t in closed)
    total_fees = sum(t.total_fees for t in trades)

    win_rate = len(winning) / len(closed) if closed else 0.0

    avg_win = sum(t.net_pnl for t in winning) / len(winning) if winning else 0.0
    avg_loss = sum(t.net_pnl for t in losing) / len(losing) if losing else 0.0

    return {
        "total_trades": len(trades),
        "closed_trades": len(closed),
        "open_trades": len(open_trades),
        "winning_trades": len(winning),
        "losing_trades": len(losing),
        "win_rate": round(win_rate, 4),
        "total_net_pnl": round(total_net_pnl, 2),
        "total_fees": round(total_fees, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2)
    }
