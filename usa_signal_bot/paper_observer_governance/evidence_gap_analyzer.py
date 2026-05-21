from typing import Any
from .observer_governance_models import PromotionEvidenceRefresh
from usa_signal_bot.core.enums import ObserverGovernanceRiskFlag, EvidenceFreshnessStatus

def analyze_evidence_gaps(refresh: PromotionEvidenceRefresh) -> dict[str, Any]:
    return {"missing": missing_evidence_types(refresh), "stale": stale_evidence_types(refresh)}

def missing_evidence_types(refresh: PromotionEvidenceRefresh) -> list[str]:
    return [i.evidence_type for i in refresh.evidence_items if not i.available]

def stale_evidence_types(refresh: PromotionEvidenceRefresh) -> list[str]:
    return [i.evidence_type for i in refresh.evidence_items if i.status == EvidenceFreshnessStatus.STALE]

def evidence_gap_risk_flags(refresh: PromotionEvidenceRefresh) -> list[ObserverGovernanceRiskFlag]:
    flags = []
    if missing_evidence_types(refresh): flags.append(ObserverGovernanceRiskFlag.EVIDENCE_MISSING)
    if stale_evidence_types(refresh): flags.append(ObserverGovernanceRiskFlag.EVIDENCE_STALE)
    return flags

def evidence_gap_analyzer_to_text(payload: dict[str, Any]) -> str:
    return str(payload)
