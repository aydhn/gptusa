
from usa_signal_bot.paper_no_order_dossier.no_order_dossier_store import no_order_dossier_store_dir
from pathlib import Path

def test_no_order_dossier_store_dir(tmp_path):
    d = no_order_dossier_store_dir(tmp_path)
    assert d.exists()
