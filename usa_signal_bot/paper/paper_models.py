from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from usa_signal_bot.core.enums import (
    PaperAccountStatus,
    PaperOrderSide,
    PaperOrderType,
    PaperOrderStatus,
    PaperFillStatus,
    PaperPositionSide,
    PaperCashLedgerEntryType,
    PaperTradeStatus,
    PaperEngineStatus,
    PaperOrderSource,
    PaperExecutionMode,
    PaperRejectReason
)
import uuid

@dataclass
class VirtualAccount:
    account_id: str
    name: str
    status: PaperAccountStatus
    starting_cash: float
    cash: float
    equity: float
    realized_pnl: float
    unrealized_pnl: float
    created_at_utc: str
    updated_at_utc: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperOrderIntent:
    order_id: str
    source: PaperOrderSource
    source_id: Optional[str]
    symbol: str
    timeframe: str
    side: PaperOrderSide
    order_type: PaperOrderType
    quantity: float
    notional: Optional[float]
    limit_price: Optional[float] = None
    created_at_utc: str = ""
    expires_at_utc: Optional[str] = None
    reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperOrder:
    order_id: str
    account_id: str
    intent: PaperOrderIntent
    status: PaperOrderStatus
    validated_at_utc: Optional[str] = None
    accepted_at_utc: Optional[str] = None
    filled_at_utc: Optional[str] = None
    rejected_at_utc: Optional[str] = None
    reject_reason: Optional[PaperRejectReason] = None
    message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperFill:
    fill_id: str
    order_id: str
    account_id: str
    symbol: str
    timeframe: str
    side: PaperOrderSide
    quantity: float
    fill_price: float
    gross_notional: float
    fees: float
    slippage_cost: float
    net_cash_impact: float
    status: PaperFillStatus
    filled_at_utc: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperPosition:
    symbol: str
    side: PaperPositionSide
    quantity: float
    average_price: float
    market_price: Optional[float]
    market_value: float
    realized_pnl: float
    unrealized_pnl: float
    opened_at_utc: Optional[str]
    updated_at_utc: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CashLedgerEntry:
    entry_id: str
    account_id: str
    timestamp_utc: str
    entry_type: PaperCashLedgerEntryType
    amount: float
    cash_after: float
    related_order_id: Optional[str] = None
    related_fill_id: Optional[str] = None
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperEquitySnapshot:
    snapshot_id: str
    account_id: str
    timestamp_utc: str
    cash: float
    equity: float
    realized_pnl: float
    unrealized_pnl: float
    gross_exposure: float
    net_exposure: float
    open_positions: int
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperTrade:
    trade_id: str
    account_id: str
    symbol: str
    timeframe: str
    status: PaperTradeStatus
    entry_order_id: Optional[str]
    exit_order_id: Optional[str]
    entry_fill_id: Optional[str]
    exit_fill_id: Optional[str]
    entry_time_utc: Optional[str]
    exit_time_utc: Optional[str]
    entry_price: Optional[float]
    exit_price: Optional[float]
    quantity: float
    gross_pnl: float
    net_pnl: float
    total_fees: float
    return_pct: Optional[float]
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperEngineRunResult:
    run_id: str
    created_at_utc: str
    status: PaperEngineStatus
    account: VirtualAccount
    orders: List[PaperOrder]
    fills: List[PaperFill]
    positions: List[PaperPosition]
    cash_ledger: List[CashLedgerEntry]
    equity_snapshots: List[PaperEquitySnapshot]
    trades: List[PaperTrade]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

def virtual_account_to_dict(account: VirtualAccount) -> dict:
    from dataclasses import asdict
    return asdict(account)

def paper_order_intent_to_dict(intent: PaperOrderIntent) -> dict:
    from dataclasses import asdict
    return asdict(intent)

def paper_order_to_dict(order: PaperOrder) -> dict:
    from dataclasses import asdict
    return asdict(order)

def paper_fill_to_dict(fill: PaperFill) -> dict:
    from dataclasses import asdict
    return asdict(fill)

def paper_position_to_dict(position: PaperPosition) -> dict:
    from dataclasses import asdict
    return asdict(position)

def cash_ledger_entry_to_dict(entry: CashLedgerEntry) -> dict:
    from dataclasses import asdict
    return asdict(entry)

def paper_equity_snapshot_to_dict(snapshot: PaperEquitySnapshot) -> dict:
    from dataclasses import asdict
    return asdict(snapshot)

def paper_trade_to_dict(trade: PaperTrade) -> dict:
    from dataclasses import asdict
    return asdict(trade)

def paper_engine_run_result_to_dict(result: PaperEngineRunResult) -> dict:
    from dataclasses import asdict
    return asdict(result)

def create_virtual_account_id(prefix: str = "paper_acct") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_order_id(prefix: str = "paper_order") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_fill_id(prefix: str = "paper_fill") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_cash_ledger_entry_id(prefix: str = "cash") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_snapshot_id(prefix: str = "paper_snap") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_trade_id(symbol: str, entry_time_utc: Optional[str] = None) -> str:
    ts = entry_time_utc.replace(":", "").replace("-", "").replace("T", "_")[:15] if entry_time_utc else uuid.uuid4().hex[:8]
    return f"paper_trade_{symbol}_{ts}"

def create_paper_run_id(prefix: str = "paper_run") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def validate_virtual_account(account: VirtualAccount) -> None:
    if account.starting_cash <= 0:
        raise ValueError("starting_cash must be positive")
    if account.cash < 0:
        raise ValueError("cash cannot be negative")
    if account.equity < 0:
        raise ValueError("equity cannot be negative")

def validate_paper_order_intent(intent: PaperOrderIntent) -> None:
    if not intent.symbol:
        raise ValueError("symbol cannot be empty")
    if not intent.timeframe:
        raise ValueError("timeframe cannot be empty")
    if intent.side in [PaperOrderSide.BUY, PaperOrderSide.SELL] and intent.quantity <= 0:
        raise ValueError(f"quantity must be positive for {intent.side}")
    if intent.notional is not None and intent.notional < 0:
        raise ValueError("notional cannot be negative")

def validate_paper_order(order: PaperOrder) -> None:
    validate_paper_order_intent(order.intent)

def validate_paper_fill(fill: PaperFill) -> None:
    if fill.fill_price <= 0:
        raise ValueError("fill_price must be positive")
    if fill.gross_notional < 0:
        raise ValueError("gross_notional cannot be negative")
    if fill.fees < 0:
        raise ValueError("fees cannot be negative")

def validate_paper_position(position: PaperPosition) -> None:
    pass

def validate_cash_ledger_entry(entry: CashLedgerEntry) -> None:
    pass

def validate_paper_equity_snapshot(snapshot: PaperEquitySnapshot) -> None:
    pass
