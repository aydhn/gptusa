from usa_signal_bot.paper_readiness_board_dossier.final_shadow_launch_blocker import FinalPaperModeShadowLaunchBlocker
from usa_signal_bot.core.enums import ShadowLaunchAttemptType

def test_final_shadow_launch_blocker():
    blocker = FinalPaperModeShadowLaunchBlocker()
    event = blocker.evaluate_attempt(ShadowLaunchAttemptType.START_PAPER_MODE)
    assert event.blocked is True
    assert event.shadow_launch_allowed is False
