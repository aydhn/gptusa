from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime, timezone

from usa_signal_bot.core.enums import PaperOrderStatus, PaperRejectReason
from usa_signal_bot.paper.paper_models import PaperOrder, PaperFill
from usa_signal_bot.paper.paper_orders import is_order_terminal

@dataclass
class OrderLifecycleTransition:
    order_id: str
    from_status: PaperOrderStatus
    to_status: PaperOrderStatus
    timestamp_utc: str
    reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

def is_valid_order_transition(from_status: PaperOrderStatus, to_status: PaperOrderStatus) -> bool:
    if from_status in [
        PaperOrderStatus.FILLED,
        PaperOrderStatus.REJECTED,
        PaperOrderStatus.CANCELLED,
        PaperOrderStatus.EXPIRED,
        PaperOrderStatus.SKIPPED,
        PaperOrderStatus.ERROR
    ]:
        return False

    valid_transitions = {
        PaperOrderStatus.CREATED: [
            PaperOrderStatus.VALIDATED,
            PaperOrderStatus.REJECTED,
            PaperOrderStatus.CANCELLED,
            PaperOrderStatus.EXPIRED
        ],
        PaperOrderStatus.VALIDATED: [
            PaperOrderStatus.ACCEPTED,
            PaperOrderStatus.REJECTED,
            PaperOrderStatus.CANCELLED,
            PaperOrderStatus.EXPIRED
        ],
        PaperOrderStatus.ACCEPTED: [
            PaperOrderStatus.QUEUED,
            PaperOrderStatus.REJECTED,
            PaperOrderStatus.CANCELLED,
            PaperOrderStatus.EXPIRED
        ],
        PaperOrderStatus.QUEUED: [
            PaperOrderStatus.FILLED,
            PaperOrderStatus.PARTIALLY_FILLED,
            PaperOrderStatus.REJECTED,
            PaperOrderStatus.CANCELLED,
            PaperOrderStatus.EXPIRED
        ],
        PaperOrderStatus.PARTIALLY_FILLED: [
            PaperOrderStatus.FILLED,
            PaperOrderStatus.CANCELLED,
            PaperOrderStatus.EXPIRED
        ]
    }

    return to_status in valid_transitions.get(from_status, [])

class PaperOrderLifecycle:
    def validate(self, order: PaperOrder) -> PaperOrder:
        return self.transition(order, PaperOrderStatus.VALIDATED)

    def accept(self, order: PaperOrder) -> PaperOrder:
        order.accepted_at_utc = datetime.now(timezone.utc).isoformat()
        return self.transition(order, PaperOrderStatus.ACCEPTED)

    def queue(self, order: PaperOrder) -> PaperOrder:
        return self.transition(order, PaperOrderStatus.QUEUED)

    def fill(self, order: PaperOrder, fill: PaperFill) -> PaperOrder:
        order.filled_at_utc = fill.filled_at_utc
        return self.transition(order, PaperOrderStatus.FILLED)

    def reject(self, order: PaperOrder, reason: PaperRejectReason, message: Optional[str] = None) -> PaperOrder:
        order.reject_reason = reason
        order.message = message
        order.rejected_at_utc = datetime.now(timezone.utc).isoformat()
        return self.transition(order, PaperOrderStatus.REJECTED, reason=reason.value if hasattr(reason, 'value') else str(reason))

    def cancel(self, order: PaperOrder, reason: Optional[str] = None) -> PaperOrder:
        order.metadata["cancel_reason"] = reason
        order.metadata["cancelled_at_utc"] = datetime.now(timezone.utc).isoformat()
        return self.transition(order, PaperOrderStatus.CANCELLED, reason=reason)

    def expire(self, order: PaperOrder, reason: Optional[str] = None) -> PaperOrder:
        order.metadata["expired_at_utc"] = datetime.now(timezone.utc).isoformat()
        return self.transition(order, PaperOrderStatus.EXPIRED, reason=reason)

    def transition(self, order: PaperOrder, to_status: PaperOrderStatus, reason: Optional[str] = None) -> PaperOrder:
        from_status = order.status

        if not is_valid_order_transition(from_status, to_status):
            raise ValueError(f"Invalid transition from {from_status} to {to_status}")

        order.status = to_status

        transition = OrderLifecycleTransition(
            order_id=order.order_id,
            from_status=from_status,
            to_status=to_status,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            reason=reason
        )

        if "lifecycle_transitions" not in order.metadata:
            order.metadata["lifecycle_transitions"] = []

        order.metadata["lifecycle_transitions"].append(order_lifecycle_transition_to_dict(transition))

        return order

def order_lifecycle_transition_to_dict(transition: OrderLifecycleTransition) -> dict:
    from dataclasses import asdict
    return asdict(transition)

def order_lifecycle_to_text(order: PaperOrder) -> str:
    lines = [
        f"--- ORDER LIFECYCLE: {order.order_id} ---",
        f"Current Status: {order.status.value if hasattr(order.status, 'value') else order.status}",
    ]

    transitions = order.metadata.get("lifecycle_transitions", [])
    if transitions:
        lines.append("Transitions:")
        for t in transitions:
            reason = f" ({t.get('reason')})" if t.get('reason') else ""
            lines.append(f"  {t.get('timestamp_utc')} | {t.get('from_status')} -> {t.get('to_status')}{reason}")
    else:
        lines.append("No transitions recorded.")

    return "\n".join(lines)
