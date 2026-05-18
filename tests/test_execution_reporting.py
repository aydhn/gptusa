import pytest
from usa_signal_bot.research_execution.execution_reporting import research_execution_limitations_text

def test_research_execution_limitations_text():
    text = research_execution_limitations_text()
    assert "NOT investment advice" in text
    assert "strictly local analytics" in text
