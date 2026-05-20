from typing import Any, Dict, List
from usa_signal_bot.paper_shadow.shadow_models import (
    ShadowSimulationContext, ShadowPortfolioState, ShadowPosition, ShadowFill,
    create_shadow_portfolio_id, get_utc_now_str
)

def initialize_shadow_portfolio(context: ShadowSimulationContext) -> ShadowPortfolioState:
    return ShadowPortfolioState(
        portfolio_id=create_shadow_portfolio_id(),
        created_at_utc=get_utc_now_str(),
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
    return ShadowPosition(
        symbol=symbol,
        quantity=quantity,
        avg_price=price,
        market_price=price,
        market_value_usd=quantity * (price or 0.0),
        unrealized_pnl_usd=0.0,
        realized_pnl_usd=0.0,
        strategy_name=strategy_name
    )

def update_shadow_portfolio_with_fill(portfolio: ShadowPortfolioState, fill: ShadowFill) -> ShadowPortfolioState:
    if fill.status != "SIMULATED_FILLED" and fill.status != "SIMULATED_PARTIAL":
        return portfolio

    fill_price = fill.fill_price or 0.0
    fill_qty = fill.filled_quantity if fill.side == "BUY" else -fill.filled_quantity

    # Very simple mock portfolio update
    cost = abs(fill_qty) * fill_price + fill.simulated_cost_usd + fill.simulated_slippage_usd

    found = False
    for pos in portfolio.positions:
        if pos.symbol == fill.symbol:
            pos.quantity += fill_qty
            pos.market_value_usd = abs(pos.quantity) * (pos.market_price or fill_price)
            found = True
            break

    if not found and fill_qty != 0:
        portfolio.positions.append(build_shadow_position(fill.symbol, fill_qty, fill_price))

    portfolio.cash_usd -= (fill_qty * fill_price + fill.simulated_cost_usd + fill.simulated_slippage_usd)

    # Recalculate exposures
    portfolio.gross_exposure_usd = sum(p.market_value_usd for p in portfolio.positions)
    portfolio.net_exposure_usd = sum(p.market_value_usd * (1 if p.quantity > 0 else -1) for p in portfolio.positions)
    portfolio.equity_usd = portfolio.cash_usd + portfolio.gross_exposure_usd

    return portfolio

def calculate_shadow_exposures(portfolio: ShadowPortfolioState) -> Dict[str, float]:
    return {
        "gross_exposure_usd": portfolio.gross_exposure_usd,
        "net_exposure_usd": portfolio.net_exposure_usd,
        "cash_usd": portfolio.cash_usd
    }

def shadow_portfolio_summary(portfolio: ShadowPortfolioState) -> Dict[str, Any]:
    return {
        "portfolio_id": portfolio.portfolio_id,
        "equity_usd": portfolio.equity_usd,
        "position_count": len(portfolio.positions)
    }

def shadow_portfolio_to_text(portfolio: ShadowPortfolioState) -> str:
    return f"ShadowPortfolio({portfolio.portfolio_id}, eq={portfolio.equity_usd}, pos={len(portfolio.positions)})"
