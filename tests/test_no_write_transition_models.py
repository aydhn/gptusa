
from usa_signal_bot.paper_no_write_transition.no_write_transition_models import create_transition_dossier_id
def test_create_dossier_id():
    assert create_transition_dossier_id() is not None
