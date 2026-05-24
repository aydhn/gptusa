import pytest
from usa_signal_bot.pre_paper_handoff_freeze_gate.simulator_dossier_adapter import handoff_freeze_full_review_from_simulator_dossier

def test_handoff_freeze_full_review_from_simulator_dossier():
    payload = {
        "candidate_id": "cand-1",
        "simulator_dossier": {"decision": "CREATE_SIMULATOR_DOSSIER"}
    }
    review = handoff_freeze_full_review_from_simulator_dossier(payload)
    assert review.gates[0].candidate_id == "cand-1"
