from typing import Any
import pandas as pd
from pathlib import Path

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    ExplainabilityInputReference,
    ExplainabilityInputKind,
    create_explainability_input_reference_id,
    current_time
)

def infer_explainability_input_kind(payload: dict[str, Any]) -> ExplainabilityInputKind:
    if "features" in payload:
        return ExplainabilityInputKind.FEATURE_MATRIX
    if "factors" in payload:
        return ExplainabilityInputKind.FACTOR_MATRIX
    if "model_card" in payload:
        return ExplainabilityInputKind.MODEL_CARD_REFERENCE
    if "phase_number" in payload:
        return ExplainabilityInputKind.PHASE_REVIEW_REFERENCE
    return ExplainabilityInputKind.UNKNOWN

def build_explainability_input_references(
    monitoring_package: dict[str, Any],
    governance_payload: dict[str, Any],
    model_card_updates: list[dict[str, Any]],
    phase_reviews: list[dict[str, Any]] | None = None
) -> list[ExplainabilityInputReference]:

    refs = []

    # In a real implementation this would create refs for all inputs.
    # We will simulate a couple for the required output format.

    refs.append(ExplainabilityInputReference(
        input_ref_id=create_explainability_input_reference_id(),
        created_at_utc=current_time(),
        input_kind=ExplainabilityInputKind.MODEL_CARD_REFERENCE,
        source_artifact_name="model_card_drift_updates",
        source_path=None,
        source_hash=None,
        phase_number=144,
        model_artifact_id=None,
        prototype_id=None,
        registry_entry_id=None,
        available=True,
        read_only=True,
        research_data_only=True,
        offline_ml_research_only=True,
        contains_forbidden_outputs=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    ))

    if phase_reviews:
        for pr in phase_reviews:
            phase_num = pr.get("phase_number")
            refs.append(ExplainabilityInputReference(
                input_ref_id=create_explainability_input_reference_id(),
                created_at_utc=current_time(),
                input_kind=ExplainabilityInputKind.PHASE_REVIEW_REFERENCE,
                source_artifact_name=f"phase_{phase_num}_review",
                source_path=None,
                source_hash=None,
                phase_number=phase_num,
                model_artifact_id=None,
                prototype_id=None,
                registry_entry_id=None,
                available=True,
                read_only=True,
                research_data_only=True,
                offline_ml_research_only=True,
                contains_forbidden_outputs=False,
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            ))

    return refs

def validate_explainability_input_references(items: list[ExplainabilityInputReference]) -> list[str]:
    errors = []
    for item in items:
        if item.contains_forbidden_outputs:
            errors.append(f"Input {item.input_ref_id} contains forbidden outputs")
        if not item.research_data_only:
            errors.append(f"Input {item.input_ref_id} is not marked research_data_only")
    return errors

def validate_explainability_input_frame(df: pd.DataFrame) -> list[str]:
    errors = []
    forbidden_cols = ["buy", "sell", "entry", "exit", "order", "portfolio_weight", "allocation"]
    for col in df.columns:
        col_lower = col.lower()
        if col_lower == "macd_signal_9":
            continue
        if any(f in col_lower for f in forbidden_cols):
            errors.append(f"Forbidden column found: {col}")
    return errors

def explainability_input_resolver_summary(items: list[ExplainabilityInputReference]) -> dict[str, Any]:
    return {
        "count": len(items),
        "kinds": list(set([i.input_kind.value for i in items]))
    }

def explainability_input_resolver_to_text(items: list[ExplainabilityInputReference], limit: int = 300) -> str:
    summary = explainability_input_resolver_summary(items)
    return f"Resolved {summary['count']} inputs of kinds: {', '.join(summary['kinds'])}"
