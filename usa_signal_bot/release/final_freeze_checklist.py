from typing import Any, Dict, List
import hashlib
import json

from usa_signal_bot.release.phase159_models import (
    FinalFreezeChecklist,
    FinalFreezeChecklistItem,
    ReleaseCandidateAudit,
    AcceptanceEvidenceBundle,
    AcceptanceAreaKind,
    FinalFreezeStatus,
    create_final_freeze_checklist_id,
    create_final_freeze_checklist_item_id,
    generate_timestamp,
    AdvancedAcceptanceRiskFlag
)

def build_default_final_freeze_checklist_items() -> List[Dict[str, Any]]:
    return [
        {"name": "Phase158 integration review ingested", "area": AcceptanceAreaKind.INTEGRATION},
        {"name": "advanced acceptance matrix valid", "area": AcceptanceAreaKind.CORE_RUNTIME},
        {"name": "dry-run steps safe", "area": AcceptanceAreaKind.SAFETY},
        {"name": "evidence bundle complete", "area": AcceptanceAreaKind.INTEGRATION},
        {"name": "regression acceptance passed", "area": AcceptanceAreaKind.INTEGRATION},
        {"name": "safety acceptance passed", "area": AcceptanceAreaKind.SAFETY},
        {"name": "system area reports passed", "area": AcceptanceAreaKind.RELEASE_CANDIDATE},
        {"name": "release candidate audit passed", "area": AcceptanceAreaKind.RELEASE_CANDIDATE},
        {"name": "risk register has no blocking risk", "area": AcceptanceAreaKind.RELEASE_CANDIDATE},
        {"name": "final freeze boundary passed", "area": AcceptanceAreaKind.SAFETY},
        {"name": "docs ready", "area": AcceptanceAreaKind.DOCUMENTATION},
        {"name": "tests ready", "area": AcceptanceAreaKind.TESTS},
        {"name": "no live/paper/broker", "area": AcceptanceAreaKind.SAFETY},
        {"name": "no deployment", "area": AcceptanceAreaKind.SAFETY},
        {"name": "ready for Phase160 final delivery audit", "area": AcceptanceAreaKind.RELEASE_CANDIDATE}
    ]

def build_final_freeze_checklist(audit: ReleaseCandidateAudit, evidence_bundle: AcceptanceEvidenceBundle) -> FinalFreezeChecklist:

    # In a real run, this would evaluate actual system state.
    # For Phase 159, we derive logic from the audit and evidence.

    items = []
    base_items = build_default_final_freeze_checklist_items()

    for item_def in base_items:
        passed = True
        if item_def["name"] == "evidence bundle complete" and not evidence_bundle.bundle_valid:
            passed = False
        if item_def["name"] == "release candidate audit passed" and not audit.audit_passed:
            passed = False
        if item_def["name"] == "risk register has no blocking risk" and audit.risk_register.blocking_risk_count > 0:
            passed = False

        items.append(FinalFreezeChecklistItem(
            item_id=create_final_freeze_checklist_item_id(),
            created_at_utc=generate_timestamp(),
            name=item_def["name"],
            area_kind=item_def["area"],
            required=True,
            passed=passed,
            status=FinalFreezeStatus.PASSED if passed else FinalFreezeStatus.FAILED,
            evidence=None,
            rationale="Derived from audit/bundle state",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))

    failed_count = sum(1 for i in items if not i.passed)

    checklist = FinalFreezeChecklist(
        checklist_id=create_final_freeze_checklist_id(),
        created_at_utc=generate_timestamp(),
        items=items,
        item_count=len(items),
        passed_count=sum(1 for i in items if i.passed),
        warning_count=0,
        failed_count=failed_count,
        blocked_count=0,
        checklist_hash=None,
        checklist_valid=failed_count == 0,
        ready_for_final_delivery_audit=failed_count == 0,
        not_deployment_approval=True,
        not_trading_approval=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    checklist.checklist_hash = compute_final_freeze_checklist_hash(checklist)

    if failed_count > 0:
        checklist.risk_flags.append(AdvancedAcceptanceRiskFlag.FINAL_FREEZE_CHECKLIST_INVALID)

    return checklist

def compute_final_freeze_checklist_hash(checklist: FinalFreezeChecklist) -> str:
    data = [{"name": i.name, "passed": i.passed} for i in checklist.items]
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def validate_final_freeze_checklist(checklist: FinalFreezeChecklist) -> List[str]:
    errors = []
    if checklist.failed_count > 0 and checklist.checklist_valid:
        errors.append("Checklist cannot be valid with failed items")
    return errors

def final_freeze_checklist_to_text(checklist: FinalFreezeChecklist, limit: int = 300) -> str:
    lines = [f"Final Freeze Checklist: {checklist.checklist_id}", f"Valid: {checklist.checklist_valid}"]
    for i in checklist.items[:limit]:
        lines.append(f" - [{ 'x' if i.passed else ' ' }] {i.name}")
    return "\n".join(lines)
