from typing import Any
from usa_signal_bot.feature_engine.factor_composition.phase120_models import (
    FeatureGroupDefinition,
    FactorComponent,
    create_factor_component_id,
    validate_factor_component,
    _now_str
)

def build_factor_components(groups: list[FeatureGroupDefinition]) -> list[FactorComponent]:
    components = []

    # Base mappings from group to component
    component_mappings = [
        ("momentum_component", "momentum", "standardized_z_score", 1.0, "positive"),
        ("trend_component", "trend", "standardized_z_score", 1.0, "positive"),
        ("volatility_component", "volatility", "inverse_standardized", 1.0, "negative"),
        ("liquidity_component", "volume_liquidity", "standardized_z_score", 1.0, "positive"),
        ("relative_strength_component", "cross_sectional", "rank_normalization", 1.0, "positive"),
        ("quality_context_component", "quality_context", "binary_flag_or_score", 1.0, "positive"),
        ("event_context_component", "event_context", "binary_flag_or_score", 1.0, "positive"),
        ("calendar_context_component", "calendar_context", "binary_flag_or_score", 1.0, "positive"),
        ("confidence_component", "confidence_freshness", "clip_0_1", 1.0, "positive"),
        ("interaction_component", "interactions", "standardized_z_score", 1.0, "positive")
    ]

    for c_name, g_name, transform, weight, direction in component_mappings:
        group = next((g for g in groups if g.group_name == g_name), None)
        columns = group.feature_columns if group else []

        comp = FactorComponent(
            component_id=create_factor_component_id(),
            created_at_utc=_now_str(),
            component_name=c_name,
            source_group_name=g_name,
            source_feature_columns=columns,
            transform=transform,
            weight_hint=weight,
            direction_hint=direction,
            produces_trade_signal=False,
            produces_order_decision=False,
            produces_portfolio_weights=False
        )
        components.append(comp)

    return components

def factor_component_by_name(name: str, components: list[FactorComponent] | None = None) -> FactorComponent | None:
    if not components: return None
    for c in components:
        if c.component_name == name:
            return c
    return None

def validate_factor_components(components: list[FactorComponent]) -> list[str]:
    errors = []
    for c in components:
        validate_factor_component(c)
        if c.errors:
            errors.extend([f"Component {c.component_name} error: {e}" for e in c.errors])
    return errors

def factor_component_registry_summary(components: list[FactorComponent]) -> dict[str, Any]:
    return {
        "component_count": len(components),
        "components": [c.component_name for c in components]
    }

def factor_component_registry_to_text(components: list[FactorComponent], limit: int = 200) -> str:
    summary = factor_component_registry_summary(components)
    lines = [f"Factor Component Registry: {summary['component_count']} components"]
    for c in components[:limit]:
        lines.append(f"  - {c.component_name} (from {c.source_group_name}) - {len(c.source_feature_columns)} source columns")
    return "\n".join(lines)
