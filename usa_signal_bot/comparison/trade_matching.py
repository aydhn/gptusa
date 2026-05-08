from typing import Any, List, Dict, Set, Optional
from datetime import datetime

from usa_signal_bot.core.enums import MatchStatus
from usa_signal_bot.comparison.comparison_models import MatchedTradePair, create_trade_match_id

def match_paper_and_backtest_trades(paper_trades: List[Dict[str, Any]], backtest_trades: List[Dict[str, Any]], tolerance_bars: int = 1) -> List[MatchedTradePair]:
    pairs = []
    used_backtest_ids: Set[str] = set()

    for paper_trade in paper_trades:
        best_match = find_best_trade_match(paper_trade, backtest_trades, used_backtest_ids, tolerance_bars)
        if best_match:
            used_backtest_ids.add(best_match.get("trade_id", best_match.get("id", str(id(best_match)))))
            pairs.append(build_matched_trade_pair(paper_trade, best_match, MatchStatus.MATCHED))
        else:
            pairs.append(build_matched_trade_pair(paper_trade, None, MatchStatus.PAPER_ONLY))

    for bt in backtest_trades:
        bt_id = bt.get("trade_id", bt.get("id", str(id(bt))))
        if bt_id not in used_backtest_ids:
            pairs.append(build_matched_trade_pair(None, bt, MatchStatus.BACKTEST_ONLY))

    return pairs

def find_best_trade_match(paper_trade: Dict[str, Any], backtest_trades: List[Dict[str, Any]], used_backtest_ids: Set[str], tolerance_bars: int = 1) -> Optional[Dict[str, Any]]:
    p_symbol = trade_symbol(paper_trade)
    p_timeframe = trade_timeframe(paper_trade)
    p_strategy = trade_strategy_name(paper_trade)
    p_entry = trade_entry_time(paper_trade)

    candidates = []
    for bt in backtest_trades:
        bt_id = bt.get("trade_id", bt.get("id", str(id(bt))))
        if bt_id in used_backtest_ids:
            continue

        b_symbol = trade_symbol(bt)
        b_timeframe = trade_timeframe(bt)
        b_strategy = trade_strategy_name(bt)

        if p_symbol != b_symbol:
            continue
        if p_timeframe and b_timeframe and p_timeframe != b_timeframe:
            continue
        if p_strategy and b_strategy and p_strategy != b_strategy:
            continue

        candidates.append(bt)

    if not candidates:
        return None

    if p_entry:
        try:
            p_date = datetime.fromisoformat(p_entry).date()
            best_diff = None
            best_bt = None
            for bt in candidates:
                b_entry = trade_entry_time(bt)
                if not b_entry:
                    continue
                try:
                    b_date = datetime.fromisoformat(b_entry).date()
                    diff = abs((p_date - b_date).days)
                    if best_diff is None or diff < best_diff:
                        best_diff = diff
                        best_bt = bt
                except Exception:
                    pass
            if best_bt and best_diff is not None and best_diff <= tolerance_bars:
                return best_bt
        except Exception:
            pass

    return candidates[0]

def trade_symbol(trade: Dict[str, Any]) -> Optional[str]:
    return trade.get("symbol")

def trade_timeframe(trade: Dict[str, Any]) -> Optional[str]:
    return trade.get("timeframe", "1d")

def trade_strategy_name(trade: Dict[str, Any]) -> Optional[str]:
    return trade.get("strategy_name")

def trade_entry_time(trade: Dict[str, Any]) -> Optional[str]:
    return trade.get("entry_time", trade.get("entry_date"))

def trade_exit_time(trade: Dict[str, Any]) -> Optional[str]:
    return trade.get("exit_time", trade.get("exit_date"))

def trade_entry_price(trade: Dict[str, Any]) -> Optional[float]:
    return trade.get("entry_price", trade.get("average_entry_price"))

def trade_exit_price(trade: Dict[str, Any]) -> Optional[float]:
    return trade.get("exit_price", trade.get("average_exit_price"))

def trade_net_pnl(trade: Dict[str, Any]) -> Optional[float]:
    return trade.get("net_pnl", trade.get("pnl"))

def calculate_trade_price_gap_pct(paper_price: Optional[float], backtest_price: Optional[float]) -> Optional[float]:
    if paper_price is None or backtest_price is None or backtest_price == 0:
        return None
    return ((paper_price - backtest_price) / backtest_price) * 100.0

def calculate_trade_return_gap_pct(paper_pnl: Optional[float], backtest_pnl: Optional[float], base_notional: Optional[float] = None) -> Optional[float]:
    if paper_pnl is None or backtest_pnl is None:
        return None
    if base_notional and base_notional > 0:
        return ((paper_pnl - backtest_pnl) / base_notional) * 100.0
    return None

def build_matched_trade_pair(paper_trade: Optional[Dict[str, Any]], backtest_trade: Optional[Dict[str, Any]], status: MatchStatus) -> MatchedTradePair:
    p_id = paper_trade.get("trade_id", paper_trade.get("id")) if paper_trade else None
    b_id = backtest_trade.get("trade_id", backtest_trade.get("id")) if backtest_trade else None

    symbol = trade_symbol(paper_trade or backtest_trade) or "unknown"
    timeframe = trade_timeframe(paper_trade or backtest_trade) or "1d"

    match_id = create_trade_match_id(symbol, p_id, b_id)

    return MatchedTradePair(
        match_id=match_id,
        symbol=symbol,
        timeframe=timeframe,
        strategy_name=trade_strategy_name(paper_trade or backtest_trade),
        paper_trade_id=p_id,
        backtest_trade_id=b_id,
        match_status=status,
        paper_entry_time=trade_entry_time(paper_trade) if paper_trade else None,
        backtest_entry_time=trade_entry_time(backtest_trade) if backtest_trade else None,
        paper_exit_time=trade_exit_time(paper_trade) if paper_trade else None,
        backtest_exit_time=trade_exit_time(backtest_trade) if backtest_trade else None,
        paper_entry_price=trade_entry_price(paper_trade) if paper_trade else None,
        backtest_entry_price=trade_entry_price(backtest_trade) if backtest_trade else None,
        paper_exit_price=trade_exit_price(paper_trade) if paper_trade else None,
        backtest_exit_price=trade_exit_price(backtest_trade) if backtest_trade else None,
        paper_net_pnl=trade_net_pnl(paper_trade) if paper_trade else None,
        backtest_net_pnl=trade_net_pnl(backtest_trade) if backtest_trade else None,
        pnl_gap=None,
        return_gap_pct=None,
        timing_gap_bars=None,
        price_gap_pct=calculate_trade_price_gap_pct(
            trade_entry_price(paper_trade) if paper_trade else None,
            trade_entry_price(backtest_trade) if backtest_trade else None
        ),
        warnings=[],
        errors=[]
    )

def matched_trades_to_text(pairs: List[MatchedTradePair], limit: int = 30) -> str:
    lines = [f"Matched Trades (Showing up to {limit}):"]
    for p in pairs[:limit]:
        lines.append(f"  [{p.match_status.value}] {p.symbol} - Paper ID: {p.paper_trade_id} / Backtest ID: {p.backtest_trade_id}")
        if p.price_gap_pct is not None:
            lines.append(f"    Entry Price Gap: {p.price_gap_pct:.2f}%")
    return "\n".join(lines)
