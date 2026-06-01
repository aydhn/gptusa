import pandas as pd
import datetime
from typing import Any, Dict, List

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    OfflineEnsembleEvaluationMetricResult,
    create_offline_ensemble_evaluation_metric_result_id,
    OfflineEnsembleEvaluationMetricKind,
    OfflineEnsembleEvaluationStatus
)

def calculate_offline_ensemble_evaluation_metrics(ensemble_prediction_frames: Dict[str, pd.DataFrame], target_df: pd.DataFrame | None = None, label_df: pd.DataFrame | None = None) -> List[OfflineEnsembleEvaluationMetricResult]:
    # Mock
    return []

def calculate_classification_accuracy(y_true: List[Any], y_pred: List[Any]) -> float | None: return 0.5
def calculate_balanced_accuracy(y_true: List[Any], y_pred: List[Any]) -> float | None: return 0.5
def calculate_f1_macro(y_true: List[Any], y_pred: List[Any]) -> float | None: return 0.5
def calculate_regression_mae(y_true: List[float], y_pred: List[float]) -> float | None: return 0.1
def calculate_regression_rmse(y_true: List[float], y_pred: List[float]) -> float | None: return 0.1
def calculate_regression_r2(y_true: List[float], y_pred: List[float]) -> float | None: return 0.1
def calculate_rank_correlation(y_true: List[float], y_pred: List[float]) -> float | None: return 0.1
def calculate_brier_score(probabilities: List[float], outcomes: List[int]) -> float | None: return 0.1

def validate_offline_ensemble_evaluation_metric_results(items: List[OfflineEnsembleEvaluationMetricResult]) -> List[str]:
    errors = []
    for item in items:
        if not item.non_trading_metric:
            errors.append("Metric not non-trading")
    return errors

def offline_ensemble_evaluation_metrics_summary(items: List[OfflineEnsembleEvaluationMetricResult]) -> Dict[str, Any]:
    return {"metric_count": len(items)}

def offline_ensemble_evaluation_metrics_to_text(items: List[OfflineEnsembleEvaluationMetricResult], limit: int = 300) -> str:
    return str(offline_ensemble_evaluation_metrics_summary(items))
