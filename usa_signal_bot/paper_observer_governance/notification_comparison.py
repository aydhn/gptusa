from typing import Any
from usa_signal_bot.core.enums import ObserverGovernanceRiskFlag

UNSAFE_WORDS = ["gönderildi", "emir gönder", "kesin al", "kesin sat", "paper'a uygula", "canlıya al", "aktif et", "garanti"]

def compare_observer_notification_safety(observer_payload: dict[str, Any]) -> dict[str, Any]:
    previews = observer_payload.get("notification_previews", [])
    violations = []
    for preview in previews:
        unsafe = detect_observer_notification_unsafe_language(preview.get("message", ""))
        if unsafe: violations.extend(unsafe)
    return {"status": "FAIL" if violations else "PASS", "violations": violations}

def detect_observer_notification_unsafe_language(text: str) -> list[str]:
    text_lower = text.lower()
    return [w for w in UNSAFE_WORDS if w in text_lower]

def count_observer_notification_previews(observer_payload: dict[str, Any]) -> int:
    return len(observer_payload.get("notification_previews", []))

def notification_comparison_risk_flags(payload: dict[str, Any]) -> list[ObserverGovernanceRiskFlag]:
    if payload.get("status") == "FAIL": return [ObserverGovernanceRiskFlag.NOTIFICATION_UNSAFE]
    return []

def notification_comparison_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
