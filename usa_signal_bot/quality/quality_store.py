"""Storage for Quality and Acceptance Results."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from usa_signal_bot.core.exceptions import QualityStorageError
from usa_signal_bot.quality.quality_models import (
    ResearchQualityScorecard,
    ProductionReadinessGateResult,
    SystemAcceptanceResult,
    QualityIssue,
    GateRuleResult,
    research_quality_scorecard_to_dict,
    production_readiness_gate_result_to_dict,
    system_acceptance_result_to_dict,
    quality_issue_to_dict,
    gate_rule_result_to_dict
)

def quality_store_dir(data_root: Path) -> Path:
    d = data_root / "quality"
    d.mkdir(parents=True, exist_ok=True)
    return d

def build_quality_run_dir(data_root: Path, acceptance_id: str) -> Path:
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    d = quality_store_dir(data_root) / f"run_{now_str}_{acceptance_id}"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_scorecard_json(path: Path, scorecard: ResearchQualityScorecard) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(research_quality_scorecard_to_dict(scorecard), f, indent=2)
        return path
    except Exception as e:
        raise QualityStorageError(f"Failed to write scorecard: {e}")

def write_gate_result_json(path: Path, gate_result: ProductionReadinessGateResult) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(production_readiness_gate_result_to_dict(gate_result), f, indent=2)
        return path
    except Exception as e:
        raise QualityStorageError(f"Failed to write gate result: {e}")

def write_acceptance_result_json(path: Path, result: SystemAcceptanceResult) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(system_acceptance_result_to_dict(result), f, indent=2)
        return path
    except Exception as e:
        raise QualityStorageError(f"Failed to write acceptance result: {e}")

def write_quality_issues_jsonl(path: Path, issues: List[QualityIssue]) -> Path:
    try:
        with open(path, "w") as f:
            for issue in issues:
                f.write(json.dumps(quality_issue_to_dict(issue)) + "\n")
        return path
    except Exception as e:
        raise QualityStorageError(f"Failed to write issues: {e}")

def write_gate_rule_results_jsonl(path: Path, results: List[GateRuleResult]) -> Path:
    try:
        with open(path, "w") as f:
            for res in results:
                f.write(json.dumps(gate_rule_result_to_dict(res)) + "\n")
        return path
    except Exception as e:
        raise QualityStorageError(f"Failed to write gate rule results: {e}")

def write_quality_artifact_index_json(path: Path, index: Any) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(index, f, indent=2)
        return path
    except Exception as e:
        raise QualityStorageError(f"Failed to write artifact index: {e}")

def write_quality_validation_report_json(path: Path, report: Any) -> Path:
    try:
        with open(path, "w") as f:
            json.dump(report, f, indent=2)
        return path
    except Exception as e:
        raise QualityStorageError(f"Failed to write validation report: {e}")

def read_acceptance_result_json(path: Path) -> Dict[str, Any]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise QualityStorageError(f"Failed to read acceptance result: {e}")

def list_quality_runs(data_root: Path) -> List[Path]:
    d = quality_store_dir(data_root)
    runs = [p for p in d.iterdir() if p.is_dir() and p.name.startswith("run_")]
    runs.sort(key=lambda p: p.name, reverse=True)
    return runs

def get_latest_quality_run_dir(data_root: Path) -> Optional[Path]:
    runs = list_quality_runs(data_root)
    return runs[0] if runs else None

def quality_store_summary(data_root: Path) -> Dict[str, Any]:
    runs = list_quality_runs(data_root)
    return {
        "total_runs": len(runs),
        "latest_run": str(runs[0]) if runs else None
    }
