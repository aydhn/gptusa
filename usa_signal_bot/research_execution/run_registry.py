from typing import Any
from usa_signal_bot.research_execution.execution_models import ResearchRun

def register_research_run(run: ResearchRun, registry: list[ResearchRun] | None = None) -> list[ResearchRun]:
    if registry is None:
        registry = []
    registry.append(run)
    return registry

def find_run_by_id(registry: list[ResearchRun], run_id: str) -> ResearchRun | None:
    for run in registry:
        if run.run_id == run_id:
            return run
    return None

def find_runs_by_experiment_id(registry: list[ResearchRun], experiment_id: str) -> list[ResearchRun]:
    return [run for run in registry if run.experiment_id == experiment_id]

def latest_run_for_experiment(registry: list[ResearchRun], experiment_id: str) -> ResearchRun | None:
    runs = find_runs_by_experiment_id(registry, experiment_id)
    if not runs:
        return None
    runs.sort(key=lambda r: r.created_at_utc)
    return runs[-1]

def run_registry_summary(registry: list[ResearchRun]) -> dict[str, Any]:
    return {
        "total_runs": len(registry),
        "unique_experiments": len(set(r.experiment_id for r in registry if r.experiment_id)),
        "completed_runs": len([r for r in registry if r.status.value == "COMPLETED"]),
        "failed_runs": len([r for r in registry if r.status.value == "FAILED"])
    }

def run_registry_to_text(registry: list[ResearchRun], limit: int = 100) -> str:
    summary = run_registry_summary(registry)
    lines = ["--- RUN REGISTRY SUMMARY ---"]
    for k, v in summary.items():
        lines.append(f"{k}: {v}")

    lines.append("\nRecent Runs:")
    sorted_runs = sorted(registry, key=lambda r: r.created_at_utc, reverse=True)[:limit]
    for r in sorted_runs:
        lines.append(f"  - {r.run_id} ({r.run_type.value}) - {r.status.value}")

    return "\n".join(lines)
