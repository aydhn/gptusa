import datetime
from typing import Any
from usa_signal_bot.core.enums import FeatureCategory, FeatureDataType, FeatureComputationMode, FeatureFoundationRiskFlag
from usa_signal_bot.feature_engine.phase116_models import FeatureDefinition, create_feature_definition_id, IndicatorDefinition, validate_feature_definition

def build_default_feature_definitions(indicators: list[IndicatorDefinition] | None = None) -> list[FeatureDefinition]:
    default_groups = [
        ("raw_close_passthrough", FeatureCategory.RAW_OHLCV),
        ("daily_return", FeatureCategory.RETURN_FEATURE),
        ("log_return_metadata_placeholder", FeatureCategory.RETURN_FEATURE),
        ("rolling_mean_placeholder", FeatureCategory.ROLLING_WINDOW),
        ("rolling_volatility_placeholder", FeatureCategory.VOLATILITY_FEATURE),
        ("momentum_placeholder", FeatureCategory.MOMENTUM_FEATURE),
        ("trend_slope_placeholder", FeatureCategory.TREND_FEATURE),
        ("volume_anomaly_placeholder", FeatureCategory.VOLUME_FEATURE),
        ("volatility_regime_metadata_placeholder", FeatureCategory.VOLATILITY_FEATURE),
        ("event_context_feature_placeholder", FeatureCategory.EVENT_CONTEXT_FEATURE),
        ("calendar_validation_feature_placeholder", FeatureCategory.CALENDAR_CONTEXT_FEATURE),
        ("provider_quality_feature_placeholder", FeatureCategory.QUALITY_CONTEXT_FEATURE),
        ("lineage_completeness_feature_placeholder", FeatureCategory.LINEAGE_FEATURE)
    ]

    out = []
    for name, cat in default_groups:
        item = FeatureDefinition(
            feature_id=create_feature_definition_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            name=name,
            category=cat,
            data_type=FeatureDataType.FLOAT,
            description=f"Placeholder feature for {name}",
            input_columns=["close"],
            output_column=name,
            source_indicator_id=None,
            nullable=True,
            default_value=None,
            computation_mode=FeatureComputationMode.PLANNED,
            lineage_required=False,
            validation_rules=[],
            produces_trade_signal=False,
            produces_order_decision=False,
            enabled_for_phase116=True,
            implementation_phase=117,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        )
        out.append(item)
    return out

def feature_definition_by_name(name: str, features: list[FeatureDefinition] | None = None) -> FeatureDefinition | None:
    if features is None:
        features = build_default_feature_definitions()
    for feat in features:
        if feat.name == name:
            return feat
    return None

def validate_feature_registry(features: list[FeatureDefinition]) -> list[str]:
    errors = []
    for feat in features:
        validate_feature_definition(feat)
        if feat.errors:
            errors.extend([f"Feature {feat.name} error: {e}" for e in feat.errors])
    return errors

def feature_registry_summary(features: list[FeatureDefinition]) -> dict[str, Any]:
    return {"total": len(features)}

def feature_registry_to_text(features: list[FeatureDefinition], limit: int = 200) -> str:
    lines = [f"Total Features: {len(features)}"]
    for i, feat in enumerate(features):
        if i >= limit:
            lines.append("... [truncated]")
            break
        lines.append(f" - {feat.name} [{feat.category.value}]")
    return "\n".join(lines)
