
from usa_signal_bot.paper_no_order_dossier.admission_adapter import admission_supports_no_order_dossier

def test_admission_supports_no_order_dossier():
    supports, _ = admission_supports_no_order_dossier({"activation_allowed": False, "all_writes_blocked": True})
    assert supports is True
