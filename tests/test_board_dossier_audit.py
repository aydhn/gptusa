from usa_signal_bot.paper_readiness_board_dossier.board_dossier import build_default_board_dossier
from usa_signal_bot.paper_readiness_board_dossier.board_dossier_audit import audit_entry_from_board_dossier

def test_audit_entry_from_board_dossier():
    dossier = build_default_board_dossier()
    audit = audit_entry_from_board_dossier(dossier)
    assert audit.action == "BUILD_BOARD_DOSSIER"
