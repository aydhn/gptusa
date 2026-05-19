import json
from pathlib import Path
from typing import Any, Optional
from usa_signal_bot.research_governance.governance_models import (
    GovernanceEvidencePack, PromotionReview, ReleaseCandidatePackage,
    DecisionBoardResult, PromotionDecisionLogEntry, GovernanceAuditTrail,
    GovernanceReview,
    governance_evidence_pack_to_dict, promotion_review_to_dict,
    release_candidate_package_to_dict, decision_board_result_to_dict,
    promotion_decision_log_entry_to_dict, governance_audit_trail_to_dict,
    governance_review_to_dict
)

def governance_store_dir(data_root: Path) -> Path:
    d = data_root / "research_governance"
    d.mkdir(parents=True, exist_ok=True)
    return d

def evidence_packs_dir(data_root: Path) -> Path:
    d = governance_store_dir(data_root) / "evidence_packs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def promotion_reviews_dir(data_root: Path) -> Path:
    d = governance_store_dir(data_root) / "promotion_reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def release_candidates_dir(data_root: Path) -> Path:
    d = governance_store_dir(data_root) / "release_candidates"
    d.mkdir(parents=True, exist_ok=True)
    return d

def decision_board_results_dir(data_root: Path) -> Path:
    d = governance_store_dir(data_root) / "decision_board_results"
    d.mkdir(parents=True, exist_ok=True)
    return d

def decision_logs_dir(data_root: Path) -> Path:
    d = governance_store_dir(data_root) / "decision_logs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def audit_trails_dir(data_root: Path) -> Path:
    d = governance_store_dir(data_root) / "audit_trails"
    d.mkdir(parents=True, exist_ok=True)
    return d

def governance_reviews_dir(data_root: Path) -> Path:
    d = governance_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_evidence_pack_json(path: Path, item: GovernanceEvidencePack) -> Path:
    with open(path, "w") as f:
        json.dump(governance_evidence_pack_to_dict(item), f, indent=2)
    return path

def write_promotion_review_json(path: Path, item: PromotionReview) -> Path:
    with open(path, "w") as f:
        json.dump(promotion_review_to_dict(item), f, indent=2)
    return path

def write_release_candidate_json(path: Path, item: ReleaseCandidatePackage) -> Path:
    with open(path, "w") as f:
        json.dump(release_candidate_package_to_dict(item), f, indent=2)
    return path

def write_decision_board_result_json(path: Path, item: DecisionBoardResult) -> Path:
    with open(path, "w") as f:
        json.dump(decision_board_result_to_dict(item), f, indent=2)
    return path

def write_promotion_decision_logs_jsonl(path: Path, items: list[PromotionDecisionLogEntry]) -> Path:
    with open(path, "w") as f:
        for it in items:
            f.write(json.dumps(promotion_decision_log_entry_to_dict(it)) + "\n")
    return path

def write_governance_audit_trail_json(path: Path, item: GovernanceAuditTrail) -> Path:
    with open(path, "w") as f:
        json.dump(governance_audit_trail_to_dict(item), f, indent=2)
    return path

def write_governance_review_json(path: Path, item: GovernanceReview) -> Path:
    with open(path, "w") as f:
        json.dump(governance_review_to_dict(item), f, indent=2)
    return path

def read_governance_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def list_governance_reviews(data_root: Path) -> list[Path]:
    d = governance_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_governance_review(data_root: Path) -> Optional[Path]:
    lst = list_governance_reviews(data_root)
    return lst[-1] if lst else None

def governance_store_summary(data_root: Path) -> dict[str, Any]:
    return {"reviews_count": len(list_governance_reviews(data_root))}
