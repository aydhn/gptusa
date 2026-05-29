from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    RegimeContextCompatibilityResult, AlignmentDiagnosticsProfile,
    create_alignment_diagnostics_profile_id, _now
)
from usa_signal_bot.regime_classification.alignment.alignment_diagnostics_builder import (
    infer_alignment_quality, build_alignment_diagnostic_summary
)
from usa_signal_bot.core.enums import RegimeCompatibilityKind

def build_cross_symbol_compatibility_profile(results: list[RegimeContextCompatibilityResult]) -> AlignmentDiagnosticsProfile:
    comp_count = len(results)
    high_count = sum(1 for r in results if r.compatibility_kind == RegimeCompatibilityKind.COMPATIBLE)
    low_count = compute_cross_symbol_low_compatibility_count(results)
    unc_count = compute_cross_symbol_uncertainty_count(results)
    dql_count = sum(1 for r in results if r.compatibility_kind == RegimeCompatibilityKind.DATA_QUALITY_LIMITED)

    avg_score = sum(r.compatibility_score for r in results) / comp_count if comp_count else None
    avg_conf = sum(r.confidence_proxy or 0 for r in results) / comp_count if comp_count else None

    prof = AlignmentDiagnosticsProfile(
        diagnostics_id=create_alignment_diagnostics_profile_id(),
        created_at_utc=_now(),
        symbol=None,
        profile_name="cross_symbol_profile",
        compatibility_count=comp_count,
        high_compatibility_count=high_count,
        low_compatibility_count=low_count,
        uncertain_count=unc_count,
        data_quality_limited_count=dql_count,
        average_compatibility_score=avg_score,
        average_confidence_proxy=avg_conf,
        diagnostic_summary=""
    )
    prof.quality = infer_alignment_quality(prof)
    prof.diagnostic_summary = build_alignment_diagnostic_summary(prof)
    return prof

def compute_cross_symbol_compatibility_distribution(results: list[RegimeContextCompatibilityResult]) -> dict[str, Any]:
    return {"count": len(results)}

def compute_cross_symbol_low_compatibility_count(results: list[RegimeContextCompatibilityResult]) -> int:
    return sum(1 for r in results if r.compatibility_kind == RegimeCompatibilityKind.LOW_COMPATIBILITY)

def compute_cross_symbol_uncertainty_count(results: list[RegimeContextCompatibilityResult]) -> int:
    return sum(1 for r in results if r.compatibility_kind == RegimeCompatibilityKind.UNCERTAIN)

def validate_cross_symbol_compatibility_profile(profile: AlignmentDiagnosticsProfile) -> list[str]:
    errs = []
    if profile.produces_portfolio_weights:
        errs.append("Cross-symbol profile produces portfolio weights")
    return errs

def cross_symbol_compatibility_summary(profile: AlignmentDiagnosticsProfile) -> dict[str, Any]:
    return {"name": profile.profile_name}

def cross_symbol_compatibility_to_text(profile: AlignmentDiagnosticsProfile) -> str:
    return f"Cross symbol profile: {profile.diagnostic_summary}"
