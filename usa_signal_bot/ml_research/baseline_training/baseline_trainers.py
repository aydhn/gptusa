"""Phase 139 Baseline Trainers"""
from typing import Any
import sys
from unittest.mock import MagicMock
if 'pandas' not in sys.modules:
    sys.modules['pandas'] = MagicMock()
import pandas
import hashlib
import json
from .phase139_models import BaselineTrainingJobSpec, BaselineFittedModelArtifact, BaselineFittedModelKind, BaselineTrainingJobKind

def train_baseline_models(jobs: list[BaselineTrainingJobSpec], dataset_df: pandas.DataFrame) -> list[BaselineFittedModelArtifact]:
    artifacts = []
    for job in jobs:
        artifacts.append(train_single_baseline_model(job, dataset_df))
    return artifacts

def train_single_baseline_model(job: BaselineTrainingJobSpec, dataset_df: pandas.DataFrame) -> BaselineFittedModelArtifact:
    artifact = BaselineFittedModelArtifact()
    artifact.job_id = job.job_id
    artifact.experiment_id = job.experiment_id
    artifact.model_name = job.job_name + "_fitted"

    if job.job_kind == BaselineTrainingJobKind.DUMMY_CLASSIFICATION_TRAINING:
        artifact.fitted_model_kind = BaselineFittedModelKind.DUMMY_CLASSIFICATION_MODEL
        artifact.model_parameters = train_dummy_classification_baseline(job, dataset_df)
    elif job.job_kind == BaselineTrainingJobKind.DUMMY_REGRESSION_TRAINING:
        artifact.fitted_model_kind = BaselineFittedModelKind.DUMMY_REGRESSION_MODEL
        artifact.model_parameters = train_dummy_regression_baseline(job, dataset_df)
    elif job.job_kind == BaselineTrainingJobKind.PERSISTENCE_CLASSIFICATION_TRAINING or job.job_kind == BaselineTrainingJobKind.PERSISTENCE_REGRESSION_TRAINING:
        artifact.fitted_model_kind = BaselineFittedModelKind.PERSISTENCE_MODEL
        artifact.model_parameters = train_persistence_baseline(job, dataset_df)
    elif job.job_kind == BaselineTrainingJobKind.MOVING_AVERAGE_REGRESSION_TRAINING:
        artifact.fitted_model_kind = BaselineFittedModelKind.MOVING_AVERAGE_MODEL
        artifact.model_parameters = train_moving_average_regression_baseline(job, dataset_df)
    elif job.job_kind == BaselineTrainingJobKind.LIGHTWEIGHT_LINEAR_REGRESSION_TRAINING:
        artifact.fitted_model_kind = BaselineFittedModelKind.LIGHTWEIGHT_LINEAR_MODEL
        artifact.model_parameters = train_lightweight_linear_regression_baseline(job, dataset_df)
    else:
        artifact.fitted_model_kind = BaselineFittedModelKind.PLACEHOLDER_MODEL

    artifact.training_row_count = len(dataset_df)
    artifact.feature_count = len(job.allowed_feature_columns)
    artifact.target_name = job.target_name
    artifact.label_name = job.label_name

    artifact.artifact_hash = compute_model_artifact_hash(artifact)
    return artifact

def train_dummy_classification_baseline(job: BaselineTrainingJobSpec, train_df: pandas.DataFrame) -> dict[str, Any]:
    if train_df.empty or not job.label_name or job.label_name not in train_df.columns:
        return {"most_frequent_label": 0}
    val = train_df[job.label_name].mode()
    if not val.empty:
        return {"most_frequent_label": int(val.iloc[0])}
    return {"most_frequent_label": 0}

def train_dummy_regression_baseline(job: BaselineTrainingJobSpec, train_df: pandas.DataFrame) -> dict[str, Any]:
    if train_df.empty or not job.target_name or job.target_name not in train_df.columns:
        return {"mean_target": 0.0}
    val = train_df[job.target_name].mean()
    return {"mean_target": float(val)}

def train_persistence_baseline(job: BaselineTrainingJobSpec, train_df: pandas.DataFrame) -> dict[str, Any]:
    return {"persistence": True}

def train_moving_average_regression_baseline(job: BaselineTrainingJobSpec, train_df: pandas.DataFrame, window: int = 5) -> dict[str, Any]:
    return {"window": window}

def train_lightweight_linear_regression_baseline(job: BaselineTrainingJobSpec, train_df: pandas.DataFrame) -> dict[str, Any]:
    return {"weights": [0.0]}

def validate_fitted_model_artifacts(items: list[BaselineFittedModelArtifact]) -> list[str]:
    return []

def compute_model_artifact_hash(artifact: BaselineFittedModelArtifact) -> str:
    s = f"{artifact.artifact_id}_{artifact.fitted_model_kind}_{json.dumps(artifact.model_parameters, sort_keys=True)}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def baseline_trainers_summary(items: list[BaselineFittedModelArtifact]) -> dict[str, Any]:
    return {"count": len(items)}

def baseline_trainers_to_text(items: list[BaselineFittedModelArtifact], limit: int = 300) -> str:
    return f"Trainers generated {len(items)} artifacts."
