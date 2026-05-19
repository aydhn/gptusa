import json
from typing import Any, Dict, List
from usa_signal_bot.core.enums import BundleSafetyFlag

def scan_text_for_secret_like_patterns(text: str) -> List[BundleSafetyFlag]:
    text_lower = text.lower()
    flags = []
    patterns = ["api_key", "token", "secret", "password", "bearer", "private_key"]
    for p in patterns:
        if p in text_lower:
            flags.append(BundleSafetyFlag.SECRET_LEAK_RISK)
            break
    return flags

def scan_payload_for_secret_keys(payload: Dict[str, Any]) -> List[BundleSafetyFlag]:
    return scan_text_for_secret_like_patterns(json.dumps(payload))

def scan_payload_for_broker_order_fields(payload: Dict[str, Any]) -> List[BundleSafetyFlag]:
    text_lower = json.dumps(payload).lower()
    flags = []
    patterns = [
        "broker_order_id", "live_order_id", "sent_to_broker",
        "execution_venue", "real_fill_id", "order_routing_enabled",
        "live_enabled", "demo_enabled"
    ]
    for p in patterns:
        if p in text_lower:
            flags.append(BundleSafetyFlag.BROKER_FIELD_RISK)
            break
    return flags

def scan_text_for_live_execution_language(text: str) -> List[BundleSafetyFlag]:
    text_lower = text.lower()
    flags = []
    patterns = ["live approved", "sent to broker", "kesin al", "garanti", "production'a geçir", "canlıya al", "kesin kâr"]
    for p in patterns:
        if p in text_lower:
            flags.append(BundleSafetyFlag.LIVE_EXECUTION_LANGUAGE)
            break
    return flags

def scan_text_for_auto_apply_language(text: str) -> List[BundleSafetyFlag]:
    text_lower = text.lower()
    flags = []
    patterns = ["otomatik uygula", "auto_apply", "enable_live", "send_order"]
    for p in patterns:
        if p in text_lower:
            flags.append(BundleSafetyFlag.AUTO_APPLY_LANGUAGE)
            break
    return flags

def scan_payload_safety(payload: Dict[str, Any]) -> List[BundleSafetyFlag]:
    flags = set()
    flags.update(scan_payload_for_secret_keys(payload))
    flags.update(scan_payload_for_broker_order_fields(payload))

    text = json.dumps(payload)
    flags.update(scan_text_for_live_execution_language(text))
    flags.update(scan_text_for_auto_apply_language(text))

    return list(flags)

def safety_flags_to_text(flags: List[BundleSafetyFlag]) -> str:
    if not flags:
        return "No safety risks detected."
    return "Detected safety risks: " + ", ".join([f.value for f in flags])
