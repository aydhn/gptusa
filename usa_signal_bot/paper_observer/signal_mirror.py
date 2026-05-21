from datetime import datetime, timezone
from typing import Any, Dict, List
from usa_signal_bot.core.enums import ObserverOutputType
from usa_signal_bot.paper_observer.observer_models import (
    ObserverRuntimeContext,
    ObserverOutput,
    create_observer_output_id
)

def build_observer_signal_outputs(context: ObserverRuntimeContext) -> List[ObserverOutput]:
    # Placeholder for actual signal generation mirroring
    return build_mock_signal_mirror_outputs(context)

def build_mock_signal_mirror_outputs(context: ObserverRuntimeContext) -> List[ObserverOutput]:
    return [
        ObserverOutput(
            output_id=create_observer_output_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            output_type=ObserverOutputType.SIGNAL_MIRROR,
            symbol="MOCK",
            status="MIRRORED",
            summary={"action": "BUY"},
            payload={"action": "BUY", "confidence": 0.9},
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

def validate_signal_mirror_outputs_safe(outputs: List[ObserverOutput]) -> List[str]:
    errors = []
    for out in outputs:
        if out.is_real_order:
            errors.append(f"Output {out.output_id} marks is_real_order=True")
        if out.mutates_paper_state:
            errors.append(f"Output {out.output_id} mutates paper state")
        if out.sends_to_broker:
            errors.append(f"Output {out.output_id} sends to broker")
    return errors

def signal_mirror_summary(outputs: List[ObserverOutput]) -> Dict[str, Any]:
    return {
        "count": len(outputs),
        "symbols": [out.symbol for out in outputs if out.symbol]
    }

def signal_mirror_to_text(outputs: List[ObserverOutput], limit: int = 50) -> str:
    return f"Signal Mirror Outputs: {len(outputs)} items generated."
