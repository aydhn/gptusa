from datetime import datetime, timezone

from usa_signal_bot.core.enums import TransactionSide, FillSimulationStatus, MarketImpactStatus
from usa_signal_bot.transaction_costs.cost_models import (
    TransactionCostBreakdown,
    MarketImpactEstimate,
    FillSimulationResult,
    create_fill_simulation_id
)

def simulate_fill_price(
    symbol: str,
    side: TransactionSide,
    reference_price: float | None,
    cost_bps: float | None
) -> float | None:
    if reference_price is None or cost_bps is None:
        return None

    cost_multiplier = cost_bps / 10000.0

    # Buy/Cover makes entry price worse (higher)
    if side in [TransactionSide.BUY, TransactionSide.COVER, TransactionSide.LONG]:
        return reference_price * (1.0 + cost_multiplier)
    # Sell/Short makes exit price worse (lower)
    elif side in [TransactionSide.SELL, TransactionSide.SHORT]:
        return reference_price * (1.0 - cost_multiplier)

    return reference_price

def decide_fill_simulation_status(
    cost_breakdown: TransactionCostBreakdown | None,
    market_impact: MarketImpactEstimate | None
) -> FillSimulationStatus:
    if market_impact:
        if market_impact.status == MarketImpactStatus.EXTREME:
            return FillSimulationStatus.UNREALISTIC

    if not cost_breakdown or cost_breakdown.total_cost_bps is None:
        return FillSimulationStatus.INSUFFICIENT_DATA

    return FillSimulationStatus.FILLED

def simulate_fill(
    symbol: str,
    side: TransactionSide,
    quantity: float | None,
    notional_usd: float | None,
    reference_price: float | None,
    cost_breakdown: TransactionCostBreakdown | None,
    market_impact: MarketImpactEstimate | None
) -> FillSimulationResult:

    cost_bps = cost_breakdown.total_cost_bps if cost_breakdown else 0.0

    simulated_price = simulate_fill_price(symbol, side, reference_price, cost_bps)
    status = decide_fill_simulation_status(cost_breakdown, market_impact)

    warnings = []
    if status == FillSimulationStatus.UNREALISTIC:
        warnings.append("Fill simulation marked unrealistic due to extreme market impact.")

    sim_quantity = quantity
    sim_notional = notional_usd

    # Rough adjustment if we have a simulated price diff
    if sim_quantity and simulated_price and reference_price and reference_price > 0:
        # If we have fixed notional, quantity changes
        if notional_usd:
            sim_quantity = notional_usd / simulated_price
        # If we have fixed quantity, notional changes
        else:
            sim_notional = sim_quantity * simulated_price

    return FillSimulationResult(
        fill_id=create_fill_simulation_id(symbol),
        symbol=symbol,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        side=side,
        requested_quantity=quantity,
        requested_notional_usd=notional_usd,
        reference_price=reference_price,
        simulated_fill_price=simulated_price,
        simulated_filled_quantity=sim_quantity,
        simulated_filled_notional_usd=sim_notional,
        status=status,
        cost_breakdown=cost_breakdown,
        market_impact=market_impact,
        warnings=warnings,
        errors=[],
        metadata={
            "disclaimer": "This is a simulated fill based on heuristic cost models. NO REAL BROKER ORDER WAS SENT. No fill guarantee."
        }
    )

def fill_simulation_result_to_text(result: FillSimulationResult) -> str:
    lines = [
        f"Fill Simulation Result (Symbol: {result.symbol})",
        f"  Status: {result.status.value if hasattr(result.status, 'value') else result.status}",
        f"  Requested Quantity: {result.requested_quantity if result.requested_quantity is not None else 'Unknown'}",
        f"  Requested Notional: ${result.requested_notional_usd if result.requested_notional_usd is not None else 'Unknown'}",
        f"  Reference Price: ${result.reference_price if result.reference_price is not None else 'Unknown'}",
        f"  Simulated Fill Price: ${result.simulated_fill_price if result.simulated_fill_price is not None else 'Unknown'}",
        f"  Simulated Filled Quantity: {result.simulated_filled_quantity if result.simulated_filled_quantity is not None else 'Unknown'}",
        f"  Simulated Filled Notional: ${result.simulated_filled_notional_usd if result.simulated_filled_notional_usd is not None else 'Unknown'}"
    ]
    if result.warnings:
        lines.append("  Warnings:")
        for w in result.warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines)
