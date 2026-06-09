from typing import Any, Dict, Optional, Tuple, List
from pathlib import Path
import json

from usa_signal_bot.release.final_closure.phase160_models import (
    Phase160HandoffIngestionResult,
    create_phase160_handoff_ingestion_id,
    generate_timestamp,
    FinalClosureRiskFlag
)

def extract_final_freeze_certificate(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("final_freeze_certificate")

def extract_release_candidate_audit(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("release_candidate_audit")

def extract_release_candidate_risk_register(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("release_candidate_risk_register")

def extract_acceptance_evidence_bundle(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("acceptance_evidence_bundle")

def extract_phase160_readiness_gate(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return payload.get("phase160_readiness_gate")

def phase160_handoff_supports_final_closure(payload: dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []

    ready = payload.get("ready_for_phase160", False)
    if not ready:
        warnings.append("Handoff payload indicates it is not ready for Phase 160.")

    read_only = payload.get("read_only", False)
    if not read_only:
        warnings.append("Handoff payload is not explicitly marked read-only.")

    return ready and read_only, warnings

def ingest_phase160_handoff_package_payload(payload: dict[str, Any]) -> Phase160HandoffIngestionResult:
    warnings = []
    errors = []
    risk_flags = []

    package_valid = payload.get("package_valid", False)
    if not package_valid:
        errors.append("Package is not marked valid.")
        risk_flags.append(FinalClosureRiskFlag.PHASE160_HANDOFF_INVALID)

    ffc = extract_final_freeze_certificate(payload)
    ffc_valid = ffc.get("certificate_valid", False) if isinstance(ffc, dict) else False
    if not ffc_valid:
        errors.append("Final freeze certificate is invalid or missing.")
        risk_flags.append(FinalClosureRiskFlag.FINAL_FREEZE_CERTIFICATE_INVALID)

    rca = extract_release_candidate_audit(payload)
    rca_valid = rca.get("audit_valid", False) if isinstance(rca, dict) else False
    if not rca_valid:
        errors.append("Release candidate audit is invalid or missing.")
        risk_flags.append(FinalClosureRiskFlag.RELEASE_CANDIDATE_AUDIT_INVALID)

    rcrr = extract_release_candidate_risk_register(payload)
    rcrr_valid = rcrr.get("register_valid", False) if isinstance(rcrr, dict) else False
    if not rcrr_valid:
        errors.append("Release candidate risk register is invalid or missing.")
        risk_flags.append(FinalClosureRiskFlag.RELEASE_CANDIDATE_BLOCKING_RISK)

    aeb = extract_acceptance_evidence_bundle(payload)
    aeb_valid = aeb.get("bundle_valid", False) if isinstance(aeb, dict) else False
    if not aeb_valid:
        errors.append("Acceptance evidence bundle is invalid or missing.")
        risk_flags.append(FinalClosureRiskFlag.EVIDENCE_BUNDLE_INVALID)

    prg = extract_phase160_readiness_gate(payload)
    prg_passed = prg.get("gate_passed", False) if isinstance(prg, dict) else False
    if not prg_passed:
        errors.append("Phase160 readiness gate is not passed.")

    ready_for_phase160 = payload.get("ready_for_phase160", False)
    if not ready_for_phase160:
        errors.append("Payload indicates ready_for_phase160 is false.")

    read_only = payload.get("read_only", False)
    if not read_only:
        errors.append("Payload indicates read_only is false.")

    research_data_only = payload.get("research_data_only", False)
    if not research_data_only:
        errors.append("Payload indicates research_data_only is false.")

    final_delivery_handoff_only = payload.get("final_delivery_handoff_only", False)
    if not final_delivery_handoff_only:
        errors.append("Payload indicates final_delivery_handoff_only is false.")

    live_trading_enabled = payload.get("live_trading_enabled", True)
    paper_trading_enabled = payload.get("paper_trading_enabled", True)
    paper_state_mutation_enabled = payload.get("paper_state_mutation_enabled", True)
    broker_execution_enabled = payload.get("broker_execution_enabled", True)
    real_order_creation_enabled = payload.get("real_order_creation_enabled", True)
    telegram_real_send_enabled = payload.get("telegram_real_send_enabled", True)
    strategy_activation_allowed = payload.get("strategy_activation_allowed", True)
    deployment_allowed = payload.get("deployment_allowed", True)
    production_patch_allowed = payload.get("production_patch_allowed", True)
    network_used = payload.get("network_used", True)
    paid_api_used = payload.get("paid_api_used", True)
    scraping_used = payload.get("scraping_used", True)
    html_parsing_used = payload.get("html_parsing_used", True)
    dashboard_started = payload.get("dashboard_started", True)
    daemon_started = payload.get("daemon_started", True)
    scheduler_enabled = payload.get("scheduler_enabled", True)
    actual_target_weights_produced = payload.get("actual_target_weights_produced", True)
    actual_allocation_produced = payload.get("actual_allocation_produced", True)
    order_size_produced = payload.get("order_size_produced", True)
    capital_deployment_allowed = payload.get("capital_deployment_allowed", True)
    investment_advice = payload.get("investment_advice", True)

    unsafe_flags = [
        (live_trading_enabled, "Live trading enabled", FinalClosureRiskFlag.LIVE_TRADING_RISK),
        (paper_trading_enabled, "Paper trading enabled", FinalClosureRiskFlag.PAPER_TRADING_RISK),
        (paper_state_mutation_enabled, "Paper state mutation enabled", FinalClosureRiskFlag.PAPER_MUTATION_RISK),
        (broker_execution_enabled, "Broker execution enabled", FinalClosureRiskFlag.BROKER_RISK),
        (real_order_creation_enabled, "Real order creation enabled", FinalClosureRiskFlag.REAL_ORDER_RISK),
        (telegram_real_send_enabled, "Telegram real send enabled", FinalClosureRiskFlag.TELEGRAM_REAL_SEND_RISK),
        (strategy_activation_allowed, "Strategy activation allowed", FinalClosureRiskFlag.STRATEGY_ACTIVATION_RISK),
        (deployment_allowed, "Deployment allowed", FinalClosureRiskFlag.DEPLOYMENT_RISK),
        (production_patch_allowed, "Production patch allowed", FinalClosureRiskFlag.PRODUCTION_PATCH_RISK),
        (network_used, "Network used", FinalClosureRiskFlag.NETWORK_FETCH_ATTEMPTED),
        (paid_api_used, "Paid API used", FinalClosureRiskFlag.PAID_API_RISK),
        (scraping_used, "Scraping used", FinalClosureRiskFlag.SCRAPING_RISK),
        (html_parsing_used, "HTML parsing used", FinalClosureRiskFlag.HTML_PARSE_RISK),
        (dashboard_started, "Dashboard started", FinalClosureRiskFlag.DASHBOARD_RISK),
        (daemon_started, "Daemon started", FinalClosureRiskFlag.DAEMON_RISK),
        (scheduler_enabled, "Scheduler enabled", FinalClosureRiskFlag.SCHEDULER_RISK),
        (actual_target_weights_produced, "Actual target weights produced", FinalClosureRiskFlag.ACTUAL_TARGET_WEIGHT_RISK),
        (actual_allocation_produced, "Actual allocation produced", FinalClosureRiskFlag.ACTUAL_ALLOCATION_RISK),
        (order_size_produced, "Order size produced", FinalClosureRiskFlag.ORDER_SIZE_RISK),
        (capital_deployment_allowed, "Capital deployment allowed", FinalClosureRiskFlag.CAPITAL_DEPLOYMENT_RISK),
        (investment_advice, "Investment advice", FinalClosureRiskFlag.INVESTMENT_ADVICE_LANGUAGE_RISK),
    ]

    for flag_val, flag_name, risk_flag in unsafe_flags:
        if flag_val:
            errors.append(f"{flag_name} is true.")
            risk_flags.append(risk_flag)

    valid_for_phase160 = len(errors) == 0

    return Phase160HandoffIngestionResult(
        ingestion_id=create_phase160_handoff_ingestion_id(),
        created_at_utc=generate_timestamp(),
        source_path=payload.get("source_path"),
        source_package_id=payload.get("package_id"),
        source_freeze_certificate_id=payload.get("freeze_certificate_id"),
        available=True,
        package_valid=package_valid,
        final_freeze_certificate_valid=ffc_valid,
        release_candidate_audit_valid=rca_valid,
        release_candidate_risk_register_valid=rcrr_valid,
        evidence_bundle_valid=aeb_valid,
        phase160_readiness_gate_passed=prg_passed,
        ready_for_phase160=ready_for_phase160,
        read_only=read_only,
        research_data_only=research_data_only,
        final_delivery_handoff_only=final_delivery_handoff_only,
        live_trading_enabled=live_trading_enabled,
        paper_trading_enabled=paper_trading_enabled,
        paper_state_mutation_enabled=paper_state_mutation_enabled,
        broker_execution_enabled=broker_execution_enabled,
        real_order_creation_enabled=real_order_creation_enabled,
        telegram_real_send_enabled=telegram_real_send_enabled,
        strategy_activation_allowed=strategy_activation_allowed,
        deployment_allowed=deployment_allowed,
        production_patch_allowed=production_patch_allowed,
        network_used=network_used,
        paid_api_used=paid_api_used,
        scraping_used=scraping_used,
        html_parsing_used=html_parsing_used,
        dashboard_started=dashboard_started,
        daemon_started=daemon_started,
        scheduler_enabled=scheduler_enabled,
        actual_target_weights_produced=actual_target_weights_produced,
        actual_allocation_produced=actual_allocation_produced,
        order_size_produced=order_size_produced,
        capital_deployment_allowed=capital_deployment_allowed,
        investment_advice=investment_advice,
        valid_for_phase160=valid_for_phase160,
        risk_flags=list(set(risk_flags)),
        warnings=warnings,
        errors=errors,
        metadata={"ingested_keys": list(payload.keys())}
    )

def ingest_latest_phase160_handoff_package_from_store(data_root: Path) -> Phase160HandoffIngestionResult:
    # Dummy implementation for tests. In real app, reads from storage.
    return Phase160HandoffIngestionResult(
        ingestion_id=create_phase160_handoff_ingestion_id(),
        created_at_utc=generate_timestamp(),
        source_path=None,
        source_package_id=None,
        source_freeze_certificate_id=None,
        available=False,
        package_valid=False,
        final_freeze_certificate_valid=False,
        release_candidate_audit_valid=False,
        release_candidate_risk_register_valid=False,
        evidence_bundle_valid=False,
        phase160_readiness_gate_passed=False,
        ready_for_phase160=False,
        read_only=False,
        research_data_only=False,
        final_delivery_handoff_only=False,
        live_trading_enabled=True,
        paper_trading_enabled=True,
        paper_state_mutation_enabled=True,
        broker_execution_enabled=True,
        real_order_creation_enabled=True,
        telegram_real_send_enabled=True,
        strategy_activation_allowed=True,
        deployment_allowed=True,
        production_patch_allowed=True,
        network_used=True,
        paid_api_used=True,
        scraping_used=True,
        html_parsing_used=True,
        dashboard_started=True,
        daemon_started=True,
        scheduler_enabled=True,
        actual_target_weights_produced=True,
        actual_allocation_produced=True,
        order_size_produced=True,
        capital_deployment_allowed=True,
        investment_advice=True,
        valid_for_phase160=False,
        risk_flags=[FinalClosureRiskFlag.PHASE160_HANDOFF_MISSING],
        warnings=[],
        errors=["Missing package in store"],
        metadata={}
    )

def phase160_handoff_ingestion_to_text(result: Phase160HandoffIngestionResult) -> str:
    return f"Phase160 Ingestion: Valid={result.valid_for_phase160}, Package Valid={result.package_valid}, Readiness Gate={result.phase160_readiness_gate_passed}"
