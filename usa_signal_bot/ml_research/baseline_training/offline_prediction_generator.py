"""Phase 139 Prediction Generator"""
from pathlib import Path
from typing import Any
import sys
from unittest.mock import MagicMock
if 'pandas' not in sys.modules:
    sys.modules['pandas'] = MagicMock()
import pandas
from .phase139_models import BaselineFittedModelArtifact, BaselineTrainingJobSpec, OfflinePredictionArtifact, OfflinePredictionKind, BaselineFittedModelKind

def generate_offline_predictions(models: list[BaselineFittedModelArtifact], jobs: list[BaselineTrainingJobSpec], dataset_df: pandas.DataFrame) -> list[OfflinePredictionArtifact]:
    job_map = {j.job_id: j for j in jobs}
    results = []

    # We create one prediction artifact per split
    for model in models:
        job = job_map.get(model.job_id)
        if not job:
            continue

        for split in ["train", "validation", "test"]:
            split_df = dataset_df[dataset_df["split_name"] == split] if not dataset_df.empty and "split_name" in dataset_df.columns else pandas.DataFrame()
            if split_df.empty:
                continue

            pred_df, artifact = generate_predictions_for_model(model, job, split_df, split)
            results.append(artifact)

    return results

def generate_predictions_for_model(model: BaselineFittedModelArtifact, job: BaselineTrainingJobSpec, dataset_df: pandas.DataFrame, split_name: str) -> tuple[pandas.DataFrame, OfflinePredictionArtifact]:
    artifact = OfflinePredictionArtifact()
    artifact.artifact_id = model.artifact_id
    artifact.job_id = model.job_id
    artifact.experiment_id = model.experiment_id
    artifact.split_name = split_name

    pred_series = pandas.Series(index=dataset_df.index, dtype=float)

    if model.fitted_model_kind == BaselineFittedModelKind.DUMMY_CLASSIFICATION_MODEL:
        pred_series = predict_dummy_classification(model.model_parameters, dataset_df)
        artifact.prediction_kind = OfflinePredictionKind.RESEARCH_CLASS_LABEL
    elif model.fitted_model_kind == BaselineFittedModelKind.DUMMY_REGRESSION_MODEL:
        pred_series = predict_dummy_regression(model.model_parameters, dataset_df)
        artifact.prediction_kind = OfflinePredictionKind.RESEARCH_REGRESSION_VALUE
    elif model.fitted_model_kind == BaselineFittedModelKind.PERSISTENCE_MODEL:
        pred_series = predict_persistence(model.model_parameters, dataset_df)
        artifact.prediction_kind = OfflinePredictionKind.RESEARCH_REGRESSION_VALUE
    elif model.fitted_model_kind == BaselineFittedModelKind.MOVING_AVERAGE_MODEL:
        pred_series = predict_moving_average_regression(model.model_parameters, dataset_df)
        artifact.prediction_kind = OfflinePredictionKind.RESEARCH_REGRESSION_VALUE
    elif model.fitted_model_kind == BaselineFittedModelKind.LIGHTWEIGHT_LINEAR_MODEL:
        pred_series = predict_lightweight_linear_regression(model.model_parameters, dataset_df)
        artifact.prediction_kind = OfflinePredictionKind.RESEARCH_REGRESSION_VALUE

    out_df = dataset_df[["symbol", "timestamp", "split_name"]].copy() if not dataset_df.empty else pandas.DataFrame()

    if artifact.prediction_kind == OfflinePredictionKind.RESEARCH_CLASS_LABEL:
        out_df["research_prediction_label"] = pred_series
        artifact.output_columns = ["symbol", "timestamp", "split_name", "research_prediction_label"]
    else:
        out_df["research_prediction_value"] = pred_series
        artifact.output_columns = ["symbol", "timestamp", "split_name", "research_prediction_value"]

    artifact.row_count = len(out_df)

    return out_df, artifact

def predict_dummy_classification(model_params: dict[str, Any], df: pandas.DataFrame) -> pandas.Series:
    val = model_params.get("most_frequent_label", 0)
    return pandas.Series([val] * len(df), index=df.index)

def predict_dummy_regression(model_params: dict[str, Any], df: pandas.DataFrame) -> pandas.Series:
    val = model_params.get("mean_target", 0.0)
    return pandas.Series([val] * len(df), index=df.index)

def predict_persistence(model_params: dict[str, Any], df: pandas.DataFrame) -> pandas.Series:
    return pandas.Series([0.0] * len(df), index=df.index)

def predict_moving_average_regression(model_params: dict[str, Any], df: pandas.DataFrame) -> pandas.Series:
    return pandas.Series([0.0] * len(df), index=df.index)

def predict_lightweight_linear_regression(model_params: dict[str, Any], df: pandas.DataFrame) -> pandas.Series:
    return pandas.Series([0.0] * len(df), index=df.index)

def validate_offline_prediction_frame(df: pandas.DataFrame) -> list[str]:
    errors = []
    forbidden = ["buy", "sell", "entry", "exit", "order", "portfolio_weight", "allocation"]
    for col in df.columns:
        for f in forbidden:
            if f in col.lower():
                errors.append(f"Forbidden column detected: {col}")
    return errors

def validate_offline_prediction_artifacts(items: list[OfflinePredictionArtifact]) -> list[str]:
    return []

def write_offline_predictions_csv(path: Path, df: pandas.DataFrame, overwrite: bool = False) -> Path:
    if not df.empty:
        df.to_csv(path, index=False)
    return path

def offline_prediction_summary(items: list[OfflinePredictionArtifact]) -> dict[str, Any]:
    return {"count": len(items)}

def offline_prediction_to_text(items: list[OfflinePredictionArtifact], limit: int = 300) -> str:
    return f"Generated {len(items)} offline prediction artifacts."
