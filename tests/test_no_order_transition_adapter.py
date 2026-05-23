
from usa_signal_bot.paper_no_order_dossier.transition_adapter import transition_supports_no_order_dossier

def test_transition_supports_no_order_dossier():
    supports, _ = transition_supports_no_order_dossier({"activation_allowed": False, "all_writes_blocked": True})
    assert supports is True
