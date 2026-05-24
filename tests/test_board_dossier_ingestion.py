from usa_signal_bot.paper_readiness_board_dossier.non_execution_board_ingestion import ingest_non_execution_board_full_review

def test_non_execution_board_ingestion():
    payload = {
        "non_execution_board": {"decision": "PASS_TO_NON_EXECUTION_BOARD_DOSSIER"}
    }
    result = ingest_non_execution_board_full_review(payload)
    assert result["decision"] == "PASS_TO_NON_EXECUTION_BOARD_DOSSIER"
