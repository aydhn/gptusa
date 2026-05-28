import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from usa_signal_bot.core.exceptions import FinalClosureIngestionError
from usa_signal_bot.core.enums import RegimeFoundationRiskFlag
from usa_signal_bot.regime_classification.foundation.phase126_models import (
    FinalClosureIngestionResult,
    create_final_closure_ingestion_id,
    _now
)

def extract_final_closure_context(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("context")

def extract_engine_readiness_certificate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("engine_certificate")

def extract_phase126_kickoff_gate(payload: dict[str, Any]) -> dict[str, Any] | None:
    return payload.get("phase126_kickoff_gate")

def final_closure_supports_phase126(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []

    ctx = extract_final_closure_context(payload)
    if not ctx:
        return False, ["Missing final closure context"]

    gate = extract_phase126_kickoff_gate(payload)
    if not gate:
        return False, ["Missing Phase 126 Kickoff Gate"]

    if not ctx.get("ready_for_phase126", False):
        warnings.append("Context indicates not ready for Phase 126")
        return False, warnings

    if not gate.get("gate_passed", False):
        warnings.append("Phase 126 Kickoff Gate not passed")
        return False, warnings

    return True, warnings

def ingest_final_closure_review_payload(payload: dict[str, Any]) -> FinalClosureIngestionResult:
    ingestion_id = create_final_closure_ingestion_id()
    created_at_utc = _now()

    warnings = []
    errors = []
    risk_flags = []

    ctx = extract_final_closure_context(payload)
    if not ctx:
        errors.append("Final closure review context missing or invalid.")
        risk_flags.append(RegimeFoundationRiskFlag.FINAL_CLOSURE_REVIEW_MISSING)

    gate = extract_phase126_kickoff_gate(payload)
    if not gate:
        errors.append("Phase 126 Kickoff Gate missing.")
        risk_flags.append(RegimeFoundationRiskFlag.PHASE126_KICKOFF_GATE_FAILED)

    cert = extract_engine_readiness_certificate(payload)
    if not cert:
        errors.append("Engine readiness certificate missing.")
        risk_flags.append(RegimeFoundationRiskFlag.ENGINE_CERTIFICATE_INVALID)

    ready_for_phase126, sup_warnings = final_closure_supports_phase126(payload)
    warnings.extend(sup_warnings)

    final_artifacts_ready = ctx.get("final_artifacts_ready", False) if ctx else False
    final_checks_passed = ctx.get("final_checks_passed", False) if ctx else False
    freeze_seal_ready = ctx.get("freeze_seal_ready", False) if ctx else False
    feature_factor_engine_final_closed = ctx.get("feature_factor_engine_final_closed", False) if ctx else False
    research_data_only = ctx.get("research_data_only", False) if ctx else False

    activation_allowed = ctx.get("activation_allowed", True) if ctx else True
    strategy_activation_allowed = ctx.get("strategy_activation_allowed", True) if ctx else True
    deployment_allowed = ctx.get("deployment_allowed", True) if ctx else True
    active_paper_enabled = ctx.get("active_paper_enabled", True) if ctx else True
    broker_execution_enabled = ctx.get("broker_execution_enabled", True) if ctx else True
    order_creation_enabled = ctx.get("order_creation_enabled", True) if ctx else True
    paper_state_mutation_enabled = ctx.get("paper_state_mutation_enabled", True) if ctx else True
    telegram_real_send_enabled = ctx.get("telegram_real_send_enabled", True) if ctx else True
    scraping_enabled = ctx.get("scraping_enabled", True) if ctx else True
    html_parse_enabled = ctx.get("html_parse_enabled", True) if ctx else True
    paid_api_enabled = ctx.get("paid_api_enabled", True) if ctx else True
    dashboard_enabled = ctx.get("dashboard_enabled", True) if ctx else True
    network_default_enabled = ctx.get("network_default_enabled", True) if ctx else True
    produces_trade_signal = ctx.get("produces_trade_signal", True) if ctx else True
    produces_order_decision = ctx.get("produces_order_decision", True) if ctx else True
    produces_portfolio_weights = ctx.get("produces_portfolio_weights", True) if ctx else True
    investment_advice = ctx.get("investment_advice", True) if ctx else True

    engine_certificate_ready = cert.get("certificate_valid", False) if cert else False
    phase126_kickoff_gate_ready = gate.get("gate_passed", False) if gate else False

    valid = True

    if not final_artifacts_ready:
        errors.append("final_artifacts_ready is False.")
        valid = False
    if not final_checks_passed:
        errors.append("final_checks_passed is False.")
        valid = False
    if not freeze_seal_ready:
        errors.append("freeze_seal_ready is False.")
        valid = False
    if not engine_certificate_ready:
        errors.append("engine_certificate_ready is False.")
        valid = False
    if not phase126_kickoff_gate_ready:
        errors.append("phase126_kickoff_gate_ready is False.")
        valid = False
    if not feature_factor_engine_final_closed:
        errors.append("feature_factor_engine_final_closed is False.")
        valid = False
    if not ready_for_phase126:
        errors.append("ready_for_phase126 is False.")
        valid = False
    if not research_data_only:
        errors.append("research_data_only is False.")
        valid = False

    # Check activation parameters
    if activation_allowed or strategy_activation_allowed or deployment_allowed or        active_paper_enabled or broker_execution_enabled or order_creation_enabled or        paper_state_mutation_enabled or telegram_real_send_enabled or scraping_enabled or        html_parse_enabled or paid_api_enabled or dashboard_enabled or network_default_enabled or        produces_trade_signal or produces_order_decision or produces_portfolio_weights or investment_advice:
        errors.append("Execution, Activation, Dashboard or Network functions are illegally enabled.")
        valid = False

    return FinalClosureIngestionResult(
        ingestion_id=ingestion_id,
        created_at_utc=created_at_utc,
        source_path=None,
        source_review_id=payload.get("review_id"),
        source_context_id=ctx.get("context_id") if ctx else None,
        available=ctx is not None,
        final_artifacts_ready=final_artifacts_ready,
        final_checks_passed=final_checks_passed,
        freeze_seal_ready=freeze_seal_ready,
        engine_certificate_ready=engine_certificate_ready,
        phase126_kickoff_gate_ready=phase126_kickoff_gate_ready,
        feature_factor_engine_final_closed=feature_factor_engine_final_closed,
        ready_for_phase126=ready_for_phase126,
        metadata_only=True,
        research_data_only=research_data_only,
        activation_allowed=False,
        strategy_activation_allowed=False,
        deployment_allowed=False,
        active_paper_enabled=False,
        broker_execution_enabled=False,
        order_creation_enabled=False,
        paper_state_mutation_enabled=False,
        telegram_real_send_enabled=False,
        scraping_enabled=False,
        html_parse_enabled=False,
        paid_api_enabled=False,
        dashboard_enabled=False,
        network_default_enabled=False,
        produces_trade_signal=False,
        produces_order_decision=False,
        produces_portfolio_weights=False,
        investment_advice=False,
        network_used=False,
        paid_api_used=False,
        scraping_used=False,
        html_parsing_used=False,
        broker_used=False,
        order_created=False,
        paper_state_mutated=False,
        telegram_real_sent=False,
        dashboard_started=False,
        valid_for_phase126=valid,
        risk_flags=risk_flags,
        warnings=warnings,
        errors=errors,
        metadata={"raw_source_keys": list(payload.keys())}
    )

def ingest_latest_final_closure_review_from_store(data_root: Path) -> FinalClosureIngestionResult:
    from usa_signal_bot.feature_engine.final_closure.final_closure_store import get_latest_final_closure_review

    review_path = get_latest_final_closure_review(data_root)
    if not review_path:
        raise FinalClosureIngestionError("No final closure review found in store.")

    try:
        with open(review_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except Exception as e:
        raise FinalClosureIngestionError(f"Error reading final closure review: {e}")

    res = ingest_final_closure_review_payload(payload)
    res.source_path = str(review_path)
    return res

def final_closure_ingestion_to_text(result: FinalClosureIngestionResult) -> str:
    lines = [
        f"Final Closure Ingestion ID: {result.ingestion_id}",
        f"Source Review ID: {result.source_review_id}",
        f"Ready for Phase 126: {result.ready_for_phase126}",
        f"Valid for Phase 126: {result.valid_for_phase126}",
        f"Final Artifacts Ready: {result.final_artifacts_ready}",
        f"Engine Certificate Ready: {result.engine_certificate_ready}",
        f"Phase 126 Kickoff Gate Ready: {result.phase126_kickoff_gate_ready}"
    ]
    if result.errors:
        lines.append("Errors:")
        for err in result.errors:
            lines.append(f"  - {err}")
    if result.warnings:
        lines.append("Warnings:")
        for wrn in result.warnings:
            lines.append(f"  - {wrn}")

    return "\n".join(lines)
