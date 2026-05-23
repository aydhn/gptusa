from usa_signal_bot.paper_safe_dossier.non_execution_acceptance_seal import build_non_execution_acceptance_seal
from usa_signal_bot.core.enums import NonExecutionAcceptanceSealStatus

def test_non_execution_acceptance_seal():
    payload = {
        "review_id": "r1",
        "gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}],
    }

    seal = build_non_execution_acceptance_seal(payload)
    assert seal.status == NonExecutionAcceptanceSealStatus.SEALED
    assert seal.sealed is True
    assert seal.immutable is True
    assert seal.non_execution_confirmed is True
    assert seal.no_broker_confirmed is True
    assert seal.seal_is_metadata_only is True
