from typing import Any
from usa_signal_bot.provider_orchestration.phase110_models import SourceBlendResult
import re

def validate_source_blend_result_safety(result: SourceBlendResult) -> list[str]:
    errors = []
    if result.produces_trade_signal: errors.append("produces_trade_signal must be False")
    if result.produces_order_decision: errors.append("produces_order_decision must be False")
    if result.network_used: errors.append("network_used must be False")
    if result.broker_used: errors.append("broker_used must be False")
    if result.order_created: errors.append("order_created must be False")
    if result.paper_state_mutated: errors.append("paper_state_mutated must be False")
    return errors

def validate_source_blend_text_safety(text: str) -> list[str]:
    errors = []
    lower_text = text.lower()
    unsafe_terms = [
        "buy", "sell", "strong buy", "strong sell", "kesin al", "kesin sat",
        "emir", "order", "trade", "garanti", "kâr garantisi", "sent to broker", "live trading"
    ]
    for term in unsafe_terms:
        if re.search(r'\b' + re.escape(term) + r'\b', lower_text):
            errors.append(f"Unsafe trade language found: {term}")
    return errors

def source_blending_has_trade_language(text: str) -> bool:
    return len(validate_source_blend_text_safety(text)) > 0

def source_blending_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "error_count": len(errors)}

def source_blending_safety_to_text(errors: list[str]) -> str:
    if not errors: return "Source Blending Result is SAFE."
    return "Source Blending Result is UNSAFE:\n" + "\n".join(errors)
