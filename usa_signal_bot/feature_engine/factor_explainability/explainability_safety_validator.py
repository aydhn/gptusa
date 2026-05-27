from typing import Any
import re

from usa_signal_bot.core.enums import FactorExplainabilityRiskFlag
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    ExplainabilityContext,
    FeatureAttributionResult,
    FactorInterpretationSummary,
    ResearchReportDocument,
    ReportQaRuleResult
)

def explainability_text_has_trade_or_execution_language(text: str) -> bool:
    forbidden = ["buy", "sell", "entry", "exit", "order", "broker", "position",
                 "portfolio_weight", "target_weight", "allocation", "paper", "live",
                 "demo_order", "live_order", "sent_to_broker"]
    # Allow macd_signal_9
    lower = text.lower()
    for f in forbidden:
        if f in lower:
            # check for exact 'signal' without 'macd_signal_9' context here if needed
            return True
    return False

def validate_explainability_columns_safety(columns: list[str]) -> list[str]:
    errors = []
    forbidden = ["buy", "sell", "entry", "exit", "order", "position",
                 "portfolio_weight", "target_weight", "allocation", "sent_to_broker"]
    for c in columns:
        if c.lower() in forbidden:
            errors.append(f"Forbidden column found: {c}")
    return errors

def validate_explainability_context_safety(context: ExplainabilityContext) -> list[str]:
    errors = []
    if context.activation_allowed:
        errors.append("activation_allowed is true")
    return errors

def validate_feature_attribution_results_safety(results: list[FeatureAttributionResult]) -> list[str]:
    errors = []
    for r in results:
        if r.produces_trade_signal:
            errors.append(f"Result {r.attribution_id} produces trade signal")
    return errors

def validate_factor_interpretations_safety(items: list[FactorInterpretationSummary]) -> list[str]:
    errors = []
    for i in items:
        if i.produces_trade_signal:
            errors.append(f"Interpretation {i.interpretation_id} produces trade signal")
        if i.investment_advice:
            errors.append(f"Interpretation {i.interpretation_id} contains investment advice")
    return errors

def validate_research_report_safety(document: ResearchReportDocument) -> list[str]:
    errors = []
    if document.produces_trade_signal:
         errors.append("Report document produces trade signal")
    return errors

def validate_report_qa_results_safety(results: list[ReportQaRuleResult]) -> list[str]:
    errors = []
    for r in results:
        if not r.passed:
             errors.append(f"QA Rule {r.rule_name} failed")
    return errors

def collect_explainability_risk_flags(context: ExplainabilityContext | None = None) -> list[FactorExplainabilityRiskFlag]:
    flags = []
    if context:
        if context.activation_allowed:
            flags.append(FactorExplainabilityRiskFlag.ORDER_RISK)
    return flags

def explainability_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"error_count": len(errors), "safe": len(errors) == 0}

def explainability_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Safety validation passed."
    return f"Safety validation failed with {len(errors)} errors."
