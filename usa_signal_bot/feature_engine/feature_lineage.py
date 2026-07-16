from typing import Any
from usa_signal_bot.feature_engine.phase116_models import FeatureDefinition, FactorDefinition

def build_feature_lineage_metadata(feature: FeatureDefinition, source_inputs: list[str] | None = None) -> dict[str, Any]:
    return {
        "feature_id": feature.feature_id,
        "source_inputs": source_inputs or [],
        "source_indicator_id": feature.source_indicator_id,
        "lineage_valid": True
    }

def build_factor_lineage_metadata(factor: FactorDefinition, source_features: list[str] | None = None) -> dict[str, Any]:
    return {
        "factor_id": factor.factor_id,
        "source_features": source_features or [],
        "lineage_valid": True
    }

def validate_feature_lineage_metadata(payload: dict[str, Any]) -> list[str]:
    errors = []
    for k in payload.keys():
        k_lower = k.lower()
        if "secret" in k_lower or "token" in k_lower or "password" in k_lower or "key" in k_lower or "api_key" in k_lower or "broker_order_id" in k_lower or "signal" in k_lower or "order" in k_lower:
            errors.append(f"Unsafe key in lineage metadata: {k}")
    return errors

def feature_lineage_summary(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    return {"total_lineages": len(payloads)}

def feature_lineage_to_text(payloads: list[dict[str, Any]], limit: int = 200) -> str:
    return f"Total lineages: {len(payloads)}"
