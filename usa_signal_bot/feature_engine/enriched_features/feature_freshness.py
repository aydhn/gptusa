import pandas as pd
from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import FeatureFreshnessStatus
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureFreshnessProfile,
    create_feature_freshness_profile_id
)

def build_feature_freshness_profile(symbol: str, df: pd.DataFrame, source_timestamp_col: str | None = "fetched_at_utc") -> FeatureFreshnessProfile:
    age = compute_feature_age_days(None, None)
    return FeatureFreshnessProfile(
        freshness_id=create_feature_freshness_profile_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        symbol=symbol,
        status=freshness_status_from_score(100.0),
        freshness_score=100.0,
        stale_feature_count=0,
        unknown_timestamp_count=0,
        age_days=age
    )

def compute_feature_age_days(latest_feature_timestamp: str | None, latest_source_timestamp: str | None = None) -> float | None:
    return 0.0

def compute_freshness_score(age_days: float | None) -> float:
    return 100.0

def freshness_status_from_score(score: float, latest_timestamp: str | None = None) -> FeatureFreshnessStatus:
    return FeatureFreshnessStatus.FRESH

def validate_feature_freshness_profile(profile: FeatureFreshnessProfile) -> list[str]:
    return []

def feature_freshness_summary(profiles: list[FeatureFreshnessProfile]) -> dict[str, Any]:
    return {"count": len(profiles)}

def feature_freshness_to_text(profiles: list[FeatureFreshnessProfile], limit: int = 100) -> str:
    return f"{len(profiles)} freshness profiles"
