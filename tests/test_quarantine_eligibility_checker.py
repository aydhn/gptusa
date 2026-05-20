import pytest
from usa_signal_bot.core.enums import QuarantineEnrollmentDecision, QuarantineCandidateStatus
from usa_signal_bot.paper_quarantine.eligibility_checker import (
    evaluate_quarantine_eligibility,
    candidate_status_from_enrollment_decision,
)

def test_clean_accepted():
    decision = evaluate_quarantine_eligibility({"decision": "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE", "score": 80.0})
    assert decision == QuarantineEnrollmentDecision.ENROLL_AS_QUARANTINED_CANDIDATE

def test_low_score():
    decision = evaluate_quarantine_eligibility({"decision": "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE", "score": 60.0})
    assert decision == QuarantineEnrollmentDecision.REQUEST_MANUAL_REVIEW

def test_missing_evidence():
    decision = evaluate_quarantine_eligibility({})
    assert decision == QuarantineEnrollmentDecision.REQUEST_MORE_SHADOW_DATA

def test_block_flag():
    decision = evaluate_quarantine_eligibility({"decision": "BLOCK"})
    assert decision == QuarantineEnrollmentDecision.BLOCK

def test_reject_decision():
    decision = evaluate_quarantine_eligibility({"decision": "REJECT"})
    assert decision == QuarantineEnrollmentDecision.REJECT

def test_status_mapping():
    assert candidate_status_from_enrollment_decision(QuarantineEnrollmentDecision.ENROLL_AS_QUARANTINED_CANDIDATE) == QuarantineCandidateStatus.ENROLLED
    assert candidate_status_from_enrollment_decision(QuarantineEnrollmentDecision.BLOCK) == QuarantineCandidateStatus.BLOCKED
