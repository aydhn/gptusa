import pytest
from usa_signal_bot.paper_observer.blocked_operation_guard import (
    assert_observer_operation_allowed,
    observer_operation_allowed,
    observer_blocked_operation_flags
)
from usa_signal_bot.core.exceptions import ObserverBlockedOperationError
from usa_signal_bot.core.enums import ObserverSafetyFlag

def test_observer_operation_allowed():
    assert observer_operation_allowed("read_paper_snapshot") is True
    assert observer_operation_allowed("send_paper_order") is False
    assert observer_operation_allowed("write_paper_state") is False

def test_assert_observer_operation_allowed():
    assert_observer_operation_allowed("read_data")

    with pytest.raises(ObserverBlockedOperationError):
        assert_observer_operation_allowed("send_telegram_real")

def test_observer_blocked_operation_flags():
    flags = observer_blocked_operation_flags("write_paper_state")
    assert ObserverSafetyFlag.PAPER_STATE_MUTATION_RISK in flags
