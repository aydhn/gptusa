
from usa_signal_bot.paper_no_order_dossier.final_paper_admission_blocker import FinalPaperAdmissionBlocker
from usa_signal_bot.core.enums import PaperAdmissionAttemptType

def test_final_paper_admission_blocker_denies():
    blocker = FinalPaperAdmissionBlocker()
    assert blocker.admission_allowed(PaperAdmissionAttemptType.ENABLE_ACTIVE_PAPER) is False
    event = blocker.evaluate_attempt(PaperAdmissionAttemptType.ENABLE_ACTIVE_PAPER)
    assert event.blocked is True
