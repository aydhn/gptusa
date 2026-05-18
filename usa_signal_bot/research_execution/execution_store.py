import json
from pathlib import Path
from typing import Any

from usa_signal_bot.research_execution.execution_models import (
    ConfigSnapshot, ExperimentRunContext, ResearchRun, ExperimentArtifact,
    ExperimentComparisonReport, ResearchExecutionReview,
    config_snapshot_to_dict, experiment_run_context_to_dict, research_run_to_dict,
    experiment_artifact_to_dict, experiment_comparison_report_to_dict, research_execution_review_to_dict
)

def execution_store_dir(data_root: Path) -> Path:
    d = data_root / "research_execution"
    d.mkdir(parents=True, exist_ok=True)
    return d

def config_snapshots_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "config_snapshots"
    d.mkdir(parents=True, exist_ok=True)
    return d

def run_contexts_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "run_contexts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def research_runs_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "research_runs"
    d.mkdir(parents=True, exist_ok=True)
    return d

def artifacts_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "artifacts"
    d.mkdir(parents=True, exist_ok=True)
    return d

def comparison_reports_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "comparison_reports"
    d.mkdir(parents=True, exist_ok=True)
    return d

def execution_reviews_dir(data_root: Path) -> Path:
    d = execution_store_dir(data_root) / "reviews"
    d.mkdir(parents=True, exist_ok=True)
    return d

def write_config_snapshot_json(path: Path, item: ConfigSnapshot) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config_snapshot_to_dict(item), f, indent=2)
    return path

def write_run_context_json(path: Path, item: ExperimentRunContext) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(experiment_run_context_to_dict(item), f, indent=2)
    return path

def write_research_run_json(path: Path, item: ResearchRun) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(research_run_to_dict(item), f, indent=2)
    return path

def write_experiment_artifacts_jsonl(path: Path, items: list[ExperimentArtifact]) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(experiment_artifact_to_dict(item)) + "\n")
    return path

def write_comparison_report_json(path: Path, item: ExperimentComparisonReport) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(experiment_comparison_report_to_dict(item), f, indent=2)
    return path

def write_research_execution_review_json(path: Path, item: ResearchExecutionReview) -> Path:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(research_execution_review_to_dict(item), f, indent=2)
    return path

def read_research_execution_review_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_research_execution_reviews(data_root: Path) -> list[Path]:
    d = execution_reviews_dir(data_root)
    return sorted(d.glob("*.json"))

def get_latest_research_execution_review(data_root: Path) -> Path | None:
    files = list_research_execution_reviews(data_root)
    return files[-1] if files else None

def execution_store_summary(data_root: Path) -> dict[str, Any]:
    return {
        "snapshots": len(list(config_snapshots_dir(data_root).glob("*.json"))),
        "contexts": len(list(run_contexts_dir(data_root).glob("*.json"))),
        "runs": len(list(research_runs_dir(data_root).glob("*.json"))),
        "reports": len(list(comparison_reports_dir(data_root).glob("*.json"))),
        "reviews": len(list(execution_reviews_dir(data_root).glob("*.json")))
    }
