from pathlib import Path
from typing import Any
import datetime

from usa_signal_bot.feature_engine.factor_explainability.phase123_models import (
    FactorValidationIngestionResult,
    ExplainabilityInputBundle,
    create_factor_validation_ingestion_id,
    create_explainability_input_bundle_id,
    validate_factor_validation_ingestion_result
)

def extract_factor_validation_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def factor_validation_supports_phase123(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    warnings = []
    if "review_id" not in payload:
        return False, ["Missing review_id in payload"]
    return True, warnings

def ingest_factor_validation_review_payload(payload: dict[str, Any]) -> FactorValidationIngestionResult:
    valid, warnings = factor_validation_supports_phase123(payload)

    result = FactorValidationIngestionResult(
        ingestion_id=create_factor_validation_ingestion_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=payload.get("context", {}).get("context_id"),
        available=valid,
        factor_validation_ready=payload.get("validation_ready", valid),
        drift_monitoring_ready=payload.get("drift_ready", valid),
        factor_versioning_ready=payload.get("versioning_ready", valid),
        factor_store_hardened=payload.get("store_hardened", valid),
        ready_for_phase123=valid,
        metadata_only=True,
        research_data_only=True,
        activation_allowed=payload.get("activation_allowed", False),
        strategy_activation_allowed=payload.get("strategy_activation_allowed", False),
        active_paper_enabled=payload.get("active_paper_enabled", False),
        broker_execution_enabled=payload.get("broker_execution_enabled", False),
        order_creation_enabled=payload.get("order_creation_enabled", False),
        paper_state_mutation_enabled=payload.get("paper_state_mutation_enabled", False),
        telegram_real_send_enabled=payload.get("telegram_real_send_enabled", False),
        scraping_enabled=payload.get("scraping_enabled", False),
        html_parse_enabled=payload.get("html_parse_enabled", False),
        paid_api_enabled=payload.get("paid_api_enabled", False),
        dashboard_enabled=payload.get("dashboard_enabled", False),
        network_default_enabled=payload.get("network_default_enabled", False),
        produces_trade_signal=payload.get("produces_trade_signal", False),
        produces_order_decision=payload.get("produces_order_decision", False),
        produces_portfolio_weights=payload.get("produces_portfolio_weights", False),
        network_used=payload.get("network_used", False),
        paid_api_used=payload.get("paid_api_used", False),
        scraping_used=payload.get("scraping_used", False),
        html_parsing_used=payload.get("html_parsing_used", False),
        broker_used=payload.get("broker_used", False),
        order_created=payload.get("order_created", False),
        paper_state_mutated=payload.get("paper_state_mutated", False),
        telegram_real_sent=payload.get("telegram_real_sent", False),
        dashboard_started=payload.get("dashboard_started", False),
        valid_for_phase123=valid,
        risk_flags=[],
        warnings=warnings,
        errors=[],
        metadata={"payload_keys": list(payload.keys())}
    )

    validate_factor_validation_ingestion_result(result)
    if result.errors:
        result.valid_for_phase123 = False

    return result

def ingest_latest_factor_validation_review_from_store(data_root: Path) -> FactorValidationIngestionResult:
    # Dummy logic to be implemented with real store reading later
    return ingest_factor_validation_review_payload({})

def extract_explainability_input_bundle(payload: dict[str, Any]) -> ExplainabilityInputBundle:
    return ExplainabilityInputBundle(
        bundle_id=create_explainability_input_bundle_id(),
        created_at_utc=datetime.datetime.utcnow().isoformat(),
        source_review_id=payload.get("review_id"),
        factor_table_paths=payload.get("factor_table_paths", {}),
        validation_result_refs=payload.get("validation_result_refs", []),
        drift_report_refs=payload.get("drift_report_refs", []),
        diagnostics_refs=payload.get("diagnostics_refs", []),
        manifest_ref=payload.get("manifest_ref"),
        schema_signature_ref=payload.get("schema_signature_ref"),
        version_ref=payload.get("version_ref"),
        available=True,
        research_data_only=True,
        bundle_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def factor_validation_ingestion_to_text(result: FactorValidationIngestionResult) -> str:
    return f"FactorValidationIngestionResult(valid={result.valid_for_phase123}, errors={result.errors})"
