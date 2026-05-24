from typing import Dict, Any, List

def build_notification_boundary_registry() -> Dict[str, Any]:
    return {
        "telegram_real_send": False,
        "preview_only": True,
        "dry_run": True,
        "investment_advice_allowed": False
    }

def validate_notification_boundary_registry(registry: Dict[str, Any]) -> List[str]:
    errors = []
    if registry.get("telegram_real_send", True):
        errors.append("telegram_real_send must be False")
    return errors

def notification_boundary_to_text(registry: Dict[str, Any]) -> str:
    return f"Telegram Real Send: {registry.get('telegram_real_send')}\nPreview Only: {registry.get('preview_only')}"
