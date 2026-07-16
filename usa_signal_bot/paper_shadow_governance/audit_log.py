from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from usa_signal_bot.core.enums import ShadowGovernanceRiskFlag
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowGovernanceAuditEntry, ShadowDecisionBoardResult,
    create_shadow_governance_audit_entry_id, utc_now_iso
)

@dataclass
class ShadowGovernanceAuditEntryParams:
    entity_type: str
    entity_id: str
    action: str
    rationale: str
    evidence_refs: Optional[List[str]] = None
    risk_flags: Optional[List[ShadowGovernanceRiskFlag]] = None

def create_shadow_governance_audit_entry(params: ShadowGovernanceAuditEntryParams) -> ShadowGovernanceAuditEntry:
    return ShadowGovernanceAuditEntry(
        audit_id=create_shadow_governance_audit_entry_id(),
        created_at_utc=utc_now_iso(),
        entity_type=params.entity_type,
        entity_id=params.entity_id,
        action=params.action,
        rationale=params.rationale,
        evidence_refs=params.evidence_refs or [],
        risk_flags=params.risk_flags or [],
        warnings=[], errors=[]
    )

def audit_entry_from_decision(result: ShadowDecisionBoardResult) -> ShadowGovernanceAuditEntry:
    return create_shadow_governance_audit_entry(
        ShadowGovernanceAuditEntryParams(
            entity_type="ShadowDecisionBoardResult",
            entity_id=result.decision_id,
            action=result.decision.value,
            rationale=result.rationale,
            evidence_refs=[result.comparison_report_id, result.scorecard_id] if result.comparison_report_id else [],
            risk_flags=result.risk_flags
        )
    )

def append_shadow_audit_entry(entries: List[ShadowGovernanceAuditEntry], entry: ShadowGovernanceAuditEntry) -> List[ShadowGovernanceAuditEntry]:
    return entries + [entry]

def shadow_audit_summary(entries: List[ShadowGovernanceAuditEntry]) -> Dict[str, Any]:
    return {"total_entries": len(entries)}

def shadow_audit_log_to_text(entries: List[ShadowGovernanceAuditEntry], limit: int = 100) -> str:
    return f"Audit log contains {len(entries)} entries."
