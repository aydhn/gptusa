import pytest
from usa_signal_bot.core.exceptions import CandidateOverlayError
from usa_signal_bot.research_execution.candidate_overlay import build_candidate_overlay_from_parameter_proposals, validate_candidate_overlay_safe

def test_build_candidate_overlay_from_parameter_proposals():
    props = [
        {"target_parameter": "strategy.threshold", "proposed_value": 0.5},
        {"target_parameter": "risk.max_dd", "proposed_value": 0.2}
    ]
    overlay = build_candidate_overlay_from_parameter_proposals(props)
    assert overlay["strategy"]["threshold"] == 0.5

def test_validate_candidate_overlay_blocks_broker_and_live_fields():
    overlay = {"broker_config": {"api_key": "test"}}
    warnings = validate_candidate_overlay_safe(overlay)
    assert any("BLOCKED" in w for w in warnings)
