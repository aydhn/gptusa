import pytest
from usa_signal_bot.paper_quarantine.shadow_governance_ingestion import (
    ingest_shadow_governance_review,
    extract_shadow_governance_decision,
    extract_shadow_acceptance_score,
    extract_shadow_risk_flags,
    extract_shadow_required_followups,
    shadow_governance_supports_quarantine,
    shadow_governance_ingestion_to_text,
)

def test_ingest():
    p = ingest_shadow_governance_review({"decision": "ACCEPT"})
    assert p["decision"] == "ACCEPT"

def test_extract_decision():
    assert extract_shadow_governance_decision({"decision": "ACCEPT"}) == "ACCEPT"

def test_extract_score():
    assert extract_shadow_acceptance_score({"score": 80.0}) == 80.0

def test_extract_flags():
    assert extract_shadow_risk_flags({"risk_flags": ["high_risk"]}) == ["high_risk"]

def test_extract_followups():
    assert extract_shadow_required_followups({"required_followups": ["f1"]}) == ["f1"]

def test_supports_quarantine():
    supports, _ = shadow_governance_supports_quarantine({"decision": "ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE"})
    assert supports is True

    supports, _ = shadow_governance_supports_quarantine({"decision": "REJECT"})
    assert supports is False

def test_to_text():
    t = shadow_governance_ingestion_to_text({"decision": "ACCEPT", "score": 80.0, "risk_flags": []})
    assert "ACCEPT" in t
