from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

DANGEROUS_LANGUAGE = [
    "gönderildi", "kesin al", "kesin sat", "canlıya al", "paper'a uygula",
    "gerçek emir", "aktif et", "kesin kâr"
]

def notification_warning_count(sessions: List[dict[str, Any]]) -> int:
    return sum(s.get("notification_warning_count", 0) for s in sessions)

def detect_unsafe_notification_history(sessions: List[dict[str, Any]]) -> List[str]:
    unsafe = []
    for s in sessions:
        for notif in s.get("notifications", []):
            text = notif.get("text", "").lower()
            for w in DANGEROUS_LANGUAGE:
                if w in text:
                    unsafe.append(f"Unsafe language detected: {w}")
    return list(set(unsafe))

def notification_safety_risk_flags(sessions: List[dict[str, Any]]) -> List[ObservationRiskFlag]:
    flags = set()
    if detect_unsafe_notification_history(sessions):
        flags.add(ObservationRiskFlag.NOTIFICATION_UNSAFE)
    # Check if there are real sends indicated
    for s in sessions:
        if s.get("telegram_real_send_detected"):
            flags.add(ObservationRiskFlag.TELEGRAM_REAL_SEND_RISK)
    return list(flags)

def aggregate_notification_safety_history(sessions: List[dict[str, Any]]) -> dict[str, Any]:
    unsafe_msgs = detect_unsafe_notification_history(sessions)
    return {
        "warning_count": notification_warning_count(sessions),
        "unsafe_messages_detected": len(unsafe_msgs),
        "unsafe_details": unsafe_msgs,
        "risk_flags": [f.value for f in notification_safety_risk_flags(sessions)]
    }

def notification_safety_history_to_text(payload: dict[str, Any]) -> str:
    return f"Notification Safety History\nWarnings: {payload.get('warning_count', 0)}\nUnsafe Detections: {payload.get('unsafe_messages_detected', 0)}"
