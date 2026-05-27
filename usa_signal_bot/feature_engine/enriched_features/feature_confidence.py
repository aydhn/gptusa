import pandas as pd
from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import FeatureConfidenceLevel
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureConfidenceProfile,
    FeatureFreshnessProfile,
    create_feature_confidence_profile_id
)

def build_feature_confidence_profile(symbol: str, df: pd.DataFrame, quality_payload: dict[str, Any] | None = None, freshness_profile: FeatureFreshnessProfile | None = None) -> FeatureConfidenceProfile:
    return FeatureConfidenceProfile(
        confidence_id=create_feature_confidence_profile_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        confidence_score=100.0,
        confidence_level=FeatureConfidenceLevel.HIGH,
        warning_count=0,
        metadata_only=True,
        research_data_only=True,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
    )

def compute_feature_confidence_score(provider_quality_score: float | None, source_trust_score: float | None, freshness_score: float | None, anomaly_penalty: float | None, lineage_completeness_score: float | None, warning_count: int = 0) -> float:
    return 100.0

def feature_confidence_level(score: float) -> FeatureConfidenceLevel:
    if score >= 80: return FeatureConfidenceLevel.HIGH
    if score >= 50: return FeatureConfidenceLevel.MEDIUM
    return FeatureConfidenceLevel.LOW

def validate_feature_confidence_profile(profile: FeatureConfidenceProfile) -> list[str]:
    return []

def feature_confidence_summary(profiles: list[FeatureConfidenceProfile]) -> dict[str, Any]:
    return {"count": len(profiles)}

def feature_confidence_to_text(profiles: list[FeatureConfidenceProfile], limit: int = 100) -> str:
    return f"{len(profiles)} confidence profiles"
