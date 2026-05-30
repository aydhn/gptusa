from typing import Any
from usa_signal_bot.core.enums import ConditionalDiagnosticKind, ConditionalDiagnosticSeverity, RegimeContextValidationQuality
from usa_signal_bot.regime_classification.validation.phase132_models import (
    ConditionalDiagnosticSpec,
    ConditionalDiagnosticResult,
    ConditionalDiagnosticsProfile,
    create_conditional_diagnostic_result_id,
    create_conditional_diagnostics_profile_id,
    _now_utc
)
from usa_signal_bot.regime_classification.validation.conditional_diagnostic_specs import build_default_conditional_diagnostic_specs

def diagnostic_triggered(result: dict[str, Any], spec: ConditionalDiagnosticSpec) -> bool:
    if spec.diagnostic_kind == ConditionalDiagnosticKind.LOW_COMPATIBILITY_DIAGNOSTIC:
        return result.get("score", 100) < 40 or "low" in result.get("classification", "").lower()
    if spec.diagnostic_kind == ConditionalDiagnosticKind.UNCERTAIN_COMPATIBILITY_DIAGNOSTIC:
        return "uncertain" in result.get("classification", "").lower()
    if spec.diagnostic_kind == ConditionalDiagnosticKind.CONFLICTED_CONTEXT_DIAGNOSTIC:
        return "conflict" in result.get("classification", "").lower()
    if spec.diagnostic_kind == ConditionalDiagnosticKind.DATA_QUALITY_LIMITED_DIAGNOSTIC:
        return result.get("data_quality_limited", False)
    # mock for others
    return False

def infer_conditional_diagnostic_severity(result: dict[str, Any], spec: ConditionalDiagnosticSpec) -> ConditionalDiagnosticSeverity:
    return spec.severity

def build_conditional_diagnostic_for_result(result: dict[str, Any], spec: ConditionalDiagnosticSpec) -> ConditionalDiagnosticResult:
    return ConditionalDiagnosticResult(
        diagnostic_id=create_conditional_diagnostic_result_id(),
        created_at_utc=_now_utc(),
        symbol=result.get("symbol"),
        source_compatibility_id=result.get("compatibility_id"),
        diagnostic_kind=spec.diagnostic_kind,
        severity=infer_conditional_diagnostic_severity(result, spec),
        condition_name=spec.spec_name,
        condition_triggered=True,
        diagnostic_text=f"Triggered {spec.spec_name} for symbol {result.get('symbol')}",
        supporting_metrics={"score": result.get("score")},
        recommended_action_type="research_review",
        required_human_review=spec.severity in [ConditionalDiagnosticSeverity.HIGH_WARNING, ConditionalDiagnosticSeverity.BLOCKING],
        research_metadata_only=True,
        investment_advice=False,
        activation_allowed=False,
        strategy_activation_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_conditional_diagnostics(
    compatibility_results: list[dict[str, Any]],
    overlay_results: list[dict[str, Any]],
    diagnostics_profiles: list[dict[str, Any]],
    specs: list[ConditionalDiagnosticSpec] | None = None
) -> list[ConditionalDiagnosticResult]:
    if specs is None:
        specs = build_default_conditional_diagnostic_specs()

    results = []
    for comp in compatibility_results:
        for spec in specs:
            if diagnostic_triggered(comp, spec):
                results.append(build_conditional_diagnostic_for_result(comp, spec))
    return results

def build_conditional_diagnostics_profiles(items: list[ConditionalDiagnosticResult]) -> list[ConditionalDiagnosticsProfile]:
    profiles = {}
    for d in items:
        sym = d.symbol or "global"
        if sym not in profiles:
            profiles[sym] = {
                "count": 0, "warn": 0, "block": 0, "low": 0, "unc": 0, "conf": 0, "data": 0
            }
        profiles[sym]["count"] += 1
        if d.severity == ConditionalDiagnosticSeverity.WARNING or d.severity == ConditionalDiagnosticSeverity.HIGH_WARNING:
            profiles[sym]["warn"] += 1
        if d.severity == ConditionalDiagnosticSeverity.BLOCKING:
            profiles[sym]["block"] += 1

        if d.diagnostic_kind == ConditionalDiagnosticKind.LOW_COMPATIBILITY_DIAGNOSTIC:
            profiles[sym]["low"] += 1
        elif d.diagnostic_kind == ConditionalDiagnosticKind.UNCERTAIN_COMPATIBILITY_DIAGNOSTIC:
            profiles[sym]["unc"] += 1
        elif d.diagnostic_kind == ConditionalDiagnosticKind.CONFLICTED_CONTEXT_DIAGNOSTIC:
            profiles[sym]["conf"] += 1
        elif d.diagnostic_kind == ConditionalDiagnosticKind.DATA_QUALITY_LIMITED_DIAGNOSTIC:
            profiles[sym]["data"] += 1

    res = []
    for sym, c in profiles.items():
        q = RegimeContextValidationQuality.HIGH
        if c["block"] > 0:
            q = RegimeContextValidationQuality.BLOCKED
        elif c["warn"] > 0:
            q = RegimeContextValidationQuality.WARNING

        res.append(ConditionalDiagnosticsProfile(
            profile_id=create_conditional_diagnostics_profile_id(),
            created_at_utc=_now_utc(),
            symbol=sym if sym != "global" else None,
            diagnostic_count=c["count"],
            warning_count=c["warn"],
            blocking_count=c["block"],
            low_compatibility_diagnostic_count=c["low"],
            uncertain_diagnostic_count=c["unc"],
            conflicted_diagnostic_count=c["conf"],
            data_quality_limited_diagnostic_count=c["data"],
            profile_summary=f"Profile for {sym} with {c['count']} diagnostics",
            quality=q,
            research_metadata_only=True,
            investment_advice=False,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return res

def validate_conditional_diagnostics(items: list[ConditionalDiagnosticResult]) -> list[str]:
    errors = []
    for item in items:
        valid_actions = ["research_review", "data_quality_review", "documentation_review", "monitor_context", "none"]
        if item.recommended_action_type not in valid_actions:
            errors.append(f"Invalid recommended_action_type {item.recommended_action_type}")
    return errors

def conditional_diagnostics_summary(items: list[ConditionalDiagnosticResult]) -> dict[str, Any]:
    return {"total": len(items)}

def conditional_diagnostics_to_text(items: list[ConditionalDiagnosticResult], limit: int = 300) -> str:
    return f"{len(items)} conditional diagnostics generated."
