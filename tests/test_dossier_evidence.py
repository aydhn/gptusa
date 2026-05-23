
from usa_signal_bot.paper_no_write_transition.dossier_evidence import required_transition_dossier_evidence_types
def test_evidence_types():
    assert len(required_transition_dossier_evidence_types()) > 0
