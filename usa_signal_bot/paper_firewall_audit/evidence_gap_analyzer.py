from typing import Any, List
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import PrePaperReadinessEvidenceRefresh
from usa_signal_bot.core.enums import FirewallAuditRiskFlag

def analyze_pre_paper_evidence_gaps(refresh: PrePaperReadinessEvidenceRefresh) -> dict[str, Any]:
    return {
        "missing": missing_pre_paper_evidence_types(refresh),
        "stale": stale_pre_paper_evidence_types(refresh)
    }

def missing_pre_paper_evidence_types(refresh: PrePaperReadinessEvidenceRefresh) -> List[str]:
    return [i.evidence_type for i in refresh.evidence_items if i.required and not i.available]

def stale_pre_paper_evidence_types(refresh: PrePaperReadinessEvidenceRefresh) -> List[str]:
    return [i.evidence_type for i in refresh.evidence_items if i.required and i.stale]

def pre_paper_evidence_gap_risk_flags(refresh: PrePaperReadinessEvidenceRefresh) -> List[FirewallAuditRiskFlag]:
    flags = []
    if refresh.missing_count > 0: flags.append(FirewallAuditRiskFlag.EVIDENCE_MISSING)
    if refresh.stale_count > 0: flags.append(FirewallAuditRiskFlag.EVIDENCE_STALE)
    return flags

def evidence_gap_analyzer_to_text(payload: dict[str, Any]) -> str:
    return f"Gaps: {len(payload.get('missing', []))} missing, {len(payload.get('stale', []))} stale"
