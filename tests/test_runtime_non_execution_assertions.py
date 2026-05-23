from usa_signal_bot.paper_safe_dossier.runtime_non_execution_assertions import check_runtime_non_execution_assertions, failed_runtime_non_execution_assertions
from usa_signal_bot.paper_safe_dossier.local_runtime_map import build_pre_paper_local_runtime_map

def test_runtime_non_execution_assertions():
    payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}]}
    rmap = build_pre_paper_local_runtime_map(payload)

    res = check_runtime_non_execution_assertions(runtime_map=rmap)
    assert res["no_broker_execution"] is True
    assert res["metadata_only_runtime_map"] is True

    failed = failed_runtime_non_execution_assertions(res)
    assert len(failed) == 0
