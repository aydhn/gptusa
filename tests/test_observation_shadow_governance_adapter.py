from usa_signal_bot.paper_observation.shadow_governance_adapter import (
    observation_requirements_from_shadow_governance, shadow_governance_supports_observation,
    attach_observation_hint_to_shadow_governance, shadow_governance_observation_summary,
    shadow_governance_adapter_to_text
)
from usa_signal_bot.paper_observation.observation_models import ObservationReview

def test_shadow_governance_adapter():
    req = observation_requirements_from_shadow_governance({})
    assert req["required_sessions"] == 3

    sup, _ = shadow_governance_supports_observation({})
    assert sup is True

    rev = ObservationReview("r1", "2023", "FULL_OBSERVATION_REVIEW", [], [], [], [], [], [], {})
    pl = attach_observation_hint_to_shadow_governance({}, rev)
    assert "observation_hint" in pl

    summ = shadow_governance_observation_summary({})
    assert summ["shadow_governance"] == "Attached"

    text = shadow_governance_adapter_to_text({})
    assert "Adapter Info" in text
