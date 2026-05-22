import pytest
from usa_signal_bot.paper_pre_rehearsal.readiness_rehearsal_adapter import readiness_rehearsal_supports_pre_paper_rehearsal

def test_readiness():
    supports, _ = readiness_rehearsal_supports_pre_paper_rehearsal({"sandbox_result": "PASS"})
    assert supports
