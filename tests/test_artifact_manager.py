import pytest
from usa_signal_bot.core.enums import ExperimentArtifactType
from usa_signal_bot.research_execution.artifact_manager import artifact_payload_checksum, create_artifact_from_payload, summarize_artifacts

def test_create_artifact_from_payload_redacts_secrets_in_checksum():
    payload = {"metrics": {"a": 1}, "api_key": "hidden"}
    art = create_artifact_from_payload("r1", ExperimentArtifactType.BACKTEST_RESULT, payload)
    assert "api_key" in art.payload_summary["keys"]
