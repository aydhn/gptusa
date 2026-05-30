from typing import Any
from usa_signal_bot.regime_classification.validation.phase132_models import (
    RegimeAlignmentIngestionResult,
    CompatibilityValidationRule,
    CompatibilityValidationResult,
    ConditionalDiagnosticSpec,
    ConditionalDiagnosticResult,
    ConditionalDiagnosticsProfile,
    RegimeContextAcceptanceRule,
    RegimeAwareAcceptanceGate,
    RegimeContextValidationContext,
    RegimeContextValidationFullReview
)
from usa_signal_bot.regime_classification.validation.regime_alignment_ingestion import regime_alignment_ingestion_to_text
from usa_signal_bot.regime_classification.validation.compatibility_validation_runner import compatibility_validation_to_text
from usa_signal_bot.regime_classification.validation.conditional_diagnostics_engine import conditional_diagnostics_to_text
from usa_signal_bot.regime_classification.validation.regime_acceptance_gate import regime_acceptance_gate_to_text
from usa_signal_bot.regime_classification.validation.regime_context_validation_report import regime_context_validation_limitations_text

def compatibility_validation_rule_to_text(item: CompatibilityValidationRule) -> str:
    return f"Rule {item.name}: Passed={item.passed}"

def conditional_diagnostic_spec_to_text(item: ConditionalDiagnosticSpec) -> str:
    return f"Spec {item.spec_name}"

def conditional_diagnostic_result_to_text(item: ConditionalDiagnosticResult) -> str:
    return f"Diagnostic {item.condition_name}: {item.diagnostic_text}"

def conditional_diagnostics_profile_to_text(item: ConditionalDiagnosticsProfile) -> str:
    return f"Profile {item.symbol or 'global'}: {item.diagnostic_count} diagnostics"

def regime_context_acceptance_rule_to_text(item: RegimeContextAcceptanceRule) -> str:
    return f"Gate Rule {item.name}: Passed={item.passed}"

def regime_context_validation_context_to_text(item: RegimeContextValidationContext, limit: int = 300) -> str:
    return f"Context {item.context_id}. Status: {item.status.value}"

def regime_context_validation_full_review_to_text(item: RegimeContextValidationFullReview, limit: int = 300) -> str:
    from usa_signal_bot.regime_classification.validation.regime_context_validation_report import regime_context_validation_full_review_to_text as _to_text
    return _to_text(item, limit)

def regime_context_validation_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Store Summary: {summary['reviews']} reviews."

# Re-exporting limits text
__all__ = [
    "regime_alignment_ingestion_to_text",
    "compatibility_validation_rule_to_text",
    "compatibility_validation_to_text",
    "conditional_diagnostic_spec_to_text",
    "conditional_diagnostic_result_to_text",
    "conditional_diagnostics_profile_to_text",
    "regime_context_acceptance_rule_to_text",
    "regime_acceptance_gate_to_text",
    "regime_context_validation_context_to_text",
    "regime_context_validation_full_review_to_text",
    "regime_context_validation_store_summary_to_text",
    "regime_context_validation_limitations_text"
]
