import sys
import pytest
from unittest.mock import patch
from usa_signal_bot.app.cli import main

@patch.object(sys, 'argv', ['python', 'paper-shadow-info'])
def test_paper_shadow_info(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Paper Shadow System Info" in captured.out

@patch.object(sys, 'argv', ['python', 'shadow-context'])
def test_shadow_context(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Created shadow context" in captured.out

@patch.object(sys, 'argv', ['python', 'shadow-session-run', '--runtime-mode', 'full_paper_shadow', '--equity', '100000'])
def test_shadow_session_run(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Ran shadow session" in captured.out

@patch.object(sys, 'argv', ['python', 'paper-shadow-validate'])
def test_paper_shadow_validate_no_review(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "No latest review found" in captured.out
