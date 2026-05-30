import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from usa_signal_bot.regime_classification.monitoring.phase133_models import (
    RegimeMonitoringContext,
    RegimeMonitoringFullReview,
    RegimeMonitoringBaseline,
    RegimeMonitoringSnapshot,
    RegimeDriftTrackingResult,
    ContextDegradationDiagnostic,
    ContextDegradationProfile,
    RegimeMonitoringReadinessGate,
    regime_monitoring_context_to_dict,
    regime_monitoring_full_review_to_dict,
    regime_monitoring_baseline_to_dict,
    regime_monitoring_snapshot_to_dict,
    regime_drift_tracking_result_to_dict,
    context_degradation_diagnostic_to_dict,
    context_degradation_profile_to_dict,
    regime_monitoring_readiness_gate_to_dict
)
from usa_signal_bot.core.exceptions import RegimeMonitoringStoreError

def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def regime_monitoring_store_dir(data_root: Path) -> Path:
    return _ensure_dir(data_root / "regime_classification" / "monitoring")

def regime_monitoring_contexts_dir(data_root: Path) -> Path:
    return _ensure_dir(regime_monitoring_store_dir(data_root) / "contexts")

def regime_monitoring_reviews_dir(data_root: Path) -> Path:
    return _ensure_dir(regime_monitoring_store_dir(data_root) / "reviews")

def monitoring_baselines_dir(data_root: Path) -> Path:
    return _ensure_dir(regime_monitoring_store_dir(data_root) / "baselines")

def monitoring_snapshots_dir(data_root: Path) -> Path:
    return _ensure_dir(regime_monitoring_store_dir(data_root) / "snapshots")

def drift_results_dir(data_root: Path) -> Path:
    return _ensure_dir(regime_monitoring_store_dir(data_root) / "drift")

def degradation_diagnostics_dir(data_root: Path) -> Path:
    return _ensure_dir(regime_monitoring_store_dir(data_root) / "degradation_diagnostics")

def degradation_profiles_dir(data_root: Path) -> Path:
    return _ensure_dir(regime_monitoring_store_dir(data_root) / "degradation_profiles")

def monitoring_gates_dir(data_root: Path) -> Path:
    return _ensure_dir(regime_monitoring_store_dir(data_root) / "gates")

def write_regime_monitoring_context_json(path: Path, item: RegimeMonitoringContext) -> Path:
    with open(path, "w") as f:
        json.dump(regime_monitoring_context_to_dict(item), f, indent=2)
    return path

def write_regime_monitoring_full_review_json(path: Path, item: RegimeMonitoringFullReview) -> Path:
    with open(path, "w") as f:
        json.dump(regime_monitoring_full_review_to_dict(item), f, indent=2)
    return path

def write_monitoring_baseline_json(path: Path, item: RegimeMonitoringBaseline) -> Path:
    with open(path, "w") as f:
        json.dump(regime_monitoring_baseline_to_dict(item), f, indent=2)
    return path

def write_monitoring_snapshot_json(path: Path, item: RegimeMonitoringSnapshot) -> Path:
    with open(path, "w") as f:
        json.dump(regime_monitoring_snapshot_to_dict(item), f, indent=2)
    return path

def write_drift_tracking_result_json(path: Path, item: RegimeDriftTrackingResult) -> Path:
    with open(path, "w") as f:
        json.dump(regime_drift_tracking_result_to_dict(item), f, indent=2)
    return path

def write_context_degradation_diagnostics_jsonl(path: Path, items: List[ContextDegradationDiagnostic]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(context_degradation_diagnostic_to_dict(item)) + "\n")
    return path

def write_context_degradation_profiles_jsonl(path: Path, items: List[ContextDegradationProfile]) -> Path:
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(context_degradation_profile_to_dict(item)) + "\n")
    return path

def write_monitoring_readiness_gate_json(path: Path, item: RegimeMonitoringReadinessGate) -> Path:
    with open(path, "w") as f:
        json.dump(regime_monitoring_readiness_gate_to_dict(item), f, indent=2)
    return path

def read_regime_monitoring_full_review_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise RegimeMonitoringStoreError(f"File not found: {path}")
    with open(path, "r") as f:
        return json.load(f)

def list_regime_monitoring_reviews(data_root: Path) -> List[Path]:
    d = regime_monitoring_reviews_dir(data_root)
    return sorted([p for p in d.glob("*.json") if p.is_file()])

def get_latest_regime_monitoring_review(data_root: Path) -> Optional[Path]:
    reviews = list_regime_monitoring_reviews(data_root)
    return reviews[-1] if reviews else None

def regime_monitoring_store_summary(data_root: Path) -> Dict[str, Any]:
    return {
        "contexts_count": len(list(regime_monitoring_contexts_dir(data_root).glob("*.json"))),
        "reviews_count": len(list_regime_monitoring_reviews(data_root))
    }
