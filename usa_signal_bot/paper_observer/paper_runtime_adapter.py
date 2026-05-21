from typing import Any, Dict, List, Optional
import copy
from usa_signal_bot.paper_observer.observer_models import ObserverOutput, PaperObserverReview
from usa_signal_bot.paper_observer.paper_snapshot_loader import load_observer_read_only_paper_snapshot

def build_read_only_paper_runtime_snapshot_for_observer(paper_payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return load_observer_read_only_paper_snapshot(paper_payload)

def compare_observer_outputs_to_paper_snapshot(outputs: List[ObserverOutput], paper_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    from usa_signal_bot.paper_observer.drift_detector import detect_observer_drift
    drifts = detect_observer_drift(paper_snapshot, outputs)
    return {
        "drifts_detected": len(drifts),
        "outputs_compared": len(outputs)
    }

def validate_paper_runtime_not_mutated_by_observer(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    errors = []
    import json
    before_str = json.dumps(before, sort_keys=True, default=str)
    after_str = json.dumps(after, sort_keys=True, default=str)
    if before_str != after_str:
        errors.append("Paper runtime state was mutated by observer.")
    return errors

def attach_observer_metadata_to_paper_analytics(payload: Dict[str, Any], review: PaperObserverReview) -> Dict[str, Any]:
    payload["paper_observer_analytics"] = {
        "review_id": review.review_id,
        "drifts": len(review.drift_events)
    }
    return payload

def paper_runtime_observer_adapter_to_text(payload: Dict[str, Any]) -> str:
    analytics = payload.get("paper_observer_analytics", {})
    return f"Paper runtime adapter attached analytics. Drifts: {analytics.get('drifts')}"
