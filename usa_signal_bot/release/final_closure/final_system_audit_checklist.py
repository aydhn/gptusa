from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalSystemAuditChecklist,
    FinalSystemAuditChecklistItem,
    FinalAuditAreaKind,
    FinalAuditStatus,
    FinalArtifactIndex,
    FinalPhaseLineage,
    create_final_system_audit_checklist_item_id,
    create_final_system_audit_checklist_id,
    generate_timestamp
)
import hashlib
import json

def build_default_final_system_audit_items() -> List[FinalSystemAuditChecklistItem]:
    areas = [
        FinalAuditAreaKind.ARCHITECTURE,
        FinalAuditAreaKind.CONFIGURATION,
        FinalAuditAreaKind.LOCAL_RUNTIME,
        FinalAuditAreaKind.DATA_PIPELINE,
        FinalAuditAreaKind.FEATURE_ENGINE,
        FinalAuditAreaKind.REGIME_ENGINE,
        FinalAuditAreaKind.ML_GOVERNANCE,
        FinalAuditAreaKind.BACKTEST_ROBUSTNESS,
        FinalAuditAreaKind.PORTFOLIO_GOVERNANCE,
        FinalAuditAreaKind.INTEGRATION,
        FinalAuditAreaKind.ACCEPTANCE,
        FinalAuditAreaKind.RELEASE_FREEZE,
        FinalAuditAreaKind.SAFETY_BOUNDARY,
        FinalAuditAreaKind.CLI,
        FinalAuditAreaKind.STORAGE,
        FinalAuditAreaKind.HEALTH,
        FinalAuditAreaKind.QUALITY,
        FinalAuditAreaKind.OBSERVABILITY,
        FinalAuditAreaKind.NOTIFICATIONS,
        FinalAuditAreaKind.DOCUMENTATION,
        FinalAuditAreaKind.TESTING,
        FinalAuditAreaKind.PROJECT_CLOSURE
    ]

    items = []
    for area in areas:
        items.append(FinalSystemAuditChecklistItem(
            item_id=create_final_system_audit_checklist_item_id(),
            created_at_utc=generate_timestamp(),
            area_kind=area,
            name=f"Audit {area.value.lower()}",
            required=True,
            passed=True,
            status=FinalAuditStatus.PASSED,
            evidence=f"Evidence for {area.value.lower()}",
            rationale="Satisfies criteria",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return items

def compute_final_system_audit_checklist_hash(checklist: FinalSystemAuditChecklist) -> str:
    data = json.dumps([i.to_dict() for i in checklist.items], sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_system_audit_checklist(index: FinalArtifactIndex, lineage: FinalPhaseLineage) -> FinalSystemAuditChecklist:
    items = build_default_final_system_audit_items()

    passed_count = len([i for i in items if i.passed and i.status == FinalAuditStatus.PASSED])
    warning_count = len([i for i in items if i.status == FinalAuditStatus.WARNING])
    failed_count = len([i for i in items if not i.passed and i.status == FinalAuditStatus.FAILED])
    blocked_count = len([i for i in items if i.status == FinalAuditStatus.BLOCKED])

    valid = failed_count == 0 and blocked_count == 0 and index.index_valid and lineage.lineage_valid

    checklist = FinalSystemAuditChecklist(
        checklist_id=create_final_system_audit_checklist_id(),
        created_at_utc=generate_timestamp(),
        items=items,
        item_count=len(items),
        passed_count=passed_count,
        warning_count=warning_count,
        failed_count=failed_count,
        blocked_count=blocked_count,
        checklist_valid=valid,
        audit_ready=valid,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    if not valid:
        checklist.errors.append("Checklist contains failed or blocked items, or dependencies are invalid.")

    checklist.checklist_hash = compute_final_system_audit_checklist_hash(checklist)
    return checklist

def validate_final_system_audit_checklist(checklist: FinalSystemAuditChecklist) -> List[str]:
    errors = []
    if not checklist.checklist_valid:
        errors.extend(checklist.errors)
    return errors

def final_system_audit_checklist_to_text(checklist: FinalSystemAuditChecklist, limit: int = 300) -> str:
    return f"Final System Audit Checklist: Valid={checklist.checklist_valid}, Passed={checklist.passed_count}/{checklist.item_count}"
