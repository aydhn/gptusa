from usa_signal_bot.paper_readiness_board_dossier.board_dossier import build_default_board_dossier
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_reporting import paper_readiness_board_dossier_to_text

def test_paper_readiness_board_dossier_to_text():
    dossier = build_default_board_dossier()
    text = paper_readiness_board_dossier_to_text(dossier)
    assert "False (GUARANTEED)" in text
