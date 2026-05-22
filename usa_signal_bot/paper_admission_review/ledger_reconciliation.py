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
