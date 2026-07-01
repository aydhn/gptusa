import pytest
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


from unittest.mock import patch
from usa_signal_bot.integration.integration_input_resolver import (
    detect_forbidden_integration_fields,
)


def test_detect_forbidden_integration_fields_logs_warning_on_serialization_error():
    class Unserializable:
        pass

    with patch(
        "usa_signal_bot.integration.integration_input_resolver.logger.warning"
    ) as mock_warning:
        payload = {"key": Unserializable()}
        detected = detect_forbidden_integration_fields(payload)

        assert detected == []
        mock_warning.assert_called_once()
        assert (
            "Failed to serialize payload for forbidden field detection: %s"
            in mock_warning.call_args[0][0]
        )
