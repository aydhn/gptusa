import pytest
from unittest.mock import MagicMock, patch
import sys
import importlib


class MockExceptions:
    class ReleaseSandboxValidationError(Exception):
        pass


# We can safely mock the broken enums globally just for this specific test
# so the module can actually be imported by pytest
mock_exceptions = MockExceptions()


@pytest.fixture(autouse=True)
def mock_broken_dependencies():
    with patch.dict(
        "sys.modules",
        {
            "usa_signal_bot.core.enums": MagicMock(),
            "usa_signal_bot.core.exceptions": mock_exceptions,
        },
    ):
        yield


def test_attach_sandbox_preview_to_execution_payload():
    # Due to the pytest collection phase, it might be safer to import it inside the test
    with patch.dict(
        "sys.modules",
        {
            "usa_signal_bot.core.enums": MagicMock(),
            "usa_signal_bot.core.exceptions": mock_exceptions,
        },
    ):
        from usa_signal_bot.release_sandbox.research_execution_adapter import (
            attach_sandbox_preview_to_execution_payload,
        )

        initial_payload = {"execution_id": "exec_123"}
        mock_output = MagicMock()
        mock_output.output_id = "prev_abc"

        updated_payload = attach_sandbox_preview_to_execution_payload(
            initial_payload, mock_output
        )

        assert "sandbox_preview_id" in updated_payload
        assert updated_payload["sandbox_preview_id"] == "prev_abc"
        assert updated_payload["execution_id"] == "exec_123"

def test_research_execution_adapter_to_text():
    with patch.dict(
        "sys.modules",
        {
            "usa_signal_bot.core.enums": MagicMock(),
            "usa_signal_bot.core.exceptions": mock_exceptions,
        },
    ):
        from usa_signal_bot.release_sandbox.research_execution_adapter import (
            research_execution_adapter_to_text,
        )

        # Test when has_sandbox_preview is False
        payload_false = {"execution_id": "exec_123"}
        result_false = research_execution_adapter_to_text(payload_false)
        assert result_false == "Research Execution Adapter: Has Sandbox Preview = False"

        # Test when has_sandbox_preview is True
        payload_true = {"execution_id": "exec_123", "sandbox_preview_id": "prev_abc"}
        result_true = research_execution_adapter_to_text(payload_true)
        assert result_true == "Research Execution Adapter: Has Sandbox Preview = True"
