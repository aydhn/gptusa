import pytest
import subprocess
import sys

def test_signal_ranking_summary_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "signal-ranking-summary"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Signal Ranking Storage Summary" in result.stdout

def test_selected_candidates_summary_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "selected-candidates-summary"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Selected Candidates Summary" in result.stdout

def test_strategy_portfolio_run_command_no_feature():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "strategy-portfolio-run", "--strategies", "trend_following_rule", "--symbols", "AAPL"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_rule_strategy_run_ranked_command_no_feature():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "rule-strategy-run-ranked", "--set", "basic_rules", "--symbols", "AAPL"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
