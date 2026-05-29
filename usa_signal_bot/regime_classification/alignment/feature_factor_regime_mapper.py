from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    FrozenFactorAlignmentReference, RegimeAwareAlignmentSpec, RegimeContextCompatibilityResult,
    create_regime_context_compatibility_result_id, _now
)
from usa_signal_bot.core.enums import RegimeCompatibilityKind, RegimeAlignmentQuality

def map_factor_columns_to_regime_context(refs: list[FrozenFactorAlignmentReference], behavior_profiles: list[dict[str, Any]], specs: list[RegimeAwareAlignmentSpec]) -> list[RegimeContextCompatibilityResult]:
    res = []
    for ref in refs:
        if not ref.available: continue
        sym_profiles = [p for p in behavior_profiles if p.get("symbol") == ref.symbol]
        if not sym_profiles: continue
        prof = sym_profiles[0]

        for sp in specs:
            if sp.alignment_kind.name not in ["FACTOR_TO_REGIME_CONTEXT", "FACTOR_TO_BEHAVIOR_PROFILE", "CROSS_SYMBOL_ALIGNMENT"]:
                continue
            for col in ref.factor_columns:
                score = compute_basic_context_compatibility_score(col, prof, sp)
                n_score = score / 100.0
                res.append(RegimeContextCompatibilityResult(
                    compatibility_id=create_regime_context_compatibility_result_id(),
                    created_at_utc=_now(),
                    symbol=ref.symbol,
                    source_column=col,
                    source_kind="factor",
                    regime_label=infer_regime_label_from_behavior_profile(prof),
                    behavior_profile_name=prof.get("profile_name"),
                    compatibility_kind=RegimeCompatibilityKind.NEUTRAL,
                    compatibility_metric_kind=sp.compatibility_metric_kind,
                    compatibility_score=score,
                    normalized_compatibility_score=n_score,
                    confidence_proxy=0.5,
                    quality=RegimeAlignmentQuality.ACCEPTABLE
                ))
    return res

def map_feature_columns_to_regime_context(refs: list[FrozenFactorAlignmentReference], behavior_profiles: list[dict[str, Any]], specs: list[RegimeAwareAlignmentSpec]) -> list[RegimeContextCompatibilityResult]:
    res = []
    for ref in refs:
        if not ref.available: continue
        sym_profiles = [p for p in behavior_profiles if p.get("symbol") == ref.symbol]
        if not sym_profiles: continue
        prof = sym_profiles[0]

        for sp in specs:
            if sp.alignment_kind.name not in ["FEATURE_TO_REGIME_CONTEXT", "FEATURE_TO_BEHAVIOR_PROFILE", "CROSS_SYMBOL_ALIGNMENT"]:
                continue
            for col in ref.feature_columns:
                score = compute_basic_context_compatibility_score(col, prof, sp)
                n_score = score / 100.0
                res.append(RegimeContextCompatibilityResult(
                    compatibility_id=create_regime_context_compatibility_result_id(),
                    created_at_utc=_now(),
                    symbol=ref.symbol,
                    source_column=col,
                    source_kind="feature",
                    regime_label=infer_regime_label_from_behavior_profile(prof),
                    behavior_profile_name=prof.get("profile_name"),
                    compatibility_kind=RegimeCompatibilityKind.NEUTRAL,
                    compatibility_metric_kind=sp.compatibility_metric_kind,
                    compatibility_score=score,
                    normalized_compatibility_score=n_score,
                    confidence_proxy=0.5,
                    quality=RegimeAlignmentQuality.ACCEPTABLE
                ))
    return res

def infer_regime_label_from_behavior_profile(profile: dict[str, Any]) -> str | None:
    return profile.get("inferred_regime_label", profile.get("regime_label"))

def compute_basic_context_compatibility_score(source_column: str, behavior_profile: dict[str, Any], spec: RegimeAwareAlignmentSpec) -> float:
    # Heuristic proxy, NOT ML
    return 50.0

def validate_feature_factor_regime_mapping(results: list[RegimeContextCompatibilityResult]) -> list[str]:
    errs = []
    for r in results:
        if r.produces_trade_signal: errs.append(f"Result {r.compatibility_id} has signal")
    return errs

def feature_factor_regime_mapper_summary(results: list[RegimeContextCompatibilityResult]) -> dict[str, Any]:
    return {"count": len(results)}

def feature_factor_regime_mapper_to_text(results: list[RegimeContextCompatibilityResult], limit: int = 300) -> str:
    return f"Mapped {len(results)} items."
