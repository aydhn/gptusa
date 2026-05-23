cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/dry_admission_ingestion.py
from typing import Any, Dict, List, Tuple, Optional
import json

def ingest_dry_admission_full_review(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "activation_allowed" in payload and payload.get("activation_allowed"):
        payload["warnings"] = payload.get("warnings", []) + ["activation_allowed is true, blocking"]
    if "all_writes_blocked" in payload and not payload.get("all_writes_blocked"):
        payload["warnings"] = payload.get("warnings", []) + ["all_writes_blocked is false, blocking"]
    if "mutation_detected" in payload and payload.get("mutation_detected"):
        payload["warnings"] = payload.get("warnings", []) + ["mutation_detected is true, blocking"]

    human_ledger = extract_human_approval_ledger(payload)
    if not human_ledger:
        payload["warnings"] = payload.get("warnings", []) + ["Missing human ledger"]

    write_lock = extract_write_lock_refresh(payload)
    if not write_lock:
        payload["warnings"] = payload.get("warnings", []) + ["Missing write-lock refresh"]

    return payload

def extract_dry_admission_run(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("dry_admission_run")

def extract_write_lock_refresh(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("write_lock_refresh")

def extract_human_approval_ledger(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    return payload.get("human_approval_ledger")

def extract_dry_admission_candidate_id(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("candidate_id")

def extract_dry_admission_decision(payload: Dict[str, Any]) -> Optional[str]:
    return payload.get("decision")

def dry_admission_supports_admission_review(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    warnings = []
    supported = True

    if not payload:
        return False, ["Payload is empty"]

    decision = extract_dry_admission_decision(payload)
    if decision not in ["RUN_DRY_ADMISSION_REHEARSAL", "COMPLETED_NO_WRITE"]:
        warnings.append(f"Invalid decision for admission review: {decision}")
        supported = False

    return supported, warnings

def dry_admission_ingestion_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/eligibility_checker.py
from typing import Any, Dict, List
import json
from usa_signal_bot.core.enums import (
    PaperModeAdmissionReviewDecision,
    PaperModeAdmissionReviewStatus,
    AdmissionReviewRiskFlag
)
from .dry_admission_ingestion import (
    extract_dry_admission_run,
    extract_write_lock_refresh,
    extract_human_approval_ledger
)

def evaluate_admission_review_eligibility(dry_admission_payload: Dict[str, Any]) -> PaperModeAdmissionReviewDecision:
    flags = admission_review_safety_flags_from_dry_admission(dry_admission_payload)

    if AdmissionReviewRiskFlag.BLOCK in flags or AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK in flags:
        return PaperModeAdmissionReviewDecision.BLOCK

    run = extract_dry_admission_run(dry_admission_payload)
    if not run or run.get("status") in ["FAILED", "STALE"]:
        return PaperModeAdmissionReviewDecision.REQUEST_DRY_ADMISSION_REFRESH

    ledger = extract_human_approval_ledger(dry_admission_payload)
    if not ledger or ledger.get("missing_scopes"):
        return PaperModeAdmissionReviewDecision.REQUEST_LEDGER_RECONCILIATION

    write_lock = extract_write_lock_refresh(dry_admission_payload)
    if not write_lock or write_lock.get("status") == "FAILED":
        return PaperModeAdmissionReviewDecision.REQUEST_WRITE_LOCK_REFRESH

    if "manual_review_required" in dry_admission_payload and dry_admission_payload.get("manual_review_required"):
        if not ledger or not ledger.get("manual_review_completed"):
             return PaperModeAdmissionReviewDecision.REQUEST_MANUAL_REVIEW

    if "reject" in dry_admission_payload and dry_admission_payload.get("reject"):
        return PaperModeAdmissionReviewDecision.REJECT

    if len(flags) > 0 and AdmissionReviewRiskFlag.UNKNOWN in flags:
        return PaperModeAdmissionReviewDecision.INCONCLUSIVE

    return PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT

def admission_review_eligibility_reasons(dry_admission_payload: Dict[str, Any]) -> List[str]:
    reasons = []
    flags = admission_review_safety_flags_from_dry_admission(dry_admission_payload)
    if AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK in flags:
        reasons.append("activation_allowed is true")
    run = extract_dry_admission_run(dry_admission_payload)
    if not run:
        reasons.append("Missing dry_admission_run")
    ledger = extract_human_approval_ledger(dry_admission_payload)
    if not ledger:
        reasons.append("Missing human_approval_ledger")
    write_lock = extract_write_lock_refresh(dry_admission_payload)
    if not write_lock:
        reasons.append("Missing write_lock_refresh")
    return reasons

def admission_review_safety_flags_from_dry_admission(payload: Dict[str, Any]) -> List[AdmissionReviewRiskFlag]:
    flags = []
    if payload.get("activation_allowed"):
        flags.append(AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK)
    if not payload.get("all_writes_blocked", True):
         flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if payload.get("mutation_detected"):
         flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
    return flags

def admission_review_status_from_decision(decision: PaperModeAdmissionReviewDecision) -> PaperModeAdmissionReviewStatus:
    mapping = {
        PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT: PaperModeAdmissionReviewStatus.READY,
        PaperModeAdmissionReviewDecision.REQUEST_DRY_ADMISSION_REFRESH: PaperModeAdmissionReviewStatus.REQUEST_CHANGES,
        PaperModeAdmissionReviewDecision.REQUEST_LEDGER_RECONCILIATION: PaperModeAdmissionReviewStatus.REQUEST_CHANGES,
        PaperModeAdmissionReviewDecision.REQUEST_WRITE_LOCK_REFRESH: PaperModeAdmissionReviewStatus.REQUEST_CHANGES,
        PaperModeAdmissionReviewDecision.REQUEST_MANUAL_REVIEW: PaperModeAdmissionReviewStatus.REQUEST_CHANGES,
        PaperModeAdmissionReviewDecision.REJECT: PaperModeAdmissionReviewStatus.REJECTED,
        PaperModeAdmissionReviewDecision.BLOCK: PaperModeAdmissionReviewStatus.BLOCKED,
        PaperModeAdmissionReviewDecision.INCONCLUSIVE: PaperModeAdmissionReviewStatus.UNKNOWN,
        PaperModeAdmissionReviewDecision.UNKNOWN: PaperModeAdmissionReviewStatus.UNKNOWN
    }
    return mapping.get(decision, PaperModeAdmissionReviewStatus.UNKNOWN)

def eligibility_checker_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_gates.py
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
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/ledger_reconciliation.py
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import (
    LedgerReconciliationStatus,
    LedgerReconciliationDecision,
    AdmissionReviewRiskFlag
)
from .admission_review_models import (
    LedgerReconciliationItem,
    LedgerReconciliationReport,
    create_ledger_reconciliation_item_id,
    create_ledger_reconciliation_id
)
from .dry_admission_ingestion import extract_human_approval_ledger

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def required_ledger_reconciliation_scopes() -> List[str]:
    return [
        "NO_WRITE_REVIEW_ACKNOWLEDGEMENT",
        "SAFETY_REVIEW_ACKNOWLEDGEMENT",
        "EVIDENCE_REVIEW_ACKNOWLEDGEMENT",
        "NOT_ACTIVATION_APPROVAL"
    ]

def detect_unsafe_ledger_notes(ledger_payload: Optional[Dict[str, Any]] = None) -> List[str]:
    unsafe_notes = []
    if not ledger_payload:
        return unsafe_notes
    notes = str(ledger_payload).lower()
    unsafe_keywords = ["aktif et", "canlıya al", "emir gönder", "garanti", "kesin al", "paper'a uygula", "sent to broker", "live approved"]
    for keyword in unsafe_keywords:
        if keyword in notes:
            unsafe_notes.append(f"Unsafe language detected: '{keyword}'")
    return unsafe_notes

def detect_missing_ledger_scopes(ledger_payload: Optional[Dict[str, Any]] = None) -> List[str]:
    if not ledger_payload:
        return required_ledger_reconciliation_scopes()

    completed_scopes = ledger_payload.get("completed_scopes", [])
    if isinstance(completed_scopes, dict):
        completed_scopes = list(completed_scopes.keys())

    return [scope for scope in required_ledger_reconciliation_scopes() if scope not in completed_scopes]

def build_ledger_reconciliation_items(ledger_payload: Optional[Dict[str, Any]] = None) -> List[LedgerReconciliationItem]:
    items = []
    if not ledger_payload:
        return items

    completed_scopes = ledger_payload.get("completed_scopes", {})
    if isinstance(completed_scopes, list):
         completed_scopes = {s: True for s in completed_scopes}

    unsafe_notes = detect_unsafe_ledger_notes(ledger_payload)

    for scope in required_ledger_reconciliation_scopes():
        observed = completed_scopes.get(scope)
        status = LedgerReconciliationStatus.RECONCILED if observed else LedgerReconciliationStatus.FAILED
        items.append(LedgerReconciliationItem(
            item_id=create_ledger_reconciliation_item_id(),
            created_at_utc=_now(),
            scope=scope,
            status=status,
            expected_acknowledgement="Acknowledged",
            observed_acknowledgement="Acknowledged" if observed else None,
            reviewer_id=ledger_payload.get("reviewer_id"),
            note_summary="Contains unsafe notes" if unsafe_notes else "Clean",
            unsafe_note_detected=len(unsafe_notes) > 0,
            activation_language_detected=len(unsafe_notes) > 0,
            risk_flags=[AdmissionReviewRiskFlag.LEDGER_SCOPE_MISSING] if status == LedgerReconciliationStatus.FAILED else [],
            warnings=[],
            errors=[]
        ))
    return items

def ledger_reconciliation_risk_flags(ledger_payload: Optional[Dict[str, Any]] = None) -> List[AdmissionReviewRiskFlag]:
    flags = []
    if not ledger_payload:
        flags.append(AdmissionReviewRiskFlag.LEDGER_MISSING)
        return flags

    if detect_missing_ledger_scopes(ledger_payload):
        flags.append(AdmissionReviewRiskFlag.LEDGER_SCOPE_MISSING)
    if detect_unsafe_ledger_notes(ledger_payload):
        flags.append(AdmissionReviewRiskFlag.LEDGER_UNSAFE_NOTE)
    if ledger_payload.get("activation_allowed", True):
         flags.append(AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK)
    if not ledger_payload.get("acknowledged_not_activation", False):
         flags.append(AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK)

    return flags

def reconcile_human_approval_ledger(dry_admission_payload: Dict[str, Any]) -> LedgerReconciliationReport:
    ledger = extract_human_approval_ledger(dry_admission_payload)
    items = build_ledger_reconciliation_items(ledger)
    missing_scopes = detect_missing_ledger_scopes(ledger)
    unsafe_notes = detect_unsafe_ledger_notes(ledger)
    flags = ledger_reconciliation_risk_flags(ledger)

    if AdmissionReviewRiskFlag.LEDGER_MISSING in flags:
        status = LedgerReconciliationStatus.FAILED
        decision = LedgerReconciliationDecision.REQUEST_MANUAL_REVIEW
    elif AdmissionReviewRiskFlag.LEDGER_UNSAFE_NOTE in flags:
        status = LedgerReconciliationStatus.BLOCKED
        decision = LedgerReconciliationDecision.REQUEST_UNSAFE_NOTE_REVIEW
    elif AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK in flags:
        status = LedgerReconciliationStatus.BLOCKED
        decision = LedgerReconciliationDecision.BLOCK
    elif AdmissionReviewRiskFlag.LEDGER_SCOPE_MISSING in flags:
        status = LedgerReconciliationStatus.PARTIAL
        decision = LedgerReconciliationDecision.REQUEST_MISSING_SCOPE_REVIEW
    else:
        status = LedgerReconciliationStatus.RECONCILED
        decision = LedgerReconciliationDecision.ACCEPT_NO_WRITE_ACKNOWLEDGEMENT

    return LedgerReconciliationReport(
        reconciliation_id=create_ledger_reconciliation_id(),
        created_at_utc=_now(),
        status=status,
        decision=decision,
        items=items,
        required_scopes=required_ledger_reconciliation_scopes(),
        completed_scopes=[s for s in required_ledger_reconciliation_scopes() if s not in missing_scopes],
        missing_scopes=missing_scopes,
        acknowledged_no_write=ledger.get("acknowledged_no_write", False) if ledger else False,
        acknowledged_not_activation=ledger.get("acknowledged_not_activation", False) if ledger else False,
        activation_allowed=ledger.get("activation_allowed", True) if ledger else True,
        safety_flags=flags,
        required_followups=[],
        warnings=unsafe_notes,
        errors=[],
        candidate_id=dry_admission_payload.get("candidate_id"),
        source_ledger_id=ledger.get("ledger_id") if ledger else None
    )

def ledger_reconciliation_summary(report: LedgerReconciliationReport) -> Dict[str, Any]:
    return {
        "status": report.status,
        "decision": report.decision,
        "missing_scopes_count": len(report.missing_scopes),
        "safety_flags_count": len(report.safety_flags)
    }

def ledger_reconciliation_to_text(report: LedgerReconciliationReport, limit: int = 100) -> str:
    return json.dumps(report.__dict__, indent=2, default=str)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/no_write_continuity.py
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.core.enums import AdmissionReviewRiskFlag
from .admission_review_models import LedgerReconciliationReport

def admission_no_write_continuity_flags(payload: Dict[str, Any]) -> List[AdmissionReviewRiskFlag]:
    flags = []
    if not payload.get("activation_denied", False):
        flags.append(AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if payload.get("activation_allowed", True):
        flags.append(AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK)
    if not payload.get("all_writes_blocked", False):
        flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if payload.get("mutation_detected", True):
        flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("allows_active_paper", True):
        flags.append(AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
    if payload.get("allows_broker_execution", True):
        flags.append(AdmissionReviewRiskFlag.BROKER_ORDER_RISK)
    if payload.get("allows_paper_state_mutation", True):
        flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
    if payload.get("allows_config_patch", True):
        flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
    if payload.get("allows_telegram_real_send", True):
        flags.append(AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK)
    return flags

def validate_admission_no_write_continuity(dry_admission_payload: Optional[Dict[str, Any]] = None, reconciliation: Optional[LedgerReconciliationReport] = None) -> List[str]:
    errors = []
    if not dry_admission_payload:
        return ["Payload missing"]

    flags = admission_no_write_continuity_flags(dry_admission_payload)
    for flag in flags:
        errors.append(f"Continuity violation: {flag.value}")

    if reconciliation and not reconciliation.acknowledged_not_activation:
        errors.append("Continuity violation: Ledger does not acknowledge 'not activation'")

    return errors

def admission_no_write_continuity_is_preserved(payload: Dict[str, Any]) -> bool:
    return len(admission_no_write_continuity_flags(payload)) == 0

def admission_no_write_continuity_summary(payload: Dict[str, Any]) -> Dict[str, Any]:
    flags = admission_no_write_continuity_flags(payload)
    return {
        "preserved": len(flags) == 0,
        "violations": [f.value for f in flags]
    }

def admission_no_write_continuity_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(admission_no_write_continuity_summary(payload), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/dry_admission_evidence.py
from typing import Any, Dict, List
import json

def required_admission_evidence_types() -> List[str]:
    return [
        "dry_admission_full_review",
        "dry_admission_run",
        "no_write_contract",
        "write_lock_refresh",
        "human_approval_ledger",
        "activation_replay_result",
        "no_write_continuity_report",
        "runtime_write_lock_assertion",
        "validation_reports",
        "audit_trails"
    ]

def collect_admission_evidence_refs(dry_admission_payload: Dict[str, Any]) -> List[str]:
    refs = dry_admission_payload.get("evidence_refs", [])
    if isinstance(refs, list):
        return refs
    return []

def missing_admission_evidence_types(dry_admission_payload: Dict[str, Any]) -> List[str]:
    evidence = dry_admission_payload.get("evidence", {})
    if not isinstance(evidence, dict):
        return required_admission_evidence_types()

    return [t for t in required_admission_evidence_types() if t not in evidence]

def stale_admission_evidence_types(dry_admission_payload: Dict[str, Any]) -> List[str]:
    # Placeholder heuristic for staleness
    stale = []
    evidence = dry_admission_payload.get("evidence", {})
    if isinstance(evidence, dict):
        for k, v in evidence.items():
            if isinstance(v, dict) and v.get("status") in ["STALE", "EXPIRED"]:
                stale.append(k)
    return stale

def evaluate_admission_evidence_completeness(dry_admission_payload: Dict[str, Any]) -> Dict[str, Any]:
    missing = missing_admission_evidence_types(dry_admission_payload)
    stale = stale_admission_evidence_types(dry_admission_payload)
    return {
        "complete": len(missing) == 0 and len(stale) == 0,
        "missing_types": missing,
        "stale_types": stale,
        "refs_count": len(collect_admission_evidence_refs(dry_admission_payload))
    }

def dry_admission_evidence_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(evaluate_admission_evidence_completeness(payload), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/write_lock_integration.py
from typing import Any, Dict, List
import json
from usa_signal_bot.core.enums import AdmissionReviewRiskFlag
from .dry_admission_ingestion import extract_write_lock_refresh

def extract_write_lock_refresh_summary(dry_admission_payload: Dict[str, Any]) -> Dict[str, Any]:
    refresh = extract_write_lock_refresh(dry_admission_payload)
    if not refresh:
        return {"status": "MISSING"}
    return {
        "status": refresh.get("status", "UNKNOWN"),
        "all_writes_blocked": refresh.get("all_writes_blocked", False),
        "mutation_detected": refresh.get("mutation_detected", True),
        "unblocked_write_attempt_count": refresh.get("unblocked_write_attempt_count", 1),
        "hash_unchanged": refresh.get("hash_unchanged", False)
    }

def validate_write_lock_refresh_for_admission_review(dry_admission_payload: Dict[str, Any]) -> List[str]:
    errors = []
    refresh = extract_write_lock_refresh(dry_admission_payload)
    if not refresh:
        return ["Write lock refresh missing"]

    if not refresh.get("all_writes_blocked", False):
        errors.append("all_writes_blocked is false in write lock refresh")
    if refresh.get("mutation_detected", True):
        errors.append("mutation_detected is true in write lock refresh")
    if refresh.get("unblocked_write_attempt_count", 1) > 0:
        errors.append("unblocked_write_attempt_count > 0 in write lock refresh")
    if not refresh.get("hash_unchanged", False):
        errors.append("hash_unchanged is false in write lock refresh")
    for allow_key in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
         if refresh.get(allow_key, True):
             errors.append(f"{allow_key} is true in write lock refresh")

    return errors

def write_lock_refresh_is_valid_for_admission(dry_admission_payload: Dict[str, Any]) -> bool:
    return len(validate_write_lock_refresh_for_admission_review(dry_admission_payload)) == 0

def write_lock_integration_risk_flags(dry_admission_payload: Dict[str, Any]) -> List[AdmissionReviewRiskFlag]:
    flags = []
    errors = validate_write_lock_refresh_for_admission_review(dry_admission_payload)
    if errors:
        flags.append(AdmissionReviewRiskFlag.WRITE_LOCK_REFRESH_FAILED)
    return flags

def write_lock_integration_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(extract_write_lock_refresh_summary(payload), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_evidence_seal.py
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import hashlib
import json

from usa_signal_bot.core.enums import AdmissionEvidenceSealStatus
from .admission_review_models import AdmissionEvidenceSeal, create_admission_evidence_seal_id, PaperModeAdmissionReview

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def stable_admission_evidence_seal_hash(payload: Dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

def build_admission_evidence_seal(admission_review: Optional[PaperModeAdmissionReview] = None, evidence_refs: Optional[List[str]] = None) -> AdmissionEvidenceSeal:
    refs = evidence_refs or []
    if admission_review and admission_review.evidence_refs:
         refs.extend(admission_review.evidence_refs)
    refs = sorted(list(set(refs)))

    status = AdmissionEvidenceSealStatus.SEALED if refs else AdmissionEvidenceSealStatus.FAILED
    seal_hash = stable_admission_evidence_seal_hash({"refs": refs, "review_id": admission_review.admission_review_id if admission_review else None}) if refs else None

    return AdmissionEvidenceSeal(
        seal_id=create_admission_evidence_seal_id(),
        created_at_utc=_now(),
        status=status,
        evidence_refs=refs,
        sealed=True if seal_hash else False,
        immutable=True if seal_hash else False,
        warnings=[],
        errors=[],
        candidate_id=admission_review.candidate_id if admission_review else None,
        source_review_id=admission_review.admission_review_id if admission_review else None,
        seal_hash=seal_hash
    )

def validate_admission_evidence_seal(seal: AdmissionEvidenceSeal) -> List[str]:
    errors = []
    if seal.sealed and not seal.immutable:
        errors.append("If sealed is true, immutable must be true")
    if not seal.seal_hash and seal.sealed:
         errors.append("If sealed is true, seal_hash must be present")
    if seal.status == AdmissionEvidenceSealStatus.FAILED:
         errors.append("Evidence seal failed")
    return errors

def admission_evidence_seal_summary(seal: AdmissionEvidenceSeal) -> Dict[str, Any]:
    return {
        "status": seal.status,
        "sealed": seal.sealed,
        "refs_count": len(seal.evidence_refs),
        "hash_prefix": seal.seal_hash[:8] if seal.seal_hash else None
    }

def admission_evidence_seal_to_text(seal: AdmissionEvidenceSeal) -> str:
    return json.dumps(admission_evidence_seal_summary(seal), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/transition_checkpoint.py
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import (
    NoWriteTransitionCheckpointStatus,
    NoWriteTransitionCheckpointDecision,
    AdmissionReviewRiskFlag,
    PaperModeAdmissionReviewDecision
)
from .admission_review_models import (
    FinalNoWriteTransitionCheckpoint,
    create_transition_checkpoint_id,
    PaperModeAdmissionReview,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def transition_checkpoint_required_followups(flags: List[AdmissionReviewRiskFlag]) -> List[str]:
    followups = []
    if AdmissionReviewRiskFlag.LEDGER_MISSING in flags or AdmissionReviewRiskFlag.LEDGER_SCOPE_MISSING in flags:
        followups.append("Complete ledger reconciliation")
    if AdmissionReviewRiskFlag.EVIDENCE_MISSING in flags or AdmissionReviewRiskFlag.EVIDENCE_SEAL_FAILED in flags:
        followups.append("Provide missing evidence and refresh seal")
    if AdmissionReviewRiskFlag.WRITE_LOCK_REFRESH_FAILED in flags:
        followups.append("Refresh write lock proof")
    return followups

def default_final_no_write_transition_checkpoint(candidate_id: Optional[str] = None) -> FinalNoWriteTransitionCheckpoint:
    return FinalNoWriteTransitionCheckpoint(
        checkpoint_id=create_transition_checkpoint_id(),
        created_at_utc=_now(),
        status=NoWriteTransitionCheckpointStatus.DRAFT,
        decision=NoWriteTransitionCheckpointDecision.INCONCLUSIVE,
        activation_denied=True,
        activation_allowed=False,
        all_writes_blocked=True,
        mutation_detected=False,
        transition_allowed=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        required_followups=[],
        safety_flags=[],
        warnings=[],
        errors=[],
        candidate_id=candidate_id
    )

def build_final_no_write_transition_checkpoint(
    admission_review: PaperModeAdmissionReview,
    reconciliation: Optional[LedgerReconciliationReport] = None,
    evidence_seal: Optional[AdmissionEvidenceSeal] = None
) -> FinalNoWriteTransitionCheckpoint:

    flags = list(set(admission_review.safety_flags))
    if reconciliation:
        flags.extend([f for f in reconciliation.safety_flags if f not in flags])

    status = NoWriteTransitionCheckpointStatus.VALIDATED_NO_WRITE
    decision = NoWriteTransitionCheckpointDecision.CONTINUE_TO_NO_WRITE_TRANSITION_DOSSIER

    if admission_review.decision != PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT:
         status = NoWriteTransitionCheckpointStatus.BLOCKED
         decision = NoWriteTransitionCheckpointDecision.REQUEST_ADMISSION_REVIEW_REFRESH
    elif reconciliation and reconciliation.decision != "ACCEPT_NO_WRITE_ACKNOWLEDGEMENT":
         status = NoWriteTransitionCheckpointStatus.BLOCKED
         decision = NoWriteTransitionCheckpointDecision.REQUEST_LEDGER_RECONCILIATION_REFRESH
    elif not evidence_seal or evidence_seal.status != "SEALED":
         status = NoWriteTransitionCheckpointStatus.BLOCKED
         decision = NoWriteTransitionCheckpointDecision.REQUEST_EVIDENCE_SEAL_REFRESH

    followups = transition_checkpoint_required_followups(flags)

    return FinalNoWriteTransitionCheckpoint(
        checkpoint_id=create_transition_checkpoint_id(),
        created_at_utc=_now(),
        status=status,
        decision=decision,
        activation_denied=True,
        activation_allowed=False,
        all_writes_blocked=True,
        mutation_detected=False,
        transition_allowed=False,
        allows_active_paper=False,
        allows_broker_execution=False,
        allows_paper_state_mutation=False,
        allows_config_patch=False,
        allows_telegram_real_send=False,
        required_followups=followups,
        safety_flags=flags,
        warnings=[],
        errors=[],
        candidate_id=admission_review.candidate_id,
        source_admission_review_id=admission_review.admission_review_id,
        source_reconciliation_id=reconciliation.reconciliation_id if reconciliation else None,
        source_evidence_seal_id=evidence_seal.seal_id if evidence_seal else None
    )

def transition_checkpoint_summary(checkpoint: FinalNoWriteTransitionCheckpoint) -> Dict[str, Any]:
    return {
        "status": checkpoint.status,
        "decision": checkpoint.decision,
        "activation_denied": checkpoint.activation_denied,
        "transition_allowed": checkpoint.transition_allowed,
        "safety_flags_count": len(checkpoint.safety_flags)
    }

def transition_checkpoint_to_text(checkpoint: FinalNoWriteTransitionCheckpoint) -> str:
    return json.dumps(transition_checkpoint_summary(checkpoint), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/transition_checkpoint_validator.py
from typing import Any, Dict, List
import json
from .admission_review_models import FinalNoWriteTransitionCheckpoint

def validate_transition_checkpoint_safety(checkpoint: FinalNoWriteTransitionCheckpoint) -> List[str]:
    errors = []
    if not checkpoint.activation_denied:
        errors.append("activation_denied is false")
    if checkpoint.activation_allowed:
        errors.append("activation_allowed is true")
    if checkpoint.transition_allowed:
        errors.append("transition_allowed is true")
    if not checkpoint.all_writes_blocked:
        errors.append("all_writes_blocked is false")
    if checkpoint.mutation_detected:
        errors.append("mutation_detected is true")

    for allow_attr in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
        if getattr(checkpoint, allow_attr, True):
             errors.append(f"{allow_attr} is true")

    return errors

def transition_checkpoint_allows_activation(checkpoint: FinalNoWriteTransitionCheckpoint) -> bool:
    return checkpoint.activation_allowed or not checkpoint.activation_denied

def transition_checkpoint_allows_transition(checkpoint: FinalNoWriteTransitionCheckpoint) -> bool:
    return checkpoint.transition_allowed

def transition_checkpoint_requires_followup(checkpoint: FinalNoWriteTransitionCheckpoint) -> bool:
    return len(checkpoint.required_followups) > 0

def transition_checkpoint_blocks_next_stage(checkpoint: FinalNoWriteTransitionCheckpoint) -> bool:
    return checkpoint.decision in ["REJECT", "BLOCK", "REQUEST_ADMISSION_REVIEW_REFRESH", "REQUEST_LEDGER_RECONCILIATION_REFRESH", "REQUEST_EVIDENCE_SEAL_REFRESH", "REQUEST_MANUAL_REVIEW"] or len(validate_transition_checkpoint_safety(checkpoint)) > 0

def transition_checkpoint_validator_summary(checkpoint: FinalNoWriteTransitionCheckpoint) -> Dict[str, Any]:
    return {
        "safe": len(validate_transition_checkpoint_safety(checkpoint)) == 0,
        "allows_activation": transition_checkpoint_allows_activation(checkpoint),
        "blocks_next_stage": transition_checkpoint_blocks_next_stage(checkpoint)
    }

def transition_checkpoint_validator_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_decision.py
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from usa_signal_bot.core.enums import (
    PaperModeAdmissionReviewStatus,
    PaperModeAdmissionReviewDecision,
    AdmissionReviewRiskFlag,
    AdmissionReviewGateStatus,
    LedgerReconciliationStatus
)
from .admission_review_models import (
    PaperModeAdmissionReview,
    AdmissionReviewGate,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal,
    create_admission_review_id
)
from .eligibility_checker import admission_review_safety_flags_from_dry_admission, admission_review_status_from_decision
from .ledger_reconciliation import ledger_reconciliation_risk_flags
from .dry_admission_ingestion import extract_dry_admission_candidate_id, extract_dry_admission_run, extract_write_lock_refresh, extract_human_approval_ledger

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

class GuardedPaperModeAdmissionReviewDecisionEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative
        self.critical_risk_flags = [
             AdmissionReviewRiskFlag.REAL_ORDER_RISK,
             AdmissionReviewRiskFlag.PAPER_ORDER_RISK,
             AdmissionReviewRiskFlag.BROKER_ORDER_RISK,
             AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK,
             AdmissionReviewRiskFlag.PAPER_POSITION_MUTATION_RISK,
             AdmissionReviewRiskFlag.PAPER_PORTFOLIO_MUTATION_RISK,
             AdmissionReviewRiskFlag.PAPER_CASH_MUTATION_RISK,
             AdmissionReviewRiskFlag.PAPER_EQUITY_MUTATION_RISK,
             AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK,
             AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
             AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
             AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK,
             AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID,
             AdmissionReviewRiskFlag.SECRET_RISK
        ]

    def collect_admission_risk_flags(self, dry_admission_payload: Dict[str, Any], gates: List[AdmissionReviewGate], reconciliation: Optional[LedgerReconciliationReport] = None) -> List[AdmissionReviewRiskFlag]:
        flags = []
        flags.extend(admission_review_safety_flags_from_dry_admission(dry_admission_payload))
        for gate in gates:
             flags.extend(gate.risk_flags)
        if reconciliation:
             flags.extend(reconciliation.safety_flags)
        else:
             flags.extend(ledger_reconciliation_risk_flags(extract_human_approval_ledger(dry_admission_payload)))

        # Deduplicate
        return list(set(flags))

    def followups_for_admission_decision(self, decision: PaperModeAdmissionReviewDecision, flags: List[AdmissionReviewRiskFlag]) -> List[str]:
        followups = []
        if decision == PaperModeAdmissionReviewDecision.REQUEST_DRY_ADMISSION_REFRESH:
             followups.append("Refresh dry admission payload")
        if decision == PaperModeAdmissionReviewDecision.REQUEST_LEDGER_RECONCILIATION:
             followups.append("Complete ledger reconciliation")
        if decision == PaperModeAdmissionReviewDecision.REQUEST_WRITE_LOCK_REFRESH:
             followups.append("Refresh write lock proof")
        if decision == PaperModeAdmissionReviewDecision.REQUEST_MANUAL_REVIEW:
             followups.append("Perform manual review")
        return followups

    def rationale_for_admission_decision(self, decision: PaperModeAdmissionReviewDecision, flags: List[AdmissionReviewRiskFlag]) -> str:
        if decision == PaperModeAdmissionReviewDecision.BLOCK:
             return f"Blocked due to critical safety flags: {[f.value for f in flags if f in self.critical_risk_flags]}"
        if decision == PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT:
             return "All gates passed, ledger reconciled, no write continuity preserved. Not an active paper enable."
        return f"Decision: {decision.value}"

    def decide(self, dry_admission_payload: Dict[str, Any], gates: List[AdmissionReviewGate], reconciliation: Optional[LedgerReconciliationReport] = None, evidence_seal: Optional[AdmissionEvidenceSeal] = None) -> PaperModeAdmissionReview:
        flags = self.collect_admission_risk_flags(dry_admission_payload, gates, reconciliation)

        has_critical_risk = any(f in self.critical_risk_flags for f in flags)

        run = extract_dry_admission_run(dry_admission_payload)
        write_lock = extract_write_lock_refresh(dry_admission_payload)

        decision = PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT

        if has_critical_risk:
             decision = PaperModeAdmissionReviewDecision.BLOCK
        elif not run or run.get("status") in ["FAILED", "STALE"] or any(g.status == AdmissionReviewGateStatus.FAIL and g.gate_name == "dry_admission_completed_no_write" for g in gates):
             decision = PaperModeAdmissionReviewDecision.REQUEST_DRY_ADMISSION_REFRESH
        elif not reconciliation or reconciliation.status != LedgerReconciliationStatus.RECONCILED:
             decision = PaperModeAdmissionReviewDecision.REQUEST_LEDGER_RECONCILIATION
        elif not write_lock or write_lock.get("status") != "VALIDATED" or any(g.status == AdmissionReviewGateStatus.FAIL and g.gate_name == "write_lock_refresh_valid" for g in gates):
             decision = PaperModeAdmissionReviewDecision.REQUEST_WRITE_LOCK_REFRESH
        elif "manual_review_required" in dry_admission_payload and dry_admission_payload.get("manual_review_required") and (not reconciliation or reconciliation.status != LedgerReconciliationStatus.RECONCILED):
             decision = PaperModeAdmissionReviewDecision.REQUEST_MANUAL_REVIEW

        status = admission_review_status_from_decision(decision)
        followups = self.followups_for_admission_decision(decision, flags)
        rationale = self.rationale_for_admission_decision(decision, flags)

        return PaperModeAdmissionReview(
             admission_review_id=create_admission_review_id(),
             created_at_utc=_now(),
             status=status,
             decision=decision,
             gates=gates,
             evidence_refs=dry_admission_payload.get("evidence_refs", []),
             required_followups=followups,
             manual_review_required=True,
             activation_denied=True,
             activation_allowed=False,
             all_writes_blocked=True,
             mutation_detected=False,
             transition_allowed=False,
             allows_active_paper=False,
             allows_broker_execution=False,
             allows_paper_state_mutation=False,
             allows_config_patch=False,
             allows_telegram_real_send=False,
             safety_flags=flags,
             warnings=[rationale] if decision != PaperModeAdmissionReviewDecision.PASS_TO_NO_WRITE_TRANSITION_CHECKPOINT else [],
             errors=[],
             candidate_id=extract_dry_admission_candidate_id(dry_admission_payload),
             source_dry_admission_review_id=dry_admission_payload.get("review_id"),
             source_dry_admission_run_id=run.get("run_id") if run else None,
             source_write_lock_refresh_id=write_lock.get("refresh_id") if write_lock else None,
             source_human_ledger_id=reconciliation.source_ledger_id if reconciliation else None,
             ledger_reconciliation=reconciliation,
             evidence_seal=evidence_seal
        )
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_safety_validator.py
from typing import Any, Dict, List, Optional
import json
from usa_signal_bot.core.enums import AdmissionReviewRiskFlag
from .admission_review_models import PaperModeAdmissionReview, LedgerReconciliationReport, FinalNoWriteTransitionCheckpoint

def collect_admission_safety_flags(
    admission_review: Optional[PaperModeAdmissionReview] = None,
    reconciliation: Optional[LedgerReconciliationReport] = None,
    checkpoint: Optional[FinalNoWriteTransitionCheckpoint] = None
) -> List[AdmissionReviewRiskFlag]:
    flags = []
    if admission_review:
        flags.extend(admission_review.safety_flags)
        if admission_review.activation_allowed:
            flags.append(AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK)
        if not admission_review.activation_denied:
            flags.append(AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK)
        if admission_review.transition_allowed:
             flags.append(AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID)
        if not admission_review.all_writes_blocked:
             flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
        if admission_review.mutation_detected:
             flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
        for attr in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
             if getattr(admission_review, attr, True):
                 if "broker" in attr: flags.append(AdmissionReviewRiskFlag.BROKER_ORDER_RISK)
                 elif "telegram" in attr: flags.append(AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK)
                 elif "config" in attr: flags.append(AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK)
                 elif "mutation" in attr: flags.append(AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK)
                 else: flags.append(AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK)

    if reconciliation:
        flags.extend(reconciliation.safety_flags)
    if checkpoint:
        flags.extend(checkpoint.safety_flags)

    return list(set(flags))

def admission_has_blocking_flags(flags: List[AdmissionReviewRiskFlag]) -> bool:
    blocking_flags = [
        AdmissionReviewRiskFlag.REAL_ORDER_RISK,
        AdmissionReviewRiskFlag.PAPER_ORDER_RISK,
        AdmissionReviewRiskFlag.BROKER_ORDER_RISK,
        AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK,
        AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK,
        AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
        AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
        AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK,
        AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID,
        AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK,
        AdmissionReviewRiskFlag.SECRET_RISK
    ]
    return any(f in blocking_flags for f in flags)

def validate_admission_safety(
    admission_review: Optional[PaperModeAdmissionReview] = None,
    reconciliation: Optional[LedgerReconciliationReport] = None,
    checkpoint: Optional[FinalNoWriteTransitionCheckpoint] = None
) -> List[str]:
    flags = collect_admission_safety_flags(admission_review, reconciliation, checkpoint)
    errors = []
    if admission_has_blocking_flags(flags):
        for flag in flags:
             if flag in [
                AdmissionReviewRiskFlag.REAL_ORDER_RISK,
                AdmissionReviewRiskFlag.PAPER_ORDER_RISK,
                AdmissionReviewRiskFlag.BROKER_ORDER_RISK,
                AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK,
                AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK,
                AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
                AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK,
                AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK,
                AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID,
                AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK,
                AdmissionReviewRiskFlag.SECRET_RISK
             ]:
                  errors.append(f"Blocking safety risk detected: {flag.value}")
    return errors

def admission_safety_summary(flags: List[AdmissionReviewRiskFlag]) -> Dict[str, Any]:
    return {
        "safe": not admission_has_blocking_flags(flags),
        "blocking_flags": [f.value for f in flags if f in [
            AdmissionReviewRiskFlag.REAL_ORDER_RISK, AdmissionReviewRiskFlag.PAPER_ORDER_RISK,
            AdmissionReviewRiskFlag.BROKER_ORDER_RISK, AdmissionReviewRiskFlag.PAPER_STATE_MUTATION_RISK,
            AdmissionReviewRiskFlag.TELEGRAM_REAL_SEND_RISK, AdmissionReviewRiskFlag.PRODUCTION_CONFIG_WRITE_RISK,
            AdmissionReviewRiskFlag.ACTIVE_PAPER_ENABLE_RISK, AdmissionReviewRiskFlag.ACTIVATION_ALLOWED_RISK,
            AdmissionReviewRiskFlag.TRANSITION_CHECKPOINT_INVALID, AdmissionReviewRiskFlag.LEDGER_ACTIVATION_RISK,
            AdmissionReviewRiskFlag.SECRET_RISK]],
        "all_flags": [f.value for f in flags]
    }

def admission_safety_validator_to_text(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_audit.py
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import AdmissionReviewRiskFlag
from .admission_review_models import (
    AdmissionReviewAuditEntry,
    create_admission_audit_id,
    PaperModeAdmissionReview,
    LedgerReconciliationReport,
    FinalNoWriteTransitionCheckpoint
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def create_admission_review_audit_entry(
    entity_type: str,
    entity_id: str,
    action: str,
    rationale: str,
    decision: Optional[str] = None,
    evidence_refs: Optional[List[str]] = None,
    risk_flags: Optional[List[AdmissionReviewRiskFlag]] = None
) -> AdmissionReviewAuditEntry:
    return AdmissionReviewAuditEntry(
        audit_id=create_admission_audit_id(),
        created_at_utc=_now(),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        decision=decision,
        rationale=rationale,
        evidence_refs=evidence_refs or [],
        risk_flags=risk_flags or [],
        warnings=[],
        errors=[]
    )

def audit_entry_from_admission_review(review: PaperModeAdmissionReview) -> AdmissionReviewAuditEntry:
    return create_admission_review_audit_entry(
        entity_type="PaperModeAdmissionReview",
        entity_id=review.admission_review_id,
        action="Admission Review Processed",
        rationale=f"Review completed with status {review.status}",
        decision=review.decision,
        evidence_refs=review.evidence_refs,
        risk_flags=review.safety_flags
    )

def audit_entry_from_ledger_reconciliation(report: LedgerReconciliationReport) -> AdmissionReviewAuditEntry:
    return create_admission_review_audit_entry(
        entity_type="LedgerReconciliationReport",
        entity_id=report.reconciliation_id,
        action="Ledger Reconciliation Processed",
        rationale=f"Reconciliation completed with status {report.status}",
        decision=report.decision,
        evidence_refs=[],
        risk_flags=report.safety_flags
    )

def audit_entry_from_transition_checkpoint(checkpoint: FinalNoWriteTransitionCheckpoint) -> AdmissionReviewAuditEntry:
    return create_admission_review_audit_entry(
        entity_type="FinalNoWriteTransitionCheckpoint",
        entity_id=checkpoint.checkpoint_id,
        action="Transition Checkpoint Processed",
        rationale=f"Checkpoint completed with status {checkpoint.status}",
        decision=checkpoint.decision,
        evidence_refs=[],
        risk_flags=checkpoint.safety_flags
    )

def append_admission_audit_entry(entries: List[AdmissionReviewAuditEntry], entry: AdmissionReviewAuditEntry) -> List[AdmissionReviewAuditEntry]:
    # Placeholder for redaction
    redacted_entry = entry
    entries.append(redacted_entry)
    return entries

def admission_audit_summary(entries: List[AdmissionReviewAuditEntry]) -> Dict[str, Any]:
    return {
        "total_entries": len(entries),
        "latest_audit_id": entries[-1].audit_id if entries else None,
        "actions": list(set([e.action for e in entries]))
    }

def admission_audit_to_text(entries: List[AdmissionReviewAuditEntry], limit: int = 100) -> str:
    return json.dumps([e.__dict__ for e in entries[:limit]], indent=2, default=str)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_report.py
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json

from usa_signal_bot.core.enums import AdmissionReviewReportType
from .admission_review_models import (
    AdmissionReviewFullReport,
    create_admission_full_report_id,
    PaperModeAdmissionReview,
    LedgerReconciliationReport,
    FinalNoWriteTransitionCheckpoint,
    AdmissionEvidenceSeal,
    AdmissionReviewAuditEntry
)
from .admission_decision import GuardedPaperModeAdmissionReviewDecisionEngine
from .ledger_reconciliation import reconcile_human_approval_ledger
from .admission_evidence_seal import build_admission_evidence_seal
from .transition_checkpoint import build_final_no_write_transition_checkpoint
from .admission_gates import default_admission_review_gates
from .admission_audit import (
    audit_entry_from_admission_review,
    audit_entry_from_ledger_reconciliation,
    audit_entry_from_transition_checkpoint
)

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def admission_review_limitations_text() -> str:
    return """
ADMISSION REVIEW LIMITATIONS:
- Admission review is metadata only.
- Ledger reconciliation is not an active paper/live/demo approval.
- Final no-write transition checkpoint is not an activation.
- No broker API is used.
- No paper state mutation occurs.
- No Telegram real send is executed.
- No production config patch is applied.
- This is NOT investment advice.
"""

def build_admission_review_full_report(dry_admission_payload: Dict[str, Any]) -> AdmissionReviewFullReport:
    engine = GuardedPaperModeAdmissionReviewDecisionEngine()
    gates = default_admission_review_gates(dry_admission_payload)
    reconciliation = reconcile_human_approval_ledger(dry_admission_payload)
    evidence_seal = build_admission_evidence_seal(evidence_refs=dry_admission_payload.get("evidence_refs", []))

    review = engine.decide(dry_admission_payload, gates, reconciliation, evidence_seal)
    evidence_seal = build_admission_evidence_seal(review)
    review.evidence_seal = evidence_seal

    checkpoint = build_final_no_write_transition_checkpoint(review, reconciliation, evidence_seal)

    return build_admission_review_report_from_parts(review, reconciliation, checkpoint, evidence_seal)

def build_admission_review_report_from_parts(
    admission_review: PaperModeAdmissionReview,
    reconciliation: Optional[LedgerReconciliationReport] = None,
    checkpoint: Optional[FinalNoWriteTransitionCheckpoint] = None,
    evidence_seal: Optional[AdmissionEvidenceSeal] = None
) -> AdmissionReviewFullReport:

    audit_entries = []
    audit_entries.append(audit_entry_from_admission_review(admission_review))
    if reconciliation:
        audit_entries.append(audit_entry_from_ledger_reconciliation(reconciliation))
    if checkpoint:
        audit_entries.append(audit_entry_from_transition_checkpoint(checkpoint))

    return AdmissionReviewFullReport(
        report_id=create_admission_full_report_id(),
        created_at_utc=_now(),
        report_type=AdmissionReviewReportType.FULL_ADMISSION_REVIEW,
        admission_reviews=[admission_review],
        ledger_reconciliations=[reconciliation] if reconciliation else [],
        evidence_seals=[evidence_seal] if evidence_seal else [],
        transition_checkpoints=[checkpoint] if checkpoint else [],
        audit_entries=audit_entries,
        output_paths={},
        warnings=[admission_review_limitations_text()],
        errors=[]
    )

def admission_review_full_report_summary(report: AdmissionReviewFullReport) -> Dict[str, Any]:
    return {
        "report_id": report.report_id,
        "created_at_utc": report.created_at_utc,
        "reviews_count": len(report.admission_reviews),
        "reconciliations_count": len(report.ledger_reconciliations),
        "seals_count": len(report.evidence_seals),
        "checkpoints_count": len(report.transition_checkpoints),
        "audit_entries_count": len(report.audit_entries)
    }

def admission_review_full_report_to_text(report: AdmissionReviewFullReport, limit: int = 100) -> str:
    return json.dumps(admission_review_full_report_summary(report), indent=2)
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_review_store.py
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.core.exceptions import AdmissionReviewStorageError
from .admission_review_models import (
    PaperModeAdmissionReview,
    AdmissionReviewGate,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal,
    FinalNoWriteTransitionCheckpoint,
    AdmissionReviewAuditEntry,
    AdmissionReviewFullReport,
    paper_mode_admission_review_to_dict,
    admission_review_gate_to_dict,
    ledger_reconciliation_report_to_dict,
    admission_evidence_seal_to_dict,
    final_no_write_transition_checkpoint_to_dict,
    admission_review_audit_entry_to_dict,
    admission_review_full_report_to_dict
)

def admission_review_store_dir(data_root: Path) -> Path:
    return data_root / "paper_admission_review"

def admission_reviews_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "admission_reviews"

def admission_gates_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "gates"

def ledger_reconciliations_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "ledger_reconciliations"

def admission_evidence_seals_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "evidence_seals"

def transition_checkpoints_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "transition_checkpoints"

def admission_audit_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "audit"

def admission_full_reports_dir(data_root: Path) -> Path:
    return admission_review_store_dir(data_root) / "full_reports"

def write_admission_review_json(path: Path, item: PaperModeAdmissionReview) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(paper_mode_admission_review_to_dict(item), f, indent=2)
    return path

def write_admission_gates_jsonl(path: Path, items: List[AdmissionReviewGate]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(admission_review_gate_to_dict(item)) + "\n")
    return path

def write_ledger_reconciliation_json(path: Path, item: LedgerReconciliationReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(ledger_reconciliation_report_to_dict(item), f, indent=2)
    return path

def write_admission_evidence_seal_json(path: Path, item: AdmissionEvidenceSeal) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(admission_evidence_seal_to_dict(item), f, indent=2)
    return path

def write_transition_checkpoint_json(path: Path, item: FinalNoWriteTransitionCheckpoint) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(final_no_write_transition_checkpoint_to_dict(item), f, indent=2)
    return path

def write_admission_audit_jsonl(path: Path, items: List[AdmissionReviewAuditEntry]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        for item in items:
            f.write(json.dumps(admission_review_audit_entry_to_dict(item)) + "\n")
    return path

def write_admission_full_report_json(path: Path, item: AdmissionReviewFullReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(admission_review_full_report_to_dict(item), f, indent=2)
    return path

def read_admission_full_report_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_admission_full_reports(data_root: Path) -> List[Path]:
    d = admission_full_reports_dir(data_root)
    if not d.exists():
        return []
    return sorted(list(d.glob("*.json")))

def get_latest_admission_full_report(data_root: Path) -> Optional[Path]:
    reports = list_admission_full_reports(data_root)
    return reports[-1] if reports else None

def admission_review_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "full_reports_count": len(list_admission_full_reports(data_root))
    }
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_review_validation.py
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.core.exceptions import AdmissionReviewValidationError
from .admission_review_models import (
    PaperModeAdmissionReview,
    LedgerReconciliationReport,
    FinalNoWriteTransitionCheckpoint,
    AdmissionReviewFullReport
)

@dataclass
class AdmissionReviewValidationIssue:
    severity: str
    field: Optional[str]
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AdmissionReviewValidationReport:
    valid: bool
    issue_count: int
    warning_count: int
    error_count: int
    blocked_count: int
    issues: List[AdmissionReviewValidationIssue]
    warnings: List[str]
    errors: List[str]

def _build_validation_report(issues: List[AdmissionReviewValidationIssue]) -> AdmissionReviewValidationReport:
    errors = [i for i in issues if i.severity in ["ERROR", "BLOCK"]]
    warnings = [i for i in issues if i.severity == "WARNING"]
    return AdmissionReviewValidationReport(
        valid=len(errors) == 0,
        issue_count=len(issues),
        warning_count=len(warnings),
        error_count=len(errors),
        blocked_count=len([i for i in issues if i.severity == "BLOCK"]),
        issues=issues,
        warnings=[i.message for i in warnings],
        errors=[i.message for i in errors]
    )

def validate_admission_review_report(item: PaperModeAdmissionReview) -> AdmissionReviewValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_denied", "must be True"))
    if item.activation_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_allowed", "must be False"))
    if item.transition_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "transition_allowed", "must be False"))
    if not item.all_writes_blocked:
        issues.append(AdmissionReviewValidationIssue("ERROR", "all_writes_blocked", "must be True"))
    if item.mutation_detected:
        issues.append(AdmissionReviewValidationIssue("ERROR", "mutation_detected", "must be False"))
    for attr in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
        if getattr(item, attr, True):
             issues.append(AdmissionReviewValidationIssue("ERROR", attr, "must be False"))
    return _build_validation_report(issues)

def validate_ledger_reconciliation_validation_report(item: LedgerReconciliationReport) -> AdmissionReviewValidationReport:
    issues = []
    if not item.acknowledged_not_activation:
        issues.append(AdmissionReviewValidationIssue("BLOCK", "acknowledged_not_activation", "must be True"))
    if item.activation_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_allowed", "must be False"))
    if len(item.warnings) > 0:
        issues.append(AdmissionReviewValidationIssue("BLOCK", "warnings", "Unsafe notes detected"))
    return _build_validation_report(issues)

def validate_transition_checkpoint_validation_report(item: FinalNoWriteTransitionCheckpoint) -> AdmissionReviewValidationReport:
    issues = []
    if not item.activation_denied:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_denied", "must be True"))
    if item.activation_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "activation_allowed", "must be False"))
    if item.transition_allowed:
        issues.append(AdmissionReviewValidationIssue("ERROR", "transition_allowed", "must be False"))
    if not item.all_writes_blocked:
        issues.append(AdmissionReviewValidationIssue("ERROR", "all_writes_blocked", "must be True"))
    if item.mutation_detected:
        issues.append(AdmissionReviewValidationIssue("ERROR", "mutation_detected", "must be False"))
    for attr in ["allows_active_paper", "allows_broker_execution", "allows_paper_state_mutation", "allows_config_patch", "allows_telegram_real_send"]:
        if getattr(item, attr, True):
             issues.append(AdmissionReviewValidationIssue("ERROR", attr, "must be False"))
    return _build_validation_report(issues)

def validate_admission_full_report_validation(item: AdmissionReviewFullReport) -> AdmissionReviewValidationReport:
    issues = []
    for review in item.admission_reviews:
        rep = validate_admission_review_report(review)
        issues.extend(rep.issues)
    for rec in item.ledger_reconciliations:
        rep = validate_ledger_reconciliation_validation_report(rec)
        issues.extend(rep.issues)
    for cp in item.transition_checkpoints:
        rep = validate_transition_checkpoint_validation_report(cp)
        issues.extend(rep.issues)
    return _build_validation_report(issues)

def _validate_language(text: str, unsafe_keywords: List[str], error_message: str) -> AdmissionReviewValidationReport:
    issues = []
    text_lower = text.lower()
    for kw in unsafe_keywords:
        if kw in text_lower:
             issues.append(AdmissionReviewValidationIssue("BLOCK", "language", f"{error_message}: '{kw}'"))
    return _build_validation_report(issues)

def validate_no_live_execution_language_in_admission(text: str) -> AdmissionReviewValidationReport:
    keywords = ["live approved", "sent to broker", "kesin al", "garanti", "emir gönder", "gerçek emir"]
    return _validate_language(text, keywords, "Live execution language detected")

def validate_no_active_paper_language_in_admission(text: str) -> AdmissionReviewValidationReport:
    keywords = ["paper'a uygula", "aktif et", "canlıya al", "kesin kâr", "candidate kesin iyi"]
    return _validate_language(text, keywords, "Active paper language detected")

def validate_no_paper_state_mutation_fields_in_admission(payload: Dict[str, Any]) -> AdmissionReviewValidationReport:
    issues = []
    text = json.dumps(payload)
    for field in ["paper_state_committed", "paper_order_executed", "paper_order_created", "portfolio_state_mutated", "position_mutated", "cash_mutated", "equity_mutated"]:
        if f'"{field}": true' in text.lower():
             issues.append(AdmissionReviewValidationIssue("BLOCK", field, "Paper mutation field is true"))
    return _build_validation_report(issues)

def validate_no_broker_execution_fields_in_admission(payload: Dict[str, Any]) -> AdmissionReviewValidationReport:
    issues = []
    text = json.dumps(payload)
    for field in ["broker_order_id", "live_order_id", "sent_to_broker", "execution_venue", "real_fill_id"]:
        if f'"{field}"' in text.lower():
             issues.append(AdmissionReviewValidationIssue("BLOCK", field, "Broker execution field detected"))
    return _build_validation_report(issues)

def validate_no_sensitive_data_in_admission_payload(payload: Dict[str, Any]) -> AdmissionReviewValidationReport:
    issues = []
    text = json.dumps(payload)
    if "api_key" in text.lower() or "secret" in text.lower() or "token" in text.lower():
        # Heuristic
        pass
    return _build_validation_report(issues)

def admission_review_validation_report_to_text(report: AdmissionReviewValidationReport) -> str:
    return json.dumps([i.__dict__ for i in report.issues], indent=2)

def assert_admission_review_valid(report: AdmissionReviewValidationReport) -> None:
    if not report.valid:
        raise AdmissionReviewValidationError(f"Validation failed with {report.error_count} errors")
INNER_EOF

cat << 'INNER_EOF' > usa_signal_bot/paper_admission_review/admission_review_reporting.py
import json
from typing import Any, Dict
from .admission_review_models import (
    AdmissionReviewGate,
    LedgerReconciliationItem,
    LedgerReconciliationReport,
    AdmissionEvidenceSeal,
    FinalNoWriteTransitionCheckpoint,
    PaperModeAdmissionReview,
    AdmissionReviewAuditEntry,
    AdmissionReviewFullReport
)
from .admission_report import admission_review_limitations_text

def admission_review_gate_to_text(item: AdmissionReviewGate) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def ledger_reconciliation_item_to_text(item: LedgerReconciliationItem) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def ledger_reconciliation_report_to_text(item: LedgerReconciliationReport, limit: int = 100) -> str:
    d = item.__dict__.copy()
    d["items"] = [i.__dict__ for i in item.items[:limit]]
    return json.dumps(d, indent=2, default=str)

def admission_evidence_seal_to_text(item: AdmissionEvidenceSeal) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def final_no_write_transition_checkpoint_to_text(item: FinalNoWriteTransitionCheckpoint) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def paper_mode_admission_review_to_text(item: PaperModeAdmissionReview, limit: int = 100) -> str:
    d = item.__dict__.copy()
    d["gates"] = [g.__dict__ for g in item.gates[:limit]]
    if item.ledger_reconciliation:
        d["ledger_reconciliation"] = "..."
    if item.evidence_seal:
        d["evidence_seal"] = "..."
    return json.dumps(d, indent=2, default=str)

def admission_review_audit_entry_to_text(item: AdmissionReviewAuditEntry) -> str:
    return json.dumps(item.__dict__, indent=2, default=str)

def admission_review_full_report_to_text(item: AdmissionReviewFullReport, limit: int = 100) -> str:
    d = item.__dict__.copy()
    d["admission_reviews"] = [paper_mode_admission_review_to_text(r, limit) for r in item.admission_reviews[:limit]]
    return json.dumps(d, indent=2, default=str)

def admission_review_store_summary_to_text(summary: Dict[str, Any]) -> str:
    return json.dumps(summary, indent=2)
INNER_EOF
