from typing import List, Optional
from datetime import datetime, timezone
from usa_signal_bot.paper_firewall_audit.firewall_audit_models import PrePaperReadinessEvidenceItem, PrePaperReadinessEvidenceRefresh, create_pre_paper_evidence_refresh_id
from usa_signal_bot.core.enums import ReadinessEvidenceRefreshStatus

def calculate_pre_paper_evidence_refresh(items: List[PrePaperReadinessEvidenceItem], max_age_days: int = 14) -> PrePaperReadinessEvidenceRefresh:
    for item in items:
        item.status = classify_pre_paper_evidence_item(item, max_age_days)
        item.fresh = item.status == ReadinessEvidenceRefreshStatus.FRESH
        item.stale = item.status == ReadinessEvidenceRefreshStatus.STALE

    req = sum(1 for i in items if i.required)
    avail = sum(1 for i in items if i.available)
    fresh = sum(1 for i in items if i.fresh)
    stale = sum(1 for i in items if i.stale)
    missing = req - avail
    score = pre_paper_evidence_score(items)

    status = ReadinessEvidenceRefreshStatus.FRESH
    if missing > 0: status = ReadinessEvidenceRefreshStatus.MISSING
    elif stale > 0: status = ReadinessEvidenceRefreshStatus.STALE
    elif fresh < req: status = ReadinessEvidenceRefreshStatus.PARTIAL

    return PrePaperReadinessEvidenceRefresh(
        refresh_id=create_pre_paper_evidence_refresh_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        candidate_id=None,
        evidence_items=items,
        required_count=req,
        available_count=avail,
        fresh_count=fresh,
        stale_count=stale,
        missing_count=missing,
        evidence_score=score,
        status=status,
        required_followups=pre_paper_evidence_followups(items),
        warnings=[],
        errors=[],
        metadata={}
    )

def classify_pre_paper_evidence_item(item: PrePaperReadinessEvidenceItem, max_age_days: int = 14) -> ReadinessEvidenceRefreshStatus:
    if not item.available: return ReadinessEvidenceRefreshStatus.MISSING
    return ReadinessEvidenceRefreshStatus.FRESH

def pre_paper_evidence_score(items: List[PrePaperReadinessEvidenceItem]) -> Optional[float]:
    req = sum(1 for i in items if i.required)
    if req == 0: return 100.0
    fresh = sum(1 for i in items if i.required and i.fresh)
    return (fresh / req) * 100.0

def pre_paper_evidence_followups(items: List[PrePaperReadinessEvidenceItem]) -> List[str]:
    f = []
    if sum(1 for i in items if i.required and not i.available) > 0:
        f.append("Collect missing required evidence")
    return f

def pre_paper_evidence_refresh_to_text(refresh: PrePaperReadinessEvidenceRefresh) -> str:
    return f"Evidence Refresh score {refresh.evidence_score} ({refresh.status.value})"
