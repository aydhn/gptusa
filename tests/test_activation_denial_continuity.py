from usa_signal_bot.paper_readiness_confirmation.activation_denial_continuity import (
    validate_activation_denial_continuity,
    activation_denial_is_preserved
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle
from usa_signal_bot.paper_readiness_confirmation.activation_denied_registry import build_activation_still_denied_registry_entry

def test_validate_activation_denial_continuity():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    r = build_activation_still_denied_registry_entry(q, b)

    errors = validate_activation_denial_continuity(q, b, r)
    assert len(errors) == 0

def test_validate_activation_denial_continuity_fail():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    b.activation_allowed = True

    errors = validate_activation_denial_continuity(q, b)
    assert len(errors) == 1
    assert "Bundle allows activation" in errors[0]

def test_activation_denial_is_preserved():
    assert activation_denial_is_preserved({"activation_denied": True, "activation_allowed": False}) is True
    assert activation_denial_is_preserved({"activation_denied": True, "activation_allowed": True}) is False
    assert activation_denial_is_preserved({"activation_denied": False, "activation_allowed": False}) is False
