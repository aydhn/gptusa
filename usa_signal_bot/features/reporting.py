import json
from pathlib import Path
from typing import Optional

from usa_signal_bot.features.output_contract import FeatureComputationResult, FeatureOutputMetadata
from usa_signal_bot.features.validation import FeatureValidationReport, feature_validation_report_to_text
from usa_signal_bot.utils.file_utils import atomic_write_text

def feature_computation_result_to_text(result: FeatureComputationResult) -> str:
    lines = [
        "--- Feature Computation Result ---",
        f"Status: {result.status.value}",
        f"Time (UTC): {result.created_at_utc}",
        f"Provider: {result.request.provider_name}",
        f"Symbols processed: {len(result.symbols_processed)}",
        f"Timeframes processed: {len(result.timeframes_processed)}",
        f"Produced features: {len(result.produced_features)}",
        f"Generated rows: {result.row_count()}"
    ]

    if result.errors:
        lines.append("\nErrors:")
        for e in result.errors:
            lines.append(f"  - {e}")

    if result.warnings:
        lines.append("\nWarnings:")
        for w in result.warnings:
            lines.append(f"  - {w}")

    return "\n".join(lines)

def feature_output_metadata_to_text(metadata: FeatureOutputMetadata) -> str:
    lines = [
        "--- Feature Output Metadata ---",
        f"Output ID: {metadata.output_id}",
        f"Provider: {metadata.provider_name}",
        f"Universe: {metadata.universe_name or 'N/A'}",
        f"Rows: {metadata.row_count}",
        f"Created (UTC): {metadata.created_at_utc}",
        "Storage Paths:"
    ]
    for p in metadata.storage_paths:
        lines.append(f"  - {p}")

    return "\n".join(lines)

def write_feature_report_json(path: Path, result: FeatureComputationResult, validation_report: Optional[FeatureValidationReport] = None, metadata: Optional[FeatureOutputMetadata] = None) -> Path:
    import dataclasses

    data = {
        "computation": dataclasses.asdict(result),
        "validation": dataclasses.asdict(validation_report) if validation_report else None,
        "metadata": dataclasses.asdict(metadata) if metadata else None
    }

    if "computation" in data and "feature_rows" in data["computation"]:
        data["computation"]["feature_rows"] = f"<{len(result.feature_rows)} rows omitted>"

    atomic_write_text(path, json.dumps(data, indent=2))
    return path

def momentum_indicator_set_to_text(indicator_set) -> str:
    return f"Momentum Indicator Set: {indicator_set.name}"
def momentum_feature_summary_to_text(result: FeatureComputationResult) -> str:
    return feature_computation_result_to_text(result)
def write_momentum_feature_report_json(path: Path, result: FeatureComputationResult, indicator_set = None) -> Path:
    import dataclasses
    data = {"computation": dataclasses.asdict(result)}
    atomic_write_text(path, json.dumps(data, indent=2))
    return path


def volatility_indicator_set_to_text(indicator_set) -> str:
    return f"Volatility Indicator Set: {indicator_set.name}"

def volatility_feature_summary_to_text(result: FeatureComputationResult) -> str:
    return feature_computation_result_to_text(result)

def write_volatility_feature_report_json(path: Path, result: FeatureComputationResult, indicator_set = None) -> Path:
    import dataclasses
    data = {"computation": dataclasses.asdict(result)}
    if indicator_set:
        from usa_signal_bot.features.volatility_sets import volatility_indicator_set_to_dict
        data["indicator_set"] = volatility_indicator_set_to_dict(indicator_set)
    atomic_write_text(path, json.dumps(data, indent=2))
    return path

from usa_signal_bot.features.composite_models import (
    CompositeFeatureResult, CompositeFeatureMetadata, FeatureGroupResult
)
from usa_signal_bot.features.feature_pipeline import FeaturePipelineResult
import json

def feature_group_result_to_text(result: FeatureGroupResult) -> str:
    lines = [f"Group: {result.group_name} ({result.group_type.value}) - {result.status.value}"]
    lines.append(f"  Rows: {result.row_count}, Features: {len(result.produced_features)}")
    if result.storage_paths:
        lines.append(f"  Storage: {', '.join(result.storage_paths)}")
    if result.warnings:
        lines.append(f"  Warnings: {len(result.warnings)}")
    if result.errors:
        lines.append(f"  Errors: {len(result.errors)}")
    return "\n".join(lines)

def composite_feature_result_to_text(result: CompositeFeatureResult) -> str:
    lines = [f"--- Composite Feature Result: {result.composite_set_name} ---"]
    lines.append(f"Status: {result.status.value}")
    lines.append(f"Created At: {result.created_at_utc}")
    lines.append(f"Total Rows: {result.total_rows}")
    lines.append(f"Total Features: {result.total_features}")
    lines.append(f"Symbols Processed: {len(result.symbols_processed)}")
    lines.append(f"Timeframes Processed: {len(result.timeframes_processed)}")
    lines.append("")
    lines.append("Group Results:")
    for gr in result.group_results:
        lines.append(feature_group_result_to_text(gr))

    if result.warnings:
        lines.append("")
        lines.append("Warnings:")
        for w in result.warnings:
            lines.append(f"  - {w}")

    if result.errors:
        lines.append("")
        lines.append("Errors:")
        for e in result.errors:
            lines.append(f"  - {e}")

    return "\n".join(lines)

def composite_feature_metadata_to_text(metadata: CompositeFeatureMetadata) -> str:
    lines = [f"--- Composite Feature Metadata: {metadata.composite_set_name} ---"]
    lines.append(f"ID: {metadata.metadata_id}")
    lines.append(f"Provider: {metadata.provider_name}")
    if metadata.universe_name:
        lines.append(f"Universe: {metadata.universe_name}")
    lines.append(f"Symbols: {len(metadata.symbols)}")
    lines.append(f"Timeframes: {', '.join(metadata.timeframes)}")
    lines.append(f"Feature Groups: {', '.join(metadata.feature_groups)}")
    lines.append(f"Produced Features: {metadata.total_features}")
    lines.append(f"Created At: {metadata.created_at_utc}")
    return "\n".join(lines)

def feature_pipeline_result_to_text(result: FeaturePipelineResult) -> str:
    lines = ["--- Feature Pipeline Result ---"]
    lines.append(f"Status: {result.status.value}")
    lines.append(f"Requested Symbols: {len(result.request.symbols) if result.request.symbols else 'Auto'}")
    lines.append(f"Used Eligible Symbols: {len(result.eligible_symbols_used)}")
    if result.missing_cache_symbols:
        lines.append(f"Missing Cache Data: {len(result.missing_cache_symbols)} symbols")

    lines.append("")
    lines.append(composite_feature_result_to_text(result.composite_result))

    return "\n".join(lines)

def write_composite_feature_report_json(path: Path, result: CompositeFeatureResult, metadata: CompositeFeatureMetadata | None = None) -> Path:
    from usa_signal_bot.features.composite_models import composite_feature_result_to_dict, composite_feature_metadata_to_dict

    data = {
        "result": composite_feature_result_to_dict(result)
    }
    if metadata:
        data["metadata"] = composite_feature_metadata_to_dict(metadata)

    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

    return path
