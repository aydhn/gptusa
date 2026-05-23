
from usa_signal_bot.paper_no_order_dossier.bridge_adapter import no_order_dossier_from_bridge

def test_no_order_dossier_from_bridge():
    dossier = no_order_dossier_from_bridge({})
    assert dossier.all_writes_blocked is True
