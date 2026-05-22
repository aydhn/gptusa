from usa_signal_bot.paper_readiness_confirmation.confirmation_safety_validator import validate_confirmation_safety
from usa_signal_bot.paper_readiness_confirmation.confirmation_queue import build_default_confirmation_queue_item
from usa_signal_bot.paper_readiness_confirmation.human_review_bundle import build_human_review_bundle
from usa_signal_bot.core.enums import ReadinessConfirmationRiskFlag

def test_validate_confirmation_safety():
    q = build_default_confirmation_queue_item()
    b = build_human_review_bundle(q)
    errors = validate_confirmation_safety(q, b)
    assert len(errors) == 0

def test_validate_confirmation_safety_block():
    q = build_default_confirmation_queue_item()
    q.safety_flags.append(ReadinessConfirmationRiskFlag.ACTIVATION_ALLOWED_RISK)
    b = build_human_review_bundle(q)
    errors = validate_confirmation_safety(q, b)
    assert len(errors) == 1
    assert "blocking safety flags" in errors[0]
