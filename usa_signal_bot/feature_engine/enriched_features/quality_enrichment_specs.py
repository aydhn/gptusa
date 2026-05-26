from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import FeatureEnrichmentFamily
from usa_signal_bot.feature_engine.enriched_features.phase119_models import (
    FeatureEnrichmentSpec,
    create_feature_enrichment_spec_id
)

def build_quality_enrichment_specs() -> list[FeatureEnrichmentSpec]:
    names = [
        "provider_quality_score_feature",
        "source_trust_score_feature",
        "data_confidence_score_feature",
        "cache_freshness_score_feature",
        "lineage_completeness_score_feature",
        "validation_warning_count_feature",
    ]

    specs = []
    for name in names:
        specs.append(
            FeatureEnrichmentSpec(
                spec_id=create_feature_enrichment_spec_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                name=name,
                family=FeatureEnrichmentFamily.QUALITY_AWARE,
                kind=name.upper(),
                local_pandas_only=True,
                requires_network=False,
                requires_paid_api=False,
                requires_scraping=False,
                produces_trade_signal=False,
                produces_order_decision=False,
                produces_portfolio_weights=False,
            )
        )
    return specs

def quality_enrichment_spec_by_name(name: str, specs: list[FeatureEnrichmentSpec] | None = None) -> FeatureEnrichmentSpec | None:
    specs = specs or build_quality_enrichment_specs()
    for s in specs:
        if s.name == name:
            return s
    return None

def validate_quality_enrichment_specs(specs: list[FeatureEnrichmentSpec]) -> list[str]:
    return []

def quality_enrichment_specs_summary(specs: list[FeatureEnrichmentSpec]) -> dict[str, Any]:
    return {"spec_count": len(specs)}

def quality_enrichment_specs_to_text(specs: list[FeatureEnrichmentSpec], limit: int = 100) -> str:
    return f"{len(specs)} quality specs"
