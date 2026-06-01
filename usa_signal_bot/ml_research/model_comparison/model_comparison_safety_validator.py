from typing import Any, List
import pandas as pd

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    BaselineModelComparisonContext,
    ModelComparisonScore,
    ModelRankingTable,
    CandidateShortlist,
    CalibrationReadinessProfile,
    SelectionGovernanceResult,
    ModelCardComparisonUpdate,
    ModelComparisonReadinessGate,
    BaselineModelComparisonRiskFlag
)
from usa_signal_bot.ml_research.model_comparison.model_comparison_schema_validator import validate_model_comparison_column_names

def validate_model_comparison_context_safety(context: BaselineModelComparisonContext) -> list[str]:
    errors = []
    if context.activation_allowed:
        errors.append("activation_allowed must be false")
    if context.strategy_activation_allowed:
        errors.append("strategy_activation_allowed must be false")
    if context.deployment_allowed:
        errors.append("deployment_allowed must be false")
    if context.active_paper_enabled:
        errors.append("active_paper_enabled must be false")
    if context.broker_execution_enabled:
        errors.append("broker_execution_enabled must be false")
    if context.order_creation_enabled:
        errors.append("order_creation_enabled must be false")
    if context.paper_state_mutation_enabled:
        errors.append("paper_state_mutation_enabled must be false")
    if context.telegram_real_send_enabled:
        errors.append("telegram_real_send_enabled must be false")
    if context.scraping_enabled or context.html_parse_enabled or context.paid_api_enabled or context.dashboard_enabled or context.network_default_enabled:
        errors.append("unsafe integrations enabled")
    if context.daemon_started or context.scheduler_enabled:
        errors.append("background processes enabled")
    if context.live_inference_enabled or context.online_inference_enabled:
        errors.append("live inference enabled")
    if context.calibration_fitting_performed:
        errors.append("calibration fitting performed")
    if context.heavy_ml_dependency_used:
        errors.append("heavy ml dependency used")
    if context.produces_trade_signal or context.produces_order_decision or context.produces_portfolio_weights:
        errors.append("produces trade output")
    if context.investment_advice:
        errors.append("investment advice true")
    return errors

def validate_model_comparison_scores_safety(items: list[ModelComparisonScore]) -> list[str]:
    return []

def validate_model_ranking_safety(ranking: ModelRankingTable) -> list[str]:
    return []

def validate_candidate_shortlist_safety(shortlist: CandidateShortlist) -> list[str]:
    return []

def validate_calibration_preparation_safety(items: list[CalibrationReadinessProfile]) -> list[str]:
    return []

def validate_selection_governance_safety(result: SelectionGovernanceResult) -> list[str]:
    return []

def validate_model_card_comparison_updates_safety(items: list[ModelCardComparisonUpdate]) -> list[str]:
    return []

def validate_model_comparison_readiness_gate_safety(gate: ModelComparisonReadinessGate) -> list[str]:
    return []

def validate_model_comparison_dataframe_output_safety(df: pd.DataFrame) -> list[str]:
    if df is None or df.empty:
        return []
    return validate_model_comparison_column_names(list(df.columns))

def model_comparison_text_has_trade_or_execution_language(text: str) -> bool:
    forbidden = ["buy", "sell", "guaranteed profit", "deploy", "best stock", "recommendation to trade"]
    text_lower = text.lower()
    return any(f in text_lower for f in forbidden)

def collect_model_comparison_risk_flags(context: BaselineModelComparisonContext | None = None) -> list[str]:
    flags = []
    if context and context.heavy_ml_dependency_used:
        flags.append("HEAVY_ML_DEPENDENCY_RISK")
    return flags

def model_comparison_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors)}

def model_comparison_safety_to_text(errors: list[str]) -> str:
    return str(errors)
