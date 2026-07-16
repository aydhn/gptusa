from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    TransactionSide,
    CostAdjustmentStatus,
    CostRealismStatus,
    TransactionCostComponent,
)
from usa_signal_bot.transaction_costs.cost_models import (
    TransactionCostInput,
    TransactionCostBreakdown,
    CostAdjustedTradeResult,
    CostAdjustedTradeInput,
    FeeScheduleProxy,
    SlippageCurve,
    create_transaction_cost_breakdown_id,
    create_cost_adjusted_trade_result_id,
    FillSimulationResult,
)
from usa_signal_bot.transaction_costs.commission_estimator import (
    estimate_total_fee_proxy_usd,
    fee_proxy_to_bps,
)
from usa_signal_bot.transaction_costs.spread_cost import (
    estimate_spread_cost_bps,
    estimate_spread_cost_usd,
)
from usa_signal_bot.transaction_costs.participation_cost import (
    estimate_participation_cost_bps,
    estimate_participation_cost_usd,
)
from usa_signal_bot.transaction_costs.volatility_penalty import (
    estimate_volatility_penalty_bps,
)


def _calculate_fee_proxy(
    input_payload: TransactionCostInput,
    schedule: FeeScheduleProxy | None,
    components_bps: dict,
    components_usd: dict,
    warnings: list
) -> None:
    if schedule:
        fee_dict = estimate_total_fee_proxy_usd(
            input_payload.side,
            input_payload.quantity,
            input_payload.notional_usd,
            schedule,
        )
        fee_usd = fee_dict.get("total_fee_usd", 0.0)
        components_usd[TransactionCostComponent.COMMISSION.value] = fee_dict.get(
            "commission_usd", 0.0
        )
        components_usd[TransactionCostComponent.REGULATORY_FEE_PROXY.value] = (
            fee_dict.get("regulatory_fee_usd", 0.0)
        )

        fee_bps = fee_proxy_to_bps(fee_usd, input_payload.notional_usd)
        if fee_bps is not None:
            components_bps[TransactionCostComponent.COMMISSION.value] = (
                fee_proxy_to_bps(
                    fee_dict.get("commission_usd", 0.0), input_payload.notional_usd
                )
                or 0.0
            )
            components_bps[TransactionCostComponent.REGULATORY_FEE_PROXY.value] = (
                fee_proxy_to_bps(
                    fee_dict.get("regulatory_fee_usd", 0.0), input_payload.notional_usd
                )
                or 0.0
            )
    else:
        warnings.append("No fee schedule provided, using 0 fee.")


def _calculate_spread_cost(
    input_payload: TransactionCostInput,
    components_bps: dict,
    components_usd: dict
) -> None:
    spread_bps = estimate_spread_cost_bps(
        input_payload.spread_proxy_bps, input_payload.side
    )
    if spread_bps is not None:
        components_bps[TransactionCostComponent.SPREAD_COST.value] = spread_bps
        spread_usd = estimate_spread_cost_usd(spread_bps, input_payload.notional_usd)
        if spread_usd is not None:
            components_usd[TransactionCostComponent.SPREAD_COST.value] = spread_usd


def _calculate_participation_cost(
    input_payload: TransactionCostInput,
    components_bps: dict,
    components_usd: dict
) -> None:
    part_bps = estimate_participation_cost_bps(input_payload.participation_rate_pct)
    if part_bps is not None:
        components_bps[TransactionCostComponent.PARTICIPATION_PENALTY.value] = part_bps
        part_usd = estimate_participation_cost_usd(part_bps, input_payload.notional_usd)
        if part_usd is not None:
            components_usd[TransactionCostComponent.PARTICIPATION_PENALTY.value] = (
                part_usd
            )


def _calculate_volatility_penalty(
    input_payload: TransactionCostInput,
    components_bps: dict,
    components_usd: dict
) -> None:
    vol_bps = estimate_volatility_penalty_bps(input_payload.atr_pct)
    if vol_bps is not None:
        components_bps[TransactionCostComponent.VOLATILITY_PENALTY.value] = vol_bps
        if input_payload.notional_usd:
            components_usd[TransactionCostComponent.VOLATILITY_PENALTY.value] = (
                input_payload.notional_usd * (vol_bps / 10000.0)
            )

def build_transaction_cost_breakdown(
    input_payload: TransactionCostInput,
    schedule: FeeScheduleProxy | None = None,
    curve: SlippageCurve | None = None,
) -> TransactionCostBreakdown:

    warnings = []
    components_bps = {}
    components_usd = {}

    _calculate_fee_proxy(input_payload, schedule, components_bps, components_usd, warnings)
    _calculate_spread_cost(input_payload, components_bps, components_usd)
    _calculate_participation_cost(input_payload, components_bps, components_usd)
    _calculate_volatility_penalty(input_payload, components_bps, components_usd)

    total_bps = sum(components_bps.values()) if components_bps else None

    total_usd = 0.0
    if total_bps is not None and input_payload.notional_usd:
        total_usd = input_payload.notional_usd * (total_bps / 10000.0)
    elif components_usd:
        total_usd = sum(components_usd.values())

    return TransactionCostBreakdown(
        breakdown_id=create_transaction_cost_breakdown_id(input_payload.symbol),
        symbol=input_payload.symbol,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        side=input_payload.side,
        notional_usd=input_payload.notional_usd,
        total_cost_bps=total_bps,
        total_cost_usd=total_usd,
        components_bps=components_bps,
        components_usd=components_usd,
        status=(
            CostAdjustmentStatus.APPLIED
            if total_bps is not None
            else CostAdjustmentStatus.PARTIAL
        ),
        realism_status=CostRealismStatus.CONSERVATIVE,
        warnings=warnings,
        errors=[],
        metadata={
            "disclaimer": "This is a heuristic cost breakdown, not an official broker receipt."
        },
    )


def apply_costs_to_trade(
    input_payload: CostAdjustedTradeInput,
) -> CostAdjustedTradeResult:
    warnings = []

    symbol = input_payload.symbol
    side = input_payload.side
    gross_pnl_usd = input_payload.gross_pnl_usd
    gross_return_pct = input_payload.gross_return_pct
    notional_usd = input_payload.notional_usd
    fill_result = input_payload.fill_result

    if fill_result is None or fill_result.cost_breakdown is None:
        warnings.append("Missing cost breakdown, returning unadjusted results.")
        return CostAdjustedTradeResult(
            result_id=create_cost_adjusted_trade_result_id(symbol),
            symbol=symbol,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            side=side,
            gross_pnl_usd=gross_pnl_usd,
            total_cost_usd=0.0,
            net_pnl_usd=gross_pnl_usd,
            gross_return_pct=gross_return_pct,
            net_return_pct=gross_return_pct,
            cost_bps=0.0,
            fill_result=fill_result,
            status=CostAdjustmentStatus.SKIPPED,
            warnings=warnings,
            errors=[],
        )

    cost_usd = fill_result.cost_breakdown.total_cost_usd or 0.0
    cost_bps = fill_result.cost_breakdown.total_cost_bps or 0.0

    net_pnl = None
    if gross_pnl_usd is not None:
        net_pnl = gross_pnl_usd - cost_usd

    net_return = None
    if gross_return_pct is not None:
        # subtract cost pct (bps/100)
        net_return = gross_return_pct - (cost_bps / 100.0)

    return CostAdjustedTradeResult(
        result_id=create_cost_adjusted_trade_result_id(symbol),
        symbol=symbol,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        side=side,
        gross_pnl_usd=gross_pnl_usd,
        total_cost_usd=cost_usd,
        net_pnl_usd=net_pnl,
        gross_return_pct=gross_return_pct,
        net_return_pct=net_return,
        cost_bps=cost_bps,
        fill_result=fill_result,
        status=CostAdjustmentStatus.APPLIED,
        warnings=warnings,
        errors=[],
    )


def estimate_round_trip_cost_bps(
    entry: TransactionCostBreakdown, exit: TransactionCostBreakdown
) -> float | None:
    if entry.total_cost_bps is None or exit.total_cost_bps is None:
        return None
    return entry.total_cost_bps + exit.total_cost_bps


def estimate_round_trip_cost_usd(
    entry: TransactionCostBreakdown, exit: TransactionCostBreakdown
) -> float | None:
    if entry.total_cost_usd is None or exit.total_cost_usd is None:
        return None
    return entry.total_cost_usd + exit.total_cost_usd


def cost_adjusted_trade_result_to_text(result: CostAdjustedTradeResult) -> str:
    lines = [
        f"Cost-Adjusted Trade Result (Symbol: {result.symbol})",
        f"  Side: {result.side.value if isinstance(result.side, TransactionSide) else result.side}",
        f"  Gross PnL: ${result.gross_pnl_usd if result.gross_pnl_usd is not None else 'Unknown'}",
        f"  Total Cost: ${result.total_cost_usd if result.total_cost_usd is not None else 'Unknown'} ({result.cost_bps if result.cost_bps is not None else 'Unknown'} bps)",
        f"  Net PnL: ${result.net_pnl_usd if result.net_pnl_usd is not None else 'Unknown'}",
        (
            f"  Gross Return: {result.gross_return_pct}%"
            if result.gross_return_pct is not None
            else "  Gross Return: Unknown"
        ),
        (
            f"  Net Return: {result.net_return_pct}%"
            if result.net_return_pct is not None
            else "  Net Return: Unknown"
        ),
    ]
    if result.warnings:
        lines.append("  Warnings:")
        for w in result.warnings:
            lines.append(f"    - {w}")
    return "\n".join(lines)
