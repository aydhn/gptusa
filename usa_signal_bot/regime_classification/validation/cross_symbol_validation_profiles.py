from typing import Any
from usa_signal_bot.regime_classification.validation.phase132_models import (
    ConditionalDiagnosticResult,
    ConditionalDiagnosticsProfile,
    create_conditional_diagnostics_profile_id,
    _now_utc
)
from usa_signal_bot.regime_classification.validation.conditional_diagnostics_engine import build_conditional_diagnostics_profiles
from usa_signal_bot.core.enums import RegimeContextValidationQuality

def build_cross_symbol_validation_profile(
    compatibility_results: list[dict[str, Any]],
    diagnostics: list[ConditionalDiagnosticResult]
) -> ConditionalDiagnosticsProfile:
    profiles = build_conditional_diagnostics_profiles(diagnostics)
    for p in profiles:
        if p.symbol is None:
            return p

    return ConditionalDiagnosticsProfile(
        profile_id=create_conditional_diagnostics_profile_id(),
        created_at_utc=_now_utc(),
        symbol=None,
        diagnostic_count=0,
        warning_count=0,
        blocking_count=0,
        low_compatibility_diagnostic_count=0,
        uncertain_diagnostic_count=0,
        conflicted_diagnostic_count=0,
        data_quality_limited_diagnostic_count=0,
        profile_summary="Empty profile",
        quality=RegimeContextValidationQuality.HIGH,
        research_metadata_only=True,
        investment_advice=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def compute_cross_symbol_validation_distribution(compatibility_results: list[dict[str, Any]]) -> dict[str, Any]:
    return {"total": len(compatibility_results)}

def compute_cross_symbol_blocking_count(diagnostics: list[ConditionalDiagnosticResult]) -> int:
    from usa_signal_bot.core.enums import ConditionalDiagnosticSeverity
    return sum(1 for d in diagnostics if d.severity == ConditionalDiagnosticSeverity.BLOCKING)

def validate_cross_symbol_validation_profile(profile: ConditionalDiagnosticsProfile) -> list[str]:
    errors = []
    if profile.symbol is not None:
        errors.append("Cross symbol profile should have symbol=None for global scope")
    return errors

def cross_symbol_validation_summary(profile: ConditionalDiagnosticsProfile) -> dict[str, Any]:
    if not profile:
        return {}
    return {"diagnostic_count": profile.diagnostic_count, "blocking_count": profile.blocking_count}

def cross_symbol_validation_to_text(profile: ConditionalDiagnosticsProfile) -> str:
    if not profile:
        return "No cross symbol profile."
    return f"Cross Symbol Profile: {profile.diagnostic_count} diagnostics, {profile.blocking_count} blocking."
