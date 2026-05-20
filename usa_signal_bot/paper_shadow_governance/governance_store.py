import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import json

from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowSessionComparisonReport, ShadowAcceptanceScorecard, ShadowEvidencePack,
    ShadowDecisionBoardResult, ShadowGovernanceAuditEntry, ShadowGovernanceReview,
    shadow_session_comparison_report_to_dict, shadow_acceptance_scorecard_to_dict,
    shadow_evidence_pack_to_dict, shadow_decision_board_result_to_dict,
    shadow_governance_audit_entry_to_dict, shadow_governance_review_to_dict
)

def shadow_governance_store_dir(data_root: Path) -> Path:
    d = data_root / "paper_shadow_governance"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_comparison_reports_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "comparison_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_scorecards_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "scorecards"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_evidence_packs_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "evidence_packs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_decisions_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "decisions"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_audit_logs_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "audit_logs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def shadow_governance_reviews_dir(data_root: Path) -> Path:
    d = shadow_governance_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_shadow_comparison_report_json(path: Path, item: ShadowSessionComparisonReport) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_session_comparison_report_to_dict(item), f, indent=2)
    return path

def write_shadow_acceptance_scorecard_json(path: Path, item: ShadowAcceptanceScorecard) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_acceptance_scorecard_to_dict(item), f, indent=2)
    return path

def write_shadow_evidence_pack_json(path: Path, item: ShadowEvidencePack) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_evidence_pack_to_dict(item), f, indent=2)
    return path

def write_shadow_decision_result_json(path: Path, item: ShadowDecisionBoardResult) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_decision_board_result_to_dict(item), f, indent=2)
    return path

def write_shadow_audit_entries_jsonl(path: Path, items: List[ShadowGovernanceAuditEntry]) -> Path:
    with open(path, 'a', encoding='utf-8') as f:
        for it in items:
            f.write(json.dumps(shadow_governance_audit_entry_to_dict(it)) + "\n")
    return path

def write_shadow_governance_review_json(path: Path, item: ShadowGovernanceReview) -> Path:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(shadow_governance_review_to_dict(item), f, indent=2)
    return path

def read_shadow_governance_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_shadow_governance_reviews(data_root: Path) -> List[Path]:
    d = shadow_governance_reviews_dir(data_root)
    return sorted(d.glob("*.json"), key=os.path.getmtime, reverse=True)

def get_latest_shadow_governance_review(data_root: Path) -> Optional[Path]:
    l = list_shadow_governance_reviews(data_root)
    return l[0] if l else None

def shadow_governance_store_summary(data_root: Path) -> Dict[str, Any]:
    return {"total_reviews": len(list_shadow_governance_reviews(data_root))}
