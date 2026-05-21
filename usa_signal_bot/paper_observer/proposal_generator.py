from datetime import datetime, timezone
from typing import Any, Dict, List
from usa_signal_bot.core.enums import ObserverOutputType
from usa_signal_bot.paper_observer.observer_models import (
    ObserverRuntimeContext,
    ObserverOutput,
    create_observer_output_id
)

def build_observer_proposal_outputs(context: ObserverRuntimeContext) -> List[ObserverOutput]:
    # Placeholder for proposal generation mirroring
    return build_mock_observer_proposals(context)

def build_mock_observer_proposals(context: ObserverRuntimeContext) -> List[ObserverOutput]:
    return [
        ObserverOutput(
            output_id=create_observer_output_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            output_type=ObserverOutputType.PROPOSAL_MIRROR,
            symbol="MOCK",
            status="PROPOSED",
            summary={"action": "BUY_PROPOSAL"},
            payload={"action": "BUY_PROPOSAL", "amount": 10},
            is_real_order=False,
            mutates_paper_state=False,
            sends_to_broker=False,
            sends_telegram_real=False,
            safety_flags=[],
            warnings=[],
            errors=[],
            metadata={}
        )
    ]

def validate_observer_proposals_safe(outputs: List[ObserverOutput]) -> List[str]:
    errors = []
    for out in outputs:
        if out.is_real_order:
            errors.append(f"Output {out.output_id} is marked as real order")
        if out.sends_to_broker:
            errors.append(f"Output {out.output_id} attempts to send to broker")
    return errors

def observer_proposal_summary(outputs: List[ObserverOutput]) -> Dict[str, Any]:
    return {
        "count": len(outputs),
        "symbols": [out.symbol for out in outputs if out.symbol]
    }

def observer_proposals_to_text(outputs: List[ObserverOutput], limit: int = 50) -> str:
    return f"Observer Proposals: {len(outputs)} items generated."
