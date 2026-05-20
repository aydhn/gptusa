from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
import uuid
from datetime import datetime, timezone
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
    source_sandbox_id: Optional[str]
    source_bundle_id: Optional[str]
    source_bundle_version: Optional[str]
    runtime_mode: ShadowRuntimeMode
    starting_equity_usd: float
    in_memory_config: Dict[str, Any]
    isolated_output_path: Optional[str]
    allow_real_orders: bool
    allow_broker_calls: bool
    allow_paper_state_mutation: bool
    allow_telegram_real_send: bool
    allow_production_config_write: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowPosition:
    symbol: str
    quantity: float
    avg_price: Optional[float]
    market_price: Optional[float]
    market_value_usd: float
    unrealized_pnl_usd: float
    realized_pnl_usd: float
    strategy_name: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowPortfolioState:
    portfolio_id: str
    created_at_utc: str
    equity_usd: float
    cash_usd: float
    positions: List[ShadowPosition]
    gross_exposure_usd: float
    net_exposure_usd: float
    realized_pnl_usd: float
    unrealized_pnl_usd: float
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowSignal:
    signal_id: str
    created_at_utc: str
    symbol: str
    strategy_name: Optional[str]
    signal_family: Optional[str]
    side: str
    score: Optional[float]
    confidence: Optional[float]
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowOrderIntent:
    intent_id: str
    created_at_utc: str
    symbol: str
    side: str
    quantity: float
    notional_usd: float
    limit_price: Optional[float]
    source_signal_id: Optional[str]
    strategy_name: Optional[str]
    status: ShadowOrderIntentStatus
    is_real_order: bool
    broker_destination: Optional[str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowFill:
    fill_id: str
    created_at_utc: str
    intent_id: str
    symbol: str
    side: str
    requested_quantity: float
    filled_quantity: float
    fill_price: Optional[float]
    simulated_cost_usd: float
    simulated_slippage_usd: float
    status: ShadowFillStatus
    is_real_fill: bool
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowLedgerEvent:
    event_id: str
    created_at_utc: str
    event_type: ShadowLedgerEventType
    symbol: Optional[str]
    ref_id: Optional[str]
    payload: Dict[str, Any]
    safety_flags: List[ShadowSafetyFlag]
    warnings: List[str]
    errors: List[str]

@dataclass
class ShadowPnLSnapshot:
    snapshot_id: str
    created_at_utc: str
    equity_usd: float
    cash_usd: float
    realized_pnl_usd: float
    unrealized_pnl_usd: float
    total_pnl_usd: float
    return_pct: Optional[float]
    max_drawdown_pct: Optional[float]
    trade_count: int
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowRehearsalSession:
    session_id: str
    created_at_utc: str
    status: ShadowSessionStatus
    context: Optional[ShadowSimulationContext]
    portfolio_state: Optional[ShadowPortfolioState]
    signals: List[ShadowSignal]
    order_intents: List[ShadowOrderIntent]
    fills: List[ShadowFill]
    ledger_events: List[ShadowLedgerEvent]
    pnl_snapshots: List[ShadowPnLSnapshot]
    safety_flags: List[ShadowSafetyFlag]
    started_at_utc: Optional[str]
    completed_at_utc: Optional[str]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ShadowRehearsalReview:
    review_id: str
    created_at_utc: str
    report_type: ShadowReportType
    sessions: List[ShadowRehearsalSession]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def get_utc_now_str() -> str:
    return datetime.now(timezone.utc).isoformat()

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
