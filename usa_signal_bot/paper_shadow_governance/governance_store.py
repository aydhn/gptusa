import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.paper_common.io import ensure_dir, write_json, append_jsonl, read_json

from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowSessionComparisonReport, ShadowAcceptanceScorecard, ShadowEvidencePack,
    ShadowDecisionBoardResult, ShadowGovernanceAuditEntry, ShadowGovernanceReview,
    shadow_session_comparison_report_to_dict, shadow_acceptance_scorecard_to_dict,
    shadow_evidence_pack_to_dict, shadow_decision_board_result_to_dict,
    shadow_governance_audit_entry_to_dict, shadow_governance_review_to_dict
)

def shadow_governance_store_dir(data_root: Path) -> Path:
    return ensure_dir(data_root / "paper_shadow_governance")

def shadow_comparison_reports_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_governance_store_dir(data_root) / "comparison_reports")

def shadow_scorecards_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_governance_store_dir(data_root) / "scorecards")

def shadow_evidence_packs_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_governance_store_dir(data_root) / "evidence_packs")

def shadow_decisions_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_governance_store_dir(data_root) / "decisions")

def shadow_audit_logs_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_governance_store_dir(data_root) / "audit_logs")

def shadow_governance_reviews_dir(data_root: Path) -> Path:
    return ensure_dir(shadow_governance_store_dir(data_root) / "reviews")

def write_shadow_comparison_report_json(path: Path, item: ShadowSessionComparisonReport) -> Path:
    return write_json(path, shadow_session_comparison_report_to_dict(item), ensure_parent=False)

def write_shadow_acceptance_scorecard_json(path: Path, item: ShadowAcceptanceScorecard) -> Path:
    return write_json(path, shadow_acceptance_scorecard_to_dict(item), ensure_parent=False)

def write_shadow_evidence_pack_json(path: Path, item: ShadowEvidencePack) -> Path:
    return write_json(path, shadow_evidence_pack_to_dict(item), ensure_parent=False)

def write_shadow_decision_result_json(path: Path, item: ShadowDecisionBoardResult) -> Path:
    return write_json(path, shadow_decision_board_result_to_dict(item), ensure_parent=False)

def write_shadow_audit_entries_jsonl(path: Path, items: List[ShadowGovernanceAuditEntry]) -> Path:
    return append_jsonl(path, (shadow_governance_audit_entry_to_dict(it) for it in items), ensure_parent=False)

def write_shadow_governance_review_json(path: Path, item: ShadowGovernanceReview) -> Path:
    return write_json(path, shadow_governance_review_to_dict(item), ensure_parent=False)

def read_shadow_governance_review_json(path: Path) -> Dict[str, Any]:
    return read_json(path)

def list_shadow_governance_reviews(data_root: Path) -> List[Path]:
    d = shadow_governance_reviews_dir(data_root)
    return sorted(d.glob("*.json"), key=os.path.getmtime, reverse=True)

def get_latest_shadow_governance_review(data_root: Path) -> Optional[Path]:
    l = list_shadow_governance_reviews(data_root)
    return l[0] if l else None

def shadow_governance_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"total_reviews": len(list_shadow_governance_reviews(data_root))}
