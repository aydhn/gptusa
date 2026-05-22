import pytest
from usa_signal_bot.paper_pre_rehearsal.mutation_firewall import PaperStateMutationFirewall
from usa_signal_bot.paper_pre_rehearsal.forbidden_operation_simulator import simulate_forbidden_operations

def test_simulate():
    fw = PaperStateMutationFirewall()
    events = simulate_forbidden_operations(fw)
    assert all(e.blocked for e in events)
