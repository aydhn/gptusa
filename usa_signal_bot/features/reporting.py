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
