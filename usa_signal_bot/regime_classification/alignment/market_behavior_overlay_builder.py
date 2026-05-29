from typing import Any
from usa_signal_bot.regime_classification.alignment.phase131_models import (
    FrozenFactorAlignmentReference, MarketBehaviorOverlaySpec, MarketBehaviorOverlayResult,
    create_market_behavior_overlay_result_id, _now
)
from usa_signal_bot.core.enums import RegimeAlignmentQuality

def build_market_behavior_overlays(refs: list[FrozenFactorAlignmentReference], behavior_profiles: list[dict[str, Any]], specs: list[MarketBehaviorOverlaySpec]) -> list[MarketBehaviorOverlayResult]:
    res = []
    for ref in refs:
        if not ref.available: continue
        sym_profiles = [p for p in behavior_profiles if p.get("symbol") == ref.symbol]
        if not sym_profiles: continue
        prof = sym_profiles[0]

        for sp in specs:
            res.append(build_overlay_for_reference(ref, prof, sp))
    return res

def build_overlay_for_reference(ref: FrozenFactorAlignmentReference, behavior_profile: dict[str, Any], spec: MarketBehaviorOverlaySpec) -> MarketBehaviorOverlayResult:
    score = compute_overlay_score(ref, behavior_profile, spec)
    return MarketBehaviorOverlayResult(
        overlay_id=create_market_behavior_overlay_result_id(),
        created_at_utc=_now(),
        symbol=ref.symbol,
        overlay_name=spec.overlay_name,
        overlay_kind=spec.overlay_kind,
        source_behavior_profile_id=behavior_profile.get("profile_id"),
        target_column=None,
        overlay_score=score,
        normalized_overlay_score=normalize_overlay_score(score),
        quality=RegimeAlignmentQuality.ACCEPTABLE
    )

def compute_overlay_score(ref: FrozenFactorAlignmentReference, behavior_profile: dict[str, Any], spec: MarketBehaviorOverlaySpec) -> float:
    return 60.0

def normalize_overlay_score(score: float) -> float:
    return max(0.0, min(1.0, score / 100.0))

def validate_market_behavior_overlays(items: list[MarketBehaviorOverlayResult]) -> list[str]:
    errs = []
    for i in items:
        if i.overlay_score < 0 or i.overlay_score > 100:
            errs.append(f"Invalid score {i.overlay_score} for {i.overlay_id}")
    return errs

def market_behavior_overlay_summary(items: list[MarketBehaviorOverlayResult]) -> dict[str, Any]:
    return {"count": len(items)}

def market_behavior_overlay_to_text(items: list[MarketBehaviorOverlayResult], limit: int = 300) -> str:
    return f"Built {len(items)} overlays."
