from usa_signal_bot.paper_readiness_board_dossier.board_dossier_continuity import validate_board_dossier_continuity
from usa_signal_bot.paper_readiness_board_dossier.board_dossier import build_default_board_dossier

def test_validate_board_dossier_continuity():
    dossier = build_default_board_dossier()
    issues = validate_board_dossier_continuity(dossier)
    assert len(issues) == 0
