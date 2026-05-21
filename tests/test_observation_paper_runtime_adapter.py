from usa_signal_bot.paper_observation.paper_runtime_adapter import (
    build_read_only_paper_observation_snapshot, compare_observation_to_paper_snapshot,
    validate_paper_snapshot_not_mutated_for_observation, attach_observation_metadata_to_paper_analytics,
    paper_runtime_observation_adapter_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_paper_runtime_adapter():
    snap = build_read_only_paper_observation_snapshot()
    assert snap["read_only"] is True
    assert snap["paper_state_committed"] is False

    rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [], [], [], [], [], [], {})
    comp = compare_observation_to_paper_snapshot(rev, snap)
    assert "diff" in comp

    errors = validate_paper_snapshot_not_mutated_for_observation(snap, {"paper_state_committed": True})
    assert len(errors) == 1

    pl = attach_observation_metadata_to_paper_analytics({}, rev)
    assert "observation_metadata" in pl

    text = paper_runtime_observation_adapter_to_text({})
    assert "Adapter Info" in text
