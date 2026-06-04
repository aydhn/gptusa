import datetime
import pandas as pd
from typing import Any

from usa_signal_bot.backtesting.stress_robustness.phase151_models import (
    StressInputReference,
    create_stress_input_reference_id
)
from usa_signal_bot.core.enums import StressInputKind, StressRobustnessRiskFlag

FORBIDDEN_COLUMNS = [
    "broker_order", "paper_order", "live_order", "sent_to_broker",
    "strategy_active", "deployment_enabled", "portfolio_weight",
    "target_weight", "allocation", "real_order", "live_signal",
    "recommended_weight", "production_patch"
]

def build_stress_input_references(payloads: dict[str, Any], dataframes: dict[str, pd.DataFrame] | None = None) -> list[StressInputReference]:
    refs = []

    if dataframes:
        for name, df in dataframes.items():
            refs.append(_resolve_dataframe_input(name, df))

    for name, payload in payloads.items():
        refs.append(_resolve_payload_input(name, payload))

    return refs

def detect_forbidden_stress_columns(columns: list[str]) -> list[str]:
    detected = []
    for col in columns:
        if col.lower() in FORBIDDEN_COLUMNS:
            detected.append(col)
    return detected

def _resolve_dataframe_input(name: str, df: pd.DataFrame) -> StressInputReference:
    cols = list(df.columns)
    forbidden = detect_forbidden_stress_columns(cols)

    kind = StressInputKind.UNKNOWN
    if "return" in name.lower() or "returns" in name.lower():
        kind = StressInputKind.STRATEGY_RETURN_SERIES
    elif "equity" in name.lower():
        kind = StressInputKind.STRATEGY_EQUITY_CURVE
    elif "fold" in name.lower():
        kind = StressInputKind.FOLD_REPLAY_RESULTS

    errors = []
    risk_flags = []
    if forbidden:
        errors.append(f"Forbidden columns detected: {forbidden}")
        risk_flags.append(StressRobustnessRiskFlag.FORBIDDEN_STRESS_COLUMN)

    valid = len(forbidden) == 0

    return StressInputReference(
        input_ref_id=create_stress_input_reference_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        input_kind=kind,
        source_artifact_name=name,
        source_path=None,
        source_hash=None,
        available=True,
        read_only=True,
        row_count=len(df),
        columns=cols,
        forbidden_columns_detected=forbidden,
        research_data_only=valid,
        offline_backtest_research_only=valid,
        warnings=[],
        errors=errors,
        risk_flags=risk_flags,
        metadata={"shape": df.shape}
    )

def _resolve_payload_input(name: str, payload: dict[str, Any]) -> StressInputReference:
    kind = StressInputKind.UNKNOWN
    if "validation_report" in name.lower():
        kind = StressInputKind.WALK_FORWARD_VALIDATION_REPORT
    elif "temporal_stability" in name.lower():
        kind = StressInputKind.TEMPORAL_STABILITY_AUDIT
    elif "oos_robustness" in name.lower():
        kind = StressInputKind.OOS_ROBUSTNESS_METRICS
    elif "robustness_summary" in name.lower():
        kind = StressInputKind.ROBUSTNESS_SUMMARY
    elif "safety_boundary" in name.lower():
        kind = StressInputKind.SAFETY_BOUNDARY
    elif "readiness_gate" in name.lower():
        kind = StressInputKind.PHASE151_READINESS_GATE

    return StressInputReference(
        input_ref_id=create_stress_input_reference_id(),
        created_at_utc=datetime.datetime.now(datetime.UTC).isoformat(),
        input_kind=kind,
        source_artifact_name=name,
        source_path=None,
        source_hash=None,
        available=True,
        read_only=True,
        row_count=None,
        columns=[],
        forbidden_columns_detected=[],
        research_data_only=True,
        offline_backtest_research_only=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={"keys": list(payload.keys())}
    )

def validate_strategy_return_series_frame(df: pd.DataFrame) -> list[str]:
    errors = []
    if "return" not in df.columns and "returns" not in df.columns and "strategy_return" not in df.columns:
        errors.append("Missing return column")
    if detect_forbidden_stress_columns(list(df.columns)):
        errors.append("Forbidden columns found")
    return errors

def validate_strategy_equity_curve_frame(df: pd.DataFrame) -> list[str]:
    errors = []
    if "equity" not in df.columns and "balance" not in df.columns:
        errors.append("Missing equity column")
    if detect_forbidden_stress_columns(list(df.columns)):
        errors.append("Forbidden columns found")
    return errors

def validate_fold_replay_results_frame(df: pd.DataFrame) -> list[str]:
    errors = []
    if "fold_id" not in df.columns:
        errors.append("Missing fold_id column")
    if detect_forbidden_stress_columns(list(df.columns)):
        errors.append("Forbidden columns found")
    return errors
