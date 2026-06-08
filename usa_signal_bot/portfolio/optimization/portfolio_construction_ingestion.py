import json
from pathlib import Path
from typing import Any, Optional, Tuple, List
from usa_signal_bot.portfolio.optimization.phase156_models import PortfolioConstructionIngestionResult

def ingest_portfolio_construction_review_payload(payload: dict) -> PortfolioConstructionIngestionResult:
    result = PortfolioConstructionIngestionResult()
    result.available = True
    result.metadata = {"original_payload_keys": list(payload.keys())}
    result.ready_for_phase156 = payload.get("ready_for_phase156", False)

    if not payload.get("ready_for_phase156", False):
        result.valid_for_phase156 = False
        result.errors.append("Payload indicates not ready for phase 156")
        return result

    result.research_data_only = payload.get("research_data_only", False)
    result.allocation_sandbox_only = payload.get("allocation_sandbox_only", False)

    if not result.research_data_only or not result.allocation_sandbox_only:
        result.valid_for_phase156 = False
        result.errors.append("Not strictly research_data_only or allocation_sandbox_only")

    for k in ["actual_target_weights_produced", "actual_allocation_produced", "order_size_produced", "capital_deployment_allowed"]:
        if payload.get(k, False):
            setattr(result, k, True)
            result.valid_for_phase156 = False
            result.errors.append(f"Forbidden true: {k}")

    for k in ["live_trading_enabled", "paper_trading_enabled", "broker_execution_enabled", "real_order_creation_enabled", "paper_state_mutation_enabled", "telegram_real_send_enabled", "deployment_allowed", "network_used", "dashboard_started"]:
        if payload.get(k, False):
            setattr(result, k, True)
            result.valid_for_phase156 = False
            result.errors.append(f"Forbidden environment feature: {k}")

    if not result.errors:
        result.valid_for_phase156 = True

    return result

def ingest_latest_portfolio_construction_review_from_store(data_root: Path) -> PortfolioConstructionIngestionResult:
    return PortfolioConstructionIngestionResult(errors=["Not implemented"], valid_for_phase156=False)

def extract_portfolio_construction_policy(payload: dict) -> Optional[dict]:
    return payload.get("policy")

def extract_allocation_sandbox_comparison_report(payload: dict) -> Optional[dict]:
    return payload.get("comparison_report")

def extract_prototype_exposure_table(payload: dict) -> Optional[dict]:
    return payload.get("prototype_exposure_table")

def extract_portfolio_construction_validation_report(payload: dict) -> Optional[dict]:
    return payload.get("validation_report")

def extract_allocation_sandbox_safety_boundary(payload: dict) -> Optional[dict]:
    return payload.get("safety_boundary")

def extract_phase156_readiness_gate(payload: dict) -> Optional[dict]:
    return payload.get("phase156_readiness_gate")

def portfolio_construction_supports_phase156(payload: dict) -> Tuple[bool, List[str]]:
    r = ingest_portfolio_construction_review_payload(payload)
    return r.valid_for_phase156, r.errors

def portfolio_construction_ingestion_to_text(result: PortfolioConstructionIngestionResult) -> str:
    return f"IngestionResult: valid={result.valid_for_phase156}, errors={result.errors}"
