
from usa_signal_bot.paper_no_order_dossier.no_order_session_dossier import build_no_order_paper_session_dossier

def test_build_no_order_paper_session_dossier():
    dossier = build_no_order_paper_session_dossier({})
    assert dossier.sealed is True
    assert dossier.allows_broker_execution is False
