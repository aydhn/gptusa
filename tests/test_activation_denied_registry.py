from usa_signal_bot.paper_readiness_confirmation.activation_denied_registry import (
    build_activation_still_denied_registry_entry,
    register_activation_still_denied_entry
)
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle
from usa_signal_bot.core.enums import ActivationStillDeniedRegistryStatus

def test_build_activation_still_denied_registry_entry():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    r = build_activation_still_denied_registry_entry(q, b)

    assert r.status == ActivationStillDeniedRegistryStatus.DRAFT
    assert r.activation_denied is True
    assert r.activation_allowed is False

def test_register_activation_still_denied_entry():
    q = build_default_confirmation_queue_item()
    r = build_activation_still_denied_registry_entry(q)
    reg = register_activation_still_denied_entry(r)

    assert len(reg) == 1
    assert reg[0].status == ActivationStillDeniedRegistryStatus.REGISTERED

def test_register_activation_still_denied_entry_fail():
    q = build_default_confirmation_queue_item()
    r = build_activation_still_denied_registry_entry(q)
    r.activation_allowed = True
    reg = register_activation_still_denied_entry(r)

    assert len(reg) == 1
    assert reg[0].status == ActivationStillDeniedRegistryStatus.BLOCKED
