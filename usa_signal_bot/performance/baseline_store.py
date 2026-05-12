import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from usa_signal_bot.performance.baseline_models import (
    PerformanceBaseline,
    CurrentPerformanceSample,
    BaselineComparisonResult,
    PerformanceReviewResult,
    performance_baseline_to_dict,
    current_performance_sample_to_dict,
    baseline_comparison_result_to_dict,
    performance_review_result_to_dict
)
from usa_signal_bot.performance.threshold_models import SLAEvaluationReport, sla_evaluation_report_to_dict
from usa_signal_bot.performance.acceptance_gate import PerformanceAcceptanceGateResult, performance_acceptance_gate_result_to_dict
from usa_signal_bot.performance.alert_rules import PerformanceAlert, performance_alert_to_dict
from usa_signal_bot.core.enums import PerformanceBaselineScope

def baseline_store_dir(data_root: Path) -> Path:
    d = data_root / "performance"
    d.mkdir(parents=True, exist_ok=True)
    return d

def baselines_dir(data_root: Path) -> Path:
    d = baseline_store_dir(data_root) / "baselines"
    d.mkdir(parents=True, exist_ok=True)
    return d

def samples_dir(data_root: Path) -> Path:
    d = baseline_store_dir(data_root) / "samples"
    d.mkdir(parents=True, exist_ok=True)
    return d

def comparisons_dir(data_root: Path) -> Path:
    d = baseline_store_dir(data_root) / "comparisons"
    d.mkdir(parents=True, exist_ok=True)
    return d

def threshold_reports_dir(data_root: Path) -> Path:
    d = baseline_store_dir(data_root) / "thresholds"
    d.mkdir(parents=True, exist_ok=True)
    return d

def acceptance_dir(data_root: Path) -> Path:
    d = baseline_store_dir(data_root) / "acceptance"
    d.mkdir(parents=True, exist_ok=True)
    return d

def alerts_dir(data_root: Path) -> Path:
    d = baseline_store_dir(data_root) / "alerts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def reviews_dir(data_root: Path) -> Path:
    d = baseline_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_performance_baseline_json(path: Path, baseline: PerformanceBaseline) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(performance_baseline_to_dict(baseline), f, indent=2)
    return path

def write_performance_baselines_jsonl(path: Path, baselines: List[PerformanceBaseline]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        for b in baselines:
            f.write(json.dumps(performance_baseline_to_dict(b)) + "\n")
    return path

def write_current_performance_sample_json(path: Path, sample: CurrentPerformanceSample) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(current_performance_sample_to_dict(sample), f, indent=2)
    return path

def write_baseline_comparison_result_json(path: Path, result: BaselineComparisonResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(baseline_comparison_result_to_dict(result), f, indent=2)
    return path

def write_sla_evaluation_report_json(path: Path, report: SLAEvaluationReport) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(sla_evaluation_report_to_dict(report), f, indent=2)
    return path

def write_performance_gate_result_json(path: Path, result: PerformanceAcceptanceGateResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(performance_acceptance_gate_result_to_dict(result), f, indent=2)
    return path

def write_performance_alerts_jsonl(path: Path, alerts: List[PerformanceAlert]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        for a in alerts:
            f.write(json.dumps(performance_alert_to_dict(a)) + "\n")
    return path

def write_performance_review_result_json(path: Path, result: PerformanceReviewResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        json.dump(performance_review_result_to_dict(result), f, indent=2)
    return path

def read_performance_baseline_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def read_performance_review_result_json(path: Path) -> Dict[str, Any]:
    with open(path, 'r') as f:
        return json.load(f)

def list_performance_baselines(data_root: Path) -> List[Path]:
    d = baselines_dir(data_root)
    return sorted(d.rglob("*.json"), reverse=True)

def list_performance_reviews(data_root: Path) -> List[Path]:
    d = reviews_dir(data_root)
    return sorted(d.glob("*.json"), reverse=True)

def get_latest_performance_baseline(data_root: Path, scope: Optional[PerformanceBaselineScope] = None) -> Optional[Path]:
    baselines = list_performance_baselines(data_root)
    if not baselines:
        return None
    if not scope:
        return baselines[0]

    for b in baselines:
        if scope.value.lower() in b.name.lower():
            return b
    return None

def get_latest_performance_review(data_root: Path) -> Optional[Path]:
    reviews = list_performance_reviews(data_root)
    return reviews[0] if reviews else None

def baseline_store_summary(data_root: Path) -> Dict[str, Any]:
    baselines = list_performance_baselines(data_root)
    reviews = list_performance_reviews(data_root)
    return {
        "baseline_count": len(baselines),
        "review_count": len(reviews),
        "latest_baseline": str(baselines[0].name) if baselines else None,
        "latest_review": str(reviews[0].name) if reviews else None
    }
