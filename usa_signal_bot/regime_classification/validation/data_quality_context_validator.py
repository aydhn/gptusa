from typing import Any
from usa_signal_bot.core.enums import ConditionalDiagnosticKind
from usa_signal_bot.regime_classification.validation.phase132_models import ConditionalDiagnosticResult

def detect_data_quality_limited_contexts(compatibility_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [c for c in compatibility_results if c.get("data_quality_limited", False)]

def validate_data_quality_context_explanations(items: list[dict[str, Any]], diagnostics: list[ConditionalDiagnosticResult]) -> list[str]:
    errors = []
    return errors

def data_quality_limited_rate(compatibility_results: list[dict[str, Any]]) -> float:
    if not compatibility_results:
        return 0.0
    dq = len(detect_data_quality_limited_contexts(compatibility_results))
    return float(dq) / len(compatibility_results)

def data_quality_context_validator_summary(items: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    return {"data_quality_limited_count": len(items), "errors": len(errors)}

def data_quality_context_validator_to_text(items: list[dict[str, Any]], errors: list[str], limit: int = 200) -> str:
    return f"Data Quality Validator: {len(items)} limited contexts. {len(errors)} errors."
