from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.core.enums import ResearchRunStatus, ExperimentArtifactType
from usa_signal_bot.research_execution.execution_models import ExperimentRunContext, ResearchRun, ExperimentArtifact, create_research_run_id, create_experiment_artifact_id

def run_backtest_experiment(context: ExperimentRunContext, backtest_callable: Any | None = None) -> ResearchRun:
    run_id = create_research_run_id()
    started_at = datetime.now(timezone.utc).isoformat()

    if backtest_callable is None:
        from usa_signal_bot.research_execution.mock_runner import build_mock_metrics
        metrics = build_mock_metrics(context.run_type)
        payload = {"mock": True, "metrics": metrics}
        status = ResearchRunStatus.COMPLETED
    else:
        try:
            payload = backtest_callable(context)
            metrics = extract_backtest_metrics(payload)
            status = ResearchRunStatus.COMPLETED
        except Exception as e:
            payload = {"error": str(e)}
            metrics = {}
            status = ResearchRunStatus.FAILED

    artifact = build_backtest_artifact(run_id, payload)

    return ResearchRun(
        run_id=run_id,
        created_at_utc=started_at,
        experiment_id=context.experiment_id,
        hypothesis_id=context.hypothesis_id,
        run_type=context.run_type,
        status=status,
        execution_mode=context.execution_mode,
        context=context,
        artifacts=[artifact],
        metrics=metrics,
        started_at_utc=started_at,
        completed_at_utc=datetime.now(timezone.utc).isoformat(),
        warnings=[],
        errors=[payload.get("error")] if "error" in payload else [],
        metadata={"runner": "backtest_runner"}
    )

def extract_backtest_metrics(result_payload: dict[str, Any]) -> dict[str, Any]:
    if "metrics" in result_payload:
        return result_payload["metrics"]
    return {}

def build_backtest_artifact(run_id: str, result_payload: dict[str, Any]) -> ExperimentArtifact:
    return ExperimentArtifact(
        artifact_id=create_experiment_artifact_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        artifact_type=ExperimentArtifactType.BACKTEST_RESULT,
        run_id=run_id,
        path=None,
        payload_summary={"has_error": "error" in result_payload},
        checksum=None,
        warnings=[],
        errors=[],
        metadata={}
    )

def backtest_runner_available() -> bool:
    return True

def backtest_run_to_text(run: ResearchRun) -> str:
    lines = [f"--- BACKTEST RUN: {run.run_id} ---"]
    lines.append(f"Status: {run.status.value}")
    return "\n".join(lines)
