from typing import Any, Dict, List
import pandas as pd
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftObservation,
    ContextDegradationDiagnostic,
    RegimeMonitoringContext
)

def validate_monitoring_baseline_schema(item: RegimeMonitoringBaseline) -> List[str]:
    errors = []
    if not item.baseline_id: errors.append("Missing baseline_id")
    if not item.baseline_version: errors.append("Missing baseline_version")
    return errors

def validate_monitoring_snapshot_schema(item: RegimeMonitoringSnapshot) -> List[str]:
    errors = []
    if not item.snapshot_id: errors.append("Missing snapshot_id")
    return errors

def validate_drift_observation_schema(item: RegimeDriftObservation) -> List[str]:
    errors = []
    if not item.metric_name: errors.append("Missing metric_name")
    return errors

def validate_degradation_diagnostic_schema(item: ContextDegradationDiagnostic) -> List[str]:
    errors = []
    if not item.recommended_action_type: errors.append("Missing recommended_action_type")
    return errors

def validate_monitoring_context_schema(context: RegimeMonitoringContext) -> List[str]:
    errors = []
    if not context.context_id: errors.append("Missing context_id")
    return errors

def validate_monitoring_column_names(columns: List[str]) -> List[str]:
    return validate_no_forbidden_monitoring_columns(columns)

def validate_no_forbidden_monitoring_columns(columns: List[str]) -> List[str]:
    forbidden = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper", "live",
        "demo_order", "live_order", "sent_to_broker", "deploy", "production_patch"
    ]
    errors = []
    for col in columns:
        col_lower = col.lower()
        if "signal" in col_lower and "macd_signal_9" not in col_lower:
            errors.append(f"Forbidden column 'signal' found in {col}")
            continue
        for f in forbidden:
            if f in col_lower:
                errors.append(f"Forbidden column fragment '{f}' found in {col}")
    return errors

def monitoring_schema_summary(errors: List[str]) -> Dict[str, Any]:
    return {"error_count": len(errors)}

def monitoring_schema_to_text(errors: List[str]) -> str:
    return f"Schema Errors: {len(errors)}"
