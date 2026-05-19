from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowPortfolioState,
    ShadowPosition,
    ShadowSimulationContext,
    ShadowFill,
    create_shadow_portfolio_id
)

def initialize_shadow_portfolio(context: ShadowSimulationContext) -> ShadowPortfolioState:
    return ShadowPortfolioState(
        portfolio_id=create_shadow_portfolio_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        equity_usd=context.starting_equity_usd,
        cash_usd=context.starting_equity_usd,
        positions=[],
        gross_exposure_usd=0.0,
        net_exposure_usd=0.0,
        realized_pnl_usd=0.0,
        unrealized_pnl_usd=0.0,
        warnings=[],
        errors=[]
    )

def build_shadow_position(symbol: str, quantity: float, price: float | None, strategy_name: str | None = None) -> ShadowPosition:
    market_val = quantity * (price if price is not None else 0.0)
    return ShadowPosition(
        symbol=symbol,
        quantity=quantity,
        avg_price=price,
        market_price=price,
        market_value_usd=market_val,
        unrealized_pnl_usd=0.0,
        realized_pnl_usd=0.0,
        strategy_name=strategy_name
    )

def update_shadow_portfolio_with_fill(portfolio: ShadowPortfolioState, fill: ShadowFill) -> ShadowPortfolioState:
    # Simplified update for simulation
    cost = fill.filled_quantity * (fill.fill_price if fill.fill_price else 0.0)
    if fill.side.upper() == "BUY":
        portfolio.cash_usd -= cost
        pos = next((p for p in portfolio.positions if p.symbol == fill.symbol), None)
        if pos:
            pos.quantity += fill.filled_quantity
            pos.avg_price = fill.fill_price # Simplified avg price
            pos.market_value_usd = pos.quantity * (fill.fill_price if fill.fill_price else 0.0)
        else:
            portfolio.positions.append(build_shadow_position(fill.symbol, fill.filled_quantity, fill.fill_price))
    elif fill.side.upper() == "SELL":
        portfolio.cash_usd += cost
        pos = next((p for p in portfolio.positions if p.symbol == fill.symbol), None)
        if pos:
            pos.quantity -= fill.filled_quantity
            pos.market_value_usd = pos.quantity * (fill.fill_price if fill.fill_price else 0.0)
            if pos.quantity <= 0:
                portfolio.positions.remove(pos)

    exposures = calculate_shadow_exposures(portfolio)
    portfolio.gross_exposure_usd = exposures["gross"]
    portfolio.net_exposure_usd = exposures["net"]
    portfolio.equity_usd = portfolio.cash_usd + portfolio.gross_exposure_usd
    return portfolio

def calculate_shadow_exposures(portfolio: ShadowPortfolioState) -> dict[str, float]:
    gross = sum(abs(p.market_value_usd) for p in portfolio.positions)
    net = sum(p.market_value_usd for p in portfolio.positions)
    return {"gross": gross, "net": net}

def shadow_portfolio_summary(portfolio: ShadowPortfolioState) -> dict[str, Any]:
    return {
        "portfolio_id": portfolio.portfolio_id,
        "equity_usd": portfolio.equity_usd,
        "cash_usd": portfolio.cash_usd,
        "position_count": len(portfolio.positions)
    }

def shadow_portfolio_to_text(portfolio: ShadowPortfolioState) -> str:
    summary = shadow_portfolio_summary(portfolio)
    text = "Shadow Portfolio\n"
    text += f"ID: {summary['portfolio_id']}\n"
    text += f"Equity: ${summary['equity_usd']:.2f}\n"
    text += f"Cash: ${summary['cash_usd']:.2f}\n"
    text += f"Positions: {summary['position_count']}\n"
    return text
