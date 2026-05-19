from usa_signal_bot.release_packaging.artifact_freezer import freeze_artifact_payload
from usa_signal_bot.core.enums import FrozenArtifactSource, FrozenArtifactStatus

def test_freezer():
    art = freeze_artifact_payload({"test": 1}, FrozenArtifactSource.MANUAL_PAYLOAD, "manual")
    assert art.status == FrozenArtifactStatus.FROZEN
