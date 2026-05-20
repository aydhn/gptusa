import pytest
from usa_signal_bot.paper_quarantine.quarantine_reporting import (
    quarantine_limitations_text
)

def test_reporting():
    t = quarantine_limitations_text()
    assert "No broker" in t
