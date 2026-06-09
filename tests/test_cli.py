# Mock simple test for CLI patching without invoking full complex logic.
from usa_signal_bot.app.cli import setup_phase157_cli
import argparse

def test_setup_phase157_cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    setup_phase157_cli(subparsers)
    assert "portfolio-risk-info" in subparsers.choices
