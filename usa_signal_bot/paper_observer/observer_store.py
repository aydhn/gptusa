import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import dataclasses

from usa_signal_bot.paper_observer.observer_models import (
    PaperObserverEnrollment, ObserverRuntimeContext, ObserverRuntimeSession,
    ObserverOutput, ObserverDriftEvent, ObserverAuditEntry, PaperObserverReview,
    paper_observer_review_to_dict
)

def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def paper_observer_store_dir(data_root: Path) -> Path:
    return _ensure_dir(data_root / "paper_observer")

def observer_enrollments_dir(data_root: Path) -> Path:
    return _ensure_dir(paper_observer_store_dir(data_root) / "enrollments")

def observer_contexts_dir(data_root: Path) -> Path:
    return _ensure_dir(paper_observer_store_dir(data_root) / "contexts")

def observer_sessions_dir(data_root: Path) -> Path:
    return _ensure_dir(paper_observer_store_dir(data_root) / "sessions")

def observer_outputs_dir(data_root: Path) -> Path:
    return _ensure_dir(paper_observer_store_dir(data_root) / "outputs")

def observer_drift_dir(data_root: Path) -> Path:
    return _ensure_dir(paper_observer_store_dir(data_root) / "drift")

def observer_audit_dir(data_root: Path) -> Path:
    return _ensure_dir(paper_observer_store_dir(data_root) / "audit")

def observer_reviews_dir(data_root: Path) -> Path:
    return _ensure_dir(paper_observer_store_dir(data_root) / "reviews")

def _write_json(path: Path, data: dict) -> Path:
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    return path

def _write_jsonl(path: Path, items: list) -> Path:
    with open(path, 'w') as f:
        for item in items:
            f.write(json.dumps(item, default=str) + "\n")
    return path

def write_observer_enrollment_json(path: Path, item: PaperObserverEnrollment) -> Path:
    return _write_json(path, dataclasses.asdict(item))

def write_observer_context_json(path: Path, item: ObserverRuntimeContext) -> Path:
    return _write_json(path, dataclasses.asdict(item))

def write_observer_session_json(path: Path, item: ObserverRuntimeSession) -> Path:
    return _write_json(path, dataclasses.asdict(item))

def write_observer_outputs_jsonl(path: Path, items: List[ObserverOutput]) -> Path:
    return _write_jsonl(path, [dataclasses.asdict(x) for x in items])

def write_observer_drift_jsonl(path: Path, items: List[ObserverDriftEvent]) -> Path:
    return _write_jsonl(path, [dataclasses.asdict(x) for x in items])

def write_observer_audit_jsonl(path: Path, items: List[ObserverAuditEntry]) -> Path:
    return _write_jsonl(path, [dataclasses.asdict(x) for x in items])

def write_paper_observer_review_json(path: Path, item: PaperObserverReview) -> Path:
    return _write_json(path, paper_observer_review_to_dict(item))

def read_paper_observer_review_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def list_paper_observer_reviews(data_root: Path) -> List[Path]:
    rev_dir = observer_reviews_dir(data_root)
    return sorted(list(rev_dir.glob("*.json")), reverse=True)

def get_latest_paper_observer_review(data_root: Path) -> Optional[Path]:
    files = list_paper_observer_reviews(data_root)
    return files[0] if files else None

def paper_observer_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "enrollments": len(list(observer_enrollments_dir(data_root).glob("*.json"))),
        "sessions": len(list(observer_sessions_dir(data_root).glob("*.json"))),
        "reviews": len(list_paper_observer_reviews(data_root))
    }
