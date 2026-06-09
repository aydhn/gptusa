from typing import Any, Dict, List, Optional
# Fallback for pandas
try:
    import pandas as pd
except ImportError:
    pd = None

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    PortfolioRiskContext,
    PortfolioRiskSummary,
    PortfolioGovernanceReport,
    PortfolioBandFinalReview,
    PortfolioBandClosureCertificate,
    Phase158HandoffPackage,
    PortfolioRiskSafetyBoundaryResult
)
from usa_signal_bot.core.enums import PortfolioRiskReportingRiskFlag
from usa_signal_bot.portfolio.risk_reporting.governance_input_resolver import detect_forbidden_portfolio_risk_columns, detect_forbidden_portfolio_risk_fields

def validate_portfolio_risk_context_safety(context: PortfolioRiskContext) -> List[str]:
    errs = []
    if context.live_trading_enabled: errs.append("live_trading_enabled")
    if context.paper_trading_enabled: errs.append("paper_trading_enabled")
    if context.broker_execution_enabled: errs.append("broker_execution_enabled")
    if context.real_order_creation_enabled: errs.append("real_order_creation_enabled")
    if context.paper_state_mutation_enabled: errs.append("paper_state_mutation_enabled")
    if context.telegram_real_send_enabled: errs.append("telegram_real_send_enabled")
    if context.strategy_activation_allowed: errs.append("strategy_activation_allowed")
    if context.actual_target_weights_produced: errs.append("actual_target_weights_produced")
    if context.actual_portfolio_weights_produced: errs.append("actual_portfolio_weights_produced")
    if context.actual_allocation_produced: errs.append("actual_allocation_produced")
    if context.actual_position_size_produced: errs.append("actual_position_size_produced")
    if context.order_size_produced: errs.append("order_size_produced")
    if context.capital_deployment_allowed: errs.append("capital_deployment_allowed")
    if context.actual_portfolio_optimization_enabled: errs.append("actual_portfolio_optimization_enabled")
    if context.deployment_allowed: errs.append("deployment_allowed")
    if context.produces_live_signal: errs.append("produces_live_signal")
    if context.produces_order_decision: errs.append("produces_order_decision")
    if context.investment_advice: errs.append("investment_advice")
    return errs

def validate_portfolio_risk_summary_safety(summary: PortfolioRiskSummary) -> List[str]:
    return []

def validate_portfolio_governance_report_safety(report: PortfolioGovernanceReport) -> List[str]:
    return []

def validate_portfolio_band_final_review_safety(review: PortfolioBandFinalReview) -> List[str]:
    return []

def validate_portfolio_band_closure_certificate_safety(certificate: PortfolioBandClosureCertificate) -> List[str]:
    return []

def validate_phase158_handoff_package_safety(package: Phase158HandoffPackage) -> List[str]:
    return []

def validate_portfolio_risk_safety_boundary_safety(boundary: PortfolioRiskSafetyBoundaryResult) -> List[str]:
    return []

def validate_phase158_readiness_gate_safety(gate: Any) -> List[str]:
    return []

def validate_portfolio_risk_dataframe_output_safety(df: Any) -> List[str]:
    if pd and isinstance(df, pd.DataFrame):
        return detect_forbidden_portfolio_risk_columns(list(df.columns))
    return []

def portfolio_risk_text_has_trade_or_execution_language(text: str) -> bool:
    t = text.lower()
    unsafe = ["buy ", "sell ", "guaranteed ", "investment advice", "execute ", "place order", "active trading"]
    for u in unsafe:
        if u in t: return True
    return False

def portfolio_risk_payload_has_forbidden_fields(payload: Dict[str, Any]) -> bool:
    return len(detect_forbidden_portfolio_risk_fields(payload)) > 0

def collect_portfolio_risk_flags(context: Optional[PortfolioRiskContext] = None) -> List[PortfolioRiskReportingRiskFlag]:
    return context.risk_flags if context else []

def portfolio_risk_safety_summary(errors: List[str]) -> Dict[str, Any]:
    return {"safety_errors": len(errors)}

def portfolio_risk_safety_to_text(errors: List[str]) -> str:
    return f"{len(errors)} Safety Errors"
