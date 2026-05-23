from typing import Any, Dict, List
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import AdmissionReviewGateStatus, AdmissionReviewRiskFlag
from .admission_review_models import AdmissionReviewGate, create_admission_review_gate_id
from .dry_admission_ingestion import (
    extract_dry_admission_run,
    extract_write_lock_refresh,
    extract_human_approval_ledger
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def gate_dry_admission_completed_no_write(payload: Dict[str, Any]) -> AdmissionReviewGate:
    run = extract_dry_admission_run(payload)
    status = AdmissionReviewGateStatus.PASS if run and run.get("status") in ["COMPLETED_NO_WRITE", "RUN_DRY_ADMISSION_REHEARSAL"] else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="dry_admission_completed_no_write",
        status=status,
        description="Checks if dry admission run completed without writes",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.DRY_ADMISSION_FAILED] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=run.get("status") if run else None,
        expected_value="COMPLETED_NO_WRITE"
    )

def gate_write_lock_refresh_valid(payload: Dict[str, Any]) -> AdmissionReviewGate:
    refresh = extract_write_lock_refresh(payload)
    status = AdmissionReviewGateStatus.PASS if refresh and refresh.get("status") == "VALIDATED" else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="write_lock_refresh_valid",
        status=status,
        description="Checks if write lock refresh is valid",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.WRITE_LOCK_REFRESH_FAILED] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=refresh.get("status") if refresh else None,
        expected_value="VALIDATED"
    )

def gate_human_ledger_present(payload: Dict[str, Any]) -> AdmissionReviewGate:
    ledger = extract_human_approval_ledger(payload)
    status = AdmissionReviewGateStatus.PASS if ledger else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="human_ledger_present",
        status=status,
        description="Checks if human approval ledger is present",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.LEDGER_MISSING] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=ledger is not None,
        expected_value=True
    )

def gate_human_ledger_not_activation(payload: Dict[str, Any]) -> AdmissionReviewGate:
    ledger = extract_human_approval_ledger(payload)
    observed = ledger.get("acknowledged_not_activation", False) if ledger else False
    status = AdmissionReviewGateStatus.PASS if observed else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="human_ledger_not_activation",
        status=status,
        description="Checks if human ledger acknowledges this is not an activation",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=observed,
        expected_value=True
    )

def gate_activation_denied(payload: Dict[str, Any]) -> AdmissionReviewGate:
    observed = payload.get("activation_denied", False)
    status = AdmissionReviewGateStatus.PASS if observed else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="activation_denied",
        status=status,
        description="Checks if activation is denied",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=observed,
        expected_value=True
    )

def gate_activation_allowed_false(payload: Dict[str, Any]) -> AdmissionReviewGate:
    observed = payload.get("activation_allowed", True)
    status = AdmissionReviewGateStatus.PASS if not observed else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="activation_allowed_false",
        status=status,
        description="Checks if activation_allowed is False",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=observed,
        expected_value=False
    )

def gate_all_writes_blocked(payload: Dict[str, Any]) -> AdmissionReviewGate:
    observed = payload.get("all_writes_blocked", False)
    status = AdmissionReviewGateStatus.PASS if observed else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="all_writes_blocked",
        status=status,
        description="Checks if all writes are blocked",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=observed,
        expected_value=True
    )

def gate_mutation_detected_false(payload: Dict[str, Any]) -> AdmissionReviewGate:
    observed = payload.get("mutation_detected", True)
    status = AdmissionReviewGateStatus.PASS if not observed else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="mutation_detected_false",
        status=status,
        description="Checks if mutation is not detected",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=observed,
        expected_value=False
    )

def gate_no_broker_execution(payload: Dict[str, Any]) -> AdmissionReviewGate:
    observed = payload.get("allows_broker_execution", True)
    status = AdmissionReviewGateStatus.PASS if not observed else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="no_broker_execution",
        status=status,
        description="Checks if broker execution is not allowed",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.BROKER_ORDER_RISK] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=observed,
        expected_value=False
    )

def gate_no_telegram_real_send(payload: Dict[str, Any]) -> AdmissionReviewGate:
    observed = payload.get("allows_telegram_real_send", True)
    status = AdmissionReviewGateStatus.PASS if not observed else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="no_telegram_real_send",
        status=status,
        description="Checks if Telegram real send is not allowed",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=observed,
        expected_value=False
    )

def gate_no_config_patch(payload: Dict[str, Any]) -> AdmissionReviewGate:
    observed = payload.get("allows_config_patch", True)
    status = AdmissionReviewGateStatus.PASS if not observed else AdmissionReviewGateStatus.FAIL
    return AdmissionReviewGate(
        gate_id=create_admission_review_gate_id(),
        created_at_utc=_now(),
        gate_name="no_config_patch",
        status=status,
        description="Checks if config patch is not allowed",
        required=True,
        risk_flags=[AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK] if status == AdmissionReviewGateStatus.FAIL else [],
        warnings=[],
        errors=[],
        observed_value=observed,
        expected_value=False
    )

def default_admission_review_gates(payload: Dict[str, Any]) -> List[AdmissionReviewGate]:
    return [
        gate_dry_admission_completed_no_write(payload),
        gate_write_lock_refresh_valid(payload),
        gate_human_ledger_present(payload),
        gate_human_ledger_not_activation(payload),
        gate_activation_denied(payload),
        gate_activation_allowed_false(payload),
        gate_all_writes_blocked(payload),
        gate_mutation_detected_false(payload),
        gate_no_broker_execution(payload),
        gate_no_telegram_real_send(payload),
        gate_no_config_patch(payload)
    ]

def admission_gates_to_text(gates: List[AdmissionReviewGate], limit: int = 100) -> str:
    return json.dumps([g.__dict__ for g in gates[:limit]], indent=2)
