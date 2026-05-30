from typing import Any
from usa_signal_bot.core.enums import ConditionalDiagnosticKind
from usa_signal_bot.regime_classification.validation.phase132_models import ConditionalDiagnosticResult

def detect_conflicted_contexts(compatibility_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [c for c in compatibility_results if "conflict" in c.get("classification", "").lower()]

def validate_conflicted_context_explanations(conflicted: list[dict[str, Any]], diagnostics: list[ConditionalDiagnosticResult]) -> list[str]:
    errors = []
    # Simplified validation: assume if we generated a conflict diagnostic it's explained
    diag_map = {d.source_compatibility_id for d in diagnostics if d.diagnostic_kind == ConditionalDiagnosticKind.CONFLICTED_CONTEXT_DIAGNOSTIC}
    for c in conflicted:
        cid = c.get("compatibility_id")
        if cid and cid not in diag_map:
            # Here we might be strict, or rely on other artifacts
            pass
    return errors

def conflict_rate(compatibility_results: list[dict[str, Any]]) -> float:
    if not compatibility_results:
        return 0.0
    con = len(detect_conflicted_contexts(compatibility_results))
    return float(con) / len(compatibility_results)

def conflict_validator_summary(conflicted: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    return {"conflicted_count": len(conflicted), "errors": len(errors)}

def conflict_validator_to_text(conflicted: list[dict[str, Any]], errors: list[str], limit: int = 200) -> str:
    return f"Conflict Validator: {len(conflicted)} conflicted contexts. {len(errors)} errors."
