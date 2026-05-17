from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    CurrentPortfolioState, PortfolioPosition, create_current_portfolio_state_id, create_portfolio_position_id
)

def normalize_position_payload(payload: Dict[str, Any], total_equity_usd: Optional[float] = None) -> PortfolioPosition:
    pos_id = payload.get("position_id") or create_portfolio_position_id(payload.get("symbol", "UNKNOWN"))
    symbol = payload.get("symbol", "")
    quantity = payload.get("quantity", 0.0)
    market_value_usd = payload.get("market_value_usd", 0.0)
    side = payload.get("side")
    market_price = payload.get("market_price")
    weight_pct_equity = payload.get("weight_pct_equity")

    if weight_pct_equity is None and total_equity_usd and total_equity_usd > 0:
        weight_pct_equity = (market_value_usd / total_equity_usd) * 100.0

    return PortfolioPosition(
        position_id=pos_id,
        symbol=symbol,
        quantity=quantity,
        market_value_usd=market_value_usd,
        side=side,
        market_price=market_price,
        weight_pct_equity=weight_pct_equity,
        strategy_name=payload.get("strategy_name"),
        sector=payload.get("sector"),
        cluster=payload.get("cluster"),
        regime_label=payload.get("regime_label"),
        liquidity_bucket=payload.get("liquidity_bucket"),
        cost_bucket=payload.get("cost_bucket"),
        metadata=payload.get("metadata", {})
    )

def build_current_state_from_positions(
    positions: List[Dict[str, Any]],
    total_equity_usd: Optional[float] = None,
    cash_usd: Optional[float] = None
) -> CurrentPortfolioState:

    now_str = datetime.now(timezone.utc).isoformat()
    parsed_positions = [normalize_position_payload(p, total_equity_usd) for p in positions]

    gross_exposure = sum(p.market_value_usd for p in parsed_positions)

    # Calculate net exposure
    net_exposure = 0.0
    for p in parsed_positions:
        if p.side == "SHORT":
            net_exposure -= p.market_value_usd
        else:
            net_exposure += p.market_value_usd

    warnings = []
    if total_equity_usd is None:
        warnings.append("Missing total_equity_usd, some drift percentages might not be calculated.")

    return CurrentPortfolioState(
        state_id=create_current_portfolio_state_id(),
        created_at_utc=now_str,
        gross_exposure_usd=gross_exposure,
        net_exposure_usd=net_exposure,
        positions=parsed_positions,
        total_equity_usd=total_equity_usd,
        cash_usd=cash_usd,
        warnings=warnings
    )

def build_current_state_from_paper_payload(payload: Dict[str, Any]) -> CurrentPortfolioState:
    total_equity = payload.get("total_equity_usd")
    cash = payload.get("cash_usd")
    positions = payload.get("positions", [])

    if not positions and "portfolio" in payload:
        positions = payload["portfolio"].get("positions", [])

    return build_current_state_from_positions(positions, total_equity_usd=total_equity, cash_usd=cash)

def build_empty_current_state(total_equity_usd: float = 100000.0) -> CurrentPortfolioState:
    now_str = datetime.now(timezone.utc).isoformat()
    return CurrentPortfolioState(
        state_id=create_current_portfolio_state_id(),
        created_at_utc=now_str,
        gross_exposure_usd=0.0,
        net_exposure_usd=0.0,
        positions=[],
        total_equity_usd=total_equity_usd,
        cash_usd=total_equity_usd,
        warnings=[]
    )

def current_state_symbol_map(state: CurrentPortfolioState) -> Dict[str, PortfolioPosition]:
    return {pos.symbol: pos for pos in state.positions if pos.symbol}

def current_portfolio_state_to_text(state: CurrentPortfolioState) -> str:
    lines = [f"Current Portfolio State: {state.state_id} at {state.created_at_utc}"]
    lines.append(f"Total Equity: ${state.total_equity_usd or 0:.2f}")
    lines.append(f"Gross Exposure: ${state.gross_exposure_usd:.2f}")
    lines.append(f"Net Exposure: ${state.net_exposure_usd:.2f}")
    lines.append(f"Positions ({len(state.positions)}):")
    for pos in state.positions:
        lines.append(f"  - {pos.symbol}: {pos.quantity} @ ${pos.market_value_usd:.2f} ({pos.side or 'LONG'})")
    return "\n".join(lines)
