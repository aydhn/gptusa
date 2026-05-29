from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    RegimeContextCompatibilityResult, AlignmentDiagnosticsProfile,
    create_alignment_diagnostics_profile_id, _now
)
from usa_signal_bot.core.enums import RegimeCompatibilityKind, RegimeAlignmentQuality

def build_alignment_diagnostics_profiles(results: list[RegimeContextCompatibilityResult]) -> list[AlignmentDiagnosticsProfile]:
    if not results: return []
    syms = set(r.symbol for r in results if r.symbol)
    if not syms: return [build_alignment_diagnostics_profile(None, results)]

    profiles = []
    for sym in syms:
        sym_res = [r for r in results if r.symbol == sym]
        profiles.append(build_alignment_diagnostics_profile(sym, sym_res))
    return profiles

def build_alignment_diagnostics_profile(symbol: str | None, results: list[RegimeContextCompatibilityResult]) -> AlignmentDiagnosticsProfile:
    comp_count = len(results)
    high_count = sum(1 for r in results if r.compatibility_kind == RegimeCompatibilityKind.COMPATIBLE)
    low_count = sum(1 for r in results if r.compatibility_kind == RegimeCompatibilityKind.LOW_COMPATIBILITY)
    unc_count = sum(1 for r in results if r.compatibility_kind == RegimeCompatibilityKind.UNCERTAIN)
    dql_count = sum(1 for r in results if r.compatibility_kind == RegimeCompatibilityKind.DATA_QUALITY_LIMITED)

    avg_score = sum(r.compatibility_score for r in results) / comp_count if comp_count else None
    avg_conf = sum(r.confidence_proxy or 0 for r in results) / comp_count if comp_count else None

    prof = AlignmentDiagnosticsProfile(
        diagnostics_id=create_alignment_diagnostics_profile_id(),
        created_at_utc=_now(),
        symbol=symbol,
        profile_name=f"diagnostics_{symbol or 'global'}",
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

def infer_alignment_quality(profile: AlignmentDiagnosticsProfile) -> RegimeAlignmentQuality:
    if profile.data_quality_limited_count > 0: return RegimeAlignmentQuality.WARNING
    if profile.average_compatibility_score is not None and profile.average_compatibility_score >= 70:
        return RegimeAlignmentQuality.HIGH
    return RegimeAlignmentQuality.ACCEPTABLE

def build_alignment_diagnostic_summary(profile: AlignmentDiagnosticsProfile) -> str:
    return f"Profile {profile.profile_name}: {profile.high_compatibility_count} high compat, {profile.low_compatibility_count} low compat."

def validate_alignment_diagnostics_profiles(profiles: list[AlignmentDiagnosticsProfile]) -> list[str]:
    errs = []
    for p in profiles:
        if p.produces_trade_signal: errs.append(f"Profile {p.diagnostics_id} has signal")
    return errs

def alignment_diagnostics_summary(profiles: list[AlignmentDiagnosticsProfile]) -> dict[str, Any]:
    return {"count": len(profiles)}

def alignment_diagnostics_to_text(profiles: list[AlignmentDiagnosticsProfile], limit: int = 300) -> str:
    return f"Built {len(profiles)} diagnostics."
