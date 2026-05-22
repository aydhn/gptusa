import pytest
from usa_signal_bot.paper_pre_rehearsal.activation_denied_checkpoint import default_activation_denied_checkpoint

def test_checkpoint():
    cp = default_activation_denied_checkpoint()
    assert cp.activation_denied
    assert not cp.allows_active_paper
