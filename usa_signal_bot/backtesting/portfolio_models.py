"""Portfolio models for the backtest engine."""
from dataclasses import dataclass, field
from typing import Any

from usa_signal_bot.core.exceptions import BacktestPortfolioError
from usa_signal_bot.backtesting.position_models import (
    BacktestPosition,
    update_position_with_fill,
    mark_position_to_market,
    position_market_value,
    create_flat_position,
    position_to_dict
)
from usa_signal_bot.backtesting.fill_models import BacktestFill

@dataclass
class BacktestPortfolio:
    """A portfolio state in the backtest engine."""
    cash: float
    starting_cash: float
    positions: dict[str, BacktestPosition]
    realized_pnl: float
    unrealized_pnl: float
    equity: float
    timestamp_utc: str | None
    warnings: list[str] = field(default_factory=list)

@dataclass
class BacktestPortfolioSnapshot:
    """A snapshot of a portfolio at a given time."""
    timestamp_utc: str
    cash: float
    equity: float
    realized_pnl: float
    unrealized_pnl: float
    gross_exposure: float
    net_exposure: float
    open_positions: int
    metadata: dict[str, Any] = field(default_factory=dict)

def create_portfolio(starting_cash: float) -> BacktestPortfolio:
    """Create a new initial portfolio."""
    return BacktestPortfolio(
        cash=starting_cash,
        starting_cash=starting_cash,
        positions={},
        realized_pnl=0.0,
        unrealized_pnl=0.0,
        equity=starting_cash,
        timestamp_utc=None
    )

def apply_fill_to_portfolio(
    portfolio: BacktestPortfolio,
    fill: BacktestFill,
    current_price: float
) -> BacktestPortfolio:
    """Apply a fill to the portfolio."""
    symbol = fill.symbol
    if symbol not in portfolio.positions:
        portfolio.positions[symbol] = create_flat_position(symbol)

    position = portfolio.positions[symbol]

    notional = fill.quantity * fill.fill_price
    total_cost = notional + fill.fees
    if fill.side.value == "BUY" and portfolio.cash < total_cost:
        portfolio.warnings.append(f"Insufficient cash for BUY {symbol}: Required {total_cost}, Have {portfolio.cash}")
        return portfolio

    result = update_position_with_fill(position, fill, current_price)

    portfolio.positions[symbol] = result.position
    portfolio.cash += result.cash_delta
    portfolio.realized_pnl += result.realized_pnl_delta
    portfolio.timestamp_utc = fill.timestamp_utc

    if result.message and "WARNING" in result.message:
        portfolio.warnings.append(result.message)

    return portfolio

def mark_portfolio_to_market(
    portfolio: BacktestPortfolio,
    prices: dict[str, float],
    timestamp_utc: str
) -> BacktestPortfolio:
    """Mark all positions to market and update total equity."""
    unrealized_pnl = 0.0
    equity = portfolio.cash

    for symbol, position in portfolio.positions.items():
        if symbol in prices:
            updated_pos = mark_position_to_market(position, prices[symbol], timestamp_utc)
            portfolio.positions[symbol] = updated_pos
            unrealized_pnl += updated_pos.unrealized_pnl
            equity += position_market_value(updated_pos, prices[symbol])
        else:
            unrealized_pnl += position.unrealized_pnl
            equity += (position.quantity * position.average_price) + position.unrealized_pnl

    portfolio.unrealized_pnl = unrealized_pnl
    portfolio.equity = equity
    portfolio.timestamp_utc = timestamp_utc

    return portfolio

def create_portfolio_snapshot(
    portfolio: BacktestPortfolio,
    prices: dict[str, float],
    timestamp_utc: str
) -> BacktestPortfolioSnapshot:
    """Create a snapshot of the current portfolio state."""
    marked_portfolio = mark_portfolio_to_market(portfolio, prices, timestamp_utc)

    gross_exposure = 0.0
    net_exposure = 0.0
    open_positions = 0

    for symbol, position in marked_portfolio.positions.items():
        if position.side.value != "FLAT":
            open_positions += 1
            price = prices.get(symbol, position.average_price)
            val = position_market_value(position, price)
            gross_exposure += abs(val)
            net_exposure += val if position.side.value == "LONG" else -val

    return BacktestPortfolioSnapshot(
        timestamp_utc=timestamp_utc,
        cash=marked_portfolio.cash,
        equity=marked_portfolio.equity,
        realized_pnl=marked_portfolio.realized_pnl,
        unrealized_pnl=marked_portfolio.unrealized_pnl,
        gross_exposure=gross_exposure,
        net_exposure=net_exposure,
        open_positions=open_positions
    )

def portfolio_to_dict(portfolio: BacktestPortfolio) -> dict:
    """Convert a portfolio to a dictionary."""
    return {
        "cash": portfolio.cash,
        "starting_cash": portfolio.starting_cash,
        "positions": {k: position_to_dict(v) for k, v in portfolio.positions.items()},
        "realized_pnl": portfolio.realized_pnl,
        "unrealized_pnl": portfolio.unrealized_pnl,
        "equity": portfolio.equity,
        "timestamp_utc": portfolio.timestamp_utc,
        "warnings": portfolio.warnings
    }

def portfolio_snapshot_to_dict(snapshot: BacktestPortfolioSnapshot) -> dict:
    """Convert a snapshot to a dictionary."""
    return {
        "timestamp_utc": snapshot.timestamp_utc,
        "cash": snapshot.cash,
        "equity": snapshot.equity,
        "realized_pnl": snapshot.realized_pnl,
        "unrealized_pnl": snapshot.unrealized_pnl,
        "gross_exposure": snapshot.gross_exposure,
        "net_exposure": snapshot.net_exposure,
        "open_positions": snapshot.open_positions,
        "metadata": snapshot.metadata
    }

def validate_portfolio(portfolio: BacktestPortfolio) -> None:
    """Validate a portfolio."""
    if portfolio.cash < 0:
        raise BacktestPortfolioError("Cash cannot be negative")
    if portfolio.starting_cash < 0:
        raise BacktestPortfolioError("Starting cash cannot be negative")
