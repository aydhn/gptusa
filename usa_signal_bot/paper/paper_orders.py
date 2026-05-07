from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    PaperOrderSide,
    PaperOrderType,
    PaperOrderStatus,
    PaperOrderSource,
    PaperRejectReason,
    PaperAccountStatus
)
from usa_signal_bot.paper.paper_models import (
    VirtualAccount,
    PaperOrderIntent,
    PaperOrder,
    create_paper_order_id,
    validate_paper_order_intent
)

def create_paper_order_intent(
    symbol: str,
    timeframe: str,
    side: PaperOrderSide,
    quantity: float,
    source: PaperOrderSource = PaperOrderSource.MANUAL_RESEARCH,
    source_id: Optional[str] = None,
    order_type: PaperOrderType = PaperOrderType.NEXT_OPEN,
    notional: Optional[float] = None,
    reason: Optional[str] = None
) -> PaperOrderIntent:
    intent = PaperOrderIntent(
        order_id=create_paper_order_id("intent"),
        source=source,
        source_id=source_id,
        symbol=symbol,
        timeframe=timeframe,
        side=side,
        order_type=order_type,
        quantity=quantity,
        notional=notional,
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        reason=reason
    )
    validate_paper_order_intent(intent)
    return intent

def create_paper_order(account: VirtualAccount, intent: PaperOrderIntent) -> PaperOrder:
    order = PaperOrder(
        order_id=create_paper_order_id(),
        account_id=account.account_id,
        intent=intent,
        status=PaperOrderStatus.CREATED
    )
    return order

def validate_paper_order_intent_for_account(account: VirtualAccount, intent: PaperOrderIntent) -> Tuple[bool, Optional[PaperRejectReason], List[str]]:
    warnings = []

    if account.status != PaperAccountStatus.ACTIVE:
        return False, PaperRejectReason.ACCOUNT_PAUSED, [f"Account is {account.status}, not ACTIVE"]

    if intent.side in [PaperOrderSide.BUY, PaperOrderSide.SELL] and intent.quantity <= 0:
        return False, PaperRejectReason.INVALID_QUANTITY, [f"Quantity must be positive for {intent.side}"]

    if intent.order_type in [PaperOrderType.LIMIT_RESERVED, PaperOrderType.STOP_RESERVED]:
        return False, PaperRejectReason.VALIDATION_FAILED, [f"Order type {intent.order_type} is not supported in this phase"]

    if intent.side == PaperOrderSide.SELL:
        warnings.append("SELL order requires an existing long position (checked at execution time)")

    return True, None, warnings

def accept_paper_order(order: PaperOrder) -> PaperOrder:
    order.status = PaperOrderStatus.ACCEPTED
    order.accepted_at_utc = datetime.now(timezone.utc).isoformat()
    return order

def reject_paper_order(order: PaperOrder, reason: PaperRejectReason, message: Optional[str] = None) -> PaperOrder:
    order.status = PaperOrderStatus.REJECTED
    order.rejected_at_utc = datetime.now(timezone.utc).isoformat()
    order.reject_reason = reason
    if message:
        order.message = message
    return order

def cancel_paper_order(order: PaperOrder, reason: Optional[str] = None) -> PaperOrder:
    order.status = PaperOrderStatus.CANCELLED
    order.metadata["cancel_reason"] = reason
    order.metadata["cancelled_at_utc"] = datetime.now(timezone.utc).isoformat()
    return order

def expire_paper_order(order: PaperOrder, now_utc: Optional[str] = None) -> PaperOrder:
    order.status = PaperOrderStatus.EXPIRED
    order.metadata["expired_at_utc"] = now_utc or datetime.now(timezone.utc).isoformat()
    return order

def is_order_terminal(order: PaperOrder) -> bool:
    terminal_statuses = [
        PaperOrderStatus.FILLED,
        PaperOrderStatus.REJECTED,
        PaperOrderStatus.CANCELLED,
        PaperOrderStatus.EXPIRED,
        PaperOrderStatus.SKIPPED,
        PaperOrderStatus.ERROR
    ]
    return order.status in terminal_statuses

def paper_order_summary(order: PaperOrder) -> Dict[str, Any]:
    return {
        "order_id": order.order_id,
        "account_id": order.account_id,
        "symbol": order.intent.symbol,
        "side": order.intent.side.value if hasattr(order.intent.side, 'value') else order.intent.side,
        "quantity": order.intent.quantity,
        "status": order.status.value if hasattr(order.status, 'value') else order.status,
        "reject_reason": order.reject_reason.value if hasattr(order.reject_reason, 'value') and order.reject_reason else None
    }
