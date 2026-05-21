from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from usa_signal_bot.core.enums import ObserverDriftType, ObserverOutputType
from usa_signal_bot.paper_observer.observer_models import (
    ObserverOutput,
    ObserverDriftEvent,
    create_observer_drift_id
)

def detect_signal_count_drift(paper_snapshot: Dict[str, Any], observer_outputs: List[ObserverOutput]) -> Optional[ObserverDriftEvent]:
    signals = [o for o in observer_outputs if o.output_type == ObserverOutputType.SIGNAL_MIRROR]
    # mock comparison for example
    baseline_count = paper_snapshot.get("signal_count", 0)
    if len(signals) != baseline_count:
        return ObserverDriftEvent(
            drift_id=create_observer_drift_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            drift_type=ObserverDriftType.SIGNAL_COUNT_DRIFT,
            symbol=None,
            baseline_value=baseline_count,
            observer_value=len(signals),
            delta=len(signals) - baseline_count,
            severity="WARNING",
            description=f"Signal count drift detected. Baseline: {baseline_count}, Observer: {len(signals)}",
            safety_flags=[],
            warnings=[],
            errors=[],
            metadata={}
        )
    return None

def detect_proposal_count_drift(paper_snapshot: Dict[str, Any], observer_outputs: List[ObserverOutput]) -> Optional[ObserverDriftEvent]:
    proposals = [o for o in observer_outputs if o.output_type == ObserverOutputType.PROPOSAL_MIRROR]
    baseline_count = paper_snapshot.get("proposal_count", 0)
    if len(proposals) != baseline_count:
        return ObserverDriftEvent(
            drift_id=create_observer_drift_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            drift_type=ObserverDriftType.PROPOSAL_COUNT_DRIFT,
            symbol=None,
            baseline_value=baseline_count,
            observer_value=len(proposals),
            delta=len(proposals) - baseline_count,
            severity="WARNING",
            description=f"Proposal count drift detected. Baseline: {baseline_count}, Observer: {len(proposals)}",
            safety_flags=[],
            warnings=[],
            errors=[],
            metadata={}
        )
    return None

def detect_risk_status_drift(observer_outputs: List[ObserverOutput]) -> List[ObserverDriftEvent]:
    events = []
    # simplified mock
    risks = [o for o in observer_outputs if o.output_type == ObserverOutputType.RISK_MIRROR]
    for r in risks:
        if "risk_flags" in r.payload and len(r.payload["risk_flags"]) > 0:
            events.append(ObserverDriftEvent(
                drift_id=create_observer_drift_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                drift_type=ObserverDriftType.RISK_STATUS_DRIFT,
                symbol=r.symbol,
                baseline_value=0,
                observer_value=len(r.payload["risk_flags"]),
                delta=len(r.payload["risk_flags"]),
                severity="WARNING",
                description="Risk status drift detected: observer generated risk flags.",
                safety_flags=[],
                warnings=[],
                errors=[],
                metadata={}
            ))
    return events

def detect_safety_flag_drift(observer_outputs: List[ObserverOutput]) -> List[ObserverDriftEvent]:
    events = []
    for out in observer_outputs:
        if out.safety_flags:
            events.append(ObserverDriftEvent(
                drift_id=create_observer_drift_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                drift_type=ObserverDriftType.SAFETY_FLAG_DRIFT,
                symbol=out.symbol,
                baseline_value=0,
                observer_value=len(out.safety_flags),
                delta=len(out.safety_flags),
                severity="CRITICAL",
                description=f"Safety flag drift on output {out.output_id}",
                safety_flags=out.safety_flags,
                warnings=[],
                errors=[],
                metadata={}
            ))
    return events

def detect_observer_drift(paper_snapshot: Dict[str, Any], observer_outputs: List[ObserverOutput]) -> List[ObserverDriftEvent]:
    events = []
    e = detect_signal_count_drift(paper_snapshot, observer_outputs)
    if e: events.append(e)
    e = detect_proposal_count_drift(paper_snapshot, observer_outputs)
    if e: events.append(e)

    events.extend(detect_risk_status_drift(observer_outputs))
    events.extend(detect_safety_flag_drift(observer_outputs))

    return events

def observer_drift_summary(events: List[ObserverDriftEvent]) -> Dict[str, Any]:
    return {"count": len(events)}

def observer_drift_to_text(events: List[ObserverDriftEvent], limit: int = 50) -> str:
    return f"Detected {len(events)} drift events."
