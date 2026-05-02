from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from usa_signal_bot.core.enums import FeatureGroupType, FeatureComputationStatus, FeaturePipelineStatus

@dataclass
class FeatureGroupSpec:
    group_name: str
    group_type: FeatureGroupType
    indicator_set_name: str
    enabled: bool = True
    priority: int = 100
    params_override: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    description: Optional[str] = None

    def __post_init__(self):
        if not self.group_name:
            raise ValueError("group_name cannot be empty")
        if not isinstance(self.group_type, FeatureGroupType):
            raise ValueError(f"group_type must be a valid FeatureGroupType, got {self.group_type}")
        if not self.indicator_set_name:
            raise ValueError("indicator_set_name cannot be empty")
        if self.priority < 0:
            raise ValueError("priority cannot be negative")

@dataclass
class CompositeFeatureSet:
    name: str
    description: str
    groups: List[FeatureGroupSpec]
    created_at_utc: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.name:
            raise ValueError("name cannot be empty")
        if not self.groups:
            raise ValueError("groups cannot be empty")
        enabled_groups = [g for g in self.groups if g.enabled]
        if not enabled_groups:
            raise ValueError("At least one enabled group is required")

@dataclass
class FeatureGroupResult:
    group_name: str
    group_type: FeatureGroupType
    status: FeatureComputationStatus
    produced_features: List[str]
    row_count: int
    symbols_processed: List[str]
    timeframes_processed: List[str]
    storage_paths: List[str]
    warnings: List[str]
    errors: List[str]

@dataclass
class CompositeFeatureResult:
    composite_set_name: str
    status: FeaturePipelineStatus
    group_results: List[FeatureGroupResult]
    total_rows: int
    total_features: int
    produced_features: List[str]
    symbols_processed: List[str]
    timeframes_processed: List[str]
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]
    created_at_utc: str

    def successful_groups(self) -> List[str]:
        return [r.group_name for r in self.group_results if r.status == FeatureComputationStatus.COMPLETED]

    def failed_groups(self) -> List[str]:
        return [r.group_name for r in self.group_results if r.status == FeatureComputationStatus.FAILED]

    def is_successful(self) -> bool:
        return self.status == FeaturePipelineStatus.COMPLETED

    def is_partial(self) -> bool:
        return self.status == FeaturePipelineStatus.PARTIAL_SUCCESS


@dataclass
class CompositeFeatureMetadata:
    metadata_id: str
    composite_set_name: str
    provider_name: str
    universe_name: Optional[str]
    symbols: List[str]
    timeframes: List[str]
    feature_groups: List[str]
    produced_features: List[str]
    total_rows: int
    total_features: int
    created_at_utc: str
    storage_paths: List[str]
    validation_report_paths: List[str]
    manifest_path: Optional[str] = None


def feature_group_spec_to_dict(spec: FeatureGroupSpec) -> dict:
    return {
        "group_name": spec.group_name,
        "group_type": spec.group_type.value,
        "indicator_set_name": spec.indicator_set_name,
        "enabled": spec.enabled,
        "priority": spec.priority,
        "params_override": spec.params_override,
        "description": spec.description
    }

def composite_feature_set_to_dict(composite: CompositeFeatureSet) -> dict:
    return {
        "name": composite.name,
        "description": composite.description,
        "groups": [feature_group_spec_to_dict(g) for g in composite.groups],
        "created_at_utc": composite.created_at_utc,
        "metadata": composite.metadata
    }

def feature_group_result_to_dict(result: FeatureGroupResult) -> dict:
    return {
        "group_name": result.group_name,
        "group_type": result.group_type.value,
        "status": result.status.value,
        "produced_features": result.produced_features,
        "row_count": result.row_count,
        "symbols_processed": result.symbols_processed,
        "timeframes_processed": result.timeframes_processed,
        "storage_paths": result.storage_paths,
        "warnings": result.warnings,
        "errors": result.errors
    }


def composite_feature_result_to_dict(result: CompositeFeatureResult) -> dict:
    return {
        "composite_set_name": result.composite_set_name,
        "status": result.status.value,
        "group_results": [feature_group_result_to_dict(r) for r in result.group_results],
        "total_rows": result.total_rows,
        "total_features": result.total_features,
        "produced_features": result.produced_features,
        "symbols_processed": result.symbols_processed,
        "timeframes_processed": result.timeframes_processed,
        "output_paths": result.output_paths,
        "warnings": result.warnings,
        "errors": result.errors,
        "created_at_utc": result.created_at_utc
    }

def composite_feature_metadata_to_dict(metadata: CompositeFeatureMetadata) -> dict:
    return {
        "metadata_id": metadata.metadata_id,
        "composite_set_name": metadata.composite_set_name,
        "provider_name": metadata.provider_name,
        "universe_name": metadata.universe_name,
        "symbols": metadata.symbols,
        "timeframes": metadata.timeframes,
        "feature_groups": metadata.feature_groups,
        "produced_features": metadata.produced_features,
        "total_rows": metadata.total_rows,
        "total_features": metadata.total_features,
        "created_at_utc": metadata.created_at_utc,
        "storage_paths": metadata.storage_paths,
        "validation_report_paths": metadata.validation_report_paths,
        "manifest_path": metadata.manifest_path
    }
