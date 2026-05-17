import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.diagnostics.diagnostic_models import (
    DiagnosticEvent, FailureModeAssessment, FailureCluster, StrategyDiagnosticResult,
    RemediationHint, DiagnosticScorecard, DiagnosticReview,
    diagnostic_event_to_dict, failure_mode_assessment_to_dict, failure_cluster_to_dict,
    strategy_diagnostic_result_to_dict, remediation_hint_to_dict, diagnostic_scorecard_to_dict,
    diagnostic_review_to_dict
)
from usa_signal_bot.core.exceptions import DiagnosticsStorageError

def diagnostics_store_dir(data_root: Path) -> Path:
    p = data_root / "diagnostics"
    p.mkdir(parents=True, exist_ok=True)
    return p

def diagnostic_events_dir(data_root: Path) -> Path:
    p = diagnostics_store_dir(data_root) / "events"
    p.mkdir(parents=True, exist_ok=True)
    return p

def failure_assessments_dir(data_root: Path) -> Path:
    p = diagnostics_store_dir(data_root) / "failure_assessments"
    p.mkdir(parents=True, exist_ok=True)
    return p

def failure_clusters_dir(data_root: Path) -> Path:
    p = diagnostics_store_dir(data_root) / "failure_clusters"
    p.mkdir(parents=True, exist_ok=True)
    return p

def strategy_diagnostics_dir(data_root: Path) -> Path:
    p = diagnostics_store_dir(data_root) / "strategy_diagnostics"
    p.mkdir(parents=True, exist_ok=True)
    return p

def remediation_hints_dir(data_root: Path) -> Path:
    p = diagnostics_store_dir(data_root) / "remediation_hints"
    p.mkdir(parents=True, exist_ok=True)
    return p

def diagnostic_scorecards_dir(data_root: Path) -> Path:
    p = diagnostics_store_dir(data_root) / "scorecards"
    p.mkdir(parents=True, exist_ok=True)
    return p

def diagnostic_reviews_dir(data_root: Path) -> Path:
    p = diagnostics_store_dir(data_root) / "reviews"
    p.mkdir(parents=True, exist_ok=True)
    return p

def _write_jsonl(path: Path, items: List[Any], to_dict_func) -> Path:
    try:
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(to_dict_func(item)) + "\n")
        return path
    except Exception as e:
        raise DiagnosticsStorageError(f"Failed to write jsonl to {path}: {e}")

def write_diagnostic_events_jsonl(path: Path, items: List[DiagnosticEvent]) -> Path:
    return _write_jsonl(path, items, diagnostic_event_to_dict)

def write_failure_assessments_jsonl(path: Path, items: List[FailureModeAssessment]) -> Path:
    return _write_jsonl(path, items, failure_mode_assessment_to_dict)

def write_failure_clusters_jsonl(path: Path, items: List[FailureCluster]) -> Path:
    return _write_jsonl(path, items, failure_cluster_to_dict)

def write_strategy_diagnostics_jsonl(path: Path, items: List[StrategyDiagnosticResult]) -> Path:
    return _write_jsonl(path, items, strategy_diagnostic_result_to_dict)

def write_remediation_hints_jsonl(path: Path, items: List[RemediationHint]) -> Path:
    return _write_jsonl(path, items, remediation_hint_to_dict)

def write_diagnostic_scorecard_json(path: Path, item: DiagnosticScorecard) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(diagnostic_scorecard_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise DiagnosticsStorageError(f"Failed to write scorecard to {path}: {e}")

def write_diagnostic_review_json(path: Path, item: DiagnosticReview) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(diagnostic_review_to_dict(item), f, indent=2)
        return path
    except Exception as e:
        raise DiagnosticsStorageError(f"Failed to write review to {path}: {e}")

def read_diagnostic_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise DiagnosticsStorageError(f"Review not found: {path}")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise DiagnosticsStorageError(f"Failed to read review from {path}: {e}")

def list_diagnostic_reviews(data_root: Path) -> List[Path]:
    d = diagnostic_reviews_dir(data_root)
    return sorted(list(d.glob("*.json")))

def get_latest_diagnostic_review(data_root: Path) -> Optional[Path]:
    reviews = list_diagnostic_reviews(data_root)
    if not reviews:
        return None
    return reviews[-1]

def diagnostics_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "events_files": len(list(diagnostic_events_dir(data_root).glob("*.jsonl"))),
        "assessments_files": len(list(failure_assessments_dir(data_root).glob("*.jsonl"))),
        "reviews_files": len(list_diagnostic_reviews(data_root))
    }
