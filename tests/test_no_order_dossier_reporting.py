
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_reporting import no_order_dossier_limitations_text

def test_no_order_dossier_limitations_text():
    text = no_order_dossier_limitations_text()
    assert "NOT an active paper trading approval" in text
