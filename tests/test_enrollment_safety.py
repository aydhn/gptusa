import pytest
from usa_signal_bot.core.enums import QuarantineSafetyFlag
from usa_signal_bot.paper_quarantine.quarantine_models import QuarantinedPaperCandidate
from usa_signal_bot.paper_quarantine.enrollment_safety import (
    collect_quarantine_safety_flags,
    quarantine_has_blocking_flags,
    validate_quarantine_enrollment_safety,
)

def test_safe(mocker):
    c = mocker.Mock(spec=QuarantinedPaperCandidate)
    c.risk_flags = []
    c.allowed_for_active_paper = False
    c.allowed_for_broker_execution = False
    c.review_due_at_utc = None

    flags = collect_quarantine_safety_flags(c)
    assert not flags
    assert not quarantine_has_blocking_flags(flags)
    assert not validate_quarantine_enrollment_safety(c)

def test_unsafe(mocker):
    c = mocker.Mock(spec=QuarantinedPaperCandidate)
    c.risk_flags = []
    c.allowed_for_active_paper = True
    c.allowed_for_broker_execution = False
    c.review_due_at_utc = None

    flags = collect_quarantine_safety_flags(c)
    assert QuarantineSafetyFlag.AUTO_ENABLE_RISK in flags
    assert quarantine_has_blocking_flags(flags)
    assert validate_quarantine_enrollment_safety(c)
