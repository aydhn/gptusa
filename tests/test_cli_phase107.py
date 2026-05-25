import sys
from unittest.mock import patch
from usa_signal_bot.app.cli import main

def test_provider_runtime_info():
    test_args = ["usa_signal_bot", "provider-runtime-info"]
    with patch.object(sys, 'argv', test_args):
        try:
            main()
        except SystemExit as e:
            assert e.code == 0


def test_provider_runtime_policy():
    test_args = ["usa_signal_bot", "provider-runtime-policy"]
    with patch.object(sys, 'argv', test_args):
        try:
            main()
        except SystemExit as e:
            assert e.code == 0


def test_provider_runtime_registry():
    test_args = ["usa_signal_bot", "provider-runtime-registry"]
    with patch.object(sys, 'argv', test_args):
        try:
            main()
        except SystemExit as e:
            assert e.code == 0
