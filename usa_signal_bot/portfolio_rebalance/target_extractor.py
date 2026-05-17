from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.portfolio_rebalance.rebalance_models import (
    TargetPortfolioState, PortfolioPosition, create_target_portfolio_state_id, create_portfolio_position_id
)

def normalize_target_allocation(payload: Dict[str, Any], total_equity_usd: Optional[float] = None) -> PortfolioPosition:
    pos_id = payload.get("position_id") or create_portfolio_position_id(payload.get("symbol", "UNKNOWN"))
    symbol = payload.get("symbol", "")
    quantity = payload.get("target_quantity", 0.0)
    market_value_usd = payload.get("target_notional_usd", 0.0)
    side = payload.get("side")
    weight_pct_equity = payload.get("target_weight_pct")

    if weight_pct_equity is None and total_equity_usd and total_equity_usd > 0:
        weight_pct_equity = (market_value_usd / total_equity_usd) * 100.0

    return PortfolioPosition(
        position_id=pos_id,
        symbol=symbol,
        quantity=quantity,
        market_value_usd=market_value_usd,
        side=side,
        weight_pct_equity=weight_pct_equity,
        strategy_name=payload.get("strategy_name"),
        sector=payload.get("sector"),
        cluster=payload.get("cluster"),
        regime_label=payload.get("regime_label"),
        liquidity_bucket=payload.get("liquidity_bucket"),
        cost_bucket=payload.get("cost_bucket"),
        metadata=payload.get("metadata", {})
    )

def build_target_state_from_allocations(
    allocations: List[Dict[str, Any]],
    total_equity_usd: Optional[float] = None,
    source_plan_id: Optional[str] = None
) -> TargetPortfolioState:

    now_str = datetime.now(timezone.utc).isoformat()
    parsed_positions = []

    for alloc in allocations:
        status = alloc.get("status", "APPROVED")
        # BLOCKED or SUPPRESSED allocations are excluded from target
        if status in ["BLOCKED", "SUPPRESSED"]:
            continue
        parsed_positions.append(normalize_target_allocation(alloc, total_equity_usd))

    gross_exposure = sum(p.market_value_usd for p in parsed_positions)

    net_exposure = 0.0
    for p in parsed_positions:
        if p.side == "SHORT":
            net_exposure -= p.market_value_usd
        else:
            net_exposure += p.market_value_usd

    warnings = []
    if total_equity_usd is None:
        warnings.append("Missing total_equity_usd, some target percentages might not be calculated.")

    return TargetPortfolioState(
        target_id=create_target_portfolio_state_id(),
        created_at_utc=now_str,
        target_gross_exposure_usd=gross_exposure,
        target_net_exposure_usd=net_exposure,
        target_positions=parsed_positions,
        source_plan_id=source_plan_id,
        total_equity_usd=total_equity_usd,
        warnings=warnings
    )

def build_target_state_from_construction_plan(
    plan_payload: Dict[str, Any],
    total_equity_usd: Optional[float] = None
) -> TargetPortfolioState:

    plan_id = plan_payload.get("plan_id")
    allocations = plan_payload.get("final_allocations", [])

    # Try getting equity from plan if not provided
    if total_equity_usd is None:
        capital_state = plan_payload.get("capital_state", {})
        total_equity_usd = capital_state.get("total_equity_usd")

    return build_target_state_from_allocations(allocations, total_equity_usd, plan_id)

def target_state_symbol_map(state: TargetPortfolioState) -> Dict[str, PortfolioPosition]:
    return {pos.symbol: pos for pos in state.target_positions if pos.symbol}

def target_portfolio_state_to_text(state: TargetPortfolioState) -> str:
    lines = [f"Target Portfolio State: {state.target_id} at {state.created_at_utc}"]
    if state.source_plan_id:
        lines.append(f"Source Plan: {state.source_plan_id}")
    lines.append(f"Total Equity: ${state.total_equity_usd or 0:.2f}")
    lines.append(f"Target Gross Exposure: ${state.target_gross_exposure_usd:.2f}")
    lines.append(f"Target Net Exposure: ${state.target_net_exposure_usd:.2f}")
    lines.append(f"Target Positions ({len(state.target_positions)}):")
    for pos in state.target_positions:
        lines.append(f"  - {pos.symbol}: {pos.quantity} @ ${pos.market_value_usd:.2f} ({pos.side or 'LONG'})")
    return "\n".join(lines)
