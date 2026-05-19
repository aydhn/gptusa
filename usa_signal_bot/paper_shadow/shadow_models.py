from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime
import uuid

from usa_signal_bot.core.enums import (
    ShadowSessionStatus,
    ShadowRuntimeMode,
    ShadowLedgerEventType,
    ShadowOrderIntentStatus,
    ShadowFillStatus,
    ShadowRiskGateStatus,
    ShadowSafetyFlag,
    ShadowReportType
)

@dataclass
class ShadowSimulationContext:
    context_id: str
    created_at_utc: str
    runtime_mode: ShadowRuntimeMode
    starting_equity_usd: float
    in_memory_config: dict[str, Any]
    allow_real_orders: bool
    allow_broker_calls: bool
    allow_paper_state_mutation: bool
    allow_telegram_real_send: bool
    allow_production_config_write: bool
    warnings: list[str]
    errors: list[str]
    source_sandbox_id: Optional[str] = None
    source_bundle_id: Optional[str] = None
    source_bundle_version: Optional[str] = None
    isolated_output_path: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowPosition:
    symbol: str
    quantity: float
    market_value_usd: float
    unrealized_pnl_usd: float
    realized_pnl_usd: float
    avg_price: Optional[float] = None
    market_price: Optional[float] = None
    strategy_name: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowPortfolioState:
    portfolio_id: str
    created_at_utc: str
    equity_usd: float
    cash_usd: float
    positions: list[ShadowPosition]
    gross_exposure_usd: float
    net_exposure_usd: float
    realized_pnl_usd: float
    unrealized_pnl_usd: float
    warnings: list[str]
    errors: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowSignal:
    signal_id: str
    created_at_utc: str
    symbol: str
    side: str
    reason: str
    strategy_name: Optional[str] = None
    signal_family: Optional[str] = None
    score: Optional[float] = None
    confidence: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowOrderIntent:
    intent_id: str
    created_at_utc: str
    symbol: str
    side: str
    quantity: float
    notional_usd: float
    status: ShadowOrderIntentStatus
    is_real_order: bool
    warnings: list[str]
    errors: list[str]
    limit_price: Optional[float] = None
    source_signal_id: Optional[str] = None
    strategy_name: Optional[str] = None
    broker_destination: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowFill:
    fill_id: str
    created_at_utc: str
    intent_id: str
    symbol: str
    side: str
    requested_quantity: float
    filled_quantity: float
    simulated_cost_usd: float
    simulated_slippage_usd: float
    status: ShadowFillStatus
    is_real_fill: bool
    warnings: list[str]
    errors: list[str]
    fill_price: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowLedgerEvent:
    event_id: str
    created_at_utc: str
    event_type: ShadowLedgerEventType
    payload: dict[str, Any]
    safety_flags: list[ShadowSafetyFlag]
    warnings: list[str]
    errors: list[str]
    symbol: Optional[str] = None
    ref_id: Optional[str] = None

@dataclass
class ShadowPnLSnapshot:
    snapshot_id: str
    created_at_utc: str
    equity_usd: float
    cash_usd: float
    realized_pnl_usd: float
    unrealized_pnl_usd: float
    total_pnl_usd: float
    trade_count: int
    warnings: list[str]
    errors: list[str]
    return_pct: Optional[float] = None
    max_drawdown_pct: Optional[float] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowRehearsalSession:
    session_id: str
    created_at_utc: str
    status: ShadowSessionStatus
    signals: list[ShadowSignal]
    order_intents: list[ShadowOrderIntent]
    fills: list[ShadowFill]
    ledger_events: list[ShadowLedgerEvent]
    pnl_snapshots: list[ShadowPnLSnapshot]
    safety_flags: list[ShadowSafetyFlag]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]
    context: Optional[ShadowSimulationContext] = None
    portfolio_state: Optional[ShadowPortfolioState] = None
    started_at_utc: Optional[str] = None
    completed_at_utc: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowRehearsalReview:
    review_id: str
    created_at_utc: str
    report_type: ShadowReportType
    sessions: list[ShadowRehearsalSession]
    output_paths: dict[str, str]
    warnings: list[str]
    errors: list[str]

def shadow_simulation_context_to_dict(item: ShadowSimulationContext) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_position_to_dict(item: ShadowPosition) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_portfolio_state_to_dict(item: ShadowPortfolioState) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_signal_to_dict(item: ShadowSignal) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_order_intent_to_dict(item: ShadowOrderIntent) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_fill_to_dict(item: ShadowFill) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_ledger_event_to_dict(item: ShadowLedgerEvent) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_pnl_snapshot_to_dict(item: ShadowPnLSnapshot) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_rehearsal_session_to_dict(item: ShadowRehearsalSession) -> dict:
    from dataclasses import asdict
    return asdict(item)

def shadow_rehearsal_review_to_dict(item: ShadowRehearsalReview) -> dict:
    from dataclasses import asdict
    return asdict(item)

def validate_shadow_simulation_context(item: ShadowSimulationContext) -> None:
    if item.allow_real_orders:
        raise ValueError("Shadow context allow_real_orders must be False")
    if item.allow_broker_calls:
        raise ValueError("Shadow context allow_broker_calls must be False")
    if item.allow_paper_state_mutation:
        raise ValueError("Shadow context allow_paper_state_mutation must be False")
    if item.allow_telegram_real_send:
        raise ValueError("Shadow context allow_telegram_real_send must be False")
    if item.allow_production_config_write:
        raise ValueError("Shadow context allow_production_config_write must be False")

def validate_shadow_order_intent(item: ShadowOrderIntent) -> None:
    if item.is_real_order:
        raise ValueError("Shadow order intent is_real_order must be False")
    if item.broker_destination is not None:
        raise ValueError("Shadow order intent broker_destination must be None")
    if item.quantity < 0 or item.notional_usd < 0:
        raise ValueError("Quantity and notional must be non-negative")

def validate_shadow_fill(item: ShadowFill) -> None:
    if item.is_real_fill:
        raise ValueError("Shadow fill is_real_fill must be False")
    if item.requested_quantity < 0 or item.filled_quantity < 0 or item.simulated_cost_usd < 0:
        raise ValueError("Quantities and cost must be non-negative")

def validate_shadow_rehearsal_session(item: ShadowRehearsalSession) -> None:
    if item.context:
        validate_shadow_simulation_context(item.context)
    for intent in item.order_intents:
        validate_shadow_order_intent(intent)
    for fill in item.fills:
        validate_shadow_fill(fill)

def create_shadow_context_id(prefix: str = "shadow_context") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_shadow_portfolio_id(prefix: str = "shadow_portfolio") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_shadow_signal_id(symbol: str) -> str:
    return f"shadow_signal_{symbol}_{uuid.uuid4().hex[:8]}"

def create_shadow_order_intent_id(symbol: str) -> str:
    return f"shadow_intent_{symbol}_{uuid.uuid4().hex[:8]}"

def create_shadow_fill_id(symbol: str) -> str:
    return f"shadow_fill_{symbol}_{uuid.uuid4().hex[:8]}"

def create_shadow_ledger_event_id(prefix: str = "shadow_event") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_shadow_pnl_snapshot_id(prefix: str = "shadow_pnl") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_shadow_rehearsal_session_id(prefix: str = "shadow_session") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_shadow_rehearsal_review_id(prefix: str = "shadow_review") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
