from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ObserverOutputType, ObserverSafetyFlag
from usa_signal_bot.paper_observer.observer_models import (
    ObserverRuntimeContext,
    ObserverOutput,
    create_observer_output_id
)

def evaluate_observer_output_risk(output: ObserverOutput, context: ObserverRuntimeContext) -> ObserverOutput:
    if output.is_real_order:
        output.safety_flags.append(ObserverSafetyFlag.REAL_ORDER_RISK)
    if output.sends_to_broker:
        output.safety_flags.append(ObserverSafetyFlag.BROKER_ORDER_RISK)
    return output

def build_observer_risk_outputs(context: ObserverRuntimeContext, proposals: Optional[List[ObserverOutput]] = None) -> List[ObserverOutput]:
    outputs = []
    if proposals:
        for p in proposals:
            risk_out = evaluate_observer_output_risk(p, context)
            outputs.append(ObserverOutput(
                output_id=create_observer_output_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                output_type=ObserverOutputType.RISK_MIRROR,
                symbol=p.symbol,
                status="EVALUATED",
                summary={"original_proposal_id": p.output_id},
                payload={"risk_flags": [f.value for f in risk_out.safety_flags]},
                is_real_order=False,
                mutates_paper_state=False,
                sends_to_broker=False,
                sends_telegram_real=False,
                safety_flags=risk_out.safety_flags,
                warnings=[],
                errors=[],
                metadata={}
            ))
    return outputs

def validate_risk_mirror_outputs_safe(outputs: List[ObserverOutput]) -> List[str]:
    errors = []
    for out in outputs:
        if out.is_real_order or out.sends_to_broker:
            errors.append(f"Output {out.output_id} is unsafe")
    return errors

def risk_mirror_summary(outputs: List[ObserverOutput]) -> Dict[str, Any]:
    return {
        "count": len(outputs)
    }

def risk_mirror_to_text(outputs: List[ObserverOutput], limit: int = 50) -> str:
    return f"Risk Mirror Outputs: {len(outputs)} items generated."
