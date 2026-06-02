from typing import Any
import pandas as pd

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    ExplainabilityInputReference,
    FeatureAttributionProxy,
    FactorContributionSummary,
    ModelBehaviorExplanation,
    ExplainabilityReport,
    MLGovernanceClosureResult,
    AdvancedMLArtifactLineage,
    AdvancedMLFinalAuditResult,
    AdvancedMLAcceptanceGate,
    AdvancedMLClosureContext
)
from usa_signal_bot.core.exceptions import MLClosureSchemaValidationError

def validate_ml_closure_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_ml_closure_columns(columns)

def validate_no_forbidden_ml_closure_columns(columns: list[str]) -> list[str]:
    errors = []
    forbidden = [
        "buy", "sell", "entry", "exit", "order", "broker", "position",
        "portfolio_weight", "target_weight", "allocation", "paper",
        "demo_order", "live_order", "sent_to_broker", "deploy",
        "production_patch", "strategy_active", "deployment_enabled",
        "alert_send", "live_monitoring", "backtest_run"
    ]

    for col in columns:
        col_lower = str(col).lower()
        if col_lower == "macd_signal_9":
            continue
        # Also skip things like 'live' if they are part of 'delivered'
        for f in forbidden:
            # simple substring match for now, could be regex if needed
            if f in col_lower and col_lower != "macd_signal_9" and col_lower != "alive":
                # Special cases to avoid false positives
                if f == "live" and ("delivered" in col_lower or "alive" in col_lower):
                    continue
                if f == "sell" and "selling" in col_lower:
                    continue # Depends on definition
                errors.append(f"Forbidden fragment '{f}' found in column name '{col}'")
    return errors

def validate_explainability_input_reference_schema(item: ExplainabilityInputReference) -> list[str]:
    return []

def validate_feature_attribution_proxy_schema(item: FeatureAttributionProxy) -> list[str]:
    return []

def validate_factor_contribution_summary_schema(item: FactorContributionSummary) -> list[str]:
    return []

def validate_model_behavior_explanation_schema(item: ModelBehaviorExplanation) -> list[str]:
    return []

def validate_explainability_report_schema(item: ExplainabilityReport) -> list[str]:
    return []

def validate_ml_governance_closure_schema(item: MLGovernanceClosureResult) -> list[str]:
    return []

def validate_advanced_ml_artifact_lineage_schema(item: AdvancedMLArtifactLineage) -> list[str]:
    return []

def validate_advanced_ml_final_audit_schema(item: AdvancedMLFinalAuditResult) -> list[str]:
    return []

def validate_advanced_ml_acceptance_gate_schema(item: AdvancedMLAcceptanceGate) -> list[str]:
    return []

def validate_advanced_ml_closure_context_schema(context: AdvancedMLClosureContext) -> list[str]:
    return []

def ml_closure_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors)
    }

def ml_closure_schema_to_text(errors: list[str]) -> str:
    if not errors:
        return "Schema validation passed."
    return f"Schema validation failed with {len(errors)} errors.\nFirst error: {errors[0]}"
