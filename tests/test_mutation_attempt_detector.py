import pytest
from usa_signal_bot.paper_pre_rehearsal.mutation_attempt_detector import detect_mutation_attempts_in_payload, detect_mutation_attempts_in_text
from usa_signal_bot.core.enums import MutationAttemptType

def test_detect_payload():
    payload = {"paper_state_committed": True}
    attempts = detect_mutation_attempts_in_payload(payload)
    assert MutationAttemptType.PAPER_STATE_WRITE in attempts

def test_detect_text():
    text = "paper'a uygula ve emir gönder"
    attempts = detect_mutation_attempts_in_text(text)
    assert MutationAttemptType.PAPER_STATE_WRITE in attempts
    assert MutationAttemptType.BROKER_ORDER_SEND in attempts
