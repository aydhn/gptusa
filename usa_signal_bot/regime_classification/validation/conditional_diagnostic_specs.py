from typing import Any
from usa_signal_bot.core.enums import ConditionalDiagnosticKind, ConditionalDiagnosticSeverity
from usa_signal_bot.regime_classification.validation.phase132_models import (
    ConditionalDiagnosticSpec,
    create_conditional_diagnostic_spec_id,
    _now_utc
)

def build_default_conditional_diagnostic_specs() -> list[ConditionalDiagnosticSpec]:
    specs = []

    # Low compatibility
    specs.append(ConditionalDiagnosticSpec(
        spec_id=create_conditional_diagnostic_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="Low Compatibility Trigger",
        diagnostic_kind=ConditionalDiagnosticKind.LOW_COMPATIBILITY_DIAGNOSTIC,
        trigger_conditions=["compatibility_score < 40"],
        required_fields=["score"],
        severity=ConditionalDiagnosticSeverity.WARNING,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Uncertain
    specs.append(ConditionalDiagnosticSpec(
        spec_id=create_conditional_diagnostic_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="Uncertain Context Trigger",
        diagnostic_kind=ConditionalDiagnosticKind.UNCERTAIN_COMPATIBILITY_DIAGNOSTIC,
        trigger_conditions=["classification == 'uncertain'"],
        required_fields=["classification"],
        severity=ConditionalDiagnosticSeverity.WARNING,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Conflicted
    specs.append(ConditionalDiagnosticSpec(
        spec_id=create_conditional_diagnostic_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="Conflicted Context Trigger",
        diagnostic_kind=ConditionalDiagnosticKind.CONFLICTED_CONTEXT_DIAGNOSTIC,
        trigger_conditions=["classification == 'conflicted'"],
        required_fields=["classification"],
        severity=ConditionalDiagnosticSeverity.HIGH_WARNING,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Data quality
    specs.append(ConditionalDiagnosticSpec(
        spec_id=create_conditional_diagnostic_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="Data Quality Limited Trigger",
        diagnostic_kind=ConditionalDiagnosticKind.DATA_QUALITY_LIMITED_DIAGNOSTIC,
        trigger_conditions=["data_quality_limited == true"],
        required_fields=["data_quality_limited"],
        severity=ConditionalDiagnosticSeverity.HIGH_WARNING,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Churn sensitive
    specs.append(ConditionalDiagnosticSpec(
        spec_id=create_conditional_diagnostic_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="Churn Sensitive Trigger",
        diagnostic_kind=ConditionalDiagnosticKind.CHURN_SENSITIVE_CONTEXT_DIAGNOSTIC,
        trigger_conditions=["churn_flag == true"],
        required_fields=["churn_flag"],
        severity=ConditionalDiagnosticSeverity.INFO,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Low stability
    specs.append(ConditionalDiagnosticSpec(
        spec_id=create_conditional_diagnostic_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="Low Stability Trigger",
        diagnostic_kind=ConditionalDiagnosticKind.LOW_STABILITY_CONTEXT_DIAGNOSTIC,
        trigger_conditions=["stability_score < 50"],
        required_fields=["stability_score"],
        severity=ConditionalDiagnosticSeverity.WARNING,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Cross symbol disagreement
    specs.append(ConditionalDiagnosticSpec(
        spec_id=create_conditional_diagnostic_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="Cross Symbol Disagreement Trigger",
        diagnostic_kind=ConditionalDiagnosticKind.CROSS_SYMBOL_DISAGREEMENT_DIAGNOSTIC,
        trigger_conditions=["cross_symbol_disagreement == true"],
        required_fields=["cross_symbol_disagreement"],
        severity=ConditionalDiagnosticSeverity.INFO,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    # Missing artifact
    specs.append(ConditionalDiagnosticSpec(
        spec_id=create_conditional_diagnostic_spec_id(),
        created_at_utc=_now_utc(),
        spec_name="Missing Artifact Trigger",
        diagnostic_kind=ConditionalDiagnosticKind.MISSING_ARTIFACT_DIAGNOSTIC,
        trigger_conditions=["missing_artifact == true"],
        required_fields=["missing_artifact"],
        severity=ConditionalDiagnosticSeverity.BLOCKING,
        deterministic=True,
        research_metadata_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    return specs

def conditional_diagnostic_spec_by_kind(kind: ConditionalDiagnosticKind, specs: list[ConditionalDiagnosticSpec] | None = None) -> ConditionalDiagnosticSpec | None:
    if specs is None:
        specs = build_default_conditional_diagnostic_specs()
    for s in specs:
        if s.diagnostic_kind == kind:
            return s
    return None

def validate_conditional_diagnostic_specs(specs: list[ConditionalDiagnosticSpec]) -> list[str]:
    errors = []
    required = {
        ConditionalDiagnosticKind.LOW_COMPATIBILITY_DIAGNOSTIC,
        ConditionalDiagnosticKind.UNCERTAIN_COMPATIBILITY_DIAGNOSTIC,
        ConditionalDiagnosticKind.CONFLICTED_CONTEXT_DIAGNOSTIC,
        ConditionalDiagnosticKind.DATA_QUALITY_LIMITED_DIAGNOSTIC,
        ConditionalDiagnosticKind.CHURN_SENSITIVE_CONTEXT_DIAGNOSTIC,
        ConditionalDiagnosticKind.LOW_STABILITY_CONTEXT_DIAGNOSTIC,
        ConditionalDiagnosticKind.CROSS_SYMBOL_DISAGREEMENT_DIAGNOSTIC,
        ConditionalDiagnosticKind.MISSING_ARTIFACT_DIAGNOSTIC
    }
    present = {s.diagnostic_kind for s in specs}
    missing = required - present
    if missing:
        errors.append(f"Missing required specs: {[m.value for m in missing]}")
    return errors

def conditional_diagnostic_specs_summary(specs: list[ConditionalDiagnosticSpec]) -> dict[str, Any]:
    return {"total": len(specs)}

def conditional_diagnostic_specs_to_text(specs: list[ConditionalDiagnosticSpec], limit: int = 200) -> str:
    return f"{len(specs)} conditional diagnostic specs defined."
