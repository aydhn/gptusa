
import pytest

from pathlib import Path
from usa_signal_bot.integration.phase157_handoff_artifact_loader import _load_json_safe
from usa_signal_bot.core.exceptions import Phase158HandoffArtifactLoaderError

from usa_signal_bot.integration.phase158_models import Phase158HandoffIngestionResult

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
        _load_json_safe(Path("../some/path.json"))

def test_load_json_safe_file_not_found():
    with pytest.raises(Phase158HandoffArtifactLoaderError, match="File not found: "):
        _load_json_safe(Path("non_existent_file_12345.json"))

def test_load_json_safe_json_decode_error(tmp_path):
    invalid_json_file = tmp_path / "invalid.json"
    invalid_json_file.write_text("not a valid json")

    with pytest.raises(Phase158HandoffArtifactLoaderError, match="Error loading JSON from "):
        _load_json_safe(invalid_json_file)
