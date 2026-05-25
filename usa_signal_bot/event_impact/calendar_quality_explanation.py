
from typing import Any, Dict, List
from usa_signal_bot.event_impact.phase112_models import CalendarAwareAnomaly

def build_calendar_quality_explanation(anomaly: CalendarAwareAnomaly) -> str:
    if anomaly.explained_by_event:
        return f"{anomaly.anomaly_kind.value} explained by {anomaly.explanation_type.value}"
    return f"Unexplained {anomaly.anomaly_kind.value}"

def build_calendar_quality_explanations(anomalies: List[CalendarAwareAnomaly]) -> List[str]:
    return [build_calendar_quality_explanation(a) for a in anomalies]

def validate_calendar_quality_explanation_safety(text: str) -> List[str]:
    errs = []
    t = text.lower()
    if "buy" in t or "sell" in t or "signal" in t:
        errs.append("Contains trade signal language.")
    return errs

def calendar_quality_explanation_summary(explanations: List[str]) -> Dict[str, Any]:
    return {"total": len(explanations)}

def calendar_quality_explanation_to_text(explanations: List[str], limit: int = 200) -> str:
    return " | ".join(explanations[:limit])
