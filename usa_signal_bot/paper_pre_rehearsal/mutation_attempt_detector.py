from typing import Any, Dict, List
import json
from usa_signal_bot.core.enums import MutationAttemptType

def payload_has_paper_mutation_fields(payload: Dict[str, Any]) -> bool:
    payload_str = json.dumps(payload).lower()
    mutation_fields = [
        "paper_state_committed",
        "paper_order_executed",
        "portfolio_state_mutated",
        "position_mutated",
        "cash_mutated",
        "equity_mutated"
    ]
    for field in mutation_fields:
        if f'"{field}": true' in payload_str or f'"{field}":true' in payload_str:
            return True
    return False

def payload_has_broker_execution_fields(payload: Dict[str, Any]) -> bool:
    payload_str = json.dumps(payload).lower()
    broker_fields = [
        "broker_order_id",
        "live_order_id",
        "sent_to_broker",
        "execution_venue",
        "real_fill_id"
    ]
    for field in broker_fields:
        if f'"{field}"' in payload_str:
            return True
    return False

def detect_mutation_attempts_in_payload(payload: Dict[str, Any]) -> List[MutationAttemptType]:
    attempts = set()

    if payload_has_paper_mutation_fields(payload):
        attempts.add(MutationAttemptType.PAPER_STATE_WRITE)
        attempts.add(MutationAttemptType.PAPER_PORTFOLIO_MUTATION)

    if payload_has_broker_execution_fields(payload):
        attempts.add(MutationAttemptType.BROKER_ORDER_SEND)

    payload_str = json.dumps(payload).lower()
    if '"config_patched": true' in payload_str or '"config_patched":true' in payload_str:
        attempts.add(MutationAttemptType.PRODUCTION_CONFIG_PATCH)
    if '"active_paper_enabled": true' in payload_str or '"active_paper_enabled":true' in payload_str:
        attempts.add(MutationAttemptType.ACTIVE_PAPER_ENABLE)
    if '"telegram_sent": true' in payload_str or '"telegram_sent":true' in payload_str:
        attempts.add(MutationAttemptType.TELEGRAM_REAL_SEND)

    return list(attempts)

def detect_mutation_attempts_in_text(text: str) -> List[MutationAttemptType]:
    attempts = set()
    text_lower = text.lower()

    if any(p in text_lower for p in ["paper'a uygula", "paper state write"]):
        attempts.add(MutationAttemptType.PAPER_STATE_WRITE)
    if any(p in text_lower for p in ["canlıya al", "aktif et", "live approved"]):
        attempts.add(MutationAttemptType.ACTIVE_PAPER_ENABLE)
    if any(p in text_lower for p in ["emir gönder", "sent to broker"]):
        attempts.add(MutationAttemptType.BROKER_ORDER_SEND)
    if "config patch" in text_lower:
        attempts.add(MutationAttemptType.PRODUCTION_CONFIG_PATCH)

    return list(attempts)

def mutation_attempt_detector_summary(attempts: List[MutationAttemptType]) -> Dict[str, Any]:
    return {
        "attempt_count": len(attempts),
        "detected_types": [a.value for a in attempts]
    }

def mutation_attempt_detector_to_text(attempts: List[MutationAttemptType]) -> str:
    s = mutation_attempt_detector_summary(attempts)
    return f"Detected Attempts: {s['attempt_count']} ({s['detected_types']})"
