from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    FrozenFactorAlignmentReference, RegimeAwareAlignmentSpec, RegimeContextCompatibilityResult
)
from usa_signal_bot.regime_classification.alignment.feature_factor_regime_mapper import (
    map_factor_columns_to_regime_context, map_feature_columns_to_regime_context
)
from usa_signal_bot.core.enums import RegimeCompatibilityKind

def compute_regime_context_compatibility(refs: list[FrozenFactorAlignmentReference], behavior_profiles: list[dict[str, Any]], diagnostics: list[dict[str, Any]] | None = None, specs: list[RegimeAwareAlignmentSpec] | None = None) -> list[RegimeContextCompatibilityResult]:
    if not specs: return []
    res = []
    res.extend(map_factor_columns_to_regime_context(refs, behavior_profiles, specs))
    res.extend(map_feature_columns_to_regime_context(refs, behavior_profiles, specs))

    for r in res:
        r.compatibility_score = compute_compatibility_score(r.source_column, {}, diagnostics)
        r.normalized_compatibility_score = normalize_compatibility_score(r.compatibility_score)
        r.compatibility_kind = classify_compatibility(r.compatibility_score)
        r.confidence_proxy = compute_compatibility_confidence_proxy(r.compatibility_score, {})
    return res

def compute_compatibility_score(source_column: str, behavior_profile: dict[str, Any], diagnostics: list[dict[str, Any]] | None = None) -> float:
    return 70.0

def normalize_compatibility_score(score: float) -> float:
    return max(0.0, min(1.0, score / 100.0))

def classify_compatibility(score: float, data_quality_limited: bool = False, conflicted: bool = False) -> RegimeCompatibilityKind:
    if conflicted: return RegimeCompatibilityKind.CONFLICTED
    if data_quality_limited: return RegimeCompatibilityKind.DATA_QUALITY_LIMITED
    if score >= 80: return RegimeCompatibilityKind.COMPATIBLE
    if score >= 60: return RegimeCompatibilityKind.PARTIALLY_COMPATIBLE
    if score >= 40: return RegimeCompatibilityKind.NEUTRAL
    if score >= 20: return RegimeCompatibilityKind.UNCERTAIN
    return RegimeCompatibilityKind.LOW_COMPATIBILITY

def compute_compatibility_confidence_proxy(score: float, behavior_profile: dict[str, Any]) -> float:
    return 0.8

def validate_compatibility_results(results: list[RegimeContextCompatibilityResult]) -> list[str]:
    errs = []
    for r in results:
        if r.compatibility_score < 0 or r.compatibility_score > 100:
            errs.append(f"Invalid score in {r.compatibility_id}")
    return errs

def compatibility_engine_summary(results: list[RegimeContextCompatibilityResult]) -> dict[str, Any]:
    return {"count": len(results)}

def compatibility_engine_to_text(results: list[RegimeContextCompatibilityResult], limit: int = 300) -> str:
    return f"Computed {len(results)} compatibilities."
