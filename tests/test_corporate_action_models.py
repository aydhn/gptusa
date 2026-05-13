"""Test corporate action models."""
import pytest
from usa_signal_bot.corporate_actions.corporate_action_models import CorporateActionEvent, validate_corporate_action_event
from usa_signal_bot.core.enums import CorporateActionType, CorporateActionSource
from usa_signal_bot.core.exceptions import CorporateActionValidationError

def test_corporate_action_event_valid():
    e = CorporateActionEvent("id", "SPY", CorporateActionType.SPLIT, "2024-01-01", None, 2.0, 1.0, CorporateActionSource.MANUAL_FILE, 1.0)
    validate_corporate_action_event(e)

def test_corporate_action_event_invalid_ratio():
    e = CorporateActionEvent("id", "SPY", CorporateActionType.SPLIT, "2024-01-01", None, -1.0, 1.0, CorporateActionSource.MANUAL_FILE, 1.0)
    with pytest.raises(CorporateActionValidationError):
        validate_corporate_action_event(e)
