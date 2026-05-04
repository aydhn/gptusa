from dataclasses import dataclass, field
from typing import Any, Optional, Tuple, List, Dict
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import TradeStatus, TradeDirection, TradeExitReason, BacktestOrderSide
from usa_signal_bot.core.exceptions import TradeLedgerError
from usa_signal_bot.backtesting.fill_models import BacktestFill
from usa_signal_bot.strategies.signal_contract import StrategySignal

@dataclass
class BacktestTrade:
    trade_id: str
    symbol: str
    timeframe: str
    direction: TradeDirection
    status: TradeStatus
    entry_fill_id: Optional[str]
    exit_fill_id: Optional[str]
    entry_time_utc: Optional[str]
    exit_time_utc: Optional[str]
    entry_price: Optional[float]
    exit_price: Optional[float]
    quantity: float
    gross_pnl: float
    net_pnl: float
    total_fees: float
    total_slippage_cost: float
    return_pct: Optional[float]
    holding_bars: Optional[int]
    holding_seconds: Optional[float]
    exit_reason: TradeExitReason
    signal_id: Optional[str]
    strategy_name: Optional[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class TradeLedger:
    ledger_id: str
    trades: List[BacktestTrade]
    open_trades: List[BacktestTrade]
    closed_trades: List[BacktestTrade]
    created_at_utc: str
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

def create_trade_id(symbol: str, entry_time_utc: Optional[str], signal_id: Optional[str] = None) -> str:
    base = f"{symbol}_{entry_time_utc or 'unknown'}"
    if signal_id:
        base += f"_{signal_id[:8]}"
    return f"{base}_{str(uuid.uuid4())[:8]}"

def calculate_trade_pnl(entry_fill: BacktestFill, exit_fill: BacktestFill) -> Tuple[float, float]:
    """Calculates gross and net PnL for a trade pair."""
    # Assuming Long trades only for now based on Phase 26 requirements
    gross_pnl = (exit_fill.fill_price - entry_fill.fill_price) * entry_fill.quantity

    # Fees are deducted from Net PnL.
    total_fees = entry_fill.transaction_cost + exit_fill.transaction_cost

    # Slippage is already baked into fill_price, so we don't deduct it again for Net PnL.
    net_pnl = gross_pnl - total_fees
    return gross_pnl, net_pnl

def calculate_trade_return_pct(entry_price: float, exit_price: float, direction: TradeDirection) -> Optional[float]:
    if entry_price <= 0:
        return None
    if direction == TradeDirection.LONG:
        return (exit_price - entry_price) / entry_price
    elif direction == TradeDirection.SHORT:
        return (entry_price - exit_price) / entry_price
    return 0.0

def _parse_time(time_str: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    except (ValueError, TypeError):
        return None

def pair_long_fills_into_trades(fills: List[BacktestFill], signals_by_id: Optional[Dict[str, StrategySignal]] = None) -> Tuple[List[BacktestTrade], List[BacktestTrade], List[str]]:
    """Pairs BUY and SELL fills into trades using FIFO."""
    warnings = []
    closed_trades = []
    open_trades = []

    # Group fills by symbol
    fills_by_symbol = {}
    for f in fills:
        if f.symbol not in fills_by_symbol:
            fills_by_symbol[f.symbol] = []
        fills_by_symbol[f.symbol].append(f)

    for symbol, sym_fills in fills_by_symbol.items():
        # Sort by timestamp to ensure FIFO
        sym_fills.sort(key=lambda x: x.timestamp_utc)

        open_buys = []

        for fill in sym_fills:
            if fill.side == BacktestOrderSide.BUY:
                open_buys.append(fill)
            elif fill.side == BacktestOrderSide.SELL:
                if not open_buys:
                    warnings.append(f"Oversell or missing BUY fill for {symbol} at {fill.timestamp_utc}")
                    continue

                # Simple FIFO pairing - assuming full quantity matching for Phase 26
                entry_fill = open_buys.pop(0)

                # In a real scenario, we might have partial fills and need quantity tracking.
                # For Phase 26 simplicity, we assume matching quantities.
                qty = min(entry_fill.quantity, fill.quantity)

                if fill.quantity != entry_fill.quantity:
                     warnings.append(f"Partial fill pairing not fully supported. Entry: {entry_fill.quantity}, Exit: {fill.quantity}")

                gross_pnl, net_pnl = calculate_trade_pnl(entry_fill, fill)
                return_pct = calculate_trade_return_pct(entry_fill.fill_price, fill.fill_price, TradeDirection.LONG)

                total_fees = entry_fill.transaction_cost + fill.transaction_cost

                # Get slippage from breakdown if available, else fallback to old slippage logic
                entry_slippage_cost = entry_fill.slippage_breakdown.get('total_slippage_cost', 0.0) if hasattr(entry_fill, 'slippage_breakdown') and entry_fill.slippage_breakdown else 0.0
                exit_slippage_cost = fill.slippage_breakdown.get('total_slippage_cost', 0.0) if hasattr(fill, 'slippage_breakdown') and fill.slippage_breakdown else 0.0

                # If using legacy simulation, slippage_breakdown is empty, but we might want to estimate. For Phase 26, rely on the breakdown.
                total_slippage_cost = entry_slippage_cost + exit_slippage_cost

                strategy_name = None
                if signals_by_id and entry_fill.signal_id and entry_fill.signal_id in signals_by_id:
                     strategy_name = signals_by_id[entry_fill.signal_id].strategy_name

                # Calculate holding time
                holding_seconds = None
                entry_dt = _parse_time(entry_fill.timestamp_utc)
                exit_dt = _parse_time(fill.timestamp_utc)
                if entry_dt and exit_dt:
                    holding_seconds = (exit_dt - entry_dt).total_seconds()

                trade = BacktestTrade(
                    trade_id=create_trade_id(symbol, entry_fill.timestamp_utc, entry_fill.signal_id),
                    symbol=symbol,
                    timeframe=entry_fill.timeframe,
                    direction=TradeDirection.LONG,
                    status=TradeStatus.CLOSED,
                    entry_fill_id=entry_fill.fill_id,
                    exit_fill_id=fill.fill_id,
                    entry_time_utc=entry_fill.timestamp_utc,
                    exit_time_utc=fill.timestamp_utc,
                    entry_price=entry_fill.fill_price,
                    exit_price=fill.fill_price,
                    quantity=qty,
                    gross_pnl=gross_pnl,
                    net_pnl=net_pnl,
                    total_fees=total_fees,
                    total_slippage_cost=total_slippage_cost,
                    return_pct=return_pct,
                    holding_bars=None,  # Need bar indices to calculate accurately
                    holding_seconds=holding_seconds,
                    exit_reason=TradeExitReason.UNKNOWN, # Could parse reason from fill
                    signal_id=entry_fill.signal_id,
                    strategy_name=strategy_name
                )
                closed_trades.append(trade)

        # Any remaining buys are open trades
        for entry_fill in open_buys:
             strategy_name = None
             if signals_by_id and entry_fill.signal_id and entry_fill.signal_id in signals_by_id:
                  strategy_name = signals_by_id[entry_fill.signal_id].strategy_name

             entry_slippage_cost = entry_fill.slippage_breakdown.get('total_slippage_cost', 0.0) if hasattr(entry_fill, 'slippage_breakdown') and entry_fill.slippage_breakdown else 0.0

             trade = BacktestTrade(
                    trade_id=create_trade_id(symbol, entry_fill.timestamp_utc, entry_fill.signal_id),
                    symbol=symbol,
                    timeframe=entry_fill.timeframe,
                    direction=TradeDirection.LONG,
                    status=TradeStatus.OPEN,
                    entry_fill_id=entry_fill.fill_id,
                    exit_fill_id=None,
                    entry_time_utc=entry_fill.timestamp_utc,
                    exit_time_utc=None,
                    entry_price=entry_fill.fill_price,
                    exit_price=None,
                    quantity=entry_fill.quantity,
                    gross_pnl=0.0,
                    net_pnl=-entry_fill.transaction_cost, # Just fees so far
                    total_fees=entry_fill.transaction_cost,
                    total_slippage_cost=entry_slippage_cost,
                    return_pct=0.0,
                    holding_bars=None,
                    holding_seconds=None,
                    exit_reason=TradeExitReason.UNKNOWN,
                    signal_id=entry_fill.signal_id,
                    strategy_name=strategy_name
                )
             open_trades.append(trade)

    return closed_trades, open_trades, warnings

def build_trade_ledger_from_fills(fills: List[BacktestFill], signals_by_id: Optional[Dict[str, StrategySignal]] = None) -> TradeLedger:
    closed_trades, open_trades, warnings = pair_long_fills_into_trades(fills, signals_by_id)
    all_trades = closed_trades + open_trades

    return TradeLedger(
        ledger_id=str(uuid.uuid4()),
        trades=all_trades,
        open_trades=open_trades,
        closed_trades=closed_trades,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        warnings=warnings
    )

def trade_to_dict(trade: BacktestTrade) -> dict:
    return {
        "trade_id": trade.trade_id,
        "symbol": trade.symbol,
        "timeframe": trade.timeframe,
        "direction": trade.direction.value if hasattr(trade.direction, 'value') else trade.direction,
        "status": trade.status.value if hasattr(trade.status, 'value') else trade.status,
        "entry_fill_id": trade.entry_fill_id,
        "exit_fill_id": trade.exit_fill_id,
        "entry_time_utc": trade.entry_time_utc,
        "exit_time_utc": trade.exit_time_utc,
        "entry_price": trade.entry_price,
        "exit_price": trade.exit_price,
        "quantity": trade.quantity,
        "gross_pnl": trade.gross_pnl,
        "net_pnl": trade.net_pnl,
        "total_fees": trade.total_fees,
        "total_slippage_cost": trade.total_slippage_cost,
        "return_pct": trade.return_pct,
        "holding_bars": trade.holding_bars,
        "holding_seconds": trade.holding_seconds,
        "exit_reason": trade.exit_reason.value if hasattr(trade.exit_reason, 'value') else trade.exit_reason,
        "signal_id": trade.signal_id,
        "strategy_name": trade.strategy_name,
        "metadata": trade.metadata
    }

def ledger_to_dict(ledger: TradeLedger) -> dict:
    return {
        "ledger_id": ledger.ledger_id,
        "created_at_utc": ledger.created_at_utc,
        "warnings": ledger.warnings,
        "errors": ledger.errors,
        "trades_count": len(ledger.trades),
        "open_trades_count": len(ledger.open_trades),
        "closed_trades_count": len(ledger.closed_trades)
        # Trades array typically stored separately in JSONL
    }

def ledger_to_text(ledger: TradeLedger, limit: int = 20) -> str:
    lines = [
        f"Trade Ledger Summary (ID: {ledger.ledger_id[:8]})",
        f"Total Trades: {len(ledger.trades)} (Closed: {len(ledger.closed_trades)}, Open: {len(ledger.open_trades)})",
    ]
    if ledger.warnings:
        lines.append("Warnings:")
        for w in ledger.warnings[:5]:
            lines.append(f"  - {w}")

    lines.append("\nRecent Closed Trades:")
    for trade in sorted(ledger.closed_trades, key=lambda x: x.exit_time_utc or "", reverse=True)[:limit]:
        lines.append(f"  {trade.symbol} | {trade.direction.value} | Qty: {trade.quantity:.2f} | Net PnL: {trade.net_pnl:.2f} | Entry: {trade.entry_price:.2f} | Exit: {trade.exit_price:.2f}")

    return "\n".join(lines)

def validate_trade(trade: BacktestTrade) -> None:
    if trade.quantity <= 0:
        raise TradeLedgerError(f"Trade quantity must be positive. ID: {trade.trade_id}")
    if trade.status == TradeStatus.CLOSED and (not trade.exit_time_utc or trade.exit_price is None):
         raise TradeLedgerError(f"Closed trade missing exit data. ID: {trade.trade_id}")

def validate_trade_ledger(ledger: TradeLedger) -> None:
    for trade in ledger.trades:
        validate_trade(trade)
