import pytest
from usa_signal_bot.regression.release_rehearsal import ReleaseCandidateRehearsalRunner
from usa_signal_bot.regression.regression_models import ReleaseRehearsalScope, ReleaseCandidateStatus

def test_release_rehearsal_run(tmp_path):
    runner = ReleaseCandidateRehearsalRunner(tmp_path)
    result = runner.run(scope=ReleaseRehearsalScope.SMOKE_ONLY, write_outputs=False)

    assert result.status in (ReleaseCandidateStatus.PASSED, ReleaseCandidateStatus.PASSED_WITH_WARNINGS)
    assert result.passed_steps > 0
    assert result.regression_result is not None

def test_release_rehearsal_required_actions(tmp_path):
    runner = ReleaseCandidateRehearsalRunner(tmp_path)
    result = runner.run(scope=ReleaseRehearsalScope.SMOKE_ONLY, write_outputs=False)

    # Just checking it builds action lists
    assert isinstance(result.required_actions, list)
    assert isinstance(result.optional_actions, list)
