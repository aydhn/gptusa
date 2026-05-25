
from typing import Any, Dict, List
from usa_signal_bot.event_impact.phase112_models import CalendarAwareValidationResult

def calendar_validation_text_has_trade_language(text: str) -> bool:
    t = text.lower()
    unsafe = ["buy", "sell", "emir", "garanti", "kesin"]
    return any(u in t for u in unsafe)

def validate_calendar_validation_result_safety(result: CalendarAwareValidationResult) -> List[str]:
    errs = []
    if result.produces_trade_signal or result.produces_order_decision:
        errs.append(f"Result {result.validation_id} produces signals")
    if result.network_used or result.broker_used:
        errs.append(f"Result {result.validation_id} used network or broker")
    for a in result.anomalies:
        if calendar_validation_text_has_trade_language(a.explanation):
            errs.append(f"Anomaly {a.anomaly_id} contains trade language")
    return errs

def validate_calendar_validation_results_safety(results: List[CalendarAwareValidationResult]) -> List[str]:
    errs = []
    for r in results:
        errs.extend(validate_calendar_validation_result_safety(r))
    return errs

def calendar_validation_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors), "safe": len(errors) == 0}

def calendar_validation_safety_to_text(errors: List[str]) -> str:
    if not errors: return "Calendar validation is safe."
    return "CALENDAR SAFETY VIOLATIONS:\n" + "\n".join(errors)
