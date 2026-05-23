
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_models import create_no_order_dossier_id

def test_create_no_order_dossier_id():
    d_id = create_no_order_dossier_id()
    assert d_id.startswith("no_order_dossier_")
