from usa_signal_bot.provider_cache.phase108_models import SourceComparisonResult, DataConfidenceHint
from typing import Any

def validate_source_comparison_safety(result: SourceComparisonResult) -> list[str]:
    errors = []
    if not result.dry_run_only: errors.append("dry_run_only false")
    if result.network_used: errors.append("network_used true")
    if result.broker_used: errors.append("broker_used true")
    return errors

def validate_data_confidence_hints_safety(items: list[DataConfidenceHint]) -> list[str]:
    errors = []
    for h in items:
        if source_comparison_has_trade_language(h.recommended_action):
            errors.append(f"Trade language in hint {h.hint_id}: {h.recommended_action}")
    return errors

def source_comparison_has_trade_language(text: str) -> bool:
    unsafe = ["buy", "sell", "strong buy", "kesin al", "kesin sat", "emir", "order", "trade", "garanti"]
    t = text.lower()
    for u in unsafe:
        if u in t: return True
    return False

def source_comparison_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "errors": errors}

def source_comparison_safety_validator_to_text(errors: list[str]) -> str:
    if not errors: return "Source comparison is safe."
    return f"Source comparison Safety Errors: {errors}"
