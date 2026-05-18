from datetime import datetime, timezone
from typing import Any

from usa_signal_bot.core.enums import ResearchRunStatus, ResearchRunType, ExperimentArtifactType
from usa_signal_bot.research_execution.execution_models import ExperimentRunContext, ResearchRun, ExperimentArtifact, create_research_run_id, create_experiment_artifact_id

def run_mock_experiment(context: ExperimentRunContext) -> ResearchRun:
    run_id = create_research_run_id()
    started_at = datetime.now(timezone.utc).isoformat()

    metrics = build_mock_metrics(context.run_type)
    artifacts = build_mock_artifacts(run_id)

    completed_at = datetime.now(timezone.utc).isoformat()

    return ResearchRun(
        run_id=run_id,
        created_at_utc=started_at,
        experiment_id=context.experiment_id,
        hypothesis_id=context.hypothesis_id,
        run_type=context.run_type,
        status=ResearchRunStatus.COMPLETED,
        execution_mode=context.execution_mode,
        context=context,
        artifacts=artifacts,
        metrics=metrics,
        started_at_utc=started_at,
        completed_at_utc=completed_at,
        warnings=["This is a MOCK run. No real logic executed."],
        errors=[],
        metadata={"runner": "mock_runner"}
    )

def build_mock_metrics(run_type: ResearchRunType) -> dict[str, Any]:
    if run_type == ResearchRunType.CANDIDATE:
        return {
            "total_net_pnl_usd": 1500.0,
            "total_gross_pnl_usd": 1800.0,
            "max_drawdown_pct": 10.5,
            "win_rate_pct": 58.2,
            "cost_drag_pct": 2.1,
            "turnover_pct": 120.0,
            "trade_count": 45,
            "walk_forward_pass_ratio": 0.8,
            "robustness_score": 85.0
        }
    else:
        return {
            "total_net_pnl_usd": 1000.0,
            "total_gross_pnl_usd": 1200.0,
            "max_drawdown_pct": 15.0,
            "win_rate_pct": 52.0,
            "cost_drag_pct": 3.0,
            "turnover_pct": 150.0,
            "trade_count": 40,
            "walk_forward_pass_ratio": 0.6,
            "robustness_score": 70.0
        }

def build_mock_artifacts(run_id: str) -> list[ExperimentArtifact]:
    return [
        ExperimentArtifact(
            artifact_id=create_experiment_artifact_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            artifact_type=ExperimentArtifactType.BACKTEST_RESULT,
            run_id=run_id,
            path=f"/mock/path/{run_id}/results.json",
            payload_summary={"records": 100},
            checksum="mockhash123",
            warnings=[],
            errors=[],
            metadata={}
        )
    ]

def mock_run_result_to_text(run: ResearchRun) -> str:
    lines = [f"--- MOCK RUN: {run.run_id} ---"]
    lines.append(f"Status: {run.status.value}")
    lines.append("Metrics:")
    for k, v in run.metrics.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)
