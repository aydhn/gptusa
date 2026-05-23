from usa_signal_bot.paper_safe_dossier.local_runtime_map import build_pre_paper_local_runtime_map
from usa_signal_bot.core.enums import PrePaperRuntimeMapStatus, RuntimeComponentMode

def test_local_runtime_map():
    payload = {
        "gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}],
    }

    rmap = build_pre_paper_local_runtime_map(payload)
    assert rmap.status == PrePaperRuntimeMapStatus.VALIDATED_READ_ONLY
    assert rmap.map_is_metadata_only is True
    assert rmap.all_write_routes_denied is True
    assert len(rmap.component_items) > 0
    assert len(rmap.route_items) > 0

    writer = [c for c in rmap.component_items if c.component_name == "paper_state_writer_blocked"][0]
    assert writer.mode == RuntimeComponentMode.WRITE_BLOCKED
    assert writer.write_allowed is False
