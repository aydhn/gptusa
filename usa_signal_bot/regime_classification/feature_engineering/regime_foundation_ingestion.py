import json
from pathlib import Path
from typing import Any
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import (
    RegimeFoundationIngestionResult,
    RegimeFeatureEngineeringRiskFlag
)

def ingest_regime_foundation_review_payload(payload: dict[str, Any]) -> RegimeFoundationIngestionResult:
    result = RegimeFoundationIngestionResult()
    result.metadata_only = True
    result.research_data_only = True
    result.activation_allowed = False
    result.strategy_activation_allowed = False
    result.deployment_allowed = False
    result.active_paper_enabled = False
    result.broker_execution_enabled = False
    result.order_creation_enabled = False
    result.paper_state_mutation_enabled = False
    result.telegram_real_send_enabled = False
    result.scraping_enabled = False
    result.html_parse_enabled = False
    result.paid_api_enabled = False
    result.dashboard_enabled = False
    result.network_default_enabled = False
    result.produces_trade_signal = False
    result.produces_order_decision = False
    result.produces_portfolio_weights = False
    result.investment_advice = False
    result.model_training_used = False
    result.heavy_ml_dependency_used = False

    if not payload:
        result.valid_for_phase127 = False
        result.risk_flags.append(RegimeFeatureEngineeringRiskFlag.REGIME_FOUNDATION_REVIEW_MISSING)
        return result

    result.available = True
    result.source_review_id = payload.get("review_id")

    foundation_context = extract_regime_foundation_context(payload)
    if foundation_context:
        result.source_context_id = foundation_context.get("context_id")
        result.final_closure_ingested = foundation_context.get("final_closure_built", False)
        result.frozen_artifacts_ready = foundation_context.get("frozen_artifacts_ready", False)
        result.input_contract_ready = foundation_context.get("input_bundle_ready", False)
        result.market_state_dataset_contract_ready = foundation_context.get("market_state_dataset_contract_ready", False)
        result.regime_taxonomy_ready = foundation_context.get("taxonomy_ready", False)
        result.non_activation_boundary_ready = foundation_context.get("non_activation_boundary_passed", False)
        result.ready_for_phase127 = foundation_context.get("ready_for_phase127", False)

    supports_p127, errors = regime_foundation_supports_phase127(payload)
    if not supports_p127:
        result.valid_for_phase127 = False
        result.errors.extend(errors)
        result.risk_flags.append(RegimeFeatureEngineeringRiskFlag.REGIME_FOUNDATION_REVIEW_INVALID)
    else:
        result.valid_for_phase127 = True

    return result

def ingest_latest_regime_foundation_review_from_store(data_root: Path) -> RegimeFoundationIngestionResult:
    reviews_dir = data_root / "regime_classification" / "foundation" / "reviews"
    if not reviews_dir.exists():
        return ingest_regime_foundation_review_payload({})

    json_files = list(reviews_dir.glob("*.json"))
    if not json_files:
        return ingest_regime_foundation_review_payload({})

    latest_file = sorted(json_files)[-1]
    try:
        with open(latest_file, "r") as f:
            payload = json.load(f)
        result = ingest_regime_foundation_review_payload(payload)
        result.source_path = str(latest_file)
        return result
    except Exception as e:
        res = ingest_regime_foundation_review_payload({})
        res.errors.append(f"Failed to read file: {e}")
        return res

def extract_regime_foundation_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_market_state_dataset_contract(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("market_state_dataset_contract")

def extract_regime_taxonomy(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("taxonomy")

def extract_regime_input_bundle(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("input_bundle")

def regime_foundation_supports_phase127(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    context = extract_regime_foundation_context(payload)
    if not context:
        return False, ["No context found"]

    if not context.get("ready_for_phase127", False):
        errors.append("ready_for_phase127 is false")

    if context.get("activation_allowed", False):
        errors.append("activation_allowed is true")

    return len(errors) == 0, errors

def regime_foundation_ingestion_to_text(result: RegimeFoundationIngestionResult) -> str:
    lines = [f"Ingestion: {result.ingestion_id}"]
    return "\\n".join(lines)
