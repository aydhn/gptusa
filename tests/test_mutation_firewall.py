import pytest
from usa_signal_bot.paper_pre_rehearsal.mutation_firewall import PaperStateMutationFirewall
from usa_signal_bot.core.enums import MutationAttemptType

def test_firewall_eval():
    fw = PaperStateMutationFirewall()
    event = fw.evaluate_attempt(MutationAttemptType.PAPER_STATE_WRITE)
    assert event.blocked
