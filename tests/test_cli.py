import pytest
import argparse
from usa_signal_bot.app.cli import phase126_regime_foundation_info, phase126_regime_taxonomy_info

def test_phase126_regime_foundation_info(capsys):
    phase126_regime_foundation_info(None)
    out, err = capsys.readouterr()
    assert "USA Signal Bot - Phase 126" in out
    assert "NOT an active paper trading phase" in out

def test_phase126_regime_taxonomy_info(capsys):
    class Args:
        write = False
    phase126_regime_taxonomy_info(Args())
    out, err = capsys.readouterr()
    assert "Taxonomy ID" in out
    assert "unknown_regime" in out
