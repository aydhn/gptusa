from pathlib import Path
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_store import board_dossier_store_dir

def test_board_dossier_store_dir():
    assert board_dossier_store_dir(Path("/tmp")).name == "paper_readiness_board_dossier"
