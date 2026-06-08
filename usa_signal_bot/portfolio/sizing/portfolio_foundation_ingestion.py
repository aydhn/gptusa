from typing import Any
from pathlib import Path
from usa_signal_bot.portfolio.sizing.phase154_models import PortfolioFoundationIngestionResult, SizingPrototypeRiskFlag
import json

def ingest_portfolio_foundation_review_payload(payload: dict[str, Any]) -> PortfolioFoundationIngestionResult:
    result = PortfolioFoundationIngestionResult()
    if not payload:
        result.valid_for_phase154 = False
        result.errors.append("Empty payload.")
        return result

    result.available = True

    # Check foundation properties
    result.ready_for_phase154 = payload.get("ready_for_phase154", False)
    result.phase154_readiness_gate_passed = payload.get("phase154_readiness_gate_passed", False)
    result.safety_boundary_validated = payload.get("safety_boundary_validated", False)
    result.candidate_universe_contract_built = payload.get("candidate_universe_contract_built", False)
    result.risk_budget_contract_built = payload.get("risk_budget_contract_built", False)
    result.position_sizing_boundary_built = payload.get("position_sizing_boundary_built", False)

    # Check forbidden properties
    result.live_trading_enabled = payload.get("live_trading_enabled", False)
    result.paper_trading_enabled = payload.get("paper_trading_enabled", False)
    result.broker_execution_enabled = payload.get("broker_execution_enabled", False)
    result.real_order_creation_enabled = payload.get("real_order_creation_enabled", False)
    result.paper_state_mutation_enabled = payload.get("paper_state_mutation_enabled", False)
    result.telegram_real_send_enabled = payload.get("telegram_real_send_enabled", False)
    result.deployment_allowed = payload.get("deployment_allowed", False)
    result.actual_portfolio_construction_executed = payload.get("actual_portfolio_construction_executed", False)
    result.actual_position_sizing_executed = payload.get("actual_position_sizing_executed", False)
    result.target_weights_produced = payload.get("target_weights_produced", False)
    result.allocation_output_produced = payload.get("allocation_output_produced", False)
    result.capital_deployment_allowed = payload.get("capital_deployment_allowed", False)
    result.investment_advice = payload.get("investment_advice", False)

    is_valid, errors = portfolio_foundation_supports_phase154(result.__dict__)
    result.valid_for_phase154 = is_valid
    result.errors.extend(errors)

    if not is_valid:
        result.risk_flags.append(SizingPrototypeRiskFlag.PORTFOLIO_FOUNDATION_REVIEW_INVALID)

    return result

def ingest_latest_portfolio_foundation_review_from_store(data_root: Path) -> PortfolioFoundationIngestionResult:
    # Dummy logic to be implemented, would search latest JSON in data_root
    return PortfolioFoundationIngestionResult(available=False, valid_for_phase154=False, errors=["Not implemented"])

def extract_candidate_universe_contract(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("candidate_universe_contract")

def extract_constraint_catalog(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("constraint_catalog")

def extract_risk_budget_contract(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("risk_budget_contract")

def extract_position_sizing_boundary(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("position_sizing_boundary")

def extract_portfolio_foundation_safety_boundary(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("safety_boundary")

def extract_phase154_readiness_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("phase154_readiness_gate")

def portfolio_foundation_supports_phase154(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []

    if not payload.get("ready_for_phase154", False):
        errors.append("Foundation is not ready for phase 154.")
    if not payload.get("phase154_readiness_gate_passed", False):
        errors.append("Phase154 readiness gate not passed.")
    if not payload.get("safety_boundary_validated", False):
        errors.append("Foundation safety boundary not validated.")
    if not payload.get("candidate_universe_contract_built", False):
        errors.append("Candidate universe contract missing.")
    if not payload.get("risk_budget_contract_built", False):
        errors.append("Risk budget contract missing.")
    if not payload.get("position_sizing_boundary_built", False):
        errors.append("Position sizing boundary missing.")

    for k in ["live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled",
              "real_order_creation_enabled", "paper_state_mutation_enabled",
              "telegram_real_send_enabled", "deployment_allowed",
              "actual_portfolio_construction_executed", "actual_position_sizing_executed",
              "target_weights_produced", "allocation_output_produced",
              "capital_deployment_allowed", "investment_advice"]:
        if payload.get(k, False):
            errors.append(f"Forbidden property '{k}' is True in foundation review.")

    return len(errors) == 0, errors

def portfolio_foundation_ingestion_to_text(result: PortfolioFoundationIngestionResult) -> str:
    return f"IngestionResult(valid={result.valid_for_phase154}, ready_for_phase154={result.ready_for_phase154}, errors={len(result.errors)})"
