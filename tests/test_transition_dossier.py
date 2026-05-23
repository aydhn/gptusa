
from usa_signal_bot.paper_no_write_transition.transition_dossier import build_default_no_write_transition_dossier
def test_build_dossier():
    assert build_default_no_write_transition_dossier() is not None
