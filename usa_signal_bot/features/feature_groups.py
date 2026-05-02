from typing import List
from usa_signal_bot.core.enums import FeatureGroupType
from usa_signal_bot.core.exceptions import FeatureGroupError
from usa_signal_bot.features.composite_models import FeatureGroupSpec

class FeatureGroupRegistry:
    def __init__(self):
        self._groups: dict[str, FeatureGroupSpec] = {}

    def register_group(self, spec: FeatureGroupSpec) -> None:
        if spec.group_name in self._groups:
            raise FeatureGroupError(f"Group {spec.group_name} already registered")
        self._groups[spec.group_name] = spec

    def get_group(self, name: str) -> FeatureGroupSpec:
        if name not in self._groups:
            raise FeatureGroupError(f"Group {name} not found in registry")
        return self._groups[name]

    def has_group(self, name: str) -> bool:
        return name in self._groups

    def list_groups(self) -> List[FeatureGroupSpec]:
        return list(self._groups.values())

    def list_enabled_groups(self) -> List[FeatureGroupSpec]:
        return [g for g in self._groups.values() if g.enabled]

    def list_by_type(self, group_type: FeatureGroupType) -> List[FeatureGroupSpec]:
        return [g for g in self._groups.values() if g.group_type == group_type]

    def unregister_group(self, name: str) -> None:
        if name in self._groups:
            del self._groups[name]

    def validate_all(self) -> None:
        pass


def default_feature_group_specs() -> List[FeatureGroupSpec]:
    return [
        FeatureGroupSpec(group_name="basic_features", group_type=FeatureGroupType.BASIC, indicator_set_name="default_basic"),
        FeatureGroupSpec(group_name="trend_features", group_type=FeatureGroupType.TREND, indicator_set_name="basic_trend"),
        FeatureGroupSpec(group_name="momentum_features", group_type=FeatureGroupType.MOMENTUM, indicator_set_name="basic_momentum"),
        FeatureGroupSpec(group_name="volatility_features", group_type=FeatureGroupType.VOLATILITY, indicator_set_name="basic_volatility"),
        FeatureGroupSpec(group_name="volume_features", group_type=FeatureGroupType.VOLUME, indicator_set_name="basic_volume"),
        FeatureGroupSpec(group_name="price_action_features", group_type=FeatureGroupType.PRICE_ACTION, indicator_set_name="basic_price_action"),
        FeatureGroupSpec(group_name="divergence_features", group_type=FeatureGroupType.DIVERGENCE, indicator_set_name="basic_divergence"),
    ]

def create_default_feature_group_registry() -> FeatureGroupRegistry:
    registry = FeatureGroupRegistry()
    for spec in default_feature_group_specs():
        registry.register_group(spec)
    return registry

def validate_feature_group_spec(spec: FeatureGroupSpec) -> None:
    if not spec.group_name:
        raise FeatureGroupError("Spec group_name cannot be empty")
