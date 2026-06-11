import pytest
import usa_signal_bot.paper_no_order_dossier as pnod


def test_init_docstring():
    """Test that the __init__.py file has a docstring."""
    assert pnod.__doc__ is not None
    assert "No-Order Paper Session Dossier" in pnod.__doc__
    assert "Bridge Replay Audit Seal" in pnod.__doc__
    assert "Final Paper Admission Blocker subsystem" in pnod.__doc__
    assert "Provides local metadata and strict non-execution validation" in pnod.__doc__
