from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    TransactionSide,
    OrderSizeClass,
    SlippageCurveType,
    MarketImpactStatus,
    CostRealismStatus,
    CostAdjustmentStatus,
    FillSimulationStatus,
    TransactionCostReportType,
    LiquidityStatus,
)


@dataclass
class TransactionCostInput:
    input_id: str
    symbol: str
    side: TransactionSide
    quantity: float | None
    notional_usd: float | None
    price: float | None
    avg_dollar_volume: float | None
    atr_pct: float | None
    spread_proxy_bps: float | None
    participation_rate_pct: float | None
    liquidity_status: LiquidityStatus | str | None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TransactionCostBreakdown:
    breakdown_id: str
    symbol: str
    created_at_utc: str
    side: TransactionSide
    notional_usd: float | None
    total_cost_bps: float | None
    total_cost_usd: float | None
    components_bps: dict[str, float]
    components_usd: dict[str, float]
    status: CostAdjustmentStatus
    realism_status: CostRealismStatus
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FeeScheduleProxy:
    schedule_id: str
    name: str
    commission_per_share: float
    min_commission_usd: float
    max_commission_pct_notional: float | None
    regulatory_fee_bps_sell: float
    taf_fee_per_share_sell: float
    enabled: bool
    notes: list[str] = field(default_factory=list)


@dataclass
class SlippageCurvePoint:
    participation_rate_pct: float
    slippage_bps: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SlippageCurve:
    curve_id: str
    symbol: str | None
    curve_type: SlippageCurveType
    created_at_utc: str
    points: list[SlippageCurvePoint]
    base_spread_bps: float | None
    volatility_multiplier: float
    liquidity_multiplier: float
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MarketImpactEstimate:
    estimate_id: str
    symbol: str
    created_at_utc: str
    side: TransactionSide
    notional_usd: float | None
    participation_rate_pct: float | None
    impact_bps: float | None
    impact_usd: float | None
    status: MarketImpactStatus
    order_size_class: OrderSizeClass
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FillSimulationResult:
    fill_id: str
    symbol: str
    created_at_utc: str
    side: TransactionSide
    requested_quantity: float | None
    requested_notional_usd: float | None
    reference_price: float | None
    simulated_fill_price: float | None
    simulated_filled_quantity: float | None
    simulated_filled_notional_usd: float | None
    status: FillSimulationStatus
    cost_breakdown: TransactionCostBreakdown | None
    market_impact: MarketImpactEstimate | None
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CostAdjustedTradeInput:
    symbol: str
    side: TransactionSide
    gross_pnl_usd: float | None = None
    gross_return_pct: float | None = None
    notional_usd: float | None = None
    fill_result: FillSimulationResult | None = None


@dataclass
class CostAdjustedTradeResult:
    result_id: str
    symbol: str
    created_at_utc: str
    side: TransactionSide
    gross_pnl_usd: float | None
    total_cost_usd: float | None
    net_pnl_usd: float | None
    gross_return_pct: float | None
    net_return_pct: float | None
    cost_bps: float | None
    fill_result: FillSimulationResult | None
    status: CostAdjustmentStatus
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TransactionCostReview:
    review_id: str
    created_at_utc: str
    report_type: TransactionCostReportType
    symbols: list[str]
    cost_breakdowns: list[TransactionCostBreakdown]
    impact_estimates: list[MarketImpactEstimate]
    fill_results: list[FillSimulationResult]
    adjusted_trade_results: list[CostAdjustedTradeResult]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]


# Dictionary conversion functions
def transaction_cost_input_to_dict(payload: TransactionCostInput) -> dict:
    return {
        "input_id": payload.input_id,
        "symbol": payload.symbol,
        "side": (
            payload.side.value
            if isinstance(payload.side, TransactionSide)
            else str(payload.side)
        ),
        "quantity": payload.quantity,
        "notional_usd": payload.notional_usd,
        "price": payload.price,
        "avg_dollar_volume": payload.avg_dollar_volume,
        "atr_pct": payload.atr_pct,
        "spread_proxy_bps": payload.spread_proxy_bps,
        "participation_rate_pct": payload.participation_rate_pct,
        "liquidity_status": (
            payload.liquidity_status.value
            if hasattr(payload.liquidity_status, "value")
            else payload.liquidity_status
        ),
        "metadata": payload.metadata,
    }


def transaction_cost_breakdown_to_dict(item: TransactionCostBreakdown) -> dict:
    return {
        "breakdown_id": item.breakdown_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "side": (
            item.side.value
            if isinstance(item.side, TransactionSide)
            else str(item.side)
        ),
        "notional_usd": item.notional_usd,
        "total_cost_bps": item.total_cost_bps,
        "total_cost_usd": item.total_cost_usd,
        "components_bps": item.components_bps,
        "components_usd": item.components_usd,
        "status": (
            item.status.value
            if isinstance(item.status, CostAdjustmentStatus)
            else str(item.status)
        ),
        "realism_status": (
            item.realism_status.value
            if isinstance(item.realism_status, CostRealismStatus)
            else str(item.realism_status)
        ),
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def fee_schedule_proxy_to_dict(item: FeeScheduleProxy) -> dict:
    return {
        "schedule_id": item.schedule_id,
        "name": item.name,
        "commission_per_share": item.commission_per_share,
        "min_commission_usd": item.min_commission_usd,
        "max_commission_pct_notional": item.max_commission_pct_notional,
        "regulatory_fee_bps_sell": item.regulatory_fee_bps_sell,
        "taf_fee_per_share_sell": item.taf_fee_per_share_sell,
        "enabled": item.enabled,
        "notes": item.notes,
    }


def slippage_curve_point_to_dict(item: SlippageCurvePoint) -> dict:
    return {
        "participation_rate_pct": item.participation_rate_pct,
        "slippage_bps": item.slippage_bps,
        "metadata": item.metadata,
    }


def slippage_curve_to_dict(item: SlippageCurve) -> dict:
    return {
        "curve_id": item.curve_id,
        "symbol": item.symbol,
        "curve_type": (
            item.curve_type.value
            if isinstance(item.curve_type, SlippageCurveType)
            else str(item.curve_type)
        ),
        "created_at_utc": item.created_at_utc,
        "points": [slippage_curve_point_to_dict(p) for p in item.points],
        "base_spread_bps": item.base_spread_bps,
        "volatility_multiplier": item.volatility_multiplier,
        "liquidity_multiplier": item.liquidity_multiplier,
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def market_impact_estimate_to_dict(item: MarketImpactEstimate) -> dict:
    return {
        "estimate_id": item.estimate_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "side": (
            item.side.value
            if isinstance(item.side, TransactionSide)
            else str(item.side)
        ),
        "notional_usd": item.notional_usd,
        "participation_rate_pct": item.participation_rate_pct,
        "impact_bps": item.impact_bps,
        "impact_usd": item.impact_usd,
        "status": (
            item.status.value
            if isinstance(item.status, MarketImpactStatus)
            else str(item.status)
        ),
        "order_size_class": (
            item.order_size_class.value
            if isinstance(item.order_size_class, OrderSizeClass)
            else str(item.order_size_class)
        ),
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def fill_simulation_result_to_dict(item: FillSimulationResult) -> dict:
    return {
        "fill_id": item.fill_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "side": (
            item.side.value
            if isinstance(item.side, TransactionSide)
            else str(item.side)
        ),
        "requested_quantity": item.requested_quantity,
        "requested_notional_usd": item.requested_notional_usd,
        "reference_price": item.reference_price,
        "simulated_fill_price": item.simulated_fill_price,
        "simulated_filled_quantity": item.simulated_filled_quantity,
        "simulated_filled_notional_usd": item.simulated_filled_notional_usd,
        "status": (
            item.status.value
            if isinstance(item.status, FillSimulationStatus)
            else str(item.status)
        ),
        "cost_breakdown": (
            transaction_cost_breakdown_to_dict(item.cost_breakdown)
            if item.cost_breakdown
            else None
        ),
        "market_impact": (
            market_impact_estimate_to_dict(item.market_impact)
            if item.market_impact
            else None
        ),
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def cost_adjusted_trade_result_to_dict(item: CostAdjustedTradeResult) -> dict:
    return {
        "result_id": item.result_id,
        "symbol": item.symbol,
        "created_at_utc": item.created_at_utc,
        "side": (
            item.side.value
            if isinstance(item.side, TransactionSide)
            else str(item.side)
        ),
        "gross_pnl_usd": item.gross_pnl_usd,
        "total_cost_usd": item.total_cost_usd,
        "net_pnl_usd": item.net_pnl_usd,
        "gross_return_pct": item.gross_return_pct,
        "net_return_pct": item.net_return_pct,
        "cost_bps": item.cost_bps,
        "fill_result": (
            fill_simulation_result_to_dict(item.fill_result)
            if item.fill_result
            else None
        ),
        "status": (
            item.status.value
            if isinstance(item.status, CostAdjustmentStatus)
            else str(item.status)
        ),
        "warnings": item.warnings,
        "errors": item.errors,
        "metadata": item.metadata,
    }


def transaction_cost_review_to_dict(item: TransactionCostReview) -> dict:
    return {
        "review_id": item.review_id,
        "created_at_utc": item.created_at_utc,
        "report_type": (
            item.report_type.value
            if isinstance(item.report_type, TransactionCostReportType)
            else str(item.report_type)
        ),
        "symbols": item.symbols,
        "cost_breakdowns": [
            transaction_cost_breakdown_to_dict(b) for b in item.cost_breakdowns
        ],
        "impact_estimates": [
            market_impact_estimate_to_dict(i) for i in item.impact_estimates
        ],
        "fill_results": [fill_simulation_result_to_dict(f) for f in item.fill_results],
        "adjusted_trade_results": [
            cost_adjusted_trade_result_to_dict(r) for r in item.adjusted_trade_results
        ],
        "output_paths": item.output_paths,
        "warnings": item.warnings,
        "errors": item.errors,
    }


# Validation functions
def validate_transaction_cost_input(payload: TransactionCostInput) -> None:
    if not payload.symbol:
        raise ValueError("symbol cannot be empty")
    if payload.quantity is not None and payload.quantity < 0:
        raise ValueError("quantity cannot be negative")
    if payload.notional_usd is not None and payload.notional_usd < 0:
        raise ValueError("notional_usd cannot be negative")
    if payload.price is not None and payload.price < 0:
        raise ValueError("price cannot be negative")
    if payload.spread_proxy_bps is not None and payload.spread_proxy_bps < 0:
        raise ValueError("spread_proxy_bps cannot be negative")
    if (
        payload.participation_rate_pct is not None
        and payload.participation_rate_pct < 0
    ):
        raise ValueError("participation_rate_pct cannot be negative")


def validate_transaction_cost_breakdown(item: TransactionCostBreakdown) -> None:
    if not item.symbol:
        raise ValueError("symbol cannot be empty")
    if item.total_cost_bps is not None and item.total_cost_bps < 0:
        raise ValueError("total_cost_bps cannot be negative")
    if item.total_cost_usd is not None and item.total_cost_usd < 0:
        raise ValueError("total_cost_usd cannot be negative")


def validate_fee_schedule_proxy(item: FeeScheduleProxy) -> None:
    if item.commission_per_share < 0:
        raise ValueError("commission_per_share cannot be negative")
    if item.min_commission_usd < 0:
        raise ValueError("min_commission_usd cannot be negative")
    if (
        item.max_commission_pct_notional is not None
        and item.max_commission_pct_notional < 0
    ):
        raise ValueError("max_commission_pct_notional cannot be negative")
    if item.regulatory_fee_bps_sell < 0:
        raise ValueError("regulatory_fee_bps_sell cannot be negative")
    if item.taf_fee_per_share_sell < 0:
        raise ValueError("taf_fee_per_share_sell cannot be negative")


def validate_slippage_curve(item: SlippageCurve) -> None:
    for point in item.points:
        if point.participation_rate_pct < 0:
            raise ValueError("participation_rate_pct cannot be negative")
        if point.slippage_bps < 0:
            raise ValueError("slippage_bps cannot be negative")


def validate_market_impact_estimate(item: MarketImpactEstimate) -> None:
    if not item.symbol:
        raise ValueError("symbol cannot be empty")
    if item.impact_bps is not None and item.impact_bps < 0:
        raise ValueError("impact_bps cannot be negative")
    if item.impact_usd is not None and item.impact_usd < 0:
        raise ValueError("impact_usd cannot be negative")


def validate_fill_simulation_result(item: FillSimulationResult) -> None:
    if not item.symbol:
        raise ValueError("symbol cannot be empty")
    if item.simulated_fill_price is not None and item.simulated_fill_price < 0:
        raise ValueError("simulated_fill_price cannot be negative")


def validate_cost_adjusted_trade_result(item: CostAdjustedTradeResult) -> None:
    if not item.symbol:
        raise ValueError("symbol cannot be empty")
    if item.total_cost_usd is not None and item.total_cost_usd < 0:
        raise ValueError("total_cost_usd cannot be negative")
    if item.cost_bps is not None and item.cost_bps < 0:
        raise ValueError("cost_bps cannot be negative")
    # basic net consistency check if fields are present
    if (
        item.gross_pnl_usd is not None
        and item.total_cost_usd is not None
        and item.net_pnl_usd is not None
    ):
        expected_net = item.gross_pnl_usd - item.total_cost_usd
        if abs(expected_net - item.net_pnl_usd) > 0.001:
            raise ValueError(
                f"net_pnl_usd {item.net_pnl_usd} does not match gross {item.gross_pnl_usd} - cost {item.total_cost_usd}"
            )


# ID factories
def create_transaction_cost_input_id(symbol: str) -> str:
    return f"tc_in_{symbol.lower()}_{uuid.uuid4().hex[:8]}"


def create_transaction_cost_breakdown_id(symbol: str) -> str:
    return f"tc_brk_{symbol.lower()}_{uuid.uuid4().hex[:8]}"


def create_fee_schedule_id(name: str) -> str:
    clean_name = name.lower().replace(" ", "_").replace("-", "_")
    return f"fs_{clean_name}_{uuid.uuid4().hex[:8]}"


def create_slippage_curve_id(symbol: str | None = None) -> str:
    prefix = f"sc_{symbol.lower()}_" if symbol else "sc_"
    return f"{prefix}{uuid.uuid4().hex[:8]}"


def create_market_impact_estimate_id(symbol: str) -> str:
    return f"mi_est_{symbol.lower()}_{uuid.uuid4().hex[:8]}"


def create_fill_simulation_id(symbol: str) -> str:
    return f"fill_sim_{symbol.lower()}_{uuid.uuid4().hex[:8]}"


def create_cost_adjusted_trade_result_id(symbol: str) -> str:
    return f"adj_trade_{symbol.lower()}_{uuid.uuid4().hex[:8]}"


def create_transaction_cost_review_id(prefix: str = "tcost_review") -> str:
    return (
        f"{prefix}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    )
