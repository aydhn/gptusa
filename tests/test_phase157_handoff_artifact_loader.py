import pytest
import json
from pathlib import Path
from unittest.mock import mock_open, patch

from usa_signal_bot.integration.phase158_models import Phase158HandoffIngestionResult
from usa_signal_bot.integration.phase157_handoff_artifact_loader import _load_json_safe
from usa_signal_bot.core.exceptions import Phase158HandoffArtifactLoaderError

def test_phase158_models_import():
    # Simple check that the model instantiates properly
    res = Phase158HandoffIngestionResult()
    assert res.read_only is True
    assert res.live_trading_enabled is False

def test_no_side_effects():
    # A generic test affirming local phase policy
    res = Phase158HandoffIngestionResult()
    assert not res.paper_state_mutation_enabled
    assert not res.broker_execution_enabled
    assert not res.telegram_real_send_enabled
    assert not res.real_order_creation_enabled
    assert not res.deployment_allowed

def test_load_json_safe_path_traversal():
    with pytest.raises(Phase158HandoffArtifactLoaderError, match="Path traversal attempt detected."):
        _load_json_safe(Path("../secret.json"))

def test_load_json_safe_file_not_found(tmp_path):
    non_existent_file = tmp_path / "does_not_exist.json"
    with pytest.raises(Phase158HandoffArtifactLoaderError, match="File not found:"):
        _load_json_safe(non_existent_file)

def test_load_json_safe_happy_path(tmp_path):
    json_file = tmp_path / "valid.json"
    valid_data = {"key": "value"}
    json_file.write_text(json.dumps(valid_data))

    result = _load_json_safe(json_file)
    assert result == valid_data

@patch("usa_signal_bot.integration.phase157_handoff_artifact_loader.open")
def test_load_json_safe_read_error(mock_open_file, tmp_path):
    json_file = tmp_path / "error.json"
    # Create the file so it passes the .exists() check
    json_file.touch()

    # Force open() to raise an exception to test the Exception block
    mock_open_file.side_effect = PermissionError("Permission denied")

    with pytest.raises(Phase158HandoffArtifactLoaderError, match="Error loading JSON from"):
        _load_json_safe(json_file)
