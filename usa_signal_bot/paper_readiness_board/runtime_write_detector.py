
from typing import Any, List
from usa_signal_bot.core.enums import RuntimeWriteAttemptType

def detect_runtime_write_attempts_in_payload(payload: dict) -> List[RuntimeWriteAttemptType]:
    attempts = []
    keys_str = " ".join(payload.keys())

    if "paper_state_committed" in keys_str: attempts.append(RuntimeWriteAttemptType.PAPER_STATE_WRITE)
    if "paper_order_executed" in keys_str: attempts.append(RuntimeWriteAttemptType.PAPER_ORDER_CREATE)
    if "paper_order_created" in keys_str: attempts.append(RuntimeWriteAttemptType.PAPER_ORDER_CREATE)
    if "portfolio_state_mutated" in keys_str: attempts.append(RuntimeWriteAttemptType.PORTFOLIO_WRITE)
    if "position_mutated" in keys_str: attempts.append(RuntimeWriteAttemptType.POSITION_WRITE)
    if "cash_mutated" in keys_str: attempts.append(RuntimeWriteAttemptType.CASH_WRITE)
    if "equity_mutated" in keys_str: attempts.append(RuntimeWriteAttemptType.EQUITY_WRITE)
    if "fill_created" in keys_str: attempts.append(RuntimeWriteAttemptType.FILL_WRITE)
    if "config_patched" in keys_str: attempts.append(RuntimeWriteAttemptType.CONFIG_PATCH)
    if "active_paper_enabled" in keys_str: attempts.append(RuntimeWriteAttemptType.ACTIVE_PAPER_ENABLE)
    if "telegram_sent" in keys_str: attempts.append(RuntimeWriteAttemptType.TELEGRAM_REAL_SEND)
    if "broker_order_sent" in keys_str or "sent_to_broker" in keys_str: attempts.append(RuntimeWriteAttemptType.BROKER_SEND)

    return list(set(attempts))

def detect_runtime_write_attempts_in_text(text: str) -> List[RuntimeWriteAttemptType]:
    attempts = []
    t = text.lower()
    if "paper'a uygula" in t or "paper state write" in t: attempts.append(RuntimeWriteAttemptType.PAPER_STATE_WRITE)
    if "canlıya al" in t or "aktif et" in t or "enable active paper" in t: attempts.append(RuntimeWriteAttemptType.ACTIVE_PAPER_ENABLE)
    if "emir gönder" in t or "sent to broker" in t or "live approved" in t: attempts.append(RuntimeWriteAttemptType.BROKER_SEND)
    if "config patch" in t: attempts.append(RuntimeWriteAttemptType.CONFIG_PATCH)
    return list(set(attempts))

def payload_has_runtime_write_fields(payload: dict) -> bool:
    return len(detect_runtime_write_attempts_in_payload(payload)) > 0

def payload_has_activation_fields(payload: dict) -> bool:
    keys = " ".join(payload.keys())
    return "activation_allowed" in keys and payload.get("activation_allowed") is True

def runtime_write_detector_summary(attempts: List[RuntimeWriteAttemptType]) -> dict:
    return {"detected_count": len(attempts), "attempts": [a.value for a in attempts]}

def runtime_write_detector_to_text(attempts: List[RuntimeWriteAttemptType]) -> str:
    return ", ".join([a.value for a in attempts])
