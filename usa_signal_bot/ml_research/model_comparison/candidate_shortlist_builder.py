import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    CandidateShortlist,
    ModelRankingTable,
    create_candidate_shortlist_id
)

def build_candidate_shortlist(ranking: ModelRankingTable, max_candidates: int = 3) -> CandidateShortlist:
    selected = ranking.entries[:max_candidates]

    shortlist = CandidateShortlist(
        shortlist_id=create_candidate_shortlist_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        shortlist_status="CREATED",
        entries=selected,
        max_candidate_count=max_candidates,
        selected_candidate_count=len(selected),
        selection_rationale=["Top ranked research candidates based on baseline metrics."],
        research_only=True,
        phase141_calibration_candidates_only=True,
        eligible_for_live_use=False,
        eligible_for_paper_use=False,
        eligible_for_broker_use=False,
        eligible_for_deployment=False,
        eligible_for_strategy_activation=False,
        shortlist_hash=None,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )
    shortlist.shortlist_hash = compute_candidate_shortlist_hash(shortlist)
    return shortlist

def validate_candidate_shortlist(shortlist: CandidateShortlist) -> list[str]:
    return []

def compute_candidate_shortlist_hash(shortlist: CandidateShortlist) -> str:
    data = [e.model_artifact_id for e in shortlist.entries]
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def candidate_shortlist_summary(shortlist: CandidateShortlist) -> dict[str, Any]:
    return {"selected_count": shortlist.selected_candidate_count}

def candidate_shortlist_to_text(shortlist: CandidateShortlist, limit: int = 300) -> str:
    return str([e.model_name for e in shortlist.entries])[:limit]
