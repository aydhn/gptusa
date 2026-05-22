from usa_signal_bot.paper_readiness_confirmation.registry_validator import (
    validate_activation_denied_registry_entry_safety,
    registry_entry_blocks_next_stage
)
from usa_signal_bot.paper_readiness_confirmation.activation_denied_registry import build_activation_still_denied_registry_entry
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item

def test_validate_activation_denied_registry_entry_safety():
    q = build_default_confirmation_queue_item()
    r = build_activation_still_denied_registry_entry(q)
    errors = validate_activation_denied_registry_entry_safety(r)
    assert len(errors) == 0
    assert not registry_entry_blocks_next_stage(r)

def test_validate_activation_denied_registry_entry_safety_fail():
    q = build_default_confirmation_queue_item()
    r = build_activation_still_denied_registry_entry(q)
    r.activation_allowed = True
    errors = validate_activation_denied_registry_entry_safety(r)
    assert len(errors) == 1
    assert "activation_allowed must be False" in errors[0]
    assert registry_entry_blocks_next_stage(r)
