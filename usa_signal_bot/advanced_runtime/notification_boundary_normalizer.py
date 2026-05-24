from typing import Any

def normalize_notification_boundary(registry: dict[str, Any]) -> dict[str, Any]:
    registry["dry_run"] = True
    registry["telegram_real_send"] = False
    registry["preview_only"] = True
    return registry

def validate_normalized_notification_boundary(registry: dict[str, Any]) -> list[str]:
    errors = []
    if not registry.get("dry_run"): errors.append("dry_run must be True")
    if registry.get("telegram_real_send"): errors.append("telegram_real_send must be False")
    return errors

def notification_boundary_normalizer_to_text(registry: dict[str, Any]) -> str:
    return "Notification boundary normalized."
