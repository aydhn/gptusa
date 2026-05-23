
from usa_signal_bot.paper_no_write_transition.evidence_seal_validator import validate_admission_evidence_seal_from_payload
def test_seal_validator():
    assert validate_admission_evidence_seal_from_payload({}) is not None
