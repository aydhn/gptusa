import hashlib
import json
from typing import List, Dict, Any
from usa_signal_bot.core.enums import PredictionOutputBoundaryKind, BaselineMLScaffoldingQuality
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    PredictionOutputBoundary,
    create_prediction_output_boundary_id,
    _now_utc
)

def allowed_prediction_output_kinds() -> List[PredictionOutputBoundaryKind]:
    return [
        PredictionOutputBoundaryKind.RESEARCH_SCORE_ONLY,
        PredictionOutputBoundaryKind.RESEARCH_PROBABILITY_ONLY,
        PredictionOutputBoundaryKind.RESEARCH_CLASS_LABEL_ONLY,
        PredictionOutputBoundaryKind.RESEARCH_REGRESSION_VALUE_ONLY,
        PredictionOutputBoundaryKind.DIAGNOSTIC_METADATA_ONLY
    ]

def forbidden_prediction_output_fields() -> List[str]:
    return [
        "buy_signal", "sell_signal", "entry", "exit", "order", "broker_order",
        "paper_order", "live_order", "position", "portfolio_weight",
        "target_weight", "allocation", "sent_to_broker", "strategy_active",
        "deployment_enabled", "production_patch"
    ]

def required_research_output_fields() -> List[str]:
    return ["prediction_id", "timestamp_utc"]

def optional_research_output_fields() -> List[str]:
    return ["score", "probability", "class_label", "regression_value", "diagnostic_metadata"]

def build_prediction_output_boundary() -> PredictionOutputBoundary:
    b = PredictionOutputBoundary(
        boundary_id=create_prediction_output_boundary_id(),
        created_at_utc=_now_utc(),
        allowed_output_kinds=allowed_prediction_output_kinds(),
        forbidden_output_fields=forbidden_prediction_output_fields(),
        required_output_fields=required_research_output_fields(),
        optional_output_fields=optional_research_output_fields(),
        forbidden_semantics=["trade signal", "buy/sell", "order decision", "broker execution", "paper mutation", "portfolio allocation", "strategy activation", "deployment"],
        allows_trade_signal=False,
        allows_order_decision=False,
        allows_portfolio_weight=False,
        allows_strategy_activation=False,
        allows_broker_execution=False,
        allows_paper_mutation=False,
        boundary_hash=None,
        boundary_valid=False,
        research_metadata_only=True
    )
    b.boundary_valid = len(validate_prediction_output_boundary(b)) == 0
    if b.boundary_valid:
        b.boundary_hash = compute_prediction_output_boundary_hash(b)
    return b

def compute_prediction_output_boundary_hash(boundary: PredictionOutputBoundary) -> str:
    s = f"{[k.value for k in boundary.allowed_output_kinds]}_{boundary.forbidden_output_fields}_{boundary.required_output_fields}_{boundary.allows_trade_signal}"
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def validate_prediction_output_boundary(boundary: PredictionOutputBoundary) -> List[str]:
    errors = []
    if boundary.allows_trade_signal:
        errors.append("Boundary allows trade signal")
    if boundary.allows_order_decision:
        errors.append("Boundary allows order decision")
    if boundary.allows_portfolio_weight:
        errors.append("Boundary allows portfolio weight")
    if boundary.allows_strategy_activation:
        errors.append("Boundary allows strategy activation")
    if boundary.allows_broker_execution:
        errors.append("Boundary allows broker execution")
    if boundary.allows_paper_mutation:
        errors.append("Boundary allows paper mutation")
    if not boundary.research_metadata_only:
        errors.append("Boundary is not metadata only")
    return errors

def validate_prediction_output_payload(payload: Dict[str, Any]) -> List[str]:
    errors = []
    for f in forbidden_prediction_output_fields():
        if f in payload:
            errors.append(f"Forbidden field found in payload: {f}")
    return errors

def validate_prediction_output_columns(columns: List[str]) -> List[str]:
    errors = []
    for f in forbidden_prediction_output_fields():
        if f in columns:
            errors.append(f"Forbidden field found in columns: {f}")
    return errors

def prediction_output_boundary_summary(boundary: PredictionOutputBoundary) -> Dict[str, Any]:
    return {
        "valid": boundary.boundary_valid,
        "hash": boundary.boundary_hash,
        "allowed_kinds": [k.value for k in boundary.allowed_output_kinds]
    }

def prediction_output_boundary_to_text(boundary: PredictionOutputBoundary, limit: int = 300) -> str:
    summary = prediction_output_boundary_summary(boundary)
    return f"Prediction Output Boundary: Valid={summary['valid']}, Hash={summary['hash']}"
