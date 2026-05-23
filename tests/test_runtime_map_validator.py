from usa_signal_bot.paper_safe_dossier.local_runtime_map import build_pre_paper_local_runtime_map
from usa_signal_bot.paper_safe_dossier.runtime_map_validator import validate_pre_paper_runtime_map_safety

def test_runtime_map_validator():
    payload = {"gates": [{"gate_id": "g1", "candidate_id": "c1", "decision": "VALIDATED_PAPER_SAFE"}]}
    rmap = build_pre_paper_local_runtime_map(payload)

    errors = validate_pre_paper_runtime_map_safety(rmap)
    assert len(errors) == 0

    rmap.map_is_metadata_only = False
    errors = validate_pre_paper_runtime_map_safety(rmap)
    assert len(errors) > 0

    rmap.map_is_metadata_only = True
    rmap.component_items[0].write_allowed = True
    errors = validate_pre_paper_runtime_map_safety(rmap)
    assert len(errors) > 0
