import pytest
from usa_signal_bot.core.enums import ResourceProfileScope, ResourceProfileStatus
from usa_signal_bot.profiling.profiling_models import ResourceProfile
from usa_signal_bot.profiling.profiling_reporting import resource_profile_to_text, profiling_limitations_text

def test_resource_profile_to_text():
    prof = ResourceProfile("id", ResourceProfileScope.TASK, "t", ResourceProfileStatus.COMPLETED, None, None, 1.0, 0, 0, 1024, 0, 0, 0, 0, [], [], [])
    text = resource_profile_to_text(prof)
    assert "Wall Time: 1.00s" in text

def test_profiling_limitations_text():
    text = profiling_limitations_text()
    assert "NO external telemetry" in text
    assert "APPROXIMATE" in text
    assert "NOT constitute investment advice" in text
