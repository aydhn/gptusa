from typing import Any, List
import pandas as pd

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    ModelComparisonScore,
    ModelRankingTable,
    CandidateShortlist,
    CalibrationReadinessProfile,
    SelectionGovernanceResult,
    BaselineModelComparisonContext
)

def validate_model_comparison_score_schema(item: ModelComparisonScore) -> list[str]:
    return []

def validate_model_ranking_table_schema(item: ModelRankingTable) -> list[str]:
    return []

def validate_candidate_shortlist_schema(item: CandidateShortlist) -> list[str]:
    return []

def validate_calibration_readiness_profile_schema(item: CalibrationReadinessProfile) -> list[str]:
    return []

def validate_selection_governance_schema(item: SelectionGovernanceResult) -> list[str]:
    return []

def validate_model_comparison_context_schema(context: BaselineModelComparisonContext) -> list[str]:
    return []

def validate_model_comparison_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_model_comparison_columns(columns)

def validate_no_forbidden_model_comparison_columns(columns: list[str]) -> list[str]:
    errors = []
    forbidden_exact = ["buy", "sell", "entry", "exit", "order", "broker", "position", "portfolio_weight", "target_weight", "allocation", "paper", "live", "demo_order", "live_order", "deploy", "strategy_active"]
    forbidden_partial = ["sent_to_broker", "production_patch", "deployment_enabled"]
    for col in columns:
        col_lower = col.lower()
        if col_lower in forbidden_exact:
            errors.append(f"Forbidden exact column name found: {col}")
        for part in forbidden_partial:
            if part in col_lower:
                errors.append(f"Forbidden partial column name found: {col}")

        if "signal" in col_lower and not ("macd_signal" in col_lower):
            errors.append(f"Forbidden 'signal' column name found: {col}")
    return errors

def model_comparison_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors)}

def model_comparison_schema_to_text(errors: list[str]) -> str:
    return str(errors)
