import pytest
from usa_signal_bot.paper_pre_rehearsal.activation_denied_checkpoint import default_activation_denied_checkpoint
from usa_signal_bot.paper_pre_rehearsal.checkpoint_validator import validate_activation_checkpoint_safety

def test_validate():
    cp = default_activation_denied_checkpoint()
    violations = validate_activation_checkpoint_safety(cp)
    assert len(violations) == 0
