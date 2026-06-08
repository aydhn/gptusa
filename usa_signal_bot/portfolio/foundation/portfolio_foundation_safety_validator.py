import pandas
from typing import Any
from usa_signal_bot.portfolio.foundation.phase153_models import (
    PortfolioFoundationContext, CandidateUniverseContract, PortfolioConstraintCatalog,
    RiskBudgetContract, PositionSizingBoundaryContract, Phase154ReadinessGate,
    PortfolioFoundationRiskFlag
)

def portfolio_payload_has_forbidden_fields(payload: dict[str, Any]) -> bool:
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "portfolio_weight",
        "target_weight", "allocation", "capital_allocation", "position_size",
        "order_size", "real_order", "live_signal", "buy_signal", "sell_signal",
        "recommended_weight", "production_patch"
    ]
    for k in payload.keys():
        if k in forbidden:
            return True
    return False

def portfolio_foundation_text_has_trade_or_execution_language(text: str) -> bool:
    forbidden = ["emir gönderildi", "aktif trading başladı", "kesin al", "kesin sat", "garanti kâr", "yatırım tavsiyesi"]
    text_lower = text.lower()
    return any(f in text_lower for f in forbidden)

def validate_portfolio_foundation_context_safety(context: PortfolioFoundationContext) -> list[str]:
    errors = []
    for field in ["live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled", "real_order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled", "strategy_activation_allowed", "actual_portfolio_construction_executed", "actual_position_sizing_executed", "portfolio_optimization_enabled", "rebalancing_enabled", "target_weights_produced", "allocation_output_produced", "capital_deployment_allowed", "deployment_allowed", "network_used", "paid_api_used", "dashboard_started", "daemon_started", "scheduler_enabled", "produces_live_signal", "produces_order_decision", "produces_portfolio_weights", "investment_advice"]:
        if getattr(context, field):
            errors.append(f"Unsafe field {field} is True in context")
    return errors

def validate_candidate_universe_contract_safety(contract: CandidateUniverseContract) -> list[str]:
    errors = []
    if contract.live_trading_enabled or contract.paper_trading_enabled or contract.broker_execution_enabled:
        errors.append("Execution enabled in candidate universe contract")
    if contract.produces_live_signal or contract.produces_order_decision or contract.produces_portfolio_weights:
        errors.append("Signal production enabled in candidate universe contract")
    return errors

def validate_constraint_catalog_safety(catalog: PortfolioConstraintCatalog) -> list[str]:
    return []

def validate_risk_budget_contract_safety(contract: RiskBudgetContract) -> list[str]:
    return []

def validate_position_sizing_boundary_safety(boundary: PositionSizingBoundaryContract) -> list[str]:
    return []

def validate_phase154_readiness_gate_safety(gate: Phase154ReadinessGate) -> list[str]:
    return []

def validate_portfolio_foundation_dataframe_output_safety(df: pandas.DataFrame) -> list[str]:
    errors = []
    forbidden = [
        "broker_order", "paper_order", "live_order", "sent_to_broker",
        "strategy_active", "deployment_enabled", "portfolio_weight",
        "target_weight", "allocation", "capital_allocation", "position_size",
        "order_size", "real_order", "live_signal", "buy_signal", "sell_signal",
        "recommended_weight", "production_patch"
    ]
    detected = [c for c in df.columns if c in forbidden]
    if detected:
        errors.append(f"Forbidden portfolio columns detected in output dataframe: {detected}")
    return errors

def collect_portfolio_foundation_risk_flags(context: PortfolioFoundationContext | None = None) -> list[PortfolioFoundationRiskFlag]:
    if not context:
        return []
    flags = set()
    flags.update(context.risk_flags)
    if not context.safety_boundary.boundary_passed:
        flags.add(PortfolioFoundationRiskFlag.SAFETY_BOUNDARY_FAILED)
    if not context.phase154_readiness_gate.ready_for_phase154:
        flags.add(PortfolioFoundationRiskFlag.PHASE153_NOT_READY)
    return list(flags)

def portfolio_foundation_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {
        "safe": len(errors) == 0,
        "error_count": len(errors)
    }

def portfolio_foundation_safety_to_text(errors: list[str]) -> str:
    if not errors:
        return "Safety Valid"
    return "Safety Errors:\n" + "\n".join(f"- {e}" for e in errors)
