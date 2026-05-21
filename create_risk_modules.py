import os
from pathlib import Path

FILES = {}

FILES["usa_signal_bot/paper_observation/risk_history.py"] = """\
from typing import Any, List
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def risk_warning_ratio(sessions: List[dict[str, Any]]) -> float | None:
    total_proposals = sum(len(s.get("proposals", [])) for s in sessions)
    if total_proposals == 0:
        return None
    warnings = sum(s.get("risk_warning_count", 0) for s in sessions)
    return min(1.0, warnings / total_proposals)

def risk_rejection_ratio(sessions: List[dict[str, Any]]) -> float | None:
    total_proposals = sum(len(s.get("proposals", [])) for s in sessions)
    if total_proposals == 0:
        return None
    rejections = sum(s.get("risk_rejected_count", 0) for s in sessions)
    return min(1.0, rejections / total_proposals)

def risk_history_flags(sessions: List[dict[str, Any]]) -> List[ObservationRiskFlag]:
    flags = set()
    for s in sessions:
        if s.get("real_order_risk_detected"):
            flags.add(ObservationRiskFlag.REAL_ORDER_RISK)
        if s.get("paper_state_mutation_detected"):
            flags.add(ObservationRiskFlag.PAPER_STATE_MUTATION_RISK)

    rej_ratio = risk_rejection_ratio(sessions)
    if rej_ratio is not None and rej_ratio > 0.5:
        flags.add(ObservationRiskFlag.RISK_REJECTION_HIGH)

    return list(flags)

def aggregate_risk_outcome_history(sessions: List[dict[str, Any]]) -> dict[str, Any]:
    return {
        "session_count": len(sessions),
        "warning_ratio": risk_warning_ratio(sessions),
        "rejection_ratio": risk_rejection_ratio(sessions),
        "risk_flags": [f.value for f in risk_history_flags(sessions)]
    }

def risk_history_to_text(payload: dict[str, Any]) -> str:
    rej = payload.get('rejection_ratio')
    r_str = f"{rej:.2f}" if rej is not None else "N/A"
    return f"Risk History\\nSessions: {payload.get('session_count', 0)}\\nRejection Ratio: {r_str}\\nFlags: {len(payload.get('risk_flags', []))}"
"""

FILES["usa_signal_bot/paper_observation/blocked_operation_history.py"] = """\
from typing import Any, List, Dict
from usa_signal_bot.paper_observation.observation_models import ObservationRiskFlag

def blocked_operation_count(events: List[dict[str, Any]]) -> int:
    return sum(1 for e in events if e.get("event_type") == "BLOCKED_OPERATION")

def blocked_operations_by_type(events: List[dict[str, Any]]) -> Dict[str, int]:
    counts = {}
    for ev in events:
        if ev.get("event_type") == "BLOCKED_OPERATION":
            op_type = ev.get("operation_type", "UNKNOWN")
            counts[op_type] = counts.get(op_type, 0) + 1
    return counts

def blocked_operation_risk_flags(events: List[dict[str, Any]]) -> List[ObservationRiskFlag]:
    flags = set()
    if blocked_operation_count(events) > 0:
        flags.add(ObservationRiskFlag.BLOCKED_OPERATION_HISTORY)

    ops = blocked_operations_by_type(events)
    if "REAL_ORDER" in ops:
        flags.add(ObservationRiskFlag.REAL_ORDER_RISK)
    if "PAPER_ORDER" in ops:
        flags.add(ObservationRiskFlag.PAPER_ORDER_RISK)
    if "BROKER_API" in ops:
        flags.add(ObservationRiskFlag.BROKER_ORDER_RISK)
    if "PAPER_STATE_MUTATION" in ops:
        flags.add(ObservationRiskFlag.PAPER_STATE_MUTATION_RISK)
    if "TELEGRAM_REAL_SEND" in ops:
        flags.add(ObservationRiskFlag.TELEGRAM_REAL_SEND_RISK)
    if "CONFIG_PATCH" in ops:
        flags.add(ObservationRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)

    return list(flags)

def aggregate_blocked_operation_history(events: List[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_blocked": blocked_operation_count(events),
        "by_type": blocked_operations_by_type(events),
        "risk_flags": [f.value for f in blocked_operation_risk_flags(events)]
    }

def blocked_operation_history_to_text(payload: dict[str, Any]) -> str:
    return f"Blocked Operation History\\nTotal Blocked: {payload.get('total_blocked', 0)}\\nRisk Flags: {len(payload.get('risk_flags', []))}"
"""

FILES["usa_signal_bot/paper_observation/notification_safety_history.py"] = """\
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
    return f"Notification Safety History\\nWarnings: {payload.get('warning_count', 0)}\\nUnsafe Detections: {payload.get('unsafe_messages_detected', 0)}"
"""

for file_path, content in FILES.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created {file_path}")
