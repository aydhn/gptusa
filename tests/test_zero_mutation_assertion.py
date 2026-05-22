import pytest
from usa_signal_bot.paper_pre_rehearsal.zero_mutation_assertion import assert_zero_paper_mutation_before_after

def test_zero_mutation():
    before = {"a": 1}
    after = {"a": 1}
    violations = assert_zero_paper_mutation_before_after(before, after)
    assert len(violations) == 0

    after["paper_state_committed"] = True
    violations = assert_zero_paper_mutation_before_after(before, after)
    assert len(violations) > 0
