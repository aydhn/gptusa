from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestClosureRiskFlag, BacktestClosureContext, BacktestFinalAuditReport,
    BacktestBandClosureCertificate, Phase153HandoffContract, Phase153HandoffPackage,
    HandoffSafetyBoundaryResult, Phase153ReadinessGate
)

def closure_text_has_trade_or_execution_language(text: str) -> bool:
    bad_phrases = [
        "is investment advice", "guaranteed profit", "sure thing", "buy now",
        "sell now", "execute immediately", "send to broker", "deploy to production"
    ]
    t = text.lower()
    for phrase in bad_phrases:
        if phrase in t:
            return True
    return False

def handoff_payload_has_forbidden_fields(payload: dict[str, Any]) -> bool:
    import json
    text = json.dumps(payload).lower()
    forbidden = [
        "portfolio_weight", "target_weight", "allocation", "position_size",
        "order", "broker_order", "paper_order", "live_order", "live_signal", "buy_signal", "sell_signal"
    ]
    for field in forbidden:
        if f'"{field}"' in text:
            return True
    return False

def closure_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "errors": errors}

def closure_safety_to_text(errors: list[str]) -> str:
    return "Safe" if not errors else f"Unsafe: {', '.join(errors)}"
