from typing import List
from usa_signal_bot.features.composite_models import CompositeFeatureSet
from usa_signal_bot.features.feature_groups import default_feature_group_specs
from usa_signal_bot.core.exceptions import CompositeFeatureError

def _get_group(name: str):
    specs = default_feature_group_specs()
    for spec in specs:
        if spec.group_name == name:
            return spec
    raise ValueError(f"Group {name} not found in defaults")

def minimal_composite_feature_set() -> CompositeFeatureSet:
    return CompositeFeatureSet(
        name="minimal",
        description="Minimal composite set containing basic and trend features",
        groups=[_get_group("basic_features"), _get_group("trend_features")]
    )

def core_composite_feature_set() -> CompositeFeatureSet:
    return CompositeFeatureSet(
        name="core",
        description="Core composite set with trend, momentum, volatility, and volume features",
        groups=[
            _get_group("trend_features"),
            _get_group("momentum_features"),
            _get_group("volatility_features"),
            _get_group("volume_features")
        ]
    )

def technical_composite_feature_set() -> CompositeFeatureSet:
    return CompositeFeatureSet(
        name="technical",
        description="Technical set including core and price action features",
        groups=[
            _get_group("trend_features"),
            _get_group("momentum_features"),
            _get_group("volatility_features"),
            _get_group("volume_features"),
            _get_group("price_action_features")
        ]
    )

def full_composite_feature_set() -> CompositeFeatureSet:
    return CompositeFeatureSet(
        name="full",
        description="Full composite set with all feature groups",
        groups=[
            _get_group("basic_features"),
            _get_group("trend_features"),
            _get_group("momentum_features"),
            _get_group("volatility_features"),
            _get_group("volume_features"),
            _get_group("price_action_features"),
            _get_group("divergence_features")
        ]
    )

def research_composite_feature_set() -> CompositeFeatureSet:
    return CompositeFeatureSet(
        name="research",
        description="Extended research set",
        groups=[
            _get_group("basic_features"),
            _get_group("trend_features"),
            _get_group("momentum_features"),
            _get_group("volatility_features"),
            _get_group("volume_features"),
            _get_group("price_action_features"),
            _get_group("divergence_features")
        ]
    )

def list_composite_feature_sets() -> List[CompositeFeatureSet]:
    return [
        minimal_composite_feature_set(),
        core_composite_feature_set(),
        technical_composite_feature_set(),
        full_composite_feature_set(),
        research_composite_feature_set()
    ]

def get_composite_feature_set(name: str) -> CompositeFeatureSet:
    sets = list_composite_feature_sets()
    for cset in sets:
        if cset.name == name:
            return cset
    raise CompositeFeatureError(f"Composite feature set {name} not found")

def composite_feature_set_summary_text(composite: CompositeFeatureSet) -> str:
    lines = [f"Composite Feature Set: {composite.name}"]
    lines.append(f"Description: {composite.description}")
    lines.append("Groups:")
    for group in composite.groups:
        enabled_str = "Enabled" if group.enabled else "Disabled"
        lines.append(f"  - {group.group_name} ({group.group_type.value}) -> {group.indicator_set_name} [{enabled_str}]")
    return "\n".join(lines)
