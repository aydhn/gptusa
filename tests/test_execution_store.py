import pytest
from pathlib import Path
from usa_signal_bot.research_execution.execution_store import execution_store_dir, write_research_run_json
from usa_signal_bot.research_execution.execution_models import ResearchRun
from usa_signal_bot.core.enums import ResearchRunType, ResearchRunStatus, ExperimentExecutionMode

def test_execution_store_dirs(tmp_path):
    d = execution_store_dir(tmp_path)
    assert d.exists()
    assert d.name == "research_execution"

def test_write_research_run_json(tmp_path):
    run = ResearchRun(
        run_id="r1", created_at_utc="now", experiment_id="exp_1", hypothesis_id=None,
        run_type=ResearchRunType.BASELINE, status=ResearchRunStatus.COMPLETED,
        execution_mode=ExperimentExecutionMode.MOCK_ONLY, context=None, artifacts=[],
        metrics={"a": 1}, started_at_utc="now", completed_at_utc="now", warnings=[], errors=[], metadata={}
    )
    p = tmp_path / "r1.json"
    write_research_run_json(p, run)
    assert p.exists()
    content = p.read_text()
    assert '"r1"' in content
