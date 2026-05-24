from usa_signal_bot.paper_readiness_board_dossier.acceptance_board_seal import build_default_acceptance_board_seal
from usa_signal_bot.paper_readiness_board_dossier.acceptance_board_seal_validator import validate_acceptance_board_seal_safety

def test_validate_acceptance_board_seal_safety():
    seal = build_default_acceptance_board_seal()
    # It will have issues because passed fields are false
    assert len(validate_acceptance_board_seal_safety(seal)) > 0
