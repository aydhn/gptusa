from typing import Any, Dict, List
from usa_signal_bot.paper_pre_rehearsal.pre_rehearsal_models import PrePaperDryRehearsalRun, PrePaperDryRehearsalReview
from usa_signal_bot.paper_pre_rehearsal.paper_baseline_loader import load_read_only_paper_baseline_for_pre_rehearsal, paper_baseline_hash

def build_read_only_paper_snapshot_for_pre_paper_rehearsal(paper_payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return load_read_only_paper_baseline_for_pre_rehearsal(paper_payload)

def compare_pre_paper_rehearsal_to_paper_snapshot(run: PrePaperDryRehearsalRun, paper_snapshot: Dict[str, Any]) -> Dict[str, Any]:
    snapshot_read_only = build_read_only_paper_snapshot_for_pre_paper_rehearsal(paper_snapshot)
    return {
        "run_baseline_hash": paper_baseline_hash(run.read_only_paper_baseline),
        "current_snapshot_hash": paper_baseline_hash(snapshot_read_only),
        "match": paper_baseline_hash(run.read_only_paper_baseline) == paper_baseline_hash(snapshot_read_only)
    }

def validate_paper_runtime_not_mutated_by_pre_paper_rehearsal(before: Dict[str, Any], after: Dict[str, Any]) -> List[str]:
    violations = []
    before_ro = build_read_only_paper_snapshot_for_pre_paper_rehearsal(before)
    after_ro = build_read_only_paper_snapshot_for_pre_paper_rehearsal(after)
    if paper_baseline_hash(before_ro) != paper_baseline_hash(after_ro):
        violations.append("Read-only baseline hashes do not match, indicating possible mutation")
    return violations

def attach_pre_paper_rehearsal_metadata_to_paper_analytics(payload: Dict[str, Any], review: PrePaperDryRehearsalReview) -> Dict[str, Any]:
    updated = payload.copy()
    updated["latest_pre_paper_review_id"] = review.review_id
    return updated

def paper_runtime_pre_paper_rehearsal_adapter_to_text(payload: Dict[str, Any]) -> str:
    has_review = "latest_pre_paper_review_id" in payload
    return f"Paper Runtime Adapter: Has Pre-Paper Review={has_review}"
