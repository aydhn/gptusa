import pandas as pd
import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from usa_signal_bot.ml_research.ensemble_evaluation.phase143_models import (
    EnsemblePrototypeSpec,
    OfflineEnsemblePredictionArtifact,
    create_offline_ensemble_prediction_artifact_id,
    OfflineEnsemblePredictionKind,
    EnsemblePrototypeRiskFlag
)

def generate_offline_ensemble_predictions(specs: List[EnsemblePrototypeSpec], prediction_df: pd.DataFrame) -> List[OfflineEnsemblePredictionArtifact]:
    artifacts = []
    for spec in specs:
        if prediction_df.empty:
            continue
        df, art = generate_prediction_frame_for_ensemble(spec, prediction_df)
        artifacts.append(art)
    return artifacts

def generate_prediction_frame_for_ensemble(spec: EnsemblePrototypeSpec, prediction_df: pd.DataFrame) -> Tuple[pd.DataFrame, OfflineEnsemblePredictionArtifact]:

    out_df = prediction_df.copy()

    # Just a mock blend logic: taking average of candidate score columns if they exist
    # Real logic would use coefficient_by_candidate_ref_id
    score_cols = [c for c in out_df.columns if 'score' in c]
    if score_cols:
        out_df['research_ensemble_prediction_score'] = out_df[score_cols].mean(axis=1)
    else:
        out_df['research_ensemble_prediction_score'] = 0.5

    out_df['ensemble_prototype_id'] = spec.prototype_id

    art = OfflineEnsemblePredictionArtifact(
        prediction_id=create_offline_ensemble_prediction_artifact_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
        prototype_id=spec.prototype_id,
        candidate_group_id=spec.candidate_group_id,
        blend_plan_id=spec.blend_plan_id,
        prediction_kind=OfflineEnsemblePredictionKind.RESEARCH_ENSEMBLE_SCORE,
        split_name="test",
        row_count=len(out_df),
        output_path=None,
        output_hash=None,
        output_columns=list(out_df.columns),
        required_columns=["symbol", "timestamp"],
        forbidden_columns_detected=[],
        offline_evaluation_only=True,
        live_inference_output=False,
        online_inference_output=False,
        threshold_optimization_output=False,
        research_data_only=True,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    return out_df, art

def blend_numeric_prediction_values(df: pd.DataFrame, coefficient_by_candidate_ref_id: Dict[str, float], value_column: str) -> pd.Series:
    # mock
    return pd.Series([0.0]*len(df), index=df.index)

def blend_class_labels_by_weighted_vote(df: pd.DataFrame, coefficient_by_candidate_ref_id: Dict[str, float], label_column: str) -> pd.Series:
    # mock
    return pd.Series([0]*len(df), index=df.index)

def validate_offline_ensemble_prediction_frame(df: pd.DataFrame) -> List[str]:
    errors = []
    forbidden = ["buy", "sell", "order", "portfolio", "allocation"]
    for c in df.columns:
        for f in forbidden:
            if f in c.lower():
                errors.append(f"Forbidden col: {c}")
    return errors

def validate_offline_ensemble_prediction_artifacts(items: List[OfflineEnsemblePredictionArtifact]) -> List[str]:
    errors = []
    for item in items:
        if not item.offline_evaluation_only:
            errors.append("Artifact not marked offline only")
    return errors

def write_offline_ensemble_predictions_csv(path: Path, df: pd.DataFrame, overwrite: bool = False) -> Path:
    if not overwrite and path.exists():
        raise FileExistsError(f"Path {path} exists")
    df.to_csv(path, index=False)
    return path

def offline_ensemble_prediction_summary(items: List[OfflineEnsemblePredictionArtifact]) -> Dict[str, Any]:
    return {"prediction_count": len(items)}

def offline_ensemble_prediction_to_text(items: List[OfflineEnsemblePredictionArtifact], limit: int = 300) -> str:
    return str(offline_ensemble_prediction_summary(items))
