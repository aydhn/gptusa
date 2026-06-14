import pytest
import usa_signal_bot.release


def test_release_init():
    """
    Test that the release module can be imported and has a valid docstring.
    """
    assert usa_signal_bot.release.__doc__ is not None
    assert "Phase 159 Advanced Acceptance Rehearsal" in usa_signal_bot.release.__doc__
