from usa_signal_bot.paper_readiness_board_dossier.eligibility_checker import evaluate_board_dossier_eligibility
from usa_signal_bot.core.enums import PaperReadinessBoardDossierDecision

def test_eligibility_checker_valid():
    payload = {
        "non_execution_board": {"decision": "PASS_TO_NON_EXECUTION_BOARD_DOSSIER"},
        "runtime_replay_result": {"status": "COMPLETED_ROUTE_SAFE"},
        "seal_integrity_audit": {"status": "VALIDATED"}
    }
    assert evaluate_board_dossier_eligibility(payload) == PaperReadinessBoardDossierDecision.CREATE_BOARD_DOSSIER
