from typing import List, Dict, Any, Optional
from usa_signal_bot.core.enums import BaselineMLScaffoldingRiskFlag
from usa_signal_bot.ml_research.experiment_scaffolding.phase138_models import (
    BaselineMLScaffoldingContext,
    BaselineExperimentSpec,
    EvaluationHarnessContract,
    PredictionOutputBoundary,
    ModelCardDraft,
    BaselineExperimentRegistry,
    BaselineExperimentReadinessGate
)

def baseline_scaffolding_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    unsafe = [
        "guaranteed profit", "sure bet", "will make money", "definitely buy", "definitely sell",
        "live order", "paper order", "real money", "live execution", "sent to broker"
    ]
    for u in unsafe:
        if u in t:
            return True
    return False

def validate_baseline_scaffolding_context_safety(context: BaselineMLScaffoldingContext) -> List[str]:
    errors = []
    if context.activation_allowed: errors.append("activation_allowed is true")
    if context.strategy_activation_allowed: errors.append("strategy_activation_allowed is true")
    if context.deployment_allowed: errors.append("deployment_allowed is true")
    if context.active_paper_enabled: errors.append("active_paper_enabled is true")
    if context.broker_execution_enabled: errors.append("broker_execution_enabled is true")
    if context.order_creation_enabled: errors.append("order_creation_enabled is true")
    if context.paper_state_mutation_enabled: errors.append("paper_state_mutation_enabled is true")
    if context.telegram_real_send_enabled: errors.append("telegram_real_send_enabled is true")
    if context.scraping_enabled: errors.append("scraping_enabled is true")
    if context.html_parse_enabled: errors.append("html_parse_enabled is true")
    if context.paid_api_enabled: errors.append("paid_api_enabled is true")
    if context.dashboard_enabled: errors.append("dashboard_enabled is true")
    if context.network_default_enabled: errors.append("network_default_enabled is true")
    if context.daemon_started: errors.append("daemon_started is true")
    if context.scheduler_enabled: errors.append("scheduler_enabled is true")
    if context.training_started: errors.append("training_started is true")
    if context.prediction_started: errors.append("prediction_started is true")
    if context.model_training_used: errors.append("model_training_used is true")
    if context.model_prediction_used: errors.append("model_prediction_used is true")
    if context.heavy_ml_dependency_used: errors.append("heavy_ml_dependency_used is true")
    if context.produces_trade_signal: errors.append("produces_trade_signal is true")
    if context.produces_order_decision: errors.append("produces_order_decision is true")
    if context.produces_portfolio_weights: errors.append("produces_portfolio_weights is true")
    if context.investment_advice: errors.append("investment_advice is true")
    return errors

def validate_baseline_experiment_specs_safety(items: List[BaselineExperimentSpec]) -> List[str]:
    errors = []
    for item in items:
        if not item.training_deferred_to_phase139:
            errors.append(f"training_deferred_to_phase139 false in {item.experiment_name}")
        if not item.prediction_deferred_to_phase139:
            errors.append(f"prediction_deferred_to_phase139 false in {item.experiment_name}")
    return errors

def validate_evaluation_harness_safety(contract: EvaluationHarnessContract) -> List[str]:
    errors = []
    if contract.training_allowed_in_phase138: errors.append("Harness allows training")
    if contract.prediction_allowed_in_phase138: errors.append("Harness allows prediction")
    return errors

def validate_prediction_output_boundary_safety(boundary: PredictionOutputBoundary) -> List[str]:
    errors = []
    if boundary.allows_trade_signal: errors.append("Boundary allows trade signal")
    return errors

def validate_model_card_draft_safety(card: ModelCardDraft) -> List[str]:
    errors = []
    if not card.not_investment_advice: errors.append("Card missing not investment advice notice")
    if baseline_scaffolding_text_has_trade_or_execution_language(card.rendered_text or ""):
        errors.append("Card contains unsafe execution language")
    return errors

def validate_experiment_registry_safety(registry: BaselineExperimentRegistry) -> List[str]:
    errors = []
    if registry.training_started: errors.append("Registry training started")
    return errors

def validate_baseline_readiness_gate_safety(gate: BaselineExperimentReadinessGate) -> List[str]:
    errors = []
    if gate.training_started: errors.append("Gate training started")
    return errors

def validate_baseline_scaffolding_dataframe_output_safety(df: Any) -> List[str]:
    # Changed type hint to Any to remove pandas import dependency for scaffolding checks
    errors = []
    forbidden = ["buy", "sell", "order", "broker", "portfolio_weight"]
    if hasattr(df, "columns"):
        for col in df.columns:
            c = str(col).lower()
            for f in forbidden:
                if f in c:
                    errors.append(f"Forbidden column in dataframe: {c}")
    return errors

def collect_baseline_scaffolding_risk_flags(context: Optional[BaselineMLScaffoldingContext] = None) -> List[BaselineMLScaffoldingRiskFlag]:
    flags = []
    if context:
        if context.heavy_ml_dependency_used:
            flags.append(BaselineMLScaffoldingRiskFlag.HEAVY_ML_DEPENDENCY_RISK)
        if context.training_started:
            flags.append(BaselineMLScaffoldingRiskFlag.MODEL_TRAINING_ATTEMPTED)
        if context.prediction_started:
            flags.append(BaselineMLScaffoldingRiskFlag.MODEL_PREDICTION_ATTEMPTED)
    return flags

def baseline_scaffolding_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": errors}

def baseline_scaffolding_safety_to_text(errors: List[str]) -> str:
    if not errors: return "Safety valid."
    return "Safety errors: " + ", ".join(errors)
